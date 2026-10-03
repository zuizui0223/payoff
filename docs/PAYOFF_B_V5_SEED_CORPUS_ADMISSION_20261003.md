# PAYOFF-B V5 seed-corpus admission audit — 2026-10-03

Status: **PREOUTCOME; focal beta_AB values not extracted**

## Purpose

Determine whether V5 has enough independent, admissible data to support its
primary transition-class comparison **before** opening focal day-for-day
propagation estimates.

The primary question is no longer whether timing slopes exist. Multi-species
departure-to-arrival slopes and stage-to-stage carry-over slopes are prior art.

The only candidate V5 contribution is a common-scale comparison across
biologically different annual-cycle transition classes.

## Fixed stability gate

Primary H1 (stationary versus active migration) opens only if the corpus contains:

- at least 20 admissible primary beta_AB effects;
- at least 10 unique underlying tracking/cohort datasets overall;
- at least 5 unique underlying datasets contributing to STATIONARY transitions;
- at least 5 unique underlying datasets contributing to ACTIVE_MIGRATION transitions.

H2 (available stationary time) opens only if there are:

- at least 10 admissible stationary-transition effects;
- from at least 5 unique underlying datasets;
- with interval duration reported or derivable without using beta_AB outcomes.

These are corpus-stability gates, not significance thresholds. They may not be
lowered after focal effects are opened.

## Prior-art correction

### Schmaljohann 2019

Already provides species-specific departure-to-arrival relationships across
17 spring and 21 autumn migrant species and reports partial compression on
average.

Therefore:

```text
DAY_FOR_DAY_DEPARTURE_TO_ARRIVAL_SLOPE = PRIOR_ART
MULTISPECIES_VARIATION_IN_THAT_SLOPE = PRIOR_ART
```

This paper can contribute effects or source datasets only after underlying
tracking samples are deduplicated.

### van Bemmelen et al. 2024 — Arctic skua

Already treats compensation versus carry-over across consecutive annual-cycle
events using timing relationships and intervening-period duration.

Therefore:

```text
STAGE_TO_STAGE_CARRYOVER_SLOPE = PRIOR_ART
STATIONARY_BUFFERING_HYPOTHESIS = PRIOR_ART
```

The paper itself states that whether carry-over is stronger under longer
migration distances / tighter schedules is still largely unresolved.

## Seed admission status

A machine-readable audit is frozen at:

`data/payoff_b_v5_seed_admission_audit_20261003.csv`.

### Confirmed public individual-level sources suitable for common-beta re-estimation

**Gow et al. 2019 — tree swallow**

Dryad DOI: 10.5061/dryad.5v5b124.

The public dataset contains full annual-cycle timing records from the tracked
tree swallows. It can in principle provide multiple annual-cycle transition
slopes under the V5 definition.

**Saino et al. 2017 — barn swallow**

Dryad DOI: 10.5061/dryad.12n6v.

Individual geolocator and reproductive data are public. Published analyses used
correlations/path models, so V5 must re-estimate only directly observable
day-scale transitions from the raw data; standardized path coefficients are not
admissible primary effects.

**Carneiro et al. 2023 — Icelandic whimbrel**

Dryad DOI: 10.5061/dryad.vt4b8gtv9.

The public data explicitly include autumn departure, autumn arrival, spring
departure, spring arrival, laying date, stopover duration and spring migration
duration at the individual-year level. This is a strong candidate source for
both migration and stationary transitions.

**López-Calderón et al. 2024 — barn swallow**

Dryad DOI: 10.5061/dryad.ghx3ffbxj.

The public dataset contains 35 individuals and five ordered migration dates:
departure from breeding colony, onset of autumn migration, arrival at wintering
area, onset of spring migration and arrival at breeding colony, linked to
reproductive outcomes. Raw dates can support direct V5 re-estimation.

### Conditional sources

**Senner et al. 2014 — Hudsonian godwit**

Sequential mixed models of relative timing deviation are published and tables
contain model/parameter estimates. Exact admissibility requires table-level
verification that the relevant predictor is an unstandardized preceding-stage
timing deviation on the same day scale.

**Briedis et al. 2018 — collared flycatcher**

Individual tracking exists in Movebank project 166151488, but the paper states
that data are available upon request. No V5 primary effect is admitted until
the accessible schema or a directly reported unstandardized slope is verified.

**van Bemmelen et al. 2024 — Arctic skua**

The paper reports 276 annual-cycle tracks from 155 individuals and gives
Movebank study IDs. It is both high-priority prior art and a possible effect
source, subject to access and deduplication.

**Conklin & Battley 2012 — bar-tailed godwit**

The same individuals link non-breeding arrival, moult and later departure, but
no primary V5 effect is admitted until an unstandardized transition slope or
raw individual records are verified.

### Not currently admissible as primary beta_AB effects

**Lourenço et al. 2011 — black-tailed godwit**

The published analysis emphasizes repeatability and correlations / lack of
domino effects. Correlations and repeatabilities are not converted to beta_AB.

**Catry et al. 2013 — Cory's shearwater**

The experiment provides treatment contrasts in annual-cycle timing and later
breeding consequences. A treatment contrast is not the continuous
stage-to-stage day-for-day propagation estimand.

**Franklin et al. 2022**

Repeatability meta-analysis; corpus-discovery source only.

**Weir & Phillimore 2024**

Conceptual buffering boundary; no primary effect.

**Wang et al. 2024**

Global corpus/discovery and possible raw-data source. Because it compiles many
previous studies, every extracted effect must be mapped back to its underlying
study/individual dataset before admission to avoid double counting.

## Duplicate-data risk

The unit of independence is the **underlying tracked individuals/cohort**, not
the publication.

This is especially important for:
- multi-species reanalyses such as Schmaljohann 2019;
- the Wang et al. 2024 global compilation;
- species/populations that appear in both dedicated annual-cycle papers and
  later syntheses.

When duplication is present, use one effect source in this order:

1. raw individual data re-estimated under the V5 definition;
2. directly reported unstandardized primary-study slope;
3. figure reconstruction for sensitivity only.

## Current decision

The primary corpus gate has **not yet passed**.

We have confirmed several strong raw-data sources, but have not yet demonstrated
the required number of independent datasets in both transition classes.

Therefore:

```text
V5_EFFECT_OUTCOME_STATE = UNOPENED
V5_H1_CORPUS_GATE = PENDING
V5_H2_CORPUS_GATE = PENDING
V5_PUBLICATION_CLAIM = NOT_YET_LICENSED
```

The next task is source-level screening and schema extraction, not effect-size
estimation.
