#!/usr/bin/env python3
"""Dependency analysis for roadmap initiatives: cycles, critical path, slack,
and an SVG dependency graph.

Each initiative may have duration_weeks and depends_on (list of IDs).

Usage:
    python dependencies.py canvas.json [-o dependencies.svg]
Standard library only. Importable: analyse(initiatives) and svg(initiatives, result).
"""
import argparse
import json
import sys
from xml.sax.saxutils import escape

HZ_COLOR = {"now": "#0ea5e9", "next": "#8b5cf6", "later": "#94a3b8"}


def find_cycle(nodes, deps):
    WHITE, GREY, BLACK = 0, 1, 2
    st = {n: WHITE for n in nodes}
    path = []

    def dfs(n):
        st[n] = GREY
        path.append(n)
        for d in deps.get(n, []):
            if d not in st:
                continue
            if st[d] == GREY:
                return path[path.index(d):] + [d]
            if st[d] == WHITE:
                r = dfs(d)
                if r:
                    return r
        path.pop()
        st[n] = BLACK
        return None

    for n in nodes:
        if st[n] == WHITE:
            r = dfs(n)
            if r:
                return r
    return None


def analyse(items):
    nodes = [i["id"] for i in items]
    by = {i["id"]: i for i in items}
    deps = {i["id"]: [d for d in i.get("depends_on", []) if d in by] for i in items}
    missing = [(i["id"], d) for i in items for d in i.get("depends_on", []) if d not in by]
    cyc = find_cycle(nodes, deps)
    if cyc:
        return {"cycle": cyc, "missing": missing}
    dur = {n: float(by[n].get("duration_weeks", 0) or 0) for n in nodes}
    order, seen = [], set()

    def visit(n):
        if n in seen:
            return
        seen.add(n)
        for d in deps[n]:
            visit(d)
        order.append(n)

    for n in nodes:
        visit(n)
    es, ef = {}, {}
    for n in order:
        es[n] = max([ef[d] for d in deps[n]], default=0.0)
        ef[n] = es[n] + dur[n]
    end = max(ef.values(), default=0.0)
    succ = {n: [m for m in nodes if n in deps[m]] for n in nodes}
    lf, ls = {}, {}
    for n in reversed(order):
        lf[n] = min([ls[s] for s in succ[n]], default=end)
        ls[n] = lf[n] - dur[n]
    slack = {n: round(ls[n] - es[n], 2) for n in nodes}
    crit = [n for n in order if abs(slack[n]) < 1e-9 and dur[n] > 0]
    depth = {}
    for n in order:
        depth[n] = max([depth[d] + 1 for d in deps[n]], default=0)
    fan = {n: len(succ[n]) for n in nodes}
    return {"cycle": None, "missing": missing, "es": es, "ef": ef, "slack": slack, "critical": crit,
            "end": end, "depth": depth, "deps": deps, "fan": fan, "order": order}


def svg(items, r, width=900):
    by = {i["id"]: i for i in items}
    cols = {}
    for n, d in r["depth"].items():
        cols.setdefault(d, []).append(n)
    ncol = max(cols) + 1 if cols else 1
    rows = max(len(v) for v in cols.values()) if cols else 1
    bw, bh, gx, gy = 190, 54, 60, 26
    W = max(width, 40 + ncol * (bw + gx))
    H = 70 + rows * (bh + gy)
    pos = {}
    for d, ns in cols.items():
        for k, n in enumerate(sorted(ns)):
            pos[n] = (30 + d * (bw + gx), 50 + k * (bh + gy))
    crit = set(r["critical"])
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Inter, Arial, sans-serif">',
         '<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#64748b"/></marker>'
         '<marker id="arc" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#dc2626"/></marker></defs>',
         f'<rect width="{W}" height="{H}" fill="#fff"/>',
         f'<text x="30" y="28" font-size="15" font-weight="700" fill="#0f172a">Dependencies · critical path {r["end"]:g} weeks</text>']
    for n, ds in r["deps"].items():
        for d in ds:
            x1, y1 = pos[d][0] + bw, pos[d][1] + bh / 2
            x2, y2 = pos[n][0], pos[n][1] + bh / 2
            c = n in crit and d in crit
            mx = (x1 + x2) / 2
            o.append(f'<path d="M{x1},{y1} C{mx},{y1} {mx},{y2} {x2 - 2},{y2}" fill="none" stroke="{"#dc2626" if c else "#94a3b8"}" stroke-width="{2.4 if c else 1.4}" marker-end="url(#{"arc" if c else "ar"})"/>')
    for n, (x, y) in pos.items():
        it = by[n]
        hz = str(it.get("horizon", "")).lower()
        c = n in crit
        o.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="9" fill="#fff" stroke="{"#dc2626" if c else "#cbd5e1"}" stroke-width="{2.2 if c else 1}"/>')
        o.append(f'<rect x="{x}" y="{y}" width="6" height="{bh}" rx="3" fill="{HZ_COLOR.get(hz, "#cbd5e1")}"/>')
        t = escape(str(it.get("title", n)))
        if len(t) > 27:
            t = t[:26] + "…"
        o.append(f'<text x="{x + 14}" y="{y + 21}" font-size="11.5" font-weight="700" fill="#0f172a">{escape(n)} · {t}</text>')
        o.append(f'<text x="{x + 14}" y="{y + 40}" font-size="10.5" fill="#475569">{it.get("duration_weeks", "?")} wks · starts wk {r["es"][n]:g} · slack {r["slack"][n]:g}</text>')
    o.append("</svg>")
    return "\n".join(o)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    items = json.load(open(a.file)).get("initiatives", [])
    r = analyse(items)
    for i, d in r["missing"]:
        print(f"WARNING: {i} depends on {d}, which is not on the roadmap")
    if r["cycle"]:
        print("BLOCKER: circular dependency: " + " -> ".join(r["cycle"]))
        sys.exit(1)
    by = {i["id"]: i for i in items}
    print(f"Critical path ({r['end']:g} weeks): " + " -> ".join(r["critical"]))
    print(f"\n  {'ID':<5}{'Initiative':<40}{'Wks':>5}{'Start':>7}{'Finish':>8}{'Slack':>7}  Blocks")
    for n in r["order"]:
        print(f"  {n:<5}{str(by[n].get('title',''))[:39]:<40}{by[n].get('duration_weeks','?')!s:>5}{r['es'][n]:7g}{r['ef'][n]:8g}{r['slack'][n]:7g}  {r['fan'][n]}{'  ← critical' if n in r['critical'] else ''}")
    hubs = [n for n, f in r["fan"].items() if f >= 2]
    if hubs:
        print(f"\nCoordination hotspots (block 2+ items): {', '.join(hubs)}")
    nowlate = [n for n in r["order"] if str(by[n].get("horizon")).lower() == "now" and any(str(by.get(d, {}).get("horizon")).lower() in ("next", "later") for d in r["deps"][n])]
    if nowlate:
        print(f"WARNING: 'now' items depending on 'next/later' work: {', '.join(nowlate)}")
    if a.out:
        open(a.out, "w").write(svg(items, r))
        print(f"\nWrote {a.out}")


if __name__ == "__main__":
    main()
