# PAYOFF-B BTBW annual dataset: pre-analysis contrast lock
2026-10-10 | source-verified, numerical outcomes not yet computed in PAYOFF-B

## Source and population
Lany et al. Oikos 2016 (online 2015), https://doi.org/10.1111/oik.02412, Dryad https://doi.org/10.5061/dryad.g1m27. Independently retrievable same-name open CSV from hurlbertlab/caterpillars-count-analysis at `data/birds/BTBW_data_Dryad.csv`; check exact raw-byte SHA256 on import. Original Dryad archive is primary DOI. 25 annual summaries, 1986–2010, black-throated blue warbler at Hubbard Brook. Not individually resolved.

## Before any new outcome regression: fixed endpoints and competing accounts
(A) **Descriptive timing contrast (primary temporal axis):** regress annual median first-clutch initiation `clutch.init.50` on `Acsa.canopy` by ordinary least squares; report slope, intercept, standard error, HC3 95% CI, and exact n. Evaluate H0 slope=1 as a **reference of 1:1 timing shifts**, not an evolutionary null. Secondary leaf cue: `Acsa.budburst`. For 1989+ separately regress median male `arrival.50` and postarrival interval `clutch.init.50 - arrival.50` on canopy to expose stage-specific buffering. The latter shares clutch mathematically and is not behavioural causality.

(B) **Annual fitness association, not optima/selection:** target `mean.fledged` (mean young fledged per pair/year); calendar phenological lag `lag = clutch.init.50 - Acsa.canopy`. Base model: intercept + standardized canopy + standardized `ln.mean.cats` + standardized `density` + standardized `prop.F.ASY`. Added-lag model: base + standardized lag. Report lag coefficient with HC3 interval, *partial association only*. Do not call significance support for mismatch causing fitness change. Additional rival model: base + standardized `survival` (daily nest survival, predation-linked fitness component); full model includes lag and survival. Compare improvements in fixed 2000–2010 held-out mean-square forecast loss from training 1986–1999, with standardization trained ONLY on 1986–1999. Report leave-one-year-out lag coefficient sign range for sensitivity, not p-value as causal proof. No forward selection.

(C) **Do not infer a fitness optimum from annual aggregates.** If only one phenological median and one mean fledged value exist per year, timing-specific counterfactual reproductive success is not identifiable, even if annual `mean.fledged` is observed. `Regret`, individual informed strategy, and feasible adjustment limit remain NOT_IDENTIFIED. No parabola optimum or post-hoc "optimal mismatch" inference.

## Data quality
Require exactly 25 unique integral years 1986..2010; fields named exactly as Dryad; finite canopy, clutch, fledged, density, food, age proportions; allow missing arrival only if 1986–1988. Check `survival` in (0,1], `prop.F.ASY` in [0,1]; no row-shuffling or imputation. Log fixed. Unit level = year. Small-N and temporal dependence; HC3 uncertainty is only descriptive. Avoid pseudo-replication of species/pairs.

## Decision gates
- Timing response reproducible from the public rows; compare reference 0.56 ±0.08 to primary canopy and secondary budburst transparently, avoiding assumptions about original modelling transformations.
- Even a nonzero association in annual fledglings is not positive fitness regret or mechanistic information constraint. A breeding-date×fitness surface needs individual nests and baseline ecological covariates, interventions, or defensible identification.
- This reanalysis is a PRIOR-ART BENCHMARK for Paper 2, not independent confirmation, and does not change frozen PAYOFF-B V7R/V8 outcomes.

## Source provenance
Original landing page documents variable glossary and 25 years: https://datadryad.org/dataset/doi%3A10.5061/dryad.g1m27.
Mirror: https://github.com/hurlbertlab/caterpillars-count-analysis/blob/master/data/birds/BTBW_data_Dryad.csv (confirm actual branch/ref and git blob SHA on fetching). Re-archiving data is solely for transparent rerunning and must retain DOI attribution.
