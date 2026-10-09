# Worked example: build, partner or wait on AI prior authorization

> **Fictional company, illustrative numbers.** Helio Health is invented for this example. Every number below exists only to show how the skill works. The files in `sample-output/` are the real artifacts this run would produce, and they pass `ledger_check.py` and `handoff_lint.py`.

## The ask

> "Our customers keep asking for AI prior authorization. Competitors are announcing it. Should we build it?"

## Step 0–1: Triage

No decision log exists, so the coordinator starts a new one. Three questions:

- **Decision and owner?** The CEO decides whether to build, partner or wait.
- **By when?** Board meeting on 15 December.
- **Stakes?** Up to $3M of build budget, a regulated data domain (HIPAA), hard to reverse once customers depend on it.

**Mode: Standard**, stepping up to Full if the board asks for an investment-committee pack. Reason: material money and a regulated domain, but one accountable owner and a reversible pilot path.

## Step 2: Work order

Filled from `assets/templates/work-order.md`. Approved sources: internal sales and pricing files, a customer time study, one licensed market report, public provider registries. Prohibited: contacting competitor staff, buying new data without approval. Freshness limit: 24 months.

## Step 3: Route (Gate 1)

Using the routing test and the **AI product bet** fast route:

| # | Role | Input | Output file | Depends on | Parallel? | Gate |
|---|---|---|---|---|---|---|
| 01 | problem-framer | CEO brief v1 | 01-problem-framer.md | none | no | Gate 1 |
| 04 | issue-tree-architect | 01 v2 | 04-issue-tree-architect.md | 01 | no | Gate 1 |
| 05 | market-sizer | 04 v1, ledger v3 | 05-market-sizer.md | 04 | yes | |
| 08 | customer-segmenter | 04 v1, time study | 08-customer-segmenter.md | 04 | yes | |
| 09 | ai-feasibility-risk | 04 v1, eval notes | 09-ai-feasibility-risk.md | 04 | yes | |
| 10 | regulatory-screen | 04 v1 | 10-regulatory-screen.md | 04 | yes | |
| 11 | strategic-options-grid | 05, 08, 09, 10 | 11-strategic-options-grid.md | Analyze | no | Gate 2 |
| 12 | build-buy-partner | 09, 11 | 12-build-buy-partner.md | 11 | no | |
| 14 | business-case-builder | 11, 12 | 14-business-case-builder.md | 12 | no | |
| 18 | pilot-experiment-designer | 14, kill criteria | 18-pilot-experiment-designer.md | 14 | no | |
| 23 | red-team-qa | memo pack | 23-red-team-qa.md | 22 | fresh context | Gate 3 |
| 22 | decision-memo-writer | approved outputs | 22-decision-memo-writer.md | 23 | no | Gate 3 |

Skipped with reasons: competitor-war-gamer scored 5 (competitor capabilities are `[UNKNOWN]` and only public announcements exist; revisit if the board asks), pricing-strategist scored 4 (price follows existing contract values).

**Gate 1:** the CEO approved on 1 October, with one condition: add the regulatory screen. Recorded in `decision-log.md`.

## Step 4: Evidence (parallel)

In Claude Code, the coordinator sent four `strategy-analyst` calls at once: market-sizer, customer-segmenter, ai-feasibility-risk, regulatory-screen. Each got the work order path, its named inputs and its output file.

`market_size.py` output (from `assets/templates/market-size.json`):

```
Base cases: top_down 300.00M USD/yr, bottom_up 294.00M USD/yr
Gap between base cases: 2% (tolerance 25%)
Ranges overlap: 194.40M USD/yr to 422.40M USD/yr
RESULT: RECONCILED within tolerance
```

AI feasibility found the extraction accuracy target (95% on required fields) is `[HYPOTHESIS]`: there is no eval yet. Regulatory screen found HIPAA business-associate obligations for both build and partner paths: a cost, not a gate.

## Step 4b: Options and Gate 2

Options: status quo, build in-house, partner with a vendor. `weighted_score.py` with the weights agreed at Gate 1:

```
1. Build in-house        3.25
2. Partner with vendor   3.15
3. Status quo            3.10
FRAGILE. Winner changes when: value -10 pts -> Status quo wins; strategic_control -10 pts -> Partner wins ...
```

The coordinator reported the result as **fragile**: the options are close, and the ranking depends on how much the CEO values control. **Gate 2:** the CEO shortlisted build and partner, and asked for the business case and a pilot design that would separate them.

## Step 4c: Business case

`business_case.py` (from `assets/templates/business-case.json`):

```
Build in-house       NPV $18.71M  IRR 105.4%  payback 1.9y
Partner with vendor  NPV $13.84M  IRR 240.9%  payback 0.8y
Break-even: build needs 27% of planned volume; partner needs 16%.
```

Volume is the biggest swing driver for both, and it is a `[HYPOTHESIS]`. So the decision hinges on adoption, which the pilot must test.

## Step 5: Challenge

- **Pre-mortem** top uncovered cause: payers change portal formats and extraction accuracy collapses. Added a monitoring guardrail and a kill criterion.
- **Reference class:** enterprise AI pilots that reach production. No credible base rate in approved sources: `[UNKNOWN]`. Volume ranges were widened.
- **Red team** (fresh context, CFO seat): "Both NPVs assume the sales plan. What if adoption is half?" Response: partner still clears break-even at half volume; build does too, but payback stretches. Logged as accepted risk.

**Gate 3:** the CEO approved this recommendation: *partner now with a 6-month pilot at 15 customers, with kill criteria on accuracy and adoption, and a contractual option to bring the model in-house once there are more than 200 customers.* Output: a decision memo for the board.

## Step 6: Package

`decision-memo-writer` produced a two-page memo from `assets/templates/decision-memo.md`. The coordinator then offered:

- `prd-writer` for the pilot PRD
- `experiment-design` to size the pilot
- `deck-brief-builder` if the board wants slides

## What made this run trustworthy

- The decision was framed before any analysis.
- Weights were set before scores.
- Two market methods agreed, and the script showed it.
- The fragile ranking was reported, not hidden.
- The load-bearing number (adoption) was named as a hypothesis and turned into a pilot.
- The red team ran without the original reasoning.
