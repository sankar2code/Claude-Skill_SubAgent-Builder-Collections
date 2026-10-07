# PRD → Production pack

Five Claude Code skills that take a PRD to a running, secure Next.js + Supabase app through approval-gated stages. I built and used this workflow to ship **ContractIQ**, an AI contract-review platform for NDAs and MSAs.

```
prd-writer ──► engineering-planner ──► implementation-specs ──► security-foundation ──► frontend-setup ──► build features
 (PRD)          Stage 1                Stage 2                  Stage 3                 Stage 4            Stage 5
                                                                                          design-system: always on for UI
```

## The one rule

After every stage, Claude stops, shows what it produced, and waits for your approval. Nothing moves forward on assumptions, and no code is written before the specs exist.

## Stages

| Stage | Skill | Input | Output |
|---|---|---|---|
| 1 | `engineering-planner` | PRD | `docs/engineering/engineering-doc.md`: architecture, flows, DB design, API spec, phases, folder structure, testing strategy |
| 2 | `implementation-specs` | Engineering doc | `docs/specs/*.md`, `docs/specs/supabase-schema.sql` (paste-and-run), `.env.example` |
| 3 | `security-foundation` | Engineering doc + specs | `docs/security/security-plan.md`, `supabase/rls-policies.sql`, `lib/security/*`, server-side auth routes |
| 4 | `frontend-setup` | Specs | Next.js 16 + React 19 + TypeScript project, running on localhost |
| 5 | build features | `docs/specs/` | One feature at a time, each confirmed before coding, with `design-system` applied to all UI |

After Stage 5: write unit, integration and E2E tests, run a production build, deploy, and smoke-test the live app.

## Default stack

- **Frontend:** Next.js 16 (App Router), React 19, TypeScript
- **Backend:** Supabase (Postgres, Auth, Storage, Row Level Security)
- **Validation:** Zod
- If your PRD names a different backend, database or LLM provider, the planner uses it and the later stages follow.

## How to run it

1. Install the skills (see the main [README](../README.md)).
2. Put your PRD in the project, or write one with `prd-writer`.
3. Ask Claude Code: *"Create the engineering doc from docs/prd.md."*
4. Review, approve, and continue: *"Generate the implementation specs"*, *"Set up security"*, *"Set up the Next.js project"*, then *"Build the first feature."*

## Why security comes before the frontend

Controls like Row Level Security, ownership checks, rate limits and prompt-injection guards are cheap to build in and expensive to retrofit. Running `security-foundation` before any feature code means every feature is built on top of them. You can also re-run it later as an audit of an existing app.
