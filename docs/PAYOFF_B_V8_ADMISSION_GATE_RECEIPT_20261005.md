# PAYOFF-B V8 admission-gate receipt — 2026-10-05

Status: **PASS; PRIMARY ENVIRONMENTAL OUTCOME STILL UNOPENED AT GATE FREEZE**

Contract:
`docs/PAYOFF_B_V8_PREDICTIVE_CONNECTIVITY_DEGRADATION_CONTRACT_20261005.md`

Frozen source:
- Amaral et al. BirdMigrationSpeed;
- source commit `62c58d77c2028bd863dfe3697b0d9cf29ceaeab0`;
- source-target mapping rule unchanged from the 2026-09-26 predictive-connectivity analysis.

Primary windows:
- EARLY = 2002–2009;
- LATE = 2010–2017;
- minimum paired annual green-up observations per window = 6.

The outcome-blind gate script constructed the frozen source-target mapping and
counted paired green-up years only. It did **not** calculate an early-window
correlation, late-window correlation, correlation change, sign reversal or
species direction.

## Gate result

```text
FROZEN_MAPPINGS_TOTAL = 842
ELIGIBLE_PAIRS_BOTH_WINDOWS = 393
ELIGIBLE_SPECIES = 28
SPECIES_WITH_AT_LEAST_3_ELIGIBLE_PAIRS = 26

REQUIRED_PAIRS = 100
REQUIRED_SPECIES = 20
REQUIRED_SPECIES_WITH_3_PAIRS = 15

V8_ADMISSION_GATE = PASS
```

All three admission requirements therefore pass without threshold relaxation.

## Outcome-access boundary

At the moment this gate was frozen:

```text
EARLY_RHO = UNOPENED
LATE_RHO = UNOPENED
DELTA_RHO = UNOPENED
NEGATIVE_SPECIES_COUNT = UNOPENED
SIGN_REVERSALS = UNOPENED
V8_PRIMARY_SUPPORT = UNOPENED
```

The next valid step is the frozen primary V8 environmental analysis.
