# PAYOFF transport principle

PAYOFF can be compressed into one idea:

> An ecology-derived architecture payoff gap is estimated upstream, then transported through increasingly rich population processes without redefining the underlying compromise quantity at every level.

The invariant upstream chain is

```text
shared-coordinate conflict
        |
        v
L
        |
        v
R=sL
        |
        v
phi=R-K=sL-K.
```

`phi` is the optimized differentiated-minus-shared architecture gap before population-frequency, drift, mutation, spatial, or temporal effects are added.

This document records how that one scalar becomes different population-level estimands.

It is not a claim that all ecological evolutionary models reduce universally to one scalar. The transport formulas below apply only under their declared model assumptions.

---

## Transport 0 — static architecture comparison

Input:

```text
phi=sL-K.
```

Output:

```text
phi>0  differentiated architecture statically higher
phi<0  shared architecture statically higher.
```

Invariant crossing:

```text
phi=0 <=> K=sL.
```

This is the SCH -> BALANCE -> BITA bridge before the evolutionary-game layer.

---

## Transport 1 — frequency-dependent reciprocal invasion

The well-mixed PAYOFF game is

```text
Delta(p)=phi+eta(2p-1).
```

The edge invasion receipts are

```text
I_D=phi-eta,
I_S=-phi-eta.
```

Thus frequency dependence does not replace `phi`; it adds one population term `eta` around it.

The reciprocal neutral surfaces are

```text
phi=+eta,
phi=-eta.
```

---

## Transport 2 — finite-population fixation

For the declared exponential Moran process,

```text
rho_D/rho_S
= exp[beta(N-2)phi].
```

Thus the reciprocal fixation ordering transports the static gap through the positive map

```text
phi
-> beta(N-2)phi
-> log(rho_D/rho_S).
```

Frequency feedback `eta` changes absolute fixation probabilities but cancels from this particular reciprocal ratio.

Under weak selection, the edge question changes again:

```text
rho_D>1/N iff 3phi>eta.
```

Therefore invasion and fixation are different receipts of the same upstream gap.

---

## Transport 3 — recurrent-mutation stationary occupancy

In the rare-mutation limit,

```text
log(Pi_N/Pi_0)
= log(u_SD/u_DS)
  + beta(N-2)phi.
```

Hence mutation bias enters additively beside the transported architecture gap.

The stationary layer therefore has the schematic form

```text
long-run occupancy log odds
= mutation bias
+ selection transport of phi.
```

---

## Transport 4 — regular-graph local competition

Under the declared Ohtsuki-Nowak weak-selection pair approximation on a degree-`k` regular graph, the special PAYOFF matrix gives

```text
phi_k
= [k/(k-2)]phi,
eta_k=eta.
```

Thus this graph model transports the static gap by a positive amplification

```text
phi -> A_k phi,
A_k=k/(k-2)>1,
```

while preserving its sign and preserving `eta`.

The static crossing remains

```text
phi=0.
```

---

## Transport 5 — heterogeneous spatial landscape

Patch-specific upstream receipts are

```text
phi_j=s_jL_j-K_j.
```

Rare-D margins are

```text
r_j^D=phi_j-eta_j,
```

and rare-S margins are

```text
r_j^S=-phi_j-eta_j.
```

Migration transports the vector of local margins through the symmetric operator

```text
A_D=diag(r^D)-mL_G,
A_S=diag(r^S)-mL_G.
```

The population receipt is no longer one local scalar but the spectral map

```text
r-vector
-> lambda_max[diag(r)-mL_G].
```

For connected conservative migration,

```text
max_j r_j
= Lambda(0)
>= Lambda(m)
-> mean_j r_j
```

as migration becomes strong.

Thus space replaces a simple scalar comparison by a monotone spectral aggregation of local PAYOFF receipts.

---

## Transport 6 — common environmental shift

If every patch gap changes by one common additive environmental effect

```text
phi_j(e)
= phi_j0+alpha(e-e0),
```

then the rare-D operator changes by

```text
+alpha(e-e0)I.
```

Therefore

```text
Lambda_D(e,m)
= Lambda_D(e0,m)+alpha(e-e0),
```

and reciprocal rare-S invasion receives the opposite shift.

The entire spatial spectrum moves without distortion. This is an exact environmental transport rule.

---

## Transport 7 — common temporal forcing

If temporal variation is also a common additive shift,

```text
A(t)=A0+q(t)I,
```

then

