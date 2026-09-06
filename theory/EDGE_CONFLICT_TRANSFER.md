# Edge conflict transfer — how releasing one coupling reroutes pressure onto another

`EDGEWISE_MODULARIZATION.md` proves that the marginal value of weakening one coupling edge equals the squared optimized disagreement across that edge.

This note derives the cross-edge derivative: how changing one coupling alters the release pressure on every other edge.

That derivative is the local mechanism behind modularization cascades.

---

## 1. Setup

Let `b_e` be the oriented incidence vector of edge `e=(i,j)`, so

```text
b_e^T x=x_i-x_j.
```

Write

```text
A=diag(a_i),
M(c)=A+sum_e c_e b_e b_e^T.
```

The optimized phenotype is

```text
x*=M^-1 A theta.
```

Define signed optimized edge disagreement

```text
q_e=b_e^T x*.
```

Then edge release pressure is

```text
p_e=q_e^2.
```

Use decoupling coordinate

```text
d_e=c_e^0-c_e.
```

---

## Theorem T1 — phenotype response to edge decoupling

For any edge `e`,

```text
partial x*/partial d_e
=M^-1 b_e b_e^T x*
=q_e M^-1 b_e.
```

### Proof

Differentiate

```text
x*=M^-1 A theta
```

with respect to `d_e`.

Because

```text
partial M/partial d_e
=-b_e b_e^T,
```

and

```text
partial M^-1
=-M^-1(partial M)M^-1,
```

one obtains

```text
partial x*/partial d_e
=M^-1 b_e b_e^T x*.
```

Since `b_e^T x*=q_e`, the stated form follows. QED.

---

## Theorem T2 — exact edge pressure-transfer matrix

For target edge `f` and released edge `e`,

```text
partial p_f/partial d_e
=
2 q_f q_e b_f^T M^-1 b_e.
```

Define

```text
H_fe
=2 q_f q_e b_f^T M^-1 b_e.
```

Then `H` is exactly the Hessian of the recovery function `R(d)`:

```text
H=nabla_d^2 R.
```

### Proof

The marginal recovery theorem gives

```text
partial R/partial d_f
=p_f=q_f^2.
```

From Theorem T1,

```text
partial q_f/partial d_e
=b_f^T(partial x*/partial d_e)
=q_e b_f^T M^-1 b_e.
```

Therefore

```text
partial p_f/partial d_e
=2q_f partial q_f/partial d_e
=2q_f q_e b_f^T M^-1 b_e.
```

QED.

---

## Corollary T2.1 — recovery convexity is visible directly in the transfer matrix

Let `B` be the matrix whose columns are edge incidence vectors and let

```text
Q=diag(q_e).
```

Then

```text
H
=2 Q B^T M^-1 B Q.
```

Because `M^-1` is positive definite,

```text
H is positive semidefinite.
```

Thus the transfer formula supplies an explicit factorization of the convexity theorem for edgewise recovery.

---

## Corollary T2.2 — self-amplification of release pressure

For `f=e`,

```text
partial p_e/partial d_e
=2 q_e^2 b_e^T M^-1 b_e
>=0.
```

Therefore weakening an edge cannot reduce its own marginal recovery pressure in the declared quadratic model.

This is the local differential form of the convex finite-jump effect in `DISCONTINUOUS_MODULARIZATION_BARRIER.md`.

---

## 2. Cross-edge signs are not fixed

Although `H` is positive semidefinite, an individual off-diagonal entry

```text
H_fe
```

can be positive or negative.

Therefore releasing edge `e` can either:

```text
increase pressure on edge f
-> conflict rerouting / cascade;

or

decrease pressure on edge f
-> conflict relief / substitution.
```

The sign is determined by three signed factors:

```text
q_f,
q_e,
b_f^T M^-1 b_e.
```

Hence no universal rule says that removing one constraint must make all neighboring constraints more strained.

---

## 3. Three-function example

For the registered complete triangle

```text
theta=(0,1,3),
a_i=1,
c_e=1,
```

with edge order

```text
(01,02,12),
```

the optimized phenotype is

```text
x*=(1,5/4,7/4),
```

so

```text
q=(-1/4,-3/4,-1/2).
```

The exact transfer matrix is

```text
H =
[[ 1/16,  3/32, -1/16],
 [ 3/32,  9/16,  3/16],
 [-1/16,  3/16,  1/4 ]].
```

The diagonal reproduces the reference edge pressures.

Now inspect release of edge `02`, i.e. column two:

```text
02 -> pressure_01 derivative = 3/32,
02 -> pressure_12 derivative = 3/16.
```

Thus the strongest positive cross-edge response is

```text
02 -> 12.
```

This predicts the observed full-release cascade in the worked example:

```text
release 02
-> pressure on 12 rises
-> release 12
-> retain 01.
```

The cascade is therefore already visible in the local Hessian before performing the full finite edge release.

---

## 4. Mechanistic use

The first-order topology prediction can now have two layers:

```text
edge pressure p_e
-> which edge is selected to weaken first;

transfer matrix H_fe
-> which other edge is predicted to gain or lose release pressure next.
```

A prospective intervention can test both:

```text
1. measure / estimate the reference optimized phenotype;
2. predict first release edge e*;
3. predict signed pressure changes H_fe for every remaining edge;
4. experimentally weaken e*;
5. re-estimate phenotype and edge pressures;
6. compare observed pressure rerouting with the frozen transfer prediction.
```

This is stronger than testing only whether the final module partition matches.

---

## 5. Uncertainty propagation

For each bootstrap/posterior draw, PAYOFF can compute

```text
p_e^(b)
```

and

```text
H_fe^(b).
```

This allows support statements such as

```text
P(first edge=e*)
```

and

```text
P(H_fe>0).
```

A future empirical implementation should distinguish uncertainty in the first edge from uncertainty in the predicted cascade sign.

---

## 6. Claim boundary

The transfer matrix is exact for the declared quadratic coupling-loss model.

It does not imply that biological developmental or genetic couplings literally update according to this derivative. It predicts the **optimized fitness-geometry consequence** of changing a registered coupling coefficient.

Appropriate:

> Under the quadratic coupling model, weakening the F1-F3 edge is predicted to increase the marginal value of weakening F2-F3, providing a mechanistic conflict-rerouting explanation for the sequential module split.

Avoid:

> Removing one developmental interaction universally causes another interaction to weaken.
