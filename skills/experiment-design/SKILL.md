---
name: experiment-design
description: >
  Designs a trustworthy A/B test (or a quasi-experiment when randomizing isn't
  possible): hypothesis, primary and guardrail metrics, randomization unit, minimum
  detectable effect, sample size and duration, and decision rules written down before
  launch. Use this skill when the user says "design an A/B test", "how long should this
  test run", "how many users do I need", "is this test big enough", "set up an
  experiment", "test this feature", or "how do we measure the impact of this launch".
  Part of the Product Analytics pack.
---

> **Product Analytics pack · Stage 4.** `analytics-question-framing` → `metric-root-cause` / `cohort-retention` → `opportunity-sizing` → `experiment-design` → `insight-storyteller`

# Experiment Design

The most expensive experiment is one that runs for weeks and then can't answer the question. Design it so the result, whatever it is, leads to a decision.

## Step 1 — Hypothesis

Write it in this form:

> If we **<change>** for **<population>**, then **<primary metric>** will **<increase/decrease>** by at least **<MDE>**, because **<reason>**.

If the user can't state the reason, the test may be premature. Say so.

## Step 2 — Metrics

- **Primary metric (one):** the metric the decision rests on. It must move within the test window and be sensitive to the change.
- **Guardrail metrics (2–4):** things that must not get worse: revenue, latency, errors, unsubscribes, support tickets, a key downstream step.
- **Secondary metrics:** to understand *why*, not to decide.

Write the exact definition and the analysis unit of each.

## Step 3 — Randomization

- **Unit:** user, account, session, or region. Use the unit at which the experience is consistent. If users in one account share an experience, randomize by account.
- **Split:** 50/50 unless risk calls for a smaller treatment group.
- **Eligibility:** who enters the test and at what moment (trigger the assignment when the user first reaches the changed experience, not at login, to avoid diluting the effect).
- **Interference:** if treated users affect control users (marketplaces, social features, shared inventory), use cluster or geo randomization, or a switchback design.

## Step 4 — Sample size and duration

Choose the **minimum detectable effect (MDE)**: the smallest change worth acting on (use `opportunity-sizing` to decide what's worth it). Use 95% confidence (α = 0.05, two-sided) and 80% power unless there's a reason not to.

For a conversion-rate metric, sample size **per group**:

```
n = (z₁₋α/₂ + z₁₋β)² × [p₁(1−p₁) + p₂(1−p₂)] / (p₂ − p₁)²
```

For a mean metric with standard deviation σ and absolute effect δ: `n = 2 × (z₁₋α/₂ + z₁₋β)² × σ² / δ²`.

Run `scripts/sample_size.py` (in this skill's folder) to compute it and the duration:

```bash
python scripts/sample_size.py --baseline 0.12 --mde-rel 0.05 --daily-users 8000
python scripts/sample_size.py --mean 42 --sd 30 --mde-abs 1.5 --daily-users 8000
```

Duration rules:
- Run **whole weeks** (at least one, usually two) so weekday and weekend behavior are both covered.
- If the required duration is more than about 4–6 weeks, the MDE is too small for the traffic. Raise the MDE, pick a more sensitive metric, or use a variance-reduction method such as CUPED (adjusting for each user's pre-period value).

## Step 5 — Decision rules (write before launch)

| Result | Decision |
|---|---|
| Primary metric up significantly, no guardrail harmed | Ship |
| Primary metric flat (confidence interval within ±MDE) | Don't ship for this reason; keep only if it has other value |
| Primary metric down, or a guardrail significantly harmed | Don't ship; investigate |
| Inconclusive (interval wide, crosses MDE) | Extend only if pre-planned; otherwise treat as flat |

## Step 6 — Pitfalls to guard against

- **Peeking:** don't stop as soon as p < 0.05. Fix the duration up front, or use a sequential testing method designed for repeated looks.
- **Sample ratio mismatch (SRM):** check the actual split matches the planned split (chi-square test). A mismatch means assignment or logging is broken, so don't trust the result.
- **Novelty effects:** new UI can spike engagement briefly. Compare week 1 to week 2.
- **Multiple comparisons:** many metrics or segments will produce false positives. Decide on the primary metric and key segments in advance.
- **Instrumentation:** verify events fire correctly in both groups before launch (an A/A test helps).

## When you can't randomize

Use the strongest available alternative, and say how strong the evidence is:

- **Difference-in-differences:** compare the change in the treated group with the change in a similar untreated group over the same period. Check the two trended in parallel beforehand.
- **Staggered rollout:** release region by region and compare regions that have it with those that don't yet.
- **Regression discontinuity:** when eligibility depends on a cut-off (e.g. accounts above 50 seats).
- **Pre/post:** the weakest; only with a long, stable baseline and no other changes in the window.

## Output: experiment plan

```markdown
# Experiment plan: <name>
**Hypothesis:** If we … then … by at least … because …
**Primary metric:** <definition> · **Guardrails:** <list>
**Unit / split / trigger:** <user, 50/50, on first visit to …>
**Baseline:** <value> · **MDE:** <abs and relative> · **α / power:** 0.05 / 0.80
**Sample size:** <n per group> · **Duration:** <weeks> at <daily eligible users>
**Decision rules:** <table>
**Checks:** SRM, A/A or event QA, novelty review
**Owner and readout date:** <…>
```

## When done

After the test, suggest `insight-storyteller` to write the readout.
