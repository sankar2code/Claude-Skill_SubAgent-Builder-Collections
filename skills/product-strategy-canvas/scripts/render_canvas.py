#!/usr/bin/env python3
"""Render canvas.json into visual product artifacts.

Outputs (to the folder given with -o):
  canvas.html             one-page interactive Product Strategy Canvas
                          (click any card to light up its chain from evidence to KPI)
  opportunity-tree.svg    goal -> opportunities -> bets -> initiatives
  priority-matrix.svg     value vs effort, bubble = reach, colour = confidence
  roadmap.svg             Now / Next / Later outcome roadmap
  dependencies.svg        dependency graph with critical path
  kpi-tree.svg            north star -> inputs -> guardrails

Usage:
    python render_canvas.py canvas.json -o canvas-output/
Standard library only.
"""
import argparse
import html
import json
import math
import os
import sys
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dependencies as deps_mod  # noqa: E402

PAL = ["#0ea5e9", "#8b5cf6", "#f97316", "#10b981", "#ec4899", "#eab308", "#64748b"]
LANES = [("now", "Now", "#0ea5e9"), ("next", "Next", "#8b5cf6"), ("later", "Later", "#94a3b8")]


def T(s, n):
    s = str(s or "")
    return s if len(s) <= n else s[: n - 1] + "…"


def bet_colors(c):
    return {b["id"]: PAL[i % len(PAL)] for i, b in enumerate(c.get("bets", []))}


# ---------------- SVG builders ----------------
def svg_tree(c):
    goals = c.get("goals", []) or [{"id": "G", "text": c.get("meta", {}).get("objective", "Goal")}]
    ops, bets, inits = c.get("opportunities", []), c.get("bets", []), c.get("initiatives", [])
    bc = bet_colors(c)
    cols = [("Goal", goals), ("Opportunities", ops), ("Bets", bets), ("Initiatives", inits)]
    bw, bh, gx, gy = 220, 50, 46, 14
    rows = max(len(x[1]) for x in cols) or 1
    W, H = 40 + 4 * bw + 3 * gx, 70 + rows * (bh + gy)
    pos = {}
    for ci, (_, items) in enumerate(cols):
        total = len(items) * (bh + gy) - gy
        y0 = 50 + ((rows * (bh + gy) - gy) - total) / 2
        for k, it in enumerate(items):
            pos[it["id"]] = (20 + ci * (bw + gx), y0 + k * (bh + gy))
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Inter, Arial, sans-serif"><rect width="{W}" height="{H}" fill="#fff"/>']
    for ci, (name, _) in enumerate(cols):
        o.append(f'<text x="{20 + ci * (bw + gx)}" y="30" font-size="12" font-weight="800" fill="#64748b" letter-spacing="1">{name.upper()}</text>')
    links = []
    g0 = goals[0]["id"]
    for op in ops:
        links.append((op.get("goal") or g0, op["id"], "#cbd5e1"))
    for b in bets:
        for op in b.get("opportunities", []):
            links.append((op, b["id"], bc.get(b["id"], "#cbd5e1")))
    for i in inits:
        if i.get("bet"):
            links.append((i["bet"], i["id"], bc.get(i["bet"], "#cbd5e1")))
    for a, b, col in links:
        if a in pos and b in pos:
            x1, y1 = pos[a][0] + bw, pos[a][1] + bh / 2
            x2, y2 = pos[b][0], pos[b][1] + bh / 2
            mx = (x1 + x2) / 2
            o.append(f'<path d="M{x1},{y1} C{mx},{y1} {mx},{y2} {x2},{y2}" fill="none" stroke="{col}" stroke-width="2" opacity=".75"/>')
    for ci, (_, items) in enumerate(cols):
        for it in items:
            x, y = pos[it["id"]]
            col = bc.get(it["id"]) or bc.get(it.get("bet"), "#0f172a" if ci == 0 else "#cbd5e1")
            fill = "#0f172a" if ci == 0 else "#fff"
            tc = "#fff" if ci == 0 else "#0f172a"
            text = it.get("text") or it.get("title") or ""
            o.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="9" fill="{fill}" stroke="{col}" stroke-width="{2 if ci >= 2 else 1}"/>')
            o.append(f'<text x="{x + 10}" y="{y + 20}" font-size="10" font-weight="800" fill="{col if ci else "#7dd3fc"}">{escape(it["id"])}{" · " + escape(str(it.get("horizon","")).upper()) if ci == 3 else ""}</text>')
            o.append(f'<text x="{x + 10}" y="{y + 37}" font-size="11.5" fill="{tc}">{escape(T(text, 34))}</text>')
    o.append("</svg>")
    return "\n".join(o)


