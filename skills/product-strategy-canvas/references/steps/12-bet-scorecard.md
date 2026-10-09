# 12 · Bet Scorecard

**Stage:** Measure · **Updates:** `scorecard, evidence, bet confidence`

## Purpose

After a bet ships, compare the result to its success metric and kill rule, decide scale / iterate / kill, and feed what was learned back into the canvas.

## Inputs

- Bet, its success metric and kill criteria
- Actual results with source

## Steps

1. Record the result against the metric with a source (`label: FACT` only if measured).
2. Compare with the target and the kill rule set in advance. Do not move the goalposts.
3. Decide: scale (hit target), iterate (partial, with a specific change), kill (hit kill rule).
4. Write what was learned, and update the canvas: new evidence items, confidence of related bets, needs that turned out bigger or smaller.
5. Re-render the canvas so the scorecard appears.

## Check before moving on

- [ ] Result sourced.
- [ ] Decision follows the pre-set rule.
- [ ] Learning written back as evidence.
- [ ] `python scripts/canvas_check.py canvas-output/canvas.json` has no errors

## Common mistake

- Declaring success on a metric that was not the success metric.

## Reuse from the kit

`experiment-design` for test readouts.
