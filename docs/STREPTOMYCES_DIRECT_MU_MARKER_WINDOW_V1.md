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

## 6. Preferred realization route is absolute-state-mass based

The state channel is frozen, and the **design** of the remaining realization channel is now frozen separately.

For compatible absolute state masses,

```text
G1 = (1-mu) g G0
D1 = d D0 + mu g G0
N  = D1 - d D0
```

so

```text
mu = N / (G1 + N).
```

This preferred route requires an independently measured realization `d` for material already in `D` at 72 h, but it does **not** require a separate measurement of intact realization `g`.

The older fraction-only route using

```text
r = d/g
```

remains valid and is retained as an optional secondary route.

The realization-panel design is frozen pre-outcome, but the biological reference panel itself has not yet been materialized or qualified.

Current status:

```text
MARKER_PANEL_FROZEN = TRUE
PRIMARY_INTERVAL_FROZEN = TRUE
STATE_CHANNEL_FROZEN = TRUE
REALIZATION_DESIGN_FROZEN = TRUE
D_REFERENCE_PANEL_MATERIALIZED = FALSE
D_REFERENCE_PANEL_QUALIFIED = FALSE
D_BAND_AVAILABLE = FALSE
REALIZATION_CHANNEL_READY = FALSE
DIRECT_MU_FULLY_READY = FALSE
```

Thus freezing the design does not authorize opening direct-`mu` outcomes.

## 7. Current opening blockers remain

The congener outcome programme still lacks:

```text
materialized and qualified D realization reference panel;
closed d realization band;
response-blind qualified primary genotoxicity scale;
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

Neither the marker/window freeze nor the frozen realization design recovers:

```text
matched generalist/shared architecture;
matched S comparator;
architecture mapping;
frequency-dependent architecture payoff;
PAYOFF eta;
E1.
```

The RED/prodiginine and congener programmes remain prospective mechanism/measurement programmes only.