def value_effort(c):
    m = c.get("meta", {}).get("prioritization", "rice")
    pts = []
    for i in c.get("initiatives", []):
        try:
            if m == "wsjf":
                v = float(i["business_value"]) + float(i["time_criticality"]) + float(i["risk_reduction"])
                e = float(i["job_size"])
                conf = float(i.get("confidence", 0.8))
                reach = 1
            elif m == "ice":
                v, e = float(i["impact"]), 11 - float(i["ease"])
                conf = float(i["confidence"])
                conf = conf / 10 if conf > 1 else conf
                reach = 1
            else:
                reach = float(i["reach"])
                v = reach * float(i["impact"])
                e = float(i["effort"])
                conf = float(i["confidence"])
        except (KeyError, ValueError, TypeError):
            continue
        pts.append((i, v, e, conf, reach))
    return pts, m


def svg_matrix(c):
    pts, m = value_effort(c)
    W, P = 760, 70
    H0 = 560
    pw, ph = W - 2 * P, H0 - 2 * P - 20
    H = H0 + 20 + 18 * ((len(pts) + 1) // 2)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Inter, Arial, sans-serif"><rect width="{W}" height="{H}" fill="#fff"/>',
         f'<text x="{P}" y="34" font-size="15" font-weight="700" fill="#0f172a">Prioritization matrix ({m.upper()} inputs)</text>']
    if not pts:
        o.append(f'<text x="{P}" y="80" font-size="13" fill="#64748b">No initiatives with {m.upper()} fields yet.</text></svg>')
        return "\n".join(o)
    vmax = max(p[1] for p in pts) * 1.1
    emax = max(p[2] for p in pts) * 1.15
    rmax = max(p[4] for p in pts)
    X = lambda e: P + e / emax * pw
    Y = lambda v: P + ph - v / vmax * ph
    quad = [("Quick wins", P + 8, P + 18, "#059669"), ("Big bets", P + pw - 8, P + 18, "#2563eb"),
            ("Fill-ins", P + 8, P + ph - 8, "#64748b"), ("Money pits", P + pw - 8, P + ph - 8, "#dc2626")]
    o.append(f'<rect x="{P}" y="{P}" width="{pw}" height="{ph}" fill="#f8fafc" stroke="#cbd5e1"/>')
    o.append(f'<line x1="{P + pw / 2}" y1="{P}" x2="{P + pw / 2}" y2="{P + ph}" stroke="#e2e8f0" stroke-dasharray="4 4"/>')
    o.append(f'<line x1="{P}" y1="{P + ph / 2}" x2="{P + pw}" y2="{P + ph / 2}" stroke="#e2e8f0" stroke-dasharray="4 4"/>')
    for name, x, y, col in quad:
        anchor = "start" if x < W / 2 else "end"
        o.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="11" font-weight="800" fill="{col}" opacity=".8">{name.upper()}</text>')
    o.append(f'<text x="{P + pw / 2}" y="{H0 - 30}" text-anchor="middle" font-size="12" font-weight="700" fill="#334155">Effort →</text>')
    o.append(f'<text x="22" y="{P + ph / 2}" text-anchor="middle" font-size="12" font-weight="700" fill="#334155" transform="rotate(-90 22 {P + ph / 2})">Value ({"reach × impact" if m == "rice" else "impact" if m == "ice" else "value + urgency + risk"}) →</text>')
    placed = []
    for i, v, e, conf, reach in sorted(pts, key=lambda p: -p[4]):
        r = 10 + 20 * math.sqrt(reach / rmax)
        cx, cy = X(e), Y(v)
        for _ in range(8):
            hit = [q for q in placed if math.hypot(q[0] - cx, q[1] - cy) < (q[2] + r) * 0.8]
            if not hit:
                break
            cx += (r + hit[0][2]) * 0.55 * (1 if len(placed) % 2 == 0 else -1)
        placed.append((cx, cy, r))
        col = "#059669" if conf >= 0.8 else "#d97706" if conf >= 0.5 else "#dc2626"
        o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{col}" fill-opacity=".25" stroke="{col}" stroke-width="2"/>')
        o.append(f'<text x="{cx:.1f}" y="{cy + 4:.1f}" text-anchor="middle" font-size="11" font-weight="800" fill="{col}">{escape(i["id"])}</text>')
    lx = P
    for lab, col in (("confidence ≥ 0.8", "#059669"), ("0.5–0.8", "#d97706"), ("< 0.5", "#dc2626")):
        o.append(f'<circle cx="{lx + 6}" cy="{H0 - 12}" r="6" fill="{col}" fill-opacity=".3" stroke="{col}"/><text x="{lx + 16}" y="{H0 - 8}" font-size="10.5" fill="#334155">{lab}</text>')
        lx += 120
    o.append(f'<text x="{W - P}" y="{H0 - 8}" text-anchor="end" font-size="10.5" fill="#64748b">bubble size = reach</text>')
    for n, (i, v, e, conf, reach) in enumerate(sorted(pts, key=lambda p: str(p[0]["id"]))):
        lx2 = P + (n % 2) * (pw / 2)
        ly2 = H0 + 22 + (n // 2) * 18
        o.append(f'<text x="{lx2}" y="{ly2}" font-size="11" fill="#334155"><tspan font-weight="800">{escape(i["id"])}</tspan>  {escape(T(i.get("title",""), 44))}</text>')
    o.append("</svg>")
    return "\n".join(o)


def svg_roadmap(c):
    bc = bet_colors(c)
    bets = {b["id"]: b for b in c.get("bets", [])}
    kp = {k["id"]: k for k in c.get("kpis", [])}
    lanes = {k: [i for i in c.get("initiatives", []) if str(i.get("horizon", "")).lower() == k] for k, _, _ in LANES}
    cw, bh, gy = 300, 64, 12
    rows = max([len(v) for v in lanes.values()] + [1])
    W, H = 30 + 3 * (cw + 20), 110 + rows * (bh + gy)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Inter, Arial, sans-serif"><rect width="{W}" height="{H}" fill="#fff"/>',
         f'<text x="20" y="30" font-size="15" font-weight="700" fill="#0f172a">Outcome roadmap · {escape(T(c.get("meta",{}).get("objective",""), 90))}</text>']
    for li, (k, name, col) in enumerate(LANES):
        x = 20 + li * (cw + 20)
        o.append(f'<rect x="{x}" y="48" width="{cw}" height="{H - 60}" rx="12" fill="#f8fafc" stroke="#e2e8f0"/>')
        o.append(f'<rect x="{x}" y="48" width="{cw}" height="34" rx="12" fill="{col}"/><rect x="{x}" y="66" width="{cw}" height="16" fill="{col}"/>')
        o.append(f'<text x="{x + 14}" y="70" font-size="13" font-weight="800" fill="#fff">{name.upper()}</text>')
        o.append(f'<text x="{x + cw - 14}" y="70" text-anchor="end" font-size="10.5" fill="#fff">{"committed" if k == "now" else "likely" if k == "next" else "exploring"}</text>')
        for r, it in enumerate(sorted(lanes[k], key=lambda i: (i.get("bet", ""), i.get("rank", 99)))):
            y = 94 + r * (bh + gy)
            b = bets.get(it.get("bet"), {})
            bcol = bc.get(it.get("bet"), "#cbd5e1")
            metric = kp.get(b.get("success_metric"), {}).get("name", "")
            o.append(f'<rect x="{x + 10}" y="{y}" width="{cw - 20}" height="{bh}" rx="8" fill="#fff" stroke="#e2e8f0"/><rect x="{x + 10}" y="{y}" width="5" height="{bh}" rx="2" fill="{bcol}"/>')
            o.append(f'<text x="{x + 24}" y="{y + 19}" font-size="11.5" font-weight="700" fill="#0f172a">{escape(it["id"])} · {escape(T(it.get("title",""), 34))}</text>')
            o.append(f'<text x="{x + 24}" y="{y + 36}" font-size="10.5" fill="{bcol}" font-weight="700">{escape(b.get("id",""))} {escape(T(b.get("title",""), 38))}</text>')
            o.append(f'<text x="{x + 24}" y="{y + 53}" font-size="10" fill="#64748b">moves: {escape(T(metric or "(no metric)", 42))}</text>')
    o.append("</svg>")
    return "\n".join(o)


