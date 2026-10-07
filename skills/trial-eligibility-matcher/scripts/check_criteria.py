#!/usr/bin/env python3
"""Deterministic eligibility check: structured rules x structured patient facts. Standard library only.

    python check_criteria.py --criteria trial_rules.json --patient patient.json
    python check_criteria.py --criteria trial_rules.json --patient patient.json --as-of 2026-09-01 --json result.json
    python check_criteria.py --example        # write example input files to look at

Every rule must be satisfied for eligibility (write an exclusion as the condition that must
hold, e.g. "brain_mets == false"). Each rule evaluates to:
  met | not_met | unknown | review | invalid
and the trial to: likely eligible | near-eligible | not eligible.

Safety rules (same principles as the Agentic Clinical Trial Matching engine):
  * A Met needs a citation: the fact must carry a source quote of at least 8 characters,
    and the quote must actually contain the value (whole token: "22C3" is not 22,
    "Stage IV" is not stage I). A quote that doesn't contain the value sends the rule
    to review whether it would pass or fail, since a bad extraction can wrongly exclude too.
  * A malformed rule is reported as invalid, never silently treated as Not met.
  * Values dated after the as-of date are ignored, so results can be replayed for any date.
  * Two different values for a fact that shouldn't change (static facts) = conflict -> review.
  * Values older than a rule's time window are stale -> unknown.
  * Extraction confidence below 0.7 -> review.
"""
import argparse
import json
import re
import sys
from datetime import date

OPS = {">=", "<=", ">", "<", "==", "!=", "in", "not_in"}
NUMERIC_OPS = {">=", "<=", ">", "<", "==", "!="}
DEFAULT_STATIC = {"diagnosis", "histology", "pdl1", "egfr_mutation", "alk_fusion", "kras_g12c", "sex", "brain_mets"}
DEFAULT_TIMELESS = {"age", "sex"}
MIN_CITATION = 8
LOW_CONFIDENCE = 0.7

EXAMPLE_RULES = {
    "trial": {"id": "NCT00000000", "title": "Example: PD-1 inhibitor in PD-L1-high NSCLC"},
    "static_facts": sorted(DEFAULT_STATIC),
    "criteria": [
        {"id": "I1", "text": "Age 18 or older", "fact": "age", "op": ">=", "value": 18},
        {"id": "I2", "text": "Histologically confirmed NSCLC", "fact": "diagnosis", "op": "==", "value": "NSCLC"},
        {"id": "I3", "text": "Stage IIIB-IV disease", "fact": "stage", "op": "in", "value": ["IIIB", "IIIC", "IV", "IVA", "IVB"]},
        {"id": "I4", "text": "PD-L1 TPS of 50% or more", "fact": "pdl1", "op": ">=", "value": 50},
        {"id": "I5", "text": "ECOG 0-1 within 28 days", "fact": "ecog", "op": "<=", "value": 1, "window_days": 28,
         "unknown_step": "Document ECOG at the next visit"},
        {"id": "I6", "text": "ANC of 1500/uL or more within 14 days", "fact": "anc", "op": ">=", "value": 1500, "window_days": 14,
         "unknown_step": "Order a CBC with differential"},
        {"id": "E1", "text": "No untreated brain metastases", "fact": "brain_mets", "op": "==", "value": False,
         "unknown_step": "Review the latest brain MRI report"},
        {"id": "E2", "text": "No prior anti-PD-1/PD-L1 therapy", "fact": "prior_pd1", "op": "==", "value": False},
    ],
}
EXAMPLE_PATIENT = {
    "id": "SYN-001 (synthetic)",
    "as_of": "2026-09-15",
    "facts": [
        {"key": "age", "value": 64, "date": "2026-09-15", "quote": "64-year-old man with lung adenocarcinoma"},
        {"key": "diagnosis", "value": "NSCLC", "date": "2026-05-02", "quote": "Final diagnosis: NSCLC, adenocarcinoma", "source": "Pathology 2026-05-02"},
        {"key": "stage", "value": "IVA", "date": "2026-05-10", "quote": "Clinical stage IVA (cT2a N2 M1a)", "source": "Staging note"},
        {"key": "pdl1", "value": 22, "date": "2026-05-04", "quote": "PD-L1 IHC 22C3 pharmDx: TPS 80%", "source": "Pathology addendum", "confidence": 0.93},
        {"key": "ecog", "value": 1, "date": "2026-07-01", "quote": "ECOG performance status 1", "source": "Oncology note"},
        {"key": "brain_mets", "value": False, "date": "2026-05-12", "quote": "MRI brain: no evidence of intracranial metastatic disease"},
    ],
}


