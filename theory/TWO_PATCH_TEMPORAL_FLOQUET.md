# Two-patch temporal heterogeneity and Floquet architecture invasion

`COMMON_TEMPORAL_ENVIRONMENT.md` proves an exact null result: if every patch receives the same additive environmental shift, temporal variance and season order do not affect the rare-architecture invasion exponent beyond the time mean.

This note identifies the minimal way to leave that null class.

For one rare architecture, season `l` has two-patch local margins

```text
r_1,l,
r_2,l
```

and duration `tau_l>0`. Migration is symmetric and constant at rate `m>=0`.

The seasonal operator is

```text
A_l
= [[r_1,l-m, m],
   [m, r_2,l-m]].
```

Over one period, the exact propagator is

```text
P
= exp(A_M tau_M)
  ...
  exp(A_2 tau_2)
  exp(A_1 tau_1).
```

The principal Floquet architecture-invasion exponent is

```text
Lambda_F
= (1/T) log rho(P),
T=sum_l tau_l.
```

---

## Theorem 1 — exact seasonal matrix exponential

For one season define

```text
a=r_1-m,
d=r_2-m,
b=m,

c=(a+d)/2,
x=(a-d)/2,
delta=sqrt(x^2+b^2).
```

Then

```text
exp(A tau)
= exp(c tau)
  [ cosh(delta tau) I
    + sinh(delta tau)/delta (A-cI) ].
```

This gives the exact period map and Floquet exponent without time discretization.

---

## Theorem 2 — patch-contrast change is the noncommutativity gate

Take two seasonal operators `A_a,A_b` with the same migration rate. Their commutator is

```text
[A_a,A_b]
= c_ab
  [[0,1],[-1,0]],
```

where

```text
c_ab
= m[(r_1,a-r_2,a)-(r_1,b-r_2,b)].
```

Therefore the seasonal operators commute iff

```text
m=0
```

or their patch contrasts are identical:

```text
r_1,a-r_2,a
= r_1,b-r_2,b.
```

### Consequence

A common additive temporal environmental shift changes

```text
r_1,l
```

and

```text
r_2,l
```

by the same amount, leaving the contrast unchanged. It therefore lies exactly in the commuting null class proved previously.

To obtain a genuine temporal effect beyond the time-averaged operator, the model needs both:

```text
migration connecting patches
and
seasonal change in relative patch quality.
```

This is a necessary gate, not a sufficient sign rule: noncommutativity can increase or decrease the Floquet exponent depending on the seasonal margins and durations.

---

## Theorem 3 — the time-averaged operator is not generally sufficient

Define weighted temporal means

```text
r_1_bar
= sum_l tau_l r_1,l / T,

r_2_bar
= sum_l tau_l r_2,l / T.
```

The naive time-average prediction is

```text
Lambda_avg
= lambda_max
  [[r_1_bar-m, m],
   [m, r_2_bar-m]].
```

When seasonal operators fail to commute,

```text
Lambda_F
```

need not equal

```text
Lambda_avg.
```

Define the temporal noncommutativity effect

```text
E_temporal
= Lambda_F-Lambda_avg.
```

There is no universal sign for `E_temporal` in the declared model.

---

## Example — temporal switching can rescue architecture invasion

Take two equal-duration seasons and migration

```text
m=0.3.
```

Season 1 margins:

```text
(r_1,r_2)=(-2.5, 1.0).
```

Season 2 margins:

```text
(r_1,r_2)=(2.0, -1.0).
```

The time-averaged margins are

```text
(-0.25,0.0).
```

The time-averaged operator has principal exponent

```text
Lambda_avg=-0.1.
```

so an average-environment model predicts decline.

The exact periodic product instead gives approximately

```text
Lambda_F=0.03353>0.
```

so the rare architecture grows under periodic switching.

This is a PAYOFF example of a known class of dispersal-induced growth / time-periodic source-sink effects. The phenomenon itself is prior art; the architecture interpretation enters through the local margins.

---

## Architecture substitution

For rare differentiated architecture in season `l`,

```text
r_j,l^D
= phi_j,l-eta_j,l
= s_j,l L_j,l-K_j,l-eta_j,l.
```

Thus the seasonal Floquet operator can receive season-specific ecological quantities from the upstream architecture programme.

For rare shared architecture,

```text
r_j,l^S
= -phi_j,l-eta_j,l.
```

The D and S Floquet exponents should be computed separately; reciprocal invasion in a time-periodic landscape is a pair of principal Floquet conditions, not one scalar static threshold.

---

## 5. Empirical null-first workflow

A temporal architecture experiment should proceed in this order:

```text
Step 1
Test whether environmental effects are a common additive shift.

Step 2
If yes, use COMMON_TEMPORAL_ENVIRONMENT.md:
only the time mean matters.

Step 3
If patch contrasts change among seasons,
compute seasonal local margins and the exact Floquet exponent.

Step 4
Compare Lambda_F with Lambda_avg.
The difference is a temporal-structure receipt that cannot be absorbed into one mean phi without losing mechanism.
```

This avoids claiming a temporal-variability effect when the model mathematically predicts none.

---

## 6. Prior-art boundary

Floquet theory, periodic linear cooperative systems, time-varying source-sink dynamics, and dispersal-induced growth are established theory.

Relevant examples include:

- Katriel (2022), *Dispersal-induced growth in a time-periodic environment*, which studies periodic patch growth and dispersal through Floquet theory.
- Benaim and collaborators (2025), *Dispersal-induced growth or decay in a time-periodic environment. The case of reducible migration matrices*, which further develops periodic source-sink growth/decay phenomena.

PAYOFF does not claim these phenomena as new. The model-specific contribution is the substitution

```text
r_j,l^D
= s_j,lL_j,l-K_j,l-eta_j,l
```

and the explicit commutator diagnostic showing exactly when the simpler common-temporal-environment null model ceases to apply.
