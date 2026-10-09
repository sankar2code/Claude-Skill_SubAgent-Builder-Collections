# Routes

Use the fewest roles that can change the decision. A route is a proposal until the decision owner approves it at Gate 1.

## Routing test

Score each candidate role 0–2 on four questions:

| Question | 0 | 1 | 2 |
|---|---|---|---|
| **Could its output change the decision?** | No | Possibly | Very likely |
| **Are its inputs ready?** | No | Partly | Yes |
| **Does it add evidence or challenge nobody else covers?** | Duplicate | Some | Clearly |
| **Is the confidence gain worth the time?** (inverse cost) | Costly, low gain | Balanced | Cheap, high gain |

Run a role when it scores 6 or more and scores at least 1 on the first question. Score 4–5: include only in Full mode. Below 4: skip and say why in the route table.

## Stage map

| Stage | Roles | Gate |
|---|---|---|
| Diagnose | problem-framer → situation-assessor → hypothesis-builder → issue-tree-architect | **Gate 1:** mandate, criteria, scope and evidence plan |
| Analyze | market-sizer, profit-pool-mapper, competitor-war-gamer, customer-segmenter, ai-feasibility-risk, regulatory-screen | Evidence reconciliation (coordinator) |
| Decide | strategic-options-grid → build-buy-partner / pricing-strategist / business-case-builder / portfolio-reviewer | **Gate 2:** option set or shortlist |
| Execute | operating-model-designer → initiative-prioritizer → pilot-experiment-designer → transformation-roadmapper → kpi-architect | Only for an approved or shortlisted option |
| Communicate | pyramid-story-builder → decision-memo-writer → red-team-qa → deck-brief-builder | **Gate 3:** recommendation and output format |

## Dependency map

```
problem-framer
  ├─ situation-assessor
  ├─ hypothesis-builder
  └─ issue-tree-architect
        ├─ market-sizer ──────────┐
        ├─ profit-pool-mapper ────┤
        ├─ customer-segmenter ────┤
        ├─ competitor-war-gamer ──┼──► strategic-options-grid
        ├─ ai-feasibility-risk ───┤        ├─ build-buy-partner
        └─ regulatory-screen ─────┘        ├─ pricing-strategist
                                           ├─ business-case-builder
                                           └─ portfolio-reviewer
                                                  │  (Gate 2)
                                                  ▼
                       operating-model-designer → initiative-prioritizer
                         → pilot-experiment-designer → transformation-roadmapper → kpi-architect
                                                  │
                                                  ▼
                       pyramid-story-builder → decision-memo-writer → red-team-qa (fresh context)
                                                  │  (Gate 3)
                                                  ▼
                                  deck-brief-builder / prd-writer / insight-storyteller
```

This is the default map, not a checklist. Red-team findings can send a targeted request back to any earlier role; if that changes the option set, repeat Gate 2.

## Fast routes

**Market entry.** problem-framer → issue-tree-architect → market-sizer + customer-segmenter + competitor-war-gamer (parallel) → strategic-options-grid → business-case-builder → red-team-qa → pyramid-story-builder. Add profit-pool-mapper when value-chain position matters; add regulatory-screen for regulated markets.

**AI product bet.** problem-framer → hypothesis-builder → customer-segmenter + ai-feasibility-risk + regulatory-screen (parallel) → strategic-options-grid → build-buy-partner → business-case-builder → pilot-experiment-designer → red-team-qa → decision-memo-writer → prd-writer.

**Build vs buy vs partner.** problem-framer → ai-feasibility-risk (if AI) → build-buy-partner → business-case-builder → red-team-qa → decision-memo-writer.

**Pricing / monetization.** problem-framer → customer-segmenter + competitor-war-gamer → pricing-strategist → business-case-builder → red-team-qa → decision-memo-writer.

**Portfolio allocation.** problem-framer → situation-assessor → market-sizer + profit-pool-mapper → portfolio-reviewer → business-case-builder for material moves → decision-memo-writer.

**Pharma / healthcare launch or capability.** problem-framer → situation-assessor → regulatory-screen + customer-segmenter + market-sizer → strategic-options-grid → business-case-builder → pilot-experiment-designer → red-team-qa (include regulator and patient-safety seats) → decision-memo-writer.

**Transformation launch.** problem-framer → situation-assessor → operating-model-designer → initiative-prioritizer → transformation-roadmapper → kpi-architect → red-team-qa → deck-brief-builder.

**Communication only.** Approved recommendation → pyramid-story-builder → decision-memo-writer and/or red-team-qa → deck-brief-builder. Refuse if there is no approved recommendation; offer the Diagnose stage instead.

**Early kill test.** problem-framer → hypothesis-builder → one targeted evidence role. Stop if a load-bearing hypothesis fails; do not commission the full sprint.

**Quick mode.** problem-framer (lite: question, owner, criteria) → the single highest-scoring evidence role → strategic-options-grid (3 options) → pre-mortem → one-page decision-memo-writer.

## Parallel rules

- Run in parallel only when neither task needs the other's output.
- Each worker gets a self-contained brief: role, work order path, named input files, output file, and the operating rules. Workers do not see the parent conversation.
- Independent streams reduce shared framing bias. Reconcile definitions, periods, units and contradictions before synthesis.
- Synthesis, recommendation and packaging stay sequential.
- No two workers write the same file.

## Coordinator checklist

- [ ] Mandate approved; route is the minimum that can change the decision
- [ ] Each role did only its job, on named and versioned inputs
- [ ] Ledger and labels complete; `ledger_check.py` passed
- [ ] Numbers reconcile; scripts passed where used
- [ ] Counterevidence and dissent preserved
- [ ] Gates recorded in the decision log before selection and packaging
- [ ] No action outside permissions
- [ ] The final output contains only approved claims with traceable sources
