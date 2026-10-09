# Product Strategy Canvas pack

One Claude skill that turns product evidence into a **connected, visual strategy**: evidence → customer needs → opportunities → product bets → a prioritized Now / Next / Later roadmap → KPIs. Everything lives in one `canvas.json` with linked IDs, so any roadmap item can be traced back to the evidence behind it. Scripts draw the visuals. Works in claude.ai, Claude Cowork and Claude Code.

```
 S source → E evidence → N need → O opportunity → B bet → I initiative → K KPI
                                      ↑                 ↓
                                   G goal        success metric · kill rule · appetite
```

| Piece | What it does |
|---|---|
| [`product-strategy-canvas`](../skills/product-strategy-canvas/SKILL.md) | 12 steps from evidence to bet scorecard, one data file, five scripts, interactive canvas and SVG visuals, exports to backlog, PRDs and a deck brief |

## What you get

| Visual | From |
|---|---|
| Interactive canvas: click any card to light up its chain from evidence to KPI | `render_canvas.py` → `canvas.html` |
| Opportunity tree: goal → opportunities → bets → initiatives | `opportunity-tree.svg` |
| Prioritization matrix: value vs effort, bubble = reach, colour = confidence | `priority-matrix.svg` |
| Outcome roadmap: Now / Next / Later, grouped by bet and KPI | `roadmap.svg` |
| Dependency graph with critical path and slack | `dependencies.svg` |
| KPI tree: north star, inputs, guardrails, baselines and targets | `kpi-tree.svg` |

## Three modes

| Mode | Use when |
|---|---|
| **Quick** | You already have research and a roadmap and need one connected page fast |
| **Full** | Building or resetting strategy for a product area |
| **Review** | Bets have shipped: score them and write what you learned back into the canvas |

## The 12 steps

| Diagnose | Analyze | Synthesize | Decide | Execute | Measure |
|---|---|---|---|---|---|
| 01 Evidence intake | 03 Opportunity tree | 05 Product bets | 07 Portfolio balance | 09 Dependency map | 10 KPI tree |
| 02 Needs map | 04 Strategic choices | 06 Prioritization | 08 Outcome roadmap | | 12 Bet scorecard |
| | | | 11 Decision brief | | |

## What makes it trustworthy

- **Traceability.** `canvas_check.py` flags:
  - broken links
  - orphan initiatives
  - top needs with no opportunity
  - bets without a success metric or kill rule
  - KPIs without baselines

  `--why I3` answers "why is this on the roadmap?"
- **Honest prioritization.** RICE, ICE or WSJF, with a stability test over 1,000 runs. Low-confidence leaders and items ranked above their dependencies are flagged.
- **Bets that can fail.** Every bet states its kill rule and appetite before starting. The scorecard compares results with those rules, not with whichever metric looks best afterwards.
- **Same evidence labels** as the Strategy and Opportunity Discovery packs.

## Scripts (Python 3, standard library only)

| Script | Does |
|---|---|
| `canvas_check.py` | Traceability, gaps, evidence strength per bet, `--why` trace |
| `prioritize.py` | RICE / ICE / WSJF, stability, dependency-aware flags, `--write` ranks |
| `dependencies.py` | Cycles, critical path, slack, hotspots, SVG |
| `render_canvas.py` | Interactive canvas page and five SVGs |
| `export.py` | `backlog.csv` (Jira/Linear), `prd-inputs/B#.md`, `deck-brief.md` |

## How it connects to the rest of the kit

```
user-research ─┐
opportunity-finder ─┼─► product-strategy-canvas ─┬─► backlog-builder (stories)
strategy-sprint ────┘                            ├─► prd-writer (one PRD per bet)
                                                 ├─► experiment-design (pilots)
                                                 └─► insight-storyteller (readout)
```

## Install

- **Claude Code, whole kit:** `/plugin marketplace add sankar2code/Claude-Skill_SubAgent-Builder-Collections`, then `/plugin install pm-builder-kit@sankar2code`.
- **Claude Code, just this skill:** copy `skills/product-strategy-canvas/` to `~/.claude/skills/`.
- **claude.ai or Cowork:** zip the `product-strategy-canvas` folder and upload it in Skills settings.

A full fictional run, with every rendered output, is in [`skills/product-strategy-canvas/examples/`](../skills/product-strategy-canvas/examples/worked-example.md).

## Credits

- **Opportunity Solution Tree:** Teresa Torres
- **RICE:** Intercom
- **ICE:** Sean Ellis
- **WSJF:** Don Reinertsen; SAFe
- **Outcome-based roadmaps:** Josh Seiden and Jeff Gothelf
- **Now / Next / Later:** Janna Bastow
- **North Star framework:** Amplitude
- **Outcome-Driven Innovation:** Tony Ulwick

The evidence-to-outcome canvas idea is inspired by public product-strategy playbooks.
