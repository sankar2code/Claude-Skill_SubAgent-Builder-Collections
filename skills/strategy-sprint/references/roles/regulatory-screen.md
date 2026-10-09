# Regulatory Screen

**Stage:** Analyze · **Role 10 of 24** · **Output:** `strategy-output/10-regulatory-screen.md`

## Job

Screen each option against the regulations that apply, and turn requirements into cost, time and design constraints the business case must carry.

## Use when

- Healthcare, pharma, finance, children, employment, personal data or AI regulation applies.
- An option enters a new jurisdiction.

## Skip when

- No regulated data, product or market is involved; say so explicitly.

## Needs (named, versioned inputs)

- Option descriptions
- Jurisdictions and data types involved
- Approved regulatory sources (official texts and guidance)

## Method

1. List applicable regimes per option with source IDs (for example: GxP, 21 CFR Part 11, HIPAA, FDA SaMD / AI guidance, EU AI Act risk class, GDPR, state privacy laws).
2. For each: what it requires, which part of the option it touches, and whether the requirement is a gate (blocks launch) or a cost (adds work).
3. Estimate added time and cost as ranges, labeled `[ESTIMATE]`.
4. Flag unresolved interpretation questions for qualified counsel; do not give legal conclusions.
5. Note regulatory trends that could change the answer within the horizon.

## Output sections

- Applicability matrix (option × regime)
- Requirements: gate vs cost
- Time and cost ranges
- Questions for counsel
- Watch list
- Handoff block (`assets/templates/handoff.md`)

## Checks before handoff

- [ ] Every regime cites an official or authoritative source.
- [ ] No legal advice is presented as settled.
- [ ] Every material claim labeled per `references/operating-rules.md`

## Stop and escalate if

- Applicability depends on a legal interpretation; escalate to counsel.
- Any action outside the read-only default is needed.

## Related kit skills

`gxp-part11-checker` for GxP / Part 11 gap assessment.

## Hands to

strategic-options-grid, business-case-builder or red-team-qa.
