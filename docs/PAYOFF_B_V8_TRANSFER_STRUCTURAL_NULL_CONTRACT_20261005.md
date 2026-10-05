# PAYOFF-B V8 transfer structural-null audit contract — 2026-10-05

Status: **POSTPRIMARY/PRE-AUDIT-OUTCOME**

Known before this audit:
- V8 environmental delta-rho is robustly positive;
- the preregistered information-to-timing transfer coefficient is +0.06244
  with 95% pair-bootstrap CI -0.01411 to +0.13635;
- all 22 leave-one-species-out transfer coefficients are positive;
- overall mean mismatch change is near zero.

The positive transfer coefficient is NOT interpreted biologically yet because
the environmental exposure and mismatch outcome both contain target green-up.

This audit is designed before opening any of the diagnostics below.

## A1 — baseline-rho adjustment

The V8 change score contains the early correlation mechanically:

`delta_rho = rho_late - rho_early`.

Using the same frozen 150-row transfer sample, obtain `rho_early` from the
already-opened V8 pair table, standardize it over the eligible unique pairs,
and fit the equal-species-weighted model:

`delta_mismatch ~ z_delta_rho + z_rho_early`.

Use 10,000 unique-spatial-pair bootstrap replicates, seed 20261005.

Purpose: diagnose whether the positive transfer coefficient is explained by
baseline predictive connectivity / change-score regression-to-the-mean.

## A2 — environmental-geometry fixed-arrival null

For each eligible species-target cell, define one fixed bird date:

`fixed_arrival = mean(arr_GAM_mean)`

across all finite years from 2002 through 2017 for that species-target cell.

For each year construct:

`pseudo_mismatch_y = log1p(abs(gr_mn - fixed_arrival))`.

Using the same >=6-years-per-window rule, calculate late-minus-early
`delta_pseudo_mismatch` and fit:

`delta_pseudo_mismatch ~ z_delta_rho`

with equal-species weighting and 10,000 unique-pair bootstrap replicates.

Because annual bird timing is held fixed, any coefficient here can arise from
the shared target-green-up geometry and the nonlinear mismatch transformation,
not from adaptive bird timing.

Also report:

`beta_bird_increment = beta_observed - beta_fixed_arrival_null`.

Bootstrap this difference by calculating both coefficients in the same sampled
pair replicate.

Interpretation:
- beta_bird_increment < 0 means observed bird timing attenuates the
  environmental-only positive association;
- beta_bird_increment = 0 means the observed coefficient is fully compatible
  with the fixed-arrival structural null;
- beta_bird_increment > 0 means observed bird timing strengthens it.

No causal label is attached.

## A3 — within-window arrival permutation null

For each eligible species-target cell independently:
- permute annual `arr_GAM_mean` values among EARLY years only;
- permute annual `arr_GAM_mean` values among LATE years only;
- keep green-up years fixed;
- preserve each cell's window-specific arrival distribution and mean while
  destroying year-specific arrival–green-up alignment.

Use exactly:
- PERMUTATION_REPLICATES = 2000;
- PERMUTATION_SEED = 20261005.

For each permutation, recompute window mean log mismatch and the original
equal-species-weighted transfer coefficient using the fixed original
`z_delta_rho`.

Report:
- null median and 2.5–97.5% interval;
- fraction of permutation coefficients <= the observed coefficient;
- fraction >= the observed coefficient.

This is a randomization diagnostic, not a replacement primary p-value.

## A4 — baseline-change coupling diagnostic

Across eligible unique environmental pairs, report Pearson correlation between:
- `rho_early`;
- `delta_rho`.

Use a 10,000 unique-pair bootstrap interval.

This is descriptive and diagnoses the expected bounded-correlation /
regression-to-the-mean coupling.

## A5 — Fisher-z transfer scale

For eligible pairs define:
`delta_z = atanh(clamp(rho_late)) - atanh(clamp(rho_early))`,
with clamp at +/-0.999 exactly as in the frozen V8 sensitivity.

Standardize delta-z over eligible unique pairs and fit the same
equal-species-weighted transfer model with 10,000 unique-pair bootstrap
replicates.

Purpose: ensure the transfer direction is not specific to raw-r change scale.

## Decision rule

No single audit produces a new flagship claim.

The positive transfer coefficient is treated as **STRUCTURALLY EXPLAINED** if:
- the fixed-arrival-null coefficient is positive and
- the 95% bootstrap interval for beta_bird_increment includes zero.

It is treated as **BIRD-INCREMENT DETECTED** only if the beta_bird_increment
interval excludes zero.

Regardless of this label, the original negative transfer prediction remains
NOT_SUPPORTED.

## Claim boundary

Even a detected bird increment does not prove cue perception, deadlines,
recourse limitation or causality.

If the positive transfer is structurally explained, the manuscript must not
say that increasing predictability worsened bird mismatch. The defensible
result would instead be:

> environmental predictability strengthened, but no corresponding improvement
> in bird mismatch was detected.

No migration-speed result is opened in this audit.