def svg_kpi(c):
    ks = c.get("kpis", [])
    if not ks:
        return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 60"><text x="10" y="30">No KPIs yet</text></svg>'
    kids = {}
    for k in ks:
        kids.setdefault(k.get("parent"), []).append(k)
    roots = kids.get(None, []) or [k for k in ks if k.get("type") == "north_star"]
    order, lvl = [], {}

    def walk(k, d):
        order.append(k)
        lvl[k["id"]] = d
        for ch in kids.get(k["id"], []):
            walk(ch, d + 1)

    for r in roots:
        walk(r, 0)
    bw, bh, gy, ind = 330, 52, 10, 60
    W = 40 + (max(lvl.values()) * ind) + bw + 20
    H = 50 + len(order) * (bh + gy)
    col = {"north_star": "#0f172a", "input": "#0ea5e9", "guardrail": "#d97706", "counter": "#d97706"}
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Inter, Arial, sans-serif"><rect width="{W}" height="{H}" fill="#fff"/>',
         '<text x="20" y="28" font-size="15" font-weight="700" fill="#0f172a">KPI tree</text>']
    ypos = {}
    for n, k in enumerate(order):
        x, y = 20 + lvl[k["id"]] * ind, 44 + n * (bh + gy)
        ypos[k["id"]] = (x, y)
        p = k.get("parent")
        if p in ypos:
            px, py = ypos[p]
            o.append(f'<path d="M{px + 16},{py + bh} V{y + bh / 2} H{x}" fill="none" stroke="#cbd5e1" stroke-width="1.5"/>')
        cc = col.get(k.get("type"), "#64748b")
        ns = k.get("type") == "north_star"
        o.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="8" fill="{cc if ns else "#fff"}" stroke="{cc}" stroke-width="1.5"/>')
        o.append(f'<text x="{x + 12}" y="{y + 19}" font-size="11.5" font-weight="700" fill="{"#fff" if ns else "#0f172a"}">{escape(k["id"])} · {escape(T(k.get("name",""), 40))}</text>')
        o.append(f'<text x="{x + 12}" y="{y + 38}" font-size="10.5" fill="{"#cbd5e1" if ns else "#475569"}">{escape(str(k.get("type","")).replace("_"," "))} · baseline {escape(T(k.get("baseline","?"), 22))} → {escape(T(k.get("target","?"), 18))}</text>')
    o.append("</svg>")
    return "\n".join(o)


