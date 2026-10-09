# 01 · Evidence Intake

**Stage:** Diagnose · **Updates:** `sources, evidence`

## Purpose

Collect what the team actually knows, one observation per item, each with a source and a strength. Contradictions are kept, not averaged.

## Inputs

- Research files, analytics exports, survey results, support tickets, sales notes, prior strategy docs
- Opportunity Finder or User Research outputs if they exist

## Steps

1. List every source as `S#` with date and type.
2. Extract observations as `E#`: one fact or finding per item, verbatim quotes only, with the source ID.
3. Rate strength (strong / moderate / weak / assumed) per `references/evidence-rules.md`.
4. Group related items and note where sources disagree. Keep both sides as separate items, and add a note naming the conflict.
5. List what is missing: segments not covered, metrics with no data, questions nobody has asked customers.

## Check before moving on

- [ ] Every item has a source and strength.
- [ ] No paraphrased "quotes".
- [ ] Contradictions visible.
- [ ] `python scripts/canvas_check.py canvas-output/canvas.json` has no errors

## Common mistake

- Summarizing instead of extracting: "users want speed" is not evidence; "9 of 12 interviewees re-type data" is.

## Reuse from the kit

`user-research` for raw interviews; `opportunity-finder` evidence and ledger import directly.
