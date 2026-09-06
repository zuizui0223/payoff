# Exact uniqueness of the anti-phase migration optimum

The anti-phase temporal premium has already been written as

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
u=m tau >=0,
v=|x|tau>0.
```

`ANTI_PHASE_SEASONAL_RESCUE.md` proves that the premium is zero at `u=0`, positive for finite `u>0`, and returns to zero as `u->infinity`.

This note strengthens the result:

> for every fixed nonzero seasonal contrast `v`, the exact anti-phase temporal premium has one and only one positive migration optimum.

---

## Theorem 1 — derivative sign reduces to one monotone crossing

Let

```text
d=sqrt(u^2+v^2),
s=sinh d,
c=cosh d.
```

For `u>0,v>0`, differentiation gives

```text
F_u
= -1
  + [v^2 s/d^3 + u^2 c/d^2]
    /sqrt[1+u^2 s^2/d^2].
```

The sign of `F_u` is the sign of

```text
R(d)-u^2/d^2,
```

where

```text
R(d)
= [sinh^2 d-d^2]
  /[d cosh d-sinh d]^2.
```

### Proof

Define

```text
N
= v^2 s/d^2 + u^2 c/d,

Q
= sqrt(v^2+u^2 c^2).
```

Then

```text
F_u=-1+N/Q.
```

Since `N,Q>0`, the sign of `F_u` is the sign of `N^2-Q^2`. Direct algebra gives

```text
N^2-Q^2
=
-v^2/d^4
[
 u^2(d c-s)^2
 -d^2(s^2-d^2)
].
```

Therefore

```text
F_u>0
```

iff

```text
u^2/d^2
<
(s^2-d^2)/(dc-s)^2
=R(d).
```

Equality gives the stationary point. QED.

---

## Theorem 2 — R(d) is strictly decreasing for d>0

For every

```text
d>0,
```

one has

```text
R'(d)<0.
```

### Proof

Differentiate:

```text
R'(d)
=
-2 H(d)
/[d cosh d-sinh d]^3,
```

where

```text
H(d)
=
cosh d(d^2+sinh^2 d)
-sinh d(d^3+2d).
```

First,

```text
d cosh d-sinh d>0
```

for `d>0` because this function is zero at the origin and has derivative

```text
d sinh d>0.
```

It remains to prove `H(d)>0`.

Using

```text
sinh^2 d cosh d
=[cosh(3d)-cosh d]/4,
```

expand `H` as an even power series. The coefficients of `d^2` and `d^4` vanish, and for `n>=3`,

```text
H(d)
=
sum_{n=3}^infinity
 A_n d^(2n)/(2n)!,
```

with

```text
A_n
= 9^n/4
  -8n^3
  +16n^2
  -10n
  -1/4.
```

One has

```text
A_2=0
```

and

```text
A_{n+1}-9A_n
=8n(n-1)(8n-11)>0
```

for every `n>=2`.

Hence

```text
A_n>0
```

for all `n>=3`, so

```text
H(d)>0
```

for every `d>0`. Therefore `R'(d)<0`. QED.

---

## Theorem 3 — the exact migration optimum is unique

For fixed

```text
v>0,
```

the function

```text
F(u,v)
```

has exactly one stationary point on

```text
u>0,
```

and that point is the unique global maximum.

### Proof

The stationary condition is

```text
u^2/d^2=R(d),
```

with

```text
d=sqrt(u^2+v^2).
```

As `u` increases, `d` increases. The left side can be written

```text
1-v^2/d^2,
```

which is strictly increasing in `d` from zero toward one.

By Theorem 2, `R(d)` is strictly decreasing and positive. Moreover

```text
R(d)->0
```

as `d->infinity`.

At `u=0`, the increasing left side is zero while `R(v)>0`. For sufficiently large `u`, the left side is near one while `R(d)` is near zero. Therefore the two curves cross exactly once.

By Theorem 1, `F_u` is positive before the crossing and negative after it. Thus the stationary point is the unique global maximum. QED.

---

## Corollary 3.1 — exact optimal migration is a one-parameter scaling function

Let

```text
u_star(v)
```

denote the unique maximizer.

Then the dimensional optimum is

```text
m_star
= nu_star(|x|tau)/tau.
```

Thus all anti-phase exact migration optima collapse onto one curve

```text
nu_star(v)
```

in the dimensionless contrast

```text
v=|x|tau.
```

---

## Corollary 3.2 — weak-contrast limit

As

```text
v->0,
```

the exact optimum converges to the weak-contrast universal constant

```text
nu_star(v)
-> 1.60611529880277....
```

This recovers `WEAK_CONTRAST_UNIVERSAL_MIGRATION_OPTIMUM.md`.

---

## Theorem 4 — strong-contrast asymptotic optimum

As

```text
v->infinity,
```

the exact optimum satisfies

```text
nu_star(v)
=1+1/v+O(v^-2).
```

Hence

```text
m_star tau
->1
```

under very strong seasonal patch contrast.

### Proof sketch

For large `d`,

```text
sinh d ~ cosh d ~ e^d/2,
```

so

```text
R(d)
=
1/(d-1)^2
[1+O(d^2 e^-2d)].
```

The exact stationary condition is

```text
u^2/d^2=R(d).
```

Thus

```text
u
= d/(d-1)
[1+o(d^-2)].
```

Since

```text
d=sqrt(v^2+u^2)=v+O(v^-1),
```

substitution gives

```text
u
=1+1/v+O(v^-2).
```

QED.

---

## Corollary 4.1 — strong-contrast maximum premium

At the exact optimum, as `v->infinity`,

```text
max_u F(u,v)
= v-log v-1+O(v^-1).
```

Therefore on the original growth scale,

```text
P_max
= |x|
  -[log(|x|tau)+1]/tau
  +O(1/(|x|tau^2)).
```

This strong-contrast expression should be used only when `|x|tau` is large; it is complementary to the weak-contrast quadratic law

```text
P_max
~=0.13248753945 x^2 tau.
```

---

## Biological interpretation

The exact theory predicts a contrast-dependent but bounded optimal timescale:

```text
weak seasonal contrast:
    m_star tau -> 1.6061153...

strong seasonal contrast:
    m_star tau -> 1.
```

So the best migration rate stays on the order of one movement event per seasonal timescale rather than diverging with contrast.

This gives a cleaner biological statement than simply saying "intermediate migration":

> the architecture-bearing migration timescale should be comparable to the timescale at which the identity of the favorable patch reverses.

---

## Claim boundary

Intermediate-dispersal optima are established in temporal source-sink theory.

PAYOFF should claim only the exact uniqueness proof and asymptotic specialization for the declared symmetric anti-phase architecture-invasion model, not a universal theorem that every periodically forced metapopulation has one migration optimum.
