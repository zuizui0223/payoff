# Exact two-season temporal premium in the two-patch PAYOFF invasion model

This note sharpens the two-patch Floquet layer for exactly two seasons.

The result is deliberately model-bounded:

```text
- two patches,
- one rare architecture at a time,
- symmetric time-independent migration m>=0,
- two piecewise-constant seasons,
- linearized invasion dynamics.
```

Within that model, periodic temporal heterogeneity cannot reduce the principal invasion exponent below the exponent of the time-averaged operator. The premium is exactly computable and, under rapid switching, begins at second order in the total period.

This is a specialization of established matrix inequalities and periodic metapopulation theory, not a new general theorem about arbitrary nonautonomous ecological systems.

---

## 1. Seasonal operator decomposition

Season `l` has local rare-type margins

```text
r_1l, r_2l
```

and duration

```text
tau_l>0.
```

With symmetric migration `m`,

```text
A_l
= [[r_1l-m, m],
   [m, r_2l-m]].
```

Define

```text
a_l = (r_1l+r_2l)/2 - m,
x_l = (r_1l-r_2l)/2,
d_l = sqrt(x_l^2+m^2).
```

Then

```text
A_l = a_l I + B_l
```

with

```text
B_l
= [[x_l, m],
   [m,  -x_l]],
```

and

```text
B_l^2=d_l^2 I.
```

Therefore

```text
exp(A_l tau_l)
= exp(a_l tau_l)
  [cosh(d_l tau_l) I
   + sinh(d_l tau_l) B_l/d_l].
```

---

## Theorem 1 — exact scalar Floquet formula

For two seasons `1,2`, let

```text
u_l=d_l tau_l
```

and

```text
Q
= exp(B_2 tau_2) exp(B_1 tau_1).
```

Because each `B_l` is traceless,

```text
det Q=1.
```

Its half-trace is

```text
C
= cosh(nu_1)cosh(nu_2)
  + gamma sinh(nu_1)sinh(nu_2),
```

where

```text
gamma
= (x_1 x_2 + m^2)/(d_1 d_2).
```

The eigenvalues of `Q` are

```text
exp(+acosh C)
and
exp(-acosh C).
```

Hence, with total period

```text
T=tau_1+tau_2,
```

the principal Floquet exponent is

```text
Lambda_F
= [a_1 tau_1+a_2 tau_2]/T
  + acosh(C)/T.
```

### Proof

Multiply the two exact seasonal exponentials. Terms linear in `B_l` have zero trace. The quadratic term has

```text
(1/2)tr(B_2 B_1)=x_1x_2+m^2.
```

This yields the stated half-trace. Since `Q` is a product of positive-definite matrix exponentials, it has positive real eigenvalues. With determinant one, they are reciprocal. Writing them as `e^q,e^-q` gives `C=cosh q`, hence `q=acosh C`. Restoring the scalar factors `exp(a_l tau_l)` and dividing the log multiplier by `T` gives the result. QED.

---

## Theorem 2 — two-season temporal premium is non-negative

Let

```text
A_bar
= (tau_1 A_1+tau_2 A_2)/T.
```

Then

```text
Lambda_F >= lambda_max(A_bar).
```

Equivalently,

```text
Delta_temp
= Lambda_F-lambda_max(A_bar)
>=0.
```

Thus, in the declared two-season symmetric two-patch model, replacing the periodic environment by its time-averaged invasion operator gives a lower bound on the true Floquet invasion exponent.

### Proof

Remove the scalar trace parts and write

```text
X=tau_1 B_1,
Y=tau_2 B_2.
```

`X` and `Y` are real symmetric, hence Hermitian. The Golden-Thompson inequality gives

```text
tr exp(X+Y)
<= tr[exp(X)exp(Y)].
```

Both matrices have determinant one. For a `2x2` matrix with positive reciprocal eigenvalues, the larger eigenvalue is a strictly increasing function of the trace. Therefore

```text
lambda_max[exp(X+Y)]
<= rho[exp(Y)exp(X)].
```

The left side is

```text
exp[T delta_bar],
```

where

```text
delta_bar
= sqrt(x_bar^2+m^2),
x_bar=(tau_1 x_1+tau_2 x_2)/T.
```

Adding back the identical scalar center contribution on both sides and taking log per unit time yields

```text
Lambda_F>=lambda_max(A_bar).
```

QED.

### Equality gate

For this model the seasonal operators commute iff

```text
m[(r_11-r_21)-(r_12-r_22)]=0.
```

Therefore the temporal premium vanishes at the basic commuting gates

```text
m=0
```

or

```text
(r_11-r_21)=(r_12-r_22).
```

