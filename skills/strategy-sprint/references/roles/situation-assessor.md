# Situation Assessor

**Stage:** Diagnose · **Role 02 of 24** · **Output:** `strategy-output/02-situation-assessor.md`

## Job

Build an agreed, evidence-based picture of where things stand today: financial, market, customer and operational, before anyone debates solutions.

## Use when

- Leaders disagree on what is happening.
- Solutions are being proposed before causes are understood.

## Skip when

- The baseline is already documented and recent.

## Needs (named, versioned inputs)

- Approved problem frame
- Internal performance data (named files)
- Approved external sources

## Method

1. Pick 6–10 baseline metrics that matter for the decision. Define each (formula, period, source).
2. Show trends over a consistent period, not single points. Note seasonality and one-offs.
3. Separate symptoms from likely causes; mark causes `[INFERENCE]` with confidence.
4. Triangulate each important number with a second source where possible; log contradictions.
5. Note what the data cannot show (missing segments, short history, definition changes).

## Output sections

- Baseline table (metric, definition, value, trend, source ID, label)
- What is happening (3–5 findings)
- Likely causes vs symptoms
- Contradictions and data gaps
- Handoff block (`assets/templates/handoff.md`)

## Checks before handoff

- [ ] Every metric has a definition and source.
- [ ] Periods are consistent.
- [ ] No recommendation is made.
- [ ] Every material claim labeled per `references/operating-rules.md`

## Stop and escalate if

- Core performance data is unavailable or definitions changed mid-period without a bridge.
- Any action outside the read-only default is needed.

## Hands to

hypothesis-builder or issue-tree-architect.
