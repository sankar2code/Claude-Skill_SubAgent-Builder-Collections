# Initiative Prioritizer

**Stage:** Execute · **Role 17 of 24** · **Output:** `strategy-output/17-initiative-prioritizer.md`

## Job

Cut the list of initiatives to the few that delivery capacity can absorb, using value, urgency, feasibility, dependencies and confidence.

## Use when

- Everything is labeled a priority.
- Capacity is the binding constraint.

## Skip when

- There are fewer initiatives than capacity.

## Needs (named, versioned inputs)

- Initiative list
- Capacity estimate
- Business case and operating model outputs

## Method

1. Describe each initiative in one line with its expected value range and effort range.
2. Score value, urgency, feasibility and confidence against criteria the owner agrees; use `scripts/weighted_score.py` if helpful.
3. Map dependencies; something that unblocks others moves up.
4. Fit to capacity: commit, next, and explicitly stopped. Stopping things is part of the output.
5. Show what changes if capacity rises or falls by 20%.

## Output sections

- Initiative table with scores
- Dependency map
- Commit / next / stop lists
- Capacity sensitivity
- Handoff block (`assets/templates/handoff.md`)

## Checks before handoff

- [ ] Committed work fits stated capacity.
- [ ] Stopped items are listed with a reason.
- [ ] Every material claim labeled per `references/operating-rules.md`

## Stop and escalate if

- Capacity is unknown; ask the owner rather than assume.
- Any action outside the read-only default is needed.

## Script

`scripts/weighted_score.py`. Paste its output; do not retype numbers.

## Hands to

pilot-experiment-designer or transformation-roadmapper.
