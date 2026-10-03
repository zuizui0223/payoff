# PAYOFF-B V5 first-effect opening receipt — 2026-10-03

Status: **PARTIAL EXTRACTION; COMPARATIVE MODEL NOT RUN**

The V5 extraction contract was frozen before focal timing-propagation effects
were opened. This receipt records the first admissible primary effects without
testing H1 or H2.

## Frozen contract

`data/payoff_b_buffer_limits_meta_contract_20261003.json`

Primary estimand:

[
d_B=a+eta_{AB}d_A+arepsilon.
]

No repeatability or correlation coefficient is converted into (eta_{AB}).

## Opened primary effects

Current effect file:

`data/payoff_b_buffer_limits_effects_v0_1_20261003.csv`

```text
STUDIES_WITH_OPENED_EFFECTS = 3
PRIMARY_EFFECTS_OPENED = 6
ACTIVE_MIGRATION_EFFECTS = 3
STATIONARY_EFFECTS = 3
H1_MODEL_RUN = NO
H2_MODEL_RUN = NO
POOLED_EFFECT_REPORTED = NO
```

### SENNER2014 — Hudsonian godwit

- active autumn migration:
  Buenos Aires departure -> Chiloé arrival,
  beta = 0.97, SE = 0.07;
- non-breeding stationary period:
  Chiloé arrival -> Chiloé departure,
  beta = 0.05, SE = 0.09.

### CONKLIN2012 — bar-tailed godwit

Two within-subject non-breeding timing transitions from Table 3:

- New Zealand arrival -> primary-moult initiation,
  beta = 1.00, SE = 0.10;
- end of pre-basic moult -> primary-moult initiation,
  beta = 0.23, SE = 0.10.

The non-significant arrival -> spring-departure relationship is not coded as
beta = 0 because the raw coefficient was not reported.

### BRIEDIS_SPRINT2018 — collared flycatcher

Direct departure-to-arrival regressions:

- autumn migration:
  beta = 0.49, SE = 0.13;
- spring migration:
  beta = 0.20, SE = 0.12.

Migration-speed regressions remain mechanistic anchors rather than primary
timing-propagation effects.

## Why no comparative conclusion is opened yet

The six effects come from only three studies, with two effects per study.
Treating them as six independent observations would create pseudoreplication.

The declared multilevel comparison therefore remains unopened until the corpus
contains enough independent studies/transitions to estimate study-level
dependence meaningfully.

No statement such as "stationary periods buffer more" is licensed by this
receipt.

## Public raw-data lanes

Three additional studies passed design admission for re-estimation from public
individual-level data:

- GOW2019 tree swallow;
- CARNEIRO2023 Icelandic whimbrel;
- LOPEZCALDERON2024 barn swallow.

Their repositories are public, but direct binary/file retrieval is currently
blocked in the active execution environment. This is recorded as an access
state, not as an analytical failure.

```text
GOW2019 = PUBLIC_FETCH_PENDING
CARNEIRO2023 = PUBLIC_FETCH_PENDING
LOPEZCALDERON2024 = PUBLIC_FETCH_PENDING
```

No published path coefficient is substituted merely because the raw file could
not be fetched here.

## Current boundary

The next valid step is corpus expansion, not interpretation.

The first formal V5 comparative model can be run only after:
- additional independent primary effects are admitted or re-estimated;
- dependence structure is encoded by study/species/cohort;
- transition classes remain those frozen before outcome opening.

