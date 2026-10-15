# Supplementary Table S3 — Day-scale forecast diagnostics versus bird mismatch

**Classification:** POST-OUTCOME, EXPLORATORY and MULTIPLICITY-EXPOSED. These six regressions were designed after the original V8 signed-correlation outcome and the subsequent day-unit diagnostic. The analysis recipe was fixed in `docs/PAYOFF_B_V8_DAYMETRIC_BIRD_TRANSFER_EXPLORATORY_LOCK_20261015.md` before execution; this does **not** make it preregistered or confirmatory.

**Data:** 166 original environmental source–target pairs in the complete day-scale record; only 72 original environmental pairs eligible for the 150 species–target bird mismatch records (22 species). The same 150 bird responses and fixed-arrival structural-null responses are used throughout. Predictor SD is calculated across the 72 unique eligible environmental pairs, NOT 150 species-target rows. Each species contributes equal total weight. Uncertainty: 10,000 percentile bootstrap draws at the 72-spatial-pair level.

| Environmental predictor change (late − early) | Bird mismatch outcome | Slope per 1 environmental-pair SD | 95% unique-pair CI | Nominal CI excludes 0? |
|---|---|---:|---:|:--:|
| Source-informed leave-one-year-out RMSE (days; higher is worse) | Observed log-mismatch | +0.009467 | −0.089423 to +0.098864 | No |
| Source-informed leave-one-year-out RMSE | Fixed-bird-arrival structural null | +0.073923 | −0.009811 to +0.159610 | No |
| Source-informed leave-one-year-out RMSE | Observed minus fixed arrival | −0.064456 | −0.138373 to +0.007657 | No |
| Incremental forecast MSE reduction from source (days²; higher is more relative forecast value) | Observed log-mismatch | +0.095296 | −0.002578 to +0.162303 | No |
| Incremental forecast MSE reduction from source | Fixed-bird-arrival structural null | **+0.150397** | **+0.094067 to +0.231582** | **Yes** |
| Incremental forecast MSE reduction from source | Observed minus fixed arrival | −0.055101 | −0.167542 to +0.021201 | No |

**Results:** Neither of the two *bird-specific increment* CIs excludes zero. One nominally nonzero positive relationship appears **when bird arrival has been fixed**. This makes the original ecological distinction particularly clear: an environment-derived retrospective forecast can covary with a phenological-mismatch statistic for mathematical/geographic reasons even when no bird arrival adjustment is allowed by the structural null. This is an observational/model comparator, not a causal isolation of every environmental mechanism.

**What cannot be concluded:** Zero effect is not established merely because two confidence intervals contain zero. Neither cue availability to the individual, movement/stopover opportunities, fitness consequences nor biological actionability was measured. Only 72 distinct geographic environmental relationships underlie the bird-target associations, and their spatial correlation could make 72-pair-bootstrap intervals optimistic. The fixed-arrival null is one structural rival, not a universal biological no-behavior counterfactual.

**Important distinction:** The early-period source-informed LOYO skill estimated by a finite-data regression can be negative, even though free, optional, perfectly rational additional information has nonnegative optimal expected decision value under unchanged feasible choices. The regression predictor is not an ideal Bayes choice and may overfit.

**Source and provenance:** The exact original 2026-10-05 day-scale R outputs were independently restored from the original source and connected to the frozen V8 transfer/structural-null rows. Exploratory R script `analysis/movement_phenology/payoff_b_v8_daymetric_bird_transfer_exploratory.R`; six-slope result receipt `docs/PAYOFF_B_V8_DAYMETRIC_BIRD_TRANSFER_EXPLORATORY_RESULT_20261015.md`. Verified original data/results artifact: https://github.com/zuizui0223/payoff/actions/runs/38672782848/artifacts/11945021036.

**Additional sensitivity disclosure:** A separate *after-six-outcome* spatial/group-omission audit is planned in `docs/PAYOFF_B_V8_DAYMETRIC_SPATIAL_SENSITIVITY_LOCK_20261015.md`. Its outcome must be reported whether or not it preserves this table's nominal interval-excludes-zero classification. Do not silently substitute a pair bootstrap for a coarser spatial-block analysis.

**Publication ceiling:** This is a supplementary model-identification check, not a new preregistered hypothesis and not evidence that a migratory bird did or did not use, perceive or benefit from the source. The original preregistered V8 negative transfer remains NOT_SUPPORTED and unchanged.
