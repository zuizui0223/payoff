# PAYOFF public raw archive reconstruction status v1

Lane: **R only**.  This document records provenance/reconstruction status and makes no game or architecture claim.

## 1. Pseudomonas stutzeri — ERIC `10.25678/0006RZ`

Primary paper: Dolinsek, Ramoneda & Johnson (2022), DOI `10.1038/s43705-022-00160-1`.

The paper explicitly states that **all experimental data and code** are publicly available in the Eawag Research Data Institutional Collection (ERIC) under DOI `10.25678/0006RZ`.

Current reconstruction state:

```text
R0 source/archive identity: PASS
R1 bytes acquired + checksum pinned: NOT YET
R2 manifest/schema reconstructed: NOT YET
R3 transformation pipeline reconstructed: NOT YET
R4 registered/raw analysis reproduced: NOT YET
```

The published-text reciprocal-invasion receipt elsewhere in PAYOFF remains a Lane G result and is not used to upgrade this R status.

Current blocker:

```text
the public DOI is verified,
but the current retrieval path has not exposed authenticated file bytes / manifest
for checksum-pinned reconstruction.
```

Therefore the allowed R claim is only:

> The public archive identity and provenance are verified.

It is not yet permissible to claim raw trajectory reconstruction or raw-analysis reproduction.

## 2. Beck et al. synthetic E. coli public GitHub archive

Public repository:

```text
rosspcarlson/becketal-syntheticconsortia
```

The repository directory exposes the workbook:

```text
filename: 22_0519_SupplementaryDataSets.xlsx
Git blob SHA: 0ed48b34713d08dbdb17d9ca626387d63c673dbf
reported byte size: 1112530
```

The same repository also contains model/code assets including `WTODE_220516.mlx`, `AAEComODE_220516.mlx`, and `LAEComODE_220520.mlx`.

Current reconstruction state:

```text
R0 source/file identity: PASS_STRONG
R1 workbook bytes independently acquired + SHA256 pinned: NOT YET
R2 workbook sheet/schema reconstruction: NOT YET
R3 analysis-ready table reconstruction: NOT YET
R4 registered comparison reproduced: NOT YET
```

The Git blob SHA is a strong repository-object identifier, but it is not substituted for the protocol's local byte acquisition + checksum step.  The current GitHub connector exposes repository metadata but refuses binary workbook decoding through its UTF-8 text path.

No WT-versus-consortium numerical result is inferred from file metadata.

## 3. Arabidopsis halleri Dryad workbook

The Dryad workbook identity is already registered elsewhere in PAYOFF.  Current state remains:

```text
R0 archive/workbook identity: PASS
R1 bytes/checksum: NOT YET
R2-R4: NOT YET
```

This lane does not use the published rare-morph result to promote the raw reconstruction status.

## 4. Reconstruction priority

The raw queue is ranked by immediate downstream numerical value, not by architecture proximity:

```text
R1 P. stutzeri ERIC
   -> recover first-three-transfer composition trajectories and reproduce published trend tests

R2 Beck synthetic E. coli workbook
   -> reconstruct environment x WT/consortium performance tables

R3 Arabidopsis halleri Dryad
   -> reconstruct composition x reproductive outcome tables
```

The order can change if file accessibility changes.  It has no effect on Lane A priority.

## 5. Hard non-promotion rule

A future R4 success means:

```text
PUBLIC_RAW_OBJECT_RECONSTRUCTED_AND_ANALYSIS_REPRODUCED
```

and nothing more.

It cannot by itself set any of:

```text
GENERIC_GAME_VALIDATION_CERTIFIED
ARCHITECTURE_MAPPING_CERTIFIED
PAYOFF_ARCHITECTURE_FREQUENCY_FEEDBACK_IDENTIFIED
```
