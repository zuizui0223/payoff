# PAYOFF-B Greenland white-fronted goose: stage-3 weather → stage-4 feeding

**Freeze:** 2026-11-19. **Design stage:** source schema and support audited, **new lagged coefficient not yet opened**. **Scientific grade:** post-publication exploratory reanalysis of an already-published dataset, **not** preregistered independent replication or a natural demonstration of information-deadline theory.

## Original source and provenance

Schindler et al. (2024), *Proceedings of the Royal Society B*, DOI [10.1098/rspb.2023.2016](https://doi.org/10.1098/rspb.2023.2016), originally studied energetic trade-offs in migration, parental care and reproduction in Greenland white-fronted geese. Original public [GitHub repository](https://github.com/aschindler23/Schindler_etal_2024_ProcB) (license MIT) supplies original `spring_data.csv`, `autumn_data.csv` and both full-annual-cycle R/JAGS model programs. Original Dryad DOI [10.5061/dryad.2547d7wzn](https://doi.org/10.5061/dryad.2547d7wzn).

**Pinned original GitHub file blob:** `spring_data.csv` Git blob SHA1 `ca3736a281dfd2465921efc940dd985499c71a4f`. The read-only runner must download the original 2024 upstream file and reject it unless `git hash-object` equals this SHA; print and store exact SHA256 of the bytes. No raw source individual IDs are committed to PAYOFF; only aggregate results are uploaded.

Original data schema audited **before the new temporal-effect fit**:
- **642 original source rows**, exactly **107 bird-years**, **49 original birds**, **five breeding years 2018–2022**;
- six stages per bird-year, with `first_day` strictly increasing for all 107 groups;
- **30 birds followed ≥2 years**, **18 birds ≥3 years**;
- breeding outcome (once per bird-year): 28 successes, 72 failed breeding attempts, 7 deferrals;
- stage 3 (first half of spring staging) frozen-day fraction has nonzero within-year variation in every study year; stage 4 is the second half of the same staging period;
- `num_feed_fixes/num_ACC_fixes` and `log_ODBA` are original behavior proxies, **not direct energetic intake or control capacity**. ACC fixes are repeated measures within a bird-year, **not independent biological samples**.

Original authors **already found** weather/habitat dependence of feeding and energetic cost and associations with subsequent breeding. We must not claim “weather affects feeding” or “longer feeding predicts breeding” as novel PAYOFF results. The new value, if any, is a **stage-ordered and out-of-bird/year predictive stress test**, not causation.

## Frozen primary test: early staging weather and later feeding

**Unit:** bird×year (n≤107), **not** 642 stage rows or 300,000 ACC fixes.

Define `feed3 = n_feeding_ACC_stage3 / n_total_ACC_stage3`, `feed4` analogously, both bounded [0,1], rejecting zero denominators. Define `freeze3_10pp = prop_days_below_freezing(stage3)/0.1`.

Primary fixed linear model (no threshold selection):

```
feed4 ~ 1 + feed3 + freeze3_10pp
        + mean_precip3 + prop_storm_days3 + first_day3
        + mean_precip4 + prop_storm_days4 + year indicators
```

Primary coefficient: **change in stage-4 feeding fraction per 10-percentage-point higher earlier stage-3 freezing fraction**, *holding stage-3 feeding and measured weather/time covariates fixed*. The observed `prop_days_below_freezing(stage4)` is nearly zero and is not in the frozen primary (but must be shown descriptively). Freeze3 is a measured weather **condition**, **not a bird's observed probabilistic cue about future breeding climate**. Stage4 weather is concurrent with the downstream feeding outcome, so the coefficient cannot be called a causal effect of early temperature.

Inference: ordinary least squares with **bird-level cluster-robust** covariance across bird-years, t interval using df = number of birds−1 = **48**, year fixed indicators (2019–2022, 2018 reference). Show β, CI, p, n birds, rank, partial R²/SSR improvement against the identical model minus `freeze3_10pp`. No arbitrary controls added or thresholds tuned after signs appear.

**Two competing, predeclared interpretations**:
- β>0: consistent with *compensatory increase* in later feeding after earlier freezing, conditional on earlier feeding; **also compatible with unmeasured year/location conditions**.
- β<0: consistent with *persistent environmental limitation*, rather than successful compensation, conditional on current weather.
- CI including zero: lagged independent association **NOT SUPPORTED** by this original cohort.

## Frozen independent-group predictive controls

1. **Leave-one-entire-year-out** (5 folds) linear **ridge α=1** comparison: same predictors using *numeric calendar year centered and standardized within each training fold*, no unlearnable year dummy. Baseline excludes freeze3; candidate adds freeze3. All regressors standardized using *training data only*; ridge intercept unpenalized. Report year-specific and pooled heldout MSE. No choice of α, year splits or predictors after results.
2. **Leave-one-entire-bird-out** (49 folds) with the same frozen ridge α=1 and train-only standardization; report pooled heldout MSE. Repeated years for the same bird cannot leak into its test fold.
3. **Leave-one-study-year-out** sensitivity of primary coefficient (5 fits), keeping year indicator encodings rebuilt using remaining years; report min/max signs, but **do not count five years as many independent environmental perturbations**.

**Promotion ceiling:** an apparent within-sample β without a stable out-of-year improvement is **not** a portable climatic-feedback effect. Even with improvement, the result remains same-source observational and not a proof of feedback gain or information-deadline access.

## Frozen secondary predictive test: does late staging behavior add forecast information for breeding?

At **the end of stage 4** (before stage 5 migration and stage 6 early breeding), compare two **penalized logistic models** for original binary `breeding_success`:

- **Weather-and-earlier-behavior baseline:** `feed3, freeze3, precip3, storms3, precip4, storms4, stage4_first_day, year_numeric`.
- **Updated observation model:** exactly baseline **plus** `feed4, log_ODBA4` (later observed feeding/energetic behavior).

Use original outcome once per bird-year (28 success, 79 fail-or-defer), **train-only z-scoring**, logistic L2 `C=1`, unpenalized intercept, no outcome-based feature screening. Evaluate **leave-one-bird-out** and **leave-one-year-out** aggregate log loss and Brier score plus per-year log loss; report both signs, no p-value on dependent folds.

This evaluates **additional predictive value from observing subsequent behavior** at a *later time*, not the information quality birds themselves perceived, its cause, or a direct fitness cost of waiting. Published paper already reports spring feeding/energetic trade-offs with reproduction. Do not market this as new independent evidence of that effect.

## Explicit fail-closed gates

- Reject if source Git blob SHA mismatch, 642 rows/107 bird-year groups/49 birds/5 years change, repeated stage absent or non-ordered, source outcome inconsistent across stages or invalid category, or denominator zero.
- Refuse model if fewer than 30 birds or 3 years or 15 successes / 15 non-successes, or no within-year freezing contrast in ≥3 years.
- No separate source-independent field validation, no causal claims about information before departure, no `q_wait`, `D_eff`, `r(t)`, no actual source-target cue predictability, and **no actual fitness-to-age-one observation**.
- No coordinates, raw bird IDs, whole original CSV, event-level ACC fixes, eBird or TinyFish used or redistributed. Use only metadata and aggregate model receipts.
- **If original source can't be downloaded or source signature changes, report ACCESS_BLOCKED, not NOT_SUPPORTED**, and don't substitute another dataset.
- Original frozen V7 source q×geographic urgency and journal manuscript remain untouched.

## Validation

Use separate clean `analysis/payoff-b-greenland-goose-lagged-weather-20261119` branch from `main`, synthetic regression tests, and a dedicated GitHub Actions original-source SHA-pinned run. Record full success, negative or failure branches without model retuning.
