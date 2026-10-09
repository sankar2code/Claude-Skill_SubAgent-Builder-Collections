# 10 · KPI Tree

**Stage:** Measure · **Updates:** `kpis`

## Purpose

Link the goal to a north star, the input metrics bets can move, and guardrails that catch harm, each with baseline, target and owner.

## Inputs

- Goal
- Bets and their success metrics

## Steps

1. One north star (`type: north_star`) tied to the goal.
2. 3–5 input metrics the team can move; every bet's success metric is one of them.
3. At least one guardrail or counter metric per risky bet (quality, trust, cost, fairness).
4. Baseline, target, source and owner role for each. Unknown baselines are `[UNKNOWN]` with a plan.
5. Review cadence from `assets/templates/review-cadence.md`.

## Check before moving on

- [ ] Every bet's metric is in the tree.
- [ ] Guardrails present.
- [ ] Baselines or a plan to get them.
- [ ] `python scripts/canvas_check.py canvas-output/canvas.json` has no errors

## Common mistake

- Vanity metrics with no link to customer value.

## Reuse from the kit

`kpi-architect` role in `strategy-sprint` for deeper threshold design.