```text
Lambda_temporal
= lambda_max(A0)+mean(q).
```

The temporal forcing is transported only through its mean.

Zero-mean common temporal variation is therefore an exact null:

```text
no temporal premium.
```

---

## Transport 8 — two-season noncommuting temporal structure

When relative patch quality changes across two seasons, the seasonal operators need not commute.

For the declared symmetric two-patch model,

```text
Lambda_F
= lambda_max(A_bar)+P_temp,
```

with

```text
P_temp>=0.
```

`P_temp` is exactly zero at the commuting gates and positive otherwise.

Under rapid switching,

```text
P_temp
=
T^2 w^2(1-w)^2 m^2(Delta patch contrast)^2
/[24 delta_bar]
+O(T^4).
```

Thus the temporal structure acts as an additional population-level payoff receipt rather than modifying the upstream definition of `L`, `s`, or `K`.

---

## Transport 9 — temporal inversion of the coordination barrier

In symmetric anti-phase seasonal switching around mean static gap `phi_bar`, both reciprocal architecture invasion problems receive the same temporal premium `P`:

```text
Lambda_D=phi_bar-eta+P,
Lambda_S=-phi_bar-eta+P.
```

Therefore define

```text
eta_eff=eta-P.
```

At the reciprocal invasion edges, temporal source switching acts exactly like a reduction of the endpoint coordination barrier:

```text
eta -> eta_eff.
```

This is an edge-level transport identity, not a claim that the full nonlinear frequency-dependent game is globally equivalent to replacing `eta` everywhere.

At `phi_bar=0`:

```text
P<eta  coordination,
P=eta  collapsed reciprocal boundary,
P>eta  reciprocal invasion.
```

---

## Transport 10 — weak-contrast universal scaling

For anti-phase switching with

```text
u=m tau,
v=x tau,
```

and weak contrast `v<<1`,

```text
tau P
= v^2 H(u)+O(v^4),
```

where

```text
H(u)=[u-tanh u]/(2u^2).
```

The shape has one universal maximum at

```text
u*=1.60611529880277...
```

with

```text
H*=0.132487539446827....
```

Thus the temporal transport itself has an asymptotically universal optimal migration timescale:

```text
m_opt tau -> 1.6061153.
```

---

# What is preserved across transports?

Several quantities repeatedly remain meaningful.

## Static center

In models that transform `phi` only by a positive multiplier or symmetric population effects, the central static crossing

```text
phi=0
```

continues to organize the phase diagram even when it is no longer the invasion boundary.

## Common fitness scale

Every transport assumes the input architecture payoffs are expressed on a scale where

```text
R,
K,
phi
```

are commensurable.

If this fails, downstream algebra can be internally correct while the biological bridge is invalid.

## Reciprocal architecture labels

The framework always distinguishes

```text
static architecture quality,
rare invasion,
fixation,
stationary occupancy,
spatial growth,
temporal Floquet growth.
```

They are different estimands even though they receive the same upstream `phi`.

---

# What changes across transports?

The population layer determines what surrounds `phi`:

```text
frequency dependence -> eta
finite population     -> N,beta
mutation              -> u_SD/u_DS
regular graph         -> k
patch migration       -> m,L_G
spatial heterogeneity -> vector phi_j,eta_j
time variation        -> seasonal operators, durations
```

The contribution of PAYOFF is not that these population processes are new. It is that the ecological architecture quantities can be passed into them through explicit, auditable receipts.

---

# Cross-scale falsification strategy

The strongest use of the framework is not to estimate every layer from one dataset.

Instead:

```text
SCH
-> estimate L

BITA/BALANCE
-> estimate s,R,K
-> predict phi_bridge=sL-K

PAYOFF endpoint game
-> estimate eta independently

space/time experiment
-> fix migration, patch contrasts, season durations
-> predict spatial/Floquet outcome

final comparison
-> observed downstream dynamics ?= frozen prediction.
```

A downstream mismatch is informative. It can expose failure of the quadratic bridge, common fitness scale, architecture cost estimate, frequency-feedback model, migration model, or temporal/spatial assumptions.

---

# Compact master chain

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
    +--> frequency game
    +--> fixation
    +--> stationary occupancy
    +--> spatial spectral growth
    +--> temporal Floquet growth
```

The paper-level question is therefore:

> **How is a measurable within-organism functional compromise transported into the population-level evolutionary fate of shared versus differentiated trait architectures across frequency dependence, drift, mutation, space, and time?**
