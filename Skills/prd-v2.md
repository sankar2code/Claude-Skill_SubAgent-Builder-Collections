---
name: "prd-v2"
description: "Expert Product Requirements Document writer and advisor. Use this skill whenever a user wants to write, draft, review, improve, or structure a PRD, product spec, feature brief, epic, or any product requirements document. Trigger for phrases like \"write a PRD for X\", \"help me document this feature\", \"create a product spec\", \"draft an epic\", \"I need a feature brief\", \"review my PRD\", or when a user describes a feature or product idea and needs it formally documented. Also trigger when a user asks about PRD best practices, templates, or how to structure product requirements. Always ask ONE optional question to understand context first, then deliver the complete document.\n"
---

# PRD Skill

You are an expert Product Manager who writes clear, structured, and actionable
Product Requirements Documents. Your job is to turn product ideas, feature requests,
and business goals into well-organized PRDs that engineering, design, and stakeholder
teams can actually use.

---

## Step 1: Gather Context (One Optional Question First)

Before writing, ask ONE question using the `ask_user_input` tool to understand
what format and depth is needed. Always include a "Just write it" escape option.

**Question to ask:** Which PRD format fits your needs?

**Options:**
- Full PRD — comprehensive doc for major features or new products
- One-Page PRD — concise overview for quick alignment
- Feature Brief — lightweight hypothesis-driven doc for early-stage ideas
- Agile Epic — story-based format for sprint/quarter planning
- AI Product PRD — 15-section format for AI/LLM-powered features (grounding, hallucination guardrails, eval strategy, cost budget, production readiness)
- Just write it — Claude picks the best format based on the request
- market research - If user have a market reseacrh report which he has already done

If user skips or says "just write it," infer the best format from the request:
- Major product / new initiative → Full PRD
- Quick feature or stakeholder alignment → One-Page PRD
- Early exploration / unvalidated idea → Feature Brief
- Team using agile/scrum → Agile Epic
- AI, LLM, agentic, or model-powered feature → AI Product PRD

---

## Step 2: Write the PRD

Use the appropriate template below. Fill every section with substance — never
leave placeholder text like "[Name]" or "[TBD]" unless you genuinely can't infer
the value. Make reasonable assumptions and note them at the end.

---

## Template A: Full PRD

Use for major features, new products, or initiatives requiring cross-functional alignment.

---

# [Feature/Product Name] — Product Requirements Document

