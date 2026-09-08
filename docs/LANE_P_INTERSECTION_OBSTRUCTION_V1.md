# Lane P intersection obstruction audit v1

Status: frozen near-miss audit for direct empirical PAYOFF architecture-frequency identification.

## Lane P admission rule

A study changes `PAYOFF_ARCHITECTURE_FREQUENCY_FEEDBACK_NOT_YET_IDENTIFIED` only if all of the following hold in the same empirical comparison.

```text
P1 architecture pair:
   S is a declared integrated/shared heritable architecture and
   D is a declared differentiated/released heritable architecture.

P2 matched functional task:
   S and D are evaluated for the same net biological task/outcome.

P3 frequency axis:
   relative performance of S versus D is measured at multiple S:D population compositions,
   ideally including reciprocal rare-resident assays or sufficiently broad predeclared support.

P4 common scale:
   both architectures have commensurable reproductive/growth fitness so Delta(p)=w_D(p)-w_S(p) is definable.

P5 unit consistency:
   the strategic unit whose frequency is varied is the same heritable architecture unit used in P1;
   an internally mixed consortium does not automatically count as one heritable D architecture.

P6 empirical rather than simulation-only:
   a model may motivate the mapping but cannot by itself promote Lane P.
```

## Obstruction codes

```text
O_ARCH       architecture contrast is not integrated/shared versus differentiated/released
O_UNIT       differentiated state is an assembled consortium or within-group composition, not the varied heritable unit
O_FREQ       frequency dependence is measured on the wrong contrast or no S:D frequency series exists
O_SCALE      no common relative-fitness scale for S and D
O_ENDPOINT   only interior/monoculture comparisons exist; reciprocal rare-resident margins are absent
O_SIM        decisive S:D comparison is simulation-only
O_TASK       compared types do not perform the same net functional task on their own declared scale
```

## Near-Lane-P microbial systems

| System | Architecture evidence | Frequency evidence | Closest positive result | Blocking obstruction | Adjudication |
| --- | --- | --- | --- | --- | --- |
| *Streptomyces coelicolor* terminal genomic differentiation, Zhang et al. 2020/2022; Avitia Domínguez et al. 2025; Colizzi et al. 2023 | WT colonies repeatedly generate sterile antibiotic-hyperproducing deletion mutants, partitioning sporulation/growth versus costly antibiotic production; mixed WT+mutant colonies increase antibiotic output without reducing colony-wide spore production | mutant-versus-WT cell competitions span multiple starting frequencies and mutants collapse even from high initial frequency; competition cues increase the internal deletion-mutant/caste ratio; a genome-architecture model compares division-of-labor-capable versus generalist architectures | Heritable genome organization plus real specialized caste, real frequency assays, and environment-responsive caste allocation make this the closest heritable architecture near miss | `O_UNIT + O_FREQ`: empirical frequency axis is specialist-cell versus WT-cell or internal caste ratio, not colony architecture S versus colony architecture D; direct generalist-architecture versus DoL-architecture competition remains model-based | `NEAR_P_ARCHITECTURE_EXCELLENT_EMPIRICAL_COMPONENTS_WRONG_FREQUENCY_UNIT` |
| evolved *E. coli* cross-feeding consortium, Yang et al. 2020 / Helling-Rosenzweig lineage | one ancestral clone evolved genetically and phenotypically differentiated primary- and secondary-resource ecotypes that coexist by cross-feeding | reconstructed two- and three-member consortia were directly competed against the common ancestor on one fitness scale, but consortium versus ancestor began at one total S:D composition: equal numbers of ancestor and consortium cells | actual S-to-D evolutionary origin plus direct common-scale S:D competition; the full consortium is fitter than the ancestor and any evolved monoculture | `O_FREQ + O_ENDPOINT + O_UNIT`: no multiple total S:D starting ratios / reciprocal architecture endpoints; D is a multigenotype consortium rather than one heritable genotype | `NEAR_P_EVOLVED_S_TO_D_DIRECT_COMPETITION_SINGLE_SD_RATIO` |
| *Pseudomonas aeruginosa* siderophores, Mridha et al. 2022 | WT is explicit generalist producing pyochelin+pyoverdine; engineered specialists each produce one siderophore | specialist relative fitness is measured across initial specialist mixing ratios and shows negative frequency dependence | specialist-mixture productivity is compared on the same growth scale with WT and changes relative to WT across iron environments | `O_UNIT + O_FREQ`: WT is not competed against the specialist consortium across a WT:D frequency axis | `NEAR_P_COMMON_SCALE_PLUS_WITHIN_D_FREQUENCY` |
| *Bacillus subtilis* biofilm matrix, Dragoš et al. 2018 | WT/generalist makes EPS+TasA; engineered genetic specialists partition EPS versus TasA and complement each other | strong negative frequency dependence between the two specialists; stable ~30% TasA-producer ratio in vitro and on roots | genetic division of labor can outperform incomplete/generalist production and specialist ratio converges to productivity optimum | `O_UNIT + O_FREQ`: frequency axis is specialist A versus specialist B, not WT S versus differentiated consortium D | `NEAR_P_ARCHITECTURE_STRONG_FREQUENCY_WITHIN_D_ONLY` |
| synthetic *E. coli* organic-acid division of labor, Beck et al. 2022 | WT generalist performs complete catabolism; producer+consumer guilds collectively have the same genomic potential and partition the pathway | no reported WT-versus-consortium frequency series | consortium versus WT performance reverses with environmental buffering; public supplementary data and code are available | `O_UNIT + O_FREQ + O_ENDPOINT`: static/contextual S-versus-consortium comparison, no mixed S:D competition | `NEAR_P_STATIC_S_D_PAYOFF_CONTEXT_SWITCH` |
| *Pseudomonas stutzeri* denitrification cross-feeding, Schink et al. 2022 | complete-pathway generalist versus nitrite-only specialist | reciprocal initial-ratio assays directly test whether each type increases from rare; coexistence recovered in a bounded pH context | direct generalist-specialist frequency-dependent relative growth on a common cell-growth scale | `O_ARCH + O_TASK`: specialist is a partial-pathway consumer, not a differentiated architecture that independently/collectively replaces the generalist as the same heritable unit | `NEAR_P_DIRECT_FREQUENCY_WRONG_ARCHITECTURE_CONTRAST` |
| *E. coli* sugar-use chemostats, Dykhuizen & Davies 1980 | generalists use maltose+lactose; specialists lack lactose use | generalist-specialist coexistence and equilibrium frequencies measured experimentally | direct generalist-specialist competition with environment-dependent equilibrium | `O_ARCH`: niche breadth specialization is not the declared conflict-release architecture mapping | `GENERIC_GENERALIST_SPECIALIST_GAME_ANALOGUE` |

