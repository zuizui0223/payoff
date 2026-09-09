# Streptomyces coelicolor architecture mapping audit v1

Lane: **A only**.  Frequency-game results are deliberately excluded from the mapping decision.

## 1. Candidate PAYOFF mapping

Biological evidence supports the following architecture hypothesis:

```text
S candidate
    integrated / generalist colony organization
    replicating lineage bears the combined growth/reproductive and antibiotic-production burden

D candidate
    division-of-labor-capable colony architecture
    reproducing progenitors repeatedly generate terminally differentiated,
    antibiotic-hyperproducing cells through large chromosome-end deletions
```

The key empirical papers show:

- spontaneous chromosome amplifications/deletions create genetically differentiated cells;
- deletion mutants strongly increase antibiotic production but suffer large autonomous fitness/spore costs;
- mixtures of parental and differentiated cells increase antibiotic output without detected loss of colony-wide spore production;
- later work supports terminal differentiation and continued genomic deterioration of the nonreproductive specialists.

These facts strongly support a real **functional differentiation mechanism**.

## 2. Independent A1--A6 adjudication

```text
A1 integrated/shared candidate explicitly defined:
    PARTIAL / CONCEPTUALLY PLAUSIBLE

A2 differentiated/released candidate explicitly defined:
    STRONG

A3 matched net biological task:
    STRONG at colony function level
    (reproduction/growth plus antibiotic-mediated competitive function)

A4 heritable or stable strategic unit:
    NOT YET CERTIFIED for the S-vs-D pair

A5 unit consistency across S and D:
    NOT YET CERTIFIED

A6 mapping independent of game result:
    PASS
```

Therefore:

```text
STREPTOMYCES_ARCHITECTURE_MAPPING_CERTIFIED = FALSE
```

The failure is not because differentiation is weak.  It is because the **matched S architecture has not been experimentally isolated as the same strategic unit as D**.

## 3. Why WT versus deletion-mutant cells is not the architecture pair

The empirical deletion-mutant competition compares

```text
WT CELL
versus
terminally differentiated specialist CELL.
```

The architecture hypothesis concerns

```text
colony/lineage architecture capable of generating a specialist caste
versus
matched colony/lineage architecture constrained to remain generalist.
```

Those are different levels of organization.  Reusing the cell competition as the architecture comparison would violate unit consistency.

## 4. Search for a matched generalist-only comparator

A focused literature audit identified engineered *S. coelicolor* M145 derivatives with large subtelomeric deletions and an artificially circularized chromosome.  One reported circularized derivative removes approximately `840 kb` from the left and `761 kb` from the right chromosome arms; related genome-reduction studies report broadly preserved growth/sporulation for some derivatives.

These strains are **not yet a valid matched S comparator** for PAYOFF because the recovered literature does not establish that they:

```text
specifically abolish the terminal-genomic-differentiation programme,
retain the same relevant antibiotic-production task,
remain otherwise matched to the DoL-capable parent,
and have been compared as competing colony architectures.
```

Large genome reduction/circularization changes many loci and biosynthetic capacities.  It would be circular reasoning to call such a strain `generalist-only` merely because its chromosome architecture differs.

Accordingly:

```text
MATCHED_GENERALIST_ONLY_STREPTOMYCES_ARCHITECTURE_NOT_YET_RECOVERED
```

## 5. What would close Lane A

A clean architecture experiment would require a pair such as:

```text
D:
    a lineage/colony retaining the native propensity to generate terminally
    differentiated antibiotic specialists

S:
    a matched lineage/colony in which that differentiation-generating mechanism
    is specifically suppressed or disabled while preserving the same relevant
    net task and background as far as possible.
```

Before any frequency experiment, demonstrate independently that:

```text
D generates the specialized caste;
S does not;
D and S are stable/heritable strategic units;
the key functional allocation difference is the intended architecture contrast.
```

Only then should Lane G compare their frequency-dependent relative performance.

## 6. Current A-lane conclusion

Allowed:

> *Streptomyces coelicolor* provides strong empirical evidence for mutation-driven functional differentiation and a compelling candidate architecture mechanism, but a matched generalist-only strategic architecture has not yet been recovered; architecture mapping therefore remains uncertified.

Not allowed:

> WT and deletion-mutant cell competitions identify PAYOFF architecture eta.

Status:

```text
STREPTOMYCES_FUNCTIONAL_DIFFERENTIATION_MECHANISM_STRONG
STREPTOMYCES_D_ARCHITECTURE_CANDIDATE_STRONG
STREPTOMYCES_MATCHED_S_ARCHITECTURE_NOT_YET_RECOVERED
STREPTOMYCES_ARCHITECTURE_UNIT_CONSISTENCY_NOT_YET_CERTIFIED
STREPTOMYCES_ARCHITECTURE_MAPPING_NOT_YET_CERTIFIED
```
