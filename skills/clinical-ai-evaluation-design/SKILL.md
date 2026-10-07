---
name: clinical-ai-evaluation-design
description: >
  Recommends how to evaluate a clinical predictive AI model, especially after a
  post-deployment monitoring signal: the immediate governance action, the right
  escalation pathway, study design, causal estimand, and the causal-inference method for
  common pitfalls. Based on the lifecycle and signal-to-trial framework in Fosset et al.,
  PLOS Digital Health (2026). Use this skill when the user asks how to evaluate or
  validate a clinical AI or ML model, what trial design to use for an AI tool, what to do
  when a deployed model drifts, loses calibration, shows subgroup bias, or when practice
  or guidelines change, or mentions estimands, stepped-wedge trials, or AI monitoring
  in healthcare. Part of the Pharma & Clinical pack.
---

> **Pharma & Clinical pack.** Built on a public, peer-reviewed framework. Cite it when you use this skill's recommendations.
>
> **Source:** Fosset M, Pensier J, Jung B, Siddiqi A, Mamdani M, Celi LA. *Clinical predictive artificial intelligence evaluation: A narrative review of trial designs and practical considerations.* PLOS Digital Health, 2026. https://doi.org/10.1371/journal.pdig.0001621

# Clinical AI Evaluation Design

The framework's central point: **performance monitoring, clinical impact monitoring, and scientific evidence generation are different activities, and one can't stand in for another.** Good AUROC doesn't show patients benefit, and a stable outcome dashboard doesn't prove the model caused anything. This skill matches each situation to the evidence it actually needs.

## Step 1 — Understand the model and the situation

Establish (ask if unclear):

- **The model:** what it predicts, who acts on it, and what action follows (alert, triage, dosing suggestion).
- **Lifecycle phase:** where it is now (see the table in Step 5).
- **The trigger:** a pre-deployment evaluation question, or a **monitoring signal** after deployment.
- **Thresholds:** whether pre-specified alert thresholds exist for performance, outcomes and fairness. If they don't, recommending them is the first finding.
- **Regulatory context:** for example, whether a Predetermined Change Control Plan (PCCP) covers model updates.

## Step 2 — Classify the monitoring signal

| Signal type | What it looks like |
|---|---|
| **Clinical outcome alert** | Measured patient outcomes get worse in the population using the model |
| **Performance degradation** | Technical metrics decline: calibration drift, lower discrimination (AUROC), more false alerts |
| **Fairness violation** | Performance gaps appear or widen across subgroups (age, sex, race/ethnicity, site, insurance) |
| **Context shift** | Something external changes the operating environment: new guidelines, practice patterns, case mix, EHR or lab changes |

## Step 3 — Apply the governance rule first

- **Below the pre-specified threshold:** continue surveillance; no escalation. Document the review.
- **Above the threshold:** take immediate governance action **before** any study: pause or roll back the model for the affected subgroup, so standard care resumes. Patient safety comes before evidence generation.

Then follow the escalation cycle: **Pause → Evaluate** (root-cause the drift) **→ Update** (recalibrate or retrain within the change-control boundaries) **→ Validate** (pre-deployment checks including a fairness audit and silent-mode testing; the paper's example uses 7 days) **→ Redeploy** (with post-update monitoring to confirm recovery).

## Step 4 — Choose the escalation pathway

| Pathway | When | Question | Design | Estimand |
|---|---|---|---|---|
| **1. Implementation audit** | Concern about process fidelity: were the governance procedures followed? | Did governance work as intended? | Audit of adherence to the pre-defined procedures | Not causal (monitoring) |
| **2. Hybrid dual-primary trial** | Performance degradation with possible patient impact: calibration decline, or subgroup performance below safety limits | Does restoring the model maintain clinical benefit? | Stepped-wedge cluster randomized trial with co-primary endpoints | (a) Implementation: restoration of model performance, e.g. calibration; (b) Patient outcomes: sustained clinical benefit |
| **3. Effectiveness trial** | A major failure, or an external context shift that fundamentally changes the clinical environment | Does the model still deliver patient benefit under the new conditions? | Pragmatic randomized controlled trial powered for patient outcomes | Direct effect of deployment on clinical endpoints (e.g. mortality, morbidity) |

Explain the choice in terms of the user's case, and say what would move it to a higher pathway.

## Step 5 — Lifecycle context

| Phase | Purpose |
|---|---|
| 1. Development and retrospective validation | Build the model and validate it on historical data |
| 2. Feasibility and workflow integration | Fit into clinical workflow; usability; silent-mode running |
| 3. Preliminary efficacy and safety | Single-center pilot with adverse-event monitoring |
| 4. Pragmatic randomized trial | Multi-center, possibly adaptive, powered for patient outcomes |
| 5. Post-deployment monitoring | Ongoing surveillance with escalation capability (Steps 2–4) |

The paper notes an alternative route: externally validated, stable models may go from Phase 2 straight to Phase 5. If you suggest this, say what evidence justifies skipping the trial phases.

## Step 6 — Anticipate the causal-inference traps

| Problem | Why it happens | Method to consider |
|---|---|---|
| Time-varying treatment–confounder feedback | The alert prompts clinician action, which changes the patient's trajectory and the next prediction | Marginal structural models with inverse probability weighting |
| Model version changes mid-study | You can't observe the same patient under both versions, so version effects mix with secular trends | Parametric g-formula, simulating outcomes under each deployment regime |
| Subgroup and equity questions | Too little power in vulnerable subgroups; site-level variation | Data fusion: combining trial and observational data |
| Cross-site transportability | Single-site results may not hold under other workflows and populations | Transportability analysis, reweighting to the target site's covariate distribution |

Recommend involving a biostatistician or epidemiologist for these methods.

## Output: evaluation plan

```markdown
# Evaluation plan: <model> · <signal or question>
**Signal type:** <…> · **Threshold exceeded:** Yes/No/Not defined
**Immediate governance action:** <continue surveillance / pause for subgroup … / roll back>
**Recommended pathway:** <1/2/3>: <name>
**Why:** <2–3 sentences tied to the case>

## Study design
- Design: <…>
- Primary estimand(s): <…>
- Population / clusters / unit: <…>
- Endpoints: <implementation and/or patient outcomes>
- Key causal-inference risks and methods: <…>

## Governance cycle
Pause → Evaluate → Update → Validate → Redeploy: <specific steps and owners>

## Gaps to close
- <e.g. no pre-specified thresholds; no subgroup monitoring; no PCCP>

**Reference:** Fosset et al., PLOS Digital Health, 2026. doi:10.1371/journal.pdig.0001621
```

## Guardrails

- This supports study planning; it doesn't replace review by a biostatistician, an ethics committee/IRB, or the organization's clinical governance and regulatory teams.
- Don't invent thresholds. If none exist, recommend that they be pre-specified and suggest how (clinically meaningful change, historical variation).
