#!/usr/bin/env python3
"""Sample size and duration for a two-group A/B test. Standard library only.

Conversion metric (baseline rate + relative or absolute MDE):
    python sample_size.py --baseline 0.12 --mde-rel 0.05 --daily-users 8000

Mean metric (mean, standard deviation, absolute MDE):
    python sample_size.py --mean 42 --sd 30 --mde-abs 1.5 --daily-users 8000

Options: --alpha (default 0.05, two-sided), --power (default 0.8),
         --split (share of traffic in the test, default 1.0 = all eligible users).
"""
import argparse
import math
from statistics import NormalDist


def z(p):
    return NormalDist().inv_cdf(p)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--baseline", type=float, help="baseline conversion rate, e.g. 0.12")
    ap.add_argument("--mean", type=float, help="baseline mean for a continuous metric")
    ap.add_argument("--sd", type=float, help="standard deviation for a continuous metric")
    ap.add_argument("--mde-rel", type=float, help="relative MDE, e.g. 0.05 for +5%%")
    ap.add_argument("--mde-abs", type=float, help="absolute MDE, e.g. 0.006 or 1.5")
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--power", type=float, default=0.8)
    ap.add_argument("--daily-users", type=float, help="eligible users per day (both groups)")
    ap.add_argument("--split", type=float, default=1.0, help="share of eligible traffic in the test")
    a = ap.parse_args()

    zz = (z(1 - a.alpha / 2) + z(a.power)) ** 2
    if a.baseline is not None:
        p1 = a.baseline
        if a.mde_abs is not None:
            p2 = p1 + a.mde_abs
        elif a.mde_rel is not None:
            p2 = p1 * (1 + a.mde_rel)
        else:
            raise SystemExit("Give --mde-rel or --mde-abs")
        if not 0 < p2 < 1:
            raise SystemExit("Treatment rate falls outside 0-1; check the MDE.")
        n = zz * (p1 * (1 - p1) + p2 * (1 - p2)) / (p2 - p1) ** 2
        desc = f"conversion {p1:.2%} -> {p2:.2%} (abs {(p2 - p1) * 100:+.2f} pts, rel {(p2 / p1 - 1):+.1%})"
    elif a.mean is not None and a.sd is not None:
        d = a.mde_abs if a.mde_abs is not None else (a.mean * a.mde_rel if a.mde_rel else None)
        if not d:
            raise SystemExit("Give --mde-abs or --mde-rel")
        n = 2 * zz * a.sd ** 2 / d ** 2
        desc = f"mean {a.mean:g} -> {a.mean + d:g} (abs {d:+g}, rel {d / a.mean:+.1%}), sd {a.sd:g}"
    else:
        raise SystemExit("Give --baseline (conversion) or --mean and --sd (continuous).")

    n = math.ceil(n)
    print(f"Effect:        {desc}")
    print(f"alpha / power: {a.alpha} two-sided / {a.power}")
    print(f"Sample size:   {n:,} per group  ({2 * n:,} total)")
    if a.daily_users:
        days = 2 * n / (a.daily_users * a.split)
        weeks = max(1, math.ceil(days / 7))
        print(f"Duration:      {days:.1f} days at {a.daily_users * a.split:,.0f} users/day -> run {weeks} full week(s)")
        if weeks > 6:
            print("Warning:       longer than ~6 weeks. Consider a larger MDE, a more sensitive metric, or CUPED.")


if __name__ == "__main__":
    main()
