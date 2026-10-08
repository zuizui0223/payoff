# PAYOFF-B V8: historical environmental forecast transfer audit

Date: 2026-10-08
Status: pre-execution contract for a **post-outcome exploratory** analysis; original V8 environmental and bird outcomes have already been viewed. This is NOT a preregistered independent test, not a confirmation of a biological information mechanism, and not a revision of any frozen result.

## Biological question

V8 found a substantial rise in **within-window correlation** of spring mid-green-up at source–target cells used by migratory species, but registered gains in bird synchrony were unsupported. Could the environmental source–target relationship learned during 2002–2009 still predict the 2010–2017 destination spring, or had its calibration deteriorated?

This is a narrower environmental-proxy question than whether any bird actually perceived the source cue or acted on a remote forecast.

## Why this is not redundant with V8 correlation

Within-window correlation measures statistical association under contemporaneous fit. Forecast transfer depends on a calibration learned in an **earlier** window. A historical slope or mean could become biased even as contemporary correlation improves; the previous V8 analysis did not estimate this held-out historical-to-later forecast performance.

Neither time-window use nor climate-only reanalysis proves the signal was available in advance of migration. An origin green-up date completed retrospectively is not automatically observable at the action decision time, which remains a separate gate in PR #314.

## Fixed analysis before opening the new forecast-transfer outcome

- Exact frozen V8 source: Amaral BirdMigrationSpeed final.rds, git commit 62c58d77c2028bd863dfe3697b0d9cf29ceaeab0. The original V8 R script rebuilds its exact unique environmental mapping and excludes nonfinite historical correlations under unchanged rules.
- Exact original support: 166 **unique source-target spatial pairs**, used by 28 bird species. No species multiplication of climate outcomes.
- Training: 2002–2009 inclusive, minimum 6 paired green-up years per pair.
- Holdout: 2010–2017 inclusive, minimum 6 paired green-up years per pair.
- Environmental target: destination mid-green-up date gr_mn in days, NOT actual bird fitness or time to hatch.
- Origin proxy: contemporaneous source mid-green-up date. It is intentionally not asserted to be a cue sensed by a bird.
- Baseline model fitted on early years only: destination green-up ~ intercept + standardized calendar year.
- Origin-augmented model fitted on early years only: destination green-up ~ intercept + standardized calendar year + standardized source green-up.
- Both models have identical fixed ridge penalty 1.0 for non-intercept regressors, and all feature centering/scaling uses early training data only. No penalty search or holdout tuning.
- Held-out pair-level score is mean[(target - baseline prediction)^2 - (target - augmented prediction)^2] / early target SD^2, with identical late-year observations in the two models. Positive values favor historically trained origin augmentation.
- Report all pair-level scores, early and late correlations, yearly score, signed calibration bias, total supported units and source-target distance without selecting species or routes based on performance.
- Aggregate the mean and median of unique-pair score gains, fraction positive; pair bootstrap 2000 resamples with fixed seed 20261008 as a descriptive interval.
- Pairs are spatially dependent: additionally block-bootstrap on target geography in fixed 5-degree and 10-degree latitude/longitude grids with 2000 replicates and at least 5 nonempty spatial blocks; otherwise label that sensitivity unavailable. Do not interpret the intervals as causally valid tests of experienced learning.
- The same eight holdout years are shared among locations: show each annual mean/median improvement and fraction positive; count only eight year-level observations for calendar-year consistency, never the number of pair-years as independent replication.

## Source and implementation gates

1. Synthetic test must show that a stable cue-target mapping is useful and a reversed mapping can make a trained cue model worse than calendar-only baseline.
2. Source dataset must pass the unchanged original V8 finite-correlation gate: 166 pairs, 28 species. At least 100 source-defined pairs must provide admissible training and holdout forecasts. Otherwise stop.
3. The run must emit CSV for every admitted pair, every year, year summaries, and one aggregate. CI failure is not a scientific null.
4. A new result is exploratory after V8 outcome exposure irrespective of its sign.
5. No bird timing, fitness, individual cue use, or actionability outcome is read or tested in this analysis. Existing V8 scripts, archive results and manuscript science freeze are untouched.

## Pre-declared descriptive interpretations (no post hoc rescue)

- Mean held-out improvement positive, spatial and year sensitivities consistent: historic origin green-up retains incremental cross-period environmental prediction versus time-only. Does NOT show birds used this information or recourse failed.
- Mean improvement near zero or negative: stronger within-window correlation does not imply that historically trained origin cue improved forecast skill under this comparator. Compatible with a calibration problem, NOT evidence that learned bird forecasts failed.
- Mixed signs, strong geographic/year dependence, unstable support: no generic result; describe heterogeneity as exploratory.
- Any outcome: cannot explain changing bird-resource mismatch or fitness without independent route-specific cue chronology, perceived information, costs and action.

## Scientific competitor framework

- Shared climatic disturbance could alter correlations at many nearby cells without changing each bird's forecast skill.
- Changing mean spring dates and source-target slope could change historical-to-later calibration.
- Birds might use photoperiod, local snow/temperature, social signals or internal schedules instead of remote source green-up.
- Even with accurate calibrated information, matching may be incomplete because movement and early arrival impose survival and energy costs (Jonzén et al. 2007; Torstenson & Shaw 2025).
- Spatial-pair estimates are NOT observed bird paths: frozen mapping links breeding grid cells to the nearest lower-latitude migration grid cell.

## Manuscript and archival boundary

This is an optional environment-only bridge in a draft stacked on PR #316. Its outcomes must be read before even exploratory supplement inclusion is decided. Supported broad results remain the frozen V8 rise in within-window correlation and failure of registered transfer to bird mismatch. No new high-impact publication claim follows automatically.

Code: analysis/movement_phenology/payoff_b_v8_historical_forecast_transfer_exploratory.R
Workflow: .github/workflows/payoff-b-v8-historical-forecast-transfer.yml
