# Streptomyces M5_T0 marker reconstruction v1

Status: **PUBLIC-SEQUENCE RECONSTRUCTION ALLOWED / NOT YET EXECUTED**.

## Purpose

PAYOFF no longer needs another candidate paper or another accession search before working on M5_T0. Exact candidate-to-run provenance is recovered and the next public-data task is now one bounded genotype reconstruction:

```text
M5_T0 exact public sequence
-> score SCO7662
-> score SCO7350
-> score SCO7036
-> score SCO3879
-> assign registered D class or remain unresolved.
```

This task may close the genomic part of R1/R2. It cannot produce a living D realization reference or a direct-mu result.

## Frozen sequence identity

The qualified sample map supplies two complementary M5_T0 runs:

```text
BGI / short-read lane
  SRR16954696
  SRX13146312
  M5_T0_BGI

PacBio / long-read lane
  SRR16954720
  SRX13146288
  M5_T0_PacBio
```

Reference chromosome:

```text
NC_003888.3
Streptomyces coelicolor A3(2) M145.
```

Candidate identity is keyed by exact experiment/run alias and candidate-named library metadata. BioSample identity alone is not sufficient because platform-level BioSamples are shared across candidates in this submission.

## Division of evidence between platforms

### BGI short reads — primary registered-marker evidence

Use the short-read lane to estimate normalized depth / copy evidence at:

```text
SCO7662 / cmlR2
SCO7350
SCO7036 / argG
SCO3879 / dnaA.
```

Each locus depth is normalized to a **predeclared central-core baseline** rather than to `SCO3879` alone, because `SCO3879` is itself a registered verification marker.

The normalization panel must be frozen before opening the M5 marker ratios.

### PacBio long reads — structural corroboration

Use the PacBio lane to reconstruct terminal breakpoints and gross T0 structure, especially:

```text
right-arm terminal boundary
left-arm terminal boundary
large additional rearrangements
consistency with the four-locus marker calls.
```

A marker-class call and a gross-rearrangement audit are separate gates. A clean four-locus pattern does not imply that all other large structural changes have been resolved.

## Fail-closed marker rule

No universal coverage cutoff is invented here.

Before M5 marker ratios are inspected, freeze:

```text
absence_max_ratio
presence_min_ratio
```

with

```text
0 <= absence_max_ratio < presence_min_ratio.
```

For any registered locus:

```text
ratio <= absence_max_ratio
  -> ABSENT

ratio >= presence_min_ratio
  -> PRESENT

absence_max_ratio < ratio < presence_min_ratio
  -> UNRESOLVED.
```

An unresolved locus cannot be assigned by nearest threshold or by the class expected from the paper phenotype.

The class patterns are exactly:

```text
ENTRY_CLASS
  SCO7662 ABSENT
  SCO7350 PRESENT
  SCO7036 PRESENT
  SCO3879 PRESENT

INTERMEDIATE_CLASS
  SCO7662 ABSENT
  SCO7350 ABSENT
  SCO7036 PRESENT
  SCO3879 PRESENT

DEEP_CLASS
  SCO7662 ABSENT
  SCO7350 ABSENT
  SCO7036 ABSENT
  SCO3879 PRESENT.
```

Any other complete pattern is outside the registered D classes.

## Why the source-level DEEP evidence does not set the call

The source study makes DEEP_CLASS a strong prior candidate for M5_T0 because the T0 phenotype supports deep right-arm loss. That evidence is useful for prioritization and interpretation.

It must not be used to choose the coverage thresholds or to fill an unresolved `SCO7350` call.

Therefore:

```text
source-supported DEEP candidate
!=
registered DEEP marker pattern verified.
```

## Threshold provenance

The production threshold receipt should state how the two cutoffs were chosen without using M5 marker outcomes. Admissible routes include, for example:

```text
retained-locus controls + known deletion controls;
independent assay-calibration data;
predeclared technical detection limits with a gray zone.
```

A post-hoc threshold selected because it gives the expected DEEP pattern is forbidden.

## Machine adjudication

The registered class logic is implemented in:

```text
src/direct_mu_marker_reconstruction.py
```

Input requires:

```text
qualified exact sequence sample map
primary short-read run
reference accession
frozen normalization panel
frozen presence/absence thresholds
normalized evidence for all four registered markers.
```

The receipt returns a class only when the exact pattern is resolved and `SCO3879` is verified present.

Even a positive marker receipt hard-codes:

```text
physical_material_identity_established = FALSE
gross_rearrangement_audit_completed = FALSE
realization_band_available = FALSE
reference_qualified = FALSE.
```

These must be closed elsewhere.

## Current blocker after PR #45/#47

The accession/mapping problem is closed. The unresolved public-data requirements are now:

```text
1. obtain/localize the exact M5 sequence bytes for the frozen runs;
2. freeze normalization panel + marker-call cutoffs before opening M5 ratios;
3. align/reconstruct against NC_003888.3;
4. compute the four normalized marker ratios;
5. run the marker-pattern gate;
6. use PacBio to audit gross terminal/rearrangement structure.
```

The current model environment can verify metadata but does not currently contain the large raw run files, so no marker state is claimed in this repository revision.

## Information-value rule

Until the exact four-locus pattern has been reconstructed, do not return to candidate-literature expansion. The public sequence already provides a more direct route to reducing uncertainty about the first target.

After marker/rearrangement reconstruction, the remaining independent path is physical material access plus the same-context 72 h -> 120 h realization assay.

## Claim ceiling

Current state remains:

```text
exact M5 sequence mapping = QUALIFIED
sequence marker reconstruction = ALLOWED
registered M5 D class = NOT YET QUALIFIED
gross rearrangement audit = NOT YET CLOSED
qualified D references = 0
architecture-specific inference = HARD CLOSED.
```
