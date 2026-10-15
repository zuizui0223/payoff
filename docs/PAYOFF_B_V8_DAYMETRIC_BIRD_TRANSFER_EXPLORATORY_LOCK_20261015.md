# PAYOFF-B V8: exploratory day-metric-to-bird-mismatch direct transfer

**Freeze of analytic recipe before new direct-slope execution:** 2026-10-15. **Epistemic status: POST-OUTCOME, MULTIPLICITY-EXPOSED EXPLORATION.** The preregistered V8 cross-site correlation → bird-matching hypothesis and results are locked and remain unchanged. This cannot retrospectively become a prespecified replication.

## The specific untested claim

The original V8 matched 150 bird species–target observations (22 species) to 72 distinct source–target environmental spatial pairs and tested signed correlation change versus change in bird log absolute arrival–green-up mismatch. The separate day-scale post hoc diagnostic, using the same registered windows and source–target mapping, reported source-informed leave-one-year-out RMSE (days) and the *cross-validated source-information advantage* in days². Previous Paper 2 drafts had **not directly tested** whether changes in these day-unit quantities are associated with bird mismatch change.

One cannot state that both correlation-based and day-based information measures failed to transfer to tracking without an actual day-metric transfer analysis.

## Fixed inputs, no phenotype remapping

Only these already-frozen original 2026-10-05 artifacts are allowed:

1. Historical day-scale diagnostic R-verified artifact: original run [38585167565](https://github.com/zuizui0223/payoff/actions/runs/38585167565), saved 166-pair file `payoff_b_v8_metric_scale_pairs.csv` and 150-row `payoff_b_v8_metric_scale_bird_rows.csv`, source R blob `a42b4d9f1a1792d647d6091e980754c428009ce1`.
2. Original frozen V8 structural-null artifact restored in [38404051747](https://github.com/zuizui0223/payoff/actions/runs/38404051747), `payoff_b_v8_transfer_structural_null_rows.csv`. These are the **original**, not newly simulated, fixed-bird-arrival structural null observations.
3. For independent identity check only, the originally frozen `payoff_b_v8_transfer_primary_rows.csv`.

The response `delta_log` must match original registered `delta_mismatch` for every `(species, target_cell, pair_key)` row within numerical error. Do not modify the set of 72 eligible environmental pairs, 22 species or 150 rows, and do not use raw bird arrival outcomes to select source pairs.

## Day-scale exposures and retained outcomes

Two exposure coordinates, selected a priori *within this exploratory task*:

- **E1:** `delta_loo_rmse` = change in out-of-sample source-informed forecast RMSE (late − early, days); higher is worse statistical accuracy.
- **E2:** `delta_loo_value_mse` = change in held-out incremental squared-error improvement from adding source green-up versus target-trend-only forecast (late − early, days²); higher means the source became relatively more valuable.

For each exposure, independently standardize using **only 72 unique environmental-pair values**, once, before bootstrapping. Six fixed descriptive slopes:

| Y | Meaning |
|--|--|
| Y1=`delta_log` | Actual late−early species-target log absolute bird mismatch |
| Y0=`delta_pseudo_mismatch` | Registered **fixed-arrival structural null** |
| Y1−Y0 | Bird-specific increment beyond fixed-arrival geometry |

Fit weighted OLS with intercept, `Y ~ z(Ek)`, using each species' total weight 1 (row weight `1/n_rows_within_species`). Analyze each of E1 and E2 against all three outcomes. All six slopes and CIs must be reported; no choosing one because significant.

**Uncertainty:** Resample the **72 distinct spatial-pair IDs** with replacement 10,000 times (seed 20261015), keeping *all* species-target rows attached to every drawn pair. Within each resample, recompute inverse-within-species row counts; keep the previously standardized exposure fixed (do not refit it to bootstrap draws). Report percentile bootstrap 95% intervals. Report positive/negative signs and whether the interval excludes zero, but no confirmatory p-values or claims of "no effect" from a CI that includes zero.

**Guardrails:** Check sample identity/joins, finite x/y, SD of x > 0, absence of duplicate join keys, and all previously registered V8 estimates unchanged. The original full V8 model tests are not rerun here as new hypotheses; this is a limited post hoc descriptive slope analysis.

## Biological meaning and competing explanations

These predictors are retrospective model skill, not cues demonstrated to have been acquired before a real migratory decision. Cross-site green-up pairs are geographically inferred, not measured individual routes. The fixed-arrival null can generate statistical association through shared target phenology and transformed mismatch, so only an increment over it merits descriptive attention. Even that increment cannot establish animal cognition, actionability, compensation, natural selection or demographic fitness because those states are unmeasured.

Alternative causes include changing variability in green-up, direct local temperature/photoperiod response, different candidate cues, non-random range availability, measurement error and mathematical coupling. The two exploratory slopes are correlated, and the six analyses are not multiplicity-controlled. Results should remain supplementary or internal unless robust and interpreted within this ceiling.

**Stop rule:** If observed-vs-original response keys/values differ, if 72 pair IDs or 150 rows do not match, if any bootstrap or nonfinite diagnostic fails, return `NOT_ESTIMABLE` rather than rerunning with modified eligibility. Every outcome, including null or counterdirectional slopes, must be committed to the record.

**No manuscript promotion before numerical run/independent review.** In particular, the headline that both measures independently failed to predict bird tracking is **not yet established**.
