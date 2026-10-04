# PAYOFF-B V5 corpus-capacity audit — 2026-10-04

Status: **PRE-MODEL CAPACITY AUDIT; H1/H2 UNOPENED**

This audit asks only whether the frozen V5 stability gate appears reachable
without changing the estimand or relaxing admission rules.

## Frozen gate

H1 remains closed unless the final primary corpus contains:

- >=20 admissible `beta_AB` effects;
- >=10 unique underlying tracked datasets/cohorts;
- >=5 unique datasets contributing a STATIONARY transition;
- >=5 unique datasets contributing an ACTIVE_MIGRATION transition.

H2 remains closed unless there are:

- >=10 admissible stationary effects;
- >=5 unique stationary datasets/cohorts;
- independently reported/derivable interval duration.

## Current opened corpus

Numerical outcomes remain exactly:

```text
OPENED_EFFECTS = 6
OPENED_UNIQUE_DATASETS = 3
OPENED_ACTIVE_DATASETS = 2
OPENED_STATIONARY_DATASETS = 2
H1 = NOT_RUN
H2 = NOT_RUN
```

The three opened biological datasets are:
- SENNER2014;
- CONKLIN2012;
- BRIEDIS_SPRINT2018.

## Admitted raw-data / individual-table candidates

The current seed ledger contains the following independent candidates for
re-estimation under the frozen V5 day/day definition:

- GOW2019 — tree swallow;
- LEMKE2013 — great reed warbler;
- JAHN2013 — distinct Tyrannus species/breeding cohorts;
- OUWEHAND2017 — Dutch pied flycatcher;
- SAINO2017 — barn swallow;
- CARNEIRO2023 — Icelandic whimbrel;
- LOPEZCALDERON2024 — barn swallow.

JAHN2013 can contribute more than one independence unit only when each
species-by-breeding cohort separately passes the final sample/missingness
screen. Paper count is never substituted for biological-cohort count.

## Prospective class capacity

Without opening any new beta value, the biological designs indicate that the
active-migration side is likely capable of exceeding five independent
datasets if raw extraction succeeds:

- SENNER2014;
- BRIEDIS_SPRINT2018;
- LEMKE2013;
- OUWEHAND2017;
- one or more JAHN2013 Tyrannus cohorts;
- with additional possible active transitions in CARNEIRO2023,
  SAINO2017 and LOPEZCALDERON2024.

The stationary side is narrower but also plausibly reaches five independent
datasets if the already-admitted public re-estimations succeed:

- SENNER2014;
- CONKLIN2012;
- GOW2019;
- CARNEIRO2023;
- LOPEZCALDERON2024;
- with additional possible stationary/pre-breeding transitions in SAINO2017.

These are **capacity candidates, not counted gate passes**.

## Effect-count capacity

The current six opened effects plus the multiple sequential transitions
available in GOW2019, CARNEIRO2023 and LOPEZCALDERON2024 make the 20-effect
threshold plausible. However, no effect is counted until:

1. the exact paired event dates are obtained;
2. the transition class is fixed without looking at beta;
3. the common day/day model is fitted;
4. duplicate underlying animals/cohorts are ruled out.

## Main bottleneck

The present bottleneck is no longer absence of relevant ecology.

It is **safe extraction of compatible unstandardized effects from independent
biological datasets**, especially public XLS/XLSX/CSV archives that are
available at Dryad/Zenodo but are not materialized by the current execution
environment.

This is an access state, not evidence for or against H1/H2.

## Decision

```text
V5_H1_CAPACITY = PROVISIONALLY_FEASIBLE
V5_H2_CAPACITY = PROVISIONALLY_FEASIBLE_BUT_STATIONARY_LIMITED
V5_STABILITY_GATE = NOT_YET_PASSED
V5_H1_MODEL = DO_NOT_RUN
V5_H2_MODEL = DO_NOT_RUN
PRIMARY_BOTTLENECK = RAW_EFFECT_EXTRACTION_AND_DEDUPLICATION
```

The correct next step is therefore continued corpus extraction and
deduplication, not model fitting and not theory revision.
