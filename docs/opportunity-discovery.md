# Opportunity Discovery pack

One Claude skill that finds business opportunities worth pursuing and tests them, instead of producing long idea lists. It looks at one business through five lenses, keeps only the opportunities that several lenses support, and ends with a clear call: Explore, Validate, Pause or Reject. It works in claude.ai, Claude Cowork and Claude Code.

```
 Customer ─┐
 Offer ────┤
 Capabilities & Assets ─┼──► Convergence matrix ──► Business Opportunity Map ──► Decision tree
 Market ───┤                 (evidence-weighted)       (one page + heatmap)        │
 Strategic Choice ─┘                                                             ▼
                                         Validate → strategy-sprint · Explore → interview guide → user-research
```

| Piece | What it does |
|---|---|
| [`opportunity-finder`](../skills/opportunity-finder/SKILL.md) | Business profile, route by starting point, 21 methods, synthesis into a Business Opportunity Map, challenge, decision and handoff |

## What an opportunity has to show

1. **Problem:** an outcome that matters to a specific customer and is poorly served
2. **Customers act:** evidence they will switch and pay
3. **Why now:** a recent change that makes it possible or necessary
4. **Value capture:** a business model that works
5. **Advantage:** something this business has that others do not

## Routes

| Starting point | Methods |
|---|---|
| Customers have a problem | JTBD → ODI → Demand-Side Forces → Value Proposition → Why Now → Opportunity Solution Tree |
| We have a capability or asset | VRIO → Core Competence → Asset Recombination → Productization → JTBD → Ansoff |
| The market is shifting | Why Now → PESTLE → Five Forces → Strategic Groups → Blue Ocean → Three Horizons |
| We have an idea to test | JTBD → Demand-Side Forces → Business Model Canvas → VRIO → Five Forces |
| Service business | Productization → Offer Ladder → Value Proposition → Demand-Side Forces → Business Model Canvas |

Every route ends with synthesis and the Opportunity Decision Tree.

## The 21 methods

| Customer | Offer | Capabilities & Assets | Market | Strategic Choice |
|---|---|---|---|---|
| Jobs-to-be-Done | Value Proposition Canvas | VRIO | Why Now / Technology Shift ★ | Ansoff Growth Matrix |
| ODI Opportunity Map | Business Model Canvas | Value Chain Opportunity Map | PESTLE Opportunity Map | Three Horizons |
| Customer Journey Map | Offer Ladder | Core Competence | Five Forces | Opportunity Solution Tree |
| Demand-Side Forces | Productization Matrix | Asset Recombination | Strategic Group Map | Opportunity Decision Tree |
| | | | Blue Ocean Canvas | |

★ New method: what changed in technology (including AI), cost, regulation or behavior to open this now, and how long the window lasts.

## What makes it trustworthy

- **Evidence labels.** Every claim is Fact, Estimate, Inference, Hypothesis or Unknown, with source IDs. Brainstormed ideas are always Hypothesis.
- **Weighted by evidence.** In the convergence matrix, an assumed signal counts 15% of a strong one, so ten guesses cannot outvote two facts.
- **Correct ODI math.** Opportunity = importance + max(importance − satisfaction, 0), from real survey data, with sample sizes flagged.
- **Visuals from scripts.** Strategy canvas, strategic group map and the opportunity heatmap are drawn by scripts, not described in words.
- **Sized before decided.** Top candidates go through `opportunity-sizing` before the decision tree.
- **Challenged cold.** The `strategy-red-team` sub-agent attacks the leading candidate without seeing the reasoning behind it.

## Scripts (Python 3, standard library only)

| Script | Output |
|---|---|
| `odi_score.py` | Opportunity scores by segment from a survey CSV, with bands and sample-size flags |
| `value_curve.py` | Blue Ocean strategy canvas (SVG) with eliminate / reduce / raise / create labels and a divergence check |
| `strategic_groups.py` | Strategic group map (SVG) with open positions |
| `convergence.py` | Business Opportunity Map: ranked markdown and a one-page HTML heatmap |

## How it connects to the rest of the kit

```
user-research ──► opportunity-finder ◄── market-research
                        │
                        ├─► opportunity-sizing (size the top candidates)
                        ├─► strategy-red-team (challenge)
                        └─► strategy-sprint (Validate) ─► prd-writer ─► backlog-builder
```

## Install

- **Claude Code, whole kit:** `/plugin marketplace add sankar2code/Claude-Skill_SubAgent-Builder-Collections`, then `/plugin install pm-builder-kit@sankar2code`.
- **Claude Code, just this skill:** copy `skills/opportunity-finder/` to `~/.claude/skills/`.
- **claude.ai or Cowork:** zip the `opportunity-finder` folder and upload it in Skills settings.

A complete fictional run is in [`skills/opportunity-finder/examples/`](../skills/opportunity-finder/examples/worked-example.md).

## Credits

The methods are established frameworks rewritten as working procedures. Their originators:

- **Jobs-to-be-Done:** Clayton Christensen and Bob Moesta
- **Outcome-Driven Innovation:** Tony Ulwick
- **Value Proposition Canvas and Business Model Canvas:** Alexander Osterwalder and Yves Pigneur
- **VRIO:** Jay Barney
- **Value Chain and Five Forces:** Michael Porter
- **Core Competence:** C.K. Prahalad and Gary Hamel
- **Blue Ocean Strategy:** W. Chan Kim and Renée Mauborgne
- **Ansoff Matrix:** Igor Ansoff
- **Three Horizons:** Baghai, Coley and White
- **Opportunity Solution Tree:** Teresa Torres
- **Forces of Progress:** Bob Moesta and Chris Spiek

The five-lens structure is inspired by public opportunity-discovery playbooks.
