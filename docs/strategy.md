# Strategy pack

One Claude skill and two sub-agents that run a strategy decision from an open question to an approved, evidence-backed recommendation. It works in claude.ai, Claude Cowork and Claude Code. In Claude Code, the sub-agents add parallel evidence streams and an independent red team.

```
          Diagnose ──► Analyze ──► Decide ──► Execute ──► Communicate
              │  Gate 1     (parallel)   │  Gate 2               │  Gate 3
              ▼                          ▼                       ▼
     problem framed,            option set or            recommendation approved
     evidence plan approved     shortlist approved       → memo, slides or PRD
```

| Piece | Type | What it does |
|---|---|---|
| [`strategy-sprint`](../skills/strategy-sprint/SKILL.md) | Skill (coordinator) | Triage, work order, route, gates, decision log, challenge and packaging. Loads one of 24 role playbooks at a time. |
| [`strategy-analyst`](../agents/strategy-analyst.md) | Sub-agent | Runs one role on frozen inputs and writes one labeled, sourced file. Use several in parallel for independent evidence. |
| [`strategy-red-team`](../agents/strategy-red-team.md) | Sub-agent | Attacks the recommendation cold from seven executive seats and recomputes a key number. |

## Three modes

| Mode | When | What you get |
|---|---|---|
| **Quick** | Reversible, modest stakes, one session | Frame → one evidence role → 3 options → pre-mortem → one-page memo |
| **Standard** | Material money or team time | Minimum route, Gate 1 and Gate 3, scripts on the numbers |
| **Full sprint** | Board, investment committee, regulated, hard to reverse | All gates, parallel evidence, independent red team, checked ledger and handoffs |

## The 24 roles

| Diagnose | Analyze | Decide | Execute | Communicate |
|---|---|---|---|---|
| problem-framer | market-sizer | strategic-options-grid | operating-model-designer | pyramid-story-builder |
| situation-assessor | profit-pool-mapper | build-buy-partner ★ | initiative-prioritizer | decision-memo-writer |
| hypothesis-builder | competitor-war-gamer | pricing-strategist | pilot-experiment-designer ★ | red-team-qa |
| issue-tree-architect | customer-segmenter | business-case-builder | transformation-roadmapper | deck-brief-builder |
| | ai-feasibility-risk ★ | portfolio-reviewer | kpi-architect | |
| | regulatory-screen ★ | | | |

★ Roles for AI products and regulated industries: whether an AI capability can be built and evaluated safely, which regulations apply (GxP, HIPAA, FDA, EU AI Act, privacy), whether to build, buy or partner, and the smallest pilot that proves or kills the choice.

## What makes it trustworthy

- **Labeled claims.** Every material claim is `[FACT S#]`, `[ESTIMATE S#]`, `[INFERENCE]`, `[HYPOTHESIS]` or `[UNKNOWN]`, and facts cite a source ID in a ledger.
- **Checks, not just checklists.** Five standard-library scripts:

  | Script | Checks |
  |---|---|
  | `market_size.py` | Reconciles top-down and bottom-up market sizing |
  | `business_case.py` | NPV, IRR, payback, sensitivity and break-even |
  | `weighted_score.py` | Ranks options and tests whether the winner holds when the weights change |
  | `ledger_check.py` | Source IDs, out-of-date sources and numbers without labels |
  | `handoff_lint.py` | Handoff blocks are complete and each gate is recorded |

- **Bias controls.** A pre-mortem, a check of how similar decisions turned out (base rates), kill criteria agreed before results, and a red team that never sees the original reasoning.
- **Human gates.** Agents draft; the decision owner approves the mandate, the shortlist and the recommendation.
- **Resumable.** `strategy-output/decision-log.md` records gates, versions and open issues, so a sprint can stop and pick up in a later session.
- **Read-only by default.** Writes only to `strategy-output/`. Paid data, outreach, uploads, publishing and system writes each need explicit approval.

## Example run

1. *"Should we build an AI prior-authorization assistant, partner with a vendor, or wait?"* → `strategy-sprint` triages to Standard mode, fills the work order and proposes the AI-product-bet route for Gate 1.
2. In Claude Code, four `strategy-analyst` calls run at the same time: market-sizer, customer-segmenter, ai-feasibility-risk, regulatory-screen.
3. Options are scored. `weighted_score.py` reports the ranking as fragile, so the owner shortlists two options at Gate 2.
4. `business_case.py` shows volume is the swing driver, and volume is still a hypothesis. That becomes the pilot.
5. `strategy-red-team` challenges the case cold; responses are logged.
6. Gate 3 approves "partner now, pilot with kill criteria, option to bring in-house". Then `decision-memo-writer` writes the memo, and `prd-writer` can take the pilot from there.

The full fictional run, with real output files that pass the checks, is in [`skills/strategy-sprint/examples/`](../skills/strategy-sprint/examples/worked-example.md).

## How it connects to the rest of the kit

```
user-research ──► customer-segmenter
market-research ─► market-sizer, competitor-war-gamer
gxp-part11-checker, clinical-ai-evaluation-design ─► regulatory-screen, ai-feasibility-risk
                                 strategy-sprint (approved recommendation)
                                   ├─► prd-writer ─► prd-evaluator ─► backlog-builder
                                   ├─► experiment-design (pilot sizing)
                                   └─► insight-storyteller (leadership summary)
```

## Install

- **Claude Code, whole kit:** `/plugin marketplace add sankar2code/Claude-Skill_SubAgent-Builder-Collections` then `/plugin install pm-builder-kit@sankar2code`.
- **Claude Code, just this pack:** copy `skills/strategy-sprint/` to `~/.claude/skills/` and the two agent files to `~/.claude/agents/`.
- **claude.ai or Cowork:** zip the `strategy-sprint` folder and upload it in Skills settings. The red team then runs in a new chat instead of a sub-agent.

## Limits

Outputs are drafts for qualified human review, not legal, investment, accounting or regulatory advice. The skill has no access of its own to data, the web or your systems; what it can read depends on your environment. Access is not proof that data is correct or current.

*Inspired by public strategy-agent playbooks; rewritten and extended for product, AI and regulated-industry decisions.*
