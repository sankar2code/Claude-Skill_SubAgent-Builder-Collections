---
name: cohort-retention
description: >
  Builds and interprets cohort retention: groups users by when (or how) they started,
  tracks what share come back in each later period, and explains what the curves say
  about product-market fit, onboarding, and churn. Use this skill when the user asks
  about retention, churn, "do users stick", "cohort analysis", "retention curve",
  "triangle chart", "are newer users better or worse", "lifetime value", or shares
  signup and activity data. Works from a CSV of user activity. Part of the Product
  Analytics pack.
---

> **Product Analytics pack · Stage 2.** `analytics-question-framing` → `metric-root-cause` / `cohort-retention` → `opportunity-sizing` → `experiment-design` → `insight-storyteller`

# Cohort Retention

Averages hide retention problems: a growing product can look healthy while every new cohort churns faster. Cohorts show whether the product is getting better at keeping people.

## Step 1 — Define it precisely

Agree on four things before computing anything:

| Choice | Options | Guidance |
|---|---|---|
| **Cohort** | signup week/month, first purchase, acquisition channel, plan | Start with signup period; split by channel or plan next |
| **Return event** | any activity, a core action, a purchase | Use the action that represents real value (e.g. "created a report"), not just a login |
| **Period** | day, week, month | Match the natural usage frequency: daily apps by day/week, B2B tools by week/month |
| **Retention type** | classic (active in period N), unbounded (active in N or later), rolling | Classic is the default and the easiest to explain |

## Step 2 — Build the table

If the data is a CSV with one row per activity event (`user_id`, `event_date`, optionally `signup_date` and a segment column), run `scripts/cohort_table.py` (in this skill's folder):

```bash
python scripts/cohort_table.py events.csv --user user_id --date event_date --period month
python scripts/cohort_table.py events.csv --user user_id --date event_date --signup signup_date --period week --segment channel
```

It prints a retention triangle (cohort × periods since start, as % of cohort size) and can save it as CSV with `--out`. If there's no signup column, each user's first event counts as their start.

Leave cells blank where a cohort hasn't had time to reach that period. Don't treat them as zero.

## Step 3 — Read the curves

Look for these patterns and say which ones apply:

- **Flattening (good):** the curve drops early, then levels off. The level it settles at is the core retained audience. A curve that keeps declining toward zero suggests weak product-market fit for that cohort.
- **Early drop:** most loss happens between period 0 and 1. That points to onboarding and first value, usually the cheapest place to improve.
- **Newer cohorts better or worse:** compare the same period across cohorts (read down a column). Improving columns mean product changes are working.
- **Smile curve:** retention rising again in later periods (reactivation, seasonality, or a new feature bringing people back).
- **Segment gaps:** large differences by channel or plan often matter more than the overall trend.

Flag small cohorts (fewer than ~100 users) as noisy.

## Step 4 — Quantify

- **Retention at key milestones:** e.g. week 1, week 4, month 3.
- **Change across cohorts** at the same milestone, in percentage points.
- **Optional lifetime value:** if revenue per active user per period is known, LTV ≈ Σ (retention in period *t* × revenue per active user) over the horizon. State the horizon and whether it's discounted.

## Output: retention summary

```markdown
# Retention: <product / population>, <period range>
**Definition:** cohort = <…>, return event = <…>, period = <…>
**Headline:** <one sentence, e.g. "Month-1 retention improved from 31% to 38% for cohorts after the June onboarding change; curves flatten around 22%.">

## Retention table
<triangle, or a link to the CSV>

## What it shows
- <pattern 1, with numbers>
- <pattern 2>

## Segments
| Segment | M1 | M3 | Note |
|---|---|---|---|

## Recommended actions
1. <action tied to the biggest drop-off>
```

## When done

Suggest `metric-root-cause` if a cohort or segment suddenly got worse, or `opportunity-sizing` to value a retention improvement.
