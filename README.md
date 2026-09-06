# PAYOFF — transporting ecological compromise into evolutionary population dynamics

PAYOFF is the population-theory bridge across three sister repositories:

- [SCH](https://github.com/zuizui0223/sch): reconstructs conflict when multiple functions must share one phenotypic coordinate.
- [BALANCE](https://github.com/zuizui0223/balance): identifies the domain where real conflict exists but shared architecture still pays better.
- [BITA](https://github.com/zuizui0223/bita): measures how much extra phenotypic dimensionality recovers and when that recovery exceeds architecture cost.

PAYOFF starts **after** those ecological quantities are defined and asks:

> What evolutionary population dynamics follow when the same shared-versus-differentiated architecture payoffs are exposed to frequency dependence, finite population size, mutation, space, and time?

Biological functions are payoff components, not literal strategic agents. The literal evolutionary game is played by alternative heritable architectures.

For the shortest conceptual map, read [`theory/PAYOFF_TRANSPORT_PRINCIPLE.md`](theory/PAYOFF_TRANSPORT_PRINCIPLE.md).

---

## 1. Invariant upstream bridge

Two functions prefer `theta1` and `theta2` but share trait `z`:

```text
loss_S(z)
= a(z-theta1)^2+b(z-theta2)^2.
```

The unique shared compromise is

```text
z_S*=(a theta1+b theta2)/(a+b)
```

with conflict load

```text
L
= [ab/(a+b)](theta1-theta2)^2.
```

For differentiated coordinates `x,y` with residual coupling `c>=0`,

```text
loss_D(x,y)
= a(x-theta1)^2
+ b(y-theta2)^2
+ c(x-y)^2.
```

Optimization gives

```text
s
= |x*-y*|/|theta1-theta2|
= ab/[ab+c(a+b)]
```

and the exact quadratic identity

```text
R=sL.
```

With added architecture cost `K`,

```text
phi
= W_D*-W_S*
= R-K
= sL-K.
```

This is the central quantity transported through the rest of the repository.

```text
L=0                 no shared-coordinate conflict
L>0, phi<0          BALANCE: conflict but shared architecture wins
phi=0               static architecture crossing
phi>0               BITA: differentiated architecture wins.
```

---

## 2. Well-mixed evolutionary game

Let `p` be differentiated-architecture frequency and add minimal linear frequency feedback:

```text
Delta(p)
= payoff_D-payoff_S
= phi+eta(2p-1).
```

Replicator dynamics are

```text
dp/dt
= p(1-p)Delta(p).
```

Strict phases:

```text
phi<-|eta|               shared dominance
phi>|eta|                differentiated dominance
|phi|<|eta|, eta<0       stable reciprocal coexistence
|phi|<|eta|, eta>0       coordination bistability.
```

Reciprocal rare-invasion boundaries are

```text
phi=+eta
phi=-eta
```

or on the architecture-cost scale

```text
K=R-eta
K=R+eta.
```

Thus static architecture advantage and invasion from rarity are different estimands.

---

## 3. Finite populations and recurrent mutation

Under the declared self-excluding exponential-fitness Moran process,

```text
Delta_N(i)
= [phi(N-2)+eta(2i-N)]/(N-1).
```

Exact reciprocal single-mutant fixation ordering is

```text
rho_D/rho_S
= exp[beta phi(N-2)].
```

Hence

```text
rho_D>rho_S
iff
phi>0.
```

Under weak selection,

```text
rho_D>1/N iff 3phi>eta
rho_S>1/N iff -3phi>eta,
```

mapping the established one-third-law machinery onto `phi=sL-K`.

With recurrent mutation, the exact stationary birth-death distribution is computed by detailed balance. In the rare-mutation limit,

```text
log(Pi_N/Pi_0)
-> log(u_SD/u_DS)
   + beta(N-2)phi.
```

So mutation bias and architecture selection add on the long-run monomorphic log-odds scale.

Neutral recurrent mutation is an exact beta-binomial negative control. For symmetric mutation `mu`, the neutral stationary shape changes at

```text
mu_c=1/(N+2).
```

---

## 4. Space: from local architecture gaps to spectral invasion

Patch `j` has its own

```text
phi_j=s_jL_j-K_j.
```

Rare-D and rare-S local margins are

```text
r_j^D=phi_j-eta_j
r_j^S=-phi_j-eta_j.
```

On an undirected patch graph with Laplacian `L_G` and migration `m`, the exact linear invasion operators are

```text
A_D=diag(r^D)-mL_G
A_S=diag(r^S)-mL_G.
```

Metapopulation invasion is determined by the principal eigenvalues

```text
Lambda_D=lambda_max(A_D)
Lambda_S=lambda_max(A_S).
```

For heterogeneous connected landscapes, increasing conservative migration reduces the principal growth rate from the best local source toward the landscape mean.

If

```text
max_j r_j>0>mean_j r_j,
```

there is one critical migration rate separating low-migration source rescue from high-migration dilution.

For two patches,

```text
Lambda(m)
=
[r1+r2-2m
 +sqrt((r1-r2)^2+4m^2)]/2.
```

If one patch is a source, the other a sink, and the mean is negative,

```text
m_c
= r1 r2/(r1+r2).
```

A local BITA source can therefore maintain D even in a landscape whose average static architecture gap lies on the BALANCE side.

---

## 5. Time: commuting null and noncommuting temporal premium

If every patch receives the same additive temporal forcing,

```text
A(t)=A0+q(t)I,
```

then exactly

```text
Lambda_temporal
= lambda_max(A0)+mean(q).
```

Zero-mean common fluctuations have no extra temporal effect. This is the registered temporal null.

When relative patch quality changes through time, seasonal operators can fail to commute. In the two-patch model,

```text
[A_a,A_b]
propto
m[(r_1a-r_2a)-(r_1b-r_2b)].
```

So temporal structure beyond the mean requires both migration and seasonal change in relative patch quality.

For exactly two seasons, PAYOFF has an exact scalar Floquet formula and, under the declared symmetric two-patch assumptions,

```text
Lambda_F
>= lambda_max(A_bar).
```

The difference is the non-negative temporal premium.

Under rapid switching,

```text
Lambda_F-lambda_max(A_bar)
=
T^2 w^2(1-w)^2
m^2(Delta patch contrast)^2
/[24 delta_bar]
+O(T^4).
```

---

## 6. Anti-phase source switching: exact migration optimum

The cleanest temporal specialization swaps which patch is favorable every equal-length season:

```text
season A: (r_bar+x, r_bar-x)
season B: (r_bar-x, r_bar+x).
```

With season duration `tau`, the exact Floquet exponent is

```text
Lambda_F
=
r_bar-m
+(1/tau)
asinh[
  m/sqrt(m^2+x^2)
  *sinh(tau sqrt(m^2+x^2))
].
```

The time-average prediction is simply

```text
Lambda_avg=r_bar.
```

Define the temporal premium

```text
P=Lambda_F-r_bar.
```

For every nonzero seasonal contrast:

```text
P(0)=0,
P(m)>0 for finite m>0,
P(m)->0 as m->infinity.
```

PAYOFF now proves more strongly that **the exact premium has one unique migration maximum for every nonzero contrast**.

Using

```text
u=m tau
v=|x|tau,
```

the exact optimum is one function

```text
u_star(v).
```

Its limits are

```text
v->0:
nu_star -> 1.60611529880277...

v->infinity:
nu_star = 1+1/v+O(v^-2).
```

Thus the optimal migration timescale stays comparable to the seasonal-switching timescale.

---

## 7. Temporal inversion of positive-frequency coordination

Suppose the anti-phase variable is the static architecture gap itself:

```text
season A phi: (phi_bar+x, phi_bar-x)
season B phi: (phi_bar-x, phi_bar+x)
```

with common `eta>0`.

Both reciprocal architecture invasion edges receive the same exact premium `P`:

```text
Lambda_D
= phi_bar-eta+P

Lambda_S
= -phi_bar-eta+P.
```

Therefore define the edge-level effective coordination coefficient

```text
eta_eff=eta-P.
```

At `phi_bar=0`:

```text
P<eta    coordination
P=eta    reciprocal boundaries collapse
P>eta    reciprocal invasion.
```

Because `P(m)` is exactly unimodal, if

```text
P_max>eta+|phi_bar|,
```

there are exactly two migration boundaries

```text
m_-<m_+
```

and one uniquely bounded intermediate-migration interval in which both architectures invade.

---

## 8. Universal weak-contrast constants and exact critical contrast

For weak seasonal contrast

```text
v=|x|tau <<1,
```

```text
tau P
= v^2 H(u)+O(v^4),
```

where

```text
H(u)
= [u-tanh u]/(2u^2).
```

`H` has one unique maximum at

```text
u*=1.60611529880277...
```

with

```text
H*=0.132487539446827....
```

Hence

```text
m_opt tau
~=1.6061153
```

and

```text
P_max
~=0.13248754 x^2 tau.
```

At `phi_bar=0`, weak-contrast temporal inversion requires approximately

```text
x^2 tau/eta
>7.547879628343014....
```

Beyond the weak approximation, PAYOFF proves the exact maximum premium

```text
M(v)=max_u F(u,v)
```

is strictly increasing in `v`. Therefore every positive barrier

```text
B=(eta+|phi_bar|)tau
```

has one unique critical seasonal contrast

```text
M(v_c)=B.
```

So the exact temporal question has a three-step answer:

```text
v<v_c
    no migration treatment can create reciprocal invasion

v=v_c
    one tangent migration point

v>v_c
    exactly two migration boundaries
    enclosing one reciprocal-invasion island.
```

---

## 9. Payoff transport is the organizing principle

The repository is not intended as a list of unrelated population models.

The same upstream quantity is carried through each layer:

```text
functional conflict
    L
    |
    v
dimensional recovery
    R=sL
    |
    v
costed architecture gap
    phi=R-K
    |
    +--> frequency-dependent invasion
    +--> finite fixation
    +--> mutation-selection occupancy
    +--> spatial spectral growth
    +--> temporal Floquet growth.
```

The population process changes the downstream estimand; it does not retroactively redefine the ecological compromise receipt.

---

## 10. Where to read next

Use these entry points:

```text
theory/PAYOFF_TRANSPORT_PRINCIPLE.md
    compact cross-scale logic

docs/CANONICAL_READER_PATH.md
    full reading order

theory/BOUNDARY_ATLAS.md
    keeps static/invasion/fixation/occupancy/spatial/temporal boundaries separate

docs/SCH_BALANCE_BITA_BRIDGE.md
    ownership of L,s,R,K across sister repositories

docs/TEMPORAL_HANDOFF.md
    prospective temporal experiment design

docs/CLAIM_BOUNDARY.md
    scientific claim ceiling

docs/PRIOR_ART_BOUNDARY.md
    broad prior-art boundary

docs/SPATIAL_PRIOR_ART_BOUNDARY.md
    spatial claim boundary

docs/TEMPORAL_PRIOR_ART_BOUNDARY.md
    Floquet/dispersal temporal claim boundary.
```

Key temporal theorem files:

```text
theory/TWO_SEASON_TEMPORAL_PREMIUM.md
theory/ANTI_PHASE_SEASONAL_RESCUE.md
theory/EXACT_ANTI_PHASE_OPTIMUM.md
theory/WEAK_CONTRAST_UNIVERSAL_MIGRATION_OPTIMUM.md
theory/TEMPORAL_COORDINATION_INVERSION.md
theory/TEMPORAL_PHASE_DIAGRAM.md
theory/CRITICAL_SEASONAL_CONTRAST.md.
```

---

## 11. Claim boundary

PAYOFF does **not** claim to invent:

```text
specialization,
modularity,
frequency-dependent selection,
Moran processes,
one-third law,
mutation-selection balance,
evolutionary graph theory,
source-sink spectral theory,
Floquet theory,
Golden-Thompson,
or dispersal-induced growth.
```

The candidate contribution is narrower:

> **an explicit, testable transport from measurable shared-trait ecological compromise `L`, through recovered dimensional value `R=sL` and architecture gap `phi=sL-K`, into reciprocal invasion, fixation, long-run occupancy, spatial source-sink, and temporal architecture predictions.**

Every exact formula remains conditional on its declared model assumptions.

---

## 12. Main question

> **When does evolution tolerate a shared-trait compromise, when does extra phenotypic dimensionality pay for itself, and how do frequency dependence, drift, mutation, space, and time change whether shared versus differentiated architectures can invade, persist, fix, coexist, or switch dominance?**
