# PAYOFF-B V5 novelty audit — 2026-10-03

Status: **PREOUTCOME NOVELTY BOUNDARY; focal comparative outcomes unopened**

## Question being audited

V5 asks:

> **Where in the annual cycle do migratory birds absorb temporal delays, and
> what predicts when those delays persist?**

The proposed common estimand is the unstandardized stage-to-stage timing
propagation coefficient

[
d_B = a + eta_{AB} d_A + arepsilon,
]

where (eta_{AB}) is interpreted in days of downstream timing deviation per
one day of upstream timing deviation.

The novelty claim under review is **not** that temporal buffering, domino
effects, or annual-cycle resets exist. Those are established prior art.

The only candidate novelty is:

> a comparative synthesis that places sequential annual-cycle transitions from
> multiple migratory-bird systems on the same day-for-day propagation scale and
> tests whether propagation differs systematically between active migration and
> stationary periods, and with available stationary time.

## Prior syntheses checked

### Franklin et al. 2022 — repeatability meta-analysis

*Journal of Animal Ecology* 91:1416–1430.
DOI: 10.1111/1365-2656.13697.

- screened 2,433 studies;
- synthesized 177 repeatability effects from 54 papers and 47 species;
- compared repeatability of migration timing across annual-cycle events.

The estimand is ICC / repeatability of the **same event across repeated years**.
It does not estimate stage-to-stage day-for-day propagation from event A to
event B within an annual cycle.

Boundary:

```text
OVERLAP = ANNUAL_CYCLE_TIMING_COMPARATIVE_SYNTHESIS
SAME_ESTIMAND = NO
V5_ROLE = CORPUS_SOURCE_AND_METHOD_BOUNDARY
```

### Romano et al. 2023 — global circannual phenology meta-analysis

*Ecological Monographs* 93:e1552.
DOI: 10.1002/ecm.1552.

- >5,500 time series;
- 684 bird species;
- synthesized long-term phenological shifts across prebreeding migration,
  breeding and postbreeding migration.

The estimand is temporal change in phenophase timing, e.g. days per year or
decade. It does not quantify within-individual or paired-cohort propagation of
a timing deviation from one consecutive stage to the next.

Boundary:

```text
OVERLAP = PHENOLOGY_ACROSS_CIRCANNUAL_STAGES
SAME_ESTIMAND = NO
V5_ROLE = GLOBAL_CHANGE_CONTEXT
```

### Briedis et al. 2019 — multi-species full annual cycle

*Proceedings of the Royal Society B* 286:20182821.
DOI: 10.1098/rspb.2018.2821.

- >350 complete annual migration tracks;
- multiple Afro-Palaearctic long-distance migrant species;
- compared male/female timing through four major migration events;
- tested departure timing and migration duration as proximate causes of
  sex-biased arrival timing.

This is important comparative full-annual-cycle prior art and demonstrates that
timing differences can disappear in one season and persist in another.
However, the paper is organized around sex-biased migration timing, not a
meta-analytic map of transition-specific (eta_{AB}) across biological
transition classes.

Boundary:

```text
OVERLAP = MULTISPECIES_FULL_ANNUAL_TIMING_AND_DOMINO_EFFECTS
SAME_PRIMARY_QUESTION = NO
SAME_COMMON_ESTIMAND = NO
V5_ROLE = HIGH_PRIORITY_PRIOR_ART_AND_POSSIBLE_CORPUS_SOURCE
```

### Wang et al. 2024 — global full-annual-cycle tracking compilation

*Nature Communications* 15:4111.
DOI: 10.1038/s41467-024-48248-7.

- 1,531 tracked individuals and 177 population means;
- 186 species;
- four key annual-cycle migration events;
- Bayesian phylogenetic SEM included carry-over paths from earlier to later
  timing;
- primary goal was to explain migration timing using body mass, geography and
  migration distance.

This is the closest macro-scale competitor. It establishes that large,
multi-species full-annual-cycle timing compilations are feasible and explicitly
models earlier timing as a predictor of later timing.

V5 differs only if it retains its declared estimand and transition focus:
unstandardized day-for-day within-study propagation slopes, sequential
transition classification, and the stationary-versus-active buffering test.
V5 must not claim that no prior multi-species carry-over analysis exists.

Boundary:

