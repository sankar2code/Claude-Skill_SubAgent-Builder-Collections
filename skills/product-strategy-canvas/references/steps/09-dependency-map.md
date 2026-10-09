# 09 · Dependency Map

**Stage:** Execute · **Updates:** `depends_on, duration_weeks`

## Purpose

Find what blocks what, the critical path, and where teams must coordinate.

## Inputs

- Initiatives with duration_weeks and depends_on

## Steps

1. Record dependencies between initiatives, and external ones as notes (other teams, vendors, approvals).
2. Run `python scripts/dependencies.py canvas-output/canvas.json -o canvas-output/dependencies.svg`.
3. Fix any cycle before anything else.
4. Name the critical path and its owner role; anything with zero slack needs early attention.
5. List coordination hotspots (items that block 2+ others) and the agreement needed for each.

## Check before moving on

- [ ] No cycles.
- [ ] Critical path named.
- [ ] External dependencies listed.
- [ ] `python scripts/canvas_check.py canvas-output/canvas.json` has no errors

## Common mistake

- Treating durations as promises; they are estimates.

## Script

`scripts/dependencies.py`. Paste its output; do not retype numbers.
