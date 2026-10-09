# Bias controls

Run these before Gate 3 in Standard and Full modes, and the pre-mortem in Quick mode. Write the results to `strategy-output/NN-challenge.md`.

## 1. Pre-mortem

Assume the recommended option was chosen and, 18 months later, clearly failed.

1. List 8–12 plausible causes. Mix internal (execution, capability, adoption) and external (competitor, regulation, market, technology).
2. For each: likelihood (H/M/L), impact (H/M/L), the earliest observable warning sign, and whether the current plan already covers it.
3. Promote the top 3 uncovered causes to the plan: a mitigation, an owner role, or a kill criterion.

A pre-mortem that finds nothing new is a sign it was run too politely. Try again from the seat of the person most likely to block the decision.

## 2. Reference class check

Ask: "When others made a decision like this, how did it usually turn out?"

1. Define the reference class (for example "B2B SaaS entering an adjacent vertical", "enterprise AI pilots moving to production", "Phase II to Phase III transition in this indication").
2. Find base rates from approved sources: success rate, typical time and cost overrun, adoption curve. Label them with source IDs.
3. Compare the plan's assumptions with the base rate. Any assumption better than the base rate needs a specific reason it applies here, marked `[INFERENCE]` or `[HYPOTHESIS]`.
4. If no credible base rate exists, write `[UNKNOWN]` and widen the ranges in the business case. Do not invent one.

## 3. Kill criteria

Before approval, agree the signals that would stop, pause or reverse the decision:

| Signal | Metric and threshold | Checked when | Owner role | Action if hit |
|---|---|---|---|---|

Good kill criteria are measurable, observable early, and agreed before results arrive. Feed them to `kpi-architect` and `pilot-experiment-designer`.

## 4. Independent red team

- Run `red-team-qa` in a fresh context: the `strategy-red-team` sub-agent in Claude Code, or a new chat in claude.ai.
- Give it only the recommendation, the evidence pack, the ledger and the business case. Do not give it the reasoning that produced the recommendation.
- Every material challenge gets a response: resolved (with evidence), accepted (plan changed), or logged as open risk with an owner.

## 5. Quick self-checks

- **Confirmation:** did any role look for evidence against the leading option? Where is it?
- **Anchoring:** did the first number we saw shape every later estimate?
- **Sunk cost:** are past investments being counted as a reason to continue?
- **Option theatre:** are the alternatives real, or straw men around a preferred answer?
- **Survivorship:** are the comparables only the winners?
- **Authority:** are assumptions from senior people labeled `[HYPOTHESIS]` like everyone else's?
