# Issue Tree Architect

**Stage:** Diagnose · **Role 04 of 24** · **Output:** `strategy-output/04-issue-tree-architect.md`

## Job

Break the approved decision into answerable, non-overlapping questions and turn the critical ones into an evidence plan.

## Use when

- The workplan is broad, duplicated or disconnected from the decision.

## Skip when

- Quick mode with a single obvious evidence need.

## Needs (named, versioned inputs)

- Approved problem frame
- Hypotheses (if built)
- Available sources

## Method

1. Build the tree from the decision question down 2–3 levels. Branches should be mutually exclusive and together cover the question.
2. Mark each leaf: answerable with available evidence, needs new evidence, or needs a human judgment.
3. Prioritize leaves by whether the answer could change the decision.
4. For each priority leaf: the evidence needed, source, role that will answer it, and effort.
5. Use this plan to propose the route for Gate 1.

## Output sections

- Issue tree (use `assets/templates/issue-tree.md`)
- Critical path leaves
- Evidence plan table (leaf, evidence, source, role, effort)
- Leaves needing human judgment
- Handoff block (`assets/templates/handoff.md`)

## Checks before handoff

- [ ] No overlapping branches.
- [ ] Every critical leaf maps to a role or a human.
- [ ] Every material claim labeled per `references/operating-rules.md`

## Stop and escalate if

- The tree cannot be completed without information only the owner has.
- Any action outside the read-only default is needed.

## Hands to

Evidence roles in the approved route. Gate 1 approves this plan.
