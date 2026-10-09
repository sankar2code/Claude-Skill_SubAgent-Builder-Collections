# 06 · Prioritization

**Stage:** Synthesize · **Updates:** `initiative score and rank`

## Purpose

Score the initiatives under each bet with one consistent method, test how stable the ranking is, and flag rankings that rest on guesses.

## Inputs

- Initiatives with RICE, ICE or WSJF inputs (from the team, not the PM alone)

## Steps

1. Pick one method for the whole canvas (`meta.prioritization`): RICE for growth and adoption work, ICE for quick experiments, WSJF for flow-based teams and cost of delay.
2. Collect inputs from the people who know them (effort from engineering, reach from data).
3. Run `python scripts/prioritize.py canvas-output/canvas.json --write`.
4. Read the flags: low-confidence leaders (validate first), unstable ranks, items ranked above their dependencies.
5. Adjust only with a written reason. Strategic must-dos are allowed, but labelled as overrides.

## Check before moving on

- [ ] One method across all items.
- [ ] Inputs sourced.
- [ ] Overrides written down.
- [ ] `python scripts/canvas_check.py canvas-output/canvas.json` has no errors

## Common mistake

- Tuning inputs until the favorite wins.

## Script

`scripts/prioritize.py`. Paste its output; do not retype numbers.
