---
name: analytics-question-framing
description: >
  Turns a vague business problem into a short list of prioritized, answerable analytics
  questions, each tied to the decision it informs, a testable hypothesis, and the exact
  data needed. Use this skill before any analysis starts: when a user says things like
  "why is X happening", "we need to look into Y", "help me scope this analysis", "what
  should we analyze", "frame this question", or shares a business problem, KPI concern,
  or stakeholder request without a clear analytical question. Stage 1 of the Product
  Analytics pack.
---

> **Product Analytics pack · Stage 1.** `analytics-question-framing` → `metric-root-cause` / `cohort-retention` → `opportunity-sizing` → `experiment-design` → `insight-storyteller`

# Analytics Question Framing

Most analyses go wrong before the first query: the question is too broad, nobody agreed what decision it serves, or the data can't answer it. Your job is to fix that up front, in a few minutes, so the analysis that follows is fast and useful.

## Step 1 — Understand the ask

Read what the user gave you and extract:

- **The trigger:** what happened or what someone noticed (e.g. "activation dropped", "the VP asked about churn").
- **The decision:** what someone will do differently depending on the answer. If no decision is stated, ask: *"What would you do differently if the answer were A versus B?"* An analysis with no decision attached is a report, not an analysis. Say so politely.
- **The audience:** who will read the result and how much time they have.
- **The deadline and the effort it deserves.**
- **The data available:** tables, tools, event tracking, known gaps.

If two or more of these are missing and you can't reasonably infer them, ask in one short batch of questions. Otherwise state your assumptions and continue.

## Step 2 — Generate candidate questions

Write 6–10 candidate questions. Make each one:

- **Specific:** names a metric, a population, and a time window. "Why is engagement down?" becomes "Which user segments drove the drop in weekly active users from August to September?"
- **Answerable with the available data** (or flag what's missing).
- **Neutral:** it doesn't assume the answer.

Cover different angles: *what* changed (descriptive), *where* and *who* (segmentation), *why* (drivers), *how much it matters* (sizing), and *what to do* (intervention).

## Step 3 — Prioritize

Score each question 1–3 on:

| Criterion | Question to ask |
|---|---|
| Decision impact | Does the answer change the decision? |
| Answerability | Can we answer it with the data we have, at the needed confidence? |
| Effort | How long will it take? (3 = quick) |

Keep the top 3–5. Put the rest in a "parked" list with one line on why.

## Step 4 — Attach hypotheses and data needs

For each kept question, write:

- **Hypotheses:** 2–3 plausible explanations, including at least one "boring" one (data or tracking issue, seasonality, a release, a mix shift in who the users are).
- **What would confirm or reject each:** the specific pattern you'd expect to see.
- **Data needed:** tables or events, fields, grain, time window, and any known quality risks.
- **Method:** the simplest method that answers it (a cut by segment, a funnel, a cohort table, a before/after with a control).

## Output: question brief

Write `question-brief.md` (or show it in chat if the user prefers):

```markdown
# Question brief: <topic>
**Decision this informs:** <one sentence>
**Audience:** <who> · **Needed by:** <date> · **Effort:** <hours/days>

## Priority questions
### Q1. <specific question>
- Why it matters: <link to the decision>
- Hypotheses: H1 <…> (confirm if …) · H2 <…> · H3 data/tracking issue (confirm if …)
- Data: <tables/events, fields, window>
- Method: <approach>

### Q2. …

## Parked questions
- <question>: <why parked>

## Risks and open items
- <data gaps, definitions to agree, people to check with>
```

## When done

Ask: *"Does this brief match the decision you're trying to make? Once you're happy, I can start on Q1."* Suggest the next skill: `metric-root-cause` for "why did a number move", `cohort-retention` for retention and lifecycle questions, `opportunity-sizing` for "how much is this worth".
