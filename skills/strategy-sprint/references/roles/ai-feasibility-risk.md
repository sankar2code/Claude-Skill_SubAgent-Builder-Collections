# AI Feasibility & Risk

**Stage:** Analyze · **Role 09 of 24** · **Output:** `strategy-output/09-ai-feasibility-risk.md`

## Job

Test whether an AI capability behind an option is feasible, measurable and safe to ship: data, model approach, evaluation, guardrails, cost and failure modes.

## Use when

- Any option depends on an AI or ML capability working well enough.
- The team is assuming model quality without evidence.

## Skip when

- No option depends on AI.

## Needs (named, versioned inputs)

- Option descriptions
- Data inventory and access status
- Any prototype or eval results
- Regulatory context (from regulatory-screen if run)

## Method

1. Define the task precisely: input, output, who acts on it, and the cost of a wrong answer.
2. Data readiness: availability, volume, quality, labels, rights to use, privacy constraints.
3. Approach options: rules, retrieval, fine-tuning, off-the-shelf model, human-in-the-loop. Note what must stay deterministic.
4. Evaluation plan: success metric and threshold, test set, failure categories, human review rate. Thresholds are set now, not after results.
5. Guardrails: what the model may not do, escalation path, monitoring, rollback.
6. Cost and latency per transaction as a range; vendor and lock-in risk.
7. Verdict per option: feasible now / feasible with conditions / not yet, with the evidence behind it.

## Output sections

- Task definition and error cost
- Data readiness table
- Approach options
- Eval plan with thresholds
- Guardrails and monitoring
- Unit cost range
- Feasibility verdict per option
- Handoff block (`assets/templates/handoff.md`)

## Checks before handoff

- [ ] Quality claims are backed by evals or labeled `[HYPOTHESIS]`.
- [ ] High-risk failure modes have a guardrail or are flagged.
- [ ] Every material claim labeled per `references/operating-rules.md`

## Stop and escalate if

- The use case touches patient safety or regulated decisions without a regulatory screen.
- Data rights are unclear.
- Any action outside the read-only default is needed.

## Related kit skills

`clinical-ai-evaluation-design` for clinical AI; the `ai-eval-builder` sub-agent to build the eval suite.

## Hands to

strategic-options-grid, build-buy-partner, business-case-builder or pilot-experiment-designer.
