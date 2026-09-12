# Streptomyces M5 BGI response-blind marker calibration v1

Status: **PRE-TARGET / CALIBRATION ONLY**.

## Decision

The M5 marker-reconstruction gate already declares the BGISEQ lane as the primary marker-depth channel. The successful M5 PacBio audit is retained as independent structural corroboration, but it must not be used to choose the BGI presence/absence thresholds after seeing the target.

The BGI thresholds are therefore calibrated without opening any M5 BGI marker ratio.

## Frozen calibration set

Use every available non-M5 T0 lineage in PRJNA780771 plus the WT ancestor:

```text
WT_ancestor
M1_T0
M2_T0
M3_T0
M4_T0
M6_T0
```

M5_T0 is explicitly excluded from every calibration calculation.

The paired public runs are frozen as:

| candidate | PacBio label channel | BGI calibration channel |
|---|---|---|
| WT_ancestor | SRR16954715 | SRR16954701 |
| M1_T0 | SRR16954714 | SRR16954700 |
| M2_T0 | SRR16954703 | SRR16954699 |
| M3_T0 | SRR16954692 | SRR16954698 |
| M4_T0 | SRR16954723 | SRR16954697 |
| M6_T0 | SRR16954719 | SRR16954695 |

M5 target runs remain:

```text
PacBio SRR16954720
BGI    SRR16954696
```

and are not inputs to this calibration.

## Registered target markers

```text
SCO7662
SCO7350
SCO7036
SCO3879
```

The reference is `NC_003888.3`.

## Frozen central-core normalization panel

BGI marker depth is normalized to the median depth across this reference-defined central panel:

```text
SCO3000
SCO3300
SCO3600
SCO3900
SCO4200
SCO4500
SCO4800
SCO5100
SCO5400
```

The panel was selected from internal chromosome coordinates before opening any M5 BGI marker ratio. It excludes the registered target markers and the terminal chromosome regions of interest.

For each run and each registered locus,

```text
normalized_ratio
= locus mean depth / median(core-panel mean depth).
```

If the core-panel median is zero or any declared core-panel locus cannot be resolved from the reference annotation, the calibration fails closed.

## Independent PacBio control labels

PacBio is used only to label calibration-control marker states. A control-marker pair is admitted only when it is extreme under the frozen rule:

```text
coverage_pct == 0
-> ABSENT_CONTROL

coverage_pct == 100
-> PRESENT_CONTROL

otherwise
-> CONTROL_STATE_UNRESOLVED
-> exclude that marker-control pair from threshold estimation.
```

The rule is frozen before the non-M5 control results are opened. It does not use M5.

`SCO3879` is handled identically and provides a central-core presence check; a control with an unresolved/absent core does not contribute calibration evidence.

## Threshold construction

Collect BGI normalized ratios only for control-marker pairs whose PacBio state is extreme and whose control core is present.

Define

```text
A = all BGI ratios with PacBio label ABSENT_CONTROL
P = all BGI ratios with PacBio label PRESENT_CONTROL.
```

Require both sets to be non-empty. Then freeze

```text
absence_max_ratio = max(A)
presence_min_ratio = min(P).
```

Qualification requires the strict calibration gap

```text
absence_max_ratio < presence_min_ratio.
```

If the sets overlap or touch, the BGI assay has not demonstrated a response-blind separation and M5 remains unopened under this gate.

This intentionally uses the most conservative observed absent and present controls rather than a fitted cutoff.

## Anti-leakage guard

The calibration job must assert:

```text
M5_T0 not in calibration candidates
SRR16954696 not downloaded as a calibration BGI run
SRR16954720 not downloaded as a calibration PacBio run
```

The generated calibration receipt contains no M5 marker ratios.

The target M5 BGI run may be opened only in a separate post-calibration job that consumes the frozen calibration receipt.

## Why all non-M5 T0 controls are used

The control set is not selected after observing which mutants provide convenient separation. Every available non-M5 T0 lineage is included, and each marker-control pair is admitted or excluded by the same predeclared PacBio extreme-state rule.

The M1-M6 shared founding origin is irrelevant to their use as technical assay controls. It remains relevant to the separate D-reference independence requirement and these controls do not count as independent qualified D references.

## Role of the successful M5 PacBio audit

The existing M5 PacBio result is strong corroboration:

```text
SCO3879 100% coverage, 124.526x
SCO7036   0% coverage,   0x
SCO7350   0% coverage,   0x
SCO7662   0% coverage,   0x
```

but it is not used to calibrate the BGI cutoffs. This prevents the already observed target result from determining the primary-channel decision rule.

## Claim ceiling

A successful calibration establishes only:

```text
response-blind BGI normalization and marker-call thresholds are frozen.
```

It does not establish:

```text
M5 BGI marker class
M5 gross-rearrangement resolution
physical M5 material access
72->120 h realization d
qualified D reference
matched S
architecture mapping
architecture-specific eta
E1.
```

## Next step after a successful calibration

Only then run:

```text
SRR16954696
-> BGI normalized marker ratios
-> src/direct_mu_marker_reconstruction.py
-> M5 registered class or unresolved.
```

In parallel, the PacBio lane must still close the separate gross-rearrangement audit.