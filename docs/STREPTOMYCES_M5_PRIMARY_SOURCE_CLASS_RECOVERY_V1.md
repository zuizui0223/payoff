# Streptomyces M5_T0 primary-source class recovery v1

Status: **SOURCE-SUPPORTED CLASS CANDIDATE / NOT QUALIFIED**.

## Purpose

The direct-mu programme has already frozen `M5_T0` as its first materialization target. This audit asks one narrower question before any new 72 h -> 120 h realization experiment:

> Does the primary publication already constrain which registered D severity class M5_T0 is likely to occupy?

It does. The source evidence supports `DEEP_CLASS` as the leading candidate. It does **not** directly verify the complete registered marker pattern, so no reference-qualification gate is promoted.

## Primary source

Zhang et al. (2022), *Nature Communications* 13:2266, DOI `10.1038/s41467-022-29924-y`.

Relevant source facts are kept separate from the already registered material-access receipt:

```text
M5_T0 whole-genome sequenced in the source study
raw sequence project reported as PRJNA780771
M5 mutant phenotype evaluated from T0
M5 began with the shortest genome among the mutant lineages
M5 did not acquire another large deletion during the serial-transfer experiment.
```

The existing `STREPTOMYCES_DIRECT_MU_MATERIAL_ACCESS_V1` receipt remains authoritative for archive existence versus current physical access. This audit does not duplicate or alter that decision.

## Registered D classes

PAYOFF's frozen right-arm classes are:

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

The central core reference is `SCO3879 / dnaA`.

## Why M5_T0 is a DEEP_CLASS candidate

The source paper uses terminal-marker phenotypes to track deletion severity. In its interpretation:

```text
loss of chloramphenicol resistance
  -> loss of terminal chloramphenicol-resistance loci including cmlR2 / SCO7662

arginine auxotrophy
  -> loss of argG / SCO7036
  -> a much deeper right-arm terminal deletion.
```

M5 is already arginine auxotrophic at T0 in the reported marker series and belongs to the mutant set showing terminal deletion evidence. The whole-genome analysis independently reports M5 as beginning with the shortest genome among the mutant lineages.

Therefore the admissible source-level conclusion is:

```text
M5_T0_PRIMARY_SOURCE_CLASS_CANDIDATE = DEEP_CLASS
M5_T0_DEEP_CLASS_CANDIDATE_SUPPORTED = TRUE.
```

## Why this is not a registered-class PASS

The direct-mu gate does not classify references from phenotype alone. A DEEP_CLASS qualification requires the exact registered pattern:

```text
SCO7662 absent
SCO7350 absent
SCO7036 absent
core SCO3879 present.
```

The inspected primary-source evidence strongly constrains the outer/deep marker state, but it does not itself provide a PAYOFF receipt directly scoring all four registered loci on the frozen M5_T0 material.

Accordingly:

```text
registered_marker_pattern_verified = FALSE
registered_deletion_class_qualified = FALSE.
```

The next sequence/genotype task is therefore direct and bounded:

```text
resolve the exact M5_T0 public sequence/sample record
-> score SCO7662
-> score SCO7350
-> score SCO7036
-> score SCO3879
-> freeze the registered class before viewing any new realization outcome.
```

## Gross rearrangement remains open

The source also shows that the ancestral mutant genomes can contain terminal loss on both chromosome arms. The fact that M5 did not acquire another large deletion during serial transfer is useful stability evidence but is not equivalent to a clean single-right-arm-deletion genotype.

Thus:

```text
M5_T0_NO_FURTHER_LARGE_DELETION_DURING_TRANSFER = TRUE
GROSS_SECONDARY_REARRANGEMENT_RESOLVED_FOR_REFERENCE_USE = FALSE.
```

The exact T0 genome structure must still be audited before qualification.

## Information-value consequence

This audit removes a literature-search uncertainty without opening the architecture claim:

```text
before:
  M5 class unspecified

after:
  M5 primary-source class candidate = DEEP_CLASS
  exact registered class still unverified.
```

The first-reference programme should therefore spend no further effort asking whether M5 is a plausible deletion reference. It should now close the remaining concrete R0-R2 items:

```text
current physical material identity/access
exact M5_T0 sequence/sample mapping
registered four-locus marker pattern
core retention
secondary-rearrangement audit.
```

Only after those remain admissible should the registered 72 h -> 120 h `d` realization assay be run.

## Claim ceiling

Nothing here changes the direct-mu empirical count:

```text
qualified matched-D references = 0
D realization band = unavailable
matched S = FALSE
architecture mapping = FALSE
architecture-specific eta = unavailable
E1 = FALSE.
```
