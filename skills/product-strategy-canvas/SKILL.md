---
name: product-strategy-canvas
description: >
  Turns product evidence into a traceable, visual Product Strategy Canvas: evidence →
  customer needs → opportunities → product bets → prioritized outcome roadmap → KPIs,
  all kept in one canvas.json with linked IDs, and rendered as real visuals (interactive
  canvas page, opportunity tree, prioritization matrix, Now/Next/Later roadmap,
  dependency graph with critical path, KPI tree). Use this skill when the user asks to
  "build a product strategy", "turn research into a roadmap", "define product bets",
  "prioritize with RICE / ICE / WSJF", "make an outcome roadmap", "map dependencies",
  "build a KPI tree", "why is this on the roadmap", "product strategy canvas", or
  "review whether our bets paid off". Exports a Jira/Linear backlog, PRD inputs and a
  deck brief. Part of the Product Strategy Canvas pack.
---

> **Product Strategy Canvas pack.** `product-strategy-canvas` (this skill). Upstream: `user-research`, `opportunity-finder`, `strategy-sprint`. Downstream: `prd-writer`, `backlog-builder`, `experiment-design`, `insight-storyteller`.

# Product Strategy Canvas

Product teams have plenty of artifacts: interview notes, opportunity lists, roadmaps and KPI decks. What they lack is the **chain** that connects them. This skill builds that chain in one file and draws it, so anyone can click a roadmap item and see the bet, the opportunity, the customer need and the evidence behind it.

**Your role:** keep the canvas honest and connected. Draft, score and draw; the team decides.

## Ground rules

- **One source of truth:** `canvas-output/canvas.json` (schema in `references/canvas-schema.md`). Every step reads it and updates it. Never retype earlier outputs.
- **Everything has an ID and a link upstream:** S source → E evidence → N need → O opportunity → B bet → I initiative → K KPI. An item with no link upstream is an orphan, and orphans get flagged.
- **Labels** (`references/evidence-rules.md`): `[FACT S#]`, `[ESTIMATE S#]`, `[INFERENCE]`, `[HYPOTHESIS]`, `[UNKNOWN]`. Bets are always hypotheses until the scorecard says otherwise.
- **No invented evidence:** no made-up quotes, survey numbers, reach figures or baselines. Unknown baselines stay `[UNKNOWN]` with a plan to measure them.
- **Read-only default:** write only to `canvas-output/`. Creating tickets, sending messages or publishing needs explicit approval.

## Step 0 — Mode and starting point

If `canvas-output/canvas.json` exists, run `scripts/canvas_check.py` on it, summarize where it stands, and continue.

Otherwise pick a mode:

| Mode | Use when | Steps |
|---|---|---|
| **Quick** | Docs already exist (research, a roadmap, OKRs); you need one connected page fast | 01 evidence → 02 needs → 05 bets → 08 roadmap → 10 KPIs → render |
| **Full** | Building or resetting strategy for a product area | All 12 steps, with checks between them |
| **Review** | Bets have shipped; did they work? | 12 bet scorecard → update the canvas |

Reuse what the kit already has instead of redoing it:
- **Opportunity Finder output** (`opportunity-output/`): import the evidence, needs and top opportunities at steps 01–03.
- **Strategy Sprint decision** (`strategy-output/`): import the choices and approved option at step 04.
- **User Research synthesis**: import themes as evidence at step 01.

Copy `assets/templates/canvas-blank.json` to `canvas-output/canvas.json` and fill `meta` (product, objective, owner, as_of, mode, prioritization method).

## Steps (load one playbook at a time: `references/steps/NN-<step>.md`)

| # | Step | Adds to canvas | Check |
|---|---|---|---|
| 01 | `evidence-intake` | sources, evidence | every item has a source and strength |
| 02 | `needs-map` | needs (jobs, unmet outcomes) | each need cites evidence |
| 03 | `opportunity-tree` | goals, opportunities | each opportunity links needs and a goal |
| 04 | `strategic-choices` | choices (we will / we won't) | real trade-offs, not slogans |
| 05 | `product-bets` | bets | hypothesis, success metric, kill criteria, appetite |
| 06 | `prioritization` | initiative scores and ranks | `scripts/prioritize.py` |
| 07 | `portfolio-balance` | balance notes | mix of safe and bold bets, capacity |
| 08 | `outcome-roadmap` | initiatives by Now / Next / Later | each initiative links a bet |
| 09 | `dependency-map` | depends_on, durations | `scripts/dependencies.py` |
| 10 | `kpi-tree` | kpis | north star, inputs, guardrails, baselines |
| 11 | `decision-brief` | — (export) | only approved claims |
| 12 | `bet-scorecard` | scorecard | result vs success metric; scale / iterate / kill |

After each step: run `python scripts/canvas_check.py canvas-output/canvas.json`. Fix errors before moving on, and report gaps to the user.

## Render

```
python scripts/render_canvas.py canvas-output/canvas.json -o canvas-output/
```

This produces:
- `canvas.html`: one interactive page. Click any card to light up its full chain.
- Five SVGs for decks and docs: opportunity tree, prioritization matrix, roadmap, dependencies, KPI tree.

Share the HTML as an artifact when the user wants a page to keep or share.

## Answer "why is this on the roadmap?"

```
python scripts/canvas_check.py canvas-output/canvas.json --why I3
```

This prints the chain from initiative to bet to opportunity to need to evidence to source, plus the success metric and kill criteria. Use it whenever someone challenges a roadmap item.

## Export

```
python scripts/export.py canvas-output/canvas.json -o canvas-output/
```

This produces three files:
- `backlog.csv`: epics per bet and stories per initiative, for Jira or Linear. Refine the stories with `backlog-builder`.
- `prd-inputs/B#.md`: one PRD starter per bet, for `prd-writer`.
- `deck-brief.md`: the action-title spine for a leadership readout.

## Scripts (Python 3, standard library only)

| Script | Does |
|---|---|
| `canvas_check.py` | Broken links, orphans, uncovered top needs, bets without metrics or kill rules, KPIs without baselines, evidence strength per bet; `--why ID` traces any item |
| `prioritize.py` | RICE, ICE or WSJF scores; stability over 1,000 jittered runs; flags low-confidence leaders and items ranked above their dependencies; `--write` stores ranks |
| `dependencies.py` | Cycles, critical path, slack, coordination hotspots, SVG graph |
| `render_canvas.py` | Interactive canvas page and five SVGs |
| `export.py` | Backlog CSV, PRD inputs, deck brief |

## Templates (`assets/templates/`)

`canvas-blank.json`, `canvas.json` (filled fictional example), `bet-card.md`, `scorecard.md`, `review-cadence.md`.

A fictional end-to-end run is in `examples/worked-example.md`, with rendered outputs in `examples/sample-output/`. Test prompts are in `evals/evals.json`.

## Credits

Opportunity Solution Tree (Teresa Torres), RICE (Intercom), ICE (Sean Ellis), WSJF (Don Reinertsen; SAFe), outcome-based roadmaps (Josh Seiden, Jeff Gothelf), Now/Next/Later (Janna Bastow), North Star framework (Amplitude), Outcome-Driven Innovation (Tony Ulwick).
