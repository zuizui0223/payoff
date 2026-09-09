# Evolved E. coli cross-feeding consortium architecture mapping audit v1

Lane: **A only**.  Direct fitness results are not used to decide whether the consortium is a PAYOFF D architecture.

Primary system: Yang et al. 2020, DOI `10.1128/AEM.00051-20`, building on the Helling/Rosenzweig glucose-limited lineage.

## 1. Mechanistic architecture signal

A single ancestral clone gave rise to genetically and phenotypically differentiated ecotypes.  Reconstructed consortia contain:

```text
primary-resource specialist
    -> strongest access to limiting glucose
    -> releases overflow metabolites

secondary-resource specialists
    -> preferentially consume acetate / glycerol-related overflow resources
```

This is a genuine evolved partition of resource-processing roles from one ancestral lineage and therefore a strong BITA-like differentiation analogue.

## 2. Independent A1--A6 adjudication

```text
A1 integrated/shared candidate:
    STRONG as the ancestral autonomous generalist clone

A2 differentiated/released candidate:
    STRONG at the ecological consortium level

A3 matched net biological task:
    STRONG
    both ancestral clone and reconstructed consortium convert the same glucose-limited
    resource system into descendants/biomass

A4 heritable or stable strategic unit:
    NOT YET CERTIFIED for D

A5 unit consistency across S and D:
    NOT YET CERTIFIED

A6 mapping independent of game result:
    PASS
```

Therefore:

```text
EVOLVED_ECOLI_ARCHITECTURE_MAPPING_CERTIFIED = FALSE
```

## 3. The precise unit problem

The S candidate is one clone/genotype-level lineage.

The D candidate is a reconstructed assemblage of multiple evolved genotypes whose internal ratio emerges ecologically.  The study shows stable coexistence among the ecotypes and characteristic steady-state ratios, but this does not automatically make the entire assemblage a single heritable strategic unit in the same sense as the ancestor.

The architecture question must be answered before importing any frequency-game result:

```text
What is inherited when D reproduces?

Is D transmitted as one stable ecological unit,
or must the component genotypes be separately assembled / maintained?

Would varying total S:D frequency preserve D's internal architecture,
or simultaneously change the internal composition that defines D?
```

Until those questions are closed, treating

```text
one ancestral cell lineage == one strategy
and
three-genotype consortium == one strategy
```

as automatically equivalent changes the strategic level.

## 4. What the steady-state ratio does and does not establish

The reconstructed ecotypes can settle into reproducible cross-feeding ratios.  That supports ecological stability of the consortium.

It does not by itself establish:

```text
heritable architecture identity,
one-to-one strategic-unit equivalence with the ancestor,
or PAYOFF S/D alignment.
```

This distinction is independent of the fact that the consortium has high measured performance.

## 5. What would close Lane A

A sufficient mapping argument would need to declare and defend a higher-level strategic unit, for example a reproducibly transmitted consortium state, and then show that:

```text
1. its component identities / internal organization are stable enough to define D;
2. D can be propagated as that same unit across the intended assay horizon;
3. S and D are compared at the same population/selection level;
4. the relevant functional release is the defining difference rather than an incidental
   consequence of multiple unrelated adaptations.
```

Alternatively, a single heritable genotype or developmental lineage that internally generates the same resource-role differentiation would remove much of the unit ambiguity.

## 6. Current A-lane conclusion

Allowed:

> The evolved E. coli system provides strong evidence that one ancestral generalist lineage can diversify into complementary cross-feeding ecotypes, but the multigenotype consortium has not yet been certified as the same kind of stable/heritable strategic unit as the ancestral clone; the PAYOFF architecture mapping remains open.

Not allowed:

> Higher consortium fitness proves that the consortium is PAYOFF's differentiated architecture.

Status:

```text
EVOLVED_ECOLI_S_TO_D_ECOLOGICAL_DIFFERENTIATION_STRONG
EVOLVED_ECOLI_D_CONSORTIUM_CANDIDATE_STRONG
EVOLVED_ECOLI_D_HERITABLE_STRATEGIC_UNIT_NOT_YET_CERTIFIED
EVOLVED_ECOLI_UNIT_CONSISTENCY_NOT_YET_CERTIFIED
EVOLVED_ECOLI_ARCHITECTURE_MAPPING_NOT_YET_CERTIFIED
```
