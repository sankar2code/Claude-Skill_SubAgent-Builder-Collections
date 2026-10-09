# Hypothesis Builder

**Stage:** Diagnose · **Role 03 of 24** · **Output:** `strategy-output/03-hypothesis-builder.md`

## Job

Convert what the team believes into falsifiable hypotheses, the assumptions that must be true for each, and the cheapest test that could kill it.

## Use when

- The team "already knows the answer".
- Evidence collection is sprawling.
- Confirmation bias is likely.

## Skip when

- The decision is purely about execution of an already-tested choice.

## Needs (named, versioned inputs)

- Approved problem frame
- Situation baseline (if available)
- Stated beliefs from stakeholders

## Method

1. Write each belief as a hypothesis that could be proven wrong, with who holds it.
2. For each, list the 2–4 must-be-true assumptions.
3. Rank assumptions by (impact if wrong) × (uncertainty).
4. For the top assumptions, define a kill test: the evidence, the threshold that would reject it, the cheapest way to get it, and how long it takes.
5. Include at least one hypothesis that argues against the favored answer.

## Output sections

- Hypothesis table (hypothesis, holder, must-be-true assumptions, label)
- Ranked assumptions
- Kill tests (evidence, threshold, method, time, cost)
- The contrarian hypothesis
- Handoff block (`assets/templates/handoff.md`)

## Checks before handoff

- [ ] Each hypothesis can fail.
- [ ] Thresholds are set before evidence is gathered.
- [ ] Every material claim labeled per `references/operating-rules.md`

## Stop and escalate if

- A load-bearing assumption fails its kill test: stop and report before more work is commissioned.
- Any action outside the read-only default is needed.

## Hands to

issue-tree-architect, or one targeted evidence role (early kill test route).
