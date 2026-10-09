# 08 · Outcome Roadmap

**Stage:** Decide · **Updates:** `initiative horizon`

## Purpose

Place initiatives in Now / Next / Later, grouped by the bet and outcome they serve, instead of a date-driven feature list.

## Inputs

- Ranked initiatives
- Capacity
- Dependencies (if known)

## Steps

1. Now: committed, sized, fits capacity. Next: likely, shaped but not committed. Later: exploring, may change.
2. Every initiative links to a bet; show the bet and the KPI it moves.
3. Respect dependencies: a Now item cannot depend on Next or Later work (the dependency script warns).
4. Use dates only where there is a real external commitment; otherwise use horizons.
5. Put measurement work (missing baselines) in Now.

## Check before moving on

- [ ] No orphan initiatives.
- [ ] Now fits capacity.
- [ ] Missing baselines scheduled.
- [ ] `python scripts/canvas_check.py canvas-output/canvas.json` has no errors

## Common mistake

- A roadmap of features with no outcome attached.
