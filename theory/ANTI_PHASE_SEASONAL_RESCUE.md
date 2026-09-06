# Anti-phase seasonal source switching: exact rescue premium and intermediate migration

This note specializes the two-season temporal PAYOFF model to the cleanest source-switching geometry.

Two patches exchange relative quality every season. Each season lasts `tau>0`:

```text
season A: (r_bar+x, r_bar-x)
season B: (r_bar-x, r_bar+x).
```

Here

```text
r_bar
```

is the time-averaged rare-architecture margin in either patch, while

```text
x
```

is half the seasonal between-patch contrast. Symmetric migration occurs at rate `m>=0`.

For a rare differentiated architecture, the margins can be read as

```text
r_jl^D=s_jl L_jl-K_jl-eta_jl.
```

The same mathematics applies to rare shared architecture after replacing the local margins by

```text
r_jl^S=-phi_jl-eta_jl.
```

---

## Theorem 1 — exact anti-phase Floquet exponent

Define

```text
delta=sqrt(m^2+x^2).
```

Then the exact principal Floquet exponent is

```text
Lambda_F
=
r_bar-m
+(1/tau)
asinh[(m/delta)sinh(delta tau)].
```

The time-averaged invasion operator has equal patch margins `r_bar`, so its principal exponent is exactly

```text
Lambda_avg=r_bar.
```

Hence the temporal rescue premium is

```text
P(m,x,tau)
=
Lambda_F-Lambda_avg
=
-m
+(1/tau)
asinh[(m/delta)sinh(delta tau)].
```

### Proof

In the two-season closed form from `TWO_SEASON_TEMPORAL_PREMIUM.md`, the two seasonal half-contrasts are

```text
x_1=+x,
x_2=-x,
```

with equal durations `tau`. Therefore

```text
d_1=d_2=delta.
```

The normalized half-trace reduces to

```text
C
= cosh^2(delta tau)
  + [(m^2-x^2)/(m^2+x^2)] sinh^2(delta tau)
```

which simplifies to

```text
C
= 1
  + 2[m^2/(m^2+x^2)]sinh^2(delta tau).
```

Using

```text
cosh(2 asinh y)=1+2y^2
```

gives

```text
acosh(C)
=2 asinh[(m/delta)sinh(delta tau)].
```

The full period is `2tau`; substituting into the exact two-season Floquet formula yields the result. QED.

---

## Theorem 2 — temporal premium is zero at both migration extremes

For fixed `x,tau`,

```text
P(0,x,tau)=0.
```

If `x!=0`, then for every finite

```text
m>0
```

one has

```text
P(m,x,tau)>0.
```

Moreover,

```text
lim_{m->infinity} P(m,x,tau)=0.
```

### Proof

At `m=0`, the patches are uncoupled and the seasonal operators are diagonal, so periodic ordering cannot change the exponent relative to the time average. The exact formula also gives zero directly.

For finite `m>0` and `x!=0`, the two seasonal operators do not commute. The strict two-season Golden-Thompson result therefore gives

```text
Lambda_F>Lambda_avg,
```

hence `P>0`.

As `m->infinity`,

```text
delta-m -> 0
```

and

```text
asinh[(m/delta)sinh(delta tau)]/tau - m -> 0.
```

The strong-migration expansion below makes the limit explicit. QED.

---

## Corollary 2.1 — at least one intermediate migration optimum exists

For `x!=0`, `P(m,x,tau)` is continuous, equals zero at `m=0`, is strictly positive for every finite positive `m`, and returns to zero as `m->infinity`.

Therefore there exists at least one finite

```text
m_opt>0
```

at which the temporal premium is maximal.

This proves an **intermediate-migration optimum** for seasonal architecture rescue in the declared anti-phase model.

No uniqueness claim is made here without an additional monotonicity proof.

---

## Corollary 2.2 — rescue of a negative average landscape

If

```text
r_bar<0,
```

the time-averaged landscape predicts decline.

