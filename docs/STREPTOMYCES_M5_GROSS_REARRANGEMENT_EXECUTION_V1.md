# Streptomyces M5_T0 gross-rearrangement execution v1

Status: **PROSPECTIVE / NOT YET EXECUTED**.

## Question

The existing D-reference gate requires `gross_secondary_rearrangement_unresolved = false` before a pre-existing D strain can qualify. For M5_T0 this does not mean that the genome must be otherwise identical to M145. The source study already indicates substantial terminal genome loss.

The registered question is therefore:

> At a declared chromosome-scale resolution, have all gross T0 structural events been identified and catalogued well enough that the 72 h -> 120 h realization measurement is not attached to an uncharacterized genome-wide state?

## Frozen public runs

```text
M5_T0 PacBio      SRR16954720
WT ancestor PacBio SRR16954715
reference          NC_003888.3
```

WT is processed through the same mapping and large-SV pipeline. It is a technical/background control, not an independent D reference.

## Frozen resolution

```text
coverage bin               10 kb
gross-event reporting floor 50 kb
central depth interval       2.5–6.0 Mb
minimum central PacBio depth 10x
```

Events below 50 kb belong to a different mutation layer and cannot be used to inflate or rescue this gross-structure gate.

## Two evidence channels

### 1. Chromosome-wide coverage segmentation

Map M5 and WT PacBio reads to `NC_003888.3`, compute 10-kb coverage bins, and recover the left and right terminal retained/deleted transitions. The terminal boundaries must be explicitly bracketed; a four-locus marker call alone is not enough.

Coverage segmentation also records any internal >=50-kb copy-loss tract.

### 2. Long-read structural-variant catalog

Run the same >=50-kb long-read SV caller on M5 and WT. Record all M5 gross calls, including calls that are also seen in WT/background. The purpose is a catalog, not favorable filtering.

## Adjudication

`src/direct_mu_gross_rearrangement_audit.py` returns the gross-rearrangement blocker as closed only when:

```text
M5 and WT central depth pass;
chromosome-wide segmentation is complete;
left terminal boundary is resolved;
right terminal boundary is resolved;
large-SV calling is complete;
WT is processed through the same pipeline;
all detected >=50-kb events are catalogued;
every catalogued event has a resolved breakpoint or interval.
```

Crucially:

```text
gross_secondary_rearrangement_unresolved = false
!= no secondary rearrangement exists.
```

A known additional event may remain in the reference; it must simply cease to be uncharacterized at the registered resolution. Whether its presence is acceptable for a later biological interpretation remains visible in the event catalog and cannot be erased.

## Claim ceiling

Closing this gate still does not establish:

```text
current physical M5_T0 stock access;
pre-existing D viability at 72 h in the registered SFM assay;
120 h measurability;
closed realization d band;
qualified D reference;
matched S;
architecture mapping;
architecture-specific eta;
E1.
```
