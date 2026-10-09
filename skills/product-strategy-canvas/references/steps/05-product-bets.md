# 05 · Product Bets

**Stage:** Synthesize · **Updates:** `bets`

## Purpose

Turn the chosen opportunities into a small set of bets: testable hypotheses with a success metric, a kill rule and an appetite (how much we will spend before deciding).

## Inputs

- Priority opportunities
- Choices
- KPIs (create input KPIs as needed)

## Steps

1. Write 2–5 bets (`B#`). Each: "If we [do X] for [segment], then [measurable change], because [evidence]".
2. Link each bet to its opportunities.
3. Set the success metric (a KPI ID) and a target.
4. Set kill criteria in advance: the result that would stop the bet.
5. Set the appetite (time or money) and an honest confidence (0–1) based on evidence strength.
6. Use `assets/templates/bet-card.md` for the narrative version.

## Check before moving on

- [ ] Every bet has metric, kill rule, appetite.
- [ ] Confidence matches evidence strength.
- [ ] Bets are distinct, not variations of one idea.
- [ ] `python scripts/canvas_check.py canvas-output/canvas.json` has no errors

## Common mistake

- Bets that cannot fail. If no result would kill it, it is a commitment, not a bet.