def ptype(v):
    if isinstance(v, bool):
        return "boolean"
    if isinstance(v, (int, float)):
        return "number"
    return "text"


def validate(rule):
    errs = []
    for k in ("id", "fact", "op"):
        if k not in rule:
            errs.append(f"missing '{k}'")
    if "value" not in rule:
        errs.append("missing 'value'")
    if errs:
        return errs
    op, v = rule["op"], rule["value"]
    if op not in OPS:
        errs.append(f"unknown operator '{op}'")
    elif op in ("in", "not_in"):
        if not isinstance(v, list) or not v:
            errs.append(f"'{op}' needs a non-empty list value")
    elif op in (">=", "<=", ">", "<") and ptype(v) != "number":
        errs.append(f"'{op}' needs a numeric value")
    if "window_days" in rule:
        w = rule["window_days"]
        if not isinstance(w, int) or isinstance(w, bool) or not 1 <= w <= 3650:
            errs.append("window_days must be a whole number from 1 to 3650")
        elif ptype(v) != "number":
            errs.append("window_days only applies to numeric measurements")
    return errs


def norm(v):
    return v.strip().lower() if isinstance(v, str) else v


def compare(op, actual, expected):
    if op in (">=", "<=", ">", "<"):
        if ptype(actual) != "number":
            return None
        return {">=": actual >= expected, "<=": actual <= expected, ">": actual > expected, "<": actual < expected}[op]
    if op in ("in", "not_in"):
        hit = norm(actual) in [norm(x) for x in expected]
        return hit if op == "in" else not hit
    same = norm(actual) == norm(expected)
    return same if op == "==" else not same


def quote_supports(value, quote):
    """Does the quoted source text actually contain this value as a whole token?"""
    if isinstance(value, bool):
        return True  # negations ("no evidence of ...") are judged by the reader, not by token search
    q = quote or ""
    if isinstance(value, (int, float)):
        num = re.escape(str(int(value)) if float(value).is_integer() else str(value))
        return re.search(rf"(?<![\w.]){num}(?:\.0+)?(?![\w.])", q) is not None
    return re.search(rf"(?<![A-Za-z0-9]){re.escape(str(value))}(?![A-Za-z0-9])", q, re.I) is not None


def days_between(a, b):
    return (date.fromisoformat(b) - date.fromisoformat(a)).days


def evaluate(rule, facts, as_of, static, timeless):
    out = {"id": rule.get("id"), "text": rule.get("text", ""), "rule": f"{rule.get('fact')} {rule.get('op')} {rule.get('value')}"
           + (f" within {rule['window_days']}d" if rule.get("window_days") else "")}
    errs = validate(rule)
    if errs:
        return {**out, "status": "invalid", "message": "Rule not evaluated: " + "; ".join(errs)}
    key = rule["fact"]
    mine = [f for f in facts if f.get("key") == key and (key in timeless or f.get("date", "9999-12-31") <= as_of)]
    mine.sort(key=lambda f: f.get("date", ""), reverse=True)
    if not mine:
        return {**out, "status": "unknown", "message": "No value found in the record.",
                "next_step": rule.get("unknown_step", f"Find or obtain a value for {key}")}
    if key in static and len({json.dumps(norm(f["value"])) for f in mine}) > 1:
        vals = " vs ".join(f"{f['value']} ({f.get('date')})" for f in mine)
        return {**out, "status": "review", "message": f"Conflicting sources: {vals}.",
                "next_step": "Clinician to adjudicate which source is correct", "evidence": mine}
    latest = mine[0]
    ev = {"evidence": [latest]}
    if rule.get("window_days") and key not in timeless:
        age = days_between(latest["date"], as_of)
        if not age <= rule["window_days"]:
            return {**out, **ev, "status": "unknown", "stale": True,
                    "message": f"Latest value is {age} days old; the criterion needs one within {rule['window_days']} days.",
                    "next_step": rule.get("unknown_step", f"Obtain a new {key} value")}
    if latest.get("confidence") is not None and latest["confidence"] < LOW_CONFIDENCE:
        return {**out, **ev, "status": "review", "message": f"Extraction confidence {latest['confidence']:.0%} is below {LOW_CONFIDENCE:.0%}. Verify against the source.",
                "next_step": "Verify the value against the source document"}
    ok = compare(rule["op"], latest["value"], rule["value"])
    if ok is None:
        return {**out, **ev, "status": "review", "message": f"Value '{latest['value']}' can't be compared with '{rule['op']}'."}
    quote = (latest.get("quote") or "").strip()
    if quote and not quote_supports(latest["value"], quote):
        # A wrong extraction can wrongly exclude a patient as easily as wrongly include one.
        return {**out, **ev, "status": "review",
                "message": f"The source quote doesn't contain the value {latest['value']!r} as a whole token. Check the extraction.",
                "next_step": "Verify the value against the source document"}
    if ok:
        if len(quote) < MIN_CITATION:
            return {**out, **ev, "status": "review", "message": "Would be Met, but the fact has no source quote. A Met needs a citation.",
                    "next_step": "Add the source text that states this value"}
        return {**out, **ev, "status": "met", "message": "Criterion satisfied."}
    return {**out, **ev, "status": "not_met", "message": "Criterion not satisfied."}


