---
name: prd-evaluator
description: >
  Evaluates an AI Product Requirements Document (PRD) against the appropriate rubric
  for its format — Full AI PRD (9 sections), One-Page PRD, or Agile Epic. Detects the
  format automatically and applies only the relevant criteria. Use this skill whenever
  a PM or student shares any PRD format and asks for feedback, review, evaluation, or
  a checklist check. Triggers include: "evaluate my PRD", "review my doc", "check my
  PRD", "what's missing", "thoughts on this?", or any product spec document shared
  for review — regardless of length or format.
metadata:
  author: Sankar Kumar Palaniappan
  email: hello@sankar.work
  version: 5.0
  category: product-management
  tags: [prd, evaluation, checklist, aipm, product-spec, agile, epic]
---

# PRD Evaluator — v5

---

## Step 1: Check for PRD Input

Before doing anything else, check whether the user has provided a PRD.

- If a PRD is present (pasted text or uploaded file): read it in full, then proceed to Step 2.
- If the user has uploaded a file: read the **entire** file before beginning. Do not start scoring until you have read the whole document.
- If no PRD has been provided: ask for it.

> "Please paste your PRD or upload the file and I'll evaluate it against the right checklist for its format."

Do not evaluate without a PRD. Do not ask any other questions first.

---

## Step 2: Detect Format

Read the document, then classify it into one of four formats using the signals below.
**Do this before scoring anything.** The format determines which sections are evaluated and which are N/A.

### Format Detection Signals

**Full AI PRD**
Any two or more of: a roadmap with phases, a pricing or cost section, a responsible AI section, an evaluation plan, a prompt strategy, model selection, market sizing, or explicit week labels (Week 1, Week 3, etc.)
→ Apply all 9 sections. Then run week-scope detection (Step 2b).

**One-Page PRD**
Short document (1–3 pages of content), summary or overview style, focused on problem + solution + key metrics. Typically has no detailed prioritization table, no pricing breakdown, no responsible AI pillars, no evaluation plan.
→ Apply Sections 1 and 2 only. Sections 3–9 are N/A.
→ Pass conditions apply at a summary level — a well-crafted sentence passes where a full paragraph is expected in a Full AI PRD.

**Agile Epic**
Story-based structure. Primary content is user stories ("As a…"), acceptance criteria, sprint or iteration scope, and story points or effort sizing. May have a "background" or "context" section but no multi-section product narrative.
→ Apply Sections 1 (Problem Definition items only — skip Core Metrics), 2, 3, and 4 (interpreted for sprint scope). Sections 5–9 are N/A.

**Unknown / Unclear**
Document is short but could be either a partial Full AI PRD or a One-Page PRD. Signals are mixed.
→ Ask the user before proceeding:
> "Is this a One-Page PRD for stakeholder alignment, a partial submission of a full AI PRD, or a different format? This determines which checklist I apply."

---

### Step 2b: Week-Scope Detection (Full AI PRD only)

If the format is Full AI PRD, check which weeks are present.

- If the PRD covers all 9 sections: evaluate all sections normally.
- If the PRD clearly covers only certain weeks (e.g. explicit week labels or only Week 1–2 content present): score only the sections submitted. For absent sections, show "— Week X not yet submitted" in the tile, not Blockers.
- The Verdict must name the actual scope.

A partial Full AI PRD is not a failed PRD. Do not penalise for sections not yet written.

---

## Step 3: Evaluate the PRD

Read the full document before scoring anything.

**Scanning rule:** For every criterion, scan the entire document. A dedicated section heading is not required. Evidence found anywhere — intro, problem statement, market context, roadmap, architecture, appendix — counts toward passing. Only fail an item if there is genuinely no evidence of it anywhere in the document.

**Four scoring outcomes:**

| Status | Meaning |
|---|---|
| **Pass** | Criterion is clearly met |
| **Blocker** | Criterion is missing and must be addressed before this PRD moves forward |
| **Improvement** | Criterion is weak or partially addressed — does not block progress but should be strengthened |
| **N/A** | Criterion is not applicable to this format — not a gap, not scored |

**Blocker vs Improvement guidance:** Use Blocker when the gap undermines core product thinking — no user flow, no MOAT, no launch criteria, no responsible AI assessment. Use Improvement when the content exists but lacks depth — metrics without baselines, a roadmap without durations, a data strategy without compliance mention.

---

## Format Scope Map

Use this to determine which sections to evaluate before writing the report.

