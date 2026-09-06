# PAYOFF claim boundary

PAYOFF is intended to make the game-theoretic extension precise without overclaiming what the mathematics or sister repositories establish.

## What the model does establish

Under the declared quadratic loss and residual-coupling assumptions:

1. the one-coordinate compromise is unique;
2. the shared conflict load is exact;
3. the `n`-function shared conflict load equals weighted pairwise disagreement;
4. the optimized differentiated coordinates are exact;
5. realized trait separation `s` exactly equals the fraction of shared conflict loss recovered, so `R=sL`;
6. architecture payoff difference is exactly `phi=sL-K`;
7. under the declared linear frequency-feedback game, replicator equilibria and their local stability are analytically classified;
8. switching costs create the stated no-switch / hysteresis interval.

## What the model does not establish

### Functions are not literal strategic agents

The two biological functions in SCH are payoff components, not autonomous players choosing actions. Calling them players is a useful metaphor only.

The literal evolutionary-game layer begins when alternative heritable architectures `S` and `D` have frequency-dependent reproductive payoffs in a population.

### `eta` is not identified by SCH, BALANCE, or BITA

`eta` is a new PAYOFF parameter. It requires evidence that the relative fitness of `D` versus `S` changes with architecture frequency.

Without such evidence, the justified model is the frequency-independent baseline `eta=0`.

### The quadratic identity is not universal

`R=sL` is exact for the declared quadratic residual-coupling model. More general convex models preserve the nesting intuition that extra phenotype dimensions cannot reduce the pre-cost optimized fit when the shared phenotypes remain accessible, but they need not preserve this exact scalar identity.

### Differentiation is not historical splitting

A present-day fitness advantage of a differentiated architecture does not prove that the modeled conflict caused its historical origin.

Historical claims require phylogenetic, developmental, genetic, or other independent evidence.

### Structural separation is not functional independence

Finite residual coupling `c` is explicitly allowed. Multiple trait axes can remain strongly integrated.

### A mixed ESS is not automatically a stable species-level polymorphism

The replicator result is a deterministic population model. Mutation, drift, demography, spatial structure, assortative interaction, linkage, inheritance architecture, and finite-population effects can alter realized dynamics.

### Positive frequency dependence and switching hysteresis are distinct

`eta>0` creates a coordination threshold from current frequency dependence. `C_SD,C_DS>0` create path dependence from transition costs. Either can occur without the other.

## Appropriate manuscript language

Preferred:

> We derive a minimal evolutionary game in which ecological conflict determines the baseline payoff difference between integrated and differentiated trait architectures, while frequency-dependent ecological feedback determines whether selection yields dominance, stable coexistence, or a coordination threshold.

Avoid:

> Biological functions play a Nash game and decide whether to split traits.

Preferred:

> In the quadratic bridge, realized dimensional separation exactly equals the fraction of shared compromise loss recovered.

Avoid:

> Trait separation always recovers the same fraction of fitness loss in arbitrary landscapes.

Preferred:

> The framework predicts conditions under which differentiated and shared architectures can each be evolutionarily stable.

Avoid:

> The framework proves that modularity evolved by this mechanism in the empirical systems reviewed by SCH or BITA.

## Current status labels

```text
QUADRATIC_SHARED_COMPROMISE_PROVED
N_FUNCTION_DISAGREEMENT_IDENTITY_PROVED
QUADRATIC_PARTIAL_RELEASE_PROVED
R_EQUALS_sL_PROVED_UNDER_DECLARED_MODEL
STATIC_THREE_WORLD_PARTITION_PROVED
LINEAR_FREQUENCY_GAME_PHASES_PROVED
SWITCHING_HYSTERESIS_BAND_PROVED
EMPIRICAL_FREQUENCY_FEEDBACK_NOT_YET_IDENTIFIED
HISTORICAL_CAUSATION_NOT_IDENTIFIED
```
