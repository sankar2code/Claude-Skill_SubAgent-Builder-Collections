# 11 · Decision Brief

**Stage:** Decide · **Updates:** `(export only)`

## Purpose

Package the canvas for the people who must approve it: the bets, the Now scope and the review date.

## Inputs

- A canvas that passes `canvas_check.py`

## Steps

1. Run `python scripts/export.py canvas-output/canvas.json -o canvas-output/ --brief`.
2. Fill the action titles: each a full sentence a reader could repeat.
3. Attach the rendered visuals (canvas.html or the SVGs).
4. State the ask exactly: which bets, which Now scope, which review date, which open risks are accepted.
5. For a governed decision (board, big budget), hand to `strategy-sprint` instead of this brief.

## Check before moving on

- [ ] Only claims present in the canvas.
- [ ] Ask is specific.
- [ ] `python scripts/canvas_check.py canvas-output/canvas.json` has no errors

## Common mistake

- Presenting the canvas as decided before approval.

## Reuse from the kit

`insight-storyteller` for a short readout; `decision-memo-writer` role in `strategy-sprint` for a formal memo.
