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

### Sub-agents

| Sub-agent | What it does |
|---|---|
| [`mockup-generator`](agents/mockup-generator.md) | Turns a PRD into a set of high-fidelity, clickable HTML mockups |

**How they fit together:** `market-research` + `user-research` → `prd-writer` → `prd-evaluator` → `mockup-generator` for a clickable prototype, or the PRD → Production pack to build the real app

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
docs/                  Guides: skills-guide.md, prd-to-production.md, subagent-guide.md, mockup-generator.md
CHANGELOG.md
```

## Guides

- [Skills guide](docs/skills-guide.md): what each skill covers and how to use them together
- [PRD → Production pack](docs/prd-to-production.md): the five-stage build workflow
- [Sub-agent guide](docs/subagent-guide.md): how sub-agents work and how to add one
- [Mockup Generator guide](docs/mockup-generator.md)

## Contributing

Issues and pull requests are welcome. New skills go in `skills/<name>/SKILL.md` with a `name` and a trigger-rich `description` in the frontmatter; new sub-agents go in `agents/<name>.md`.

## License

[MIT](LICENSE): free to use, modify and share, including commercially. Please keep the copyright notice.

⭐ If this helps you, star the repo and share it with your team.
