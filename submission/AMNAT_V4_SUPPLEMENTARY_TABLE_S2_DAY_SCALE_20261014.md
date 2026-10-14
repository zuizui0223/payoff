# Supplementary Table S2 — day-scale predictability after V8

**Status:** EXPLORATORY / POST HOC, outcome-informed, computed after the original 2026-10-05 signed correlation result. Do not substitute for the registered tests.

**Units:** 166 unique source–target spatial pairs across 28 bird species; early 2002–2009 vs late 2010–2017. Last row: 150 bird species–target records sharing 72 independent environmental pairs, 22 species.

| Summary metric | Early | Late | Change | Pair bootstrap 95% CI (change) |
|:--|--:|--:|--:|:--|
| Detrended signed Pearson correlation (registered primary) | +0.2838 | +0.6528 | +0.3690 | +0.2984 to +0.4365 |
| Target residual SD (days) | 2.412 | 4.662 | +2.250 | +1.946 to +2.549 |
| Source-to-target residual slope (days/day) | 0.399 | 0.640 | +0.241 | +0.142 to +0.339 |
| In-window explained variance R² | 0.290 | 0.572 | +0.282 | +0.234 to +0.330 |
| Fitted in-window residual RMSE (days) | 1.821 | 2.494 | +0.673 | +0.460 to +0.891 |
| Source-informed leave-one-year-out RMSE (days) | 4.113 | 4.168 | +0.055 | −0.591 to +0.632 |
| Target-trend-only leave-one-year-out RMSE (days) | 3.182 | 5.865 | +2.683 | +2.342 to +3.013 |
| Incremental source skill: LOYO no-source RMSE minus source RMSE (days) | −0.931 | +1.697 | +2.628 | +2.134 to +3.202 |
| Source squared-loss value: LOYO MSE reduction from source (days²) | −16.094 | +15.987 | +32.082 | +21.040 to +46.796 |
| Bird absolute arrival–green-up mismatch (days; 150 rows, unweighted) | 8.418 | 8.066 | −0.352 | −0.890 to +0.200 |

**Bird sensitivity:** equal-species day-scale change −0.627 days (95% pair CI −1.147 to −0.018 days); the frozen equal-species *log-mismatch* result has a CI crossing zero. This is not a new registered improvement claim.

## Measurement and inference contract

Source and target green-up dates were each linearly detrended against year in each registered period. In-window regression RMSE is measured on the same observations used for fitting; it is optimistic. For leave-one-year-out (LOYO), refit source and destination trends and the source-to-target anomaly regression without one held-out year. The target-trend-only comparison predicts the same held-out destination without the source anomaly. Reported RMSE means are the arithmetic mean of *pair-specific* RMSE values, not a pooled observation-level RMSE. Paired delta confidence intervals use 10,000 resamples over unique environmental pairs.

Spatial-sensitivity note: 10° geographic-block CI for in-window residual RMSE change was −0.257 to +1.598 days, crossing zero. LOYO source RMSE change (+0.055 days) has 95% intervals crossing zero under all reported pair/source/target and 5°/10° checks. Mean squared-loss source value increases under the reported spatial-dependence checks. All such analyses are outcome-informed, post hoc sensitivities.

**Interpretation rules:** (i) Doubling the destination's variability did not *cause* Pearson correlation to rise—correlation is scale invariant. (ii) LOYO is retrospective statistical prediction using contemporaneous source values, *not* proof that birds possessed calibrated forecasts before departure. (iii) The registered matching transfer tested environmental correlation change as the exposure, *not* daily-RMSE change. A negative direct RMSE-to-mismatch transfer has not been established from this table. (iv) The group of 150 bird rows does not provide 150 independent environmental relationships or survival/fitness outcomes.

## Immutable provenance

Source R script: analysis/movement_phenology/payoff_b_v8_metric_scale_diagnostic.R, restored byte-identically from 2026-10-05 commit a341f8a082a33a095622c77f1777a7c8249b7156; Git blob SHA a42b4d9f1a1792d647d6091e980754c428009ce1. Prior post hoc audit run: https://github.com/zuizui0223/payoff/actions/runs/37389432690 ; original artifact 11380965912, SHA256 18a8b34abd989f09d5fd98995bf43022b1efeccff2ab4cc744fa91f7d8970ed3.

Complete original numeric receipts: docs/PAYOFF_B_V8_METRIC_SCALE_DIAGNOSTIC_RESULT_20261005.md. The primary V8 hypothesis and all original source/target pair definitions, bootstrap and matching outcomes are unchanged.