| Section | Full AI PRD | One-Page PRD | Agile Epic |
|---|---|---|---|
| 1. Problem Definition | Evaluate (all 8 items) | Evaluate (all 8 items) | Evaluate (1.1–1.4 only) |
| 1. Core Metrics | Evaluate (all 4 items) | Evaluate (all 4 items) | N/A |
| 2. Solution Definition | Evaluate | Evaluate | Evaluate |
| 3. Prioritization | Evaluate | N/A | Evaluate |
| 4. Roadmap | Evaluate | N/A | Evaluate (sprint-adapted — see Section 4 note) |
| 5. Implementation Plan | Evaluate | N/A | N/A |
| 6. Evaluation Plan | Evaluate | N/A | N/A |
| 7. Data Requirements & Prompt Strategy | Evaluate | N/A | N/A |
| 8. Responsible AI | Evaluate | N/A | N/A |
| 9. Pricing & Cost Structure | Evaluate | N/A | N/A |

---

## Evaluation Checklist

---

### Section 1: Problem Definition & Core Metrics

**Full AI PRD and One-Page PRD:** Evaluate all 12 items.
**Agile Epic:** Evaluate items 1.1–1.4 only. Items 1.5–1.12 are N/A.

#### Problem Definition

| # | Criterion | Pass Condition |
|---|-----------|----------------|
| 1.1 | Problem & job-to-be-done clearly articulated | PRD states what the user is trying to accomplish and what is currently broken or missing — "the process is inefficient" is not specific enough |
| 1.2 | Customer persona(s) defined with role, industry, needs | At least one persona with a specific role, industry, and pain point — "enterprise users" or "SMBs" alone does not pass |
| 1.3 | Problem validated with real data or market research | Includes stats, interviews, survey data, market size, or cited research — assertions without evidence do not pass |
| 1.4 | Why this problem is worth solving for this user | Explains urgency, frequency, or cost of the problem to the target persona — "it's a big problem" is not enough |
| 1.5 | Clear and defensible MOAT defined | Names what makes this hard to copy — data advantage, domain fine-tuning, workflow lock-in, or network effects — "we use AI" or "better UX" does not pass |
| 1.6 | Justification for Agentic AI over rule-based systems | Explains why rules or logic alone cannot solve this — references variability, unstructured inputs, context, or judgment calls |
| 1.7 | Unstructured data types listed and need for ML/LLMs explained | Names the unstructured inputs (emails, PDFs, voice, images, etc.) and explains why pattern-matching or rule-based systems fail |
| 1.8 | Differentiated from ChatGPT, copilots, Claude Code, Co-Work, or similar tools | Explicitly addresses why existing AI tools do not solve this — workflow fit, domain specialisation, or integration depth |

#### Core Metrics

| # | Criterion | Pass Condition |
|---|-----------|----------------|
| 1.9 | North Star metric defined | One metric explicitly named as the primary success signal — multiple metrics listed without a declared winner does not pass |
| 1.10 | 1–2 primary metrics listed | Includes accuracy, time saved, task completion rate, or similar quantifiable outcomes with a unit |
| 1.11 | Secondary or supporting metrics included | Covers adoption, retention, cost reduction, or NPS — at least one |
| 1.12 | Metrics are measurable and trackable over time | Each metric has a unit, a baseline or target, and a plausible way to measure it — "we will track satisfaction" without a method does not pass |

---

### Section 2: Solution Definition

**All formats:** Evaluate all 4 items.

| # | Criterion | Pass Condition |
|---|-----------|----------------|
| 2.1 | Visual user flow included (input → processing → output) | Contains a diagram or clearly numbered step-by-step flow with distinct stages showing what the user does vs what the system does — prose paragraphs alone do not pass |
| 2.2 | AI drawbacks addressed (hallucination, explainability, etc.) | At least 2 risks acknowledged with mitigations — human-in-the-loop, confidence scores, audit trails, or disclaimers |
| 2.3 | Core functional requirements in user story format | Uses "As a [user], I want [action] so that [outcome]" format for key features — plain feature lists do not pass |
| 2.4 | Agent capabilities and system behaviour clearly described | States what the agent can do autonomously, what requires human approval, and how it handles errors or edge cases |

---

### Section 3: Prioritization

**Full AI PRD and Agile Epic:** Evaluate all 5 items.
**One-Page PRD:** N/A — mark all items as N/A in the report.

