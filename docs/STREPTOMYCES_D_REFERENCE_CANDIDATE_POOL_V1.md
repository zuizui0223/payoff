# Streptomyces D-reference candidate pool v1

Status: literature recovery only. This document does **not** materialize or qualify a pre-existing-D realization panel and reports no new Streptomyces outcome.

## Why this pool exists

The frozen direct-`mu` realization design requires at least two independent pre-existing deletion references in each registered severity class over the same 72->120 h interval as the state channel. Literature isolates can nominate candidates, but a literature name or deletion size is not a realized `d` measurement.

## Exactly classifiable WGS candidates from the focal M145-derived 2020 set

The eight reported right-arm deletion sizes are:

```text
387, 522, 740, 744, 783, 791, 871, 878 kb.
```

Using the already frozen marker cutoffs:

```text
ENTRY:        >178 and <503 kb     -> 1 candidate
INTERMEDIATE: >=503 and <841 kb    -> 5 candidates
DEEP:         >=841 kb             -> 2 candidates
```

Thus the exactly classifiable WGS pool meets the registered minimum of two candidates in the intermediate and deep classes but not in the entry class.

Current bottleneck:

```text
ENTRY_REFERENCE_SHORTFALL_IN_EXACTLY_CLASSIFIABLE_WGS_POOL
```

This is a candidate-count bottleneck, not a claim that any of the eight references is already available, retyped, or qualified for the registered realization assay.

## Additional sources are not silently promoted

The larger 2020 PFGE/phenotype collection contains `WT-like`, `CamS Arg+`, and `CamS Arg-` categories. `CamS Arg+` supports a broad terminal-deletion range but does not distinguish the frozen ENTRY versus INTERMEDIATE classes without exact SCO7350 retyping. These isolates are therefore candidate sources only.

The 2007 `delta ftsK_SC` experiment demonstrates that the registered marker-loss states are biologically populated, but its altered chromosome-segregation background is not the focal M145-derived realization background. It cannot supply qualified `d` references by substitution.

## What materialization still requires

For a literature candidate to enter the registered D-realization panel it still needs:

```text
physical reference material available;
registered marker panel retyped;
background compatibility confirmed;
72->120 h assay in the same context as the state channel;
core chromosome-equivalent fold change measured;
minimum two independent references in every registered class.
```

Only after those steps can the reference panel be marked materialized/qualified and a `d` band be constructed.

## Claim ceiling

```text
LITERATURE_D_REFERENCE_CANDIDATE_POOL_RECOVERED = TRUE
D_REFERENCE_PANEL_MATERIALIZED = FALSE
D_REFERENCE_PANEL_QUALIFIED = FALSE
D_REALIZATION_BAND_AVAILABLE = FALSE
DIRECT_MU_RESULT_AVAILABLE = FALSE
MATCHED_GENERALIST_SHARED_ARCHITECTURE_RECOVERED = FALSE
MATCHED_S_CERTIFIED = FALSE
ARCHITECTURE_MAPPING_CERTIFIED = FALSE
ETA_PROMOTED = FALSE
E1_PROMOTED = FALSE
```
