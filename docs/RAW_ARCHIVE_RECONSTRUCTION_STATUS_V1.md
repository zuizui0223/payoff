# PAYOFF public raw archive reconstruction status v1

Lane: **R only**. This document records provenance/reconstruction status and makes no game or architecture claim.

## 1. Pseudomonas stutzeri — ERIC `10.25678/0006RZ`

Primary paper: Dolinsek, Ramoneda & Johnson (2022), DOI `10.1038/s43705-022-00160-1`.

The paper explicitly states that **all experimental data and code** are publicly available in the Eawag Research Data Institutional Collection (ERIC) under DOI `10.25678/0006RZ`.

A public catalog harvesting the ERIC record exposes the top-level file objects as:

```text
Dolinsek_et_al_2022.zip   ZIP   ~3.3 GB
File-List.txt             TXT   ~95.4 KB
README.txt                TXT   ~16.2 KB
```

This strengthens source-object discovery but does not reconstruct the contents of `File-List.txt`, the ZIP manifest, or any data table.

Current reconstruction state:

```text
R0 source/archive identity + top-level object metadata: PASS_STRONG
R1 bytes acquired + checksum pinned: NOT YET
R2 internal manifest/schema reconstructed: NOT YET
R3 transformation pipeline reconstructed: NOT YET
R4 registered/raw analysis reproduced: NOT YET
```

The published-text reciprocal-invasion receipt elsewhere in PAYOFF remains a Lane G result and is not used to upgrade this R status.

Current blocker:

```text
the public DOI and top-level file listing are verified,
but the current retrieval path has not exposed the file bytes or File-List/README
contents needed for checksum-pinned and schema-level reconstruction.
```

Therefore the allowed R claim is only:

> The public archive identity, provenance, and top-level file-object metadata are verified.

It is not yet permissible to claim raw trajectory reconstruction or raw-analysis reproduction.

## 2. Beck et al. synthetic E. coli public GitHub archive

Public repository:

```text
rosspcarlson/becketal-syntheticconsortia
```

Workbook:

```text
filename: 22_0519_SupplementaryDataSets.xlsx
Git blob SHA1: 0ed48b34713d08dbdb17d9ca626387d63c673dbf
verified byte size: 1112530
SHA256: 526bd7a0deebd9196762ea711639d0acd727eda9a30df29554909a7d3f5a4baa
```

A one-off isolated GitHub Actions reconstruction run downloaded the public workbook bytes, recomputed the Git object hash, and verified exact agreement with the repository object.

The XLSX container was then parsed without spreadsheet software or semantic reinterpretation. The workbook contains 30 sheets (`Table of Contents`, `SuppSheet1`--`SuppSheet28`, and an empty `Sheet1`). The table of contents maps the experimental blocks, including WT pH-series growth data, lactate/acetate producer and consortium series, producer:consumer ratio experiments, and standard-buffer experiments.

A second isolated run normalized every non-empty cell to a deterministic long-form table with fields

```text
sheet_order
sheet
row
cell_ref
cell_type
formula
value
```

without assigning biological/game semantics.

Registered reconstruction outputs:

```text
non-empty normalized cells: 33125
normalized-cell TSV SHA256:
82fe0d7a591cb091d9efddfceede15116b55c293ffc64402f6f9c5ee0940fdc0

raw metric-row count: 63
metric-row TSV SHA256:
2a139b2acdf50e357ba09935b3bc199e29738659adb7f7d29696ab35a082f087

reconstruction workflow run: 34295583193
artifact id: 10082985862
artifact ZIP SHA256:
b2cc2ee77a0fad4141b39245367d1e765ffcc31c94df1c0e74cbe0836b69b235
```

Current reconstruction state:

```text
R0 source/file identity: PASS
R1 workbook bytes acquired + checksum pinned: PASS
R2 workbook sheet/structural schema reconstructed: PASS
R3 deterministic lossless cell-table transformation reconstructed: PASS
R4 registered biological/statistical comparison reproduced: NOT YET
```

The isolated reconstruction workflow and helper scripts are **not** merged into main as a standing analysis route. Main records the receipt and hashes; the one-off branch remains the provenance source for the reconstruction event.

Raw rows containing labels such as `X/pH`, `YXS`, `ΔX (g/L)`, biomass, OD, metabolite concentrations, or strain proportions have been reconstructed. Their existence does not choose any of them as a PAYOFF fitness/payoff estimand.

Accordingly, this R3 success does **not** imply any of:

```text
GENERIC_GAME_VALIDATION_CERTIFIED
BECK_WT_VS_CONSORTIUM_PAYOFF_ADVANTAGE_IDENTIFIED
ARCHITECTURE_MAPPING_CERTIFIED
PAYOFF_ARCHITECTURE_FREQUENCY_FEEDBACK_IDENTIFIED
```

A separate Lane G contract must predeclare a commensurable outcome and comparison before numerical game analysis.

## 3. Arabidopsis halleri Dryad workbook

The Dryad workbook identity is already registered elsewhere in PAYOFF. Current state remains:

```text
R0 archive/workbook identity: PASS
R1 bytes/checksum: NOT YET
R2-R4: NOT YET
```

This lane does not use the published rare-morph result to promote the raw reconstruction status.

## 4. Reconstruction priority after Beck R3

The raw queue is ranked by immediate downstream reproducibility value, not by architecture proximity:

```text
R1 P. stutzeri ERIC
   -> acquire File-List.txt + README first, then isolate first-three-transfer
      composition trajectories and reproduce published trend tests

R2 Arabidopsis halleri Dryad
   -> reconstruct composition x reproductive outcome tables

Beck synthetic E. coli
   -> R3 complete; next R-only step is R4 reproduction of a predeclared
      published/raw comparison, which must remain separate from choosing a G estimand.
```

The order has no effect on Lane A priority.

## 5. Hard non-promotion rule

An R3 or future R4 success is a reproducibility statement and nothing more.

Even R4 cannot by itself set any of:

```text
GENERIC_GAME_VALIDATION_CERTIFIED
ARCHITECTURE_MAPPING_CERTIFIED
PAYOFF_ARCHITECTURE_FREQUENCY_FEEDBACK_IDENTIFIED
```
