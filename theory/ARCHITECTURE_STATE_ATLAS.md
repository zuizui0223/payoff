# Architecture-state atlas — intrinsic optimum, branching, accessibility, topology invasion, and long-run abundance

PAYOFF now contains two kinds of transition logic:

```text
1. population processes acting on a fixed set of architectures;
2. evolution of the architecture state space itself.
```

`BOUNDARY_ATLAS.md` tracks the first kind. This document tracks the second.

The common upstream object remains recovered shared-conflict loss.

---

## A1. Continuous intrinsic architecture optimum

Architecture coordinate:

```text
r in [0,L]
```

with intrinsic payoff

```text
b(r)=r-C(r).
```

For a smooth cost curve, an interior intrinsic optimum satisfies

```text
C'(r*)=1.
```

For quadratic cost

```text
C(r)=c1*r+(kappa/2)r^2,
alpha=1-c1,
```

this becomes

```text
r*=alpha/kappa.
```

The constrained no-feedback phase boundaries are

```text
alpha=0
```

and

```text
alpha=kappa L.
```

They separate

```text
shared / partial / fully differentiated
```

intrinsic architecture optima.

---

## A2. Continuous architecture branching boundary

With symmetric architecture-distance feedback

```text
H(r,q)=-gamma(r-q)^2,
```

the monomorphic selection gradient remains

```text
1-C'(r).
```

But the mutant curvature at an interior singular architecture is

```text
-C''(r*)-2gamma.
```

Therefore the local branching boundary is

```text
gamma_branch
=-C''(r*)/2.
```

For quadratic cost this is

```text
gamma=-kappa/2.
```

This boundary asks:

> Does a convergence-stable partial architecture remain an ESS, or does nearby architecture diversity become invasible?

It is not the same question as which `r` maximizes intrinsic payoff.

---

## A3. Quadratic global architecture-distribution phases

For quadratic intrinsic payoff and the squared-distance interaction kernel, the global population potential is

```text
V
=2alpha mu-kappa mu^2-(kappa+2gamma)sigma^2.
```

For

```text
gamma>-kappa/2,
```

variance is penalized and the global optimum is monomorphic.

For

```text
gamma=-kappa/2,
```

variance is neutral at the optimal mean.

For

```text
gamma<-kappa/2,
```

the optimum lies on endpoint mixtures. The endpoint-polymorphism boundaries on the `alpha` axis are

```text
alpha_S
=[(kappa+2gamma)L]/2,

alpha_D
=[(kappa-2gamma)L]/2.
```

The protected endpoint-polymorphism wedge is

```text
alpha_S<alpha<alpha_D.
```

Its width is

```text
2|gamma|L
```

and midpoint is

```text
kappa L/2.
```

---

## A4. Edgewise marginal release boundary

For edge coupling `e=(i,j)`, the optimized marginal loss per unit coupling is exactly

```text
partial D*/partial c_e
=(x_i*-x_j*)^2.
```

Using decoupling amount `d_e`, the marginal recovery is therefore

```text
partial R/partial d_e
=(x_i*-x_j*)^2.
```

Against architecture cost `K(d)`, an interior edge balance satisfies

```text
(x_i*-x_j*)^2
=partial K/partial d_e.
```

This boundary asks:

> Is a small additional weakening of this specific coupling edge locally favored?

It is an architecture-construction condition, not a population invasion boundary.

---

## A5. Local-versus-global decoupling barrier

For one edge with linear cost `k d`, define

```text
k_local=R'(0),
k_global=R(dmax)/dmax.
```

Convex recovery gives

```text
k_local<=k_global.
```

Hence:

```text
k<k_local
-> small release locally favored;

k_local<k<k_global
-> finite-jump barrier;

k>k_global
-> retained coupling locally and globally favored.
```

For the two-function quadratic model:

```text
k_local=s0^2 Delta^2,
k_global=s0 Delta^2,
```

with barrier width

```text
s0(1-s0)Delta^2.
```

This is the architecture analogue of PAYOFF's recurring distinction between static advantage and accessibility from rarity.

---

## A6. Linear edge-cost topology discretization

For multiple edge-decoupling coordinates `d`, optimized recovery is convex.

With additive linear costs,

```text
Phi(d)=R(d)-sum_e k_e d_e
```

is convex on the coupling box.

Therefore at least one global optimizer is a box vertex:

```text
d_e in {0,c_e^0}.
```

This is a topology-selection result:

```text
each edge retained or maximally released
```

for at least one globally optimal representative.

It does not say that partial edge strengths are impossible under convex architecture costs.

---

## A7. Pairwise topology invasion boundary

For two discrete topologies `S,T`, intrinsic optimized payoffs are

```text
b_S,b_T
```

and weighted topology distance is

```text
q_ST.
```

With topology-distance feedback `gamma`, the pair maps exactly to the canonical PAYOFF game:

```text
phi_ST=b_T-b_S,
eta_ST=gamma q_ST.
```

The reciprocal topology invasion boundaries are

```text
b_T-b_S=+gamma q_ST
```

and

```text
b_T-b_S=-gamma q_ST.
```

Thus:

```text
gamma<0 and |Delta b|<|gamma|q
-> stable topology coexistence;

gamma>0 and |Delta b|<gamma q
-> topology coordination / bistability.
```

---

## A8. Finite topology fixation boundary

Under the declared exponential Moran process,

```text
rho(T|S)/rho(S|T)
=
exp[beta(N-2)(b_T-b_S)].
```

So reciprocal fixation ordering is centered on

```text
b_T=b_S,
```

not on the deterministic topology-invasion boundaries.

Under weak selection, a single `T` mutant exceeds neutral fixation when

```text
3(b_T-b_S)>gamma q_ST.
```

---

## A9. Rare-mutation stationary topology abundance

With connected symmetric rare topology mutation,

```text
Pi_S
propto
exp[beta(N-2)b_S].
```

Thus long-run monomorphic abundance is an intrinsic-payoff Gibbs law in the declared process.

Topology feedback `gamma q` still changes substitution kinetics.

This produces another distinction:

```text
stationary abundance
!=
evolutionary accessibility / mixing time.
```

---

## A10. Single-edge topology valley

For a topology source `S` and target `G`, let

```text
m*(S,G)
=max over single-edge paths
  min payoff along path.
```

Define intrinsic valley depth

```text
B(S->G)
=max[0,b_S-m*(S,G)].
```

Then:

```text
B=0
```

means there exists a single-edge path to `G` that never drops below the source payoff.

```text
B>0
```

means every such path crosses an intrinsic fitness valley.

This is a path-accessibility diagnostic, not itself a fixation probability or first-passage time.

---

# Architecture hierarchy

The full architecture-state hierarchy is therefore:

```text
where is the intrinsic partial optimum?
        C'(r*)=1
            |
            v
is that optimum evolutionarily stable?
        gamma ? -C''(r*)/2
            |
            v
which edge changes are locally favored?
        (x_i-x_j)^2 ? marginal cost
            |
            v
is global modularization locally accessible?
        k_local ? k ? k_global
            |
            v
which discrete topology has highest intrinsic payoff?
        b_S
            |
            v
can topology T invade topology S?
        Delta b ? gamma q
            |
            v
which topology fixes more often?
        sign(Delta b)
            |
            v
which topology dominates long-run rare-mutation occupancy?
        exp[beta(N-2)b_S]
            |
            v
how hard is it to reach?
        mutation graph + valley + fixation kinetics.
```

The same biological architecture system can give different answers at every line.
