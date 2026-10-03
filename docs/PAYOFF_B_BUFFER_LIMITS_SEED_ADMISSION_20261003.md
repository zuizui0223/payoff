# PAYOFF-B V5 seed-study admission ledger — 2026-10-03

Status: **eligibility screen only; focal comparative effect sizes not yet extracted**

This ledger applies the frozen V5 contract in
`data/payoff_b_buffer_limits_meta_contract_20261003.json` before numerical
`beta_AB` values are entered into the comparative corpus.

## Admission principle

The primary corpus requires an unstandardized day-for-day transition slope
between two ordered annual-cycle timing events, either reported directly with
uncertainty or estimable from individual-level data.

Correlation, repeatability and qualitative statements about "reset" are not
converted into `beta_AB`.

## SENNER2014 — Hudsonian godwit

Source:
Senner NR et al. 2014. *PLoS ONE* 9:e86588.
DOI 10.1371/journal.pone.0086588.

Design audit:
- 26 tracked adults; 43 complete and 13 partial tracks across 2009–2012;
- individual arrival/departure timing was expressed relative to year-specific
  population schedules;
- sequential mixed models were fitted to relative timing and to the change in
  timing deviation between stages;
- individual and year were random effects;
- breeding success and return were analysed separately.

Admission status:

```text
PRIMARY_STATUS = CONDITIONAL_REPORTED_SLOPE
INDIVIDUAL_LEVEL_DESIGN = YES
COMMON_DAY_UNITS = YES
YEAR_ADJUSTMENT = YES
REPORTED_SEQUENTIAL_MODELS = YES
RAW_BETA_COMPATIBILITY = VERIFY_TABLE_2_3_PARAMETERIZATION
NUMERICAL_EXTRACTION = NOT_YET_OPENED
```

Reason for conditional status:
the published models are clearly sequential and use timing deviations in days,
but V5 must verify that the specific table coefficient used as `beta_AB`
represents a one-day A -> B propagation slope rather than a coefficient on the
authors' derived "rate of change" state.

## GOW2019 — tree swallow

Source:
Gow EA et al. 2019. *Proc. R. Soc. B* 286:20181916.
DOI 10.1098/rspb.2018.1916.
Dryad 10.5061/dryad.5v5b124.

Design audit:
- 133 individuals from 12 North American breeding populations;
- each bird was tracked for one annual cycle;
- individual breeding, departure, stopover, non-breeding and spring-return
  timing variables were analysed;
- the individual-level timing dataset is publicly archived on Dryad;
- published models include geography and distance moderators, but the raw data
  permit V5 to estimate the prespecified transition slope on a common scale.

Admission status:

```text
PRIMARY_STATUS = ADMIT_REESTIMATE_FROM_PUBLIC_INDIVIDUAL_DATA
INDIVIDUAL_LEVEL_DESIGN = YES
COMMON_DAY_UNITS = YES
PUBLIC_RAW_DATA = YES
TRANSITIONS = MULTIPLE
NUMERICAL_EXTRACTION = NOT_YET_OPENED
```

The V5 reanalysis must use the frozen centering and transition-class rules; it
must not select only the published "domino" links.

## CARNEIRO2023 — Icelandic whimbrel

Source:
Carneiro C et al. 2023. *The American Naturalist* 201:353–362.
DOI 10.1086/722566.
Dryad 10.5061/dryad.vt4b8gtv9.

Design audit:
- 38 individuals tracked across seven years;
- public `dataStationary.csv` contains individual identifier, tracking years,
  autumn departure, winter arrival, spring departure, spring arrival and
  subsequent laying date;
- stopover duration, spring migration duration and breeding outcomes are also
  available;
- dates are reported in day-of-year units.

Admission status:

```text
PRIMARY_STATUS = ADMIT_REESTIMATE_FROM_PUBLIC_INDIVIDUAL_DATA
INDIVIDUAL_LEVEL_DESIGN = YES
COMMON_DAY_UNITS = YES
PUBLIC_RAW_DATA = YES
TRANSITIONS = MULTIPLE
FITNESS_LAYER = PARTIAL
NUMERICAL_EXTRACTION = NOT_YET_OPENED
```

This is currently the cleanest seed for estimating both active-migration and
stationary-period propagation from a common individual dataset.

## SAINO2017 — barn swallow

Source:
Saino N et al. 2017. *Journal of Animal Ecology* 86:239–249.
DOI 10.1111/1365-2656.12625.

Design audit:
- annual-cycle timing and fecundity are linked;
- the accessible primary results report Pearson correlation coefficients among
  focal phenological events;
- the frozen V5 contract explicitly forbids converting correlation
  coefficients into raw day-for-day propagation slopes.

Admission status:

```text
PRIMARY_STATUS = EXCLUDE_PRIMARY_CORRELATION_ONLY
INDIVIDUAL_LEVEL_BIOLOGY = YES
REPORTED_RAW_BETA = NO_CONFIRMED
SECONDARY_CORRELATION_SYNTHESIS = ELIGIBLE
FITNESS_LAYER = ELIGIBLE
NUMERICAL_PRIMARY_EXTRACTION = PROHIBITED
```

This study can enter the separately declared secondary standardized-correlation
or fitness layer, but not the primary `beta_AB` synthesis unless a public
individual dataset or reported unstandardized slope is independently located.

## Current seed-screen tally

```text
SCREENED = 4
PRIMARY_ADMIT_REESTIMATE = 2
PRIMARY_CONDITIONAL = 1
PRIMARY_EXCLUDE_CORRELATION_ONLY = 1
FOCAL_BETA_VALUES_OPENED = 0
```

## Next screen

Before primary modelling, continue the same eligibility audit for:
- BRIEDIS2018;
- LOPEZCALDERON2024;
- ARCTIC_SKUA2024;
- BLACKTAILED2011;
- CATRY2013;
- CONKLIN2013.

The screen must record exclusions as actively as admissions.
