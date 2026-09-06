# Temporal source switching can invert the coordination barrier

This note connects the anti-phase temporal rescue result back to the core two-architecture evolutionary game.

Assume two patches and two equal-length seasons. Patch-specific static architecture gaps swap symmetrically around a mean gap:

```text
season A phi: (phi_bar+x, phi_bar-x)
season B phi: (phi_bar-x, phi_bar+x).
```

Let the frequency-feedback coefficient be one common constant

```text
eta.
```

For rare differentiated architecture,

```text
r^D=phi-eta.
```

For rare shared architecture,

```text
r^S=-phi-eta.
```

Because changing `phi` to `-phi` only swaps the anti-phase contrast sign, both reciprocal invasion problems receive the same exact temporal premium

```text
P=P(m,x,tau)>=0.
```

---

## Theorem 1 — exact reciprocal temporal exponents

The two rare-architecture Floquet exponents are

```text
Lambda_D
= phi_bar-eta+P,

Lambda_S
= -phi_bar-eta+P.
```

### Proof

Rare D has seasonal patch margins

```text
(phi_bar-eta+x, phi_bar-eta-x)
```

followed by their swap. The anti-phase theorem therefore gives

```text
Lambda_D=(phi_bar-eta)+P.
```

Rare S has seasonal patch margins

```text
(-phi_bar-eta-x, -phi_bar-eta+x),
```

which is the same anti-phase geometry with mean `-phi_bar-eta` and contrast amplitude `|x|`. Hence

```text
Lambda_S=(-phi_bar-eta)+P.
```

QED.

---

## Corollary 1.1 — temporal premium acts as an effective reduction in coordination

Define

```text
eta_eff
= eta-P.
```

Then

```text
Lambda_D=phi_bar-eta_eff,
Lambda_S=-phi_bar-eta_eff.
```

Thus the reciprocal invasion geometry has exactly the same algebraic form as the static endpoint game, but with

```text
eta -> eta_eff=eta-P.
```

This statement concerns reciprocal **rare-invasion exponents**. It does not imply that the entire nonlinear frequency-dependent game can always be replaced by a scalar `eta_eff` away from the invasion edges.

---

## Theorem 2 — exact classification of temporal reciprocal invasion

Let

```text
q=P-eta=-eta_eff.
```

Then:

### Reciprocal invasion

Both architectures invade when rare iff

```text
q>|phi_bar|,
```

i.e.

```text
P>eta+|phi_bar|.
```

### Mutual non-invasion

Neither architecture invades when rare iff

```text
q<-|phi_bar|,
```

i.e.

```text
P<eta-|phi_bar|.
```

### Directional region

Between those conditions, exactly one architecture invades, with direction determined by the sign of `phi_bar`.

### Proof

The two exponents are

```text
q+phi_bar
```

and

```text
q-phi_bar.
```

Both are positive exactly when `q>|phi_bar|`; both are negative exactly when `q<-|phi_bar|`. Otherwise their signs differ. QED.

---

## Corollary 2.1 — temporal middle-region inversion at phi_bar=0

At the mean static architecture crossing

```text
phi_bar=0,
```

one has

```text
Lambda_D=Lambda_S=P-eta.
```

Therefore

```text
P<eta
-> mutual non-invasion / coordination,

P=eta
-> both reciprocal boundaries coincide,

P>eta
-> reciprocal invasion.
```

The anti-phase temporal premium can therefore **invert the type of the middle region** around the same static crossing.

In the language of boundary width, the temporal half-width is

```text
|eta-P|.
```

Its biological type is determined by the sign of

```text
eta-P.
```

---

## Theorem 3 — exact reciprocal-invasion migration interval is unique

Assume

```text
eta>0,
x!=0,
tau>0.
```

By `EXACT_ANTI_PHASE_OPTIMUM.md`, the exact temporal premium

```text
P(m,x,tau)
```

is strictly increasing from zero to one unique maximum

```text
P_max
```

at one unique

```text
m_star>0,
```

and is then strictly decreasing back to zero as `m->infinity`.

Define the reciprocal-invasion target

```text
C
= eta+|phi_bar|.
```

Then exactly one of the following holds.

### No reciprocal-invasion migration interval

If

```text
P_max<C,
```

then both architectures are never simultaneously invasible for any migration rate.

### Tangency

If

```text
P_max=C,
```

then reciprocal neutrality occurs at exactly one migration rate

```text
m=m_star,
```

but there is no open reciprocal-invasion interval.

### One and only one reciprocal-invasion island

If

```text
P_max>C,
```

then the equation

```text
P(m,x,tau)=C
```

has exactly two positive solutions

```text
m_-<m_star<m_+.
```

Moreover,

