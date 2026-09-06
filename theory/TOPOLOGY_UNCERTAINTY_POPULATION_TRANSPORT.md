# Topology uncertainty transport — from architecture support to population-phase support

`TOPOLOGY_UNCERTAINTY_AND_SUPPORT.md` distinguishes uncertainty in the first constrained edge, final global topology, and accessibility path.

This note carries the same uncertainty draws one level further into the population game.

The key point is:

> Uncertainty in which topology is intrinsically best does not imply equal uncertainty in the population-level relation among the top competing architectures.

---

## 1. Draw-specific top pair

For uncertainty draw `b`, let

```text
S_b
```

be the best intrinsic vertex topology and

```text
T_b
```

be its runner-up.

Their intrinsic payoffs are

```text
b_S,b_T
```

with

```text
b_S>b_T
```

away from ties.

Under the registered topology-distance feedback

```text
H(S,T)=-gamma q(S,T),
```

the pair has canonical PAYOFF coordinates

```text
phi_b
=b_T-b_S<0,

eta_b
=gamma q(S,T).
```

These coordinates are recomputed in every uncertainty draw after topology optimization. Population parameters are not used to select `S_b` or `T_b`.

---

## 2. Population support is a different ensemble object

Define the draw-specific pair phase

```text
C_b
in {
  first dominance,
  second dominance,
  stable coexistence,
  coordination,
  boundary
}.
```

Then

```text
P_hat_phase(C)
= #{b:C_b=C}/B
```

is **population-phase support**.

Likewise define

```text
P_hat_both-invade
= #{b:I_T,b>0 and I_S,b>0}/B.
```

These quantities can be more robust than

```text
P_hat_best(S).
```

For example, the identity of the intrinsic best topology may swap across uncertainty draws while the same unordered pair remains at the top and remains inside the same coexistence wedge.

---

## 3. Unordered top-pair support

Because best/runner-up orientation can reverse, PAYOFF separately records

```text
{S_b,T_b}
```

as an unordered pair.

Define

```text
P_hat_pair({S,T})
= #{b:{S_b,T_b}={S,T}}/B.
```

This can reveal a stable competitive architecture set even when ranking within the set is uncertain.

Biologically:

```text
best-topology support
```

asks

> Which architecture has the largest intrinsic optimized payoff?

whereas

```text
top-pair support
```

asks

> Which architecture alternatives consistently form the relevant competitive neighborhood?

---

## 4. Finite-population ordering is transported draw by draw

For population size `N` and exponential-fitness intensity `beta`, the exact reciprocal fixation ratio in each draw is

```text
rho_T/rho_S
=exp[beta(N-2)phi_b].
```

Because `S_b` is the intrinsic best by construction,

```text
phi_b<0
```

and therefore, for `N>2,beta>0`,

```text
rho_S>rho_T.
```

This produces another support quantity:

```text
P_hat_fix-best
= #{b:rho_S>rho_T}/B.
```

In the absence of exact payoff ties this equals one by the registered pairwise Moran theorem, even when the identity of `S_b` itself changes across draws.

Thus:

```text
which named topology is best
```

can be uncertain while

```text
the intrinsic best has larger reciprocal fixation probability
```

is theoremically stable under the declared process.

---

## 5. Registered five-draw synthetic result

The three-function fixture uses

```text
gamma=-1/4,
N=20,
beta=0.4.
```

Across its five uncertainty draws:

```text
best topology 011:               4/5
best topology 111:               1/5

unordered top pair {011,111}:    5/5
stable pairwise coexistence:     5/5
both top architectures invade:   5/5
intrinsic best has larger
reciprocal fixation probability: 5/5.
```

So the synthetic hierarchy is

```text
first conflict edge            support 1.0
greedy local endpoint 011      support 1.0
named global best 011          support 0.8
relevant top pair 011--111     support 1.0
stable coexistence of top pair support 1.0.
```

This is exactly why uncertainty should be transported through each estimand rather than summarized once at the upstream parameter level.

---

## 6. Context and fitness-scale lock

`PAYOFF_TOPOLOGY_ENSEMBLE_V1` can carry the root identity block

```text
context_id
system
population_id
season_id
fitness_scale_id.
```

For empirical use these should be inherited unchanged from the registered cross-repository context.

The synthetic fixture uses synthetic identifiers only.

If draws mix different biological contexts or fitness scales, ensemble support is not interpretable as uncertainty about one topology problem.

---

## 7. Population parameters are frozen downstream

The registered workflow is

```text
uncertain upstream architecture inputs
-> per-draw intrinsic topology landscape
-> choose best and runner-up within each draw
-> freeze gamma,N,beta
-> transport top pair into population receipts.
```

Do not choose `gamma` separately in each draw to force one population phase.

A sensitivity analysis over population parameters is valid, but it should form another declared outer loop rather than an adaptive fit to the topology results.

---

## 8. Claim boundary

Appropriate:

> The identity of the intrinsic best topology varied across the registered draws, but the same two topology states formed the top competitive pair in all draws and were predicted to reciprocally invade under the frozen negative-frequency feedback.

Avoid:

> The data prove that both topologies coexist in nature.

Population-phase support remains conditional on the declared architecture kernel, `gamma`, population process, and upstream identification assumptions.
