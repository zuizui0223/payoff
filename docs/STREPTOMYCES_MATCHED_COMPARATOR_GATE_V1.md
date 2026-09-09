# Streptomyces matched architecture comparator gate v1

Lane: **A only**.

This document sharpens `STREPTOMYCES_ARCHITECTURE_MAPPING_AUDIT_V1.md` by separating evidence for a strong differentiated architecture candidate from evidence for a **matched S:D comparator pair**.

## Target pair

The PAYOFF architecture comparison is not

```text
WT cell vs terminal deletion-mutant cell.
```

It is

```text
S = colony/lineage constrained to remain integrated/generalist
D = matched colony/lineage retaining the native capacity to generate
    terminally differentiated antibiotic-specialist cells.
```

Both sides must therefore be compared at the same colony/lineage architecture level.

## Matched-comparator requirements

A candidate pair is certified only when all of the following are independently supported:

```text
M1 same strategic-unit level
M2 same net biological task
M3 matched genetic/biological background
M4 focal architecture difference isolated
M5 S generalist-only state experimentally verified
M6 D differentiated state experimentally verified
M7 both units stable over the intended assay horizon
M8 a common matched-task assay exists
```

Comparator choice must be independent of both game outcome and raw-data availability.

## Current Streptomyces adjudication

Evidence strongly supports D:

```text
native colonies generate chromosome-deletion specialists;
those cells show strong production/reproduction trade-offs;
parent + differentiated-cell mixtures can increase antibiotic output
without an observed colony-wide spore penalty;
terminal differentiation and genomic deterioration are independently supported.
```

But the matched S comparator remains missing.

Current gate:

```text
M1 same strategic-unit level: FAIL / S colony comparator absent
M2 same net task: PASS conceptually at colony level
M3 matched background: FAIL
M4 focal architecture difference isolated: FAIL
M5 S generalist-only state verified: FAIL
M6 D differentiated state verified: PASS
M7 both units stable over assay: FAIL because the S unit is not recovered
M8 common matched-task assay: FAIL
```

Therefore:

```text
STREPTOMYCES_MATCHED_ARCHITECTURE_COMPARATOR_CERTIFIED = FALSE
```

## Why genome-reduced/circularized M145 derivatives do not close M3--M5

Large subtelomeric deletion or circularized M145 derivatives are useful architecture perturbations, but the recovered evidence does not show that they specifically suppress the terminal differentiation programme while otherwise preserving the relevant colony background and net task.

Because those manipulations alter many loci and biosynthetic capacities, they cannot be relabeled `generalist-only` merely because their chromosome architecture differs.

That would make the desired PAYOFF mapping part of the definition rather than an independently tested fact.

## What experiment would close the comparator gate

A clean S candidate would be a stable colony/lineage in which the specialist-generating mechanism is specifically disabled or strongly suppressed while preserving, as far as possible:

```text
genetic background
colony-level reproduction
the antibiotic-mediated competitive task
assay environment
measurement scale.
```

Before any frequency experiment, verify:

```text
D generates the specialized caste;
S does not;
S and D remain distinct stable colony-level units;
the principal difference relevant to the comparison is the intended
architecture allocation mechanism.
```

Only after this matched A-pair exists should Lane G vary their external S:D frequency.

## Claim ceiling

Allowed:

> Streptomyces provides strong empirical evidence for mutation-driven functional differentiation and a strong D-architecture candidate, but no matched generalist-only colony architecture has yet been recovered; the S:D architecture comparator remains uncertified.

Not allowed:

> Existing WT-versus-deletion-mutant competitions estimate PAYOFF architecture frequency feedback.

Status:

```text
STREPTOMYCES_D_ARCHITECTURE_CANDIDATE_STRONG
STREPTOMYCES_MATCHED_S_COMPARATOR_NOT_RECOVERED
STREPTOMYCES_MATCHED_ARCHITECTURE_COMPARATOR_NOT_CERTIFIED
STREPTOMYCES_ARCHITECTURE_MAPPING_NOT_YET_CERTIFIED
PAYOFF_ARCHITECTURE_FREQUENCY_FEEDBACK_NOT_YET_IDENTIFIED
```
