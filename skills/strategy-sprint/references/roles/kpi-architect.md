# KPI Architect

**Stage:** Execute · **Role 20 of 24** · **Output:** `strategy-output/20-kpi-architect.md`

## Job

Link the strategic goal to leading and lagging metrics, value tracking, action thresholds, owners and stop / scale rules.

## Use when

- A roadmap exists but leaders lack early warning or benefit ownership.

## Skip when

- Quick mode; use the kill criteria table instead.

## Needs (named, versioned inputs)

- Approved option and roadmap
- Kill criteria
- Business case drivers

## Method

1. Build a KPI tree from the goal to 3–5 drivers to leading indicators (use `assets/templates/kpi-tree.md`).
2. For each KPI: definition, formula, data source, baseline, target range, review frequency, owner role.
3. Set action thresholds: green / amber / red, and what happens at each.
4. Add anti-gaming checks: a counter-metric for each target that can be gamed.
5. Map business-case drivers to KPIs so value realization can be tracked.

## Output sections

- KPI tree
- KPI definitions table
- Thresholds and actions
- Counter-metrics
- Value tracking map
- Handoff block (`assets/templates/handoff.md`)

## Checks before handoff

- [ ] Each KPI is measurable with available data or flagged.
- [ ] Kill criteria are included.
- [ ] Every material claim labeled per `references/operating-rules.md`

## Stop and escalate if

- Baseline data does not exist; propose how to create it.
- Any action outside the read-only default is needed.

## Hands to

pyramid-story-builder or decision-memo-writer.
