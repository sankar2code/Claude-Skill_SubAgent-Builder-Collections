# Market size

**Boundary:** US mid-size provider groups (20–200 clinicians), outpatient prior authorization, software spend only, 2027, USD.

Top-down: total prior-auth admin software spend of about $2.0B [ESTIMATE S1], of which mid-size groups are about 30% [ESTIMATE S2], half of it addressable by an AI assistant [INFERENCE] (medium confidence; depends on payer API access).

Bottom-up: about 10,000 groups in scope [FACT S3] × 70% adoption within the horizon [HYPOTHESIS] × $42K annual contract value [ESTIMATE S4].

Script output (`market_size.py`): top-down base $300M, bottom-up base $294M, gap 2%, ranges overlap from $194M to $422M. RESULT: RECONCILED.

**Biggest swing drivers:** adoption rate and the addressable share. Adoption is a hypothesis and should be tested in the pilot.

## Handoff
- Role: market-sizer
- Status: draft
- As-of: 2026-10-06
- Inputs: 04-issue-tree-architect.md v1; source-ledger.csv v3
- Output: 05-market-sizer.md v1
- Labels: FACT 1 · ESTIMATE 3 · INFERENCE 1 · HYPOTHESIS 1 · UNKNOWN 0
- Contradictions: none
- Open issues: [OPEN] adoption rate untested
- Checks: market_size.py RECONCILED; ledger_check PASS
- Next: strategic-options-grid
- Human approval: none
