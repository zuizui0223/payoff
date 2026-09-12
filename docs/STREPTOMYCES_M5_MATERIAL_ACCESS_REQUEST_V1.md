# Streptomyces M5_T0 material-access request packet v1

Status: **READY TO SEND / NO REQUEST SENT BY THIS REPOSITORY**.

## Purpose

The PAYOFF direct-mu programme needs to determine whether the exact `M5_T0` material from Zhang et al. (2022) can be used as the first pre-existing D realization reference.

The request should be narrow. It is not a request for all mutant strains or for unpublished direct-mu outcomes.

## Requested items

Priority 1 — material access:

```text
Is the archived M5_T0 spore stock from the 2022 mutation-accumulation experiment still available?
If yes, who is the current custodian and what material-transfer / shipping procedure applies?
```

Priority 2 — exact sequence identity:

```text
Which BioSample / SRA run(s) under PRJNA780771 correspond exactly to M5_T0?
If the T0 PacBio-derived assembly / mapped deletion-boundary file is available separately,
what is its accession or archive identifier?
```

Priority 3 — marker / genome metadata if already available:

```text
For M5_T0, are the following loci retained or deleted?
SCO7662 / cmlR2
SCO7350
SCO7036 / argG
SCO3879 / dnaA

Are the left- and right-arm deletion boundaries for M5_T0 available as exact coordinates?
Were any additional large rearrangements detected in the T0 genome beyond the terminal losses?
```

## Why these exact items

PAYOFF has frozen a direct-mu realization assay over 72 h -> 120 h. M5_T0 is currently the first reference target because the published study reports that it was archived, sequenced at T0, began with the shortest mutant genome, and did not acquire another large deletion during serial transfer.

The publication also supports M5_T0 as a likely `DEEP_CLASS` right-arm deletion candidate from its T0 arginine-auxotrophy phenotype, but the project will not promote that class until the exact registered marker pattern is verified.

## Information that is not being requested

No request is made for:

```text
post-hoc selection of the best-growing deletion mutant;
unpublished outcome data from the planned direct-mu experiment;
new interpretation of PAYOFF architecture-specific eta;
or a claim that M5 is already a qualified reference.
```

## Minimal response sufficient to advance R0-R2

The pre-lab packet can advance substantially with:

```text
1. yes/no on current M5_T0 stock availability;
2. exact M5_T0 sequence accession / file identity;
3. marker states or deletion coordinates for SCO7662, SCO7350, SCO7036 and SCO3879;
4. any known additional gross rearrangement at T0.
```

The 72 h -> 120 h realization measurement remains a new experiment even if all four items above are recovered.

## Suggested email subject

```text
Request for M5_T0 Streptomyces coelicolor stock and sequence metadata (Zhang et al. 2022)
```

## Suggested concise message

Dear Dr. Zhang / Prof. Rozen,

I am working on a prospective analysis of the terminal-deletion state in *Streptomyces coelicolor* and would like to use the exact M5_T0 lineage from Zhang et al. (2022, Nature Communications 13:2266) as a pre-existing deletion reference. Could you please let me know whether the archived M5_T0 spore stock is still available and, if so, who currently holds it and what material-transfer procedure would apply?

I would also be grateful for the exact BioSample/SRA run or assembly identifier corresponding to M5_T0 under PRJNA780771. If readily available, the retained/deleted state or deletion coordinates for SCO7662/cmlR2, SCO7350, SCO7036/argG and SCO3879/dnaA, plus any other large T0 rearrangement, would let us verify the reference class before any new assay is run.

We are treating the published phenotype only as a candidate-class indication and will not infer a qualified reference without direct marker and realization measurements.

Best regards,

[Name / affiliation]

## Claim boundary

Preparing this request does not confirm stock access, sequence identity, marker state, realization, or qualification. The corresponding status fields remain false until an external response or direct public-record recovery supplies them.