Periodic anti-phase switching permits invasion exactly when

```text
P(m,x,tau)>-r_bar.
```

Therefore a negative-average architecture landscape is rescuable iff

```text
max_m P(m,x,tau)>-r_bar.
```

This creates a directly estimable rescue budget:

```text
temporal rescue capacity
= max_m P(m,x,tau).
```

The quantity should be compared with the architecture deficit `-r_bar`, not with zero alone.

---

## Theorem 3 — small-migration expansion

For fixed `x,tau` and `x!=0`, let

```text
z=|x|tau.
```

As `m->0+`,

```text
P(m,x,tau)
=
m[sinh(z)/z - 1]
+O(m^3).
```

Since

```text
sinh(z)/z>1
```

for every `z>0`, the initial migration slope is strictly positive.

### Interpretation

A small amount of migration always increases the temporal rescue premium when the seasonal source really switches between patches.

The initial sensitivity grows with the dimensionless seasonal contrast `|x|tau`.

---

## Theorem 4 — rapid-switching expansion

As

```text
tau->0
```

at fixed `m,x`,

```text
P(m,x,tau)
=
(m x^2 tau^2)/6
+O(tau^4).
```

Thus very rapid source switching has only a second-order effect.

This is the anti-phase reduction of the general two-season premium

```text
T^2 w^2(1-w)^2 m^2(Delta c)^2
/[24 delta_bar].
```

With equal seasons,

```text
T=2tau,
w=1/2,
Delta c=4x,
delta_bar=m,
```

which gives the stated formula.

---

## Theorem 5 — strong-migration asymptotic

For fixed positive `tau` and `x`, as `m->infinity`,

```text
P(m,x,tau)
=
x^2/(2m)
-x^2/(2m^2 tau)
+O(m^-3)
```

up to exponentially small terms in `m tau`.

Therefore strong migration destroys the seasonal premium at rate approximately

```text
x^2/(2m).
```

### Interpretation

Strong coupling homogenizes the patches too quickly for alternating local source quality to be exploited.

The anti-phase rescue mechanism therefore fails at both extremes:

```text
m=0       no transfer between seasonal sources
m>>1      patches homogenize too strongly
```

and is strongest in between.

---

## Dimensionless form

Let

```text
u=m tau,
v=x tau.
```

Then

```text
tau P
=
-u
+asinh[
  u/sqrt(u^2+v^2)
  *sinh(sqrt(u^2+v^2))
].
```

So the shape of the migration optimum depends only on the dimensionless pair

```text
(m tau, x tau).
```

The absolute growth-scale premium is recovered by division by `tau`.

This is useful for collapsing experiments with different generation times or seasonal durations onto one theoretical surface.

---

## PAYOFF interpretation

The anti-phase model says that temporal rescue requires three ingredients:

```text
1. seasonal architecture margin contrast x != 0,
2. migration m > 0,
3. enough temporal premium to pay the average architecture deficit -r_bar.
```

For rare differentiated architecture,

```text
r_bar
```

and

```text
x
```

are not free demographic abstractions. They can be constructed from seasonal patch-level

```text
sL-K-eta.
```

This creates the empirical chain

```text
seasonal SCH/BITA/BALANCE receipts
        |
        v
r_bar, x
        |
        v
exact temporal premium P(m,x,tau)
        |
        v
predict rescue interval in migration.
```

A strong test would estimate seasonal architecture margins independently, then manipulate connectivity/migration and predict where invasion appears and disappears without refitting the payoff geometry.

---

## Prior-art boundary

Intermediate-dispersal optima and dispersal-induced growth in alternating source-sink environments are established ideas in metapopulation theory.

PAYOFF does not claim to discover that migration can rescue periodically varying sinks.

The candidate contribution is narrower:

> the exact anti-phase specialization of the PAYOFF architecture margins, including the explicit temporal rescue premium and its asymptotic receipts, after substituting `r=sL-K-eta`.
