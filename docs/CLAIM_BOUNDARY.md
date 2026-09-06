# PAYOFF claim boundary

PAYOFF is intended to make the game-theoretic extension precise without overclaiming what the mathematics or sister repositories establish.

## What the model does establish

Under the declared quadratic loss, residual-coupling, and linear frequency-feedback assumptions:

1. the one-coordinate compromise is unique;
2. the shared conflict load is exact;
3. the `n`-function shared conflict load equals weighted pairwise disagreement;
4. the optimized differentiated coordinates are exact;
5. realized trait separation `s` exactly equals the fraction of shared conflict loss recovered, so `R=sL`;
6. architecture payoff difference is exactly `phi=sL-K`;
7. under the declared linear frequency-feedback game, replicator equilibria and their local stability are analytically classified;
8. the static architecture crossing splits into the reciprocal invasion surfaces `K=R-eta` and `K=R+eta`;
9. the game-generated middle region has exact cost width `2|eta|`;
10. reciprocal neutral-cost thresholds algebraically identify `R` and `eta` when both thresholds are experimentally accessible;
11. along a linear environmental path `phi(e)=alpha(e-e0)`, the two game transitions have exact width `2|eta|/|alpha|`;
12. the two-strategy symmetric game has mean-payoff Lyapunov function `V`, with `dV/dt=2p(1-p)Delta^2>=0`;
13. inside the negative-feedback coexistence wedge, the sign of `phi` determines whether `D` is the minority or majority architecture;
14. inside the positive-feedback coordination wedge, the sign of `phi` determines deterministic basin-size risk dominance;
15. switching costs create the stated no-switch / hysteresis interval.

## What the model does not establish

### Functions are not literal strategic agents

The biological functions in SCH are payoff components, not autonomous players choosing actions. Calling them players is a metaphor only.

The literal evolutionary-game layer begins when alternative heritable architectures `S` and `D` have frequency-dependent reproductive payoffs in a population.

### `eta` is not identified by SCH, BALANCE, or BITA

`eta` is a new PAYOFF parameter. It requires evidence that the relative fitness of `D` versus `S` changes with architecture frequency.

Without such evidence, the justified model is the frequency-independent baseline `eta=0`.

### Algebraic threshold inversion is not empirical identification by itself

The identities

```text
R=(K_D+K_S)/2
eta=(K_S-K_D)/2
```

show what two neutral invasion thresholds would identify under the model. They do not show that a given system permits manipulation of architecture cost while holding `R` and `eta` fixed, nor that both thresholds lie in a biologically feasible range.

### The quadratic identity is not universal

`R=sL` is exact for the declared quadratic residual-coupling model. More general convex models preserve the nesting intuition that extra phenotype dimensions cannot reduce the pre-cost optimized fit when shared phenotypes remain accessible, but they need not preserve this exact scalar identity.

### Linear frequency feedback is a local/minimal model

```text
Delta(p)=phi+eta(2p-1)
```

is the minimal affine frequency-feedback model. Nonlinear, asymmetric, spatial, stage-structured, or density-dependent interactions can produce additional equilibria and re-entry not represented by the two-plane phase diagram.

### Risk dominance is model-specific terminology here

Inside the strict `eta>0` coordination wedge, `risk dominant` refers to the pure architecture with the larger deterministic basin of attraction under the declared one-dimensional replicator dynamics. It is not a claim that every finite-population, stochastic, mutation-selection, or equilibrium-selection definition of risk dominance gives the same empirical outcome.

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

> Under linear frequency feedback, one static architecture crossing splits into two reciprocal invasion surfaces whose separation is `2|eta|` on the cost scale.

Avoid:

> Every ecological architecture transition has two universal thresholds.

Preferred:

> Within the declared coordination game, the sign of the static payoff gap determines which pure architecture has the larger deterministic basin.

Avoid:

> Positive static payoff proves that differentiation will evolve from rarity.

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
RECIPROCAL_INVASION_SURFACES_PROVED
GAME_MIDDLE_WIDTH_PROVED
RECIPROCAL_THRESHOLD_INVERSION_PROVED_UNDER_DECLARED_HOLD_FIXED_DESIGN
LINEAR_ENVIRONMENTAL_THRESHOLD_SPLIT_PROVED
TWO_STRATEGY_POTENTIAL_LYAPUNOV_PROVED
COEXISTENCE_COMPOSITION_BOUNDARY_PROVED
COORDINATION_RISK_DOMINANCE_BOUNDARY_PROVED
SWITCHING_HYSTERESIS_BAND_PROVED
EMPIRICAL_FREQUENCY_FEEDBACK_NOT_YET_IDENTIFIED
HISTORICAL_CAUSATION_NOT_IDENTIFIED
```
