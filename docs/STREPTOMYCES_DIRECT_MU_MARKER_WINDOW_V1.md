# Streptomyces direct-mu marker and window contract v1

Lane: **A mechanism-measurement sublane only**.

Status: **prospective / pre-outcome**.

This document freezes the DNA-state panel and primary sampling interval used by the registered direct-`mu` estimand. It does not report a new biological outcome and does not recover the missing matched generalist/shared architecture.

## 1. Registered state entry

The primary registered deletion state `D` is entered when the right-terminal locus

```text
SCO7662 / cmlR2
```

is lost relative to a calibrated central-core reference.

The literature places SCO7662 about 178 kb from the right chromosome end and has used it directly in PCR panels for terminal-deletion characterization.

This is the **entry marker**, not the whole deletion phenotype.

## 2. Severity ladder is separate from entry

Two deeper loci are retained as severity markers:

```text
SCO7350  ~503 kb from the right end
SCO7036 / argG  ~841 kb from the right end
```

The registered ordering is therefore

```text
SCO7662 loss
    -> registered D entry

SCO7350 loss
    -> intermediate right-arm deletion severity

SCO7036 / argG loss
    -> deep right-arm deletion severity
```

A shift from the entry state into a deeper severity state is **not** counted as another new entry event into `D`.

This prevents the direct-`mu` estimand from conflating

```text
new terminal-deletion entry
```

with

```text
continued erosion of an already-deleted chromosome.
```

## 3. Core reference and dosage calibration

The predeclared central reference is

```text
SCO3879 / dnaA
```

in the centrally located oriC region.

The raw terminal/core copy ratio is not interpreted directly as deletion fraction because oriC-to-terminal dosage can vary with chromosome replication state.

Every registered terminal/core readout therefore requires

```text
genotype-matched
x time-matched
x condition-matched
```

intact baseline material verified to retain all registered terminal loci.

A universal M145 baseline alone is not sufficient for a congener probe whose growth or replication state may differ from M145.

The calibrated state channel therefore uses relative terminal/core depletion **after** this matched intact baseline correction.

## 4. Primary interval

The primary direct-`mu` interval is frozen as

```text
72 h -> 120 h
```

for a duration of 48 h.

Rationale:

- 72 h and 120 h are the first two adjacent sampling points in the registered 2025 Streptomyces colony time course;
- 120 h corresponds to five days, aligning the end of the state interval with the five-day external-function assay used in the focal 2020 division-of-labour study;
- the interval was selected before congener task, genotoxicity, or direct-`mu` outcomes were opened.

Later intervals may be exploratory or secondary but cannot replace the primary interval after outcome opening.

## 5. Whole-biomass state channel

The primary state channel is a whole-biomass / explicitly defined whole-colony DNA channel.

The estimand is therefore a transition of

```text
chromosome-equivalent state mass
```

rather than an automatic count of independent cells or spores.

This preserves the unit guardrail from `STREPTOMYCES_DIRECT_MU_MEASUREMENT_CONTRACT_V1`:

```text
DNA-state mu != automatic cell mutation rate
DNA-state mu != automatic total specialist generation rate.
```

Any lineage/caste interpretation remains behind a separate unit bridge.

## 6. The state channel is now frozen; the realization channel is not

The algebraic direct-`mu` estimand still requires

```text
r = d/g
```

for pre-existing registered-`D` material versus intact material over the same 72->120 h interval and context.

That realization channel must be measured independently and must not be reverse-engineered from the final deletion-state fraction.

Current status:

```text
MARKER_PANEL_FROZEN = TRUE
PRIMARY_INTERVAL_FROZEN = TRUE
STATE_CHANNEL_FROZEN = TRUE
INDEPENDENT_REALIZATION_CHANNEL_FROZEN = FALSE
DIRECT_MU_FULLY_READY = FALSE
```

Thus freezing the marker/window does not authorize opening direct-`mu` outcomes.

## 7. Current opening blockers remain

The congener outcome programme still lacks:

```text
response-blind qualified primary genotoxicity scale;
independent frozen realization channel r;
predeclared uncertainty construction;
task materiality threshold;
genotoxicity materiality threshold;
direct-mu materiality threshold.
```

Consequently

```text
OUTCOME_OPENING_ALLOWED = FALSE
```

remains unchanged.

## 8. Claim ceiling

This marker/window freeze does not recover:

```text
matched generalist/shared architecture;
matched S comparator;
architecture mapping;
frequency-dependent architecture payoff;
PAYOFF eta;
E1.
```

The RED/prodiginine and congener programmes remain prospective mechanism/measurement programmes only.
