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
| *Bacillus subtilis* biofilm matrix, Dragoš et al. 2018 | WT/generalist makes EPS+TasA; engineered genetic specialists partition EPS versus TasA and complement each other | Strong negative frequency dependence between the two specialists; stable ~30% TasA-producer ratio in vitro and on roots | Genetic division of labor can outperform incomplete/generalist production and specialist ratio converges to productivity optimum | `O_UNIT + O_FREQ`: frequency axis is specialist A versus specialist B, not WT S versus differentiated consortium D | `NEAR_P_ARCHITECTURE_STRONG_FREQUENCY_WITHIN_D_ONLY` |
| *Pseudomonas aeruginosa* siderophores, Mridha et al. 2022 | WT is explicit generalist producing pyochelin+pyoverdine; engineered specialists each produce one siderophore | Specialist relative fitness is measured across initial specialist mixing ratios and shows negative frequency dependence | Specialist-mixture productivity is compared on the same growth scale with WT and changes relative to WT across iron environments | `O_UNIT + O_FREQ`: WT is not competed against the specialist consortium across a WT:D frequency axis | `NEAR_P_COMMON_SCALE_PLUS_WITHIN_D_FREQUENCY` |
| synthetic *E. coli* organic-acid division of labor, Beck et al. 2022 | WT generalist performs complete catabolism; producer+consumer guilds collectively have the same genomic potential and partition the pathway | No reported WT-versus-consortium frequency series | Consortium versus WT performance reverses with environmental buffering; public supplementary data and code are available | `O_UNIT + O_FREQ + O_ENDPOINT`: static/contextual S-versus-consortium comparison, no mixed S:D competition | `NEAR_P_STATIC_S_D_PAYOFF_CONTEXT_SWITCH` |
| *Pseudomonas stutzeri* denitrification cross-feeding, Schink et al. 2022 | complete-pathway generalist versus nitrite-only specialist | Reciprocal initial-ratio assays directly test whether each type increases from rare; coexistence recovered in a bounded pH context | Direct generalist-specialist frequency-dependent relative growth on a common cell-growth scale | `O_ARCH + O_TASK`: specialist is a partial-pathway consumer, not a differentiated architecture that independently/collectively replaces the generalist as the same heritable unit | `NEAR_P_DIRECT_FREQUENCY_WRONG_ARCHITECTURE_CONTRAST` |
| *E. coli* sugar-use chemostats, Dykhuizen & Davies 1980 | generalists use maltose+lactose; specialists lack lactose use | Generalist-specialist coexistence and equilibrium frequencies measured experimentally | Direct generalist-specialist competition with environment-dependent equilibrium | `O_ARCH`: niche breadth specialization is not the declared conflict-release architecture mapping | `GENERIC_GENERALIST_SPECIALIST_GAME_ANALOGUE` |
| *Streptomyces* genome-fragility division of labor, Colizzi et al. 2023 | genome architecture generates sterile antibiotic specialists from replicating progenitors, directly resolving replication-production trade-off | Colony competition exists in the multiscale model; generalist versus division-of-labor architectures are compared computationally | Heritable genome architecture is unusually close to PAYOFF's integrated-versus-differentiated architecture concept | `O_SIM + O_FREQ`: decisive architecture competition is computational and no empirical S:D frequency series is recovered | `NEAR_P_ARCHITECTURE_EXCELLENT_SIMULATION_FREQUENCY_ONLY` |

## Key consequence

The current literature is not missing either ingredient separately.

```text
frequency dependence exists in many real systems;
division-of-labor / integrated-versus-specialized architectures exist in many real systems.
```

What remains missing is their intersection on the same strategic unit:

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
DIRECT_EMPIRICAL_S_D_FREQUENCY_INTERSECTION_NOT_YET_RECOVERED
PAYOFF_ARCHITECTURE_FREQUENCY_FEEDBACK_NOT_YET_IDENTIFIED
```
