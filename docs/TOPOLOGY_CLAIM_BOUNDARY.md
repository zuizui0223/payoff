# Topology-game claim boundary

The topology extension connects edgewise modularization to pairwise evolutionary games and rare-mutation substitution chains. Several formulas are exact under declared assumptions, but none should be generalized beyond those assumptions without a new derivation.

## 1. Binary vertex topologies are conditional on linear edge costs

`EDGEWISE_MODULARIZATION.md` proves that with convex recovery and **linear** edge-decoupling cost, at least one global optimizer exists at a vertex of the coupling box.

This does not mean:

```text
all biological coupling strengths must be binary,
all local optima are vertices,
or partial edge strengths are impossible.
```

Sufficiently convex architecture costs can stabilize graded couplings.

## 2. Weighted Hamming feedback is a registered ecological kernel, not a universal topology metric

The topology game uses

```text
q(S,T)=sum_e w_e(s_e-t_e)^2
```

and

```text
H(S,T)=-gamma q(S,T).
```

This is a simple symmetric distance kernel chosen to make topology differences explicit and auditable.

Real ecological effects can depend on:

```text
which particular modules differ,
higher-order edge combinations,
directionality,
stage structure,
spatial context,
or nonmetric topology features.
```

The exact pairwise reduction

```text
phi_ST=b_T-b_S,
eta_ST=gamma q_ST
```

belongs to this declared kernel.

## 3. Pairwise topology coexistence does not guarantee stable coexistence in a many-topology population

Two topology strategies may satisfy the canonical negative-frequency coexistence condition when considered alone. A third topology can invade that pair or change the potential optimum.

Pairwise classification is therefore a necessary local diagnostic, not a complete many-strategy community classification.

## 4. The rare-mutation Gibbs law is a monomorphic-substitution limit

Under connected symmetric topology mutation and the declared exponential Moran process,

```text
Pi_S proportional to exp[beta(N-2)b_S].
```

This result assumes mutation is sufficiently rare that the population effectively reaches a monomorphic state between successful topology mutations.

When negative-frequency topology feedback creates a long-lived interior polymorphism, finite populations still eventually absorb without mutation, but the absorption time can be very long. If new mutations arrive before absorption, the monomorphic substitution-chain reduction is invalid.

Then one must model the full recurrent-mutation population process rather than use the topology Gibbs law.

## 5. Gamma cancels from stationary monomorphic weights, not from evolutionary dynamics

In the declared symmetric weak-mutation chain, `gamma q` cancels from reciprocal fixation ratios and therefore from stationary monomorphic weights.

It still affects:

```text
absolute fixation probabilities,
substitution rates,
waiting times,
metastability,
and whether the weak-mutation approximation is biologically plausible.
```

Do not write:

> topology interactions do not matter in finite populations.

Preferred:

> Under symmetric rare topology mutation and exponential Moran fitness, topology-distance feedback changes substitution kinetics but cancels from the reversible monomorphic stationary weights.

## 6. Intrinsic valley depth is not a mean first-passage time

The path diagnostic

```text
B(S->G)
=max[0,b_S-best_path_bottleneck]
```

identifies whether every single-edge route crosses an intrinsic-payoff valley.

Actual escape kinetics depend on

```text
N,
beta,
gamma,
mutation rates,
edge weights,
and fixation probabilities.
```

Do not convert `B` directly into an escape time without a stochastic derivation.

## 7. Endpoint and topology polymorphisms are model predictions, not historical reconstructions

A stable topology mixture or endpoint architecture polymorphism does not show that historical modularity evolved by a specific branching sequence.

Historical claims require independent phylogenetic, developmental, genetic, or experimental evidence.

## Preferred manuscript language

Preferred:

> Edgewise phenotype optimization supplies intrinsic topology payoffs, and a symmetric topology-distance kernel maps every topology pair onto the canonical PAYOFF parameters `phi=b_T-b_S` and `eta=gamma q_ST`.

Avoid:

> Graph topologies naturally play a universal Hamming-distance evolutionary game.

Preferred:

> Under the declared symmetric rare-mutation Moran process, stationary monomorphic topology weights depend only on intrinsic optimized topology payoffs, while topology interactions remain visible in substitution kinetics.

Avoid:

> Frequency dependence has no effect on topology evolution.
