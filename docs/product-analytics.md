# Product Analytics pack

Six Claude skills that cover a product analytics question from start to finish: frame it, find the cause, put a value on it, test it, and tell the story. They work in Claude Code or claude.ai, with a CSV, SQL access, or numbers pasted into chat. Three include small standard-library Python scripts, so there's nothing to install.

```
analytics-question-framing ──► metric-root-cause ──┐
        (what to ask)          cohort-retention ───┼──► opportunity-sizing ──► experiment-design ──► insight-storyteller
                               (why / who)         │      (how much)            (prove it)            (tell it)
```

| Skill | Use it when | Output | Script |
|---|---|---|---|
| `analytics-question-framing` | A request is vague: "look into churn" | Question brief: prioritized questions, hypotheses, data needs | |
| `metric-root-cause` | "Why did this metric drop?" | Root-cause summary with mix vs rate split and confidence | `mix_rate.py` |
| `cohort-retention` | "Do users stick? Are new cohorts better?" | Retention triangle, curve patterns, actions | `cohort_table.py` |
| `opportunity-sizing` | "Is this worth building?" | Low/base/high value, driver tree, sensitivity, break-even | |
| `experiment-design` | "How do we test this? How long?" | Experiment plan: metrics, sample size, duration, decision rules | `sample_size.py` |
| `insight-storyteller` | "Write this up for leadership" | Answer-first summary, slide outline, Slack and email drafts | |

## Example run

1. *"Activation dropped from 38% to 34% last month. Help me figure out why."* → `analytics-question-framing` scopes it, then `metric-root-cause` rules out tracking issues and runs `mix_rate.py` by platform and channel.
2. *"What's it worth to fix the Android onboarding step?"* → `opportunity-sizing`.
3. *"Design a test for the new onboarding flow."* → `experiment-design` runs `sample_size.py`.
4. *"Write the readout for the VP."* → `insight-storyteller`.

## Principles behind the pack

- **Decision first.** Every analysis starts from the decision it informs.
- **Rule out broken data before explaining it.**
- **Ranges, not false precision.** Assumptions are visible and sourced.
- **Decide the rules before seeing the results.**
- **Lead with the answer.** Method goes in the appendix.
