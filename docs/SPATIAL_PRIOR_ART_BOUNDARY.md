# Spatial prior-art boundary for PAYOFF

PAYOFF does not claim that spatial evolutionary games, graph-structured selection, migration-coupled populations, synchronization, or bistable patch mosaics are new.

## Established theory

### Evolutionary games on graphs

Ohtsuki, Hauert, Lieberman & Nowak (2006), *A simple rule for the evolution of cooperation on graphs and social networks*, Nature 441:502-505, established influential graph-structured evolutionary-game results.

Ohtsuki & Nowak (2006) and related work derived graph/cycle evolutionary dynamics and graph analogues of replicator behavior under several update rules.

These works already establish that population structure and who-interacts-with-whom can change evolutionary-game outcomes.

### Migration-coupled and bistable patch systems

Coupled-patch systems with local bistability, migration-driven synchronization, critical coupling, and spatially heterogeneous metastable states are established dynamical-systems and metapopulation topics.

PAYOFF therefore does not claim to invent migration thresholds, synchronization, or polarized patch states as general phenomena.

## PAYOFF-specific contribution candidate

The defensible contribution is the architecture parameter bridge:

```text
SCH conflict load L
-> BITA recovery R=sL
-> architecture gap phi=R-K
-> frequency feedback eta
-> spatial patch game
```

followed by exact results for the declared model:

```text
mean spatial correction
= V[eta(3-6mu)-phi]-2eta T;

graph mode rate
= f'(p*)-m lambda_k;

two-patch phi=0 polarized branch
x^2=1/4-m/eta;

stable polarization threshold
m=eta/6;

polarization existence threshold
m=eta/4.
```

The novelty language should therefore be

```text
we derive the spatial consequences of the ecology-calibrated architecture game
```

rather than

```text
we introduce spatial evolutionary games
we discover synchronization by migration
we discover bistable spatial mosaics.
```

## Why PAYOFF uses a patch model before microscopic graph updating

Microscopic evolutionary graph theory requires an explicit replacement/update rule, interaction graph, demographic timing, and usually a weak-selection or finite-population approximation.

The first spatial PAYOFF extension instead uses conservative migration among local architecture-frequency patches because this keeps the upstream empirical quantities `phi` and `eta` unchanged and yields exact deterministic theorems.

A later stochastic graph layer can be added, but it should be treated as another model with another update-rule-specific claim ceiling rather than silently identified with the patch-migration results.
