#!/usr/bin/env python3
"""Build a cohort retention triangle from an activity CSV. Standard library only.

    python cohort_table.py events.csv --user user_id --date event_date --period month
    python cohort_table.py events.csv --user user_id --date event_date \
        --signup signup_date --period week --segment channel --out retention.csv

Each user's cohort is their signup date (if --signup is given) or their first event.
Cells are the share of the cohort active in that period; blank = not reached yet.
"""
import argparse
import csv
from collections import defaultdict
from datetime import date, datetime, timedelta


def parse(s):
    s = s.strip()[:19]
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(s if "%H" in fmt else s[:10], fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Unrecognized date: {s!r}")


def bucket(d, period):
    if period == "day":
        return d
    if period == "week":
        return d - timedelta(days=d.weekday())
    return date(d.year, d.month, 1)


def diff(a, b, period):
    if period == "day":
        return (b - a).days
    if period == "week":
        return (b - a).days // 7
    return (b.year - a.year) * 12 + (b.month - a.month)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--user", required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--signup")
    ap.add_argument("--segment")
    ap.add_argument("--period", choices=["day", "week", "month"], default="month")
    ap.add_argument("--max-periods", type=int, default=12)
    ap.add_argument("--out")
    a = ap.parse_args()

    start, seg, active = {}, {}, defaultdict(set)
    last = None
    with open(a.csv, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            u, d = row[a.user], parse(row[a.date])
            last = d if last is None or d > last else last
            s = parse(row[a.signup]) if a.signup and row.get(a.signup) else d
            if u not in start or s < start[u]:
                start[u] = s
            if a.segment:
                seg.setdefault(u, row.get(a.segment) or "(blank)")
            active[u].add(d)

    groups = defaultdict(lambda: defaultdict(set))  # (segment, cohort) -> period index -> users
    sizes = defaultdict(set)
    for u, s in start.items():
        key = (seg.get(u, "all"), bucket(s, a.period))
        sizes[key].add(u)
        for d in active[u]:
            k = diff(bucket(s, a.period), bucket(d, a.period), a.period)
            if 0 <= k <= a.max_periods:
                groups[key][k].add(u)

    lastb = bucket(last, a.period)
    rows = []
    for key in sorted(sizes):
        segname, coh = key
        n = len(sizes[key])
        reach = diff(coh, lastb, a.period)
        cells = [(len(groups[key][k]) / n if k <= reach else None) for k in range(a.max_periods + 1)]
        rows.append((segname, coh, n, cells))

    width = max((sum(c is not None for c in r[3]) for r in rows), default=1)
    p = a.period[0].upper()
    head = (["segment"] if a.segment else []) + ["cohort", "users"] + [f"{p}{k}" for k in range(width)]
    print("  ".join(f"{h:>7}" for h in head))
    for segname, coh, n, cells in rows:
        vals = ([segname[:7]] if a.segment else []) + [coh.isoformat()[:10 if a.period != "month" else 7], str(n)]
        vals += ["" if c is None else f"{c:.0%}" for c in cells[:width]]
        flag = "  (small)" if n < 100 else ""
        print("  ".join(f"{v:>7}" for v in vals) + flag)
    if a.out:
        with open(a.out, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(head)
            for segname, coh, n, cells in rows:
                w.writerow(([segname] if a.segment else []) + [coh.isoformat(), n] + ["" if c is None else round(c, 4) for c in cells[:width]])
        print(f"\nSaved {a.out}")


if __name__ == "__main__":
    main()
