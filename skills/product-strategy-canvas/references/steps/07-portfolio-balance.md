# 07 · Portfolio Balance

**Stage:** Decide · **Updates:** `meta.balance`

## Purpose

Check that the set of bets is balanced: not all safe, not all moonshots, and within capacity.

## Inputs

- Bets with confidence and appetite
- Team capacity

## Steps

1. Classify each bet: core (improve what works), adjacent (new value for current customers), transformational (new customers or model).
2. Sum appetites against capacity. If over, cut, don't squeeze.
3. Check risk spread: if every bet has confidence below 0.5, add a safer one; if all are above 0.8, the team may be under-ambitious.
4. Check coverage: are top needs and segments all served by some bet?
5. Write a short balance note in the canvas meta (`meta.balance`).

## Check before moving on

- [ ] Total appetite fits capacity.
- [ ] Mix of core / adjacent / transformational stated.
- [ ] `python scripts/canvas_check.py canvas-output/canvas.json` has no errors

## Common mistake

- Calling everything core to avoid the conversation.

## Reuse from the kit

`three-horizons-map` in `opportunity-finder`; `portfolio-reviewer` role in `strategy-sprint`.
