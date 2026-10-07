#!/usr/bin/env python3
"""Search ClinicalTrials.gov (API v2) for trials a patient might fit. Standard library only.

    python search_trials.py --condition "non-small cell lung cancer" --location "Boston, MA"
    python search_trials.py --condition NSCLC --term "PD-L1" --phase 2 3 --limit 20
    python search_trials.py --file search_response.json    # parse a saved API response

Defaults to trials that are RECRUITING or NOT_YET_RECRUITING. This is a first-pass
list: every candidate still needs a criterion-by-criterion check.
"""
import argparse
import json
import urllib.error
import urllib.parse
import urllib.request

API = "https://clinicaltrials.gov/api/v2/studies"


def build_url(a):
    q = {"pageSize": str(min(max(a.limit, 1), 100)), "format": "json",
         "filter.overallStatus": ",".join(a.status)}
    if a.condition:
        q["query.cond"] = a.condition
    if a.term:
        q["query.term"] = a.term
    if a.location:
        q["query.locn"] = a.location
    if a.phase:
        q["filter.advanced"] = "AREA[Phase](" + " OR ".join(f"PHASE{p}" for p in a.phase) + ")"
    return API + "?" + urllib.parse.urlencode(q)


def summarize(study, location_hint):
    ps = study.get("protocolSection", {})
    idm, sm, dm = ps.get("identificationModule", {}), ps.get("statusModule", {}), ps.get("designModule", {})
    el = ps.get("eligibilityModule", {})
    locs = ps.get("contactsLocationsModule", {}).get("locations", []) or []
    hint = (location_hint or "").lower().split(",")[0].strip()
    near = [l for l in locs if hint and hint in " ".join(str(l.get(k, "")) for k in ("city", "state", "country")).lower()]
    return {
        "nct_id": idm.get("nctId"),
        "title": idm.get("briefTitle"),
        "status": sm.get("overallStatus"),
        "phases": dm.get("phases", []),
        "conditions": ps.get("conditionsModule", {}).get("conditions", [])[:3],
        "age": f"{el.get('minimumAge') or 'no min'}–{el.get('maximumAge') or 'no max'}",
        "sex": el.get("sex"),
        "enrollment": dm.get("enrollmentInfo", {}).get("count"),
        "sponsor": ps.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}).get("name"),
        "sites_total": len(locs),
        "sites_matching_location": len(near),
        "example_site": (near or locs or [{}])[0].get("city"),
        "url": f"https://clinicaltrials.gov/study/{idm.get('nctId')}",
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--condition", help='disease or condition, e.g. "NSCLC"')
    ap.add_argument("--term", help="other keywords, e.g. a biomarker or drug class")
    ap.add_argument("--location", help='city, state or country, e.g. "Boston, MA"')
    ap.add_argument("--phase", nargs="*", choices=["1", "2", "3", "4"], help="phases to include")
    ap.add_argument("--status", nargs="*", default=["RECRUITING", "NOT_YET_RECRUITING"])
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--file", help="parse a saved API search response instead of calling the API")
    ap.add_argument("--json", help="save the candidate list as JSON")
    a = ap.parse_args()

    if a.file:
        data = json.load(open(a.file, encoding="utf-8"))
    else:
        if not (a.condition or a.term):
            raise SystemExit("Give at least --condition or --term.")
        url = build_url(a)
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "trial-eligibility-matcher/1.0"}), timeout=30) as r:
                data = json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            raise SystemExit(f"ClinicalTrials.gov error {e.code}: {url}")
        except urllib.error.URLError as e:
            raise SystemExit(f"Couldn't reach ClinicalTrials.gov ({e.reason}). Run the search on the website and use --file.")

    rows = [summarize(s, a.location) for s in data.get("studies", [])]
    if a.location:
        rows.sort(key=lambda r: -r["sites_matching_location"])
    print(f"{len(rows)} candidate trial(s)\n")
    for r in rows:
        loc = f" · {r['sites_matching_location']} site(s) near {a.location}" if a.location else ""
        print(f"{r['nct_id']}  [{r['status']}, {', '.join(r['phases']) or 'n/a'}]  {r['title']}")
        print(f"    {', '.join(r['conditions'])} · age {r['age']} · sex {r['sex']} · {r['sites_total']} sites{loc} · {r['sponsor'] or 'sponsor n/a'}")
        print(f"    {r['url']}")
    if a.json:
        json.dump(rows, open(a.json, "w", encoding="utf-8"), indent=2)
        print(f"\nSaved {a.json}")


if __name__ == "__main__":
    main()
