# Beck public raw reconstruction receipt v1

Lane: **R only**.

This receipt records a successful public-archive reconstruction event for the Beck et al. synthetic *E. coli* supplementary workbook. It deliberately makes no generic-game or architecture-specific claim.

## 1. Source object

```text
repository: rosspcarlson/becketal-syntheticconsortia
file: 22_0519_SupplementaryDataSets.xlsx
expected Git blob SHA1: 0ed48b34713d08dbdb17d9ca626387d63c673dbf
```

The workbook was downloaded from the repository's public raw URL on an isolated GitHub Actions runner.

Verified source receipt:

```text
byte size: 1112530
SHA256: 526bd7a0deebd9196762ea711639d0acd727eda9a30df29554909a7d3f5a4baa
recomputed Git blob SHA1: 0ed48b34713d08dbdb17d9ca626387d63c673dbf
Git blob match: true
```

Therefore R1 byte acquisition and object-identity verification are complete.

## 2. Workbook manifest and structural schema

The XLSX ZIP/XML structure was parsed directly.

Sheet count:

```text
30
```

Sheet names:

```text
Table of Contents
SuppSheet1 ... SuppSheet28
Sheet1
```

`Sheet1` is empty. The table of contents maps the experimental blocks as follows:

```text
Sheets 2-5
    WT growth data under buffer limitation, pH 6.0-7.5

Sheets 6-9
    lactate-producer growth data under buffer limitation, pH 6.0-7.5

Sheets 10-14
    lactate-consortium growth data under buffer limitation, pH 6.0-7.5

Sheets 15-17 in the workbook's declared contents map
    lactate-consortium producer:consumer ratio experiments at pH 7.0
    including 100:1, 10:1 and 1:2 conditions

Sheets 18-21
    acetate-producer growth data under buffer limitation, pH 6.0-7.5

Sheets 22-25
    acetate-consortium growth data under buffer limitation, pH 6.0-7.5

Sheets 26-28
    WT, lactate producer and lactate consortium under standard buffer capacity
```

The reconstruction also records each sheet's declared XLSX dimension, observed rows, and raw header/keyword rows. This completes R2 structural manifest/schema reconstruction.

## 3. Deterministic cell normalization

Every non-empty worksheet cell was normalized losslessly to a long-form TSV with the fields:

```text
sheet_order
sheet
row
cell_ref
cell_type
formula
value
```

No biological category was assigned during normalization.

Registered transformation receipt:

```text
non-empty cells: 33125
normalized TSV SHA256:
82fe0d7a591cb091d9efddfceede15116b55c293ffc64402f6f9c5ee0940fdc0
```

A second raw view selected rows containing workbook labels such as `X/pH`, `YXS`, `ΔX (g/L)`, biomass and related metric labels, without interpreting those labels as PAYOFF quantities:

```text
metric-row count: 63
metric-row TSV SHA256:
2a139b2acdf50e357ba09935b3bc199e29738659adb7f7d29696ab35a082f087
```

This completes the registered R3 deterministic transformation.

## 4. Reconstruction provenance

The successful R3 run is:

```text
workflow: raw-reconstruct-beck
run id: 34295583193
head: empirical/beck-raw-reconstruct-20260909
artifact: beck-raw-reconstruction-v2
artifact id: 10082985862
artifact ZIP SHA256:
b2cc2ee77a0fad4141b39245367d1e765ffcc31c94df1c0e74cbe0836b69b235
```

The artifact contains:

```text
beck_raw_reconstruction_v1.json
beck_keyword_rows_v1.tsv
beck_nonempty_cells_v1.tsv
beck_metric_rows_v1.tsv
```

The one-off reconstruction workflow is intentionally isolated from main. Main retains this receipt and the machine-readable registry state rather than turning public-data acquisition into a standing generic-game analysis.

## 5. Exact status

```text
R0 source identity: PASS
R1 bytes/checksum: PASS
R2 manifest/schema: PASS
R3 deterministic normalized transformation: PASS
R4 registered biological/statistical analysis reproduction: NOT YET
```

Status label:

```text
BECK_PUBLIC_RAW_ARCHIVE_R3_RECONSTRUCTED
```

## 6. Non-promotion boundary

R3 means only that the public source object and deterministic data substrate are reconstructed.

It does **not** establish that any workbook metric is the correct game payoff. In particular, the reconstructed labels

```text
X/pH
YXS
ΔX (g/L)
OD600
biomass
strain proportions
```

remain raw workbook variables until a separate Lane G contract predeclares the outcome scale and comparison.

Therefore all of the following remain false/unclaimed:

```text
BECK_GENERIC_GAME_VALIDATION_CERTIFIED
BECK_FREQUENCY_FEEDBACK_IDENTIFIED
BECK_ARCHITECTURE_MAPPING_CERTIFIED
PAYOFF_ARCHITECTURE_FREQUENCY_FEEDBACK_IDENTIFIED
```

The architecture lane remains independent. The fact that the workbook uses terms such as `Generalist` or `Consortia` is not itself an A-lane certificate.
