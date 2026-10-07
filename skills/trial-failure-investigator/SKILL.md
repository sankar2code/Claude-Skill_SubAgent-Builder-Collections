---
name: trial-failure-investigator
description: >
  Investigates why a clinical trial was terminated, withdrawn, or suspended, starting
  from its NCT ID. Pulls the registry record from ClinicalTrials.gov and linked PubMed
  abstracts, then produces ranked, source-backed hypotheses across a 7-category failure
  taxonomy, with every claim labeled as fact, inference, or hypothesis and every
  hypothesis paired with its strongest counter-argument. Use this skill when the user
  shares an NCT number, asks "why did this trial fail/stop/terminate", "what happened to
  trial X", "analyze this terminated study", or wants lessons learned for trial design
  or feasibility. Part of the Pharma & Clinical pack.
---

> **Pharma & Clinical pack.** Based on my ClinicalAI Trial Failure Investigator app. Uses only public registry and literature data.

# Trial Failure Investigator

Registries rarely say plainly why a trial stopped. The `whyStopped` field is often blank or a few vague words. Your job is to assemble the public evidence, reason from it carefully, and be honest about how much it can and can't support.

## Step 1 — Get the evidence

Validate the ID first: an NCT ID is `NCT` followed by 8 digits.

**If you can run code with internet access**, use `scripts/fetch_trial.py` (in this skill's folder). It uses only the Python standard library:

```bash
python scripts/fetch_trial.py NCT01234567              # fetch live and print an evidence packet
python scripts/fetch_trial.py NCT01234567 --json out.json
python scripts/fetch_trial.py --file saved_record.json  # parse a record saved from the API
```

It calls the public ClinicalTrials.gov API v2 (`https://clinicaltrials.gov/api/v2/studies/<NCT ID>`) and PubMed E-utilities (references linked in the record, plus a search for the NCT ID), and prints a structured packet.

**If you can't run code**, fetch `https://clinicaltrials.gov/study/<NCT ID>` with a web tool, or ask the user to paste the record. Work only from what you actually retrieved.

The evidence packet should include: title, status, `whyStopped`, phase, conditions, sponsor and sponsor class (industry, NIH, other), start / primary completion / completion dates, enrollment (after a stop this is usually the actual number; the original target is often only in the record's version history on ClinicalTrials.gov), number of sites and countries, eligibility basics, whether results are posted, outcome measures and adverse-event summary (if results exist), and linked publications.

If the trial is **not** terminated, withdrawn, or suspended, say so and ask whether the user still wants an analysis (for example, of a completed trial that missed its endpoint).

## Step 2 — Read the signals

Note what each piece of evidence suggests, for example:

- **Status:** *withdrawn* means it stopped before enrolling anyone; *terminated* means it stopped after enrolling; *suspended* means paused and may resume.
- **Enrollment:** actual far below the original target (check the record's history tab for the earlier estimated number), especially after a long recruitment window, points toward recruitment problems. If you can't find the target, say so rather than guessing it.
- **Timing:** stopping right after a planned interim analysis points toward futility, efficacy or safety findings.
- **Sponsor patterns:** many trials from the same sponsor stopping around the same date suggests a portfolio or business decision.
- **Results and adverse events:** posted results with a missed primary endpoint, or an imbalance in serious adverse events.
- **Publications:** a paper or conference abstract that explains the stop.

## Step 3 — Build hypotheses against the taxonomy

Classify each hypothesis into one or more of these categories (they are not mutually exclusive):

| Category | Meaning |
|---|---|
| Recruitment shortfall | Enrollment fell short of target, or accrual was too slow to sustain the trial |
| Efficacy miss | The primary or key secondary endpoint was not met |
| Safety / toxicity | Adverse events, a data monitoring committee stop, or another safety signal |
| Funding / business decision | Funding withdrawn, or a business decision unrelated to trial performance |
| Operational / protocol issues | Site problems, drug supply, protocol deviations or amendments |
| Strategic / competitive | A competing therapy, a portfolio reprioritization, or a shifting standard of care |
| Futility | An interim analysis showed the trial was unlikely to reach a meaningful result |

Produce 2–4 hypotheses, ranked by how well the evidence supports them.

## Step 4 — Apply the labeling contract (non-negotiable)

Tag every claim with exactly one label:

- **[fact]**: directly stated in the evidence (an enrollment number, the literal `whyStopped` text, a date).
- **[inference]**: a reasonable, evidence-grounded reading of the facts ("a shortfall this large very likely contributed").
- **[hypothesis]**: plausible given the pattern but not directly evidenced ("a competing trial may have affected recruitment", with no competing trial named in the evidence).

Never present a hypothesis as a fact. Reason only from the evidence packet, not from general knowledge about the sponsor, drug or disease. If you mention outside context, label it and keep it separate. When the evidence is insufficient, say so plainly instead of inventing an explanation.

## Step 5 — Counter-arguments and confidence

For each hypothesis, give its **strongest counter-argument**: the best case against it, not a token objection. If you can't build a real counter-argument, the hypothesis is probably under-evidenced; lower its confidence.

Rate each hypothesis **High / Medium / Low** confidence:
- **High:** the registry or a publication states the reason, or several independent facts point the same way.
- **Medium:** facts support it, but other explanations remain plausible.
- **Low:** pattern-based only.

## Output: investigation report

```markdown
# Why did <NCT ID> stop? <short title>
**Status:** <Terminated/Withdrawn/Suspended> · **Phase:** <…> · **Sponsor:** <name (class)>
**Registry reason (whyStopped):** "<verbatim text>" or "Not provided"
**Bottom line:** <1–2 sentences, with the overall confidence>

## Key evidence
- [fact] Enrollment: <actual> of <target> (<%>), <start> → <stop>
- [fact] …

## Ranked hypotheses
### 1. <Category>: <one-line hypothesis> · Confidence: <High/Med/Low>
- Support: [fact] … · [inference] …
- Strongest counter-argument: …

### 2. …

## What the evidence can't tell us
- <gaps, and where the answer might be found: sponsor press releases, SEC filings, conference abstracts>

## Lessons for future trials
- <1–3 design or feasibility lessons, labeled as inferences>

## Sources
- ClinicalTrials.gov record: https://clinicaltrials.gov/study/<NCT ID>
- PubMed: <links>
```

## Guardrails

- This is an evidence review of public information, not a regulatory or legal determination. Say so if the user may rely on it for decisions.
- Don't speculate about named individuals.
- Quote `whyStopped` text exactly as written.
