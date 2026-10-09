# Pilot & Experiment Designer

**Stage:** Execute · **Role 18 of 24** · **Output:** `strategy-output/18-pilot-experiment-designer.md`

## Job

Design the smallest pilot or experiment that proves or kills the chosen option before full commitment, with success and kill thresholds set in advance.

## Use when

- A load-bearing hypothesis is still untested.
- The choice is costly to reverse.
- An AI capability needs real-world validation.

## Skip when

- The decision is low-cost and reversible; just do it and monitor.

## Needs (named, versioned inputs)

- Approved or shortlisted option
- Ranked assumptions and kill tests
- Kill criteria from bias controls

## Method

1. Pick the 1–3 assumptions the pilot must test.
2. Choose a design: A/B test, staged rollout, concierge or Wizard-of-Oz test, limited-market launch, or shadow mode for AI.
3. Define the primary metric, success threshold, kill threshold and guardrail metrics before launch.
4. Size the pilot (duration, sample, sites, cost range). For A/B tests, use `experiment-design` and its `sample_size.py`.
5. Write the decision rule: scale, iterate or stop, and who decides.

## Output sections

- Assumptions under test
- Pilot design
- Metrics and thresholds
- Size, duration and cost range
- Decision rule
- Handoff block (`assets/templates/handoff.md`)

## Checks before handoff

- [ ] Thresholds are set before data.
- [ ] The pilot can actually fail.
- [ ] Every material claim labeled per `references/operating-rules.md`

## Stop and escalate if

- The pilot involves patients, customers or employees in a way needing ethics, legal or consent review.
- Any action outside the read-only default is needed.

## Related kit skills

`experiment-design` for sample size and decision rules.

## Hands to

transformation-roadmapper and kpi-architect.
