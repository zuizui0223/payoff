# Streptomyces M5_T0 material-access request packet v1

Status: **READY TO SEND / NO REQUEST SENT BY THIS REPOSITORY**.

## Purpose

The PAYOFF direct-mu programme needs to determine whether the exact `M5_T0` material from Zhang et al. (2022) can be used as the first pre-existing D realization reference.

The request is now deliberately narrow. Public sequence identity and the frozen four-locus marker evidence have already been recovered independently, so they should not be requested again.

## Public evidence already recovered

Exact public sequence identity:

```text
PacBio  SRR16954720 / SRX13146288 / M5_T0_PacBio
BGI     SRR16954696 / SRX13146312 / M5_T0_BGI
BioProject PRJNA780771
```

Independent public PacBio audit:

```text
SCO3879 / dnaA   present: 100% coverage, 124.526x mean depth
SCO7036 / argG   absent:    0% coverage,   0x
SCO7350          absent:    0% coverage,   0x
SCO7662 / cmlR2  absent:    0% coverage,   0x
```

These observations strongly corroborate the source-level `DEEP_CLASS` candidate. PAYOFF still keeps BGI as the prospectively declared primary marker-depth channel and does not use this request to bypass that response-blind gate.

## Remaining requested items

Priority 1 — exact living material:

```text
Is the archived M5_T0 spore stock from the 2022 mutation-accumulation experiment still extant and recoverable?
If yes, who is the current physical custodian?
What material-transfer, biosafety and shipping procedure applies?
```

Priority 2 — curated gross-structure metadata, only if already available:

```text
Is there an exact T0 assembly, chromosome-end boundary file, or curated large-SV call set for M5_T0?
If yes, what are the exact left- and right-arm terminal boundaries and any other >=50 kb rearrangements?
```

The 72 h -> 120 h realization measurement remains a new experiment and is not requested as an unpublished prior result.

## Current public contact route

The 2022 paper lists Zheren Zhang and Daniel E. Rozen as corresponding authors. Current public institutional information in 2026 lists:

```text
Dr Zheren Zhang
Lecturer in Biotechnology
Queen Mary University of London
zheren.zhang@qmul.ac.uk
```

Secondary publication-era corresponding route:

```text
Daniel E. Rozen
Leiden University
d.e.rozen@biology.leidenuniv.nl
```

## Suggested email subject

```text
Request for archived M5_T0 Streptomyces coelicolor stock (Zhang et al. 2022)
```

## Suggested concise message

Dear Dr. Zhang and Prof. Rozen,

I am working on a prospective analysis of terminal genomic differentiation in *Streptomyces coelicolor* and would like to use the exact M5_T0 lineage from Zhang et al. (2022, Nature Communications 13:2266) as a pre-existing deletion reference. Could you please let me know whether the archived M5_T0 spore stock is still extant and available for research use and, if so, who currently holds it and what material-transfer procedure would apply?

We have already resolved the public M5_T0 PacBio/BGI accessions under PRJNA780771 and are independently auditing the registered deletion markers, so no additional sequence mapping is needed. If an exact T0 assembly or curated chromosome-end / large-SV file is already available, its identifier or breakpoint coordinates would also be very helpful for resolving the remaining gross-structure audit before any new realization assay.

The project treats material access, genomic classification and the new 72 h -> 120 h realization measurement as separate gates; we are not treating M5_T0 as a qualified reference until all of them are closed.

Best regards,

[Name / affiliation]

## Claim boundary

Preparing this request and recovering public contact information do not confirm stock access. Until the current custodian confirms the exact archived material:

```text
M5_T0 physical stock access = UNCONFIRMED
qualified D reference count = 0
architecture-specific inference = HARD CLOSED
```
