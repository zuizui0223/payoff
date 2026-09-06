# Rare mutation on the topology graph — stationary architecture abundance versus evolutionary accessibility

Discrete modular topologies naturally form a mutation graph. If architectural mutations usually alter one coupling edge at a time, vertex architectures are nodes of a hypercube and mutation connects Hamming-neighbor topologies.

This note combines that mutation graph with the exact pairwise topology PAYOFF reduction.

The main result separates two questions:

```text
Which topology dominates long-run monomorphic occupancy?
```

from

```text
How difficult is it to reach that topology through single-edge mutations?
```

Under the declared rare-mutation exponential Moran process, the first question has a simple exact answer; the second retains topology-distance and fitness-valley information.

---

## 1. Rare-mutation topology chain

Let topology states be

```text
S,T,...
```

with intrinsic optimized payoffs

```text
b_S,b_T,...
```

and pairwise topology-distance feedback

```text
eta_ST=gamma q(S,T).
```

Assume a finite population of size `N` and exponential payoff-to-fitness mapping with selection strength `beta`.

Let architectural mutation rates be

```text
mu_ST>=0.
```

In the rare-mutation limit, the population spends almost all of its time monomorphic. A mutation from resident topology `S` to mutant topology `T` produces a topology substitution with rate proportional to

```text
Q_ST
=mu_ST rho(T|S),
```

where `rho(T|S)` is the exact single-mutant Moran fixation probability of `T` in resident `S`.

For a topology pair,

```text
phi_ST=b_T-b_S,
eta_ST=gamma q(S,T).
```

---

## Theorem TRM1 — reciprocal topology substitution ratio

For every mutually connected topology pair,

```text
rho(T|S)/rho(S|T)
=exp[beta(N-2)(b_T-b_S)].
```

Therefore

```text
Q_ST/Q_TS
=
(mu_ST/mu_TS)
exp[beta(N-2)(b_T-b_S)].
```

The topology-distance feedback `gamma q(S,T)` cancels from the reciprocal fixation ratio.

---

## Theorem TRM2 — exact stationary topology law under symmetric mutation

Assume the topology mutation graph is connected and mutation is symmetric on every allowed edge:

```text
mu_ST=mu_TS>0.
```

Then the rare-mutation monomorphic topology chain is reversible with stationary distribution

```text
Pi_S
=
exp[beta(N-2)b_S]
/
sum_U exp[beta(N-2)b_U].
```

### Proof

Let

```text
w_S=exp[beta(N-2)b_S].
```

For an allowed pair,

```text
w_S Q_ST/(w_T Q_TS)
=
exp[beta(N-2)(b_S-b_T)]
*rho(T|S)/rho(S|T)
=1.
```

Symmetric mutation cancels. Hence detailed balance holds:

```text
Pi_S Q_ST=Pi_T Q_TS.
```

Connectedness gives the unique stationary distribution. QED.

---

## Corollary TRM2.1 — topology interaction changes kinetics but not symmetric-mutation stationary weights

Under this declared process,

```text
gamma
```

and

```text
q(S,T)
```

can strongly change the absolute fixation probabilities and therefore the substitution rates

```text
Q_ST.
```

But they do not appear in the stationary monomorphic weights `Pi_S` when mutation is symmetric.

Thus:

```text
stationary abundance
!=
transition kinetics.
```

A topology can have the largest long-run occupancy while still being very slow to reach from a local architecture state.

---

## Corollary TRM2.2 — neutral-selection control

At

```text
beta=0,
```

and symmetric mutation on a connected topology graph,

```text
Pi_S=1/M
```

for all `M` topology states.

---

## Theorem TRM3 — reversible asymmetric mutation adds a topology mutational prior

More generally, suppose mutation rates are reversible with positive weights `nu_S`:

```text
nu_S mu_ST
=nu_T mu_TS
```

for every allowed pair.

Then the rare-mutation stationary law is

```text
Pi_S
propto
nu_S exp[beta(N-2)b_S].
```

Thus reversible mutation bias and intrinsic architecture quality combine multiplicatively, or additively on a log scale:

```text
log Pi_S
=constant
+log nu_S
+beta(N-2)b_S.
```

This is the topology analogue of PAYOFF's earlier mutation-bias-plus-selection occupancy receipt.

---

## 2. Single-edge accessibility

Stationary weights do not answer whether a topology is easy to reach.

Assume mutations are restricted to single-edge flips. Two binary release topologies are mutational neighbors iff their Hamming distance is one.

Define a topology `S` to be a **single-edge local intrinsic optimum** if

```text
b_S >= b_T
```

for every one-edge neighbor `T`.

A different topology `G` can still satisfy

```text
b_G>b_S.
```

Then the population faces an architecture-accessibility problem even though the long-run stationary law prefers `G`.

---

## 3. Intrinsic topology valley depth

For a single-edge path

```text
P=(S=S_0,S_1,...,S_k=G),
```

define its bottleneck payoff

```text
m(P)=min_i b_{S_i}.
```

Among all single-edge paths, define the best bottleneck

```text
m*(S,G)=max_P m(P).
```

The intrinsic valley depth is

```text
B(S->G)
=max[0,b_S-m*(S,G)].
```

---

## Theorem TRM4 — zero barrier is equivalent to a nondecreasing-payoff-accessible corridor above the source level

```text
B(S->G)=0
```

iff there exists a single-edge path from `S` to `G` along which every visited topology has intrinsic payoff at least `b_S`.

If

```text
B(S->G)>0,
```

then every single-edge route to `G` must pass through at least one topology with lower intrinsic payoff than `S` by at least `B`.

### Interpretation

`B` is a geometric accessibility diagnostic. It is **not** automatically equal to a mean first-passage time or a fixation exponent, because actual substitution kinetics also depend on:

```text
N,
beta,
gamma,
q(S,T),
mu_ST.
```

---

## 4. Connection to the finite-jump modularization barrier

`DISCONTINUOUS_MODULARIZATION_BARRIER.md` showed that with convex recovery and linear decoupling cost, a fully released architecture can have higher payoff even when infinitesimal decoupling is selected against.

The topology graph gives the multi-edge counterpart:

```text
local one-edge optimum S
        |
        | every neighbor lower
        v
positive topology valley B
        |
        | multi-edge coordinated jump or drift may cross
        v
globally better topology G.
```

Thus PAYOFF now distinguishes:

```text
architecture payoff optimum,
local edge-release accessibility,
single-edge mutation accessibility,
and long-run rare-mutation stationary abundance.
```

They are different estimands.

---

## 5. Empirical / simulation handoff

For a small candidate coupling graph:

```text
1. enumerate vertex topologies;
2. compute b_S=R(S)-K(S);
3. choose a biologically justified topology mutation graph;
4. estimate topology-distance feedback gamma;
5. predict pairwise fixation rho(T|S);
6. predict stationary Pi_S under the declared mutation model;
7. compute local optima and intrinsic valley depths;
8. compare observed transition frequencies and occupancy separately.
```

A strong test would deliberately choose two starting topologies with similar stationary predictions but different valley depths, or vice versa.

---

# Prior-art / claim boundary

Weak-mutation substitution chains, fixation-driven evolutionary Markov chains, reversible stationary distributions, fitness landscapes, and valley crossing are established theory.

PAYOFF's topology-specific result is the exact transport

```text
edgewise conflict recovery
-> intrinsic topology payoff b_S
-> pairwise phi_ST=b_T-b_S
-> topology-distance eta_ST=gamma q_ST
-> fixation-driven mutation graph,
```

plus the resulting separation between intrinsic-payoff stationary weights and topology-dependent transition kinetics under the declared exponential Moran process.
