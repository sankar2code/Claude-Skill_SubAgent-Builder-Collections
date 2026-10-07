# Pharma & Clinical pack

Three Claude skills for product, data and clinical-operations teams in life sciences. They come from my work on regulated systems and clinical-trial products, and use only public data and published frameworks.

| Skill | Use it when | Output |
|---|---|---|
| `trial-failure-investigator` | You have an NCT ID for a terminated, withdrawn or suspended trial and want to know why it stopped | Ranked hypotheses across a 7-category taxonomy, every claim labeled fact / inference / hypothesis, with counter-arguments and sources |
| `gxp-part11-checker` | You're designing or reviewing a system, feature or AI tool for a GxP process | Requirement-by-requirement gap assessment against 21 CFR Part 11, EU Annex 11 and ALCOA+, with fixes written as testable requirements |
| `clinical-ai-evaluation-design` | You need to evaluate a clinical AI model, or a deployed model is drifting or showing bias | Governance action, escalation pathway, study design, estimand and causal methods, based on Fosset et al. (PLOS Digital Health, 2026) |

## Examples

- *"Why was NCT01234567 terminated?"* → `trial-failure-investigator` runs `scripts/fetch_trial.py` against ClinicalTrials.gov and PubMed, then reasons from the evidence packet only.
- *"Review this PRD for an AI-assisted adverse-event intake tool for Part 11."* → `gxp-part11-checker`.
- *"Our sepsis model's calibration dropped for patients over 75. What now?"* → `clinical-ai-evaluation-design`.

## Notes

- `fetch_trial.py` uses only the Python standard library and the public ClinicalTrials.gov v2 and NCBI E-utilities APIs. If your network blocks them, save the record from the website and run it with `--file`.
- These skills support expert work. They are not legal, regulatory or medical advice, and they don't replace your Quality, Regulatory, biostatistics or clinical governance teams.