The second condition means that seasons differ only by common shifts in patch quality rather than by changing relative patch contrast.

Golden-Thompson and its equality theory are established matrix analysis; PAYOFF only applies that machinery to this architecture-invasion operator.

---

## Corollary 2.1 — temporal rescue criterion

If the time-averaged operator predicts decline,

```text
lambda_max(A_bar)<0,
```

but

```text
Delta_temp > -lambda_max(A_bar),
```

then

```text
Lambda_F>0.
```

Thus periodic switching can turn a time-average sink into an invasible architecture landscape.

The repository example

```text
season 1: (r1,r2)=(-2.5, 1.0)
season 2: (r1,r2)=( 2.0,-1.0)
m=0.3
```

gives

```text
lambda_max(A_bar)=-0.1
```

but

```text
Lambda_F ~= 0.03352797.
```

---

## Theorem 3 — rapid-switching premium starts at order T^2

Fix the season fractions

```text
w=tau_1/T,
1-w=tau_2/T,
0<w<1,
```

and let the total period `T -> 0` while holding the seasonal margins and migration fixed.

Define the seasonal patch contrasts

```text
c_1=r_11-r_21,
c_2=r_12-r_22,
```

and

```text
x_bar=[w c_1+(1-w)c_2]/2,
delta_bar=sqrt(x_bar^2+m^2).
```

For the nondegenerate case `delta_bar>0`,

```text
Lambda_F-lambda_max(A_bar)
=
T^2
* w^2(1-w)^2
* m^2(c_1-c_2)^2
/[24 delta_bar]
+ O(T^4).
```

### Proof sketch

Use the exact half-trace formula from Theorem 1 and expand

```text
C
= cosh(d_1 wT)cosh[d_2(1-w)T]
  + gamma sinh(d_1 wT)sinh[d_2(1-w)T]
```

through fourth order in `T`. Write

```text
acosh(C)
= T delta_bar + T^3 q_3 + O(T^5).
```

Matching the `T^4` coefficients in `cosh(acosh C)=C` gives

```text
q_3
= w^2(1-w)^2 m^2(c_1-c_2)^2
  /(24 delta_bar).
```

Division by the total period yields the stated `T^2` premium. QED.

---

## Interpretation of the rapid-switching coefficient

The leading premium is proportional to

```text
m^2
```

and

```text
(c_1-c_2)^2.
```

So rapid temporal rescue requires both:

```text
movement among patches
and
seasonal change in relative patch quality.
```

The premium also contains

```text
w^2(1-w)^2,
```

which is maximal for equal season lengths and approaches zero when one season occupies almost the whole cycle.

There is no first-order-in-period premium. The leading effect is quadratic in `T`; this is consistent with the fact that the first Baker-Campbell-Hausdorff commutator contribution is skew-symmetric and does not shift the principal eigenvalue of the symmetric time-average at first order.

---

## PAYOFF substitution

For rare differentiated architecture in season `l`, patch `j`,

```text
r^D_jl
= phi_jl-eta_jl
= s_jl L_jl-K_jl-eta_jl.
```

Therefore the seasonal contrast entering the exact and rapid-switching formulas is

```text
c^D_l
= (s_1l L_1l-K_1l-eta_1l)
  -(s_2l L_2l-K_2l-eta_2l).
```

For rare shared architecture,

```text
r^S_jl
= -phi_jl-eta_jl.
```

The temporal theorem therefore receives the same upstream ecological quantities as the static, spatial, and stochastic layers rather than introducing an abstract seasonal growth parameter disconnected from SCH/BALANCE/BITA.

---

## Prior-art boundary

The following are established theory:

- Golden-Thompson trace inequality for Hermitian matrices;
- Floquet theory for periodic linear systems;
- dispersal-induced growth in periodic patch environments;
- source-sink rescue through spatiotemporal environmental variation.

Useful anchors include:

- Golden and Thompson (1965) for the trace inequality; see Forrester & Thompson (2014), arXiv:1408.2008, for a historical survey.
- Katriel (2022), *Dispersal-induced growth in a time-periodic environment*, Journal of Mathematical Biology 85:24, DOI `10.1007/s00285-022-01791-7`.
- Benaim, Lobry, Sari & Strickler and later work on dispersal-induced growth/decay in periodic environments.

PAYOFF should therefore claim only:

> We derive the exact two-season Floquet specialization, its non-negative temporal premium relative to the time-averaged PAYOFF invasion operator, and its rapid-switching coefficient after substituting the ecology-calibrated architecture margins `sL-K-eta`.

It should not claim to discover Golden-Thompson, Floquet theory, or dispersal-induced growth.
