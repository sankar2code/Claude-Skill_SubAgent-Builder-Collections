#!/usr/bin/env python3
"""Export a canvas.json for the next tool in the chain.

  --backlog   backlog.csv for Jira / Linear: one epic per bet, one story per
              initiative, with the bet hypothesis, success metric and the
              evidence trail in the description
  --brief     deck-brief.md: action-title spine and slide-by-slide spec for a
              leadership readout (any slide tool)
  --prd       prd-inputs/<bet>.md: one PRD starter per bet for the prd-writer skill

Usage:
    python export.py canvas.json -o canvas-output/ [--backlog] [--brief] [--prd]
    (no flag = all three)
Standard library only.
"""
import argparse
import csv
import json
import os


def idx(c):
    d = {}
    for k in ("sources", "evidence", "needs", "goals", "opportunities", "bets", "initiatives", "kpis"):
        for it in c.get(k, []):
            d[it["id"]] = it
    return d


def trail(c, D, bet):
    ev = []
    for o in bet.get("opportunities", []):
        for n in D.get(o, {}).get("needs", []):
            for e in D.get(n, {}).get("evidence", []):
                x = D.get(e)
                if x and x not in ev:
                    ev.append(x)
    return ev


def backlog(c, D, out):
    path = os.path.join(out, "backlog.csv")
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["Issue Type", "Summary", "Description", "Epic Link", "Labels", "Priority Rank"])
        for b in c.get("bets", []):
            k = D.get(b.get("success_metric"), {})
            ev = "; ".join(f"{e['id']} {e['text']} [{e.get('label','')} {e.get('source','')}]" for e in trail(c, D, b))
            desc = (f"Hypothesis: {b.get('hypothesis','')}\nSuccess metric: {k.get('name', b.get('success_metric',''))} "
                    f"(baseline {k.get('baseline','?')}, target {k.get('target','?')})\nKill criteria: {b.get('kill_criteria','')}\n"
                    f"Appetite: {b.get('appetite','')}\nEvidence: {ev}")
            w.writerow(["Epic", f"{b['id']} {b.get('title','')}", desc, "", "product-bet", ""])
            for i in sorted([i for i in c.get("initiatives", []) if i.get("bet") == b["id"]], key=lambda i: i.get("rank", 99)):
                deps = ", ".join(i.get("depends_on", []))
                w.writerow(["Story", f"{i['id']} {i.get('title','')}",
                            f"Part of {b['id']}. Horizon: {i.get('horizon','')}. Estimate: {i.get('duration_weeks','?')} weeks."
                            + (f" Depends on: {deps}." if deps else "") + " Acceptance criteria: to be written with backlog-builder.",
                            f"{b['id']} {b.get('title','')}", str(i.get("horizon", "")), i.get("rank", "")])
    return path


def brief(c, D, out):
    m = c.get("meta", {})
    bets = c.get("bets", [])
    ns = next((k for k in c.get("kpis", []) if k.get("type") == "north_star"), {})
    now = [i for i in c.get("initiatives", []) if str(i.get("horizon")).lower() == "now"]
    L = [f"# Deck brief: {m.get('product','')}", "",
         f"**Audience:** leadership · **Decision:** approve the bets and the Now column · **Source:** canvas.json as of {m.get('as_of','')}", "",
         "## Action-title spine", "",
         f"1. {m.get('objective','')}",
         f"2. Customers' top unmet need is \"{max(c.get('needs') or [{}], key=lambda n: float(n.get('importance', 0) or 0)).get('text','')}\"",
         f"3. {len(bets)} product bets address it, each with a success metric and a kill rule",
         f"4. Now: {len(now)} initiatives, critical path first",
         f"5. We will know it worked when {ns.get('name','the north star')} moves from {ns.get('baseline','?')} to {ns.get('target','?')}",
         "6. The ask: approve the bets, the Now scope and the review date", "",
         "## Slides", "",
         "| # | Action title | Exhibit | Source |", "|---|---|---|---|",
         "| 1 | (title 1) | Objective and north star | canvas meta, K1 |",
         "| 2 | (title 2) | Evidence → needs chain (canvas.html section 1) | evidence IDs |",
         "| 3 | (title 3) | Opportunity tree (opportunity-tree.svg) | O, B IDs |",
         "| 4 | (title 4) | Prioritization matrix + Now/Next/Later (priority-matrix.svg, roadmap.svg) | prioritize.py output |",
         "| 5 | (title 5) | KPI tree (kpi-tree.svg) | K IDs |",
         "| 6 | (title 6) | Choices (will / won't) and the ask | C IDs |", "",
         "## Appendix", "", "- Dependencies and critical path (dependencies.svg)", "- Full evidence list with sources",
         "- Bets with hypotheses, success metrics and kill criteria", "",
         "Only approved claims go into slides. Labels ([FACT], [HYPOTHESIS]...) stay in speaker notes."]
    path = os.path.join(out, "deck-brief.md")
    open(path, "w").write("\n".join(L))
    return path


def prd(c, D, out):
    folder = os.path.join(out, "prd-inputs")
    os.makedirs(folder, exist_ok=True)
    paths = []
    for b in c.get("bets", []):
        k = D.get(b.get("success_metric"), {})
        ops = [D.get(o, {}) for o in b.get("opportunities", [])]
        inits = [i for i in c.get("initiatives", []) if i.get("bet") == b["id"]]
        L = [f"# PRD input: {b['id']} {b.get('title','')}", "",
             "Hand this to the `prd-writer` skill (AI Product PRD or Feature Brief format).", "",
             f"**Problem / opportunity:** " + "; ".join(o.get("text", "") for o in ops),
             f"**Hypothesis:** {b.get('hypothesis','')}",
             f"**Success metric:** {k.get('name','')} (baseline {k.get('baseline','?')}, target {k.get('target','?')})",
             f"**Kill criteria:** {b.get('kill_criteria','')}",
             f"**Appetite:** {b.get('appetite','')}", "",
             "**Evidence:**"] + [f"- {e['id']} {e['text']} [{e.get('label','')} {e.get('source','')}]" for e in trail(c, D, b)] + [
             "", "**Scope (initiatives):**"] + [f"- {i['id']} {i.get('title','')} ({i.get('horizon','')})" for i in inits] + [
             "", "**Choices that constrain this bet:**"] + [f"- Will: {x.get('we_will','')} / Won't: {x.get('we_wont','')}" for x in c.get("choices", [])]
        p = os.path.join(folder, f"{b['id']}.md")
        open(p, "w").write("\n".join(L))
        paths.append(p)
    return paths


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("-o", "--out", default="canvas-output")
    ap.add_argument("--backlog", action="store_true")
    ap.add_argument("--brief", action="store_true")
    ap.add_argument("--prd", action="store_true")
    a = ap.parse_args()
    c = json.load(open(a.file))
    D = idx(c)
    os.makedirs(a.out, exist_ok=True)
    allx = not (a.backlog or a.brief or a.prd)
    if a.backlog or allx:
        print("Wrote", backlog(c, D, a.out))
    if a.brief or allx:
        print("Wrote", brief(c, D, a.out))
    if a.prd or allx:
        for p in prd(c, D, a.out):
            print("Wrote", p)


if __name__ == "__main__":
    main()
