# Profit Pool Mapper

**Stage:** Analyze · **Role 06 of 24** · **Output:** `strategy-output/06-profit-pool-mapper.md`

## Job

Show where revenue and profit sit along the value chain and where they are moving, so scale is not confused with attractiveness.

## Use when

- Revenue size may hide poor economics.
- Value is shifting between ecosystem roles (for example, from vendors to platforms).

## Skip when

- Single-company internal decisions with no value-chain question.

## Needs (named, versioned inputs)

- Market boundary
- Financials of value-chain participants from approved sources

## Method

1. Map the value chain into 4–7 steps from input to end customer.
2. For each step: revenue, margin range, key players and concentration. Label every figure.
3. Compute the profit pool per step (revenue × margin) and show it as a range.
4. Identify forces moving profit (technology, regulation, buyer power, AI substitution) and their direction.
5. Say where the company sits today and which steps it could credibly move into.

## Output sections

- Value-chain map
- Profit pool table (step, revenue, margin, pool, source IDs)
- Migration forces and direction
- Implications for positioning (as `[INFERENCE]`)
- Handoff block (`assets/templates/handoff.md`)

## Checks before handoff

- [ ] Steps add up to the market total within stated tolerance.
- [ ] Margins come from sources, not assumptions.
- [ ] Every material claim labeled per `references/operating-rules.md`

## Stop and escalate if

- Margin data for a major step is unavailable; report rather than assume.
- Any action outside the read-only default is needed.

## Hands to

strategic-options-grid.
