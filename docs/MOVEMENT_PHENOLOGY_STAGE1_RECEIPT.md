# PAYOFF-B movement–phenology Stage-1 receipt

Status: **preliminary empirical result; not promoted to the active PAYOFF-B theorem paper**.

Run date: 2026-09-18  
Workflow run: `35328297725`  
Analysis head: `9c8d66aa3c71ee873643c25c5b9bfb0378ea0fbb`

## Dataset

Stage 1 reanalyses Amaral et al. (2025), *Diversity and Distributions*, using the public `br-amaral/BirdMigrationSpeed` analysis data pinned at source commit `62c58d77c2028bd863dfe3697b0d9cf29ceaeab0`.

After the registered complete-case and source velocity filters:

```text
N_ROWS = 5816
N_CENTERED_ROWS = 5746
N_SPECIES = 55
N_YEARS = 15
MEDIAN_SPEED_RATIO = 1.262677869
MEDIAN_DIRECTIONAL_ALIGNMENT = 0.948293188
MEDIAN_SIGNED_LAG_DAYS = -5.15617
MEDIAN_ABSOLUTE_LAG_DAYS = 8.26100
```

The speed-ratio analogue is

```text
u_macro = bird migration-front speed / vegetation green-up-front speed.
```

## Source audit

Two upstream metadata inconsistencies were caught before interpreting the analysis.

1. The generating code sets stored `lag = green-up date - bird arrival date`, while the data dictionary verbally describes the opposite sign. All signed analyses therefore recompute lag directly from `arr_GAM_mean` and `gr_mn`.
2. The data dictionary labels `vArrAng` and `vGrAng` as radians, but `code/1_GetEstimates.R` explicitly applies `rad2deg()` before storing these columns. Directional alignment therefore treats these values as degrees.

The second correction changes median apparent alignment from approximately zero under the incorrect radian interpretation to `0.9483`, consistent with the two fronts moving largely in the same direction.

## Result A — raw absolute arrival/green-up lag

With absolute contemporaneous lag as the response, the flexible GAM detects a speed-ratio effect but its fitted minimum is below the PAYOFF-B order-one reference.

```text
ratio smooth p = 0.00286
ratio × alignment interaction p = 0.0132
delta AIC for adding ratio structure = +17.99

GAM u*_macro at median alignment = 0.405
GAM u*_macro at alignment = 1     = 0.365
```

The quadratic companion places its formal vertex near `u=1.043`, but the curvature term is not supported:

```text
beta(q^2) = 0.04625
p = 0.183
```

Therefore the raw-lag result does **not** support an order-one universal optimum.

## Result B — deviation from the local species × cell phase baseline

The stronger PAYOFF-B analogue is the departure from each species × cell's usual arrival/green-up phase:

```text
lag_deviation
= current signed lag
- mean signed lag for that species × cell.
```

This does not force all species to arrive exactly at vegetation mid-green-up. It asks whether movement/environment timescale matching minimizes interannual phenological displacement from the locally realized phase relationship.

For this centered response:

```text
delta AIC for adding ratio structure = +4.30
ratio smooth p = 0.0748
ratio × alignment interaction p = 0.0519

GAM u*_macro at median alignment = 1.043
GAM u*_macro at alignment = 1     = 1.397
```

Both point estimates are inside the PAYOFF-B theorem's descriptive endpoint interval

```text
1 <= u* <= 1.606115...
```

but the fitted minimum is shallow.

Conditional coefficient draws show substantial optimum uncertainty:

```text
median alignment:
  median u* = 1.079
  95% interval = 0.347 .. 14.465
  fraction inside PAYOFF-B reference interval = 0.277

alignment = 1:
  median u* = 1.522
  95% interval = 0.465 .. 14.465
  fraction inside PAYOFF-B reference interval = 0.284
```

The quadratic centered model is not a useful optimum estimator: its curvature is non-significant and places the formal vertex far above the order-one range.

## Species-level heterogeneity

A within-species quadratic diagnostic could be fit for 41 species.

```text
positive curvature = 16 / 41
finite vertex inside that species' observed 5–95% q support = 11 / 41
positive-curvature p < 0.1 = 1 / 41
median u* among supported internal vertices = 1.913
fraction of those vertices inside 1 .. 1.606115 = 4 / 11 = 0.364
```

The one species with positive curvature at `p<0.1` in this exploratory diagnostic is `Vireo_olivaceus`:

```text
u* = 1.343
p(curvature) = 0.0524
N = 274
```

This species-level scan is a heterogeneity diagnostic, not a multiple-testing discovery exercise.

## Current interpretation

Stage 1 does **not** establish a universal natural constant matching the exact PAYOFF-B optimum.

It does establish a more useful empirical direction:

> The order-one timescale-matching signal appears when mismatch is defined relative to the locally realized species-specific phenological phase, but the location and strength of that minimum are highly heterogeneous.

That shifts the macroecological question from

```text
"Is u* universally 1–1.606?"
```

to

```text
"Under which ecological conditions does a finite order-one movement–phenology
matching optimum emerge, sharpen, or disappear?"
```

The leading candidate moderators are directional alignment, phenological predictability, route geometry, migration strategy, movement capacity, and the degree to which local resource timing is an informative cue.

## Claim ceiling

Licensed now:

- the Amaral dataset contains a strong population-front tracking geometry, with median directional alignment about `0.95`;
- raw absolute mismatch and baseline-centered mismatch produce different optimum locations;
- the baseline-centered flexible GAM has order-one point minima, including `u=1.397` under perfect directional alignment;
- uncertainty and species-level heterogeneity are too large to claim a universal PAYOFF-B constant.

Not licensed:

- global validation of the exact `1 .. 1.606115` interval;
- an evolutionary optimum;
- a fitness optimum;
- causal evidence that speed-ratio matching itself reduces demographic loss;
- extension of the exact two-patch uniqueness theorem to a moving continuous phenology wave.

## Next empirical gate

The macro programme advances only if the order-one minimum becomes reproducible when evidence is broadened in one of two ways:

1. **global bird replication:** eBird Status weekly timing surfaces × MCD12Q2 phenology, testing spatial/species heterogeneity and moderators;
2. **individual cross-taxon replication:** Movebank trajectories × remotely sensed phenology, testing movement/green-wave matching without relying on population-front timing surfaces.

A global average alone is no longer the target. The target is an explanatory model for **when timescale matching emerges**.
