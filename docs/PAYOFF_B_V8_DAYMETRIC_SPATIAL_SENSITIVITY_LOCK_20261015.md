# PAYOFF-B V8 day-metric→bird transfer: dependence sensitivity lock

**Date:** 2026-10-15. **Post-outcome, exploratory second-order sensitivity.** The six exploratory point coefficients and 72-pair bootstrap results were already opened in PR #333 before this sensitivity was planned. **Do not treat this as a preregistered robustness confirmation.**

## Fixed scientific data

Use the already source-verified joined 150 species–target rows in the original [PR #333 CI artifact](https://github.com/zuizui0223/payoff/actions/runs/38672782848/artifacts/11945021036), plus the separately verified full original 166-pair day-scale diagnostic artifact for target lat/long, source-cell and target-cell membership. Retain exactly 150 bird rows, 72 unique environmental source–target pairs, 22 species and the **same two externally standardized predictor coordinates** and three outcomes as PR #333. The original six coefficients and CIs **MUST remain unchanged**.

## Four prespecified sensitivity families (chosen after six-slope outcomes)

1. Source-cell cluster bootstrap: draw distinct `source_cell` groups with replacement, preserving all linked environmental pairs and all linked bird rows; 10,000 replicates.
2. Target-cell cluster bootstrap: likewise resample distinct `target_cell` groups; 10,000 replicates.
3. Breeding target-grid **5° geographic block** bootstrap: block identity `floor((target_lat+90)/5):floor((target_lng+180)/5)`, then resample blocks, retaining all linked rows; 10,000 replicates.
4. Breeding target-grid **10° geographic block** bootstrap: same definition at 10 degrees; 10,000 replicates.

Each draw estimates the **same six slopes** from inverse-included-rows-per-species weighting. Do not estimate a new regression, include or exclude a species after looking at the result, or restandardize exposures in each draw. The point coefficients must exactly match original PR #333. The difference between observed and fixed-arrival effects must equal the bird-specific incremental effect.

A few spatial resamples can become degenerate. **Do not silently filter**: report number of distinct blocks, number and fraction of invalid replicates for each scheme, and assign the full scheme `NOT_ESTIMABLE` if more than 5% are degenerate, fewer than 5 independent clusters exist or any prespecified CI fails. For 95% or more valid draws, report the 2.5–97.5% percentile interval alongside the invalid replicate count; this is a conditional computational sensitivity, not a new confirmatory inference. Retain the full nominal 10,000 draw positions with NA for failures and report each.

## Nonbootstrap sensitivity (deterministic, no selection)

- Leave-one-species-out: 22 slopes for each of the six fixed contrasts, reporting min/max and sign fraction rather than selectively named species.
- Leave-one-environmental-pair-out: 72 slopes for all six fixed contrasts, with min/max and sign fraction.

No species, pair or method is to be called a "confounder" or omitted from the primary slope. Do not search cutoffs, compare significance among unregistered alternative models to select a preferred result, or claim that a confidence interval crossing zero proves a zero effect.

## Scientific ceiling

This tests sensitivity of *environmental proxy–mismatch associations* to geographic dependence and influential taxa/pairs. The purported cue and squared-error forecast fit are retrospective and not confirmed available to a migrant at its decision. An observation-derived fixed-arrival null can reflect mathematical coupling. No individual route, animal sensing, feasible correction, survival, reproduction or causal biological mechanism has been identified. All inference is post hoc and multiplicitous. The original preregistered correlation transfer remains **NOT_SUPPORTED** and untouched.

**Stop rule:** no authenticated pair coordinates or exact 72/150/22 membership, no sensitivity result. Fail rather than fabricate coordinates or reuse species rows as independently randomized geographical pairs.
