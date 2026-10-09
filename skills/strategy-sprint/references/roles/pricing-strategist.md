# Pricing Strategist

**Stage:** Decide · **Role 13 of 24** · **Output:** `strategy-output/13-pricing-strategist.md`

## Job

Diagnose value, price structure and execution, and design pricing options tied to customer evidence and unit economics.

## Use when

- Growth, margin, packaging, discounting or monetization of a new product is central to the decision.

## Skip when

- Price is fixed by contract or regulation; note it and skip.

## Needs (named, versioned inputs)

- Customer segments and willingness-to-pay evidence
- Competitor pricing (public)
- Unit costs

## Method

1. Diagnose: value delivered per segment, current price realization, discount leakage, packaging fit.
2. Choose a value metric (what the customer pays per) that grows with value received.
3. Design 2–3 pricing options (structure, tiers, price points as ranges, discount rules).
4. Model volume, revenue and margin per option with assumptions labeled; hand the numbers to business-case-builder.
5. Predict competitor and customer reactions (link to competitor-war-gamer).
6. Define a test plan where possible instead of a big-bang change.

## Output sections

- Pricing diagnosis
- Value metric
- Pricing options
- Economics per option
- Reaction risks
- Test plan
- Handoff block (`assets/templates/handoff.md`)

## Checks before handoff

- [ ] Willingness-to-pay claims cite evidence or are `[HYPOTHESIS]`.
- [ ] Unit economics stay positive in the low case or the risk is flagged.
- [ ] Every material claim labeled per `references/operating-rules.md`

## Stop and escalate if

- Pricing evidence would require customer outreach or surveys (needs approval).
- Any action outside the read-only default is needed.

## Hands to

business-case-builder, then pilot-experiment-designer.
