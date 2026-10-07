#!/usr/bin/env python3
"""Build an evidence packet for a clinical trial from public sources. Standard library only.

    python fetch_trial.py NCT01234567                 # fetch from ClinicalTrials.gov + PubMed
    python fetch_trial.py NCT01234567 --json out.json # also save the packet as JSON
    python fetch_trial.py --file record.json          # parse a saved ClinicalTrials.gov v2 record
    python fetch_trial.py NCT01234567 --no-pubmed     # skip PubMed

Sources: ClinicalTrials.gov API v2 (https://clinicaltrials.gov/api/v2/studies/{id})
         NCBI E-utilities (esearch / efetch on PubMed)
Set NCBI_API_KEY in the environment for higher PubMed rate limits (optional).
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

CTGOV = "https://clinicaltrials.gov/api/v2/studies/"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
UA = {"User-Agent": "trial-failure-investigator/1.0 (Claude skill)"}
NCT_RE = re.compile(r"^NCT\d{8}$")


def get(url, retries=2):
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise
            if attempt == retries:
                raise
        except urllib.error.URLError:
            if attempt == retries:
                raise
        time.sleep(1.5 * (attempt + 1))


def parse_record(data):
    ps = data.get("protocolSection", {})
    idm, sm, dm = ps.get("identificationModule", {}), ps.get("statusModule", {}), ps.get("designModule", {})
    spon = ps.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {})
    elig = ps.get("eligibilityModule", {})
    locs = ps.get("contactsLocationsModule", {}).get("locations", []) or []
    rs = data.get("resultsSection", {}) or {}
    outcomes = rs.get("outcomeMeasuresModule", {}).get("outcomeMeasures", []) or []
    ae = rs.get("adverseEventsModule", {}) or {}
    refs = [r for r in ps.get("referencesModule", {}).get("references", []) or [] if r.get("pmid")]
    planned = [o for o in ps.get("outcomesModule", {}).get("primaryOutcomes", []) or []]
    d = lambda k: (sm.get(k) or {}).get("date")
    return {
        "nct_id": idm.get("nctId"),
        "title": idm.get("briefTitle") or idm.get("officialTitle"),
        "overall_status": sm.get("overallStatus"),
        "why_stopped": sm.get("whyStopped"),
        "phases": dm.get("phases", []),
        "study_type": dm.get("studyType"),
        "conditions": ps.get("conditionsModule", {}).get("conditions", []),
        "lead_sponsor": spon.get("name"),
        "sponsor_class": spon.get("class"),
        "start_date": d("startDateStruct"),
        "primary_completion_date": d("primaryCompletionDateStruct"),
        "completion_date": d("completionDateStruct"),
        "last_update": d("lastUpdatePostDateStruct"),
        "enrollment": dm.get("enrollmentInfo", {}).get("count"),
        "enrollment_type": dm.get("enrollmentInfo", {}).get("type"),
        "sites": len(locs),
        "countries": sorted({l.get("country") for l in locs if l.get("country")}),
        "eligibility": {k: elig.get(k) for k in ("minimumAge", "maximumAge", "sex", "healthyVolunteers")},
        "primary_outcomes_planned": [o.get("measure") for o in planned][:5],
        "has_results": bool(data.get("hasResults")),
        "results_outcomes": [f"{o.get('type', '')}: {o.get('title', '')}" for o in outcomes][:6],
        "serious_ae_types": len(ae.get("seriousEvents", []) or []),
        "other_ae_types": len(ae.get("otherEvents", []) or []),
        "registry_pmids": [r["pmid"] for r in refs],
        "brief_summary": (ps.get("descriptionModule", {}).get("briefSummary") or "")[:1500],
    }


def pubmed(nct, pmids):
    key = os.environ.get("NCBI_API_KEY")
    k = f"&api_key={key}" if key else ""
    try:
        q = urllib.parse.quote(f"{nct}[si] OR {nct}")
        found = json.loads(get(f"{EUTILS}esearch.fcgi?db=pubmed&retmode=json&retmax=5&term={q}{k}"))
        ids = list(dict.fromkeys(list(pmids) + found.get("esearchresult", {}).get("idlist", [])))[:6]
        if not ids:
            return []
        xml = get(f"{EUTILS}efetch.fcgi?db=pubmed&rettype=abstract&retmode=xml&id={','.join(ids)}{k}")
    except Exception as e:  # PubMed is optional; never fail the packet on it
        print(f"(PubMed lookup skipped: {e})", file=sys.stderr)
        return []
    out = []
    for art in re.findall(r"<PubmedArticle>(.*?)</PubmedArticle>", xml, re.S):
        pmid = re.search(r"<PMID[^>]*>(\d+)</PMID>", art)
        title = re.search(r"<ArticleTitle>(.*?)</ArticleTitle>", art, re.S)
        year = re.search(r"<PubDate>.*?<Year>(\d{4})</Year>", art, re.S)
        abstract = " ".join(re.sub(r"<[^>]+>", "", a) for a in re.findall(r"<AbstractText[^>]*>(.*?)</AbstractText>", art, re.S))
        out.append({
            "pmid": pmid.group(1) if pmid else None,
            "title": re.sub(r"<[^>]+>", "", title.group(1)) if title else "",
            "year": year.group(1) if year else None,
            "abstract": abstract[:1200],
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid.group(1)}/" if pmid else None,
        })
    return out


def show(p):
    line = lambda k, v: print(f"{k:<24}{v}")
    print(f"# Evidence packet: {p['nct_id']}\n{p['title']}\n")
    line("Status", p["overall_status"])
    line("whyStopped", f"\"{p['why_stopped']}\"" if p["why_stopped"] else "Not provided")
    line("Phase / type", f"{', '.join(p['phases']) or 'n/a'} / {p['study_type']}")
    line("Conditions", ", ".join(p["conditions"][:5]))
    line("Sponsor", f"{p['lead_sponsor']} ({p['sponsor_class']})")
    line("Start -> primary compl.", f"{p['start_date']} -> {p['primary_completion_date']}")
    line("Completion / updated", f"{p['completion_date']} / {p['last_update']}")
    line("Enrollment", f"{p['enrollment']} ({p['enrollment_type']})")
    line("Sites / countries", f"{p['sites']} / {', '.join(p['countries'][:8]) or 'n/a'}")
    line("Eligibility", ", ".join(f"{k}={v}" for k, v in p["eligibility"].items() if v is not None))
    line("Results posted", p["has_results"])
    if p["has_results"]:
        line("Adverse events", f"{p['serious_ae_types']} serious type(s), {p['other_ae_types']} other type(s)")
        for o in p["results_outcomes"]:
            print(f"{'':<24}- {o}")
    if p["primary_outcomes_planned"]:
        print("\nPlanned primary outcome(s):")
        for o in p["primary_outcomes_planned"]:
            print(f"  - {o}")
    if p.get("publications"):
        print("\nPublications:")
        for a in p["publications"]:
            print(f"  - {a['year']} {a['title']} ({a['url']})")
    print(f"\nRegistry: https://clinicaltrials.gov/study/{p['nct_id']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("nct_id", nargs="?")
    ap.add_argument("--file", help="parse a saved ClinicalTrials.gov v2 JSON record instead of fetching")
    ap.add_argument("--json", help="write the evidence packet to this JSON file")
    ap.add_argument("--no-pubmed", action="store_true")
    a = ap.parse_args()

    if a.file:
        data = json.load(open(a.file, encoding="utf-8"))
    else:
        nct = (a.nct_id or "").strip().upper()
        if not NCT_RE.match(nct):
            raise SystemExit("Give a valid NCT ID (NCT + 8 digits), or --file.")
        try:
            data = json.loads(get(CTGOV + nct))
        except urllib.error.HTTPError as e:
            raise SystemExit(f"{nct} not found on ClinicalTrials.gov" if e.code == 404 else f"ClinicalTrials.gov error {e.code}")
        except urllib.error.URLError as e:
            raise SystemExit(f"Couldn't reach ClinicalTrials.gov ({e.reason}). Save the record from the website and use --file.")

    packet = parse_record(data)
    packet["publications"] = [] if (a.no_pubmed or a.file) else pubmed(packet["nct_id"], packet["registry_pmids"])
    show(packet)
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(packet, f, indent=2)
        print(f"\nSaved {a.json}")


if __name__ == "__main__":
    main()
