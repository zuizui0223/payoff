# PAYOFF-B V5 post-first-open corpus stability rule — 2026-10-03

Status: **POST-FIRST-OPEN CONSERVATIVE STOP RULE**

## Timing and transparency

This rule was written **after** the first six admissible V5 effects from three
studies had been extracted and recorded on main.

It is therefore **not a preregistration** and is not added retroactively to the
frozen preoutcome contract.

At the time this rule was written:

```text
OPENED_PRIMARY_EFFECTS = 6
OPENED_STUDIES = 3
ACTIVE_MIGRATION_EFFECTS = 3
STATIONARY_EFFECTS = 3
H1_RUN = NO
H2_RUN = NO
POOLED_COMPARATIVE_RESULT = NONE
```

The purpose is only to prevent an underpowered, pseudoreplicated comparative
claim from being generated from a handful of effects.

## Conservative H1 stability rule

Do not run or interpret the primary stationary-versus-active comparison unless
the primary corpus contains all of:

- at least 20 admissible beta_AB effects;
- at least 10 unique underlying tracked datasets/cohorts overall;
- at least 5 unique underlying datasets contributing a STATIONARY transition;
- at least 5 unique underlying datasets contributing an ACTIVE_MIGRATION
  transition.

Multiple effects from one study do not satisfy the independent-dataset count.

## Conservative H2 stability rule

Do not run or interpret the available-stationary-time moderator unless there are:

- at least 10 admissible stationary-transition effects;
- at least 5 unique underlying tracked datasets/cohorts;
- interval duration reported or derivable independently of the focal beta_AB
  value.

## Why these are not outcome gates

These rules do not depend on the sign, significance or magnitude of the six
opened effects.

They only govern whether the corpus has enough independent biological sources
to support the proposed comparative model.

The thresholds may not be lowered later to rescue a sparse corpus.

## Duplicate-data rule

The independence unit is the underlying tracked individuals/cohort, not the
paper.

Multi-species reanalyses, global compilations and primary species papers can
reuse the same animals. When overlap is documented, count the underlying
dataset once for the relevant transition.

Preferred effect source:

1. raw individual data re-estimated under the V5 day-for-day definition;
2. directly reported unstandardized primary-study slope;
3. figure-reconstructed slope only as a sensitivity analysis.

## Interpretation

Passing this rule does **not** establish novelty or biological support for H1
or H2. It only licenses fitting the prespecified comparative model.

Failure yields:

```text
V5_COMPARATIVE_STATE = INSUFFICIENT_INDEPENDENT_CORPUS
```

with no post hoc lowering of the rule.