| # | Criterion | Pass Condition |
|---|-----------|----------------|
| 3.1 | Agentic workflow broken into components | Names at least 2–3 distinct pipeline stages (e.g. ingestion, extraction, analysis, summarisation) — "AI processes the data" does not pass |
| 3.2 | Risk assessment conducted per component | Each named component has at least one risk identified with severity or mitigation — generic AI risks not tied to specific components do not pass |
| 3.3 | ML feasibility, data availability, accuracy expectations, and explainability addressed | At least ML necessity and data availability are addressed per component — components with no feasibility reasoning do not pass |
| 3.4 | Features prioritised by risk, cost, and value | Stories or requirements have explicit priority labels (P0/P1/P2 or equivalent) with a rationale — unprioritised feature lists do not pass |
| 3.5 | Scope clearly narrowed to MVP with rationale | A clear boundary between what ships first and what is deferred, with a stated reason — a list that includes everything is not an MVP |

---

### Section 4: Roadmap

**Full AI PRD:** Evaluate all 5 items against the multi-phase product roadmap standard.
**Agile Epic:** Evaluate items 4.1, 4.2, 4.4 only — interpreted for sprint scope (see notes). Items 4.3 and 4.5 are N/A for Agile Epics.
**One-Page PRD:** N/A — mark all items as N/A in the report.

| # | Criterion | Pass Condition (Full AI PRD) | Pass Condition (Agile Epic) |
|---|-----------|-------------------------------|------------------------------|
| 4.1 | Clear phases listed: MVP, MVP1, Launch, Iteration | At least two distinct phases exist — a flat feature list without phases does not pass | Sprint or iteration scope is defined — "we will build this eventually" does not pass |
| 4.2 | Feature sets and target durations defined per phase | Each phase has both a feature description and a time estimate — phases without duration do not pass | Stories have story points or effort estimates — stories with no sizing do not pass |
| 4.3 | Roadmap items linked back to priorities and risks | Roadmap phases can be traced to prioritised stories or risk levels from Section 3 | N/A for Agile Epic |
| 4.4 | Dependencies named | At least one cross-functional dependency identified — data sourcing, legal, design, infra, or third-party — a PRD assuming all resources are available fails | At least one external dependency named (e.g. API access, design, data availability) |
| 4.5 | Phasing is realistic and distinct | MVP is meaningfully smaller than full launch — identical MVP and launch feature sets fail | N/A for Agile Epic |

---

### Section 5: Implementation Plan

**Full AI PRD only.** Mark N/A for One-Page PRD and Agile Epic.

| # | Criterion | Pass Condition |
|---|-----------|----------------|
| 5.1 | Model selection criteria and requirements listed | Names at least 2 specific criteria — context window, latency, cost, accuracy, open vs closed source — "we chose GPT-4" without criteria does not pass |
| 5.2 | Chosen model(s) justified against alternatives | At least one alternative is named and a reason given for not choosing it — a PRD with only the chosen model and no comparison does not pass |

---

### Section 6: Evaluation Plan

**Full AI PRD only.** Mark N/A for One-Page PRD and Agile Epic.

| # | Criterion | Pass Condition |
|---|-----------|----------------|
| 6.1 | AI performance evaluation described over time | Concrete evaluation approach with at least one eval type and method — "we will monitor the model" without specifics does not pass |
| 6.2 | Ground truth datasets or sources identified | Names a specific dataset, benchmark, or labelling process — "we will test accuracy" without stating against what does not pass |
| 6.3 | Accuracy thresholds or HHH (Helpful, Honest, Harmless) scores defined | At least one quantified target — ">90% F1", ">80% user satisfaction", or a populated HHH table — qualitative statements like "high accuracy" do not pass |
| 6.4 | Evaluation spreadsheet linked or planned | A link or an explicit plan with column headers — no mention of an eval spreadsheet does not pass |
| 6.5 | Launch criteria and go/no-go decision framework defined | Measurable criteria at each launch stage — "we will launch when ready" does not pass |
| 6.6 | Experimentation or A/B testing plan described | At least one experiment described — holdback, A/B test, or measurement launch rollout — "we will experiment" alone does not pass |
| 6.7 | Post-launch monitoring defined | States how AI performance will be tracked after launch — cadence, metrics, alerting threshold, or drift detection |

---

### Section 7: Data Requirements & Prompt Strategy

**Full AI PRD only.** Mark N/A for One-Page PRD and Agile Epic.

