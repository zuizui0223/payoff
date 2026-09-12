# Streptomyces M5 pre-lab evidence recovery v1

Status: **PRIMARY-SOURCE RECOVERY / NOT A QUALIFIED D REFERENCE**.

## Purpose

The first-reference programme is now focused on `M5_T0`. Before requesting new biological measurements, recover everything that can be established from the existing primary publication and public sequence provenance without opening or fabricating a direct-mu realization result.

The distinction is strict:

```text
published evidence that M5 is a useful D candidate
!=
direct marker qualification
!=
physical stock access
!=
72 h -> 120 h realization measurement
!=
qualified matched-D reference.
```

## 1. Archived-material existence is recovered, access is not

Zhang et al. (2022), DOI `10.1038/s41467-022-29924-y`, states that transferred lineages were archived by producing a lawn from the transferred colony, harvesting spores after approximately seven days, and maintaining all stocks at -20 C.

`M5` is one of the transferred mutant lineages and `M5_T0` is explicitly used in the T0 competition and whole-genome analyses. Therefore PAYOFF may now record:

```text
M5_T0_ARCHIVED_MATERIAL_EXISTENCE_DOCUMENTED = TRUE
```

but must retain:

```text
M5_T0_PHYSICAL_STOCK_ACCESS_CONFIRMED = FALSE.
```

A publication-level statement that a stock was archived is not evidence that the stock is currently available to this project. The next R0 action is a material-access confirmation with the source laboratory / current custodian.

## 2. Public sequence provenance is recovered

The same study reports whole-genome sequencing of `M1-M6` at T0 and deposits raw sequence data under BioProject:

```text
PRJNA780771.
```

Thus:

```text
M5_T0_WHOLE_GENOME_SEQUENCED = TRUE
PUBLIC_SEQUENCE_PROJECT_RECOVERED = TRUE
```

but the exact run/sample mapping required to extract `M5_T0` marker states has not yet been resolved in the registered PAYOFF receipt. Therefore:

```text
M5_T0_EXACT_SEQUENCE_RUN_RESOLVED = FALSE.
```

The next sequence action is not another literature search. It is to map the public BioProject or source-data metadata to the exact `M5_T0` record, then directly score the registered markers.

## 3. Primary phenotype strongly supports a DEEP_CLASS candidate

The registered right-arm classes are:

```text
ENTRY_CLASS
    SCO7662 / cmlR2 absent
    SCO7350 present
    SCO7036 / argG present

INTERMEDIATE_CLASS
    SCO7662 absent
    SCO7350 absent
    SCO7036 / argG present

DEEP_CLASS
    SCO7662 absent
    SCO7350 absent
    SCO7036 / argG absent.
```

The 2022 study uses two phenotypic deletion markers:

```text
chloramphenicol susceptibility
    -> loss of cmlR1/SCO7526 and cmlR2/SCO7662
    -> right-arm deletion at least ~322 kb in the published marker interpretation

arginine auxotrophy
    -> loss of argG/SCO7036
    -> right-arm deletion at least ~843 kb in the published marker interpretation.
```

Figure 2 shows `M5` as arginine auxotrophic already at T0, while the mutant lineages have reduced chloramphenicol resistance relative to WT. Figure 4 independently places `M5` among strains with large terminal deletions and reports that M5 began with the shortest genome.

Under the paper's own terminal-deletion interpretation, T0 argG loss is strong evidence that the right-arm deletion extends past the registered deep marker. PAYOFF may therefore record:

```text
M5_T0_PRIMARY_SOURCE_CLASS_CANDIDATE = DEEP_CLASS
M5_T0_DEEP_CLASS_CANDIDATE_SUPPORTED = TRUE.
```

This is deliberately **not** promoted to:

```text
marker_pattern_verified = TRUE.
```

The registered qualification gate asks for the exact marker pattern, including `SCO7350`, and the direct-mu programme must verify that pattern from the frozen M5 material / sequence rather than infer every marker solely from phenotypic ordering.

## 4. Initial genomic stability is useful but not a clean-genome certificate

The paper reports that M5 began with the shortest genome and, unlike the other mutant lineages, did not acquire another large deletion during the serial-transfer experiment.

This supports choosing M5 first because its deletion architecture appears unusually stable over that experiment. It does **not** prove that the T0 genome contains only the registered right-arm deletion.

Figure 4 shows terminal losses on both chromosome arms for the ancestral mutant lineages. Therefore the direct-mu receipt must still resolve:

```text
registered core marker SCO3879/dnaA
exact right-arm class markers
left-arm deletion structure
other gross secondary rearrangements relevant to realization.
```

Accordingly:

```text
gross_secondary_rearrangement_unresolved = TRUE
```

remains correct until the T0 sequence/marker audit is completed.

## 5. What is genuinely removed from the uncertainty set

Before this audit the M5 packet could be read as if material existence, sequence existence, and deletion severity were all unknown. That is now too pessimistic.

Recovered:

```text
archived M5 lineage material existed in the source programme
M5_T0 was whole-genome sequenced
public sequencing project PRJNA780771 exists
M5_T0 is a strong primary-source DEEP_CLASS candidate
M5 had no further large deletion during the transfer experiment.
```

Still open:

```text
current physical stock access
exact M5_T0 public run/sample mapping
registered SCO7662/SCO7350/SCO7036 marker-pattern verification
SCO3879/dnaA core-reference verification
exact secondary-rearrangement resolution
72 h / 120 h same-context D mass measurements
closed d realization band
per-reference qualification.
```

## 6. Revised next-action order

The shortest route to the first qualified reference is now:

```text
A. confirm current M5_T0 stock access / custodian
B. resolve exact M5_T0 sequence accession or obtain the archived T0 sequence record
C. score SCO7662, SCO7350, SCO7036 and SCO3879 directly
D. resolve left/right terminal structure and any other gross rearrangement
E. if R0-R2 remain admissible, run the frozen 72 h -> 120 h D-realization assay
F. compute the exact closed d band
G. run the existing per-reference qualification gate.
```

Steps A-D are the only remaining pre-lab / material-audit work. They are higher information value than adding more candidate papers.

## 7. Claim ceiling

This audit changes no architecture-specific empirical conclusion.

Current state remains:

```text
qualified matched-D references = 0
first qualified reference recovered = FALSE
architecture-specific inference = HARD CLOSED
eta architecture-specific = unavailable
E1 = FALSE.
```

The only promotion is from an unspecified literature candidate to a **source-supported DEEP_CLASS candidate whose exact registered marker pattern is still unverified**.
