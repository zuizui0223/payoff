# Public raw archive reconstruction protocol v1

Lane: **R only**.

This protocol reconstructs public evidence objects without assigning game or architecture meaning.

## Required receipt

For every archive target freeze:

```text
system_id
dataset_id
source DOI / repository / version / commit
retrieval date
original filename(s)
byte size
cryptographic checksum
file manifest
sheet/table names
row/column schema
identifier keys
treatment coding
missing-value coding
unit conventions
transformation recipe
analysis-ready table checksum
```

## Reconstruction stages

```text
R0 source metadata identified
R1 bytes acquired + checksum pinned
R2 file manifest + schema reconstructed
R3 transformations to analysis-ready tables reproduced
R4 registered analysis reproduced from reconstructed tables
```

A stage can advance only from evidence in the archive itself or its declared source documentation.

## Hard separation rule

Lane R must never contain a field whose truth depends on interpreting the biological alternatives as PAYOFF architectures.

Do not store in a raw receipt:

```text
shared / differentiated architecture assignment
phi
eta
phase label
coexistence / dominance claim
E1 promotion
```

Those belong to Lane G or Lane A.

## Current targets

```text
PSTUTZERI_ERIC_0006RZ
    state: R0
    next: acquire archive/file index and isolate first-three-transfer composition trajectories

BECK_SYNTHETIC_CONSORTIA_GITHUB
    state: R0
    source workbook identity recovered
    next: obtain binary workbook bytes and pin SHA256 before parsing

ARABIDOPSIS_HALLERI_DRYAD_53K2D
    state: R0
    next: acquire workbook bytes and reconstruct mesocosm composition/reproduction sheets
```

## Promotion rule

Even `R4` means only:

> the declared public evidence object and analysis were reproducibly reconstructed.

It does **not** mean the generic PAYOFF game is supported and does **not** mean an architecture mapping is valid.