#### Data Requirements

| # | Criterion | Pass Condition |
|---|-----------|----------------|
| 7.1 | Data strategy listed (sources, formats, pipelines) | Names at least one specific data source, format, or pipeline — "we have the data" without specifics does not pass |
| 7.2 | Data quality, availability, and compliance constraints addressed | Mentions at least one of: quality checks, availability risk, or compliance constraint (GDPR, HIPAA, data residency) |

#### Prompt Strategy

| # | Criterion | Pass Condition |
|---|-----------|----------------|
| 7.3 | Prompting techniques described (few-shot, CoT, conditional, etc.) | Names at least one technique and explains why it was chosen — "we use prompts" or "we use GPT-4" alone does not pass |
| 7.4 | Prompt constraints and output formats defined per task type | At least one task has a defined output format or constraint — JSON schema, word limit, structured list — unconstrained output for all tasks does not pass |
| 7.5 | Plan for improving prompts based on user feedback and error analysis | Describes a process — versioned prompt library, A/B testing, error logging, or a correction-rate threshold that triggers review |

---

### Section 8: Responsible AI Risks & Mitigation

**Full AI PRD only.** Mark N/A for One-Page PRD and Agile Epic.

| # | Criterion | Pass Condition |
|---|-----------|----------------|
| 8.1 | Risks assessed across Accountability, Transparency, Fairness, and Reliability | All four pillars addressed — even briefly. PRDs covering only one or two pillars do not pass. |
| 8.2 | Human-in-the-loop and fallback paths planned | Names at least one scenario where human review is required and what the fallback is if the AI is wrong — "humans will review" without specifying when or what does not pass |
| 8.3 | Sensitive use cases and mitigation strategies listed | Names at least one high-stakes scenario specific to this product with a concrete mitigation — "we are aware of AI risks" does not pass |
| 8.4 | Bias, hallucination, and safe failure modes addressed | All three must be addressed — missing any one fails this item |

---

### Section 9: Pricing & Cost Structure

**Full AI PRD only.** Mark N/A for One-Page PRD and Agile Epic.

| # | Criterion | Pass Condition |
|---|-----------|----------------|
| 9.1 | Cost/accuracy tradeoffs explained | At least one infrastructure choice explained with its trade-off — listing what was chosen without the tradeoff does not pass |
| 9.2 | Development costs broken down (infra + manpower) | Separates infrastructure and manpower with at least rough figures — a single total without breakdown does not pass |
| 9.3 | Operational costs listed | Names at least 2 recurring cost items — LLM API, hosting, monitoring, maintenance, etc. |
| 9.4 | Market size calculated (TAM, SAM) | Provides both TAM and SAM with a source or rationale — numbers without basis do not pass |
| 9.5 | Revenue scenarios defined | At least two scenarios (e.g. conservative and target) with customer count and ARR — a single scenario is not enough |
| 9.6 | Pricing model selected with rationale | One model chosen as primary with an explicit reason — listing all models without selecting one does not pass |
| 9.7 | Directional pricing included | At least one price point named — "we will price competitively" is not directional pricing |

---

## Output Format

Structure your response exactly as shown below. Do not reorder sections.

---

### PRD Evaluation Report: [Product Name]

**Format detected:** [Full AI PRD / One-Page PRD / Agile Epic]
**Author: Sankar Kumar Palaniappan**
**X passing · X blockers · X improvements** *(count only evaluated sections — exclude N/A)*

Section summary tiles:

| Section | Status |
|---|---|
| 1. Problem Definition & Core Metrics | ● X blocker(s) · ● X improvement(s) — or — ● all pass |
| 2. Solution Definition | same |
| 3. Prioritization | same — or — *N/A for this format* |
| 4. Roadmap | same — or — *N/A for this format* |
| 5. Implementation Plan | same — or — *N/A for this format* |
| 6. Evaluation Plan | same — or — *N/A for this format* |
| 7. Data Requirements & Prompt Strategy | same — or — *N/A for this format* |
| 8. Responsible AI | same — or — *N/A for this format* |
| 9. Pricing & Cost Structure | same — or — *N/A for this format* |

For Full AI PRD partial submissions: show "— Week X not yet submitted" for absent sections.

---

#### Strengths

2–3 things the PRD does genuinely well, grounded in specific content from the actual document. One to two sentences each. Write this before gaps so the author knows what to keep.

---

#### Blockers

