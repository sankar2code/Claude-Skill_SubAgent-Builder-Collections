#!/usr/bin/env python3
"""Reconcile top-down and bottom-up market size estimates.

Each method is a chain of drivers multiplied together. Every driver has a
low / base / high value and a label (FACT, ESTIMATE, INFERENCE, HYPOTHESIS)
with an optional source ID. The script multiplies each chain, compares the
methods, and flags gaps and unlabeled drivers.

Usage:
    python market_size.py market-size.json [--tolerance 0.25]

Input format: see assets/templates/market-size.json
Standard library only.
"""
import argparse
import json
import sys

LABELS = {"FACT", "ESTIMATE", "INFERENCE", "HYPOTHESIS", "UNKNOWN"}
CASES = ("low", "base", "high")


def chain_value(drivers):
    out = {c: 1.0 for c in CASES}
    for d in drivers:
        for c in CASES:
            out[c] *= float(d[c])
    return out


def fmt(x, unit=""):
    if abs(x) >= 1e9:
        s = f"{x/1e9:,.2f}B"
    elif abs(x) >= 1e6:
        s = f"{x/1e6:,.2f}M"
    elif abs(x) >= 1e3:
        s = f"{x/1e3:,.1f}K"
    else:
        s = f"{x:,.2f}"
    return f"{s} {unit}".strip()


def check_driver(name, d, problems):
    for c in CASES:
        if c not in d:
            problems.append(f"{name}: missing '{c}' value")
    if not all(c in d for c in CASES):
        return
    if not (float(d["low"]) <= float(d["base"]) <= float(d["high"])):
        problems.append(f"{name}: expected low <= base <= high")
    label = str(d.get("label", "")).upper()
    if label not in LABELS:
        problems.append(f"{name}: missing or invalid label (use one of {sorted(LABELS)})")
    if label in {"FACT", "ESTIMATE"} and not d.get("source"):
        problems.append(f"{name}: {label} needs a source ID")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--tolerance", type=float, default=0.25,
                    help="max allowed gap between method base cases (default 0.25 = 25%%)")
    a = ap.parse_args()
    spec = json.load(open(a.file))
    unit = spec.get("unit", "")
    methods = spec.get("methods", {})
    if len(methods) < 2:
        print("BLOCKER: need at least two independent methods (for example top_down and bottom_up).")
        sys.exit(2)

    problems, results = [], {}
    print(f"Market: {spec.get('boundary', '(boundary not stated)')}")
    print(f"Unit: {unit or '(not stated)'}  Period: {spec.get('period', '(not stated)')}\n")
    if not spec.get("boundary"):
        problems.append("boundary is not stated")

    for m, drivers in methods.items():
        print(f"== {m} ==")
        for d in drivers:
            name = f"{m}.{d.get('name', '?')}"
            check_driver(name, d, problems)
            print(f"  x {d.get('name','?'):<40} low {d.get('low')!s:>12}  base {d.get('base')!s:>12}  high {d.get('high')!s:>12}  [{d.get('label','?')}{' ' + d['source'] if d.get('source') else ''}]")
        try:
            v = chain_value(drivers)
        except (KeyError, ValueError):
            print("  (cannot compute: fix driver values)\n")
            continue
        results[m] = v
        print(f"  = low {fmt(v['low'], unit)} | base {fmt(v['base'], unit)} | high {fmt(v['high'], unit)}\n")

    if len(results) >= 2:
        names = list(results)
        bases = [results[n]["base"] for n in names]
        lo, hi = min(bases), max(bases)
        gap = (hi - lo) / hi if hi else 0
        print("== Reconciliation ==")
        print(f"  Base cases: " + ", ".join(f"{n} {fmt(results[n]['base'], unit)}" for n in names))
        print(f"  Gap between base cases: {gap:.0%} (tolerance {a.tolerance:.0%})")
        overlap_lo = max(results[n]["low"] for n in names)
        overlap_hi = min(results[n]["high"] for n in names)
        if overlap_lo <= overlap_hi:
            print(f"  Ranges overlap: {fmt(overlap_lo, unit)} to {fmt(overlap_hi, unit)}")
        else:
            print("  Ranges do NOT overlap")
            problems.append("method ranges do not overlap")
        if gap > a.tolerance:
            problems.append(f"base-case gap {gap:.0%} exceeds tolerance; find the driver that explains it")
        blended = sum(bases) / len(bases)
        print(f"  Simple average of base cases (for reference only): {fmt(blended, unit)}")
        # driver swing: which single driver moves each chain most
        print("\n== Biggest swing drivers (high/low ratio) ==")
        for m, drivers in methods.items():
            try:
                swings = sorted(((float(d['high']) / float(d['low']) if float(d['low']) else float('inf'), d.get('name', '?')) for d in drivers), reverse=True)
                print(f"  {m}: " + ", ".join(f"{n} ({s:.1f}x)" for s, n in swings[:3]))
            except (KeyError, ValueError):
                pass

    print()
    if problems:
        print("RESULT: NOT RECONCILED")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print("RESULT: RECONCILED within tolerance")


if __name__ == "__main__":
    main()
