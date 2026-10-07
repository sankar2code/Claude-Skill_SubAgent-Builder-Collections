# Changelog

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
