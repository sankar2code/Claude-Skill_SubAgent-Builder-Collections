#!/usr/bin/env python3
"""Check a canvas.json for traceability and evidence, and trace why any item exists.

Checks:
  - IDs are unique and every reference points to an existing item
  - Orphans: evidence without a source, needs without evidence, opportunities
    without needs, bets without opportunities, initiatives without a bet,
    KPIs without a parent (except the north star)
  - Gaps: high-importance needs (>= --need-threshold) that no opportunity covers,
    opportunities no bet covers, bets with no success metric or kill criteria,
    bets with no initiative
  - Evidence: FACT / ESTIMATE items must cite a source; each bet's weakest
    supporting evidence is reported
  - KPIs: baseline missing or [UNKNOWN]; no guardrail or counter metric

Usage:
    python canvas_check.py canvas.json
    python canvas_check.py canvas.json --why I2      # trace an item back to its evidence
Standard library only.
"""
import argparse
import json
import sys

STRENGTH = {"strong": 3, "moderate": 2, "weak": 1, "assumed": 0}


def load(path):
    c = json.load(open(path))
    for k in ("sources", "evidence", "needs", "goals", "opportunities", "choices", "bets", "initiatives", "kpis", "scorecard"):
        c.setdefault(k, [])
    return c


def index(c):
    idx = {}
    dup = []
    for k in ("sources", "evidence", "needs", "goals", "opportunities", "choices", "bets", "initiatives", "kpis"):
        for it in c[k]:
            if it["id"] in idx:
                dup.append(it["id"])
            idx[it["id"]] = (k, it)
    return idx, dup


def parents(kind, it):
    """Upstream links for an item."""
    if kind == "evidence":
        return [it.get("source")] if it.get("source") else []
    if kind == "needs":
        return it.get("evidence", [])
    if kind == "opportunities":
        return it.get("needs", []) + ([it["goal"]] if it.get("goal") else [])
    if kind == "bets":
        return it.get("opportunities", [])
    if kind == "initiatives":
        return [it["bet"]] if it.get("bet") else []
    if kind == "kpis":
        return [it["parent"]] if it.get("parent") else []
    if kind == "goals":
        return []
    return []


