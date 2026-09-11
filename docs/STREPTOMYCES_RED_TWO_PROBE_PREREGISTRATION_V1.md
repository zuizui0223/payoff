# Streptomyces RED two-probe preregistration v1

Lane: **A mechanism-probe sublane only**.

## Status correction: frozen design, prospective evidence

This preregistration is **prospective**. What is frozen is the probe set, estimand, and decision rule **before outcome data**. No direct terminal-specialist generation-rate outcome has yet been recovered for either primary probe.

The PAYOFF Streptomyces matched-S comparator also remains unresolved:

```text
matched generalist/shared architecture recovered = FALSE
matched S comparator certified = FALSE
architecture mapping certified = FALSE
```

Therefore neither the existence of two qualified RED/prodiginine probes nor their preregistration is evidence that a PAYOFF shared/generalist architecture has already been isolated.

In short:

```text
FROZEN != EMPIRICALLY CONFIRMED
MECHANISM PROBE != MATCHED S ARCHITECTURE
PROSPECTIVE TRIANGULATION != ARCHITECTURE-SPECIFIC PAYOFF VALIDATION
```

This preregistration prevents post-hoc selection between the two RED-deficient probe systems already qualified in PAYOFF.

## Primary probe set

Frozen before any direct terminal-specialist generation-rate result is available:

```text
P1 = M1141 (Δact) vs M1142 (Δact Δred)
P2 = M145 vs redU/SCO5883 single mutant
```

The probes have complementary caveats:

```text
P1 -> whole RED-cluster deletion; both strains share Δact background
P2 -> RED nearly abolished with gross morphology preserved; possible redV polar effect
```

Because the caveats differ, agreement is more informative than choosing either result alone.

## Required outcome variable

The outcome is **direct terminal-specialist generation**, not final mutant frequency alone.

Before a probe result is interpretable, the receipt must state that:

```text
differentiation generation was directly measured;
post-generation survival/realization was separated from that measurement;
the probe was one of the two predeclared primary comparisons.
```

The prospective direct measurement contract is registered as:

```text
STREPTOMYCES_DIRECT_MU_MEASUREMENT_CONTRACT_V1
```

It uses a two-state transition estimand in which direct deletion-state measurements at adjacent times are combined with an independently measured deleted-lineage realization ratio. This is a measurement design, not a recovered biological result.

A non-significant test is not automatically evidence that a material reduction is absent. It remains `unresolved` unless a separately predeclared criterion establishes `material_reduction_excluded`.

## Four-way decision rule

```text
P1 reduced + P2 reduced
    -> TRIANGULATED_MEDIATOR_GENERATION_REDUCTION

P1 material reduction excluded + P2 material reduction excluded
    -> REGISTERED_MEDIATOR_ROUTE_NOT_SUPPORTED

one reduced + one material reduction excluded
    -> PROBE_DISCORDANCE_MECHANISM_UNRESOLVED

any unresolved/unqualified result
    -> INCOMPLETE_OR_UNRESOLVED_TRIANGULATION
```

No branch permits choosing the favorable probe and ignoring the other primary probe.

## Existing-data audit

A focused literature search recovered RED-production, growth, sporulation, developmental, and biosynthetic measurements for the primary probes, but did **not** recover a published direct terminal chromosome-deletion/specialist-generation-rate comparison for either P1 or P2.

Therefore the current registered state is:

```text
P1 = unresolved
P2 = unresolved
status = INCOMPLETE_OR_UNRESOLVED_TRIANGULATION
outcome data opened = FALSE
prospective = TRUE
```

This is a genuine new measurement target rather than a relabeling of an existing mutant-frequency result.

## Secondary probe reserve

A `redJ` deletion reduces prodiginine production by roughly 75%, and genetic complementation restores production (JBC 2011, DOI `10.1074/jbc.M110.213512`). This makes `redJ` attractive as a later orthogonal/dose probe.

It is **not** in the primary pair because the current audit did not recover the gross growth/sporulation comparability required by the existing mechanism-probe gate. It cannot replace P1 or P2 post hoc because one primary result is inconvenient.

## What a positive triangulation would and would not establish

Two interpretable reductions would support the narrower mechanism statement:

```text
RED/prodiginine loss reduces the generation of terminal genomic specialists
across two predeclared perturbation backgrounds.
```

Even that would not by itself establish:

```text
matched S architecture
matched generalist/shared architecture
full S:D architecture mapping
frequency-dependent architecture fitness
PAYOFF eta
E1
```

Those require the existing downstream architecture and game gates.

## Current status

```text
PRIMARY_RED_PROBES_PREREGISTERED = TRUE
RED_TWO_PROBE_TRIANGULATION_PROSPECTIVE = TRUE
OUTCOME_DATA_OPENED = FALSE
DIRECT_MU_DATA_RECOVERED_FROM_EXISTING_LITERATURE = FALSE
TRIANGULATION_STATUS = INCOMPLETE_OR_UNRESOLVED_TRIANGULATION
MATCHED_GENERALIST_SHARED_ARCHITECTURE_RECOVERED = FALSE
MATCHED_S_CERTIFIED = FALSE
ARCHITECTURE_MAPPING_CERTIFIED = FALSE
PAYOFF_ARCHITECTURE_FREQUENCY_FEEDBACK_IDENTIFIED = FALSE
```
