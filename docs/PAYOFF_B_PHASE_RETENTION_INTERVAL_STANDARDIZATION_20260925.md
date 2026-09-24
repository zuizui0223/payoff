# PAYOFF-B phase-retention interval standardization — pre-Aikens freeze

Frozen: **2026-09-25**

Status: **secondary cross-system standardization frozen before the Aikens lambda outcome is opened**.

## Why this amendment exists

The direct empirical programme uses

```text
E_next = a + lambda E_current + error
```

across ecologically meaningful but unequal intervals.

The raw coefficient is therefore a valid within-system phase-retention
estimand, but its magnitude is not automatically comparable across systems when
one row represents a whole spring migration and another represents one staging
transition.

This amendment does **not** replace the registered raw-lambda analyses. It
adds secondary coordinates that make interval scale explicit.

## Frozen coordinates

For each segment-scale coefficient,

```text
R = |lambda|
```

and for the preregistered reference duration `Delta t_ref`,

```text
k_eq = -ln(R) / Delta t_ref
R_day = exp(-k_eq)
```

where `k_eq` has units day^-1.

**Important:** `k_eq` is an equivalent reference-interval transformation. It
is not described as a directly estimated continuous-time controller rate.

The reference duration is the **median observed elapsed time** in the exact
frozen pair sample. The interval IQR is retained as a sensitivity envelope
because several systems, especially wigeon, have strongly skewed transition
durations.

Negative lambda values retain their sign as an overshoot/reversal flag.
`k_eq` uses `|lambda|` only for the magnitude envelope and never erases the
sign result.

## Cumulative retained-memory coordinate

For a homogeneous sequence of `n` transitions,

```text
R_path(n) = R^n
```

This quantity means only the propagated memory of the **incoming** phase
deviation if the same transition coefficient were applied repeatedly.

It is **not** the expected final phase error, because intercepts, new
environmental innovations, stage heterogeneity and process noise can add new
error between transitions.

### Wigeon

The exact source artifact contains 224 transitions from 28 unique individuals
but **32 animal-years**. Therefore `224/28 = 8` is not the appropriate typical
migration-stage count.

The observed animal-year transition-count distribution has:

```text
mean = 7
median = 7
range = 1..16
```

so the frozen representative path-memory calculation uses `n=7`, while the
full observed count histogram is retained by the script.

For the registered source-faithful POWER estimate,

```text
lambda = 0.749768
R_path(7) = 0.1332
```

For the independent ERA5 reconstruction,

```text
lambda = 0.811312
R_path(7) = 0.2314
```

These are the same order as the retrospective whole-spring-migration mule-deer
retention `R=0.1073`, which shows why raw transition-scale lambdas should not
be interpreted as a seven-fold difference in whole-migration correction.

However, the complete-calibration wigeon SIMEX sensitivity range remains
important. At the frozen upper sensitivity value `lambda=0.935394`,

```text
R_path(7) = 0.6266
```

so the programme does **not** license a universal claim that 80--90% of phase
error disappears over one migration.

### Barnacle geese

The highlighted goose estimates are fixed route transitions. A common,
prospectively declared full-route transition chain is absent, so whole-route
`R_path` is deliberately **not reported**. Their median interval durations
are used only for the secondary `k_eq` calculation.

## Aikens rule frozen before outcome opening

The prospective Aikens phase-retention contrast already uses fixed 24-hour
phase pairs. If that registered analysis becomes estimable,

```text
Delta t_ref = 1 day
```

by construction.

The interval-standardized quantities are secondary. They cannot change:

- the registered group definitions;
- the fixed 24-hour target rule;
- the support thresholds;
- the direction of the lambda contrast;
- the significance rule;
- the environmental reconstruction contract.

Thus the standardization method is fixed before either Aikens group-specific
lambda is opened.

## Current claim boundary

Licensed:

- raw lambda values are segment-scale estimands and should not be ranked as
  portable biological constants when segment durations differ;
- `k_eq` makes the declared time scale explicit;
- wigeon homogeneous path-memory retention over the observed typical
  seven-transition animal-year is much lower than its single-transition lambda;
- the naive POWER and independent ERA5 wigeon path-memory values are of the same
  order as the retrospective whole-migration mule-deer retention;
- measurement-error sensitivity remains large enough to prevent a universal
  whole-migration correction fraction.

Not licensed:

- treating `k_eq` as a directly fitted physiological or behavioral rate;
- claiming that every migrant removes 80--90% of phase error per migration;
- multiplying goose transition lambdas into a post-hoc whole-route coefficient;
- treating wigeon SIMEX as a corrected truth;
- altering the preregistered Aikens primary contrast after its outcome opens.

## Machine implementation

```text
data/payoff_b_phase_retention_interval_standardization_contract_20260925.json
scripts/standardize_phase_retention_intervals.py
tests/test_phase_retention_interval_standardization.py
```
