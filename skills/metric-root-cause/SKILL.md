---
name: metric-root-cause
description: >
  Finds the specific, actionable reason a product or business metric changed, by
  ruling out data problems first, then splitting the change into "who the users are"
  (mix) versus "how they behave" (rate), and drilling down dimension by dimension.
  Use this skill when the user asks "why did X go up/down", "what's driving this drop",
  "investigate this metric", "root cause this", "explain this KPI change", or shares a
  chart or table showing a metric moving. Works with CSVs, SQL access, or numbers pasted
  into chat. Part of the Product Analytics pack.
---

> **Product Analytics pack · Stage 2.** `analytics-question-framing` → `metric-root-cause` / `cohort-retention` → `opportunity-sizing` → `experiment-design` → `insight-storyteller`

# Metric Root Cause

A metric moved and someone wants to know why. The goal is not a list of everything that changed; it's the **smallest true explanation that someone can act on**, with the evidence and a confidence level.

## Step 0 — Pin down the change

Confirm, in one line each:

- **Metric and definition:** exact formula, numerator and denominator (e.g. "activation = users completing setup within 7 days ÷ new signups").
- **The change:** from what to what, over which periods (e.g. "38.2% in Aug → 33.9% in Sep, −4.3 pts").
- **Comparison baseline:** previous period, same period last year, or forecast.

If any is unclear, ask before analyzing.

## Step 1 — Rule out "the data broke" first

Surprising metric moves are often measurement problems. Check, in this order:

1. **Tracking or pipeline changes:** a new app release, renamed or dropped events, a changed definition, late-arriving data, a backfill.
2. **Volume sanity:** did the denominator change sharply? Look at raw counts, not just the rate.
3. **Missing segments:** a platform, country or source suddenly at zero or null.
4. **Duplicates or bots:** spikes in a single user, IP or source.

If you find a data issue, stop and report it. The real change may be zero.

## Step 2 — Check the usual non-product suspects

- **Seasonality and calendar:** holidays, day-of-week mix, month length.
- **Marketing and acquisition:** a campaign started or ended, a new channel, paid spend changes.
- **External events:** outages, competitor launches, news, pricing changes.
- **Releases:** list product releases and experiments in the window.

## Step 3 — Split mix from rate

When a metric is a rate over a population made of segments (platform, channel, country, plan…), its change has two parts:

- **Mix effect:** the population shifted toward segments that naturally have a lower or higher rate. Nothing about the product changed.
- **Rate effect:** users within the same segments behaved differently. This is usually the product signal.

For segments *i* with population share *w* and rate *r*, from period 0 to period 1:

```
total change = Σ (w1ᵢ − w0ᵢ) · r0ᵢ        ← mix effect
             + Σ w1ᵢ · (r1ᵢ − r0ᵢ)        ← rate effect
```

The two parts add up exactly to the total change. If you have the data as a CSV, run `scripts/mix_rate.py` (in this skill's folder) to compute the split per segment:

```bash
python scripts/mix_rate.py data.csv --segment platform --period month --num activated --den signups --p0 2026-08 --p1 2026-09
```

Run it for each candidate dimension. The dimension where one or two segments explain most of the change is where to drill next.

## Step 4 — Drill down

Repeat Step 3 inside the segment that explains the most, using the next most plausible dimension (e.g. platform → app version → onboarding step). Stop when:

- one cut explains roughly 70% or more of the change, **and**
- you can name a concrete cause (a release, a broken step, a campaign, a policy change), **or**
- further cuts get too small to be reliable (flag the sample size).

At each level, check the change is bigger than normal week-to-week noise for that segment before treating it as real.

## Step 5 — Validate the explanation

- **Timing:** does the change start when the suspected cause started?
- **Dose:** where the cause is stronger, is the effect bigger?
- **Counterfactual:** do unaffected segments stay flat?
- **Alternative explanations:** say which ones you ruled out and how.

## Output: root-cause summary

```markdown
# Why <metric> changed: <period>
**Bottom line:** <one sentence: what changed, how much, and the main cause>
**Confidence:** High / Medium / Low, because <reason>

## What happened
- <metric> moved from <a> to <b> (<Δ>), vs a normal range of <±x>.
- Data checks: <passed / issue found>.

## Where it came from
| Segment | Mix effect | Rate effect | Share of total change |
|---|---|---|---|

## The cause
<2–4 sentences with the evidence: timing, dose, counterfactual>

## What to do
1. <action> · owner · expected effect
2. …

## Ruled out
- <hypothesis>: <why>
```

## When done

Offer the next step: `opportunity-sizing` to put a value on fixing it, or `experiment-design` if the fix should be tested before rollout.
