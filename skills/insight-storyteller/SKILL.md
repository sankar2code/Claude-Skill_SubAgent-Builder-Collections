---
name: insight-storyteller
description: >
  Turns analysis results into a decision-ready story: a one-line answer, a short
  executive summary, a slide-by-slide outline with the right chart for each point, and
  stakeholder messages for Slack, email, and leadership. Use this skill when the user
  says "write up these findings", "make a readout", "turn this into a deck/story",
  "executive summary", "how do I present this", "draft the update for leadership",
  "experiment readout", or shares analysis output that needs to be communicated.
  Final stage of the Product Analytics pack.
---

> **Product Analytics pack · Stage 5.** `analytics-question-framing` → `metric-root-cause` / `cohort-retention` → `opportunity-sizing` → `experiment-design` → `insight-storyteller`

# Insight Storyteller

Stakeholders don't need everything you found. They need the answer, why they should believe it, and what to do. Lead with that; put the method in the appendix.

## Step 1 — Find the one thing

Before writing anything, complete this sentence in under 25 words:

> **"We found <insight>, which means <implication>, so we recommend <action>."**

If you can't, the analysis isn't finished. Say which question is still open instead of padding the story.

## Step 2 — Structure: Situation → Complication → Resolution

Use this order (the Minto "SCR" structure, with the answer first):

1. **Answer first:** the one-line insight and recommendation.
2. **Situation:** what the audience already knows and agrees with (the baseline, the goal).
3. **Complication:** what changed or what's at risk. This is why it matters now.
4. **Resolution:** the evidence (3 points maximum), the recommendation, its expected impact, and the ask (decision, budget, owner, date).

## Step 3 — Match each point to a chart

| The point is about… | Use | Avoid |
|---|---|---|
| Change over time | Line chart, with the event annotated | Pie charts, 3D |
| Comparing groups | Sorted horizontal bar chart | Unsorted bars, too many colors |
| Part of a whole changing | Stacked bar (≤ 5 parts) or waterfall | Multiple pies |
| What drove a change | Waterfall (mix vs rate, or by segment) | Long tables |
| Retention | Cohort curves or a heat-mapped triangle | Single averages |
| Experiment result | Point estimate with confidence interval vs zero | Bars without error ranges |

Every chart gets an **action title** that states the takeaway ("Android drove 80% of the activation drop"), not a label ("Activation by platform"). Highlight the one series that matters and grey out the rest.

## Step 4 — Calibrate confidence honestly

State how sure you are and why: sample size, data quality, causal versus correlational evidence. Use plain words: "We're confident…", "The evidence suggests…", "We can't yet tell whether…". Never overstate a correlation as a cause.

## Step 5 — Write for each audience

Produce what the user needs from this list:

- **Executive summary** (5 lines): answer, why, impact in numbers, recommendation, ask.
- **Slide outline** (6–10 slides): title slide with the answer → situation → complication → 2–3 evidence slides → recommendation and impact → next steps and owners → appendix (method, definitions, caveats).
- **Slack update** (3–4 lines, plus a link to details).
- **Email to leadership** (subject line that states the finding, 1 short paragraph, bullets, the ask).
- **Speaker notes** for each slide (what to say, the question you'll likely get, and the answer).

## Output template

```markdown
# <Action title: the insight in one line>

**Recommendation:** <action> · **Impact:** <number, range> · **Ask:** <decision needed, by when>
**Confidence:** <High/Medium/Low>, because <reason>

## Executive summary
1. …
2. …

## Slide outline
| # | Action title | Chart | Key number | Speaker note |
|---|---|---|---|---|

## Messages
**Slack:** …
**Email subject:** …
**Email body:** …

## Appendix
- Method and definitions
- Caveats and what we couldn't test
```

## Quality check before handing over

- Could a busy executive get the point from the title and first line alone?
- Does every slide title state a takeaway?
- Is every number traceable to the analysis, with units and time period?
- Are caveats present but not burying the message?
- Is there a clear owner and date for the next step?

If the user has slide tooling available (for example a PowerPoint or Slides skill), offer to build the deck from the outline.