```text
P>C
```

exactly on

```text
m_-<m<m_+.
```

Hence both architectures invade when rare on one and only one bounded intermediate-migration interval.

### Proof

Theorem 2 says reciprocal invasion is equivalent to `P>C`. Exact unimodality of `P` supplies the rest: a horizontal level below the unique maximum intersects the increasing and decreasing branches once each; equality touches only at the maximum; a level above the maximum does not intersect. QED.

---

## Corollary 3.1 — exact coordination inversion interval at phi_bar=0

At

```text
phi_bar=0,
```

the target becomes

```text
C=eta.
```

If

```text
P_max>eta,
```

there are exactly two migration switches

```text
m_-<m_+.
```

Then

```text
0<=m<m_-
-> coordination,

m_-<m<m_+
-> reciprocal invasion,

m>m_+
-> coordination.
```

Thus the temporal coordination inversion is not merely an intermediate-migration tendency: in the exact anti-phase model it is one uniquely bounded invasion island.

---

## Theorem 4 — weak-contrast criterion for whether coordination can be overcome

For

```text
|x|tau << 1,
```

the anti-phase maximum premium is

```text
P_max
~= H_star x^2 tau,
```

where

```text
H_star
= 0.132487539446827...
```

and the corresponding optimum obeys

```text
m_opt tau
~= 1.60611529880277.
```

Therefore temporal source switching can overcome the positive-frequency barrier at `phi_bar=0` approximately iff

```text
H_star x^2 tau > eta.
```

Equivalently,

```text
x^2 tau / eta
> 1/H_star
= 7.547879628343014...
```

for `eta>0`.

This is the weak-contrast temporal coordination-inversion threshold.

---

## Theorem 5 — weak-contrast migration band has two boundaries

Under weak contrast, write

```text
u=m tau.
```

The premium is

```text
P
~= x^2 tau H(u),
```

where

```text
H(u)=[u-tanh u]/(2u^2)
```

has one unique positive maximum at

```text
u_star=1.6061152988...
```

as proved in `WEAK_CONTRAST_UNIVERSAL_MIGRATION_OPTIMUM.md`.

If

```text
eta/(x^2 tau)<H_star,
```

then the equation

```text
H(u)=eta/(x^2 tau)
```

has exactly two positive roots

```text
u_-<nu_star<nu_+.
```

Therefore the approximate reciprocal-invasion band is

```text
nu_- < m tau < nu_+.
```

Outside this band the weak-contrast prediction returns to coordination.

At equality with `H_star`, the two thresholds merge at the universal optimum. Above `H_star`, no weak-contrast migration treatment overcomes coordination.

---

## Dimensionless phase diagram

At `phi_bar=0`, define

```text
u=m tau,
v=x tau,
epsilon=eta tau.
```

The exact anti-phase condition for reciprocal invasion is

```text
F(u,v)>epsilon,
```

where

```text
F(u,v)
= tau P
= -u
  + asinh[
      u/sqrt(u^2+v^2)
      *sinh(sqrt(u^2+v^2))
    ].
```

Thus the temporal coordination problem collapses to a dimensionless three-quantity comparison:

```text
migration timescale u,
seasonal contrast v,
coordination strength epsilon.
```

The weak-contrast boundary is simply

```text
v^2 H(u)=epsilon.
```

---

## PAYOFF interpretation

The core static/frequency game says positive `eta` creates a coordination barrier around

```text
phi=0.
```

The temporal anti-phase result adds a new possibility:

```text
seasonal architecture-margin switching
        |
        v
temporal premium P(m,x,tau)
        |
        v
eta_eff=eta-P
        |
        +-> eta_eff>0 : coordination persists
        +-> eta_eff=0 : reciprocal boundaries collapse
        +-> eta_eff<0 : reciprocal invasion.
```

The ecological quantities remain upstream:

```text
phi_jl=s_jl L_jl-K_jl.
```

So a future test can estimate seasonal `L,s,K,eta`, freeze the predicted temporal premium, and test whether connectivity moves the population through the predicted coordination-to-reciprocal-invasion transition.

---

## Claim boundary

Temporal coexistence/rescue generated by spatiotemporal heterogeneity and dispersal is established theory in broader metapopulation models.

PAYOFF should claim only the architecture-game specialization:

> In the declared anti-phase model, the same temporal premium enters both reciprocal architecture invasion exponents, so it subtracts from the endpoint coordination barrier as `eta_eff=eta-P`; exact unimodality gives one uniquely bounded reciprocal-invasion migration island whenever `P_max>eta+|phi_bar|`, and weak contrast yields the explicit threshold `x^2 tau/eta > 7.5478796...` at `phi_bar=0`.
