#!/usr/bin/env python3
"""Fetch a trial's eligibility criteria from ClinicalTrials.gov (API v2). Standard library only.

    python fetch_criteria.py NCT01234567
    python fetch_criteria.py NCT01234567 --json trial.json   # save the trial details as JSON
    python fetch_criteria.py --file record.json              # parse a saved v2 study record

Prints the status, conditions, phase, age/sex limits, the full inclusion/exclusion text
split into numbered lines, and the recruiting sites.
"""
import argparse
import json
import re
import urllib.error
import urllib.request

API = "https://clinicaltrials.gov/api/v2/studies/"
NCT_RE = re.compile(r"^NCT\d{8}$")


def fetch(nct):
    req = urllib.request.Request(API + nct, headers={"User-Agent": "trial-eligibility-matcher/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def split_criteria(text):
    """Split the free-text criteria into inclusion and exclusion item lists."""
    inc, exc, cur = [], [], None
    for raw in (text or "").splitlines():
        line = raw.strip()
        if not line:
            continue
        low = line.lower().strip("*:# ")
        if low.startswith("inclusion"):
            cur = inc
            continue
        if low.startswith("exclusion"):
            cur = exc
            continue
        item = re.sub(r"^(\*|-|•|\d+[.)])\s*", "", line).replace("\\>", ">").replace("\\<", "<").replace("\\", "")
        (cur if cur is not None else inc).append(item)
    return inc, exc


def parse(data):
    ps = data.get("protocolSection", {})
    idm, sm, dm = ps.get("identificationModule", {}), ps.get("statusModule", {}), ps.get("designModule", {})
    el = ps.get("eligibilityModule", {})
    locs = ps.get("contactsLocationsModule", {}).get("locations", []) or []
    inc, exc = split_criteria(el.get("eligibilityCriteria"))
    return {
        "nct_id": idm.get("nctId"),
        "title": idm.get("briefTitle") or idm.get("officialTitle"),
        "status": sm.get("overallStatus"),
        "phases": dm.get("phases", []),
        "conditions": ps.get("conditionsModule", {}).get("conditions", []),
        "minimum_age": el.get("minimumAge"),
        "maximum_age": el.get("maximumAge"),
        "sex": el.get("sex"),
        "healthy_volunteers": el.get("healthyVolunteers"),
        "inclusion": inc,
        "exclusion": exc,
        "sites": [
            {"facility": l.get("facility"), "city": l.get("city"), "state": l.get("state"),
             "country": l.get("country"), "status": l.get("status")}
            for l in locs
        ],
        "url": f"https://clinicaltrials.gov/study/{idm.get('nctId')}",
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("nct_id", nargs="?")
    ap.add_argument("--file")
    ap.add_argument("--json")
    a = ap.parse_args()
    if a.file:
        data = json.load(open(a.file, encoding="utf-8"))
    else:
        nct = (a.nct_id or "").strip().upper()
        if not NCT_RE.match(nct):
            raise SystemExit("Give a valid NCT ID (NCT + 8 digits), or --file.")
        try:
            data = fetch(nct)
        except urllib.error.HTTPError as e:
            raise SystemExit(f"{nct} not found" if e.code == 404 else f"ClinicalTrials.gov error {e.code}")
        except urllib.error.URLError as e:
            raise SystemExit(f"Couldn't reach ClinicalTrials.gov ({e.reason}). Save the record and use --file.")
    t = parse(data)
    print(f"# {t['nct_id']}: {t['title']}")
    print(f"Status: {t['status']} · Phase: {', '.join(t['phases']) or 'n/a'} · Conditions: {', '.join(t['conditions'][:5])}")
    print(f"Age: {t['minimum_age'] or 'no min'} to {t['maximum_age'] or 'no max'} · Sex: {t['sex']} · Healthy volunteers: {t['healthy_volunteers']}\n")
    for label, items, pre in (("Inclusion criteria", t["inclusion"], "I"), ("Exclusion criteria", t["exclusion"], "E")):
        print(f"## {label}")
        for i, it in enumerate(items, 1):
            print(f"{pre}{i}. {it}")
        print()
    rec = [s for s in t["sites"] if (s["status"] or "").upper() in ("RECRUITING", "NOT_YET_RECRUITING", "")]
    print(f"## Sites ({len(t['sites'])} total, {len(rec)} recruiting or status not given)")
    for s in rec[:15]:
        print(f"- {s['facility']}, {s['city']}, {s['state'] or ''} {s['country']} [{s['status'] or 'n/a'}]")
    print(f"\n{t['url']}")
    if a.json:
        json.dump(t, open(a.json, "w", encoding="utf-8"), indent=2)
        print(f"Saved {a.json}")


if __name__ == "__main__":
    main()
