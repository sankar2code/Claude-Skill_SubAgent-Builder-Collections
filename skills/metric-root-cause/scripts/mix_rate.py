#!/usr/bin/env python3
"""Split the change in a rate metric into mix and rate effects by segment.

Input: a CSV with one row per (period, segment) or raw rows to aggregate, holding a
numerator and a denominator column. Uses only the Python standard library.

    python mix_rate.py data.csv --segment platform --period month \
        --num activated --den signups --p0 2026-08 --p1 2026-09

total change = sum((w1 - w0) * r0)   # mix effect
             + sum(w1 * (r1 - r0))   # rate effect
"""
import argparse
import csv
from collections import defaultdict


def load(path, seg, per, num, den):
    agg = defaultdict(lambda: [0.0, 0.0])
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            key = (row[per].strip(), row[seg].strip() or "(blank)")
            agg[key][0] += float(row[num] or 0)
            agg[key][1] += float(row[den] or 0)
    return agg


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--segment", required=True)
    ap.add_argument("--period", required=True)
    ap.add_argument("--num", required=True, help="numerator column (e.g. conversions)")
    ap.add_argument("--den", required=True, help="denominator column (e.g. users)")
    ap.add_argument("--p0", required=True, help="baseline period value")
    ap.add_argument("--p1", required=True, help="comparison period value")
    a = ap.parse_args()

    agg = load(a.csv, a.segment, a.period, a.num, a.den)
    segs = sorted({s for (p, s) in agg if p in (a.p0, a.p1)})
    tot = {p: sum(agg[(p, s)][1] for s in segs) for p in (a.p0, a.p1)}
    if not tot[a.p0] or not tot[a.p1]:
        raise SystemExit("No data for one of the periods; check --p0/--p1 values.")

    def rate(p):
        return sum(agg[(p, s)][0] for s in segs) / tot[p]

    rows, mix_sum, rate_sum = [], 0.0, 0.0
    for s in segs:
        n0, d0 = agg[(a.p0, s)]
        n1, d1 = agg[(a.p1, s)]
        w0, w1 = d0 / tot[a.p0], d1 / tot[a.p1]
        r0 = n0 / d0 if d0 else 0.0
        r1 = n1 / d1 if d1 else r0
        mix, rt = (w1 - w0) * r0, w1 * (r1 - r0)
        mix_sum += mix
        rate_sum += rt
        rows.append((s, w0, w1, r0, r1, mix, rt, d0, d1))

    total = rate(a.p1) - rate(a.p0)
    print(f"Overall rate: {rate(a.p0):.4f} -> {rate(a.p1):.4f}  (change {total:+.4f})")
    print(f"Mix effect {mix_sum:+.4f} | Rate effect {rate_sum:+.4f} | check {mix_sum + rate_sum - total:+.1e}\n")
    hdr = f"{'segment':<20}{'share0':>8}{'share1':>8}{'rate0':>8}{'rate1':>8}{'mix':>9}{'rate eff':>9}{'% of Δ':>8}{'n1':>9}"
    print(hdr)
    print("-" * len(hdr))
    for s, w0, w1, r0, r1, mix, rt, d0, d1 in sorted(rows, key=lambda r: -abs(r[5] + r[6])):
        share = (mix + rt) / total * 100 if total else 0.0
        flag = "  (small n)" if d1 < 100 else ""
        print(f"{s[:19]:<20}{w0:>8.1%}{w1:>8.1%}{r0:>8.1%}{r1:>8.1%}{mix:>+9.4f}{rt:>+9.4f}{share:>7.0f}%{int(d1):>9}{flag}")


if __name__ == "__main__":
    main()