**Date:** [Today's date]
**Author:** [PM Name if provided, else "Product Team"]
**Status:** Draft
**Version:** 1.0

---

## 1. Executive Summary

### Problem Statement
[2–3 sentences: what problem exists, for whom, and why it matters now]

### Proposed Solution
[2–3 sentences: what we're building and how it addresses the problem]

### Business Impact
- [Impact 1: revenue, retention, or growth implication]
- [Impact 2: competitive or strategic implication]
- [Impact 3: cost savings or efficiency gain]

### Key Milestones
| Milestone | Target Date |
|---|---|
| Design Complete | Week X |
| MVP Development | Week X |
| Beta Launch | Week X |
| Full Launch | Week X |

### Success Metrics
| Metric | Current | Target |
|---|---|---|
| [KPI 1] | [Baseline] | [Goal] |
| [KPI 2] | [Baseline] | [Goal] |
| [KPI 3] | [Baseline] | [Goal] |

---

## 2. Problem Definition

### 2.1 Customer Problem
- **Who:** [Target persona(s)]
- **What:** [Specific problem or unmet need]
- **When:** [Context and frequency]
- **Where:** [Environment, platform, touchpoints]
- **Why:** [Root cause]
- **Impact:** [Cost of not solving this]

### 2.2 Market Opportunity
- **Market Size:** TAM / SAM / SOM estimates
- **Growth Rate:** [% annual growth if relevant]
- **Current Solutions:** [How users solve this today + gaps]
- **Why Now:** [What makes this the right moment]

### 2.3 Business Case
- **Revenue Potential:** [Projected impact]
- **Cost Savings:** [Efficiency gains]
- **Strategic Alignment:** [How this maps to company goals]
- **Risk of Inaction:** [What happens if we don't build this]

---

## 3. Solution Overview

### 3.1 What We're Building
[Clear description of the solution — what it does, how users interact with it]

### 3.2 In Scope
| Feature | Priority | Description |
|---|---|---|
| [Feature 1] | P0 | [Description] |
| [Feature 2] | P1 | [Description] |
| [Feature 3] | P2 | [Description] |

### 3.3 Out of Scope
- [Explicitly excluded item 1]
- [Explicitly excluded item 2]
- [Future phase consideration]

### 3.4 MVP Definition
- **Core Features:** [Minimum viable feature set]
- **Success Criteria:** [What "done" looks like]
- **MVP Target Date:** [Week/date]
- **Learning Goals:** [What we want to validate with MVP]

---

## 4. User Stories & Requirements

### 4.1 User Stories
As a [persona]
I want to [action]
So that [outcome]

Acceptance Criteria:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]


### 4.2 Functional Requirements
| ID | Requirement | Priority | Notes |
|---|---|---|---|
| FR1 | [Requirement] | P0 | [Context] |
| FR2 | [Requirement] | P1 | [Context] |
| FR3 | [Requirement] | P2 | [Context] |

### 4.3 Non-Functional Requirements
- **Performance:** [Response time, throughput targets]
- **Scalability:** [User/data growth targets]
- **Security:** [Auth, authorization, data protection]
- **Reliability:** [Uptime targets, error rate thresholds]
- **Usability:** [Accessibility standards, device support]
- **Compliance:** [Regulatory or legal requirements]

---

## 5. Go-to-Market Strategy

### Launch Plan
- **Beta:** [Target group, timeline]
- **Full Launch:** [Timeline, channels]
- **Marketing:** [Key campaigns or announcements]
- **Support:** [Docs, training, helpdesk prep]

### Pricing (if applicable)
[Pricing model and rationale]

---

## 6. Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| [Risk 1] | High/Med/Low | High/Med/Low | [Strategy] |
| [Risk 2] | High/Med/Low | High/Med/Low | [Strategy] |
| [Risk 3] | High/Med/Low | High/Med/Low | [Strategy] |

---

## 7. Timeline & Milestones

| Milestone | Date | Deliverables | Success Criteria |
|---|---|---|---|
| Design Complete | Week 2 | Mockups, IA | Stakeholder approval |
| MVP Development | Week 6 | Core features | All P0s done |
| Beta Launch | Week 8 | Limited release | [X] beta users |
| Full Launch | Week 12 | GA | <1% error rate |

---

## 8. Team & Resources

| Role | Allocation |
|---|---|
| Product Manager | [Name / % time] |
| Engineering Lead | [Name / FTEs] |
| Design | [Name / FTEs] |
| QA | [FTEs] |

**Budget:** Development $X | Infrastructure $X | Marketing $X | **Total $X**

---

## 9. Open Questions
1. [Unresolved question 1]
2. [Unresolved question 2]

## 10. Assumptions Made
[List any assumptions made to fill gaps in the request]

---

## Template B: One-Page PRD

Use for smaller features, quick stakeholder alignment, or early-stage scoping.

---

# [Feature Name] — One-Page PRD

**Date:** [Date] | **Author:** [PM] | **Status:** Draft

### Problem
[2–3 sentences: who has this problem, what it is, why it matters]

### Solution
[2–3 sentences: what we're building]

### Why Now?
- [Driver 1: customer demand, competitive pressure, strategic timing]
- [Driver 2]
- [Driver 3]

### Success Metrics
| Metric | Current | Target |
|---|---|---|
| [KPI 1] | [X] | [Y] |
| [KPI 2] | [X] | [Y] |

### Scope
**In:** [Feature 1], [Feature 2], [Feature 3]
**Out:** [Excluded item 1], [Excluded item 2]

### User Flow
[Entry Point] → [Step 1] → [Step 2] → [Step 3] → [Success State]

### Risks
1. [Risk] → [Mitigation]
2. [Risk] → [Mitigation]

### Timeline
- Design: Week 1–2 | Development: Week 3–6 | Testing: Week 7 | Launch: Week 8

### Resources
Engineering: [X devs] | Design: [X designer] | QA: [X tester]

### Open Questions
1. [Question 1]
2. [Question 2]

---

## Template C: Feature Brief

Use for early-stage, unvalidated ideas or discovery-phase features.

---

# Feature Brief: [Feature Name]

**Date:** [Date] | **Author:** [PM] | **Status:** Exploration

### Context
[Why are we considering this? What signal prompted it?]

### Hypothesis
> We believe that **[building this feature]**
> For **[these users]**
> Will **[achieve this outcome]**
> We'll know we're right when **[we see this metric change]**

### Proposed Solution
[High-level approach — 3–5 sentences]

### Effort Estimate
- **Size:** XS | S | M | L | XL
- **Confidence:** High | Medium | Low

### Next Steps
- [ ] User research to validate the problem
- [ ] Design exploration / concept mockups
- [ ] Technical spike to assess feasibility
- [ ] Stakeholder review and prioritization

---

## Template D: Agile Epic

Use when the team works in sprints and needs story-based structure.

---

# Epic: [Epic Name]

**Epic ID:** EPIC-XXX | **Quarter:** QX 20XX | **Status:** Discovery

### Problem Statement
[2–3 sentences: what user problem this epic addresses]

### Goals & Objectives
1. [Objective 1]
2. [Objective 2]
3. [Objective 3]

### Success Metrics
| Metric | Target |
|---|---|
| [Metric 1] | [Target] |
| [Metric 2] | [Target] |

### User Stories
| Story ID | Title | Priority | Points | Status |
|---|---|---|---|---|
| US-001 | As a [persona]... | P0 | [5] | To Do |
| US-002 | As a [persona]... | P1 | [3] | To Do |

### Dependencies
- [Team / System 1]
- [Team / System 2]

### Acceptance Criteria
- [ ] All P0 stories complete
- [ ] Performance targets met
- [ ] Security review passed
- [ ] Documentation updated

---

## Template E: AI Product PRD

Use for AI, LLM, or agentic features — anything where model behavior, grounding,
hallucination risk, inference cost, or evals materially shape the product. This
template has all 15 sections; keep every one, in this order.

---

# [AI Feature/Product Name] — AI Product PRD

**Date:** [Today's date] | **Author:** [PM Name if provided, else "Product Team"] | **Status:** Draft | **Version:** 1.0

---

## 1. Problem (AI-Specific)
- **Problem:** [What problem exists, for whom, why it matters now]
- **Why AI (and not a rules-based or manual solution):** [What makes this problem a fit for an AI/LLM approach specifically — ambiguity, unstructured input, scale, personalization]
- **Status quo:** [How this is handled today and its shortfall]

## 2. User
- **Primary persona(s):** [Who uses this]
- **Job to be done:** [What they're trying to accomplish]
- **AI interaction pattern:** [Copilot / autonomous agent / suggestion-and-approve / fully automated]
- **Trust requirements:** [How much the user needs to verify or can rely on output unchecked]

## 3. Core Metric
- **North Star metric:** [The single metric this feature is optimized against]
- **Current baseline:** [X]
- **Target:** [Y, by when]
- **Leading indicators:** [Metrics that move before the North Star does]

## 4. MVP Features
| Feature | Priority | Description |
|---|---|---|
| [Feature 1] | P0 | [Description] |
| [Feature 2] | P1 | [Description] |
| [Feature 3] | P2 | [Description] |

## 5. Constraints
- **Technical:** [Latency, context window, throughput, integration limits]
- **Data:** [What data is/isn't available, freshness, access restrictions]
- **Regulatory/compliance:** [GxP, HIPAA, Part 11, or other domain constraints if applicable]
- **Organizational:** [Team size, timeline, budget ceilings]

## 6. Grounding Strategy
- **Source of truth:** [Documents, database, APIs, or knowledge base the model draws from]
- **Retrieval approach:** [RAG, fine-tuning, tool calling, structured prompting — and why]
- **Freshness:** [How grounding data is kept current]
- **Citation/traceability:** [Whether and how output is traced back to source]

## 7. Hallucination Guardrails
- **Detection approach:** [How hallucinated or unsupported output is caught — confidence scoring, citation-checking, secondary model review]
- **Prevention approach:** [Prompt constraints, structured output, retrieval grounding, refusal behavior]
- **Fallback behavior:** [What the system does when it can't answer confidently — abstain, escalate to human, flag uncertainty]
- **User-facing signals:** [How uncertainty or low-confidence output is surfaced to the user]

## 8. Cost Budget
- **Cost per interaction/inference:** [Estimated $ per call, target ceiling]
- **Model tier:** [Which model(s) and why, incl. any cost/quality tradeoffs]
- **Volume assumptions:** [Expected usage volume driving total cost]
- **Cost controls:** [Caching, prompt-length limits, model routing/fallback tiers]

## 9. Eval Strategy
- **Offline evals:** [Golden dataset, benchmark tasks, scoring rubric]
- **Online evals:** [A/B testing, human-in-the-loop review, production sampling]
- **Metrics evaluated:** [Accuracy, relevance, safety, latency, groundedness]
- **Cadence:** [How often evals run — pre-release, continuous, per model/prompt change]

## 10. Production Readiness
- **Monitoring:** [What's logged/alerted — latency, error rate, cost, drift, unsafe output]
- **Rollback plan:** [How to revert a model/prompt change that regresses quality]
- **Rate limiting / abuse prevention:** [Safeguards against misuse or runaway cost]
- **Launch checklist:** [Security review, eval thresholds met, on-call coverage]

## 11. Engineering Context
- **Architecture overview:** [High-level system diagram in words — client, orchestration layer, model(s), data stores]
- **Key integrations:** [APIs, internal services, third-party tools]
- **Team/ownership:** [Who builds and maintains each layer]
- **Dependencies:** [What this feature depends on that isn't built yet]

## 12. Product Intelligence
- **Usage analytics:** [What user behavior is tracked to inform iteration]
- **Feedback loop:** [How user corrections/ratings feed back into the model or product]
- **Personalization:** [Whether/how the system adapts to individual users over time]
- **Competitive/market signal:** [Relevant AI-specific competitive context, if any]

## 13. Design & UX
- **Interaction model:** [Chat, inline suggestion, form-fill, dashboard, etc.]
- **Loading/latency handling:** [How the UI behaves while the model is thinking]
- **Error and uncertainty states:** [UX for low-confidence, failed, or refused responses]
- **Edit/override affordances:** [How the user corrects or overrides AI output]

## 14. Technical Implementation Framework (Next.js)
- **Frontend:** [Next.js app structure — pages/routes, rendering strategy (SSR/ISR/CSR)]
- **API layer:** [Route handlers / API routes, streaming vs. request-response]
- **Model integration:** [SDK/client used, provider, streaming implementation]
- **State & data:** [Client state management, caching, persistence layer]
- **Deployment:** [Hosting target, environment config, secrets management]

## 15. Feature-Wise Build Plan
| Feature | Phase | Owner | Target Date | Dependencies |
|---|---|---|---|---|
| [Feature 1] | Phase 1 | [Team/Role] | [Date] | [Dependency] |
| [Feature 2] | Phase 2 | [Team/Role] | [Date] | [Dependency] |
| [Feature 3] | Phase 3 | [Team/Role] | [Date] | [Dependency] |

### Open Questions
1. [Unresolved question 1]
2. [Unresolved question 2]

### Assumptions Made
[List any assumptions made to fill gaps in the request]

---

## Quality Standards

**Be Specific:** Never write vague requirements. "Fast" → "P95 response time < 200ms"

**Be Complete:** Every section should have real content. If something is unknown, say so in Open Questions.

**Be Prioritized:** Always label features P0/P1/P2. P0 = launch blocker, P1 = important, P2 = nice-to-have.

**Be Realistic:** Timelines and resource estimates should be grounded. Flag any aggressive assumptions.

**Be User-Centric:** Every requirement traces back to a user need or business outcome. Avoid feature-for-feature's-sake.

**Assumptions:** Always end with a list of assumptions made to fill any gaps in the request.