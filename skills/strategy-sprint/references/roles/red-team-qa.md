# Red-Team Q&A

**Stage:** Communicate · **Role 23 of 24** · **Output:** `strategy-output/23-red-team-qa.md`

## Job

Attack the recommendation independently from the seats of the CEO, CFO, operator, board member, regulator, customer and competitor, and find the load-bearing weak points.

## Use when

- Stakes are high, dissent may be hidden, or the meeting could expose a weak assumption.
- Always in Full mode.

## Skip when

- Quick mode (use the pre-mortem instead).

## Needs (named, versioned inputs)

- Recommendation, evidence pack, ledger and business case only. Not the reasoning that produced them.

## Method

1. Run in a fresh context (the `strategy-red-team` sub-agent, or a new chat).
2. For each seat, ask the 3 hardest questions that seat would ask.
3. Find the 3–5 load-bearing assumptions and test each against the evidence.
4. Check the numbers: recompute one key figure from the ledger.
5. Rate each challenge: fatal, material or minor. For each, say what evidence would resolve it.
6. Do not soften. Do not propose a new strategy.

## Output sections

- Questions by seat
- Load-bearing assumptions and their support
- Number check
- Challenges rated with resolution needed
- Handoff block (`assets/templates/handoff.md`)

## Checks before handoff

- [ ] Independent of the original framing.
- [ ] Every material challenge has a requested resolution.
- [ ] Every material claim labeled per `references/operating-rules.md`

## Stop and escalate if

- A fatal challenge cannot be resolved with available evidence; return to the coordinator before Gate 3.
- Any action outside the read-only default is needed.

## Hands to

Coordinator, who routes fixes back to earlier roles and records responses.
