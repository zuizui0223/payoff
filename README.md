# PAYOFF — from ecological compromise to evolving architecture and population dynamics

PAYOFF is the mathematical bridge across three sister repositories:

- [SCH](https://github.com/zuizui0223/sch): reconstructs conflict when multiple functions share one phenotypic coordinate.
- [BALANCE](https://github.com/zuizui0223/balance): identifies when that real conflict is still cheaper than changing architecture.
- [BITA](https://github.com/zuizui0223/bita): measures how much extra dimensionality recovers and when recovery can outweigh architecture cost.

PAYOFF asks what happens next:

> **How does a measurable within-organism functional conflict generate an architecture payoff landscape, and how is that landscape transported into architecture construction, evolutionary games, fixation, mutation-selection occupancy, space, and time?**

Biological functions are payoff components, not literal strategic agents. The strategic/evolutionary objects are heritable architectures.

Start with [`theory/PAYOFF_TRANSPORT_PRINCIPLE.md`](theory/PAYOFF_TRANSPORT_PRINCIPLE.md). For the full reading order use [`docs/CANONICAL_READER_PATH.md`](docs/CANONICAL_READER_PATH.md).

---

## 1. Upstream architecture payoff landscape

For two functions forced to share one trait,

```text
loss_S(z)=a(z-theta1)^2+b(z-theta2)^2.
```

The unique compromise has conflict load

```text
L=[ab/(a+b)](theta1-theta2)^2.
```

For the registered differentiated residual-coupling model,

```text
R=sL,
```

with

```text
s=ab/[ab+c(a+b)].
```

The original binary shared-versus-differentiated gap is

```text
phi=R-K=sL-K.
```

The more general architecture-level object is

```text
b(a)=R(a)-K(a),
```

where `a` can be a coupling strength, a partial modular architecture, or a discrete coupling topology.

So the original binary PAYOFF model is one pairwise contrast on a broader architecture payoff landscape.

---

## 2. Continuous architecture: shared, partial, full, then branching

Along a monotone release path use recovered conflict loss itself as architecture coordinate:

```text
r=R(lambda) in [0,L].
```

With smooth architecture cost `C(r)`, intrinsic payoff is

```text
b(r)=r-C(r).
```

An interior intrinsic optimum satisfies

```text
C'(r*)=1.
```

With symmetric architecture-distance feedback

```text
H(r,q)=-gamma(r-q)^2,
```

the monomorphic selection gradient is still

```text
1-C'(r).
```

but the mutant curvature at `r*` is

```text
-C''(r*)-2gamma.
```

Therefore the general local branching boundary is

```text
gamma_branch=-C''(r*)/2.
```

For quadratic cost

```text
C(r)=c1*r+(kappa/2)r^2,
alpha=1-c1,
```

one gets

```text
r0=clip(alpha/kappa,0,L)
```

and

```text
gamma_branch=-kappa/2.
```

Thus:

```text
alpha<=0              shared intrinsic optimum
0<alpha<kappa L       partial-modularity intrinsic optimum
alpha>=kappa L        full-differentiation intrinsic optimum.
```

For the declared quadratic potential game, crossing `gamma=-kappa/2` converts an interior partial architecture from a monomorphic ESS into a protected mixture of the two recovery endpoints.

See:

- [`theory/CONTINUOUS_ARCHITECTURE_ESS.md`](theory/CONTINUOUS_ARCHITECTURE_ESS.md)
- [`theory/GENERAL_CONVEX_ARCHITECTURE_BRANCHING.md`](theory/GENERAL_CONVEX_ARCHITECTURE_BRANCHING.md)
- [`theory/CONTINUOUS_ARCHITECTURE_GLOBAL_PHASE_DIAGRAM.md`](theory/CONTINUOUS_ARCHITECTURE_GLOBAL_PHASE_DIAGRAM.md)

---

## 3. Continuous branching closes back into the original two-strategy game

For endpoint architectures

```text
S: r=0,
D: r=L,
```

the continuous model gives

```text
phi_end
=alpha L-(kappa/2)L^2,
```

and

```text
eta_end=gamma L^2.
```

When

```text
0<alpha<kappa L,
gamma<-kappa/2,
```

one automatically has

```text
|phi_end|<|eta_end|,
eta_end<0.
```

So the post-branching endpoint game lies exactly inside PAYOFF's stable negative-frequency coexistence wedge.

The differentiated-endpoint frequency is

```text
p_D*
=(1-phi_end/eta_end)/2
```

and is identical to the endpoint frequency from the continuous potential solution.

Thus the binary PAYOFF game reappears endogenously as the post-branching endpoint phase.

See [`theory/CONTINUOUS_ENDPOINT_COEXISTENCE.md`](theory/CONTINUOUS_ENDPOINT_COEXISTENCE.md).

---

## 4. Edgewise modularization: which functional connection should weaken?

Give every functional coupling edge `e=(i,j)` its own strength `c_e`.

After phenotype optimization,

```text
partial D*/partial c_e
=(x_i*-x_j*)^2.
```

So squared optimized disagreement across an edge is exactly its marginal coupling penalty.

Using decoupling amount `d_e`,

```text
partial R/partial d_e
=(x_i*-x_j*)^2.
```

Recovery is convex in edgewise decoupling. Therefore with additive linear decoupling cost,

```text
Phi(d)=R(d)-sum_e k_e d_e
```

is convex on the coupling box, and at least one global optimizer is a vertex:

```text
d_e in {0,c_e^0}.
```

So under the declared geometry, continuously variable couplings can generate a discrete retain/release modular topology.

This does not mean graded coupling is universally impossible; sufficiently convex architecture cost can stabilize interior edge strengths.

See [`theory/EDGEWISE_MODULARIZATION.md`](theory/EDGEWISE_MODULARIZATION.md).

---

## 5. Global architecture value can differ from local accessibility

For one edge with linear decoupling cost `k d`, define

```text
k_local=R'(0),
k_global=R(dmax)/dmax.
```

Convex recovery gives

```text
k_local<=k_global.
```

Hence

```text
k_local<k<k_global
```

is a finite-jump modularization barrier:

```text
small release mutations are selected against,
complete release has higher payoff.
```

For the original two-function quadratic model, with reference separation fraction `s0`,

```text
k_local=s0^2 Delta^2,
k_global=s0 Delta^2,
```

and the exact gap is

```text
W_k=s0(1-s0)Delta^2.
```

At fixed functional optimum separation `Delta`, the gap is largest at

```text
s0=1/2,
```

where

```text
W_k,max=Delta^2/4.
```

So intermediate residual integration produces the largest mismatch between global payoff advantage and local evolvability in this model.

See [`theory/DISCONTINUOUS_MODULARIZATION_BARRIER.md`](theory/DISCONTINUOUS_MODULARIZATION_BARRIER.md).

---

## 6. Discrete topology game

Represent a vertex architecture by a binary edge-release vector `S` with intrinsic optimized payoff

```text
b_S=R(S)-K(S).
```

For weighted topology distance

```text
q(S,T)=sum_e w_e(s_e-t_e)^2
```

and symmetric feedback

```text
H(S,T)=-gamma q(S,T),
```

every topology pair is exactly a canonical PAYOFF game with

```text
phi_ST=b_T-b_S,
eta_ST=gamma q(S,T).
```

Therefore:

```text
gamma<0 and |Delta b|<|gamma|q
-> stable pairwise topology coexistence;

gamma>0 and |Delta b|<gamma q
-> pairwise topology coordination.
```

All deterministic and finite-population PAYOFF receipts can be reused pair by pair.

See [`theory/TOPOLOGY_PAYOFF_GAME.md`](theory/TOPOLOGY_PAYOFF_GAME.md).

---

## 7. Any symmetric architecture pair has canonical PAYOFF coordinates

The topology-distance kernel is only one special case.

For any symmetric pair

```text
[[a,b],
 [b,d]],
```

define

```text
phi=(d-a)/2,
eta=(a+d-2b)/2.
```

After a common additive shift, the pair is exactly

```text
[[0,phi-eta],
 [phi-eta,2phi]].
```

Thus `(phi,eta)` are canonical local coordinates for any symmetric architecture pair.

For a decomposition

```text
A_ij=b_i+b_j+H_ij,
```

```text
phi_ij
=b_j-b_i+(H_jj-H_ii)/2,
```

```text
eta_ij
=(H_ii+H_jj-2H_ij)/2.
```

So intrinsic architecture gap and population-game `phi` coincide only when same-type feedback is equal across the pair.

See [`theory/SYMMETRIC_GAME_CANONICALIZATION.md`](theory/SYMMETRIC_GAME_CANONICALIZATION.md).

---

## 8. Well-mixed invasion and finite-population fixation

For any canonical architecture pair,

```text
Delta(p)=phi+eta(2p-1),
```

with strict phases

```text
phi<-|eta|             first architecture dominance
phi>|eta|              second architecture dominance
|phi|<|eta|, eta<0     stable coexistence
|phi|<|eta|, eta>0     coordination bistability.
```

Rare-invasion boundaries are

```text
phi=+eta,
phi=-eta.
```

Under the declared exponential Moran process,

```text
rho_T/rho_S
=exp[beta(N-2)phi].
```

Under weak selection,

```text
rho_T>1/N iff 3phi>eta.
```

So deterministic rare invasion, reciprocal fixation ordering, and absolute mutant advantage remain separate estimands.

---

## 9. Rare topology mutation: stationary abundance is not accessibility

With connected symmetric rare mutation among architecture states and exponential Moran fixation, any finite symmetric architecture game has self-play scores

```text
u_i=A_ii/2.
```

The exact monomorphic stationary law is

```text
Pi_i
propto
exp[beta(N-2)u_i].
```

For zero-diagonal architecture feedback,

```text
u_i=b_i,
```

so

```text
Pi_i
propto
exp[beta(N-2)b_i].
```

Off-diagonal ecological interaction changes invasion, coexistence, fixation probabilities, substitution rates, and metastability, but cancels from these symmetric weak-mutation monomorphic weights.

Single-edge topology accessibility is tracked separately by the intrinsic path valley

```text
B(S->G)
=max[0,b_S-best_path_bottleneck].
```

Thus a globally favored topology can have high long-run stationary weight and still be difficult to reach through local edge mutations.

See:

- [`theory/TOPOLOGY_RARE_MUTATION.md`](theory/TOPOLOGY_RARE_MUTATION.md)
- [`theory/SYMMETRIC_RARE_MUTATION_GIBBS.md`](theory/SYMMETRIC_RARE_MUTATION_GIBBS.md)
- [`theory/ARCHITECTURE_STATE_ATLAS.md`](theory/ARCHITECTURE_STATE_ATLAS.md)

---

## 10. Space: local architecture gaps become spectral invasion

Patch-specific rare-type margins are transported through

```text
A=diag(r)-mL_G.
```

Metapopulation invasion is

```text
Lambda=lambda_max(A).
```

For connected conservative migration, the principal exponent falls from the best local source toward the landscape mean as migration strengthens.

A local architecture source can therefore rescue a type in a landscape whose average static payoff disfavors it, but only below a critical migration rate.

See [`theory/ENVIRONMENT_MOSAIC_SOURCE_SINK.md`](theory/ENVIRONMENT_MOSAIC_SOURCE_SINK.md).

---

## 11. Time: common forcing is a null, source switching creates a premium

If every patch receives the same additive temporal forcing,

```text
A(t)=A0+q(t)I,
```

then

```text
Lambda_temporal
=lambda_max(A0)+mean(q).
```

Zero-mean common fluctuations have no extra long-run effect.

When relative patch quality changes through time, seasonal operators need not commute. For the registered symmetric two-patch two-season model,

```text
Lambda_F
=lambda_max(A_bar)+P_temp,
```

with

```text
P_temp>=0.
```

For anti-phase source switching,

```text
season A: (r_bar+x,r_bar-x)
season B: (r_bar-x,r_bar+x),
```

```text
Lambda_F
=r_bar-m
+(1/tau)asinh[
  m/sqrt(m^2+x^2)
  *sinh(tau sqrt(m^2+x^2))
].
```

The temporal premium has one unique finite migration maximum for every nonzero contrast.

In weak contrast,

```text
m_opt tau -> 1.6061152988...
```

and

```text
P_max
~=0.13248753945 x^2 tau.
```

The exact critical seasonal contrast and two migration boundaries are implemented when temporal switching is strong enough to overcome a coordination barrier.

---

## 12. Main organizing principle

PAYOFF is now best read as one transport hierarchy:

```text
functional conflict
        L
        |
        v
architecture landscape
        a -> R(a)-K(a)=b(a)
        |
        +--> continuous ESS / branching
        +--> edgewise modularization / topology
        |
        v
symmetric architecture pair
        (phi,eta)
        |
        +--> deterministic invasion
        +--> finite fixation
        +--> rare-mutation occupancy
        +--> spatial spectral growth
        +--> temporal Floquet growth.
```

The same biological system can have different answers to:

```text
which architecture has highest intrinsic payoff?
which architecture is locally reachable?
which architecture can invade when rare?
which mutant fixes more often?
which topology dominates weak-mutation occupancy?
which architecture persists in space or periodic environments?
```

Those distinctions are the point of the framework, not nuisances to be collapsed.

---

## 13. Reading and claim boundaries

Start with:

- [`theory/PAYOFF_TRANSPORT_PRINCIPLE.md`](theory/PAYOFF_TRANSPORT_PRINCIPLE.md)
- [`theory/ARCHITECTURE_STATE_ATLAS.md`](theory/ARCHITECTURE_STATE_ATLAS.md)
- [`theory/BOUNDARY_ATLAS.md`](theory/BOUNDARY_ATLAS.md)
- [`docs/CANONICAL_READER_PATH.md`](docs/CANONICAL_READER_PATH.md)

Empirical handoffs:

- [`docs/SCH_BALANCE_BITA_BRIDGE.md`](docs/SCH_BALANCE_BITA_BRIDGE.md)
- [`docs/CONTINUOUS_ARCHITECTURE_HANDOFF.md`](docs/CONTINUOUS_ARCHITECTURE_HANDOFF.md)
- [`docs/TEMPORAL_HANDOFF.md`](docs/TEMPORAL_HANDOFF.md)

Claim ceilings:

- [`docs/CLAIM_BOUNDARY.md`](docs/CLAIM_BOUNDARY.md)
- [`docs/PRIOR_ART_BOUNDARY.md`](docs/PRIOR_ART_BOUNDARY.md)
- [`docs/CONTINUOUS_ARCHITECTURE_PRIOR_ART_BOUNDARY.md`](docs/CONTINUOUS_ARCHITECTURE_PRIOR_ART_BOUNDARY.md)
- [`docs/TOPOLOGY_CLAIM_BOUNDARY.md`](docs/TOPOLOGY_CLAIM_BOUNDARY.md)
- [`docs/SPATIAL_PRIOR_ART_BOUNDARY.md`](docs/SPATIAL_PRIOR_ART_BOUNDARY.md)
- [`docs/TEMPORAL_PRIOR_ART_BOUNDARY.md`](docs/TEMPORAL_PRIOR_ART_BOUNDARY.md)

PAYOFF does not claim to invent specialization, adaptive dynamics, branching, modularity, evolutionary games, Moran processes, source-sink theory, graph selection, or Floquet theory. The candidate contribution is the **explicit architecture payoff transport from measured functional compromise into those established population-theoretic objects, with exact receipts under declared models.**
