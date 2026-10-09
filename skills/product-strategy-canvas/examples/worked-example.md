# Worked example: from prior-auth research to a connected roadmap

> **Fictional company, illustrative data.** Helio Health continues from the Opportunity Discovery and Strategy pack examples: discovery found AI prior authorization, and the strategy sprint chose "partner now, pilot with kill criteria". This run turns that decision into product bets, a roadmap and KPIs. Every file in `sample-output/` was produced by the scripts from `sample-output/canvas.json`.

## Step 0: Mode

Mode: **Full**. Opportunity Finder outputs already exist, so evidence, needs and opportunities were imported, not rebuilt. Prioritization method: RICE (adoption-driven work).

## 01–02: Evidence and needs

7 evidence items from 5 sources. For example, E1: "9 of 12 interviewees re-type patient data into payer portals" `[FACT S1 · strong]`. E6 (pricing intent from 6 clinics) is `weak` and stays out of the needs. The checker later flags it as unused, which is correct: it belongs to the business case, not to a customer need.

Four needs were written as outcomes. N4, "Trust that nothing is submitted without review", has importance 7. It has no opportunity of its own; it is handled through choice C2 instead.

## 03–04: Opportunity tree and choices

Goal G1, "Clinics get payer decisions faster", is measured by K1, median days to payer decision.

| Opportunity | Needs |
|---|---|
| O1: requests are slow because data is re-typed and incomplete | N1, N2 |
| O2: clinics cannot see where a request is stuck | N1 |
| O3: denials come from missing documentation | N3 |

The two strategic choices:

| Choice | We will | We won't | Why |
|---|---|---|---|
| C1 | Pre-fill requests from schedule data | Build our own payer network | Our data is the advantage; networks are commodity |
| C2 | Keep a human approval step | Auto-submit in year one | Anxiety is the strongest force against switching (E7) |

## 05: Bets

| Bet | Success metric | Kill rule | Confidence |
|---|---|---|---|
| B1 Auto-filled requests | K2 staff minutes per request, −50% | field accuracy < 95% after 500 requests | 0.6 |
| B2 Live status tracker | K3 status tickets per 100 requests, 14 → 6 | < 30% weekly use | 0.8 |
| B3 Denial-risk check | K4 denial rate, −25% | no change after a quarter | 0.4 |

## 06: Prioritization (`prioritize-output.txt`)

```
1  I4  Status tracker in the schedule view   120.0  100%  needs I1 first
2  I3  Human review queue                     96.0   98%  needs I2 first
3  I1  Payer API integration (top 5 payers)   64.0   78%
4  I2  Field extraction and pre-fill          45.0   24%
```

The flags matter more than the scores:
- The two highest scorers both depend on lower-ranked work. Building I4 and I3 first is impossible.
- I1 is on the critical path, so it moves to the front despite ranking third.
- I5 (denial-risk check) scored low, partly because its confidence is 0.4. That points to validating B3 first, not dropping it.

## 07–09: Balance, roadmap, dependencies

- **Balance:** 18 weeks of appetite against about 20 weeks of capacity. No transformational bet, by choice.
- **Roadmap:** Now holds I1–I4; Next holds I5; Later holds I6.
- **Dependencies** (`dependencies-output.txt`): the critical path is I1 → I2 → I5, 20 weeks. I1 and I2 are coordination hotspots, because each blocks two or more items.

## 10: KPI tree

- **North star:** K1, median days to payer decision.
- **Inputs:** K2–K4 and K6.
- **Guardrail:** K5, submissions corrected after review, < 5%.

Two baselines are `[UNKNOWN]`, so measuring them was added to the Now column.

## Check, trace, render

`canvas_check.py`: PASS WITH WARNINGS (two missing baselines, two unused evidence items, one need deliberately not addressed).

`canvas_check.py --why I5` traces the chain I5 → B3 → O3 → N3 → E3 → S2, with the success metric K4 and the kill rule.

`render_canvas.py` produced `canvas.html` and five SVGs. Clicking I5 on the canvas lights up E3, N3, O3, B3 and K4.

## 11: Export

`export.py` produced:
- `backlog.csv`: 3 epics and 6 stories, refined next with `backlog-builder`
- `prd-inputs/B1–B3.md`: one PRD starter per bet, for `prd-writer`
- `deck-brief.md`: the spine for the leadership readout

## 12: Scorecard (later)

After the pilot, B2's status tickets fell from 14 to 7 per 100 requests `[FACT]`. That missed the target of 6, but it was far from the kill rule. Decision: **scale**, with the note that the remaining tickets are about denials, which strengthens the case for B3. The learning was added back to the canvas as new evidence.
