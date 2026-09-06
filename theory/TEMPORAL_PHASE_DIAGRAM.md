# Dimensionless temporal phase diagram for reciprocal architecture invasion

This note compresses the anti-phase temporal architecture game into four dimensionless variables.

For two equal-length seasons of duration `tau`, symmetric migration `m`, mean static architecture gap `phi_bar`, common frequency-feedback coefficient `eta`, and anti-phase half-contrast `x`, define

```text
u = m tau,
v = x tau,
epsilon = eta tau,
psi = phi_bar tau.
```

The exact dimensionless temporal premium is

```text
F(u,v)
= tau P
= -u
  + asinh[
      u/sqrt(u^2+v^2)
      *sinh(sqrt(u^2+v^2))
    ].
```

At `u=0`, set `F(0,v)=0` by continuity.

The reciprocal rare-architecture Floquet exponents multiplied by `tau` are

```text
ell_D
= psi-epsilon+F(u,v),

ell_S
= -psi-epsilon+F(u,v).
```

Everything in the exact anti-phase reciprocal-invasion problem follows from these two scalar expressions.

---

## Theorem 1 — exact four-phase partition

Define

```text
Q(u,v,epsilon)
= F(u,v)-epsilon.
```

Then

```text
ell_D=Q+psi,
ell_S=Q-psi.
```

Therefore:

### Reciprocal invasion

```text
Q>|psi|
```

iff both architectures invade when rare.

### Mutual non-invasion / coordination

```text
Q<-|psi|
```

iff neither architecture invades when rare.

### D-only invasion

```text
-|psi|<Q<|psi|
and
psi>0.
```

### S-only invasion

```text
-|psi|<Q<|psi|
and
psi<0.
```

At `psi=0`, the directional region collapses and the sign of `Q` alone determines reciprocal invasion versus coordination.

### Proof

Immediate from the signs of

```text
Q+psi
```

and

```text
Q-psi.
```

QED.

---

## Corollary 1.1 — exact temporal reciprocal boundaries

For fixed `u,v,epsilon`, rare-D neutrality is

```text
psi_D
= epsilon-F(u,v),
```

while rare-S neutrality is

```text
psi_S
= -epsilon+F(u,v).
```

Thus the two boundaries remain symmetric around

```text
psi=0,
```

and their signed half-width is

```text
epsilon_eff
= epsilon-F(u,v).
```

Equivalently on the original scale,

```text
eta_eff
= eta-P.
```

If

```text
epsilon_eff>0,
```

the central region is mutual non-invasion. If

```text
epsilon_eff<0,
```

the central region has inverted into reciprocal invasion.

---

## Theorem 2 — temporal inversion surface

At the static architecture midpoint

```text
psi=0,
```

the exact inversion surface is

```text
F(u,v)=epsilon.
```

Therefore:

```text
F(u,v)<epsilon
-> coordination,

F(u,v)=epsilon
-> reciprocal neutral boundary,

F(u,v)>epsilon
-> reciprocal invasion.
```

This is the exact dimensionless temporal analogue of the static game condition around `phi=0`.

---

## Theorem 3 — weak-contrast phase boundary

For

```text
v<<1,
```

one has

```text
F(u,v)
= v^2 H(u)+O(v^4),
```

where

```text
H(u)
= [u-tanh u]/(2u^2).
```

Hence the temporal inversion surface becomes

```text
v^2 H(u)=epsilon
```

at leading order.

Because `H` has one positive maximum

```text
H_star
=0.132487539446827...
```

at

```text
u_star
=1.60611529880277...,
```

there are three weak-contrast regimes.

### Below threshold

If

```text
v^2 H_star < epsilon,
```

no migration rate can invert coordination.

### Critical point

If

```text
v^2 H_star = epsilon,
```

the two temporal switch boundaries merge at

```text
u=nu_star.
```

### Reciprocal-invasion island

If

```text
v^2 H_star > epsilon,
```

there are exactly two positive migration boundaries

```text
u_- < nu_star < nu_+
```

solving

```text
v^2 H(u)=epsilon.
```

The middle interval

```text
u_-<u<nu_+
```

has reciprocal invasion at `psi=0`; low and high migration retain coordination.

---

## Corollary 3.1 — universal weak-contrast control parameter

The existence of the reciprocal-invasion island is determined by

```text
v^2/epsilon
= x^2 tau/eta.
```

The threshold is

```text
x^2 tau/eta
> 1/H_star
= 7.547879628343014...
```

for `eta>0`.

Thus the competition is between

```text
seasonal spatial contrast squared x temporal duration
```

and

```text
positive-frequency coordination strength.
```

---

## Corollary 3.2 — static gap tilts the temporal island

For nonzero

```text
psi=phi_bar tau,
```

reciprocal invasion requires the stronger condition

```text
F(u,v)-epsilon>|psi|.
```

Equivalently,

```text
P(m,x,tau)>eta+|phi_bar|.
```

Thus a static architecture advantage for either side does not destroy the temporal mechanism, but it raises the premium required for reciprocal invasion.

In the directional strip

```text
-|psi|<F-epsilon<|psi|,
```

only the statically favored architecture can invade.

---

## 4. Phase-diagram coordinates

A compact manuscript phase diagram can use

```text
x-axis: u=m tau

y-axis: v^2/epsilon=x^2 tau/eta
```

at `psi=0`, with the exact boundary

```text
F(u,v)=epsilon
```

or the weak-contrast boundary

```text
[v^2/epsilon] H(u)=1.
```

The weak-contrast diagram has:

```text
low u       coordination
intermediate u reciprocal invasion when v^2/epsilon>7.54788...
high u      coordination.
```

The tip of the reciprocal-invasion island occurs at

```text
u=1.6061153...
```

and

```text
v^2/epsilon=7.5478796....
```

---

## 5. PAYOFF mapping

The dimensionless variables are built from ecological architecture quantities:

```text
phi_bar
= seasonal/patch mean of sL-K,

eta
= endpoint frequency-feedback strength,

x
= half-amplitude of the anti-phase seasonal difference in local architecture margin,

tau
= season duration,

m
= architecture-bearing migration/connectivity rate.
```

For rare D, the local margin is

```text
sL-K-eta.
```

For rare S, it is

```text
-sL+K-eta.
```

Thus the phase diagram remains anchored to the SCH/BALANCE/BITA estimands.

---

## 6. Interpretation

The temporal phase diagram reveals a non-monotone connectivity effect:

```text
low migration
-> seasonal sources cannot exchange enough individuals
-> coordination remains;

intermediate migration
-> seasonal source switching generates enough premium
-> coordination can invert to reciprocal invasion;

high migration
-> spatial contrast is homogenized
-> temporal premium vanishes
-> coordination returns.
```

This is not a claim that temporal heterogeneity universally promotes coexistence. It is an exact result for the declared anti-phase two-patch architecture-invasion model.

---

## Claim boundary

The general ideas of dispersal-induced growth, temporal source-sink rescue, and intermediate-dispersal effects are prior art.

PAYOFF's candidate contribution is the dimensionless architecture-game bridge

```text
(sL-K, eta, seasonal contrast, migration, season duration)
-> (psi,epsilon,v,u)
-> exact reciprocal architecture phase.
```
