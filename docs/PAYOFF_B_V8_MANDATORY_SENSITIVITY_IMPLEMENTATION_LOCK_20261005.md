# PAYOFF-B V8 mandatory-sensitivity implementation lock — 2026-10-05

Status: **POSTPRIMARY IMPLEMENTATION LOCK; WRITTEN BEFORE ANY MANDATORY-SENSITIVITY OUTPUT IS OPENED**

The V8 primary environmental result has already been opened under the frozen
prospective contract. Its interpretation cannot be rescued or reclassified by
any sensitivity below. The purpose of this document is only to fix the exact
implementation of the eight mandatory sensitivities that were named in the
preoutcome contract before inspecting their outcomes.

Primary provenance:
- source commit: `62c58d77c2028bd863dfe3697b0d9cf29ceaeab0`;
- frozen source-target mapping rule unchanged;
- primary windows: 2002–2009 and 2010–2017;
- primary inferential unit: unique spatial source-target pair;
- dependency-aware bootstrap: 10,000 pair resamples, seed 20261005.

## S1 — Fisher-z change

For every primary finite unique spatial pair, clamp each correlation only for
the numerical transform to [-0.999, +0.999] and calculate:

`delta_z = atanh(rho_late_clamped) - atanh(rho_early_clamped)`.

Report the unweighted unique-pair mean and the equal-species exposure mean with
95% unique-pair/dependency-aware bootstrap intervals.

## S2 — exact-complete primary windows

Restrict the already frozen primary sample to pairs with exactly all 8 paired
green-up years in both 2002–2009 and 2010–2017. Recompute the primary
`delta_rho` unique-pair mean and equal-species exposure mean with the same
bootstrap unit.

No minimum sample threshold is introduced post hoc; the retained count is
reported.

## S3 — target-cell equal weighting within species

Within each species, give each frozen breeding target cell one equal vote.
Because the frozen mapping assigns one source to each species-target cell,
first average `delta_rho` across any accidental duplicate rows for the same
species-target cell, then average target-cell means within species, then average
species means equally. Report this value and its dependency-aware pair
bootstrap interval.

## S4 — source-target geographic distance moderator

Use the unique primary spatial-pair sample. Define the moderator before
inspection as:

`z_log_distance = scale(log1p(source_target_distance_km))`.

Fit the pair-level linear model:

`delta_rho ~ z_log_distance`.

Report the slope and a 95% percentile interval from 10,000 unique-pair
bootstrap resamples. This is a moderator description, not a replacement
primary test.

## S5 — migration-distance class moderator

Use the species-level `Migration distance (km)` field from
`data/stopover_percent.csv` in the same frozen Amaral source commit. Convert
species names to the underscore convention used by `final.rds`.

Define classes from that source table only, without reference to V8 outcomes:
- SHORT: distance <= the median migration distance across all finite species in
  the frozen stopover table;
- LONG: distance > that median.

For V8 species with an available class, compute each species' mean
`delta_rho`, then report the equal-species LONG-minus-SHORT contrast. Its 95%
interval is obtained by resampling unique spatial pairs and carrying the full
species-incidence set into each replicate.

Species lacking the source-table distance are excluded only from S5 and their
number is reported.

## S6 — leave-one-species-out

For each V8 species in turn, remove that species from the frozen
species-to-spatial-pair incidence table. A spatial pair remains in the
geographical sample if at least one other species still uses it.

For every omission report:
1. unweighted mean `delta_rho` across the remaining unique spatial pairs;
2. equal-species mean across the remaining species.

Report the full ranges and the number of omissions retaining positive versus
negative direction. No omission can redefine the primary result.

## S7 — raw undetrended negative-control coordinate

Using the same primary eligible unique spatial pairs and the same two primary
windows, calculate the ordinary Pearson source-target green-up correlation
without year detrending and form:

`delta_rho_raw = rho_raw_late - rho_raw_early`.

Report unique-pair and equal-species means with the same dependency-aware
bootstrap. This remains a negative-control coordinate and cannot replace the
signed-detrended primary analysis.

## S8 — alternative non-overlapping 7-year windows

Keep the frozen spatial mapping but independently apply the original >=6 paired
years rule to:
- EARLY_ALT = 2002–2008;
- LATE_ALT = 2011–2017.

For pairs estimable in both windows, detrend source and target separately on
year, calculate `delta_rho_alt`, and report unique-pair and equal-species
means with the same bootstrap unit.

## Descriptive sign reversal

On the primary pair sample, report the prespecified count and fraction with
`rho_early > 0` and `rho_late <= 0`.

## Interpretation boundary

These sensitivities assess whether the already opened V8 result depends on
correlation scale, missing years, biological weighting, route distance,
migration-distance class, one species, detrending, or the exact window split.
They do not test bird timing, mismatch, fitness, cue perception, or causality,
and they cannot convert the primary NOT_SUPPORTED degradation result into
SUPPORTED.
