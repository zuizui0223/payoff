# PAYOFF claim boundary

PAYOFF is intended to make the game-theoretic extension precise without overclaiming what the mathematics or sister repositories establish.

## What the model does establish

Under the declared quadratic loss, residual-coupling, linear frequency-feedback, and finite-population assumptions:

1. the one-coordinate compromise is unique;
2. the shared conflict load is exact;
3. the `n`-function shared conflict load equals weighted pairwise disagreement;
4. the optimized differentiated coordinates are exact;
5. realized trait separation `s` exactly equals the fraction of shared conflict loss recovered, so `R=sL`;
6. architecture payoff difference is exactly `phi=sL-K`;
7. under the declared linear frequency-feedback game, replicator equilibria and their local stability are analytically classified;
8. the static architecture crossing splits into reciprocal invasion surfaces `K=R-eta` and `K=R+eta`;
9. the game-generated middle region has exact cost width `2|eta|`;
10. reciprocal neutral-cost thresholds algebraically identify `R` and `eta` when both thresholds are experimentally accessible;
11. along a linear environmental path `phi(e)=alpha(e-e0)`, the two game transitions have exact width `2|eta|/|alpha|`;
12. the two-strategy symmetric game has a mean-payoff Lyapunov function with nonnegative derivative;
13. inside negative-feedback coexistence, the sign of `phi` determines whether `D` is minority or majority;
14. inside positive-feedback coordination, the sign of `phi` determines deterministic basin-size risk dominance;
15. switching costs create the stated no-switch / hysteresis interval;
16. under self-excluding pairwise interactions and exponential payoff-to-fitness mapping, the finite-population payoff gap `Delta_N(i)` and single-mutant Moran fixation probabilities are exact;
17. under that finite Moran model, `rho_D/rho_S=exp[beta phi(N-2)]`, so the sign of `phi` exactly orders reciprocal fixation probabilities for `N>2`, `beta>0`;
18. under weak selection, `rho_D>1/N` iff `3phi>eta` and `rho_S>1/N` iff `-3phi>eta` for the declared game;
19. the corresponding weak-selection stochastic-core width on the cost scale is `2|eta|/3`.

## What the model does not establish

### Functions are not literal strategic agents

The biological functions in SCH are payoff components, not autonomous players choosing actions. Calling them players is a metaphor only.

The literal evolutionary-game layer begins when alternative heritable architectures `S` and `D` have frequency-dependent reproductive payoffs in a population.

### `eta` is not identified by SCH, BALANCE, or BITA

`eta` is a new PAYOFF parameter. It requires evidence that relative fitness of `D` versus `S` changes with architecture frequency.

Without such evidence, the justified model is the frequency-independent baseline `eta=0`.

### Algebraic threshold inversion is not empirical identification by itself

The identities

```text
R=(K_D+K_S)/2
eta=(K_S-K_D)/2
```

show what two neutral invasion thresholds would identify under the model. They do not show that a given system permits manipulation of architecture cost while holding `R` and `eta` fixed, nor that both thresholds lie in a biologically feasible range.

### The quadratic identity is not universal

`R=sL` is exact for the declared quadratic residual-coupling model. More general convex models need not preserve this exact scalar identity.

### Linear frequency feedback is a local/minimal model

```text
Delta(p)=phi+eta(2p-1)
```

is the minimal affine frequency-feedback model. Nonlinear, asymmetric, spatial, stage-structured, or density-dependent interactions can produce additional equilibria and re-entry not represented by the two-plane phase diagram.

### The finite-population fixation formula is model-specific

The exact finite-population formulas use:

```text
- a well-mixed population of fixed size N,
- random pairwise interaction,
- exclusion of self-interaction,
- Moran birth-death updating,
- exponential payoff-to-fitness mapping f=exp(beta*pi).
```

Changing update rule, population structure, interaction network, mutation regime, inheritance, or payoff-to-fitness mapping can change exact fixation probabilities and finite-selection thresholds.

### The one-third law is not a PAYOFF discovery

The one-third law is established prior theory in finite-population evolutionary games. PAYOFF only maps its criterion onto the ecological architecture quantities through

```text
phi=sL-K.
```

Appropriate novelty language concerns the cross-scale bridge, not the one-third rule itself.

### Exact reciprocal-fixation ordering is conditional on exponential fitness

The result

```text
rho_D/rho_S=exp[beta phi(N-2)]
```

is exact for the declared exponential Moran model. The cancellation of `eta` from this ratio should not be claimed as universal across arbitrary stochastic evolutionary processes.

### Weak-selection statements are first-order statements

The tests

```text
3phi>eta
and
-3phi>eta
```

compare fixation probability with `1/N` in the weak-selection limit. At stronger selection, the exact fixation expression should be evaluated rather than applying the weak-selection inequalities as universal thresholds.

### Risk dominance is model-specific terminology here

Inside the strict `eta>0` coordination wedge, `risk dominant` refers to the pure architecture with the larger deterministic basin of attraction under the declared one-dimensional replicator dynamics. It is not a claim that every stochastic or equilibrium-selection definition gives the same empirical outcome.

### Differentiation is not historical splitting

A present-day fitness advantage of a differentiated architecture does not prove that the modeled conflict caused its historical origin. Historical claims require independent evidence.

### Structural separation is not functional independence

Finite residual coupling `c` is explicitly allowed. Multiple trait axes can remain strongly integrated.

### A mixed ESS is not automatically a stable species-level polymorphism

Mutation, drift, demography, spatial structure, assortative interaction, linkage, inheritance architecture, and finite-population effects can alter realized dynamics.

### Positive frequency dependence and switching hysteresis are distinct

`eta>0` creates a coordination threshold from current frequency dependence. `C_SD,C_DS>0` create path dependence from transition costs. Either can occur without the other.

## Appropriate manuscript language

Preferred:

> We derive a minimal evolutionary game in which ecological conflict determines the baseline payoff difference between integrated and differentiated trait architectures, while frequency-dependent ecological feedback determines dominance, coexistence, or coordination.

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

> Under the declared exponential Moran process, the sign of `phi=sL-K` exactly orders reciprocal single-mutant fixation probabilities, while `eta` controls their absolute values.

Avoid:

> Frequency dependence never affects which architecture fixes more readily in finite populations.

Preferred:

> Under weak selection, the established one-third law maps onto the architecture criterion `3(sL-K)>eta`.

Avoid:

> PAYOFF discovers a new one-third law for trait architecture.

Preferred:

> The framework predicts conditions under which differentiated and shared architectures can each be evolutionarily stable or stochastically favored.

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
FINITE_MORAN_FIXATION_FORMULA_PROVED_UNDER_DECLARED_PROCESS
RECIPROCAL_FIXATION_RATIO_PROVED_UNDER_EXPONENTIAL_FITNESS
WEAK_SELECTION_ARCHITECTURE_ONE_THIRD_MAPPING_PROVED
FINITE_STOCHASTIC_CORE_WIDTH_PROVED_UNDER_WEAK_SELECTION
EMPIRICAL_FREQUENCY_FEEDBACK_NOT_YET_IDENTIFIED
FINITE_POPULATION_EMPIRICAL_TEST_NOT_YET_EXECUTED
HISTORICAL_CAUSATION_NOT_IDENTIFIED
```
