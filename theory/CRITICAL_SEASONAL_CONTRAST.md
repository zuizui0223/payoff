# Exact critical seasonal contrast for temporal architecture rescue

The anti-phase model has exact dimensionless premium

```text
F(u,v)
= -u
  + asinh[
      u/sqrt(u^2+v^2)
      *sinh(sqrt(u^2+v^2))
    ],
```

with

```text
u=m tau,
v=|x|tau.
```

For each `v>0`, `EXACT_ANTI_PHASE_OPTIMUM.md` proves one unique optimal migration

```text
u_star(v)
```

and therefore one exact maximum premium

```text
M(v)
= max_u F(u,v).
```

This note proves that `M(v)` is strictly increasing. Consequently every positive coordination/static barrier has one unique critical seasonal contrast.

---

## Theorem 1 — F(u,v) is strictly increasing in contrast at fixed positive migration

For every

```text
u>0,
v>0,
```

one has

```text
partial F/partial v > 0.
```

### Proof

Let

```text
d=sqrt(u^2+v^2)
```

and

```text
y(u,v)
= [u/d]sinh d.
```

Then

```text
F=-u+asinh y.
```

Differentiating with respect to `v`,

```text
partial y/partial v
=
u v
[d cosh d-sinh d]
/d^3.
```

For `d>0`,

```text
d cosh d-sinh d>0
```

because it vanishes at zero and its derivative is

```text
d sinh d>0.
```

Hence

```text
partial y/partial v>0.
```

Since `asinh` is strictly increasing,

```text
partial F/partial v>0.
```

QED.

---

## Theorem 2 — exact maximum temporal premium M(v) is strictly increasing

For

```text
0<v_1<v_2,
```

one has

```text
M(v_1)<M(v_2).
```

### Proof

Let `u_1>0` be the unique maximizer at `v_1`. By Theorem 1,

```text
F(u_1,v_2)>F(u_1,v_1)=M(v_1).
```

But

```text
M(v_2)
=max_u F(u,v_2)
>=F(u_1,v_2).
```

Therefore

```text
M(v_2)>M(v_1).
```

QED.

---

## Theorem 3 — one unique critical contrast for every positive barrier

Let

```text
B>0
```

be a dimensionless reciprocal-invasion barrier.

Because

```text
M(0)=0
```

and, from the strong-contrast asymptotic,

```text
M(v)
= v-log v-1+O(v^-1)
-> infinity,
```

while Theorem 2 gives strict monotonicity, there exists exactly one

```text
v_c>0
```

such that

```text
M(v_c)=B.
```

Therefore:

```text
v<v_c
-> no migration rate can supply premium B;

v=v_c
-> the barrier is reached only at the unique optimal migration;

v>v_c
-> exactly one bounded migration interval supplies premium greater than B.
```

QED.

---

## Corollary 3.1 — exact coordination-inversion contrast

At

```text
phi_bar=0,
eta>0,
```

the dimensionless barrier is

```text
B=eta tau.
```

The exact minimum seasonal half-contrast needed for any migration treatment to overcome coordination is

```text
|x|_c
= v_c(eta tau)/tau.
```

If

```text
|x|<|x|_c,
```

coordination persists for every migration rate.

If

```text
|x|>|x|_c,
```

there is one and only one intermediate migration interval with reciprocal architecture invasion.

---

## Corollary 3.2 — nonzero static architecture gap

For general

```text
phi_bar,
```

reciprocal invasion requires

```text
P>eta+|phi_bar|.
```

Thus

```text
B
= (eta+|phi_bar|)tau
```

and the critical contrast is

```text
|x|_c
= v_c[(eta+|phi_bar|)tau]/tau.
```

The static architecture advantage therefore raises the seasonal contrast required for both architectures to invade reciprocally.

---

## Theorem 4 — weak-barrier critical contrast

For

```text
B->0+,
```

the critical contrast is weak, so

```text
M(v)
= H_star v^2+O(v^4),
```

where

```text
H_star
=0.132487539446827....
```

Therefore

```text
v_c(B)
= sqrt(B/H_star)
  [1+O(B)].
```

At `phi_bar=0`,

```text
|x|_c
~= sqrt[eta/(H_star tau)].
```

Equivalently,

```text
x_c^2 tau/eta
~=1/H_star
=7.547879628343014....
```

This recovers the weak-contrast threshold in `TEMPORAL_COORDINATION_INVERSION.md`.

---

## Theorem 5 — strong-barrier critical contrast

For large `B`, use

```text
M(v)
= v-log v-1+O(v^-1).
```

Inverting gives

```text
v_c(B)
= B+log B+1+o(1).
```

Thus, under very strong positive-frequency or static barriers, the seasonal contrast required for temporal reciprocal invasion grows approximately linearly with the barrier, with a logarithmic correction.

---

## Exact phase hierarchy

For fixed

```text
B=(eta+|phi_bar|)tau>0,
```

the exact anti-phase temporal problem has three levels:

```text
contrast below v_c
    no reciprocal-invasion migration interval

contrast exactly v_c
    one tangent migration point

contrast above v_c
    exactly two migration boundaries
    enclosing one reciprocal-invasion island.
```

This turns the temporal phase diagram into a genuine cusp-like organization in contrast and migration, although no catastrophe-theory novelty claim is intended.

---

## Empirical interpretation

The threshold is built from quantities that can be frozen before a connectivity experiment:

```text
eta
phi_bar
season duration tau
```

which determine

```text
B=(eta+|phi_bar|)tau.
```

The theory then predicts a minimum seasonal architecture-margin contrast

```text
2|x|_c
```

between patches.

A prospective test can therefore ask first:

> Is observed seasonality even strong enough for any migration rate to overcome the architecture barrier?

Only if the answer is yes does it make sense to test the predicted intermediate migration island.

---

## Claim boundary

Thresholds for dispersal-induced persistence under temporal heterogeneity are established in broader source-sink theory.

PAYOFF's claim is the exact monotone contrast threshold after transporting the ecology-calibrated architecture margins into the declared anti-phase two-patch game, not a universal critical-contrast theorem for arbitrary periodic metapopulations.