```text
OVERLAP = GLOBAL_MULTISPECIES_FULL_ANNUAL_CYCLE_AND_CARRYOVER_PATHS
SAME_PRIMARY_QUESTION = NO
SAME_EFFECT_SIZE_SYNTHESIS = NO_EVIDENCE_FOUND
NOVELTY_THREAT = HIGH
V5_MUST_CITE_AND_DIFFERENTIATE_EXPLICITLY = YES
```

### Weir & Phillimore 2024 — buffering perspective

*Global Change Biology* 30:e17294.
DOI: 10.1111/gcb.17294.

This perspective argues that phenological asynchrony and its fitness
consequences can be buffered and shifts attention toward buffering mechanisms
and their limits.

Therefore V5 cannot claim novelty for:
- the concept of phenological buffering;
- asking whether buffers exist;
- arguing that buffer limits matter.

Its possible contribution is empirical quantification of one specific form of
buffering in migratory annual cycles.

### Single-system annual-cycle studies

Senner et al. 2014, Gow et al. 2019, Carneiro et al. 2023, Briedis et al. 2018,
Saino et al. 2017, Conklin & Battley 2012, Catry et al. 2013 and related work
already show:
- domino effects;
- partial propagation;
- schedule reset;
- stationary-period compensation;
- stage-dependent persistence of timing deviations.

These studies establish the biological phenomenon. They are potential
effect-size sources, not discoveries to be rebranded by PAYOFF-B.

## Search audit

Before opening focal V5 comparative outcomes, searches were run for combinations
of:

- timing propagation + migration + annual cycle;
- temporal buffering + migratory birds + meta-analysis;
- domino effects + migration timing + meta-analysis;
- annual-cycle timing + carry-over + meta-analysis;
- day-for-day migration timing slopes;
- annual schedule adjustment + comparative synthesis.

The searches recovered the syntheses and primary studies above but did **not**
recover a published meta-analysis whose primary effect size is the
stage-to-stage unstandardized timing-propagation slope (eta_{AB}), nor a
published comparison of that common estimand between stationary and active
migration transitions.

This is a **search result, not proof of priority**. The claim must remain
"we found no prior quantitative synthesis using this estimand" unless a formal
systematic novelty search is completed and documented for submission.

## Current novelty decision

```text
BUFFERING_EXISTS = PRIOR_ART
DOMINO_EFFECTS_AND_RESETS = PRIOR_ART
STATIONARY_PERIOD_COMPENSATION = PRIOR_ART
FULL_ANNUAL_CYCLE_MULTISPECIES_TIMING = PRIOR_ART
GLOBAL_CARRYOVER_PATH_MODELS = PRIOR_ART
REPEATABILITY_META_ANALYSIS = PRIOR_ART
LONG_TERM_PHENOLOGICAL_SHIFT_META_ANALYSIS = PRIOR_ART

COMMON_DAY_FOR_DAY_TRANSITION_PROPAGATION_META_ANALYSIS = NOT_FOUND
STATIONARY_VS_ACTIVE_PROPAGATION_TEST = NOT_FOUND
AVAILABLE_STATIONARY_TIME_MODERATOR = NOT_FOUND

V5_NOVELTY_CLASS = PROSPECTIVE_COMPARATIVE_QUANTIFICATION
V5_NOVELTY_STATUS = PROVISIONALLY_DEFENSIBLE
```

## Allowed novelty wording

Allowed:

> Individual studies have shown that annual-cycle timing deviations can
> propagate, weaken or disappear. We found no comparative synthesis that places
> these transitions on a common day-for-day propagation scale. We therefore
> test whether the persistence of timing deviations differs systematically
> among annual-cycle transition types.

Not allowed:

- "We discovered temporal buffering."
- "We are the first to show that stationary periods reset migration timing."
- "No multi-species study has examined carry-over effects."
- "No previous synthesis has compared migration timing across the annual
  cycle."
- "This is the first full-annual-cycle comparative analysis."

## Fail-closed rule

V5 proceeds only if the eligible literature yields enough independent raw-slope
effects to estimate the declared comparison without changing the estimand.

Do not rescue sample size by:
- converting correlations or repeatabilities into (eta_{AB});
- switching to standardized coefficients after seeing the corpus;
- adding non-migratory taxa to the primary analysis;
- reclassifying MIXED transitions after seeing effect sizes;
- using population means as if they were within-individual propagation slopes.

If the corpus is too small, the primary V5 result is **INSUFFICIENT_CORPUS**,
not a new post hoc question.
