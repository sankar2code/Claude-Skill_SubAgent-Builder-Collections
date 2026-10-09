# Claude Code Subagent Collection

A collection of [Claude Code](https://docs.claude.com/en/docs/claude-code) **subagents** — specialized, reusable AI helpers that live as Markdown files and get delegated work by the main agent. This README explains what subagents are, how they work, when and where to use them, and then indexes the subagents in this folder.

![type](https://img.shields.io/badge/type-subagent%20collection-4f46e5)
![format](https://img.shields.io/badge/format-markdown%20%2B%20YAML%20frontmatter-0ea5e9)
![runtime](https://img.shields.io/badge/runtime-claude%20code-22c55e)

---

## What is a subagent?

A **subagent** is a focused, named persona that Claude Code can dispatch a task to instead of (or in addition to) handling it in the main conversation. Each one is just a Markdown file with a small YAML header — no code, no build step. The header tells Claude Code *when* to reach for this persona and *what it's allowed to touch*; the Markdown body becomes that persona's system prompt.

Think of it less like a plugin and more like **hiring a specialist for a specific kind of job**: a "PRD-to-mockup designer," a "code reviewer," a "test writer," a "release-notes drafter." You describe the job once, in detail, and Claude Code routes matching requests to that description from then on — pulling that detailed context into play only when it's actually relevant, instead of bloating every conversation with it.

## Why subagents exist (the problem they solve)

Without subagents, every specialized instruction you want Claude to follow has to either:
- live in your head and get re-typed each time, or
- live in `CLAUDE.md` / the system prompt, where it's *always* loaded — even for unrelated work, crowding out context and diluting focus.

Subagents solve this with **progressive disclosure**: a short `description` is always available for routing, but the full persona — its principles, workflow, conventions, and quality bar — only enters context when a matching task actually arrives. That keeps the main conversation lean while still giving you deep, reusable expertise on tap.

They also give you **tool scoping**: a subagent can be handed a narrower toolset than the main session (e.g. read-and-generate but no shell access, or vice versa), which both focuses its behavior and limits its blast radius.

## How subagents work — architecture

### Anatomy of a subagent file

```
agent-name.md
├── YAML frontmatter           # routing + capability metadata (always loaded)
│   ├── name           — identifier used to invoke it directly
│   ├── description    — WHEN to use it; the primary trigger for auto-routing
│   ├── tools          — the allow-list of tools it can call (omit = inherit all)
│   └── model          — which model runs it ("inherit" = match the parent session)
└── Markdown body              # the persona's system prompt (loaded on activation)
    ├── Role framing       — who this persona is, what "success" looks like
    ├── Operating principles — the judgment calls that guide its decisions
    ├── Workflow            — the ordered phases it works through
    ├── Conventions/standards — concrete rules about output format & quality
    └── Self-review         — how it checks its own work before handing off
```

### The lifecycle of a delegated task

1. **Routing** — Claude Code (or the user, by name) matches an incoming request against every subagent's `description`. The description is the *only* thing always in context, so it has to be specific and a little assertive about when it applies — vague descriptions cause "undertriggering," where a perfectly suited subagent never gets picked.
2. **Activation** — once selected, the subagent's Markdown body is loaded as its system prompt, and it receives the task with **its own context window** — it doesn't see the parent conversation's history, only what it's explicitly told.
3. **Execution** — it works autonomously through its own described workflow, calling only the tools listed in its `tools` frontmatter (or all available tools, if that field is omitted).
4. **Handoff** — it returns a final result to whatever invoked it. The parent conversation sees the outcome, not the subagent's internal step-by-step reasoning — which is what keeps delegation cheap on context.

### Where subagents live

| Location | Scope | Use it for |
| --- | --- | --- |
| `<project>/.claude/agents/*.md` | **Project-local** — only active in this project | Personas tightly coupled to one codebase, domain, or workflow (e.g. "this repo's migration-writer") |
| `~/.claude/agents/*.md` | **User-level** — active across all your projects | General-purpose personas you want everywhere (e.g. "code reviewer," "commit-message writer") |

Project-local agents win on name conflicts, so a project can override a general-purpose persona with a more specific one of the same name.

## When to reach for a subagent

Use a subagent when a task is:

- **Recurring** — you find yourself wanting to give Claude the same detailed brief over and over ("when you write tests, do X, Y, Z…"). Capture it once as a persona instead.
- **Specialized** — it benefits from a distinct mindset, vocabulary, or quality bar that would feel out of place as a blanket instruction for *all* work in the project (e.g. "write like a senior designer" doesn't belong in `CLAUDE.md` if most of the work here is backend).
- **Self-contained** — it can be briefed, executed, and handed back without needing constant back-and-forth with the parent conversation. Subagents work best as "go do this whole thing and report back," not "help me think through this interactively."
- **Worth isolating** — either to protect the main context window from a lot of intermediate noise (e.g. reading a 200-page spec), or to scope down its tool access for safety/focus.

Don't reach for one when the task is a single quick lookup, needs tight interactive back-and-forth with the user, or is a one-off that will never recur — the overhead of writing and maintaining a persona file outweighs the benefit.

## How to invoke one

Two ways:

- **By name**, explicitly: *"Use the `mockup-generator` agent on `docs/spec.pdf`."*
- **By description match**, implicitly: phrase your request the way the persona's `description` expects to be triggered, and Claude Code routes it there automatically. (This is why descriptions matter so much — they're the trigger, not just documentation.)

## How to add a new subagent to this collection

1. Create `<name>.md` in the repo's `agents/` folder (or `~/.claude/agents/` for a cross-project persona).
2. Write a `description` that states **both** what the agent does *and* the concrete situations/phrases that should trigger it — be a little assertive; under-specified descriptions get skipped.
3. Scope `tools` to the minimum the persona genuinely needs (omit the field only if it truly needs everything).
4. Write the body as a system prompt: frame the role, state the operating principles (the *why* behind its judgment calls), lay out an ordered workflow, define concrete conventions/output format, and give it a self-review step so it catches its own mistakes before handoff.
5. Add an entry to the index below.

---

## Agents in this collection

| Agent | Purpose | Tools | Model |
| --- | --- | --- | --- |
| [`mockup-generator`](../agents/mockup-generator.md) | Turns a PRD into a set of high-fidelity, clickable HTML mockups — a navigable prototype a team can click through and react to before design/eng investment begins. | `Read, Write, Edit, Glob, Grep, Bash` | `inherit` |
| [`prd-red-team-reviewer`](../agents/prd-red-team-reviewer.md) | Reviews a PRD cold: gaps, risky assumptions, missing metrics, scored with fixes. Read-only. | `Read, Glob, Grep, WebSearch, WebFetch` | `inherit` |
| [`backlog-builder`](../agents/backlog-builder.md) | Turns a PRD into epics and INVEST-checked stories with Given/When/Then acceptance criteria, plus a Jira/Linear CSV. | `Read, Write, Edit, Glob, Grep` | `inherit` |
| [`feature-builder`](../agents/feature-builder.md) | Builds one feature at a time from docs/specs/, with tests and a passing build. Stage 5 of PRD → Production. | `Read, Write, Edit, Glob, Grep, Bash` | `inherit` |
| [`data-analyst`](../agents/data-analyst.md) | Runs an analytics question end to end on a data file: checks, analysis, charts and an answer-first readout. | `Read, Write, Edit, Glob, Grep, Bash` | `inherit` |
| [`clinical-trial-landscape-scout`](../agents/clinical-trial-landscape-scout.md) | Maps the ClinicalTrials.gov landscape for a condition or drug class: sponsors, phases, endpoints, stops, white space. | `Read, Write, Bash, WebFetch, WebSearch` | `inherit` |
| [`security-compliance-auditor`](../agents/security-compliance-auditor.md) | Read-only audit of a codebase: auth, RLS, validation, secrets, LLM risks, and Part 11 / ALCOA+ where relevant. | `Read, Glob, Grep, Bash` | `inherit` |
| [`release-notes-writer`](../agents/release-notes-writer.md) | Reads git history and writes customer release notes, a changelog entry and an announcement. | `Read, Write, Edit, Glob, Grep, Bash` | `inherit` |
| [`ai-eval-builder`](../agents/ai-eval-builder.md) | Builds an eval suite for an AI feature: labeled test set, rubric, LLM judge, release gates and a runnable script. | `Read, Write, Edit, Glob, Grep, Bash` | `inherit` |
| [`strategy-analyst`](../agents/strategy-analyst.md) | Runs one `strategy-sprint` role on frozen inputs and writes one labeled, sourced output file. Parallel-safe leaf worker. | `Read, Write, Glob, Grep, Bash, WebSearch, WebFetch` | `inherit` |
| [`strategy-red-team`](../agents/strategy-red-team.md) | Attacks a strategy recommendation cold from seven executive seats, recomputes a key number, rates challenges. Writes only its own review. | `Read, Write, Glob, Grep, Bash, WebSearch, WebFetch` | `inherit` |

### `mockup-generator`

**What/when:** Give it a PRD, product spec, or feature brief (PDF, Markdown, or pasted text) and ask to "mock up," "wireframe," "prototype," or "visualize" it — it produces a self-contained, zero-build HTML prototype where every screen traces back to a specific requirement in the source document.

**How it works:** runs a six-phase workflow — *ingest the PRD → plan a screen inventory & flow map (and check in with you) → establish a shared design system → build the mockups → self-review against a checklist → hand off with assumptions and open questions logged*. Output is plain HTML + Tailwind CDN + vanilla JS + Lucide icons, organized under a `mockups/` directory with a hub `index.html`, one file per screen, shared `assets/`, and its own traceability `README.md`.

See [`mockup-generator.md`](../agents/mockup-generator.md) for the full persona definition, or this folder's prior worked example (an 11-screen prototype generated from a hotel-booking-cancellation PRD) for a sense of the depth and polish it aims for.

---

### How the agents fit with the skills

| Stage | Skill(s) | Sub-agent |
| --- | --- | --- |
| Define | `prd-writer`, `prd-evaluator` | `prd-red-team-reviewer` (independent critique), `backlog-builder` (stories) |
| Prototype | | `mockup-generator` |
| Build | PRD → Production pack | `feature-builder` (Stage 5), `security-compliance-auditor` (before launch) |
| Ship | | `release-notes-writer` |
| Measure | Product Analytics pack | `data-analyst` (runs the pack end to end), `ai-eval-builder` (for AI features) |
| Clinical | Pharma & Clinical pack | `clinical-trial-landscape-scout` |

Read-only agents (`prd-red-team-reviewer`, `security-compliance-auditor`) have no Write or Edit tools, so they can't change your files.

---

<sub>For the full reference on subagent file format, discovery rules, and routing behavior, see <a href="https://docs.claude.com/en/docs/claude-code/sub-agents">Claude Code: Subagents</a>.</sub>
