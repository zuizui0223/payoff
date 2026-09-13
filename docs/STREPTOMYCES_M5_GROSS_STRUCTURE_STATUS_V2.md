# Streptomyces M5_T0 gross-structure status v2

Status: **terminal losses recovered from pre-existing source data; R2 still open**.

This update separates two questions that the first PacBio-only audit had conflated:

1. were large terminal losses already present in `M5_T0`, and how large were they?;
2. does the public long-read lane reveal any additional gross structure that remains insufficiently characterized for reference qualification?

## Pre-existing source record

The Zhang et al. 2022 Fig. 4 source workbook records the initial M5 terminal losses as:

```text
left  =   372,936 bp
right =   864,624 bp
total = 1,237,560 bp
```

At transfer 25 the same source record reports no additional left- or right-terminal deletion for M5.

These values predate the PAYOFF qualification exercise. They therefore resolve the existence and reported size of the terminal losses without tuning a depth threshold to the M5 target reads.

## Public PacBio audit

The registered public PacBio comparison produced adequate central depth (`92.1028x` M5; `178.524x` WT) and three M5 gross calls at the registered `>=50 kb` scale, versus zero in WT. The M5 calls include a catalogued 83,009-bp duplication and two precise BND calls. The left BND starts at approximately 372,932 bp, extremely close to the source-recorded 372,936-bp left terminal loss, but its mate lies near 6.14 Mb. Therefore it is not defensible to rewrite it post hoc as a simple terminal breakpoint merely because one coordinate agrees with the source record.

## Current R2 ceiling

The terminal deletion record is now empirical progress. R2 as a whole is **not** closed because the structural interpretation of the two BND calls remains open for reference qualification.

Allowed recovery routes are only:

- pre-existing author/archive curated breakpoint or structural metadata; or
- a target-excluded, independently calibrated structural-audit v2.

A threshold chosen after inspecting M5 terminal trace coverage is explicitly forbidden.

Even a future R2 closure would not establish current stock access, matched 72→120 h realization `d`, or a qualified direct-mu reference. The qualified D-reference count therefore remains zero and architecture-specific inference remains hard closed.
