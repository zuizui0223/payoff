# PAYOFF-B Scottish observed food mass: *temporal-phase specificity* falsification (2026-11-16)

**Status:** strict frozen exploratory gate **HOLD_PHASE_SPECIFICITY_NOT_ESTABLISHED**. Source and full-year/site CV verified with GitHub Actions run https://github.com/zuizui0223/payoff/actions/runs/43888766365 ; four synthetic contract tests passed. This is an original-data exploratory reanalysis after the count+mass fledging (PR #390) and first-visit body-mass (PR #391) outcomes were opened, **not** prospective independent confirmatory evidence.

## Why the hypothesis was tested

PR #390 had found an apparent predictive improvement when source-measured caterpillar **mass g per standardized branch beating** was added to a seasonal count model of blue-tit fledged/clutch. This could arise either from (a) having more prey production generally, or (b) the prey mass occurring at the *right hatch-relative phase*. The information×irreversibility×recourse PAYOFF-B hypothesis requires a true temporal interaction component. A phase-specific effect should add prediction after controlling overall seasonal food amount, not only beat a count-only baseline.

## Source and full-support gate

Original UKCEH EIDC DOI:10.5285/b63d53ae-2fe7-4ce9-82a2-2325098489e3, exact source CSV content SHA256 verified by the imports, preserving the 2018–2021 measurement-era cohort: **138 independent site-years, 427 verified unmanipulated blue-tit nests, 44 sites and 4 calendar years**. No source sample drift. Source mass dates per site-year ranged **11 to 26 (median 22)** after the mass-coverage gate. Positive-count unweighed mass was missing, not zero; original `<0.02` mass was bounded [0, 0.02] grams. Original branch beating was a standardized 30-hit sampling unit; this cannot be translated to g/m² or consumed prey. Every hatch-to-hatch+13 day temporal predictor still required full originally observed/interpolated support and no >8-day source gaps.

**Seasonal abundance control** is the arithmetic mean of mass per beating on observed field-sampling dates (NOT an annual production integral, a daily season-weighted mean, or any independently monitored food intake). Both lower and upper censor bounds included. All eight models use the same source site-year and nest set, train-only predictor standardization, and fixed ridge penalty=1.

## Models and outcomes

- A = year + spatial/site climate + mean hatch and clutch + observed seasonal peak *count* and signed peak–hatch difference.
- B = A + hatch-window *count* per standardized beating.
- H0/H1 = B + observed hatch-window *mass g/beat*, lower/upper censor bounds.
- S0/S1 = B + observed sampled-season **mean mass g/beat**, lower/upper bounds.
- HS0/HS1 = B + season mean **and** hatch-window mass, lower/upper bounds.

### Mean squared error, held-out years and held-out sites (squared fledged/clutch fraction)

| Model | LOYO equal-year MSE | LOSO equal-site MSE |
|---|---:|---:|
| A | 0.051477 | 0.047927 |
| B | 0.054442 | 0.049263 |
| H lower/upper | 0.048473 / 0.048521 | 0.044941 / 0.044957 |
| **S lower/upper** | **0.047563 / 0.048160** | **0.044652 / 0.044896** |
| HS lower/upper | 0.048903 / 0.049212 | 0.044785 / 0.044931 |

Both **H vs S** and incremental **HS vs S** are unfavorable to a unique hatch-window effect in **both** held-out validation directions and both censor bounds. Specifically, `MSE(S)-MSE(HS)` = **−0.001340/−0.001052** LOYO and **−0.000132/−0.000034** LOSO. These are squared outcome fractions, not regression slopes or causal effect sizes.

In four individual LOYO year folds, the incremental HS vs S improvement for both censor bounds was positive in 2018, 2020, 2021, but negative in 2019 (−0.005833/−0.004973). The strict frozen gate required positive *overall* year- and site-heldout performance and >0 across both bounds in at least 3/4 years; thus the gate failed despite 3/4 positive folds. The unbalanced between-year signal cannot be spun as support.

### COVID sampling sensitivity prelisted

Removing 2020 still gave **HOLD**. `MSE(S)-MSE(HS)` = −0.002596/−0.002280 (LOYO), −0.000082/+0.000017 (LOSO): no consistent conditional temporal improvement.

## Prior-art novelty boundary and interpretation

Existing research already links prey seasonality, food availability, and bird reproductive outcomes. In particular, Macphie et al. 2026 preprint `10.32942/X27Q35` studies maximum abundance and duration of a seasonal resource vs blue-tit reproduction. Thus no discovery claim for "biomass predicts fitness" or "prey peak overlaps nestling demand" is warranted.

**Retained ecological reading:** source-measured caterpillar mass may encode information beyond counts in a site-year fledging model, but the current matched negative control suggests its incremental predictive signal need not be **specific to nestling demand timing**. A stronger mechanism claim is explicitly **not supported**. Measured resource availability is upstream of parental decisions, actual prey selection, food delivery, the nestlings' energetic state, survival/competition, and multi-species interactions. None of those mediators was identified from this Scottish observational panel. The Scottish first-visit nestling body-mass endpoint was previously null (PR #391), leaving the trophic conversion mechanism unresolved.

## Next source admissibility criterion: actual interspecific contacts

To connect PAYOFF-B information×commitment×recourse theory to empirical payoff rather than descriptive resource quantity, future data must contain **time-stamped actual encounters/provisioning or pollinator visit events** and outcome/fitness, with independent pre-decision environmental cues and documented downstream behavioral adjustment. A distant-cue prediction/route correction study would test information vs recourse; resident blue-tit nest provisioning records alone cannot measure migratory information deficit. Do not optimize the same Scottish resource windows after this negative result, or reuse source overlapping papers as independent replication.

**Source and code:** `scripts/payoff_b_scotland_mass_phase_specificity.py`, `tests/test_payoff_b_scotland_mass_phase_specificity.py`, `docs/PAYOFF_B_SCOTLAND_MASS_PHASE_SPECIFICITY_FREEZE_20261116.md`. No change to previous PR #390 or #391 outcomes.
