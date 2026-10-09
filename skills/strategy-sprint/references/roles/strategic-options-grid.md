# Strategic Options Grid

**Stage:** Decide · **Role 11 of 24** · **Output:** `strategy-output/11-strategic-options-grid.md`

## Job

Design 3–4 real, internally coherent options (plus the status quo) and the explicit non-choices each implies, then score them against the pre-agreed criteria.

## Use when

- A decision is framed as yes / no.
- Token alternatives are hiding a preferred answer.

## Skip when

- The choice is already made and approved; go to Execute.

## Needs (named, versioned inputs)

- Approved frame with criteria and weights
- Reconciled evidence from Analyze roles

## Method

1. For each option describe: where to play, how to win, capabilities needed, management systems, economics, and what we will explicitly not do.
2. Make options different in kind, not degree. Include status quo and at least one bold option.
3. For each option, list what would have to be true for it to be the best choice.
4. Score options 1–5 on each agreed criterion with the evidence for each score. Put weights and scores in `criteria.json` and run `scripts/weighted_score.py`.
5. Report whether the winner is fragile (changes when a weight moves by 10 points).
6. Shortlist for Gate 2. Do not select a final option.

## Output sections

- Options grid (use `assets/templates/options-grid.md`)
- What must be true per option
- Scores with evidence
- Script output and fragility note
- Proposed shortlist for Gate 2
- Handoff block (`assets/templates/handoff.md`)

## Checks before handoff

- [ ] Options are coherent and genuinely different.
- [ ] Criteria weights are the ones agreed at Gate 1.
- [ ] Status quo is scored.
- [ ] Every material claim labeled per `references/operating-rules.md`

## Stop and escalate if

- Criteria or weights were changed after evidence arrived without owner approval.
- Any action outside the read-only default is needed.

## Script

`scripts/weighted_score.py`. Paste its output; do not retype numbers.

## Hands to

build-buy-partner, pricing-strategist, business-case-builder or portfolio-reviewer, after Gate 2.