# ---------------- HTML ----------------
def links_map(c):
    up = {}
    for e in c.get("evidence", []):
        up[e["id"]] = [e.get("source")] if e.get("source") else []
    for n in c.get("needs", []):
        up[n["id"]] = n.get("evidence", [])
    for o in c.get("opportunities", []):
        up[o["id"]] = o.get("needs", [])
    for b in c.get("bets", []):
        up[b["id"]] = b.get("opportunities", [])
    for i in c.get("initiatives", []):
        up[i["id"]] = [i["bet"]] if i.get("bet") else []
    for k in c.get("kpis", []):
        up[k["id"]] = [b["id"] for b in c.get("bets", []) if b.get("success_metric") == k["id"]] + ([k["parent"]] if k.get("parent") else [])
    return up


def card(it, kind, bc):
    e = html.escape
    t = it.get("text") or it.get("title") or it.get("name") or ""
    sub = ""
    if kind == "evidence":
        sub = f'{it.get("label","")} · {it.get("source","")} · {it.get("strength","")}'
    elif kind == "needs":
        sub = f'importance {it.get("importance","?")} · {it.get("segment","")}'
    elif kind == "bets":
        sub = f'confidence {it.get("confidence","?")} · appetite {it.get("appetite","?")}'
    elif kind == "initiatives":
        sub = f'{str(it.get("horizon","")).upper()} · {it.get("duration_weeks","?")} wks' + (f' · rank {it["rank"]}' if it.get("rank") else "")
    elif kind == "kpis":
        sub = f'{str(it.get("type","")).replace("_"," ")} · {it.get("baseline","?")} → {it.get("target","?")}'
    col = bc.get(it["id"]) or bc.get(it.get("bet"), "")
    style = f' style="--bc:{col}"' if col else ""
    return f'<div class="cd" data-id="{e(it["id"])}"{style}><b>{e(it["id"])}</b><span>{e(t)}</span><small>{e(sub)}</small></div>'


