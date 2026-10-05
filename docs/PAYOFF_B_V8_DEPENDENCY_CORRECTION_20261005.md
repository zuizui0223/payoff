# PAYOFF-B V8 preoutcome dependency correction — 2026-10-05

Status: **DESIGN CORRECTION AFTER ADMISSION GATE, BEFORE FOCAL OUTCOME ACCESS**

## Timing

The original V8 contract and the outcome-blind admission gate were frozen before
any early-window correlation, late-window correlation or correlation change was
calculated.

After the admission gate passed, the frozen source-target mapping was audited
for exact reuse of the same environmental source-target cell pair across
species.

At this point:

```text
EARLY_RHO = UNOPENED
LATE_RHO = UNOPENED
DELTA_RHO = UNOPENED
V8_PRIMARY_SUPPORT = UNOPENED
```

## Dependency audit

Among the 393 eligible species-by-pair mapping rows:

```text
ELIGIBLE_SPECIES_BY_PAIR_ROWS = 393
UNIQUE_SPATIAL_SOURCE_TARGET_PAIRS = 166
SPATIAL_PAIRS_SHARED_BY_MORE_THAN_ONE_SPECIES = 81
ROWS_BELONGING_TO_SHARED_SPATIAL_PAIRS = 308
MAX_SPECIES_SHARING_ONE_SPATIAL_PAIR = 13
ELIGIBLE_SPECIES = 28
```

The environmental correlation for a given source cell and target cell is the
same object regardless of how many species use that spatial pair.

Therefore treating all 393 species-by-pair rows as independent or clustering
only by species would replicate identical environmental outcomes and
understate dependence.

## Corrected primary inferential unit

The primary environmental unit is now the **unique spatial source-target pair**.

For each unique pair (p), calculate exactly one:

[
Deltaho_p
=
ho^{late}_p-ho^{early}_p.
]

Species labels remain biologically important because they define which spatial
pairs enter the ecologically relevant sample. They are represented in a
separate incidence table linking each unique pair to all species using that
pair.

## Two complementary estimands

### 1. Spatial-pair estimand

[
ar{Deltaho}_{pair}
=
rac{1}{P}sum_pDeltaho_p.
]

This weights each unique environmental relationship once.

### 2. Equal-species exposure estimand

For species (j), calculate the mean (Deltaho) across its eligible unique
spatial pairs, then average those species means:

[
ar{Deltaho}_{species}
=
rac{1}{J}sum_joverline{Deltaho}_j.
]

This prevents species represented by many breeding cells from automatically
dominating the biological summary.

Neither estimand treats duplicated species-by-pair rows as independent
environmental observations.

## Dependency-aware uncertainty

Primary bootstrap:

```text
BOOTSTRAP_UNIT = UNIQUE_SPATIAL_PAIR
BOOTSTRAP_REPLICATES = 10000
BOOTSTRAP_SEED = 20261005
```

Each bootstrap sample resamples unique spatial pairs with replacement.

For the equal-species summary, a sampled spatial pair carries its full frozen
species-incidence set into the replicate. Species means are recomputed from the
sampled pair incidences. This preserves the fact that several species can share
the same environmental relationship.

## Corrected support rule

V8 supports broad degradation only if all are true:

1. (ar{Deltaho}_{pair}<0);
2. the 95% unique-spatial-pair bootstrap interval for
   (ar{Deltaho}_{pair}) excludes zero;
3. (ar{Deltaho}_{species}<0);
4. the dependency-aware bootstrap interval for
   (ar{Deltaho}_{species}) excludes zero.

The number and fraction of species with negative species means are still
reported descriptively, but the original one-sided binomial sign test is
removed from the support rule because species means share underlying spatial
pairs and are not independent Bernoulli trials.

## Admission gate under the corrected unit

The original gate required at least 100 pair mappings, 20 species and 15
species with at least three eligible mappings.

After exact spatial deduplication:

```text
UNIQUE_ELIGIBLE_SPATIAL_PAIRS = 166
ELIGIBLE_SPECIES = 28
SPECIES_WITH_AT_LEAST_3_ELIGIBLE_PAIRS = 26
```

Thus the admission gate still passes without relaxing any threshold.

## Claim boundary

This correction does not alter the biological question, environmental windows,
detrending procedure, source-target mapping, or directional hypothesis.

It only prevents pseudoreplication of an environmental quantity that is exactly
shared by multiple species.

No focal V8 outcome was inspected in making this correction.
