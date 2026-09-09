# PAYOFF consortium strategic-unit gate v1

Lane: **A only**.

This is a subgate of `docs/ARCHITECTURE_MAPPING_PROTOCOL_V1.md` for cases where the differentiated candidate `D` is a multigenotype consortium rather than one genotype, organism, colony lineage, or other already-obvious strategic unit.

It does not use Lane R availability or Lane G outcomes.

## 1. Two frequencies must not be conflated

For a consortium candidate, define

```text
q = internal composition of D
    e.g. producer:consumer or ecotype proportions inside the consortium

p = external frequency of architecture D relative to architecture S
    in the population/game being tested.
```

A study may show strong regulation, convergence, or reproducibility of `q` without defining `p` at all.

Therefore

```text
stable q  !=  architecture frequency p
```

and a frequency experiment among the internal members of D cannot be reused as an S-vs-D architecture-frequency experiment.

## 2. Structural identity subgate

A multigenotype consortium is eligible to be treated as one strategic unit only if its identity is independently specified and maintained over the intended assay horizon.

Required declarations:

```text
U1 member set predeclared
U2 unit boundary predeclared
U3 assembly or regeneration protocol predeclared
U4 composition/state reproducibility supported
U5 propagation or transmission of the unit supported
U6 unit identity retained over the assay horizon
```

This does not require genetic clonality. It requires an operationally reproducible entity rather than an arbitrary mixture assembled differently for each assay.

## 3. PAYOFF unit-alignment subgate

Even a reproducible consortium is not yet a PAYOFF strategy unless the same unit can enter the population game.

Required declarations:

```text
U7 internal q is kept distinct from external p
U8 external p can vary the frequency of whole D units relative to whole S units
U9 fitness/output is defined at that same unit level
```

Without U8, there is no architecture-level frequency variable corresponding to the canonical `p` in

```text
Delta(p)=phi+eta(2p-1).
```

## 4. Independence rules

The unit decision must be made without asking whether the consortium wins.

Therefore certification must be independent of:

```text
rare-type advantage
coexistence
high productivity
better yield
negative frequency dependence
R-lane raw availability
```

A consortium does not become an architecture merely because it has a favorable game result or an unusually complete public dataset.

## 5. Beck synthetic E. coli adjudication

The Beck LAE consortium has a declared producer/consumer member set, a declared assembly design, and culture-level performance measurements. However, the current evidence programme does not establish a discrete or transmitted consortium unit whose **whole-unit external frequency** can be varied against WT.

Current blockers include:

```text
unit boundary not established as an external strategic unit
consortium propagation/transmission not established for this purpose
internal producer:consumer composition q is not an architecture frequency p
whole-D-unit external frequency is not defined
```

Therefore:

```text
BECK_CONSORTIUM_STRATEGIC_UNIT_CERTIFIED = FALSE
```

This conclusion is unchanged by the successful Beck R3 raw reconstruction and by the Lane G multimetric trade-off audit.

## 6. Evolved E. coli adjudication

The evolved cross-feeding ecotypes are biologically stronger on one component of this subgate: the consortium was reconstituted using established internal ecological proportions, so reproducibility of the internal state `q` has stronger support than in the Beck synthetic design.

But that does not solve the external-unit problem.

The direct competition with the ancestor mixes consortium member cells with ancestor cells. It does not establish independently reproducing or transmitted `D` units whose population frequency `p` can be varied separately from the consortium's internal `q`.

Thus the current blockers remain:

```text
no predeclared discrete consortium boundary as the strategic unit
no certified propagation/transmission of D as one unit
internal q is not separated from external p in the competition design
whole-D-unit external frequency is not defined
```

Therefore:

```text
EVOLVED_ECOLI_CONSORTIUM_STRATEGIC_UNIT_CERTIFIED = FALSE
```

The fact that the internal composition is reproducible is explicitly insufficient by itself.

## 7. What would close the subgate

Examples of designs that could close U1--U9 include a consortium propagated as a reproducible compartment/colony/community unit, with parent-to-offspring or serial-regeneration rules that preserve its declared identity, and an experiment in which the number/frequency of those whole D units can be varied against matched S units.

The exact biological implementation can differ among systems. The invariant requirement is:

```text
unit used to define architecture
=
unit whose external frequency is varied
=
unit whose fitness/output is measured.
```

## 8. Status

```text
CONSORTIUM_INTERNAL_Q_EXTERNAL_P_DISTINCTION_FROZEN
STABLE_INTERNAL_COMPOSITION_NOT_SUFFICIENT_FOR_STRATEGIC_UNIT
BECK_CONSORTIUM_STRATEGIC_UNIT_NOT_CERTIFIED
EVOLVED_ECOLI_CONSORTIUM_STRATEGIC_UNIT_NOT_CERTIFIED
ARCHITECTURE_MAPPING_REMAINS_GAME_INDEPENDENT
PAYOFF_ARCHITECTURE_FREQUENCY_FEEDBACK_NOT_YET_IDENTIFIED
```
