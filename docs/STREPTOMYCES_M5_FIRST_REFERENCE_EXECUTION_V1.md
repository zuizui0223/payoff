# Streptomyces M5 first direct-mu reference execution v1

Status: **PROSPECTIVE / ZERO-TO-ONE EXECUTION TARGET**.

## Objective

The immediate PAYOFF empirical target is not another candidate paper. It is one qualified direct-mu matched-D realization reference.

The frozen first target is:

```text
reference_id = M5_T0
origin_cluster = ZHANG2022_SINGLE_MUTANT_PARENT
```

A successful M5 execution changes exactly one state:

```text
qualified matched-D realization references: 0 -> 1.
```

It does not, by itself, open architecture-specific inference.

## Why M5 first

The registered materialization audit gives M5 the highest priority because the published 2022 programme reports it as:

```text
named archived T0 material
T0 genome sequenced
T0 competition information available
shortest starting genome among the mutant lineages
no further large deletion detected during the serial-transfer experiment.
```

These properties make M5 worth materializing first. They do not certify its registered deletion class or realization rate.

## Required execution chain

```text
R0  physical stock / archive access
        |
R1  exact registered marker class from M5_T0 material
        |
R2  core reference + gross-rearrangement audit
        |
R3  same-context 72 h and 120 h calibrated D core-equivalent masses
        |
R4  exact closed d band = D_120 / D_72
        |
R5  existing per-reference qualification gate
        |
        +-- pass -> FIRST QUALIFIED MATCHED-D REFERENCE
        +-- fail -> retain blockers; do not promote
```

## R0 — material identity

The assay must use the frozen `M5_T0` material identity. Stock access must be confirmed before a realization result can qualify.

A reconstructed strain with the same phenotype is not silently relabelled M5_T0. A new reconstruction would need its own reference ID and provenance.

## R1 — deletion-class assignment

M5 must be assigned to exactly one registered class before its realization result is used:

```text
ENTRY_CLASS
    SCO7662 / cmlR2 absent
    SCO7350 present
    SCO7036 / argG present

INTERMEDIATE_CLASS
    SCO7662 absent
    SCO7350 absent
    SCO7036 / argG present

DEEP_CLASS
    SCO7662 absent
    SCO7350 absent
    SCO7036 / argG absent.
```

The central core reference remains:

```text
SCO3879 / dnaA.
```

The class assignment must come from the frozen M5 material / sequence-marker evidence, not from its measured realization `d`.

## R2 — reference integrity

Qualification requires:

```text
registered core reference present
pre-existing D state at 72 h
same medium and ecological context as the direct-mu state channel
M5 selection independent of the future direct-mu candidate outcome
gross secondary rearrangement relevant to interpretation resolved.
```

The existing statement that M5 did not accumulate another large deletion during the serial-transfer experiment is useful provenance, but the qualification receipt still requires the registered integrity fields to be resolved explicitly.

## R3 — realization measurement

The registered interval is fixed:

```text
72 h -> 120 h.
```

The registered quantitative unit is:

```text
CALIBRATED_CORE_CHROMOSOME_EQUIVALENTS.
```

For M5, estimate closed uncertainty bands for pre-existing D material at both times:

```text
D_72 in [D72_L, D72_H]
D_120 in [D120_L, D120_H].
```

The realization quantity is

```text
d = D_120 / D_72.
```

The repository computes its exact Cartesian closed band as

```text
d_L = D120_L / D72_H
d_H = D120_H / D72_L,
```

requiring a strictly positive lower bound for D_72.

This avoids declaring `REALIZATION_BAND_AVAILABLE` by hand.

## Matched intact comparator

The execution receipt must name the intact comparator used to establish the same-context reference frame. The comparator does not convert M5 into a matched-S architecture; it serves only the direct-mu realization measurement context.

Therefore:

```text
matched intact realization comparator
!= matched shared/generalist architecture S.
```

## R5 — semantic qualification

After the quantitative receipt is valid, the existing gate

```text
src/direct_mu_reference_panel_qualification.py
```

is applied unchanged.

The candidate must still satisfy:

```text
registered deletion class
marker pattern verified
core reference present
pre-existing at 72 h
same medium/context
independently derived from the direct-mu candidate outcome
candidate outcome not used to select reference
viable/measurable at 72 h
measurable at 120 h
gross secondary rearrangement resolved
realization band available.
```

Only the conjunction of the quantitative and semantic gates produces:

```text
qualified_reference = TRUE.
```

## Machine-readable implementation

Use:

```text
src/direct_mu_single_reference_execution.py
scripts/adjudicate_direct_mu_reference_execution.py
validation/streptomyces_m5_first_reference_execution_v1.json
```

The current JSON is a prospective status/receipt template. It must remain unqualified until real material and realization measurements replace the unresolved fields.

## What a positive M5 receipt changes

A positive receipt allows:

```text
FIRST_QUALIFIED_MATCHED_D_REFERENCE_RECOVERED = TRUE
DIRECT_MU_MATCHED_D_REFERENCE_PRECONDITION = TRUE
```

and changes the first-reference execution objective from materializing M5 to continuing the registered D panel / matched-S programme.

It still does **not** establish:

```text
complete D realization panel
conservative all-class d envelope
matched generalist/shared architecture S
S:D architecture mapping
architecture-specific frequency feedback
architecture-specific eta
finite-population architecture inference
E1.
```

## Failure routing

If M5 fails for a terminal reason, preserve the failure receipt and move to:

```text
W3_POST_DELETION.
```

If the blocker is reversible — stock confirmation pending, marker assay pending, realization assay not run — it is not a terminal failure and does not license new literature hunting.

Only after M5, W3 and M1 are all terminally exhausted while the qualified-reference count remains zero may bounded candidate search resume.

## Current status

```text
M5_T0 physical stock access        NOT YET CONFIRMED
registered M5 deletion class       NOT YET VERIFIED
72 h D mass band                    NOT YET MEASURED
120 h D mass band                   NOT YET MEASURED
closed d realization band           NOT AVAILABLE
per-reference semantic qualification NOT PASSED
qualified matched-D references      0
architecture-specific inference     HARD CLOSED
```
