# mockup-generator

A [Claude Code](https://docs.claude.com/en/docs/claude-code) **subagent** that turns a written PRD (Product Requirements Document) into a set of high-fidelity, clickable HTML mockups — so a team can click through a spec and react to it before a line of production code is written.

```
.claude/agents/mockup-generator.md
```

![type](https://img.shields.io/badge/type-project--local%20subagent-4f46e5)
![tools](https://img.shields.io/badge/tools-Read%20·%20Write%20·%20Edit%20·%20Glob%20·%20Grep%20·%20Bash-0ea5e9)
![model](https://img.shields.io/badge/model-inherit-22c55e)

---

## What it does

Point this agent at a PRD (PDF, Markdown, docx-as-text, or pasted text) and it produces a **navigable, realistic prototype** — not a static design comp. It reads the spec end to end, plans a screen inventory and flow map, establishes a small shared design system, then builds a set of self-contained HTML files that link to each other like the real product would. Every screen traces back to a specific requirement, user story, or flow in the source document, and the handoff includes a list of assumptions and open questions for a human to resolve.

It's the agent to reach for when someone wants to **see** a spec rather than read it — to pressure-test ambiguity, give stakeholders something concrete to react to, or give a PM/designer/engineer a shared artifact to align on before design or engineering investment begins.

## When Claude Code reaches for it

This agent triggers on requests like:

- "Mock up / wireframe / prototype this PRD"
- "Can you design the screens for this feature spec?"
- "Build a clickable demo of what this document describes"
- "I want something stakeholders can click through and react to"
- "Show me what this would look like" (in the context of a written spec)

Claude Code matches subagents by their `description` frontmatter, so the more clearly a request maps to "I have a spec, I want to see it as a UI," the more reliably this agent is selected over ad‑hoc HTML generation.

## Configuration

```yaml
---
name: mockup-generator
description: >-
  Turns a PRD (Product Requirements Document) into a set of high-fidelity,
  clickable HTML mockups. Use this agent whenever the user has a PRD, product
  spec, feature brief, or written requirements (PDF, Markdown, docx, or pasted
  text) and wants to SEE it...
tools: Read, Write, Edit, Glob, Grep, Bash
model: inherit
---
```

| Field | Value | Why |
| --- | --- | --- |
| `tools` | `Read, Write, Edit, Glob, Grep, Bash` | Enough to ingest a PRD (including PDFs), generate/edit a multi-file static site, and self-check its own output (e.g. grepping for stray template-literal artifacts) — and nothing more. No network or destructive tools. |
| `model` | `inherit` | Runs on whichever model drives the parent session, so its output quality tracks the user's chosen model. |

## How it works — the six-phase workflow

The agent's system prompt encodes a designer-grade process, not just "write some HTML":

1. **Ingest and understand the PRD** — reads the document fully (PDF and all), and extracts the product/goal, personas, user flows, screen inventory, data entities, and business rules/copy before designing anything.
2. **Plan the screen inventory and flow map** — shares a numbered screen list, navigation map, key assumptions, and open questions with the user *before* building, so misalignment gets caught early and cheaply.
3. **Establish a lightweight design system first** — locks down color, type, spacing/radius, and a shared component vocabulary once, so every screen feels like one product.
4. **Build the mockups** — generates the actual files: an `index.html` hub plus one file per screen, fully clickable (buttons navigate, tabs switch, modals open) with no backend.
5. **Self-review before handoff** — runs a explicit checklist (coverage, states, navigation, content realism, consistency, responsive/accessible, assumptions logged) and fixes what fails.
6. **Hand off** — ends with how to open it, the screen list, assumptions made, open questions for a human, and a map of screens back to PRD requirements.

## Output conventions

Everything the agent produces is a **self-contained, zero-build static site** — no `npm install`, no bundler, no server required (though one can be served locally for convenience):

- One HTML file per screen, **Tailwind CSS via CDN**, **vanilla JS**, **Lucide icons**, **Google Fonts**, and placeholder images only where genuinely needed.
- A conventional file layout under `mockups/`:
  ```
  mockups/
  ├── index.html        # Hub: product framing, flow map, links to every screen
  ├── screens/          # 01-search.html, 02-results.html, … ordered like a storyboard
  ├── assets/           # shared styles.css / app.js so screens don't visually drift
  └── README.md         # what this is, how to open it, screen → PRD traceability
  ```
- Realistic, domain-plausible content throughout — **never lorem ipsum** — and deliberate coverage of empty/loading/error/success states, not just the happy path.

## Operating principles worth knowing

- **The PRD is the source of truth, not a cage.** It implements what's specified and makes sensible, conventional, *logged* decisions where the spec is silent — rather than stalling on every ambiguity.
- **Realism over lorem ipsum.** Believable names, prices, dates, and copy drawn from the document's domain.
- **Show the system, not just the happy path.** Empty states, loading, errors, permission-denied, and "lots of data" cases are treated as first-class, not afterthoughts.
- **Design with intent, justify with the PRD.** If a screen can't be traced to a requirement or story, the agent questions whether it belongs.
- It explicitly **avoids** inventing or dropping scope, blocking on answerable questions, adding real backends/build steps, or letting visual polish paper over functional gaps.

## Using it

Drop `mockup-generator.md` into a project's `.claude/agents/` directory (project-local) — or `~/.claude/agents/` for a user-level agent available across projects — and invoke it naturally:

```
Use the mockup-generator agent to turn docs/HotelBooking-PRD.pdf into clickable mockups.
```

```
Mock up the screens described in this feature spec — I want something the team can click through in tomorrow's review.
```

Claude Code will route matching requests to it automatically based on the `description` field; you can also invoke it by name. The agent will narrate its plan after Phase 2 (the screen inventory and flow map) so you can redirect course before it builds everything out.

## Example output

Running this agent against a 19-page hotel-booking-cancellation PRD produced an 11-screen interactive workspace (`mockups/`) — sign-in, dashboard, at-risk queue, booking detail, forecast, automation rules, intervention ROI, model monitoring, segment analytics, and settings — sharing one design-token layer (`assets/app.css`, `assets/data.js`, `assets/app.js`), each screen citing the specific PRD requirements (FR1–FR12, user stories, sections) it serves. See that mockup set's own `README.md` for a fuller example of the kind of traceability and assumptions log this agent produces.

---

<sub>Project-local Claude Code subagent. See <a href="https://docs.claude.com/en/docs/claude-code/sub-agents">Claude Code: Subagents</a> for how subagent files are structured and discovered.</sub>
