# Microbial near-Lane-P evidence ledger v1

This ledger ranks systems by how close they come to direct empirical identification of PAYOFF frequency feedback between an integrated/shared architecture and a differentiated/released architecture.

## 1. *Pseudomonas aeruginosa* siderophore specialization — closest empirical two-axis near miss

Mridha et al. (2022), DOI `10.1111/jeb.14001`.

```text
S candidate: WT generalist producing pyochelin + pyoverdine
D candidate: mixed specialist community, one producer for each siderophore
same outcome: population growth/productivity
frequency experiment: yes, but only specialist-A : specialist-B ratio
WT-vs-D mixed-frequency experiment: no
```

Why it matters:

- WT is explicitly treated as the generalist baseline;
- specialist mixtures are compared quantitatively with WT on a common growth scale;
- specialist relative fitness changes with initial specialist composition and maintains coexistence by negative frequency dependence;
- iron availability changes whether specialist mixtures outperform, equal, or underperform WT.

Why it does not enter Lane P:

The manipulated frequency is internal composition of D, not the population frequency of S versus D. Treating a two-genotype consortium as one heritable architecture would silently change the strategic unit.

Status:

```text
NEAR_P_COMMON_SCALE_PLUS_WITHIN_D_FREQUENCY
```

## 2. *Bacillus subtilis* EPS/TasA biofilm specialization — strongest architecture + within-D frequency result

Dragoš et al. (2018), Current Biology, DOI `10.1016/j.cub.2018.05.046`.

```text
S candidate: generalist/WT matrix production
D candidate: complementary EPS-only and TasA-only genetic specialists
frequency experiment: specialist-specialist negative frequency dependence
stable D-internal ratio: ~30% TasA producers
WT-vs-D mixed-frequency experiment: no
```

The ratio that is dynamically stable also coincides with maximal group productivity, making this a strong real example of frequency feedback stabilizing internal differentiated composition.

Status:

```text
NEAR_P_ARCHITECTURE_STRONG_FREQUENCY_WITHIN_D_ONLY
```

## 3. synthetic *E. coli* organic-acid consortia — strongest static S-versus-D context switch with public data

Beck et al. (2022), mSystems, DOI `10.1128/msystems.00051-22`.

```text
S: WT generalist
D: producer-consumer consortium partitioning catabolism
same genomic potential at consortium level: yes
same net transformation: yes
S-vs-D common performance scale: yes
S:D mixed-frequency competition: no
public supplementary workbook/code: yes
```

The lactic-acid-exchanging consortium outperforms WT under low buffering in some metrics, whereas WT has superior properties under stronger buffering. This is a direct environmental architecture-payoff reversal, not frequency feedback.

Public data repository recorded in the paper:

```text
https://github.com/rosspcarlson/becketal-syntheticconsortia
22_0519_SupplementaryDataSets.xlsx
```

Current tooling recovered the public repository metadata and workbook identity, but the binary workbook could not be decoded through the text-only GitHub connector. No numeric result is inferred from metadata alone.

Status:

```text
NEAR_P_STATIC_S_D_PAYOFF_CONTEXT_SWITCH
PUBLIC_SUPPLEMENTARY_WORKBOOK_IDENTIFIED_NOT_YET_NUMERICALLY_INSPECTED
```

## 4. *Pseudomonas stutzeri* generalist-specialist cross-feeding — strongest direct frequency experiment with wrong architecture mapping

Schink et al., `Initial community composition determines the long-term dynamics of a microbial cross-feeding interaction by modulating niche availability`.

```text
G: complete denitrification generalist
specialist: nitrite-only consumer
reciprocal initial-ratio experiment: yes
common relative growth scale: yes
mutual invasibility: recovered in bounded conditions
```

This is directly useful for validating PAYOFF-style reciprocal-invasion measurement logic in a real microbial system. It is not a clean architecture release pair because the specialist alone is a partial-pathway consumer and the differentiated state is not one replacement heritable architecture.

Status:

```text
NEAR_P_DIRECT_FREQUENCY_WRONG_ARCHITECTURE_CONTRAST
```

## 5. *E. coli* maltose/lactose chemostat competition — direct generalist-specialist game analogue

Dykhuizen & Davies (1980), Ecology, DOI `10.2307/1936839`.

Generalists able to use maltose and lactose competed against maltose-only specialists in chemostats with both sugars, yielding coexistence under bounded resource compositions and environment-dependent equilibrium frequency.

The game layer is real and direct. The architecture mapping is not the declared SCH/BITA conflict-release mechanism; it is resource-breadth specialization.

Status:

```text
GENERIC_GENERALIST_SPECIALIST_GAME_ANALOGUE
```

## 6. *Streptomyces* mutation-driven division of labor — best heritable architecture concept, decisive comparison simulation-only

Colizzi et al. (2023), Molecular Systems Biology, DOI `10.15252/msb.202211353`.

A genome architecture with fragile sites generates sterile antibiotic-producing specialists from replicating progenitors, directly resolving a replication-versus-antibiotic trade-off. In the model, generalist architectures that cannot divide labor lose direct competitions against architectures that can.

This is conceptually the closest current architecture analogue because the differentiated organization is encoded by a heritable genome architecture rather than assembled ad hoc from separately maintained strains.

The blocker is empirical: the decisive S-versus-D frequency series is computational, not an experimental reciprocal-invasion dataset.

Status:

```text
NEAR_P_ARCHITECTURE_EXCELLENT_SIMULATION_FREQUENCY_ONLY
```

## Overall conclusion

No reviewed microbial system yet satisfies all of:

```text
heritable S architecture
heritable D architecture
same net task
common fitness scale
multiple S:D resident frequencies
empirical relative fitness
```

The closest systems fail in complementary ways. This makes the missing intersection itself a concrete experimental target rather than a vague literature gap.
