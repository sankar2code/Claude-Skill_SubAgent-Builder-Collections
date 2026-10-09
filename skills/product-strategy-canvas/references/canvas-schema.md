# canvas.json schema

One file holds the whole strategy. Every item has an `id` and links to the items above it. Arrays may be empty. The filled example is `assets/templates/canvas.json`.

```
S source ─► E evidence ─► N need ─► O opportunity ─► B bet ─► I initiative
                                        │               │
                                        └─ G goal       └─ K success metric ─► KPI tree
```

## meta
| Field | Notes |
|---|---|
| product | Product or area name |
| objective | One sentence: the outcome this strategy is for |
| owner | Role or name the user supplied |
| as_of | Date (YYYY-MM-DD) |
| mode | quick, full or review |
| prioritization | rice, ice or wsjf |
| balance | Portfolio balance note (written at step 07) |

## sources `S#`
`id, title, date, type` (primary-internal, primary-external, secondary, expert, model-output). Model output is never a source for a FACT.

## evidence `E#`
`id, text, source (S#), label (FACT|ESTIMATE|INFERENCE|HYPOTHESIS|UNKNOWN), strength (strong|moderate|weak|assumed)`
One observation per item. Quotes only verbatim.

## needs `N#`
`id, text, segment, importance (1-10), satisfaction (optional, 1-10), evidence [E#], label`
Write as a customer outcome ("minimize time to…"), not a feature.

## goals `G#`
`id, text, metric (K#), label`
Usually one goal per canvas.

## opportunities `O#`
`id, text, needs [N#], goal (G#)`
A customer problem worth solving, not a solution.

## choices `C#`
`id, we_will, we_wont, rationale`

## bets `B#`
`id, title, hypothesis ("If we…, then…"), opportunities [O#], success_metric (K#), kill_criteria, appetite, confidence (0-1), label`

## initiatives `I#`
`id, title, bet (B#), horizon (now|next|later), duration_weeks, depends_on [I#]`, plus prioritization inputs:
- RICE: `reach` (per period), `impact` (0.25 / 0.5 / 1 / 2 / 3), `confidence` (0-1), `effort` (person-months or weeks; use one unit)
- ICE: `impact`, `confidence`, `ease` (1-10 each)
- WSJF: `business_value`, `time_criticality`, `risk_reduction`, `job_size` (relative, e.g. Fibonacci)
`score` and `rank` are written by `prioritize.py --write`.

## kpis `K#`
`id, name, type (north_star|input|guardrail|counter), parent (K# or null), formula (optional), baseline, target, source (S#, optional), owner_role`

## scorecard
`bet (B#), review_date, metric (K#), result, label, decision (scale|iterate|kill), learned`

## Rules the checker enforces
- IDs unique; every reference exists; no circular dependencies
- Every evidence item has a source; FACT and ESTIMATE always do
- Needs cite evidence; opportunities cite needs; bets cite opportunities; initiatives cite a bet
- Top needs (importance ≥ 8) are covered by an opportunity
- Bets have a success metric and kill criteria
- KPIs (except the north star) have a parent; missing baselines are reported
