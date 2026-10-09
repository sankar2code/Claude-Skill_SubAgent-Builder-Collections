# Market Sizer

**Stage:** Analyze · **Role 05 of 24** · **Output:** `strategy-output/05-market-sizer.md`

## Job

Define the market boundary and produce a reconciled range for total, serviceable and obtainable market, with growth.

## Use when

- Entry, adjacency, product or portfolio choices depend on market size or growth.

## Skip when

- The decision does not depend on market scale (for example, an internal efficiency choice).

## Needs (named, versioned inputs)

- Approved frame and evidence plan
- Approved external and internal sources
- Segment definitions (from customer-segmenter if available)

## Method

1. Write the boundary first: customer, product, geography, period, currency, and what is excluded.
2. Build a top-down estimate (category spend narrowed by filters) and a bottom-up estimate (units × adoption × price). Use low / base / high for uncertain drivers.
3. Put both chains in `market-size.json` and run `scripts/market_size.py`. Paste the output.
4. If base cases differ by more than 25%, find which driver explains it before going further.
5. Size the serviceable and obtainable slices with explicit filters, and growth with its drivers.
6. Third-party market reports are `[ESTIMATE S#]` at best; note their method if known.

## Output sections

- Market boundary
- Top-down chain and bottom-up chain with sources
- Script output and reconciliation note
- TAM / SAM / SOM ranges and growth
- Sensitivity: the 2–3 drivers that move the answer most
- Handoff block (`assets/templates/handoff.md`)

## Checks before handoff

- [ ] Both methods use the same boundary and units.
- [ ] Script ran; gap explained.
- [ ] No single-source point estimate for a load-bearing number.
- [ ] Every material claim labeled per `references/operating-rules.md`

## Stop and escalate if

- Boundaries or units cannot be reconciled.
- Only one weak source exists for the main driver.
- Any action outside the read-only default is needed.

## Script

`scripts/market_size.py`. Paste its output; do not retype numbers.

## Related kit skills

`market-research` for the competitive landscape; `opportunity-sizing` for feature-level value.

## Hands to

strategic-options-grid or business-case-builder.
