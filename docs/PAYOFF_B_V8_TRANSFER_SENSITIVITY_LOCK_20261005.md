# PAYOFF-B V8 downstream transfer sensitivity lock — 2026-10-05

Status: **POSTPRIMARY; WRITTEN BEFORE POSTPRIMARY TRANSFER SENSITIVITY OUTPUTS ARE OPENED**

The primary V8 downstream transfer coefficient is frozen:
- beta_transfer = +0.06243969;
- 95% unique-pair bootstrap CI = -0.01411178 to +0.1363489;
- INFORMATION_TO_TIMING_TRANSFER = NOT_SUPPORTED;
- PRIOR_MAGNITUDE_TRANSFER_EXCLUDED = YES.

This document fixes implementation details for the already-prespecified
mandatory sensitivities and one necessary descriptive quantity.

## Descriptive mismatch change

Before interpreting the transfer result, report the overall late-minus-early
change in the same log-mismatch outcome.

Two summaries:
1. unweighted species-target-cell mean delta-mismatch;
2. equal-species mean delta-mismatch.

Uncertainty uses the same 10,000 unique-spatial-pair bootstrap, seed 20261005.
This is descriptive and does not alter the transfer support rule.

## S1 — unweighted row model

Fit:
`delta_mismatch ~ z_delta_rho`
with no species-equalizing weights.

Use the same unique-pair bootstrap.

## S2 — equal-species collapse

For each species, calculate:
- mean delta-mismatch across eligible target cells;
- mean z-delta-rho across those cells.

Fit an unweighted species-level regression:
`species_mean_delta_mismatch ~ species_mean_z_delta_rho`.

For bootstrap uncertainty, resample unique spatial pairs, carry all mapped
species-target rows, recompute species means, then refit the species-level
regression.

## S3 — baseline mismatch covariate

Define:
`z_baseline_mismatch = scale(mean_mismatch_early)`
once in the original eligible sample.

Fit the primary equal-species-weighted model:
`delta_mismatch ~ z_delta_rho + z_baseline_mismatch`.

Bootstrap unique pairs and keep the original standardization constants fixed.

## S4 — target green-up shift covariate

Define:
`delta_greenup = mean_greenup_late - mean_greenup_early`;
`z_delta_greenup = scale(delta_greenup)`
once in the original eligible sample.

Fit:
`delta_mismatch ~ z_delta_rho + z_delta_greenup`
with equal-species weighting and the same pair bootstrap.

## S5 — both covariates

Fit:
`delta_mismatch ~ z_delta_rho + z_baseline_mismatch + z_delta_greenup`
with equal-species weighting and the same pair bootstrap.

## S6 — leave one species out

Omit each eligible species in turn and refit the original primary
equal-species-weighted model. Report:
- coefficient range;
- number negative;
- number positive.

No omitted fit can replace the full-sample primary result.

## S7 — exact-complete bird windows

Restrict to species-target rows with exactly 8 finite mismatch years in both
2002–2009 and 2010–2017.

Recompute the eligible unique-pair mean/SD used to standardize delta-rho within
this restricted sample, then fit the original equal-species-weighted model and
use 10,000 unique-pair bootstrap replicates.

No minimum retained sample threshold is chosen after inspection; the retained
row, pair and species counts are reported.

## Interpretation boundary

Robust positive coefficients across these sensitivities would strengthen the
descriptive statement that larger environmental-connectivity gains did not map
onto larger mismatch reductions in this dataset. They still would not identify
why.

A negative sensitivity result does not overturn the primary result; it instead
shows dependence on weighting, baseline state, climate shift or completeness.

No migration-speed-change result is opened in this sensitivity script.
