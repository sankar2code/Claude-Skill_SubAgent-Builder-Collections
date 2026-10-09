#!/usr/bin/env python3
"""Driver-based business case: NPV, IRR, payback, sensitivity and break-even.

Each option has an upfront investment and yearly drivers. Yearly cash flow is:

    volume x price x margin  -  fixed_cost  (plus any extra 'other' cash flow)

Values are incremental to the status quo. All options share the same
discount rate and horizon so they can be compared.

Usage:
    python business_case.py business-case.json [--swing 0.2]

Input format: see assets/templates/business-case.json
Standard library only.
"""
import argparse
import copy
import json
import sys

DRIVERS = ("volume", "price", "margin", "fixed_cost")


def series(v, years):
    if isinstance(v, list):
        if len(v) != years:
            raise ValueError(f"expected {years} yearly values, got {len(v)}")
        return [float(x) for x in v]
    return [float(v)] * years


def cash_flows(opt, years):
    s = {k: series(opt.get(k, 0), years) for k in DRIVERS}
    other = series(opt.get("other", 0), years)
    flows = [-float(opt.get("investment", 0))]
    for t in range(years):
        flows.append(s["volume"][t] * s["price"][t] * s["margin"][t] - s["fixed_cost"][t] + other[t])
    return flows


def npv(rate, flows):
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(flows))


def irr(flows, lo=-0.99, hi=10.0):
    f_lo, f_hi = npv(lo, flows), npv(hi, flows)
    if f_lo * f_hi > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        f_mid = npv(mid, flows)
        if abs(f_mid) < 1e-7:
            return mid
        if f_lo * f_mid < 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2


def payback(flows, rate=None):
    cum = 0.0
    for t, cf in enumerate(flows):
        v = cf / (1 + rate) ** t if rate is not None else cf
        prev = cum
        cum += v
        if t > 0 and cum >= 0 > prev:
            return t - 1 + (-prev / v if v else 0)
    return None


def scale(opt, key, factor):
    o = copy.deepcopy(opt)
    v = o.get(key, 0)
    o[key] = [x * factor for x in v] if isinstance(v, list) else float(v) * factor
    return o


def breakeven(opt, key, rate, years):
    """Multiplier on a driver at which NPV = 0 (bisection), or None."""
    def f(m):
        return npv(rate, cash_flows(scale(opt, key, m), years))
    lo, hi = 0.0, 10.0
    if f(lo) * f(hi) > 0:
        return None
    for _ in range(100):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def money(x, cur):
    sign = "-" if x < 0 else ""
    x = abs(x)
    if x >= 1e6:
        return f"{sign}{cur}{x/1e6:,.2f}M"
    if x >= 1e3:
        return f"{sign}{cur}{x/1e3:,.1f}K"
    return f"{sign}{cur}{x:,.0f}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--swing", type=float, default=0.2, help="sensitivity swing per driver (default 0.2 = +/-20%%)")
    a = ap.parse_args()
    spec = json.load(open(a.file))
    rate = float(spec["discount_rate"])
    years = int(spec["years"])
    cur = spec.get("currency_symbol", "$")
    print(f"Horizon {years} years · discount rate {rate:.1%} · values incremental to: {spec.get('baseline', 'status quo (not described)')}\n")

    problems, summary = [], []
    for name, opt in spec["options"].items():
        print(f"== {name} ==")
        if "assumptions" not in opt:
            problems.append(f"{name}: no 'assumptions' notes (label and source each driver)")
        try:
            flows = cash_flows(opt, years)
        except ValueError as e:
            problems.append(f"{name}: {e}")
            print(f"  cannot compute: {e}\n")
            continue
        v = npv(rate, flows)
        r = irr(flows)
        pb = payback(flows)
        dpb = payback(flows, rate)
        print("  Cash flows: " + ", ".join(f"Y{t} {money(cf, cur)}" for t, cf in enumerate(flows)))
        print(f"  NPV {money(v, cur)} | IRR {'n/a' if r is None else f'{r:.1%}'} | payback {'not within horizon' if pb is None else f'{pb:.1f} yrs'} | discounted payback {'not within horizon' if dpb is None else f'{dpb:.1f} yrs'}")

        sens = []
        for k in DRIVERS + ("investment",):
            if k not in opt or not opt.get(k):
                continue
            up = npv(rate, cash_flows(scale(opt, k, 1 + a.swing), years))
            dn = npv(rate, cash_flows(scale(opt, k, 1 - a.swing), years))
            sens.append((abs(up - dn), k, dn, up))
        sens.sort(reverse=True)
        print(f"  Sensitivity (driver +/-{a.swing:.0%} -> NPV):")
        for width, k, dn, up in sens:
            print(f"    {k:<11} {money(dn, cur):>10} .. {money(up, cur):>10}   swing {money(width, cur)}")
        print("  Break-even (driver multiplier for NPV = 0):")
        for k in ("volume", "price", "margin"):
            if k in opt and opt.get(k):
                m = breakeven(opt, k, rate, years)
                print(f"    {k:<11} {'not reachable in 0-10x' if m is None else f'{m:.2f}x of base ({(m-1):+.0%})'}")
        if "assumptions" in opt:
            print("  Assumptions:")
            for k, note in opt["assumptions"].items():
                print(f"    {k}: {note}")
        summary.append((v, name, r, pb))
        print()

    if summary:
        print("== Comparison (sorted by NPV) ==")
        for v, name, r, pb in sorted(summary, reverse=True):
            print(f"  {name:<28} NPV {money(v, cur):>11}  IRR {'n/a' if r is None else f'{r:.1%}':>7}  payback {'-' if pb is None else f'{pb:.1f}y'}")
    print()
    if problems:
        print("WARNINGS:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print("RESULT: computed. Check that every driver in 'assumptions' carries a label and source ID.")


if __name__ == "__main__":
    main()