def why(c, idx, target, depth=0, seen=None):
    seen = seen or set()
    if target not in idx or target in seen:
        print("  " * depth + f"{target} (missing)")
        return
    seen.add(target)
    kind, it = idx[target]
    text = it.get("text") or it.get("title") or it.get("name") or it.get("we_will", "")
    extra = ""
    if kind == "evidence":
        extra = f" [{it.get('label','?')} {it.get('source','')} · {it.get('strength','?')}]"
    single = {"sources": "source", "evidence": "evidence", "needs": "need", "goals": "goal", "opportunities": "opportunity",
              "choices": "choice", "bets": "bet", "initiatives": "initiative", "kpis": "KPI"}[kind]
    print("  " * depth + f"{target} ({single}): {text}{extra}")
    for p in parents(kind, it):
        if p and not (kind == "opportunities" and p.startswith("G")):
            why(c, idx, p, depth + 1, seen)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--why", help="trace an item (for example I2 or B1) back to its evidence")
    ap.add_argument("--need-threshold", type=float, default=8)
    a = ap.parse_args()
    c = load(a.file)
    idx, dup = index(c)

    if a.why:
        print(f"Why does {a.why} exist?\n")
        why(c, idx, a.why)
        if a.why in idx and idx[a.why][0] in ("initiatives", "bets"):
            kind, it = idx[a.why]
            bet = it if kind == "bets" else idx.get(it.get("bet"), (None, {}))[1]
            if bet:
                print(f"\nSuccess metric: {bet.get('success_metric','(none)')} · kill criteria: {bet.get('kill_criteria','(none)')}")
        return

    errors, gaps, warns = [], [], []
    for d in dup:
        errors.append(f"duplicate id {d}")
    for kind in ("evidence", "needs", "opportunities", "bets", "initiatives", "kpis"):
        for it in c[kind]:
            for p in parents(kind, it) + it.get("depends_on", []):
                if p and p not in idx:
                    errors.append(f"{it['id']} references {p}, which does not exist")

    # orphans
    for e in c["evidence"]:
        if not e.get("source"):
            gaps.append(f"{e['id']} evidence has no source")
        if e.get("label", "").upper() in ("FACT", "ESTIMATE") and not e.get("source"):
            errors.append(f"{e['id']} is {e['label']} without a source")
    for n in c["needs"]:
        if not n.get("evidence"):
            gaps.append(f"{n['id']} need has no evidence ([HYPOTHESIS] at best)")
    for o in c["opportunities"]:
        if not o.get("needs"):
            gaps.append(f"{o['id']} opportunity is not linked to any need")
    for b in c["bets"]:
        if not b.get("opportunities"):
            gaps.append(f"{b['id']} bet is not linked to an opportunity")
        if not b.get("success_metric"):
            gaps.append(f"{b['id']} bet has no success metric")
        if not b.get("kill_criteria"):
            gaps.append(f"{b['id']} bet has no kill criteria")
    for i in c["initiatives"]:
        if not i.get("bet"):
            gaps.append(f"{i['id']} initiative is not linked to a bet (why is it on the roadmap?)")
    for k in c["kpis"]:
        if k.get("type") != "north_star" and not k.get("parent"):
            gaps.append(f"{k['id']} KPI has no parent in the tree")
        if not k.get("baseline") or "UNKNOWN" in str(k.get("baseline")):
            warns.append(f"{k['id']} {k.get('name','')}: no baseline yet")

    # coverage
    covered_needs = {n for o in c["opportunities"] for n in o.get("needs", [])}
    for n in c["needs"]:
        if float(n.get("importance", 0)) >= a.need_threshold and n["id"] not in covered_needs:
            gaps.append(f"{n['id']} is a top need (importance {n.get('importance')}) but no opportunity addresses it")
    covered_ops = {o for b in c["bets"] for o in b.get("opportunities", [])}
    for o in c["opportunities"]:
        if o["id"] not in covered_ops:
            warns.append(f"{o['id']} opportunity has no bet yet")
    bets_with_work = {i.get("bet") for i in c["initiatives"]}
    for b in c["bets"]:
        if b["id"] not in bets_with_work:
            warns.append(f"{b['id']} bet has no initiative on the roadmap")
    used_ev = {e for n in c["needs"] for e in n.get("evidence", [])}
    for e in c["evidence"]:
        if e["id"] not in used_ev:
            warns.append(f"{e['id']} evidence is not used by any need")
    for n in c["needs"]:
        if float(n.get("importance", 0)) < a.need_threshold and n["id"] not in covered_needs:
            warns.append(f"{n['id']} need (importance {n.get('importance')}) is not addressed; say if that is a deliberate choice")
    types = {k.get("type") for k in c["kpis"]}
    if c["kpis"] and not types & {"guardrail", "counter"}:
        warns.append("KPI tree has no guardrail or counter metric")
    if not c["choices"]:
        warns.append("no explicit choices (we will / we won't)")

    # weakest evidence per bet
    print(f"Canvas: {c.get('meta', {}).get('product', '')} · as of {c.get('meta', {}).get('as_of', '')}")
    counts = {k: len(c[k]) for k in ("evidence", "needs", "opportunities", "bets", "initiatives", "kpis")}
    print("Items: " + ", ".join(f"{k} {v}" for k, v in counts.items()))
    print("\n== Evidence behind each bet ==")
    for b in c["bets"]:
        ev = set()
        for o in b.get("opportunities", []):
            for n in idx.get(o, (None, {}))[1].get("needs", []):
                ev.update(idx.get(n, (None, {}))[1].get("evidence", []))
        levels = [idx[e][1].get("strength", "assumed") for e in ev if e in idx]
        if levels:
            best = max(levels, key=lambda s: STRENGTH.get(s, 0))
            print(f"  {b['id']} {b.get('title','')}: {len(ev)} evidence items, strongest '{best}'"
                  f"{'  ⚠ no strong evidence' if best not in ('strong',) else ''}")
        else:
            print(f"  {b['id']} {b.get('title','')}: no linked evidence  ⚠")
            gaps.append(f"{b['id']} bet has no evidence chain")

    for title, items in (("ERRORS", errors), ("TRACEABILITY GAPS", gaps), ("WARNINGS", warns)):
        if items:
            print(f"\n{title} ({len(items)}):")
            for x in items:
                print(f"  - {x}")
    print()
    if errors:
        print("RESULT: FAIL")
        sys.exit(1)
    print("RESULT: " + ("PASS WITH GAPS" if gaps else "PASS WITH WARNINGS" if warns else "PASS"))


if __name__ == "__main__":
    main()
