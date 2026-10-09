#!/usr/bin/env python3
"""Score initiatives with RICE, ICE or WSJF, and test how stable the ranking is.

Reads initiatives from canvas.json (or a CSV with the same field names).

  RICE = reach x impact x confidence / effort
         impact: 0.25 minimal, 0.5 low, 1 medium, 2 high, 3 massive
         confidence: 0-1 (1.0 high, 0.8 medium, 0.5 low)
  ICE  = impact x confidence x ease          (each 1-10; confidence may be 0-1)
  WSJF = (business_value + time_criticality + risk_reduction) / job_size

Stability: every input is jittered by +/- --jitter (default 25%) over --runs
random trials (fixed seed). The report shows how often each item stays in the
top N. Items ranked high mainly because of low-confidence inputs are flagged.

Usage:
    python prioritize.py canvas.json [--method rice|ice|wsjf] [--top 3] [--write]
    python prioritize.py initiatives.csv --method wsjf
--write stores score and rank back into canvas.json.
Standard library only.
"""
import argparse
import csv
import json
import random
import sys

FIELDS = {"rice": ("reach", "impact", "confidence", "effort"),
          "ice": ("impact", "confidence", "ease"),
          "wsjf": ("business_value", "time_criticality", "risk_reduction", "job_size")}


def score(m, d):
    if m == "rice":
        return d["reach"] * d["impact"] * d["confidence"] / d["effort"]
    if m == "ice":
        conf = d["confidence"] * 10 if d["confidence"] <= 1 else d["confidence"]
        return d["impact"] * conf * d["ease"]
    return (d["business_value"] + d["time_criticality"] + d["risk_reduction"]) / d["job_size"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--method", choices=FIELDS)
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--jitter", type=float, default=0.25)
    ap.add_argument("--runs", type=int, default=1000)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    canvas = None
    if a.file.endswith(".json"):
        canvas = json.load(open(a.file))
        items = canvas.get("initiatives", [])
        method = a.method or canvas.get("meta", {}).get("prioritization", "rice")
    else:
        items = list(csv.DictReader(open(a.file)))
        method = a.method or "rice"
    need = FIELDS[method]
    rows, skipped = [], []
    for it in items:
        try:
            d = {k: float(it[k]) for k in need}
        except (KeyError, ValueError, TypeError):
            skipped.append(it.get("id", it.get("title", "?")))
            continue
        if (method == "rice" and d["effort"] <= 0) or (method == "wsjf" and d["job_size"] <= 0):
            skipped.append(it.get("id", "?"))
            continue
        rows.append((it, d))
    if not rows:
        print(f"No initiatives have all {method.upper()} fields: {', '.join(need)}")
        sys.exit(2)

    base = sorted(((score(method, d), it, d) for it, d in rows), key=lambda x: -x[0])
    rng = random.Random(42)
    top_hits = {id(it): 0 for it, _ in rows}
    for _ in range(a.runs):
        trial = []
        for it, d in rows:
            j = {k: v * (1 + rng.uniform(-a.jitter, a.jitter)) for k, v in d.items()}
            if "confidence" in j and j["confidence"] <= 1.2 and d["confidence"] <= 1:
                j["confidence"] = min(1.0, j["confidence"])
            trial.append((score(method, j), id(it)))
        trial.sort(reverse=True)
        for _, iid in trial[: a.top]:
            top_hits[iid] += 1

    print(f"Method: {method.upper()} = " + {"rice": "reach x impact x confidence / effort",
                                           "ice": "impact x confidence x ease",
                                           "wsjf": "(value + time criticality + risk reduction) / job size"}[method])
    print(f"Stability: inputs jittered +/-{a.jitter:.0%} over {a.runs} runs; share of runs in top {a.top}\n")
    print(f"  {'#':<3}{'ID':<5}{'Initiative':<42}{'Score':>9}  {'Top-' + str(a.top):>7}  Notes")
    flags = []
    for r, (s, it, d) in enumerate(base, 1):
        stab = top_hits[id(it)] / a.runs
        notes = []
        conf = d.get("confidence")
        if conf is not None and conf <= (0.5 if conf <= 1 else 5) and r <= a.top:
            notes.append("low confidence")
            flags.append(f"{it.get('id','?')} is top {a.top} but confidence is low: validate before committing")
        if r <= a.top and stab < 0.6:
            notes.append("unstable")
        if r > a.top and stab >= 0.4:
            notes.append("close contender")
        rank_of = {str(x.get("id")): k for k, (_, x, _) in enumerate(base, 1)}
        later = [dep for dep in it.get("depends_on", []) or [] if rank_of.get(dep, 0) > r]
        if later:
            notes.append("needs " + ", ".join(later) + " first")
        print(f"  {r:<3}{str(it.get('id','')):<5}{str(it.get('title',''))[:41]:<42}{s:9.1f}  {stab:7.0%}  {', '.join(notes)}")
        it["score"] = round(s, 2)
        it["rank"] = r
    if skipped:
        print(f"\nSkipped (missing {method.upper()} fields): {', '.join(map(str, skipped))}")
    if flags:
        print("\nFLAGS:")
        for f in flags:
            print(f"  - {f}")
    if a.write and canvas is not None:
        canvas.setdefault("meta", {})["prioritization"] = method
        json.dump(canvas, open(a.file, "w"), indent=2, ensure_ascii=False)
        print(f"\nWrote score and rank into {a.file}")
    print("\nRESULT: ranked. Scores rank options; the team still decides.")


if __name__ == "__main__":
    main()
