# Claude Skill & Sub-agent Builder Collections

Reusable [Claude](https://claude.ai) **skills** and Claude Code **sub-agents** for product managers, built and used in my own product work.

**Author:** Sankar Kumar Palaniappan · [sankar.work](https://sankar.work) · [LinkedIn](https://www.linkedin.com/in/sankar-kumar-palaniappan-pm) · [hello@sankar.work](mailto:hello@sankar.work)

> 🔴 **Try it live:** the PRD Writer runs on my portfolio. Give it a feature idea and get a PRD in seconds at [sankar.work](https://sankar.work).

---

## What's inside

### Skills

| Skill | What it does |
|---|---|
| [`prd-writer`](skills/prd-writer/SKILL.md) | Writes structured PRDs in five formats: One-Page, Feature Brief, AI Product PRD, Agile Epic, Full PRD |
| [`prd-evaluator`](skills/prd-evaluator/SKILL.md) | Detects a PRD's format, scores it against the matching rubric, and lists fixes |
| [`market-research`](skills/market-research/SKILL.md) | Competitive landscape, TAM/SAM/SOM sizing, trends and positioning |
| [`user-research`](skills/user-research/SKILL.md) | Synthesizes interviews and feedback into themes, personas and pain points |

### PRD → Production pack

Five skills that take a PRD to a running, secure Next.js 16 + Supabase app, one approved stage at a time. Built and used to ship ContractIQ. [Read the pack guide →](docs/prd-to-production.md)

| Stage | Skill | What it does |
|---|---|---|
| 1 | [`engineering-planner`](skills/engineering-planner/SKILL.md) | PRD → engineering doc: architecture, flows, DB design, API spec, roadmap |
| 2 | [`implementation-specs`](skills/implementation-specs/SKILL.md) | Engineering doc → buildable specs, paste-and-run Supabase SQL, `.env.example` |
| 3 | [`security-foundation`](skills/security-foundation/SKILL.md) | Auth, RLS, Zod validation, rate limits, prompt-injection guard, upload checks |
| 4 | [`frontend-setup`](skills/frontend-setup/SKILL.md) | Scaffolds and runs a Next.js 16 + React 19 + TypeScript app |
| always on | [`design-system`](skills/design-system/SKILL.md) | Keeps every UI on your design tokens, with WCAG AA contrast |

### Product Analytics pack

Six skills that take an analytics question from vague request to decision-ready readout. Three include small Python scripts (standard library only). [Read the pack guide →](docs/product-analytics.md)

| Skill | What it does |
|---|---|
| [`analytics-question-framing`](skills/analytics-question-framing/SKILL.md) | Turns a vague ask into prioritized questions tied to a decision, with hypotheses and data needs |
| [`metric-root-cause`](skills/metric-root-cause/SKILL.md) | Explains why a metric moved: data checks, mix vs rate split, drill-down (`mix_rate.py`) |
| [`cohort-retention`](skills/cohort-retention/SKILL.md) | Builds and reads retention triangles and curves (`cohort_table.py`) |
| [`opportunity-sizing`](skills/opportunity-sizing/SKILL.md) | Low/base/high value with a driver tree, sensitivity and break-even |
| [`experiment-design`](skills/experiment-design/SKILL.md) | A/B test plan: metrics, MDE, sample size and duration (`sample_size.py`), decision rules |
| [`insight-storyteller`](skills/insight-storyteller/SKILL.md) | Answer-first readout: exec summary, slide outline with chart choices, Slack and email drafts |

### Pharma & Clinical pack

Four skills for life-sciences product, data and clinical-operations teams, using only public data and published frameworks. [Read the pack guide →](docs/pharma-clinical.md)

| Skill | What it does |
|---|---|
| [`trial-failure-investigator`](skills/trial-failure-investigator/SKILL.md) | NCT ID → why the trial stopped: evidence from ClinicalTrials.gov and PubMed (`fetch_trial.py`), ranked hypotheses labeled fact / inference / hypothesis, with counter-arguments |
| [`gxp-part11-checker`](skills/gxp-part11-checker/SKILL.md) | Gap assessment of a system, feature or AI tool against 21 CFR Part 11, EU Annex 11 and ALCOA+, with fixes written as testable requirements |
| [`trial-eligibility-matcher`](skills/trial-eligibility-matcher/SKILL.md) | Screens a de-identified patient against trial criteria, or finds recruiting trials (`search_trials.py`, `fetch_criteria.py`); deterministic checker with citation and span checks (`check_criteria.py`) |
| [`clinical-ai-evaluation-design`](skills/clinical-ai-evaluation-design/SKILL.md) | Monitoring signal → governance action, escalation pathway, trial design and estimand for clinical AI (Fosset et al., PLOS Digital Health 2026) |

### Strategy pack

One coordinator skill and two sub-agents that run a strategy decision from open question to approved recommendation: 24 bounded roles across Diagnose → Analyze → Decide → Execute → Communicate, three modes (Quick, Standard, Full sprint), human approval gates, labeled claims with a source ledger, and a resumable decision log. Five standard-library scripts check the numbers. [Read the pack guide →](docs/strategy.md)

| Piece | What it does |
|---|---|
| [`strategy-sprint`](skills/strategy-sprint/SKILL.md) | Market entry, build vs buy vs partner, pricing, portfolio and AI product bets: frames the decision, routes the fewest roles that can change it, runs pre-mortem and red team, and packages a memo, slide brief or PRD handoff. Includes AI feasibility and regulatory screens (GxP, HIPAA, FDA, EU AI Act). Scripts: `market_size.py`, `business_case.py`, `weighted_score.py`, `ledger_check.py`, `handoff_lint.py` |

### Sub-agents

| Sub-agent | What it does |
|---|---|
| [`mockup-generator`](agents/mockup-generator.md) | Turns a PRD into a set of high-fidelity, clickable HTML mockups |
| [`prd-red-team-reviewer`](agents/prd-red-team-reviewer.md) | Reviews a PRD cold: gaps, risky assumptions, missing metrics, scored with fixes. Read-only. |
| [`backlog-builder`](agents/backlog-builder.md) | Turns a PRD into epics and INVEST-checked stories with Given/When/Then acceptance criteria, plus a Jira/Linear CSV. |
| [`feature-builder`](agents/feature-builder.md) | Builds one feature at a time from docs/specs/, with tests and a passing build. Stage 5 of PRD → Production. |
| [`data-analyst`](agents/data-analyst.md) | Runs an analytics question end to end on a data file: checks, analysis, charts and an answer-first readout. |
| [`clinical-trial-landscape-scout`](agents/clinical-trial-landscape-scout.md) | Maps the ClinicalTrials.gov landscape for a condition or drug class: sponsors, phases, endpoints, stops, white space. |
| [`security-compliance-auditor`](agents/security-compliance-auditor.md) | Read-only audit of a codebase: auth, RLS, validation, secrets, LLM risks, and Part 11 / ALCOA+ where relevant. |
| [`release-notes-writer`](agents/release-notes-writer.md) | Reads git history and writes customer release notes, a changelog entry and an announcement. |
| [`ai-eval-builder`](agents/ai-eval-builder.md) | Builds an eval suite for an AI feature: labeled test set, rubric, LLM judge, release gates and a runnable script. |
| [`strategy-analyst`](agents/strategy-analyst.md) | Runs one strategy-sprint role on frozen inputs and writes one labeled, sourced output. Run several in parallel for independent evidence. |
| [`strategy-red-team`](agents/strategy-red-team.md) | Attacks a strategy recommendation cold from seven executive seats, recomputes a key number, and rates each challenge. |

**How they fit together:** `strategy-sprint` decides what to build → `market-research` + `user-research` → `prd-writer` → `prd-evaluator` → `mockup-generator` for a clickable prototype, or the PRD → Production pack to build the real app

---

## Install

### Option 1: Claude Code plugin (everything, one command)

```
/plugin marketplace add sankar2code/Claude-Skill_SubAgent-Builder-Collections
/plugin install pm-builder-kit@sankar2code
```

### Option 2: Pick individual pieces

- **Skill in Claude Code:** copy a folder from `skills/` into `~/.claude/skills/` (all projects) or `<project>/.claude/skills/`.
- **Skill in claude.ai:** zip a folder from `skills/` (for example `prd-writer/`) and upload it in Claude's Skills settings.
- **Sub-agent in Claude Code:** copy a file from `agents/` into `~/.claude/agents/` or `<project>/.claude/agents/`.

Then just ask naturally, for example *"Write a one-page PRD for AI triage of support tickets"*. Claude picks up the right skill from its description.

---

## Repository structure

```
.claude-plugin/        Plugin + marketplace manifest
skills/<name>/SKILL.md Skills (standard Agent Skills format)
agents/<name>.md       Claude Code sub-agents
docs/                  Guides: skills-guide.md, prd-to-production.md, product-analytics.md, pharma-clinical.md, strategy.md, subagent-guide.md, mockup-generator.md
CHANGELOG.md
```

## Guides

- [Skills guide](docs/skills-guide.md): what each skill covers and how to use them together
- [PRD → Production pack](docs/prd-to-production.md): the five-stage build workflow
- [Product Analytics pack](docs/product-analytics.md): from question to readout
- [Pharma & Clinical pack](docs/pharma-clinical.md): trials, GxP and clinical AI evaluation
- [Strategy pack](docs/strategy.md): governed strategy decisions, from open question to approved recommendation
- [Sub-agent guide](docs/subagent-guide.md): how sub-agents work and how to add one
- [Mockup Generator guide](docs/mockup-generator.md)

## Contributing

Issues and pull requests are welcome. New skills go in `skills/<name>/SKILL.md` with a `name` and a trigger-rich `description` in the frontmatter; new sub-agents go in `agents/<name>.md`.

## License

[MIT](LICENSE): free to use, modify and share, including commercially. Please keep the copyright notice.

⭐ If this helps you, star the repo and share it with your team.
