---
name: gxp-part11-checker
description: >
  Reviews a software system, feature, PRD, user story, or AI tool used in a regulated
  (GxP) life-sciences setting against FDA 21 CFR Part 11 (electronic records and
  signatures), EU GMP Annex 11, and ALCOA+ data-integrity principles. Produces a
  requirement-by-requirement gap assessment, a risk rating, and concrete fixes written as
  testable requirements. Use this skill when the user mentions Part 11, Annex 11, GxP,
  CSV or CSA, validation, audit trails, e-signatures, data integrity, ALCOA, IQ/OQ/PQ,
  or asks "is this compliant", "what do we need for a regulated system", or "review this
  for GxP". Part of the Pharma & Clinical pack.
---

> **Pharma & Clinical pack.** Written from hands-on GxP delivery work on regulated systems in pharma.

# GxP / 21 CFR Part 11 Checker

Turn regulatory text into build-ready requirements. Regulated teams lose the most time when compliance is discovered late, in validation or an audit, instead of designed in at the PRD stage.

**Important:** this produces a structured self-assessment to support the team's Quality and Regulatory functions. It is not a legal opinion or a formal validation, and final decisions belong to the organization's Quality Assurance unit.

## Step 1 — Establish scope

Ask (or infer and state):

1. **What is it?** System, feature or AI tool; what it does; who uses it.
2. **Which GxP area?** GCP (clinical), GMP (manufacturing), GLP (lab), GVP (pharmacovigilance), or none.
3. **Which records does it create, change, store or transmit?** Is any of them required by a predicate rule (the underlying regulation that requires the record, e.g. GCP or GMP regulations), or submitted to a regulator?
4. **Does it use electronic signatures** in place of handwritten ones?
5. **Market:** US (Part 11), EU (Annex 11), or both.
6. **Hosting:** on-premise, SaaS, or cloud, and who the supplier is.

**If no records are required by a predicate rule and nothing goes to a regulator, Part 11 likely doesn't apply.** Say so and recommend documenting that rationale. Good data-integrity practice is still worth following.

## Step 2 — Classify risk