def render_html(c, svgs, check_note):
    e = html.escape
    m = c.get("meta", {})
    bc = bet_colors(c)
    cols = [("Evidence", "evidence"), ("Needs", "needs"), ("Opportunities", "opportunities"), ("Bets", "bets"), ("Roadmap", "initiatives"), ("KPIs", "kpis")]
    chain = "".join(f'<div class="col"><h3>{n}<i>{len(c.get(k, []))}</i></h3>' + "".join(card(it, k, bc) for it in c.get(k, [])) + "</div>" for n, k in cols)
    choices = "".join(f'<tr><td>{e(x.get("we_will",""))}</td><td>{e(x.get("we_wont",""))}</td><td>{e(x.get("rationale",""))}</td></tr>' for x in c.get("choices", []))
    sc = "".join(f'<tr><td><b>{e(s.get("bet",""))}</b></td><td>{e(s.get("result",""))}</td><td><span class="dc {e(str(s.get("decision","")).lower())}">{e(str(s.get("decision","")))}</span></td><td>{e(s.get("learned",""))}</td></tr>' for s in c.get("scorecard", []))
    bets = "".join(f'<div class="bet" style="--bc:{bc[b["id"]]}"><b>{e(b["id"])} · {e(b.get("title",""))}</b><p>{e(b.get("hypothesis",""))}</p><small>Success: {e(b.get("success_metric",""))} · Kill if: {e(b.get("kill_criteria",""))} · Appetite: {e(b.get("appetite",""))}</small></div>' for b in c.get("bets", []))
    up = json.dumps(links_map(c))
    betk = json.dumps({b["id"]: b.get("success_metric") for b in c.get("bets", []) if b.get("success_metric")})
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Product Strategy Canvas</title><style>
:root{{--ink:#0f172a;--mut:#64748b;--line:#e2e8f0;--bg:#f8fafc}}
*{{box-sizing:border-box}} body{{margin:0;font-family:Inter,system-ui,Arial,sans-serif;background:var(--bg);color:var(--ink);padding:24px 16px 60px}}
.w{{max-width:1280px;margin:0 auto}} h1{{margin:0;font-size:26px}} h2{{font-size:17px;margin:34px 0 10px}} .lead{{color:#334155;margin:6px 0}} .meta{{color:var(--mut);font-size:13px}}
.note{{display:inline-block;margin-top:8px;font-size:12px;border-radius:10px;padding:4px 10px;background:#ecfeff;color:#155e75}}
.chain{{display:grid;grid-template-columns:repeat(6,minmax(180px,1fr));gap:10px;overflow-x:auto;padding-bottom:6px}}
.col h3{{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);margin:0 0 8px;display:flex;justify-content:space-between}} .col h3 i{{font-style:normal;background:#e2e8f0;border-radius:8px;padding:0 6px}}
.cd{{background:#fff;border:1px solid var(--line);border-left:4px solid var(--bc,#cbd5e1);border-radius:9px;padding:8px 10px;margin-bottom:8px;cursor:pointer;transition:.15s}}
.cd b{{font-size:11px;color:var(--bc,#475569)}} .cd span{{display:block;font-size:12.5px;line-height:1.35;margin-top:2px}} .cd small{{display:block;color:var(--mut);font-size:10.5px;margin-top:4px}}
.chain.sel .cd{{opacity:.25}} .chain.sel .cd.on{{opacity:1;box-shadow:0 0 0 2px var(--bc,#0ea5e9)}}
.hint{{font-size:12px;color:var(--mut);margin:-4px 0 8px}}
.fig{{background:#fff;border:1px solid var(--line);border-radius:12px;padding:10px;overflow-x:auto}} .fig svg{{width:100%;height:auto;min-width:640px;display:block}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:14px}} .two>div{{min-width:0}} .two .fig svg{{min-width:0}} @media(max-width:900px){{.two{{grid-template-columns:1fr}}}}
table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden;font-size:13px}} th,td{{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top}} th{{background:#0f172a;color:#fff;font-size:12px}}
.bets{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px}} .bet{{background:#fff;border:1px solid var(--line);border-top:4px solid var(--bc);border-radius:10px;padding:12px}} .bet b{{color:var(--bc)}} .bet p{{margin:6px 0;font-size:13px}} .bet small{{color:var(--mut);font-size:11.5px}}
.dc{{border-radius:8px;padding:2px 8px;font-weight:700;font-size:12px;background:#e2e8f0}} .dc.scale{{background:#d1fae5;color:#065f46}} .dc.iterate{{background:#fef3c7;color:#92400e}} .dc.kill{{background:#fee2e2;color:#991b1b}}
@media print{{body{{background:#fff}} .chain.sel .cd{{opacity:1}}}}
</style></head><body><div class="w">
<h1>Product Strategy Canvas</h1>
<p class="lead"><b>{e(m.get("product",""))}</b>: {e(m.get("objective",""))}</p>
<p class="meta">Owner: {e(m.get("owner",""))} · as of {e(m.get("as_of",""))} · prioritization: {e(str(m.get("prioritization","rice")).upper())}</p>
<span class="note">{e(check_note)}</span>
<h2>The chain: evidence to outcomes</h2><p class="hint">Click any card to light up everything it connects to. Click again to clear.</p>
<div class="chain" id="chain">{chain}</div>
<h2>Choices</h2><table><tr><th>We will</th><th>We won't</th><th>Why</th></tr>{choices or '<tr><td colspan=3>No explicit choices yet</td></tr>'}</table>
<h2>Product bets</h2><div class="bets">{bets}</div>
<h2>Opportunity tree</h2><div class="fig">{svgs["tree"]}</div>
<div class="two"><div><h2>Prioritization</h2><div class="fig">{svgs["matrix"]}</div></div><div><h2>KPI tree</h2><div class="fig">{svgs["kpi"]}</div></div></div>
<h2>Outcome roadmap</h2><div class="fig">{svgs["roadmap"]}</div>
<h2>Dependencies</h2><div class="fig">{svgs["deps"]}</div>
<h2>Bet scorecard</h2><table><tr><th>Bet</th><th>Result</th><th>Decision</th><th>What we learned</th></tr>{sc or '<tr><td colspan=4>No bets reviewed yet</td></tr>'}</table>
</div><script>
(function(){{var UP={up};var BETK={betk};var DOWN={{}};Object.keys(UP).forEach(function(k){{UP[k].forEach(function(p){{(DOWN[p]=DOWN[p]||[]).push(k);}});}});
var ch=document.getElementById('chain'),cur=null;
function walk(id,map,acc){{(map[id]||[]).forEach(function(n){{if(!acc[n]){{acc[n]=1;walk(n,map,acc);}}}});return acc;}}
ch.addEventListener('click',function(ev){{var c=ev.target.closest('.cd');if(!c)return;var id=c.dataset.id;
 if(cur===id){{cur=null;ch.classList.remove('sel');[].forEach.call(ch.querySelectorAll('.cd'),function(x){{x.classList.remove('on');}});return;}}
 cur=id;var on={{}};on[id]=1;walk(id,UP,on);walk(id,DOWN,on);Object.keys(on).forEach(function(k){{if(BETK[k])on[BETK[k]]=1;}});ch.classList.add('sel');
 [].forEach.call(ch.querySelectorAll('.cd'),function(x){{x.classList.toggle('on',!!on[x.dataset.id]);}});}});}})();
</script></body></html>"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("-o", "--out", default="canvas-output")
    a = ap.parse_args()
    c = json.load(open(a.file))
    os.makedirs(a.out, exist_ok=True)
    r = deps_mod.analyse(c.get("initiatives", []))
    if r.get("cycle"):
        dsvg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 60"><text x="10" y="35" fill="#dc2626" font-family="Arial">Circular dependency: {escape(" -> ".join(r["cycle"]))}</text></svg>'
    else:
        dsvg = deps_mod.svg(c.get("initiatives", []), r)
    svgs = {"tree": svg_tree(c), "matrix": svg_matrix(c), "roadmap": svg_roadmap(c), "kpi": svg_kpi(c), "deps": dsvg}
    names = {"tree": "opportunity-tree.svg", "matrix": "priority-matrix.svg", "roadmap": "roadmap.svg", "kpi": "kpi-tree.svg", "deps": "dependencies.svg"}
    for k, fn in names.items():
        open(os.path.join(a.out, fn), "w").write(svgs[k])
    note = "Run canvas_check.py for traceability gaps before sharing"
    open(os.path.join(a.out, "canvas.html"), "w").write(render_html(c, svgs, note))
    print(f"Wrote canvas.html and {len(names)} SVGs to {a.out}")


if __name__ == "__main__":
    main()
