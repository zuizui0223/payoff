# PAYOFF-B V5 novelty audit — 2026-10-03

Status: **PREOUTCOME NOVELTY BOUNDARY; focal comparative outcomes unopened**

## Question being audited

V5 asks:

> **Where in the annual cycle do migratory birds absorb temporal delays, and
> what predicts when those delays persist?**

The common estimand is the unstandardized stage-to-stage timing propagation
coefficient

[
d_B = a + \beta_{AB} d_A + \varepsilon,
]

where (\beta_{AB}) is interpreted in days of downstream timing deviation per
one day of upstream timing deviation.

The novelty claim is **not** that temporal buffering, domino effects, annual
cycle resets, or the day-for-day slope itself are new.

The only candidate contribution is:

> a comparative synthesis that places **biologically different sequential
> annual-cycle transitions** on the same day-for-day propagation scale and
> tests whether propagation differs systematically between active migration
> and stationary periods, and with available stationary time.

## High-priority prior art

### Schmaljohann 2019 — multi-species departure-to-arrival slopes

*Movement Ecology* 7:25.
DOI: 10.1186/s40462-019-0169-1.

- spring analysis: 17 species, 161 individuals;
- autumn analysis: 21 species, 241 individuals;
- start of migration was positively associated with arrival timing within and
  between species;
- species differed in slope strength;
- a one-day later start corresponded on average to about 0.4 d later arrival
  within species.

Boundary:

```text
DAY_FOR_DAY_DEPARTURE_TO_ARRIVAL_PROPAGATION = PRIOR_ART
MULTISPECIES_SPECIES_SPECIFIC_SLOPES = PRIOR_ART
CROSS_TRANSITION_CLASS_SYNTHESIS = NOT_DONE_IN_THIS_STUDY
```

V5 therefore cannot claim that departure-to-arrival retention, partial
compression, or species variation in that slope is newly discovered.

### van Bemmelen et al. 2024 — Arctic skua annual-cycle carry-over slopes

*Movement Ecology* 12:22.
DOI: 10.1186/s40462-024-00459-9.

This study explicitly quantifies compensation versus carry-over between
successive annual-cycle events using timing relationships and intervening
period durations across multiple breeding and wintering areas.

It also states that whether temporal carry-over is stronger for longer-distance
migrations and tighter annual schedules remains largely unresolved.

Boundary:

```text
STAGE_TO_STAGE_SLOPE_AS_CARRYOVER_STRENGTH = PRIOR_ART
STATIONARY_BUFFERING_HYPOTHESIS = PRIOR_ART
GEOGRAPHIC_TIME_CONSTRAINT_MODERATION = OPEN_WITHIN_FIELD
CROSS_STUDY_TRANSITION_CLASS_META_ANALYSIS = NOT_DONE_IN_THIS_STUDY
```

### Franklin et al. 2022 — repeatability meta-analysis

*Journal of Animal Ecology* 91:1416–1430.
DOI: 10.1111/1365-2656.13697.

- 177 repeatability effects;
- 54 papers;
- 47 species.

The estimand is ICC / repeatability of the same event across years, not
day-for-day propagation between consecutive events.

### Romano et al. 2023 — global circannual phenology meta-analysis

*Ecological Monographs* 93:e1552.
DOI: 10.1002/ecm.1552.

This synthesis quantifies long-term phenological shifts across annual-cycle
stages, not within-cycle propagation of individual/cohort timing deviation.

### Briedis et al. 2019 — multi-species full annual cycle

*Proceedings of the Royal Society B* 286:20182821.
DOI: 10.1098/rspb.2018.2821.

This comparative study shows that timing differences may persist through some
segments and disappear through others across multiple long-distance migrant
species. It is high-priority prior art for any transition-class claim.

### Wang et al. 2024 — global full-annual-cycle tracking compilation

*Nature Communications* 15:4111.
DOI: 10.1038/s41467-024-48248-7.

- 1,531 tracked individuals plus 177 population means;
- 186 species;
- four major annual-cycle migration events;
- pooled carry-over paths among successive timings.

This is the closest macro-scale competitor. V5 must not claim that multi-species
annual-cycle carry-over analysis is new.

### Weir & Phillimore 2024 — buffering perspective

*Global Change Biology* 30:e17294.
DOI: 10.1111/gcb.17294.

Phenological buffering and the need to identify buffer limits are prior art.

## Single-system prior art

