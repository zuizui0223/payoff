# Microbial near-Lane-P evidence ledger v1

This ledger ranks systems by how close they come to direct empirical identification of PAYOFF frequency feedback between an integrated/shared architecture and a differentiated/released architecture.

## 1. *Streptomyces coelicolor* terminal genomic differentiation — closest heritable architecture target

Zhang et al. (2020), Science Advances, DOI `10.1126/sciadv.aay5781`; Zhang et al. (2022), Nature Communications, DOI `10.1038/s41467-022-29924-y`; Colizzi et al. (2023), Molecular Systems Biology, DOI `10.15252/msb.202211353`; Avitia Domínguez et al. (2025), DOI `10.1098/rstb.2023.0267`.

The empirical series establishes:

```text
integrated progenitor colony:
    replicates/sporulates and produces antibiotics;

differentiated caste:
    large chromosome deletions generate sterile antibiotic hyperproducers;

trade-off:
    more antibiotic production accompanies sharply reduced autonomous spore fitness;

group benefit:
    mixtures of parent + deletion mutants produce more antibiotics while colony-wide spore production remains unchanged;

frequency assay:
    mutant versus WT cells were competed from multiple starting frequencies;
    differentiated mutants collapse from the reproductive pool even when initially common;

context response:
    competitor exposure can increase the internal deletion-mutant/caste ratio and spore production.
```

The 2023 genome-architecture model then shows why a heritable architecture capable of repeatedly generating this differentiated caste can beat matched generalist architectures.

Why it still does not enter Lane P:

The empirical frequency axis is **specialist cell versus WT cell**, not **DoL-capable colony architecture versus generalist-only colony architecture**. The latter direct architecture-frequency comparison remains model-based.

Status:

```text
NEAR_P_ARCHITECTURE_EXCELLENT_EMPIRICAL_COMPONENTS_WRONG_FREQUENCY_UNIT
```

## 2. experimentally evolved *E. coli* cross-feeding consortium — closest S-to-D origin plus direct S:D competition

Yang et al. (2020), Applied and Environmental Microbiology, DOI `10.1128/AEM.00051-20`, reanalyzed the classic Helling/Rosenzweig glucose-limited chemostat lineage.

```text
S candidate:
    the single common ancestral clone JA122;

D candidate:
    a genetically and phenotypically differentiated E3+E1+E6 cross-feeding consortium
    descended from that same ancestor;

origin:
    one initially clonal population evolved persistent primary-resource and secondary-resource specialists;

common scale:
    evolved ecotypes and reconstructed consortia were directly competed against GFP-labeled ancestor;

result:
    every evolved strain was fitter than the ancestor;
    two-member consortia were fitter than the ancestor;
    the three-member consortium was fitter than the ancestor and every evolved monoculture;
    fitness and productivity rankings agreed.
```

The consortium-versus-ancestor competition is especially close to PAYOFF's desired S-versus-D comparison because it closes an actual evolutionary route from one ancestral generalist into a differentiated cross-feeding organization and then compares the two on one fitness scale.

However, the consortium was reconstituted at its internal steady-state ratio and then mixed with an **equal number** of ancestral cells. This supplies one direct S:D starting composition, not a multi-frequency S:D response curve. It also retains a strategic-unit caveat because D is a multi-genotype consortium rather than one genotype.

Status:

```text
NEAR_P_EVOLVED_S_TO_D_DIRECT_COMPETITION_SINGLE_SD_RATIO
O_FREQ_REMAINING_MULTIPLE_SD_FREQUENCIES_NOT_TESTED
O_UNIT_CONSORTIUM_IS_MULTIGENOTYPE
```

This system is therefore the strongest current empirical target for a simple follow-up question:

```text
repeat ancestor-versus-reconstituted-consortium competition at multiple total S:D starting ratios,
while freezing the internal D consortium ratio,
and estimate Delta(p) prospectively.
```

## 3. *Pseudomonas aeruginosa* siderophore specialization — closest empirical two-axis near miss

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

## 4. *Bacillus subtilis* EPS/TasA biofilm specialization — strongest internal differentiated-frequency result

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

## 5. synthetic *E. coli* organic-acid consortia — strongest static S-versus-D context switch with public data

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

## 6. *Pseudomonas stutzeri* generalist-specialist cross-feeding — strongest direct frequency experiment with wrong architecture mapping

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

## 7. *E. coli* maltose/lactose chemostat competition — direct generalist-specialist game analogue

Dykhuizen & Davies (1980), Ecology, DOI `10.2307/1936839`.

Generalists able to use maltose and lactose competed against maltose-only specialists in chemostats with both sugars, yielding coexistence under bounded resource compositions and environment-dependent equilibrium frequency.

The game layer is real and direct. The architecture mapping is not the declared SCH/BITA conflict-release mechanism; it is resource-breadth specialization.

Status:

```text
GENERIC_GENERALIST_SPECIALIST_GAME_ANALOGUE
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

The near misses now split into two especially informative frontiers:

```text
Streptomyces:
    best heritable architecture concept,
    but the empirical frequency unit is specialist cell rather than colony architecture.

Yang et al. E. coli:
    actual single-ancestor -> differentiated consortium evolution
    plus direct S:D common-scale competition,
    but only one S:D starting ratio and a multi-genotype D unit.
```

So the remaining Lane P gap is no longer a generic demand for more evidence: it is a narrow strategic-unit/frequency-design intersection.