def run(rules, patient, as_of):
    static = set(rules.get("static_facts", DEFAULT_STATIC))
    timeless = set(rules.get("timeless_facts", DEFAULT_TIMELESS))
    results = [evaluate(r, patient.get("facts", []), as_of, static, timeless) for r in rules.get("criteria", [])]
    counts = {s: sum(r["status"] == s for r in results) for s in ("met", "not_met", "unknown", "review", "invalid")}
    if counts["not_met"]:
        state = "not eligible"
    elif counts["unknown"] or counts["review"] or counts["invalid"]:
        state = "near-eligible (needs follow-up)"
    else:
        state = "likely eligible (clinician to confirm)"
    evaluated = len(results) - counts["invalid"]
    return {"trial": rules.get("trial", {}), "patient": patient.get("id"), "as_of": as_of, "state": state,
            "fit": round(counts["met"] / evaluated, 2) if evaluated else 0.0, "counts": counts, "results": results}


ICON = {"met": "MET", "not_met": "NOT MET", "unknown": "UNKNOWN", "review": "REVIEW", "invalid": "INVALID"}


def show(r):
    t = r["trial"]
    print(f"# {t.get('id', '')} {t.get('title', '')}")
    print(f"Patient {r['patient']} · as of {r['as_of']}")
    print(f"Result: {r['state'].upper()} · fit {r['fit']:.0%} · " + ", ".join(f"{k} {v}" for k, v in r["counts"].items() if v))
    print()
    for x in r["results"]:
        print(f"[{ICON[x['status']]:<8}] {x['id']}: {x['text']}  ({x['rule']})")
        for e in x.get("evidence", [])[:1]:
            print(f"           value {e.get('value')!r} on {e.get('date')}: \"{(e.get('quote') or '')[:90]}\"")
        print(f"           {x['message']}")
        if x.get("next_step"):
            print(f"           Next step: {x['next_step']}")
    print("\nScreening support only. A clinician confirms eligibility.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--criteria", help="JSON file with trial rules")
    ap.add_argument("--patient", help="JSON file with patient facts (de-identified)")
    ap.add_argument("--as-of", help="evaluate as of this date (YYYY-MM-DD); default: patient's as_of or today")
    ap.add_argument("--json", help="save the full result as JSON")
    ap.add_argument("--example", action="store_true", help="write example_rules.json and example_patient.json")
    a = ap.parse_args()
    if a.example:
        json.dump(EXAMPLE_RULES, open("example_rules.json", "w"), indent=2)
        json.dump(EXAMPLE_PATIENT, open("example_patient.json", "w"), indent=2)
        print("Wrote example_rules.json and example_patient.json. Run:\n"
              "  python check_criteria.py --criteria example_rules.json --patient example_patient.json")
        return
    if not (a.criteria and a.patient):
        ap.error("--criteria and --patient are required (or use --example)")
    rules = json.load(open(a.criteria, encoding="utf-8"))
    patient = json.load(open(a.patient, encoding="utf-8"))
    as_of = a.as_of or patient.get("as_of") or date.today().isoformat()
    try:
        date.fromisoformat(as_of)
    except ValueError:
        sys.exit(f"Invalid as-of date: {as_of}")
    result = run(rules, patient, as_of)
    show(result)
    if a.json:
        json.dump(result, open(a.json, "w", encoding="utf-8"), indent=2, default=str)
        print(f"Saved {a.json}")


if __name__ == "__main__":
    main()
