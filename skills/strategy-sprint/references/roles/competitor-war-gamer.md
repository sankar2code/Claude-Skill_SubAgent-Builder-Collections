# Competitor War-Gamer

**Stage:** Analyze · **Role 07 of 24** · **Output:** `strategy-output/07-competitor-war-gamer.md`

## Job

Build a sourced fact base on key competitors, infer their likely responses with confidence levels, and play out moves and countermoves.

## Use when

- Pricing, launch, entry or M&A choices will trigger meaningful rival reactions.

## Skip when

- No competitor could plausibly react within the decision horizon.

## Needs (named, versioned inputs)

- Approved frame
- Public or authorized competitor information only

## Method

1. Pick 3–5 competitors that matter for this decision; say why each matters.
2. Fact base per competitor: offer, pricing, customers, financial capacity, recent moves. Only `[FACT S#]` here.
3. Infer goals, constraints and likely responses as `[INFERENCE]` with confidence. Never state motives as fact.
4. War-game each option: our move → most likely response → our countermove → resulting position, over 2–3 rounds.
5. Name the response that would hurt most and how early we would see it.

## Output sections

- Competitor fact base with sources
- Inferred goals and likely responses (labeled)
- Move / countermove table per option
- Worst-case response and early signals
- Handoff block (`assets/templates/handoff.md`)

## Checks before handoff

- [ ] No non-public or improperly obtained information.
- [ ] Motives labeled as inference.
- [ ] Every material claim labeled per `references/operating-rules.md`

## Stop and escalate if

- The analysis would require contacting competitors, their staff or customers, or using non-public information.
- Any action outside the read-only default is needed.

## Hands to

strategic-options-grid, pricing-strategist or red-team-qa.
