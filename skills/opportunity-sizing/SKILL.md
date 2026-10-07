---
name: opportunity-sizing
description: >
  Puts a defensible value on a product opportunity, fix, or feature: a low / base / high
  range built from an explicit driver tree, with every assumption sourced and a
  sensitivity check showing which assumptions matter most. Use this skill when the user
  asks "how much is this worth", "size this opportunity", "what's the impact of fixing
  X", "build a business case", "estimate revenue/retention impact", "is this worth
  building", or needs numbers to prioritize a roadmap item. Part of the Product
  Analytics pack.
---

> **Product Analytics pack · Stage 3.** `analytics-question-framing` → `metric-root-cause` / `cohort-retention` → `opportunity-sizing` → `experiment-design` → `insight-storyteller`

# Opportunity Sizing

A good sizing is not a precise number. It's a **range** that a skeptical stakeholder can follow line by line, with the assumptions out in the open, so the team can argue about the right inputs instead of the conclusion.

## Step 1 — Define what's being sized

Agree, in one line each:

- **The change:** what will be different (e.g. "fix the Android onboarding bug", "add SSO", "launch in Canada").
- **The outcome metric:** what value means here: revenue, retained users, hours saved, cost avoided, risk reduced.
- **The horizon:** annualized, first 12 months, or steady state. Say whether it's gross or incremental.
- **The population it touches.**

## Step 2 — Build the driver tree

Write the value as a chain of multiplications, from reach down to value. Keep it to 4–6 drivers. Example:

```
Annual value = affected users per year
             × share who hit the problem
             × uplift in conversion if fixed
             × value per converted user
```

Every driver must be something you can look up or reasonably estimate on its own.

## Step 3 — Source each assumption

For each driver, give a **low / base / high** value and where it came from, in this order of preference:

1. The team's own data (best)
2. A past experiment or launch in the same product
3. A comparable product or public benchmark (name it)
4. A reasoned estimate (say so explicitly)

Never present an estimate as data. Mark estimates clearly.

## Step 4 — Calculate the range

- **Base case:** all base values.
- **Low and high:** don't just multiply all lows together or all highs together. That makes an absurdly wide range. Instead, report the base case, then a realistic low and high where only the 1–2 most uncertain drivers move to their low/high.
- Show the arithmetic so anyone can re-run it.

If a spreadsheet or Python is available, build it so the inputs are editable.

## Step 5 — Sensitivity

Flex each driver from low to high with the others at base, and rank drivers by how much the result moves (a "tornado" ranking). Report:

- The **one or two drivers that matter most**. That's where to spend effort validating.
- The **break-even value**: how low the most uncertain driver can go before the opportunity stops being worth the cost (if cost is known).

## Step 6 — Sanity checks

- Compare the result to a known total (e.g. it can't exceed the revenue of the whole segment).
- Compare to past launches of similar size.
- Check for double counting with other roadmap items that touch the same users.
- Note **time to value**: how long until the impact shows up, and any ramp.

## Output: sizing summary

```markdown
# Sizing: <opportunity>
**Base case:** <value per year> · **Realistic range:** <low> – <high>
**Biggest uncertainty:** <driver>. Validate with <how>.

## Driver tree
| Driver | Low | Base | High | Source |
|---|---|---|---|---|

## Calculation
<the arithmetic, line by line>

## Sensitivity (most to least important)
1. <driver>: result moves <x> – <y>
2. …

**Break-even:** worth doing if <driver> ≥ <value> (cost <z>)

## Caveats
- <double counting, ramp time, what's excluded>
```

## When done

If the decision hinges on an uncertain driver, suggest `experiment-design` to measure it before committing. If the user needs to present the case, suggest `insight-storyteller`.