## Two leading frontiers

### Frontier A — heritable architecture is strongest in Streptomyces

The Streptomyces series supplies nearly every component separately:

```text
2020:
    direct experimental terminal differentiation;
    antibiotic-production / spore-production trade-off;
    mixed WT + deletion-mutant colonies improve antibiotic output without sacrificing colony-wide spore output.

2022:
    mutant versus WT competition at multiple initial frequencies;
    differentiated mutants have extremely low autonomous fitness and are eliminated from the reproductive pool.

2025:
    competitor exposure increases the mutation/caste ratio and spore production;
    the extent of internal differentiation is environmentally responsive.

2023 model:
    a heritable genome architecture that can generate differentiated cells beats matched generalist architectures under declared conditions.
```

The missing experiment is narrow:

```text
vary the population frequency of a heritable colony architecture that can generate the differentiated caste
versus
a matched heritable colony architecture constrained to remain generalist,
and measure their relative reproductive output on one common scale.
```

### Frontier B — direct S-to-D origin and common-scale competition are strongest in evolved E. coli

Yang et al. reconstituted the cross-feeding ecotypes that had evolved from one ancestral clone. Consortia were directly competed against that ancestor, and the three-member differentiated consortium had higher relative fitness than the ancestor and all evolved monocultures.

For the consortium competition, evolved strains were first reconstituted at their established internal steady-state ratios and then an equal number of GFP-labeled ancestor cells was added. This gives one architecture-level S:D competition point.

The missing experiment is therefore:

```text
freeze the internal D consortium ratio,
repeat ancestor-versus-consortium competitions at multiple total S:D starting frequencies,
and estimate Delta(p) without changing the architecture labels.
```

This still carries `O_UNIT` because D is a multigenotype consortium, but the actual evolutionary S-to-D origin and common-scale competition make it the closest empirical direct-comparison complement to Streptomyces.

## Key consequence

The current literature is not missing either ingredient separately.

```text
frequency dependence exists in many real systems;
division-of-labor / integrated-versus-specialized architectures exist in many real systems;
actual S-to-D evolutionary transitions and direct S:D competitions also exist.
```

What remains missing is their intersection on the same strategic unit and multiple architecture frequencies:

```text
heritable integrated architecture S
        versus
heritable architecture D that generates/encodes differentiated function
        across
multiple S:D resident frequencies
        with
common relative fitness.
```

This is a sharper empirical target than another broad search for frequency-dependent selection or another broad search for division of labor.

## Search stop rule

Do not promote a study merely because it contains both the words `generalist/specialist` and `frequency dependence`.

For each new candidate, fill P1--P6 first. If one of P1, P3, P4, or P5 fails structurally, retain it as analogue evidence and stop attempting to estimate PAYOFF architecture `eta` from that study.

## Current status

```text
LANE_P_INTERSECTION_RULE_FROZEN
MICROBIAL_NEAR_P_OBSTRUCTION_CLASSES_RECOVERED
STREPTOMYCES_ARCHITECTURE_NEAR_P_INTERSECTION_RECOVERED_BUT_FREQUENCY_UNIT_MISMATCHED
EVOLVED_ECOLI_S_TO_D_DIRECT_COMPETITION_RECOVERED_BUT_MULTI_FREQUENCY_SERIES_MISSING
DIRECT_EMPIRICAL_S_D_FREQUENCY_INTERSECTION_NOT_YET_RECOVERED
PAYOFF_ARCHITECTURE_FREQUENCY_FEEDBACK_NOT_YET_IDENTIFIED
```
