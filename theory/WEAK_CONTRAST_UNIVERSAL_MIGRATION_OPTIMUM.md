# Weak seasonal contrast: universal optimal migration constant

This note takes the exact anti-phase seasonal rescue model and studies the weak-contrast regime

```text
v=|x| tau << 1.
```

The exact dimensionless premium is

```text
F(u,v)
= tau P
= -u
  + asinh[
      u/sqrt(u^2+v^2)
      *sinh(sqrt(u^2+v^2))
    ],
```

where

```text
u=m tau,
v=x tau.
```

The main result is that the migration optimum approaches one universal dimensionless number, independent of the absolute architecture margin scale.

---

## Theorem 1 — weak-contrast expansion

For fixed `u>0` and `v->0`,

```text
F(u,v)
= v^2 H(u)+O(v^4),
```

where

```text
H(u)
= [u-tanh(u)]/(2u^2).
```

Hence on the original growth scale,

```text
P(m,x,tau)
= x^2 tau H(m tau)
  + O(x^4 tau^3).
```

### Proof

Expand

```text
d=sqrt(u^2+v^2)
```

and

```text
asinh[(u/d)sinh d]
```

around `v=0`. For `u>0`,

```text
asinh(sinh u)=u.
```

The quadratic term is

```text
v^2[1/(2u)-tanh(u)/(2u^2)]
```

which equals `v^2 H(u)`. Odd powers vanish because the exact premium depends on `v` only through `v^2`. QED.

---

## Theorem 2 — H(u) has one positive maximizer

For `u>0`,

```text
H'(u)
=
[u tanh^2(u)-2u+2tanh(u)]/(2u^3).
```

Define

```text
f(u)
= u tanh^2(u)-2u+2tanh(u).
```

Then

```text
f'(u)
= tanh(u) sech^2(u)
  [2u-sinh(u)cosh(u)].
```

Let

```text
g(u)=2u-sinh(u)cosh(u).
```

Its derivative is

```text
g'(u)=2-cosh(2u).
```

Thus `g'` is initially positive, crosses zero exactly once, and is thereafter negative. Since

```text
g(0)=0
```

and

```text
g(u)->-infinity,
```

`g` has exactly one positive zero. Therefore `f'` is first positive and then negative.

Also

```text
f(0)=0,
```

with

```text
f(u)=u^3/3+O(u^5)
```

near zero, while

```text
f(u)=2-u+o(1)
```

as `u->infinity`.

Hence `f` crosses zero exactly once for `u>0`. Therefore `H'` changes sign exactly once from positive to negative, proving that `H` has one unique positive maximizer. QED.

---

## Corollary 2.1 — universal dimensionless optimum

The unique positive root of

```text
u tanh^2(u)-2u+2tanh(u)=0
```

is

```text
u_star
= 1.60611529880277...
```

Therefore, for weak seasonal contrast,

```text
m_opt tau
-> 1.6061152988.
```

Equivalently,

```text
m_opt
~= 1.6061152988/tau.
```

This is a universal leading-order prediction of the declared anti-phase model.

---

## Corollary 2.2 — universal maximum-shape constant

At the optimum,

```text
H(u_star)
= 0.132487539446827...
```

Therefore

```text
P_max
~= 0.13248753945 x^2 tau
```

for

```text
|x|tau << 1.
```

The rescue capacity scales quadratically with seasonal patch contrast and linearly with season duration in this weak-contrast regime.

---

## Corollary 2.3 — approximate rescue criterion

Let the time-averaged landscape be a sink:

```text
r_bar<0.
```

The exact anti-phase rescue criterion is

```text
P_max>-r_bar.
```

Under weak contrast this becomes

```text
0.13248753945 x^2 tau
> -r_bar.
```

Thus the approximate rescue boundary is

```text
-r_bar
= 0.13248753945 x^2 tau.
```

This is a quantitative architecture-rescue receipt:

```text
average deficit
versus
seasonal contrast^2 x season duration.
```

---

## Biological interpretation

For rare differentiated architecture,

```text
r_jl^D
= s_jl L_jl-K_jl-eta_jl.
```

In the symmetric anti-phase special case,

```text
r_bar
```

is the seasonal and patch average of these margins, while

```text
2x
```

is the seasonal between-patch difference in the rare-D margin.

The weak-contrast theorem therefore predicts, without fitting migration response itself:

```text
optimal migration
~= 1.6061/tau,

maximum temporal rescue budget
~= 0.13249 x^2 tau.
```

A prospective experiment can estimate `r_bar`, `x`, and `tau` from seasonal architecture assays, then test the predicted connectivity scale on independent populations.

---

## Claim boundary

The existence of intermediate-dispersal optima in periodic source-sink systems is established prior theory.

PAYOFF should claim only the **weak-contrast asymptotic specialization of its architecture-calibrated anti-phase model**, including the derived constants

```text
u_star=1.6061152988...
```

and

```text
H(u_star)=0.13248753945...
```

under the declared assumptions.
