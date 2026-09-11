# Streptomyces direct deletion-generation measurement contract v1

Lane: **A mechanism-measurement sublane only**.

Status: **prospective / pre-outcome**.

This document does not report a new Streptomyces result. It defines what would have to be measured before the pre-registered RED/prodiginine two-probe triangulation can be adjudicated.

## 1. Current architecture status remains negative

PAYOFF has **not** recovered the required matched generalist/shared Streptomyces architecture.

```text
MATCHED_GENERALIST_SHARED_ARCHITECTURE_RECOVERED = FALSE
MATCHED_S_COMPARATOR_CERTIFIED = FALSE
ARCHITECTURE_MAPPING_CERTIFIED = FALSE
```

The RED/prodiginine two-probe programme is therefore a prospective **mechanism probe**, not a validated S:D architecture comparison.

## 2. Why final mutant frequency is insufficient

Let `G_t` and `D_t` denote chromosome-equivalent mass in an intact state and one **registered terminal-deletion state** at the start of an interval. The measurement model is

```text
G_(t+1) = (1 - mu) * g * G_t
D_(t+1) = d * D_t + mu * g * G_t
```

where

```text
mu = fraction of new intact-state output entering the registered deletion state
g  = realization of intact-state material over the interval
d  = realization of already-deleted material over the interval
r  = d/g.
```

A terminal-deletion fraction measured only at the end of the interval conflates `mu` with `r`.

With

```text
f_t = D_t / (G_t + D_t),
```

two state censuses and an independent `r` identify

```text
mu = f_(t+1) - r * f_t * (1 - f_(t+1)) / (1 - f_t).
```

This is an exact algebraic result **conditional on the registered two-state transition model**.

## 3. Exact uncertainty projection

For closed Cartesian bands

```text
f_t     in [f0L, f0H]
f_(t+1) in [f1L, f1H]
r       in [rL, rH],
```

`mu` is decreasing in `f_t` and `r`, and increasing in `f_(t+1)`. Therefore the exact raw projection is obtained from opposite corners:

```text
mu_L = mu(f0H, f1L, rH)
mu_H = mu(f0L, f1H, rL).
```

The biological state-transition model is compatible only where this projection intersects `[0,1]`.

No numerical optimizer or post-hoc choice of favorable corners is permitted.

## 4. What the state channel must measure

The state channel must provide at least two time-matched estimates of the abundance of the **same predeclared deletion class** in whole-colony or otherwise explicitly defined whole-biomass material.

Candidate marker regions already used in the Streptomyces genome-instability literature include terminal loci such as `cmlR`-region and `argG`-region loss. Their use here is prospective: an assay must first establish exactly which deletion class each marker panel detects.

Required controls:

```text
core-reference locus or loci;
same-age, same-condition intact baseline;
replication-dosage calibration;
assay detection/quantification limits;
predeclared rule for classifying a chromosome equivalent as the registered D state.
```

The same-age intact baseline is required because chromosome replication state can alter terminal-to-core copy ratios even in the absence of deletion.

## 5. Streptomyces unit bridge is not automatic

Streptomyces is filamentous and can contain multiple chromosome copies across a mycelium. Therefore a whole-DNA deletion-state fraction is not automatically identical to a frequency of independent cells, spores, or colonies.

The primary estimand is deliberately written as a transition of **chromosome-equivalent state mass**. Any stronger statement that this equals a lineage-level or caste-generation probability requires an additional unit bridge.

Required bridge evidence includes a declared sampling unit and evidence that changes in DNA-state fraction are not driven solely by spatial DNA-content differences, multinucleate structure, or extraction bias.

Accordingly:

```text
DIRECT_DNA_STATE_MU != AUTOMATIC_CELL_MUTATION_RATE
DIRECT_DNA_STATE_MU != AUTOMATIC_TOTAL_SPECIALIST_GENERATION_RATE
```

## 6. What the realization channel must measure

`r=d/g` must be estimated independently for already-deleted versus intact material over the same interval and ecological context.

The estimate must not be reverse-engineered from the same final deletion fraction used in the state channel.

An admissible `r` receipt therefore needs:

```text
pre-existing D material at interval start;
matched intact comparator;
same time horizon and medium/context;
closed uncertainty band or point estimate;
measurement unit compatible with the state channel.
```

If `r` is not independently constrained, `mu` remains unidentified.

## 7. Mapping mu into the frozen two-probe rule

For a control and probe comparison, let

```text
mu_C in [CL, CH]
mu_P in [PL, PH]
```

and predeclare a material reduction threshold `delta >= 0` before outcome data are opened.

The registered qualitative outcome is

```text
reduced
    iff CL - PH > delta

material_reduction_excluded
    iff CH - PL < delta

unresolved
    otherwise.
```

Equality/contact is unresolved because closed uncertainty sets still touch the decision boundary. A merely non-significant test is also not sufficient to claim material exclusion.

The two primary comparisons remain frozen as

```text
P1 = M1141 (Delta act) vs M1142 (Delta act Delta red)
P2 = M145 vs redU/SCO5883
```

and must be adjudicated jointly under the already registered four-way triangulation rule.

## 8. What a positive result would still not establish

Even if both primary probes show a material reduction in the registered `mu` estimand, that result would support only a narrower mediator claim such as:

> RED/prodiginine perturbation reduces entry into the registered terminal-deletion state across two predeclared probe backgrounds.

It would **not** automatically establish:

```text
a matched generalist/shared architecture;
a matched S comparator;
full S:D architecture mapping;
a frequency-dependent architecture payoff;
PAYOFF eta;
E1.
```

Those promotions remain behind their independent A- and G-lane gates.

## 9. Current frozen status

```text
DIRECT_MU_MEASUREMENT_CONTRACT_REGISTERED = TRUE
DIRECT_MU_MEASUREMENT_CONTRACT_PROSPECTIVE = TRUE
OUTCOME_DATA_OPENED = FALSE
DIRECT_MU_RESULT_AVAILABLE = FALSE
RED_TWO_PROBE_TRIANGULATION_FROZEN_PREOUTCOME = TRUE
RED_TWO_PROBE_TRIANGULATION_PROSPECTIVE = TRUE
MATCHED_GENERALIST_SHARED_ARCHITECTURE_RECOVERED = FALSE
MATCHED_S_COMPARATOR_CERTIFIED = FALSE
ARCHITECTURE_MAPPING_CERTIFIED = FALSE
PAYOFF_ARCHITECTURE_FREQUENCY_FEEDBACK_IDENTIFIED = FALSE
```
