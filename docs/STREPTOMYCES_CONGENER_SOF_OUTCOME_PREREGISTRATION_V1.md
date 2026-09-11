# Streptomyces congener separation-of-function outcome preregistration v1

Lane: **A task/mechanism separation sublane only**.

This document freezes the interpretation rule for the two pre-outcome congener candidates:

```text
C1 = delta redG congener partition
C2 = delta redG + mcpG cyclic-congener swap
```

It does not claim that either candidate has passed task preservation, genotoxicity, direct-mu, separation-of-function, matched-S, or architecture mapping.

## 1. What is frozen now

The **logical outcome map** is frozen before task/genotoxic/direct-mu outcomes are opened.

The numerical materiality thresholds are **not yet frozen**, because the final assay scales have not yet been selected. They must be declared after the measurement scales are fixed but before any outcome values are opened.

Therefore the current state is deliberately:

```text
RULE_FROZEN_PREOUTCOME = TRUE
NUMERIC_THRESHOLDS_FROZEN = FALSE
OUTCOME_OPENING_ALLOWED = FALSE
OUTCOME_DATA_OPENED = FALSE
```

This prevents a nominal preregistration in which the qualitative rule is declared early but the decisive threshold is chosen after seeing the data.

## 2. C1: task-preservation rule

Let

```text
delta_task = performance_probe - performance_control
```

on a predeclared scale where larger values are better for the focal ecological task. Let `epsilon_task >= 0` be the largest predeclared material task loss that is acceptable.

Task preservation is certified only if the entire closed uncertainty band lies **strictly above** `-epsilon_task`.

```text
lower(delta_task) > -epsilon_task
    -> preserved

upper(delta_task) < -epsilon_task
    -> material_task_loss

otherwise
    -> unresolved
```

Boundary contact is unresolved. A non-significant difference is not automatically task preservation.

The task itself must be fixed before outcome opening; pigment amount or prodiginine presence is not a substitute for the focal ecological performance measure.

## 3. C2: genotoxicity + direct-mu branch

Two separate positive-oriented reductions are required:

```text
R_genotoxic = control - probe
R_mu        = control_mu - probe_mu
```

Each is classified against its own predeclared material-reduction threshold using the same strict closed-band rule:

```text
entire band strictly above threshold -> reduced
entire band strictly below threshold -> material_reduction_excluded
contact / straddle                  -> unresolved
```

The direct-mu estimate must come from `STREPTOMYCES_DIRECT_MU_MEASUREMENT_CONTRACT_V1`, not from final recoverable mutant frequency alone.

Joint C2 status is then:

```text
genotoxicity reduced + mu reduced
    -> genotoxic_generation_reduced

both material reductions excluded
    -> registered_route_not_supported

one reduced + one excluded
    -> genotoxic_mu_discordant

any unresolved
    -> unresolved
```

This prevents a change in DNA-damage proxy alone from being called a differentiation-generation result, and prevents a mu change without the registered genotoxic branch from being called the proposed congener mechanism.

## 4. Frozen C1 x C2 outcome matrix

| Task branch | Genotoxic/direct-mu branch | Registered interpretation |
|---|---|---|
| preserved | genotoxic_generation_reduced | `SEPARATION_OF_FUNCTION_SUPPORTED` |
| preserved | registered_route_not_supported | `TASK_PRESERVED_REGISTERED_GENOTOXIC_GENERATION_ROUTE_NOT_SUPPORTED` |
| material task loss | genotoxic_generation_reduced | `MECHANISM_SIGNAL_PRESENT_BUT_TASK_CONFOUNDED` |
| material task loss | registered_route_not_supported | `CANDIDATE_FAILS_TASK_AND_REGISTERED_ROUTE_CRITERIA` |
| any | genotoxic_mu_discordant | `GENOTOXIC_MU_DISCORDANCE_SOF_UNRESOLVED` |
| unresolved | any, or any | unresolved | `INCOMPLETE_OR_UNRESOLVED_SOF` |

The key anti-cherry-picking distinction is the third row. A congener perturbation may reduce genotoxicity and direct mu yet still fail as a separation-of-function architecture route because the focal task was materially lost.

## 5. Thresholds that still must be frozen

Before any outcome is opened, the programme must record numerical values for:

```text
TASK_MATERIAL_LOSS_TOLERANCE
GENOTOXICITY_MATERIAL_REDUCTION_THRESHOLD
DIRECT_MU_MATERIAL_REDUCTION_THRESHOLD
```

and must identify the exact assay scale, normalization, direction, time window, and uncertainty construction for each.

Until then the candidate outcomes remain:

```text
delta redG       -> unresolved
delta redG+mcpG  -> unresolved
```

## 6. What a positive C3 result would mean

A candidate passing task preservation plus the joint genotoxic/direct-mu branch would support a **separation-of-function result at the congener-probe level**:

```text
focal ecological task retained
while
registered genotoxic/differentiation-generation branch is reduced.
```

This would be a materially stronger result than a full RED knockout mechanism probe.

It still would not automatically establish:

```text
matched generalist/shared architecture
same-unit S:D architecture pair
full architecture mapping
frequency-dependent architecture fitness
eta
E1
```

Those downstream promotions remain blocked by the independent matched-comparator and mechanism-to-architecture gates.

## 7. Current status

```text
PRIMARY_CONGENER_CANDIDATES_FROZEN = TRUE
QUALITATIVE_OUTCOME_RULE_FROZEN = TRUE
NUMERIC_THRESHOLDS_FROZEN = FALSE
OUTCOME_OPENING_ALLOWED = FALSE
SEPARATION_OF_FUNCTION_SUPPORTED_COUNT = 0
MATCHED_GENERALIST_SHARED_ARCHITECTURE_RECOVERED = FALSE
MATCHED_S_CERTIFIED = FALSE
ARCHITECTURE_MAPPING_CERTIFIED = FALSE
PAYOFF_ARCHITECTURE_FREQUENCY_FEEDBACK_IDENTIFIED = FALSE
```
