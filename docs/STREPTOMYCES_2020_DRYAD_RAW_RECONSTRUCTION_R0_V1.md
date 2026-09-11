# Streptomyces 2020 Dryad raw reconstruction — R0 receipt v1

Lane: **R — raw archive reconstruction only**.

This receipt deliberately does not adjudicate generic game behavior, D-reference qualification, or architecture mapping.

## Recovered source identity

The 2020 Streptomyces division-of-labour study points to Dryad dataset

```text
10.5061/dryad.bnzs7h462
```

with one reported raw-data workbook:

```text
Data_Dryad_DoL-Zheren_Zhang.xlsx
reported size: 81.04 KB
format: XLSX
```

The dataset description states that the workbook contains a tab for each paper figure.

## Current R level

```text
source identity          = recovered
file manifest            = recovered
raw bytes                = NOT acquired
checksum                 = NOT verified
workbook opened          = FALSE
sheet/schema manifest    = NOT reconstructed
lossless cell table      = NOT reconstructed
numeric reproduction     = NOT performed

R level = R0_SOURCE_IDENTITY_AND_FILE_MANIFEST_RECOVERED
```

The current Dryad download path requires bearer authorization for file bytes in the available API route. This is an access-state statement only. It must not be converted into `file missing`, `dataset unavailable`, or any empirical negative result.

## Firewall to G and A

R0 does not change any semantic claim:

```text
GENERIC_GAME_RESULT_FROM_THIS_RECEIPT = FALSE
D_REFERENCE_QUALIFIED_FROM_THIS_RECEIPT = FALSE
MATCHED_GENERALIST_SHARED_ARCHITECTURE_RECOVERED = FALSE
MATCHED_S_CERTIFIED = FALSE
ARCHITECTURE_MAPPING_CERTIFIED = FALSE
ETA_PROMOTED = FALSE
E1_PROMOTED = FALSE
```

Even a future R3 reconstruction of this workbook would only make the source auditable. Generic-game and architecture-specific claims would still require their independent G and A gates.

## Next R transitions

The next allowed transitions are strictly evidentiary:

```text
R0 -> R1 : acquire exact workbook bytes and record byte size/checksum
R1 -> R2 : open workbook and reconstruct sheet/schema manifest
R2 -> R3 : produce lossless normalized cell table with its own checksum
R3 -> R4 : reproduce a predeclared numerical analysis, if one is separately registered
```

None of these transitions can by itself qualify a Streptomyces D reference or recover the missing matched-S comparator.
