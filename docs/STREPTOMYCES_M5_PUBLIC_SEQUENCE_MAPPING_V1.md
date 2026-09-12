# Streptomyces M5_T0 public sequence mapping v1

Status: **EXACT PUBLIC RECORD RECOVERED / MARKER PATTERN NOT YET SCORED**.

## Exact mapping

NCBI SRA project `PRJNA780771` contains an experiment explicitly labelled:

```text
WGS of S. coelicolor: T0 M5
```

with the following frozen identifiers:

```text
BioProject   PRJNA780771
Study        SRP346308
Experiment   SRX13146312
BioSample    SAMN23176398
SRS          SRS11078736
Run          SRR16954696
Library      M5_T0_BGI
Platform     BGISEQ-500
Strategy     WGS
```

This removes the earlier blocker:

```text
EXACT_M5_T0_SEQUENCE_ACCESSION_NOT_RESOLVED.
```

## What this unlocks

The next public-data task is no longer accession discovery. It is direct scoring of the registered reference loci from the frozen M5_T0 sequence record:

```text
SCO7662 / cmlR2
SCO7350
SCO7036 / argG
SCO3879 / dnaA.
```

The source-level phenotype/WGS audit already supports `DEEP_CLASS` as the leading M5 candidate class. The exact SRA mapping makes that hypothesis testable against the registered marker panel without waiting for a physical stock transfer.

## What this does not unlock

A public WGS run is sequence evidence, not a living realization reference. Therefore it does not establish:

```text
current stock access
72 h viability in the registered assay
120 h measurability
same-context realization d
closed d band
qualified D reference
matched S
architecture mapping
architecture-specific eta
E1.
```

The existing physical-material access receipt remains separate and unchanged.

## Frozen next step

```text
SRR16954696
-> registered four-locus scoring
-> gross T0 rearrangement audit
-> preoutcome class assignment
```

in parallel with:

```text
confirm physical M5_T0 stock identity and current availability.
```

Only if both the material and genotype/integrity lanes remain admissible should the new 72 h -> 120 h realization assay be run.