Senner et al. 2014, Gow et al. 2019, Carneiro et al. 2023, Saino et al. 2017,
Conklin & Battley 2012, Catry et al. 2013, Briedis et al. 2018, black-tailed
godwit work and related studies already establish:

- domino effects;
- partial timing propagation;
- schedule reset;
- stationary-period compensation;
- stage-dependent persistence;
- links from annual-cycle timing to survival or reproduction in some systems.

These studies are potential effect-size sources, not discoveries to be
rebranded by PAYOFF-B.

## Search audit

Before opening focal V5 comparative outcomes, searches were run for
combinations of:

- timing propagation + migration + annual cycle;
- temporal buffering + migratory birds + meta-analysis;
- domino effects + migration timing + meta-analysis;
- annual-cycle timing + carry-over + meta-analysis;
- day-for-day migration timing slopes;
- annual schedule adjustment + comparative synthesis;
- migration timing retention + species comparison;
- carry-over slope + active migration + stationary period.

The search recovered the prior syntheses and slope-based studies above.

It did **not** recover a published quantitative synthesis whose primary
comparison places multiple biological transition classes on a common
unstandardized day-for-day propagation scale, nor a meta-regression of that
common estimand comparing stationary versus active migration transitions.

This is a search result, not proof of priority.

## Current novelty decision

```text
BUFFERING_EXISTS = PRIOR_ART
DOMINO_EFFECTS_AND_RESETS = PRIOR_ART
STATIONARY_PERIOD_COMPENSATION = PRIOR_ART
DAY_FOR_DAY_PROPAGATION_SLOPE = PRIOR_ART
MULTISPECIES_DEPARTURE_TO_ARRIVAL_SLOPES = PRIOR_ART
FULL_ANNUAL_CYCLE_MULTISPECIES_TIMING = PRIOR_ART
GLOBAL_CARRYOVER_PATH_MODELS = PRIOR_ART
REPEATABILITY_META_ANALYSIS = PRIOR_ART
LONG_TERM_PHENOLOGICAL_SHIFT_META_ANALYSIS = PRIOR_ART

CROSS_TRANSITION_CLASS_DAY_FOR_DAY_META_ANALYSIS = NOT_FOUND
STATIONARY_VS_ACTIVE_COMMON_ESTIMAND_TEST = NOT_FOUND
AVAILABLE_STATIONARY_TIME_COMMON_ESTIMAND_MODERATOR = NOT_FOUND

V5_NOVELTY_CLASS = PROSPECTIVE_COMPARATIVE_QUANTIFICATION
V5_NOVELTY_STATUS = PROVISIONALLY_DEFENSIBLE_BUT_HIGH_THREAT
```

## Allowed novelty wording

Allowed:

> Individual and multi-species studies already show that annual-cycle timing
> deviations can propagate, weaken or disappear, and day-for-day carry-over
> slopes have already been estimated. We found no comparative synthesis that
> places biologically different annual-cycle transitions on the same
> unstandardized propagation scale. We therefore test whether propagation
> differs systematically among transition types.

Not allowed:

- "We discovered temporal buffering."
- "We introduce timing retention / carry-over slopes."
- "We are the first to show that departure timing propagates to arrival."
- "We are the first to show species differ in departure-to-arrival retention."
- "We are the first to show stationary periods reset migration timing."
- "No multi-species study has examined carry-over effects."
- "This is the first full-annual-cycle comparative analysis."

## Duplicate-data rule

Many tracking datasets are reused across papers and syntheses.

V5 must identify the underlying individual/cohort dataset for every effect.
If two publications reuse the same tracked individuals for the same transition,
only one effect enters the primary synthesis unless the samples are
non-overlapping and this can be documented.

Priority is:

1. raw individual-level re-estimation under the V5 estimand;
2. directly reported unstandardized transition slope;
3. figure-reconstructed unstandardized slope, sensitivity only.

A slope from a secondary synthesis must not be counted in addition to its
underlying primary dataset.

## Fail-closed rule

V5 proceeds only if the eligible corpus supports the declared transition-class
comparison without changing the estimand.

Do not rescue sample size by:

- converting correlations or repeatabilities into (\beta_{AB});
- treating standardized path coefficients as day-for-day slopes;
- adding non-migratory taxa to the primary analysis;
- reclassifying MIXED transitions after seeing effect sizes;
- treating population means as within-individual propagation;
- double-counting reused tracking datasets.

If the admission gate fails, the V5 result is **INSUFFICIENT_CORPUS**.
