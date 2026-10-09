#!/usr/bin/env python3
"""Check claim labels and source lineage across strategy output files.

Checks:
  1. Every [FACT S#] / [ESTIMATE S#] tag cites source IDs that exist in the ledger.
  2. FACT and ESTIMATE tags without a source ID.
  3. Ledger rows missing required fields, and sources older than --max-age-days
     before --as-of (stale).
  4. Sentences with numbers ($, %, digits) but no label anywhere in the sentence
     (warnings). Tables, code blocks, handoff/source/appendix sections, and
     definition lines (Boundary, Decision question, Criteria, Weights, Script
     output, Scope, As-of) are skipped.
  5. Model output used as the source of a FACT.

Usage:
    python ledger_check.py strategy-output/ --ledger strategy-output/source-ledger.csv \
        [--as-of 2026-10-09] [--max-age-days 730] [--strict]

--strict turns unlabeled-number warnings into failures.
Standard library only.
"""
import argparse
import csv
import datetime as dt
import os
import re
import sys

TAG = re.compile(r"\[(FACT|ESTIMATE|INFERENCE|HYPOTHESIS|UNKNOWN)((?:\s+S\d+(?:\s*,\s*S\d+)*)?)\]", re.I)
SRC = re.compile(r"S\d+")
NUM = re.compile(r"(\$\s?\d|\d+(\.\d+)?\s?%|\b\d{2,}(,\d{3})*(\.\d+)?\b)")
REQUIRED = ("id", "title", "date", "location", "type", "trust")
SKIP_LINES = re.compile(r"^\s*(\*\*)?(Boundary|Decision question|Criteria|Weights|Script output|Scope|As-of)", re.I)
SKIP_HEADINGS = re.compile(r"^#{1,6}\s*(handoff|source|sources|ledger|appendix)", re.I)


def parse_date(s):
    for f in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            return dt.datetime.strptime(s.strip(), f).date()
        except ValueError:
            pass
    return None


def load_ledger(path, as_of, max_age, problems):
    rows = {}
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            sid = (r.get("id") or "").strip()
            if not sid:
                continue
            rows[sid] = r
            for f in REQUIRED:
                if not (r.get(f) or "").strip():
                    problems.append(("ledger", f"{sid}: missing '{f}'"))
            d = parse_date(r.get("as_of") or r.get("date") or "")
            if d and as_of and (as_of - d).days > max_age:
                problems.append(("stale", f"{sid}: dated {d}, older than {max_age} days before {as_of}"))
    return rows


def sentences(text):
    out, in_code = [], False
    for ln, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or line.strip().startswith("|") or not line.strip():
            continue
        for s in re.split(r"(?<=[.!?])\s+", line):
            out.append((ln, s))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--as-of")
    ap.add_argument("--max-age-days", type=int, default=730)
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    as_of = parse_date(a.as_of) if a.as_of else dt.date.today()

    problems = []
    ledger = load_ledger(a.ledger, as_of, a.max_age_days, problems)
    counts, used = {}, set()
    warnings = []

    files = sorted(f for f in os.listdir(a.folder) if f.endswith(".md") and f != "decision-log.md")
    for fn in files:
        text = open(os.path.join(a.folder, fn)).read()
        for ln, line in enumerate(text.splitlines(), 1):
            for m in TAG.finditer(line):
                label = m.group(1).upper()
                counts[label] = counts.get(label, 0) + 1
                ids = SRC.findall(m.group(2) or "")
                if label in ("FACT", "ESTIMATE") and not ids:
                    problems.append(("lineage", f"{fn}:{ln} [{label}] has no source ID"))
                for sid in ids:
                    used.add(sid)
                    if sid not in ledger:
                        problems.append(("lineage", f"{fn}:{ln} cites {sid}, which is not in the ledger"))
                    elif label == "FACT" and (ledger[sid].get("type") or "").strip().lower() == "model-output":
                        problems.append(("lineage", f"{fn}:{ln} FACT cites {sid}, a model-output source"))
        # unlabeled numbers (skip handoff, source and appendix sections)
        lines = text.splitlines()
        heading_at = {}
        cur = False
        for i, line in enumerate(lines, 1):
            if line.startswith("#"):
                cur = bool(SKIP_HEADINGS.match(line))
            heading_at[i] = cur
        for ln, s in sentences(text):
            if heading_at.get(ln) or s.lstrip().startswith("#") or SKIP_LINES.match(lines[ln - 1]):
                continue
            if NUM.search(s) and not TAG.search(s) and "[OPEN]" not in s and "[UNSOURCED]" not in s:
                warnings.append(f"{fn}:{ln} number without a label: {s.strip()[:90]}")

    unused = sorted(set(ledger) - used)
    print(f"Files checked: {len(files)} · ledger sources: {len(ledger)} · as of {as_of}")
    print("Labels: " + (", ".join(f"{k} {v}" for k, v in sorted(counts.items())) or "none found"))
    if unused:
        print(f"Ledger sources never cited: {', '.join(unused)}")
    for kind in ("lineage", "ledger", "stale"):
        items = [p for k, p in problems if k == kind]
        if items:
            print(f"\n{kind.upper()} ({len(items)}):")
            for p in items:
                print(f"  - {p}")
    if warnings:
        print(f"\nUNLABELED NUMBERS ({len(warnings)}):")
        for w in warnings[:40]:
            print(f"  - {w}")
        if len(warnings) > 40:
            print(f"  ... and {len(warnings) - 40} more")

    fail = [p for k, p in problems if k in ("lineage", "ledger")]
    print()
    if fail or (a.strict and warnings):
        print("RESULT: FAIL")
        sys.exit(1)
    if warnings or any(k == "stale" for k, _ in problems):
        print("RESULT: PASS WITH WARNINGS")
    else:
        print("RESULT: PASS")


if __name__ == "__main__":
    main()