Rate the system **High / Medium / Low** GxP impact based on patient safety, product quality and data integrity. For example, an EDC or safety database is High; an internal training tracker is usually Low. Under a risk-based approach (GAMP 5, and FDA's Computer Software Assurance approach), the depth of validation and controls should match the risk. Say how the rating changes the recommendations.

## Step 3 — Assess against the requirements

Assess each item as **Met / Partial / Gap / Not applicable / Unknown**, with the evidence (what in the design or PRD shows it) and a fix.

### 21 CFR Part 11, Subpart B — Electronic records

| Ref | Control | What to look for |
|---|---|---|
| 11.10(a) | Validation | The system is validated for accuracy, reliability and consistent intended performance, and can detect invalid or altered records |
| 11.10(b) | Accurate, complete copies | Records can be produced in human-readable and electronic form for inspection |
| 11.10(c) | Record protection | Records are retained and retrievable for the full retention period |
| 11.10(d) | Access limited | Only authorized individuals can access the system |
| 11.10(e) | Audit trail | Secure, computer-generated, time-stamped trail of who did what and when for creating, modifying or deleting records; changes don't obscure previous values; retained as long as the record |
| 11.10(f) | Operational checks | Steps and events happen in the required sequence where that matters |
| 11.10(g) | Authority checks | Only authorized people can sign, change records, or perform specific operations (role-based permissions) |
| 11.10(h) | Device checks | The validity of input sources (devices, terminals, integrations) is checked where appropriate |
| 11.10(i) | Training | People who build, maintain or use the system have the education, training and experience for their tasks |
| 11.10(j) | Signature accountability policy | Written policy holding people accountable for actions under their e-signature |
| 11.10(k) | Documentation controls | Controlled distribution, access and change history for system documentation |
| 11.30 | Open systems | Extra controls (such as encryption) when the system is open to parties outside the organization's control |
| 11.50 | Signature manifestation | Signed records show the signer's printed name, date and time, and the meaning of the signature (review, approval, authorship) |
| 11.70 | Signature/record linking | Signatures can't be cut, copied or transferred to falsify another record |

### Subpart C — Electronic signatures

| Ref | Control | What to look for |
|---|---|---|
| 11.100 | Uniqueness and identity | Each e-signature belongs to one person, is never reused or reassigned, and identity is verified before it's issued |
| 11.200 | Components | Non-biometric signatures use at least two distinct components (e.g. user ID + password). In one continuous session, the first signing uses all components and later signings use at least one |
| 11.300 | ID and password controls | Unique ID/password combinations, periodic review, loss management, safeguards against unauthorized use, and testing of tokens or devices |

Also note that organizations using e-signatures must certify to FDA that they are legally binding equivalents of handwritten signatures (11.100(c)).

### EU GMP Annex 11 (if the EU is in scope)

Check additionally: risk management through the lifecycle, supplier assessment and agreements, validation with traceability to user requirements, data checks for interfaces, periodic evaluation, security, audit trails based on risk, change and configuration management, incident management, business continuity, archiving, and batch release (if GMP).

### ALCOA+ data integrity

| Principle | Check |
|---|---|
| Attributable | Every entry tied to a unique user |
| Legible | Readable and permanent for the retention period |
| Contemporaneous | Recorded when the activity happens, with a trustworthy timestamp (synchronized clock, defined time zone) |
| Original | The first capture, or a certified true copy, is kept |
| Accurate | Validated inputs, checks, no unexplained edits |
| Complete | Nothing deleted without a trail; includes metadata |
| Consistent | Chronological, sequenced, consistent formats |
| Enduring | Survives the retention period, including format migrations |
| Available | Retrievable for review and inspection when needed |

## Step 4 — AI and machine-learning features (if any)

If the system uses AI or an LLM in a GxP process, also check:

- **Intended use and human oversight:** is AI output advisory, with a qualified person reviewing and approving it? Is the reviewer's decision captured in the audit trail?
- **Traceability:** model and prompt version, inputs, outputs, and confidence logged with each record the AI influenced.
- **Validation:** performance tested on representative data against acceptance criteria; known failure modes documented.
- **Change control:** model, prompt or provider changes go through change control and regression testing; nothing changes silently. Pinned model versions where the provider allows it.
- **Data protection:** patient or confidential data handled under the right agreements; no training on regulated data without approval.
- **Monitoring:** ongoing checks for drift and errors, with a defined path to pause the feature.

## Step 5 — Validation approach

Recommend a proportionate approach:

- **Documents:** user requirements (URS), risk assessment, functional/configuration specification, traceability matrix, test protocols, validation summary report.
- **Qualification:** IQ (installed correctly), OQ (operates as specified), PQ (performs for its intended use in the real process). For SaaS, leverage supplier documentation and focus testing on configuration and intended use.
- **Under a Computer Software Assurance mindset:** focus rigorous scripted testing on high-risk functions and use unscripted or exploratory testing for lower-risk ones.

## Output: gap assessment

```markdown
# GxP / Part 11 assessment: <system or feature>
**Scope:** <GxP area, records, e-signatures yes/no, US/EU, hosting>
**Part 11 applies:** Yes / No / Partly, because <reason>
**GxP risk:** High / Medium / Low, because <reason>
**Summary:** <x> met · <y> partial · <z> gaps · <n> unknown. Top risks: <1–3>

## Findings
| Ref | Requirement | Status | Evidence | Fix (testable requirement) | Priority |
|---|---|---|---|---|---|
| 11.10(e) | Audit trail | Gap | No history kept on record edits | "The system shall record user, timestamp (UTC), old value, new value and reason for every create/update/delete of a <record>; audit entries cannot be edited or deleted by any role." | High |

## AI-specific findings (if applicable)

## Recommended validation approach
<proportionate plan>

## Open questions for Quality / Regulatory
- …

_This is a structured self-assessment, not a legal opinion or formal validation. Final decisions rest with the organization's Quality Assurance unit._
```

Write every fix as a requirement that a tester could verify ("The system shall…"), so it can drop straight into a PRD, user story or URS.
