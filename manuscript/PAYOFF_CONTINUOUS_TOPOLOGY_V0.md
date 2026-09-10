# From partial modularity to branching and discrete architecture

## Abstract

Architecture need not jump directly from a fully shared to a fully differentiated state. We represent recoverable conflict loss as a continuous architecture coordinate and ask when partial modularity is optimal, when an interior architecture loses evolutionary stability, and when continuous coupling strengths generate discrete retained-versus-released topologies. The framework links an intrinsic condition for partial modularity, frequency-dependent branching, edgewise marginal release value, and convex recovery under additive release costs. Under the declared geometry, these results explain how continuous variation in coupling can produce both stable intermediate architectures and abrupt modular topology.

## 1. Continuous architecture coordinate

Let `r` denote recovered conflict loss along a monotone release path,

```text
r in [0,L].
```

With architecture cost `C(r)`, intrinsic payoff is

```text
b(r)=r-C(r).
```

An interior optimum satisfies

```text
C'(r*)=1.
```

Thus shared, partial, and fully differentiated architectures arise as different regions of one continuous optimization problem.

## 2. Branching of an interior architecture

Add symmetric architecture-distance feedback

```text
H(r,q)=-gamma(r-q)^2.
```

The monomorphic selection gradient retains the intrinsic optimum condition, while local mutant curvature becomes

```text
-C''(r*)-2gamma.
```

The local branching boundary is therefore

```text
gamma_branch=-C''(r*)/2.
```

For quadratic cost, this reduces to the registered `-kappa/2` threshold.

## 3. Endpoint phase after branching

When branching destabilizes an interior architecture, the endpoint shared and differentiated states recover the canonical two-strategy architecture game. This gives a direct bridge from continuous architecture evolution to stable endpoint coexistence or coordination without assuming the binary game at the start.

## 4. Edgewise modularization

For a network of functional couplings with edge strength `c_e`, phenotype optimization gives the marginal coupling penalty

```text
partial D*/partial c_e=(x_i*-x_j*)^2.
```

Equivalently, for decoupling amount `d_e`,

```text
partial R/partial d_e=(x_i*-x_j*)^2.
```

Optimized disagreement therefore ranks edges by marginal release value.

## 5. From continuous coupling to discrete topology

When recovery is convex in edgewise release and decoupling cost is additive and linear, the architecture objective is convex on the coupling box. At least one global optimizer is then a vertex, so each edge is fully retained or fully released.

This is a model-based route by which continuous coupling strengths can generate discrete modular architecture. It does not imply that graded coupling is impossible under other cost geometries.

## 6. Discussion

The paper unifies three phenomena usually treated separately: partial modularity, evolutionary branching, and modular topology. Their common basis is the shape of recovered conflict value relative to the cost and interaction geometry of architecture release.

## Scope after SLK integration

SLK uses only the minimal architecture-payoff transport needed to distinguish global value, accessibility, invasion, fixation, and occupancy. The continuous and network-topological architecture theory developed here remains canonical in PAYOFF and is not required for the flagship SLK proof spine.
