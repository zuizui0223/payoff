# Multi-architecture potential game

The two-strategy PAYOFF model compares a shared architecture `S` and a differentiated architecture `D`. The network extension naturally produces many candidate architectures: different coupling graphs, different coupling strengths, or different modular partitions.

This note shows how to place all of them in one evolutionary game while retaining a Lyapunov function under symmetric ecological feedback.

## 1. Intrinsic optimized architecture payoffs

Suppose there are `m` heritable architecture strategies. For each architecture `i`, phenotype optimization and architecture cost produce an intrinsic optimized payoff

```text
b_i.
```

These values can come from SCH/BALANCE/BITA-style optimization, including the network model in `NETWORK_EXTENSION.md`.

If there is no frequency dependence, only differences among the `b_i` matter.

## 2. Pairwise ecological feedback

Let

```text
H = H^T
```

be a symmetric matrix of pairwise ecological feedback among architecture states. Define the game payoff matrix

```text
A_ij = b_i + b_j + H_ij.
```

Because `H` is symmetric, `A` is symmetric.

For population frequency vector `p` on the simplex,

```text
pi_i = (A p)_i
     = b_i + b_bar + (H p)_i,
```

where

```text
b_bar = sum_j p_j b_j.
```

The common term `b_bar` cancels from relative payoffs. Therefore selection compares

```text
b_i + (H p)_i.
```

This cleanly separates:

```text
intrinsic architecture advantage
+
frequency-dependent ecological feedback.
```

---

## Theorem M1 — replicator equation for multiple trait architectures

Under the standard replicator dynamic,

```text
dp_i/dt = p_i [pi_i - pi_bar],
```

with

```text
pi_bar = p^T A p.
```

The simplex is forward invariant: frequencies remain nonnegative and continue to sum to one.

### Proof

If `p_i=0`, then `dp_i/dt=0`, so no coordinate crosses below zero. Also

```text
sum_i dp_i/dt
= sum_i p_i pi_i - pi_bar sum_i p_i
= pi_bar-pi_bar
=0.
```

Thus a trajectory beginning on the simplex remains on it.

QED.

---

## Theorem M2 — mean game payoff is a Lyapunov function

If `A=A^T`, then along replicator trajectories

```text
d/dt (p^T A p)
= 2 sum_i p_i (pi_i-pi_bar)^2
>= 0.
```

Equality holds exactly when every strategy present in the population has the same payoff.

### Proof

Because `A` is symmetric,

```text
d/dt (p^T A p)
= 2 (dp/dt)^T A p
= 2 sum_i [p_i(pi_i-pi_bar)] pi_i.
```

Hence

```text
=2[sum_i p_i pi_i^2 - pi_bar sum_i p_i pi_i]
=2[sum_i p_i pi_i^2 - pi_bar^2]
=2 sum_i p_i(pi_i-pi_bar)^2.
```

The final expression is a weighted variance and is nonnegative. It vanishes iff all strategies with `p_i>0` have `pi_i=pi_bar`.

QED.

### Interpretation

For symmetric ecological feedback, architecture evolution is a potential-like ascent process rather than an arbitrary cyclic game. This is useful because candidate modular architectures can be compared in one common dynamical system without introducing unconstrained game behavior.

---

## Corollary M2.1 — no-feedback limit

If

```text
H=0,
```

then

```text
pi_i-pi_k = b_i-b_k.
```

Therefore any architecture with a unique maximal intrinsic payoff excludes all lower-payoff architectures under deterministic replicator dynamics from any initial state in which it is present.

This is the multi-strategy version of the static `phi=sL-K` comparison.

---

## 3. Two-strategy PAYOFF model as an exact special case

Set

```text
b_S=0,
b_D=phi.
```

Let unlike architecture encounters carry feedback `-eta` and like encounters carry zero extra feedback:

```text
H = [[0,    -eta],
     [-eta, 0   ]].
```

Then

```text
A_ij=b_i+b_j+H_ij
```

becomes

```text
          S          D
S         0       phi-eta
D      phi-eta      2phi.
```

At differentiated frequency `p`,

```text
pi_S = p(phi-eta),
pi_D = (1-p)(phi-eta)+2phi p,
```

so

```text
pi_D-pi_S
= phi+eta(2p-1)
= Delta(p).
```

Thus the minimal PAYOFF game is not an ad hoc frequency term: it is the two-strategy member of the symmetric potential-game family.

### Ecological meaning of `eta`

In this representation:

```text
eta > 0
```

means unlike-architecture encounters are penalized relative to like encounters. This creates positive frequency dependence and coordination/bistability.

```text
eta < 0
```

means unlike-architecture encounters are favored. This creates negative frequency dependence and stable coexistence when the intrinsic payoff difference is not too large.

The same replicator classification in `THEOREMS.md` follows.

---

## 4. Architecture graphs as strategies

A particularly useful construction is:

```text
strategy i = coupling graph G_i + coupling strength lambda_i + architecture cost K_i.
```

For each strategy:

```text
1. optimize trait vector x under G_i,
2. compute pre-cost loss D_i*,
3. compute intrinsic payoff b_i=B-D_i*-K_i,
4. place b_i into the architecture game,
5. estimate H_ij from ecological interactions among architecture states.
```

This separates two questions:

```text
What architecture is intrinsically good at resolving functional conflict?
```

from

```text
What architecture is stable once its ecological consequences depend on how common it is?
```

---

## 5. Continuous recovery path is now solved for the registered quadratic game

For a fixed connected coupling topology whose release function

```text
R(lambda)
```

is continuous and strictly monotone, recovery itself can be used as the architecture coordinate

```text
r=R(lambda) in [0,L].
```

`CONTINUOUS_ARCHITECTURE_ESS.md` studies

```text
b(r)=alpha*r-(kappa/2)r^2
```

with symmetric architecture-distance feedback

```text
H(r,q)=-gamma(r-q)^2.
```

The exact threshold is

```text
gamma=-kappa/2.
```

For an intrinsic interior architecture:

```text
gamma>-kappa/2
-> one monomorphic partial architecture;

gamma=-kappa/2
-> neutral variance manifold at the same mean recovery;

gamma<-kappa/2
-> branching-compatible singular strategy
   and protected endpoint polymorphism.
```

The endpoint phase reduces exactly to the original two-strategy PAYOFF game with

```text
phi_endpoint=b(L)-b(0),
eta_endpoint=gamma L^2.
```

The more general local result in `GENERAL_CONVEX_ARCHITECTURE_BRANCHING.md` replaces constant `kappa` by cost curvature at the singular architecture:

```text
gamma_branch=-C''(r*)/2,
C'(r*)=1.
```

So the scalar continuous-coupling path is no longer an open target.

---

## 6. Remaining nontrivial target — topology cannot always be collapsed to recovery alone

The next unsolved layer is not merely continuous `lambda`. It is competition among architectures with different coupling **topologies**.

Two graphs can have the same recovered conflict value

```text
R_i=R_j
```

while differing in:

```text
which functions are coupled,
architecture cost,
developmental constraints,
ecological interaction kernel H_ij,
and responses to environment.
```

A one-dimensional recovery coordinate cannot preserve those distinctions.

The remaining graph-level question is therefore:

> **Which coupling topology or modular partition is evolutionarily stable when candidate graphs differ not only in recovered conflict loss but also in architecture-specific costs and ecological interactions?**

The finite symmetric potential-game framework in this file already supplies the population dynamics once those graph-specific payoffs are constructed. The missing piece is a biologically defensible graph-mutation / graph-distance model, not the replicator algebra itself.
