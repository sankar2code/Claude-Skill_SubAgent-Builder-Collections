# Business Case Builder

**Stage:** Decide · **Role 14 of 24** · **Output:** `strategy-output/14-business-case-builder.md`

## Job

Translate each shortlisted option into a driver-based case: revenue, cost, cash, NPV, IRR, payback, sensitivity and the break-even conditions.

## Use when

- Capital, pricing, share, timing or cost could change the choice.

## Skip when

- Quick mode with a reversible, low-cost choice; use a simple cost-benefit line instead.

## Needs (named, versioned inputs)

- Shortlisted options
- Market, pricing, cost and regulatory inputs with source IDs
- Discount rate and horizon from the work order

## Method

1. Build each case from drivers (volume × price × margin, cost lines), not from a target result.
2. Use the same horizon, currency, discount rate and status-quo baseline for every option. Value is incremental to status quo.
3. Put the cases in `business-case.json` and run `scripts/business_case.py`. Paste the output.
4. Run sensitivities on every driver (the script does ±20% by default) and report the top 3.
5. Report break-even: the value each key driver must reach for NPV to be zero.
6. Low / base / high scenarios with named assumptions. Never present only the base case.

## Output sections

- Driver tree per option
- Assumption table (driver, value, range, source / label)
- Script output: NPV, IRR, payback, sensitivity, break-even
- Scenario summary
- What the numbers do not include
- Handoff block (`assets/templates/handoff.md`)

## Checks before handoff

- [ ] Totals recomputed by script.
- [ ] Same baseline and discount rate across options.
- [ ] Every driver labeled and sourced.
- [ ] Every material claim labeled per `references/operating-rules.md`

## Stop and escalate if

- Cash flows depend on an input nobody can supply; mark `[OWNER NEEDED]` and stop for that option.
- Any action outside the read-only default is needed.

## Script

`scripts/business_case.py`. Paste its output; do not retype numbers.

## Related kit skills

`opportunity-sizing` for single-feature value estimates.

## Hands to

strategic-options-grid (rescore), pyramid-story-builder, or Execute roles after Gate 2.
