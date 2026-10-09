# Changelog

## v1.8.0 (October 2026)
- Added the **Opportunity Discovery pack**: `opportunity-finder` skill with 21 method playbooks across five lenses (Customer, Offer, Capabilities & Assets, Market, Strategic Choice), including a new `why-now-shift` method for technology, AI, regulation and behavior changes.
- Routes by starting point (customer problem, capability, market shift, idea, service business, portfolio, full scan) instead of running every framework.
- Synthesis into an evidence-weighted Business Opportunity Map (convergence matrix, five opportunity conditions, Explore / Validate / Pause / Reject); Validate hands off to `strategy-sprint`.
- Corrected ODI scoring: importance + max(importance − satisfaction, 0), from survey data with sample-size flags.
- Standard-library scripts: `odi_score.py`, `value_curve.py` (Blue Ocean strategy canvas SVG), `strategic_groups.py` (SVG), `convergence.py` (markdown + HTML heatmap).
- 8 templates (including an interview guide), a fictional worked example with generated sample outputs, 8 eval prompts, and credits to the original framework authors.

## v1.7.0 (October 2026)
- Added the **Strategy pack**: `strategy-sprint` skill with 24 role playbooks across Diagnose → Analyze → Decide → Execute → Communicate, including four roles for AI and regulated products (`ai-feasibility-risk`, `regulatory-screen`, `build-buy-partner`, `pilot-experiment-designer`).
- Quick, Standard and Full sprint modes; three human approval gates; one claim-label scheme (FACT / ESTIMATE / INFERENCE / HYPOTHESIS / UNKNOWN) with a source ledger; resumable `decision-log.md`.
- Standard-library scripts: `market_size.py` (top-down vs bottom-up reconciliation), `business_case.py` (NPV, IRR, payback, sensitivity, break-even), `weighted_score.py` (weighted options with fragility test), `ledger_check.py` (lineage, staleness, unlabeled numbers), `handoff_lint.py`.
- Bias controls: pre-mortem, reference-class check, kill criteria, independent red team.
- 13 templates, a fictional worked example with sample outputs that pass the checks, and 8 eval prompts.
- Added 2 sub-agents: `strategy-analyst` (runs one role, parallel-safe) and `strategy-red-team` (cold challenge).
- Added `docs/strategy.md`.

## v1.6.0 (October 2026)
- Added 8 sub-agents: `prd-red-team-reviewer`, `backlog-builder`, `feature-builder` (Stage 5 of PRD → Production), `data-analyst`, `clinical-trial-landscape-scout`, `security-compliance-auditor`, `release-notes-writer`, `ai-eval-builder`.
- Sub-agent guide now maps each agent to the skills it works with.

## v1.5.0 (October 2026)
- Added `trial-eligibility-matcher` to the Pharma & Clinical pack, based on my Agentic Clinical Trial Matching product: `search_trials.py` (find recruiting trials), `fetch_criteria.py` (eligibility text from ClinicalTrials.gov), and `check_criteria.py` (deterministic rules check: citation required for Met, whole-token span check, conflicts, time windows, confidence floor, as-of replay).

## v1.4.0 (October 2026)
- Added the **Pharma & Clinical pack**: `trial-failure-investigator` (with `fetch_trial.py` for ClinicalTrials.gov v2 and PubMed), `gxp-part11-checker`, `clinical-ai-evaluation-design`, plus `docs/pharma-clinical.md`.

## v1.3.0 (October 2026)
- Added the **Product Analytics pack**: `analytics-question-framing`, `metric-root-cause`, `cohort-retention`, `opportunity-sizing`, `experiment-design`, `insight-storyteller`, plus `docs/product-analytics.md`.
- Added standard-library Python scripts: `mix_rate.py` (mix vs rate decomposition), `cohort_table.py` (retention triangle), `sample_size.py` (A/B test sample size and duration).

## v1.2.0 (October 2026)
- Added the **PRD → Production pack**: `engineering-planner`, `implementation-specs`, `security-foundation`, `frontend-setup`, `design-system`, plus `docs/prd-to-production.md`.
- `frontend-setup` updated to Next.js 16, React 19 and TypeScript (template build-tested).
- `security-foundation` generalized: route lists, limits and resources are derived from your specs (ContractIQ values kept as examples); uses `proxy.ts` on Next.js 16.
- Consistent stage order and file paths across the pack, with an approval gate after every stage.

## v1.1.0 (October 2026)
- Restructured into the standard layout: `skills/<name>/SKILL.md` and `agents/<name>.md`, so everything installs directly in Claude Code and claude.ai.
- Renamed skills: `prd-v2` → `prd-writer`, `prd-evaluator-v5` → `prd-evaluator`.
- Added `.claude-plugin/` manifest: install the whole kit with one command.
- Added MIT license.
- Moved guides to `docs/`. Removed machine-specific settings and `.DS_Store` files; added `.gitignore`.

## v1.0.0 (Q1–Q2 2026)
- PRD Writer, PRD Evaluator, Market Research and User Research skills.
- Mockup Generator sub-agent.
