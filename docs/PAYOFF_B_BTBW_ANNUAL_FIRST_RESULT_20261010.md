# PAYOFF-B BTBW annual source reanalysis: first outcome receipt

**Date:** 2026-10-10
**Status:** DESCRIPTIVE PRIOR-ART BENCHMARK ONLY
**Prospective protocol:** `docs/PAYOFF_B_BTBW_ANNUAL_PREANALYSIS_LOCK_20261010.md` committed **before** this PAYOFF-B outcome computation.
**Input:** the 25-row Lany et al. (2015/2016) Dryad annual CSV, reproduced byte-for-byte from a public third-party GitHub mirror; Git blob SHA `887fc0539d88e770a17da740dea960b45db899aa` at both source and PAYOFF-B paths. Original archival DOI: https://doi.org/10.5061/dryad.g1m27.
**Program:** `scripts/payoff_b_btbw_annual_reanalysis.py`.
**Unit:** year, NOT bird/individual. 1986–2010 = 25 years. Male arrival is unavailable in 1986–1988, so arrival analyses have 22 years.

## 1. Reproduce published timing response — without claiming novelty

The chosen prespecified leaf-out coordinate is `Acsa.canopy` (90% sugar-maple leaf expansion). Clutch initiation = median first-clutch date.

| Annual descriptive contrast | n | Slope, days/day | HC3 95% CI | Assessment |
|---|---:|---:|---|---|
| Clutch initiation vs canopy | 25 | **+0.5654** | +0.3649 to +0.7659 | Consistent with published +0.56 ± 0.08 (original SE vs this OLS SE 0.0852) |
| Clutch initiation vs budburst (alternative) | 25 | +0.4101 | +0.2177 to +0.6025 | Positive sensitivity |
| Male median arrival vs canopy | 22 | +0.1779 | -0.0311 to +0.3869 | No resolved positive direction at HC3 95% |
| Arrival-to-first-clutch interval vs canopy | 22 | **+0.3771** | +0.0986 to +0.6557 | Earlier springs associate with shorter postarrival interval |

Clutch-to-canopy lag across the 25 years averages **+7.28 days**; this is an offset to 90% canopy expansion, NOT a confirmed caterpillar-peak mismatch. The clutch-canopy response differs from a 1:1 timing slope (HC3 descriptive p against 1 = 0.000168). The stage contrasts are not randomization-based: the postarrival interval includes clutch and arrival by definition.

The original source already reported the sub-unity spring response, post-arrival adjustments, and an inference of fitness-optimal breeding timing. Those are **prior-art findings**, not new PAYOFF-B discoveries.

## 2. Can annual lag be called fitness loss? No.

Annual outcome `mean.fledged` is number of young fledged per pair/year. Fixed baseline covariates: canopy date, log seasonal caterpillar biomass, bird density and proportion of older females; standardize each predictor. Registered focal lag = first-clutch initiation minus canopy date, in days.

| Descriptive model | In-sample R² | Heldout MSE* |
|---|---:|---:|
| Baseline | 0.324 | 1.162 |
| Baseline + lag | 0.337 | 1.053 |
| Baseline + daily nest survival | 0.537 | 0.927 |
| Baseline + lag + survival | 0.549 | 0.828 |

*Fixed chronological split: training 1986–1999 (14 years), holdout 2000–2010 (11 years). Predictors such as seasonal food/nest survival can become known only after the breeding decision. These are **cross-year explanatory association scores, never prospective animal forecasts**. No causal ranking follows from MSE.

- Standardized lag partial coefficient in baseline+lag = **+0.2178 young/pair/year per 1 SD lag**, HC3 95% CI **-0.5102 to +0.9458** (p=0.539). This does not establish a negative lag cost, positive lag benefit, or optimal lag.
- After also conditioning on nest survival, lag coefficient = +0.2039, HC3 95% CI **-0.4267 to +0.8346**.
- Standardized daily nest-survival coefficient in baseline+survival = +0.4922, HC3 95% CI +0.1287 to +0.8556. Nest survival is mechanistically and arithmetically tied to fledging and measured after nests exist. **Not a causal effect and not a predecision cue**.
- Leave-one-year-out lag coefficients for baseline+lag range +0.1053 to +0.4465, but every HC3 focal lag confidence interval in the primary full fit includes zero. Stable point-estimate sign does not imply robust biological evidence.

The source contains one median timing and one annual reproductive mean per year, **not within-year individual timing-by-fitness profiles**. One cannot infer which alternative breeding date an individual would have chosen, its demographic payoff, or a feasible action set. A non-1:1 seasonal slope alone does not establish maladaptation; nor does a nonnegative annual lag association demonstrate optimality.

## 3. What is empirically identified

**IDENTIFIED descriptively**: incomplete clutch tracking; a post-arrival interval component that varies with canopy phenology; annual fledging associations with temporally realized resource, survival and lag variables.

**NOT IDENTIFIED**: ex-ante migratory information, learned cue calibration, individual reaction to a *new* forecast, cost of route/flight adjustment, causal reproductive fitness optimum, fitness regret, and biological information or coordination constraints.

## 4. Publication decision

- Include the source as an explicit **prior-art and cautionary ecological benchmark** in Paper 2, without presenting an annual regression as a PAYOFF-B mechanistic validation.
- This benchmark challenges the automatic inference `phenological gap -> adaptive failure`.
- A stand-alone mechanism claim would require individual nest dates and relative fitness data, a defensible counterfactual fitness curve, and decision-time available information/constraints for the relevant actor; absent these, **H_info, H_cap, H_cost and H_null remain observationally unresolved**.
- The V7R / V8 frozen results and V4 manuscript remain untouched. No new causal discovery or journal upgrade is asserted.

## Sources
Lany et al., Oikos 125:656–666, https://doi.org/10.1111/oik.02412.
Dryad dataset https://doi.org/10.5061/dryad.g1m27.
Public source mirror (same raw Git blob): https://github.com/hurlbertlab/caterpillars-count-analysis/blob/master/data/birds/BTBW_data_Dryad.csv.
