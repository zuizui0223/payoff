# PAYOFF-B V8: after-outcome geographical-dependence check of day-metric/bird transfer

**Date:** 2026-10-15  
**Status:** 6 previously opened post-outcome exploratory slopes; spatial and influence robustness designed **after** those six outcomes were known. Not a preregistered corroboration. The original V8 registered signed-rho transfer remains unchanged and NOT_SUPPORTED.

## Source/run and method identity

- Fixed sensitivity contract: `docs/PAYOFF_B_V8_DAYMETRIC_SPATIAL_SENSITIVITY_LOCK_20261015.md`, committed before executing the four sensitivity families.
- **SUCCESS:** [source/frozen-data CI 38697479092](https://github.com/zuizui0223/payoff/actions/runs/38697479092).
- Original-source and all 4 bootstrap matrices + 564 complete omission-slope observations: [CI artifact 11954737468](https://github.com/zuizui0223/payoff/actions/runs/38697479092/artifacts/11954737468). Outer archive SHA256 `fd14cb580a7fb4e952747663e56d1158a2f7917f9e18f175fb2e3ce292d9bfbb`.
- Original source sample was **150 bird species–target rows**, using **72 distinct environmental source–target pairs** from 22 bird species, with the 166 original full environment-pair record supplying verified cell IDs and coordinates.
- Predictor scaling, 2×3 slopes, species-equal weighting, and original outcomes matched PR #333 exactly. 10,000 bootstrap draws per grouping (seed 20261015); **no regression retuned**.

## Original 72-pair bootstrap six-slope baseline

| Metric | Observed log-mismatch β [95% CI] | Fixed-arrival null β [95% CI] | Bird-specific increment β [95% CI] |
|---|---|---|---|
| Δ LOYO source-informed RMSE (higher = worse) | +0.0095 [−0.0894, +0.0989] | +0.0739 [−0.0098, +0.1596] | −0.0645 [−0.1384, +0.0077] |
| Δ source incremental squared-loss forecast value (higher = more relative skill) | +0.0953 [−0.0026, +0.1623] | **+0.1504 [+0.0941, +0.2316]** | −0.0551 [−0.1675, +0.0212] |

**Neither bird-specific increment CI excludes zero**; the nominally positive fixed-arrival source-value effect is not a bird behavioral change.

## Geographic/source-target dependence sensitivity: all six slopes by scheme

All rows below report the same six *point estimates* as the baseline. Only the bootstrap resampling unit changes. In the matrix, each cell is its 95% percentile interval; all are after-outcome exploratory.

| Grouping / independent clusters | Δ RMSE → observed | Δ RMSE → fixed arrival | Δ RMSE → bird increment | Δ forecast value → observed | Δ forecast value → fixed arrival | Δ forecast value → bird increment |
|---|---|---|---|---|---|---|
| **Source cell (20)** | [−0.1001, +0.1731] | [−0.0306, +0.2061] | [−0.1596, +0.0450] | [−0.0064, +0.1722] | **[+0.1053, +0.2780]** | [−0.2087, +0.0232] |
| **Target cell (19)** | [−0.0831, +0.1111] | [−0.0071, +0.1412] | [−0.1617, +0.0404] | [−0.0226, +0.1529] | **[+0.0981, +0.2369]** | [−0.1876, +0.0315] |
| **Target 5° grid (9)** | [−0.0861, +0.1126] | [−0.0294, +0.1427] | [−0.1332, +0.0351] | [−0.0690, +0.1443] | **[+0.0506, +0.2470]** | [−0.2080, +0.0301] |
| **Target 10° grid (4)** | NOT_ESTIMABLE | NOT_ESTIMABLE | NOT_ESTIMABLE | NOT_ESTIMABLE | NOT_ESTIMABLE | NOT_ESTIMABLE |

No bootstrap draw was numerically degenerate for the 20-source-cell, 19-target-cell or 9-grid-block schemes (10,000 valid draws each). The 10° scheme failed the **pre-fixed minimum five independent blocks**; all 10,000 locations in its draw output are explicitly NA by design. No result or sign is claimed for 10° inference.

**Prespecified-after-outcome conclusion:** In all three *estimable* alternative dependence models, neither bird-specific increment CI excludes zero. Conversely, the positive fixed-arrival source-value association's interval stays above zero. This strengthens the warning against treating source forecasting gain as biological action, **not** a conclusion that actual bird action was absent. Three broader bootstrap partitions do not resolve unmeasured year dependence or conceptual causal confounding.

## Complete leave-one-out diagnostics (no unit chosen for exclusion)

The analysis reported **564 deletion fits**: all 22 leave-one-species-out and 72 leave-one-environment-pair-out outcomes for every one of six slopes. No fit failed or was dropped.

| Contrast | Leave 1 of 22 species out: β range | Leave 1 of 72 pairs out: β range |
|---|---|---|
| Δ RMSE → bird-specific increment | −0.0825 to −0.0517 | −0.0825 to −0.0413 |
| Δ source MSE value → bird-specific increment | −0.0815 to −0.0397 | −0.1146 to −0.0329 |
| Δ source MSE value → fixed-arrival null | +0.1322 to +0.1833 | +0.1310 to +0.1764 |

The incremental estimates stayed negative under each single-unit omission. **Stable signs of noisy point estimates do not establish a biological effect**, particularly when all spatial-bootstrap 95% intervals for the increments include zero. The fixed-arrival structural-null effect stayed positive under all omissions.

## Scientific interpretation and limitations

- This is now a particularly explicit **negative mechanism-identification result**: correlations between an environmental *statistical* forecast-value gain and a bird mismatch endpoint can survive all three available spatial clustering rules *even with bird arrival fixed*.
- No animal-specific cue calibration, actual source-route use, available route correction, mortality or fecundity was observed. The null is a model of holding bird arrival fixed, **not** a randomized field manipulation.
- Spatial dependence is substantial: a target 10° grouping left only 4 independent clusters and is nonestimable by the fixed criterion. None of the 150 species-target observations should be called an independent source–target pair.
- This is **a second layer of post-outcome exploration**, in addition to the six earlier post-outcome slope tests; no nominal interval is interpreted as confirmatory or multiplicity corrected.
- Full scripts, original joined rows, 40,000 spatial-bootstrap *attempts*, and the 564 leave-one-out coefficient observations are in the source artifact. The registered V8 environmental/rho and bird-transfer outcome rules are unaffected.

## Publication decision

The core ecological message is **observed environmental predictability, and even its day-unit forecasting benefit, cannot by themselves identify bird timing adjustment**. Do not change this into a proof that birds did not track, a causal fitness effect, or a claim that the two metrics are biologically useless.

Retain the full table and sensitivity results as Supplementary S3/associated sensitivity material. A restrained cross-reference in the Paper 2 Discussion is appropriate once manuscript word count and source-verbatim reproducibility are checked.