Two-column table: one row per Blocker across all evaluated sections.

| Item | Gap |
|---|---|
| [Section + item number and name] | [One sentence referencing the actual PRD — what is missing or absent] |

*See section detail below for what to write on each item.*

---

#### Improvements

Same format as Blockers.

| Item | Gap |
|---|---|
| [Section + item number and name] | [One sentence referencing the actual PRD] |

*See section detail below for what to write on each item.*

---

#### Section Detail

Repeat the block below for each **evaluated** section. Skip sections marked N/A entirely — do not list them in section detail.

For Agile Epics: include a brief note before the detail block stating which items were adapted for sprint scope (4.1, 4.2, 4.4) and which were N/A (4.3, 4.5, Core Metrics, Sections 5–9).

---

**Section X: [Name]**

Full item table — include every evaluated item, pass or not. For N/A items within a partially-applicable section (e.g. 1.5–1.8 in an Agile Epic, 4.3 and 4.5 in an Epic), include them in the table with status N/A and a one-word note "Not applicable for this format."

| Status | Item | Notes |
|---|---|---|
| Pass | 1.1 Problem & JTBD | One sentence on what is present, referencing the actual PRD |
| Blocker | 1.5 Defensible MOAT | One sentence on what is missing, referencing the actual PRD |
| Improvement | 1.12 Metrics trackable | One sentence on what is weak, referencing the actual PRD |
| N/A | 1.6 Agentic AI justified | Not applicable for this format |

Then for each Blocker and Improvement in that section, write a gap block:

**[Item number and name]**
**What's missing:** Reference the specific section or quote the closest thing the PRD has, then explain what is absent.
**What to write:** Concrete guidance with a short example — what a good version would actually say.

---

*(Repeat for all evaluated sections)*

---

#### Verdict

**Full AI PRD** — state one of four outcomes:
- **Ready to share** — minor gaps only, can proceed to engineering or leadership. Name what to tidy.
- **Send back** — list the specific Blockers that must be addressed, in priority order.
- **Needs a conversation** — fundamental questions about strategy or scope must be resolved first. Name them.
- **Week X complete** — for partial submissions: state which weeks are done, what remains, and name the strongest and weakest item in the submitted sections.

**One-Page PRD** — state one of three outcomes:
- **Ready to circulate** — covers problem, solution, and metrics well enough for stakeholder alignment. Name any quick tidies.
- **Strengthen before sharing** — has gaps that will draw questions in a stakeholder review. List the Blockers.
- **Needs more thinking** — core problem framing or solution logic has fundamental issues. Name them.

**Agile Epic** — state one of three outcomes:
- **Ready for sprint planning** — stories are well-formed, scoped, and have acceptance criteria. Name any quick tidies.
- **Needs refinement** — stories exist but lack acceptance criteria, sizing, or clear scope. List the Blockers.
- **Missing critical stories** — core user flows are absent or the epic scope is unclear. Name what is missing.

---

## Tone and Style Guidelines

- Be direct and specific — PMs need actionable feedback, not vague encouragement
- When something is missing, always say what to write, not just "add more detail"
- Reference or quote specific sections of the actual PRD when calling out gaps — do not describe problems in the abstract
- Use examples when helpful — show what a good version would say, not just what is wrong
- Be honest: a PRD with 6 blockers should feel like it has 6 blockers, not softened
- For Sections 3–9 (new sections), always note where in the document you looked before concluding something is absent — these sections may live under different headings
- Never score an N/A item as a Blocker or Improvement — "not applicable" is not a gap
- For partial Full AI PRD submissions, do not penalise for weeks not yet written
- For One-Page PRDs, interpret pass conditions at summary depth — a well-crafted sentence passes where a paragraph is expected in a Full AI PRD
- For Agile Epics, interpret Section 4 against sprint/iteration standards, not multi-phase product roadmap standards


## Step 4: Save and Deliver the Report

After writing the full evaluation to screen, ALWAYS save it as a file:

1. Save the complete report (everything from "PRD Evaluation Report:" through
   the Verdict) to the outputs folder as:
   `[product-name-slug]-prd-evaluation-[YYYY-MM-DD].md`
   Example: `product-prd-evaluation-2026-06-04.md`

2. Provide a computer:// link so the user can open the file directly.

3. If the user has Google Drive connected (check for available MCP tools),
   also export the report as a Google Doc using the Drive connector.
   If Google Drive is not connected, skip step 3 silently — do not ask.
