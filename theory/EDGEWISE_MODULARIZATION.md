# Edgewise modularization — marginal release pressure and discrete topology from continuous couplings

`NETWORK_EXTENSION.md` varies one global integration strength `lambda`. Real modular architectures can weaken some functional couplings while retaining others.

This note gives each coupling edge its own strength and derives an exact edge-level selection rule.

The result provides a bridge from continuous coupling strengths to discrete modular topology.

---

## 1. Edgewise coupling model

Let there be `n` function-specific coordinates

```text
x in R^n
```

with optima `theta` and positive diagonal weighting matrix

```text
A=diag(a_1,...,a_n), a_i>0.
```

Choose an oriented incidence matrix

```text
B
```

for a candidate functional coupling graph. Row `b_e^T` corresponds to edge `e=(i,j)` and satisfies

```text
b_e^T x=x_i-x_j
```

up to orientation sign.

Let each edge have nonnegative coupling strength

```text
c_e>=0.
```

Write

```text
C=diag(c_e).
```

The phenotype loss is

```text
D(x;c)
=(x-theta)^T A(x-theta)
+x^T B^T C B x
```

or equivalently

```text
D(x;c)
=(x-theta)^T A(x-theta)
+sum_e c_e(b_e^T x)^2.
```

Define

```text
M(c)=A+B^T C B.
```

Since `A` is positive definite,

```text
M(c)>0
```

for every nonnegative coupling vector.

The unique optimized phenotype is

```text
x*(c)=M(c)^(-1)A theta.
```

---

## Theorem EWM1 — exact marginal conflict pressure on every coupling edge

Let

```text
z_e=b_e^T x*(c)=x_i*-x_j*.
```

Then

```text
partial D*(c)/partial c_e
=z_e^2.
```

### Proof

The optimized loss is

```text
D*(c)=min_x D(x;c).
```

By the envelope theorem, differentiating the objective with respect to `c_e` at the optimum holds `x*` fixed:

```text
partial D*/partial c_e
=(b_e^T x*)^2.
```

QED.

### Interpretation

The squared optimized disagreement carried by an edge is its exact marginal fitness penalty per additional unit of coupling.

Equivalently, if an architecture weakens edge `e` by a small amount `dd_e`, the first-order recovered loss is

```text
z_e^2 dd_e.
```

This turns the abstract idea of a "constraining edge" into a directly computed marginal quantity.

---

## 2. Concavity of optimized loss in coupling strengths

Differentiate the optimum condition

```text
M x*=A theta
```

with respect to edge coupling `c_f`:

```text
partial x*/partial c_f
=-M^(-1)b_f(b_f^T x*).
```

Using `z_e=b_e^T x*`,

```text
partial^2 D*/partial c_e partial c_f
=-2 z_e z_f b_e^T M^(-1)b_f.
```

In matrix form,

```text
H_c(D*)
=-2 diag(z) B M^(-1) B^T diag(z).
```

---

## Theorem EWM2 — optimized loss is concave in the coupling vector

For every coupling state,

```text
H_c(D*) <= 0
```

in the positive-semidefinite ordering.

Thus

```text
D*(c)
```

is concave in edge coupling strengths.

### Proof

`M^(-1)` is positive definite. Therefore

```text
diag(z) B M^(-1) B^T diag(z)
```

is positive semidefinite. Multiplication by `-2` makes the Hessian negative semidefinite. QED.

### Alternative proof

For fixed phenotype `x`, the objective is affine in `c`:

```text
D(x;c)=base(x)+sum_e c_e q_e(x).
```

The pointwise infimum over `x` of affine functions of `c` is concave.

---

## 3. Decoupling coordinates and increasing returns

Choose a reference architecture with edge couplings

```text
c^0_e>0.
```

Let

```text
d_e in [0,c^0_e]
```

be the amount of decoupling on edge `e`, so

```text
c_e=c^0_e-d_e.
```

Define recovery relative to the reference architecture:

```text
R(d)
=D*(c^0)-D*(c^0-d).
```

Then

```text
partial R/partial d_e
=z_e(d)^2.
```

Its Hessian is

```text
H_d(R)
=2 diag(z) B M^(-1) B^T diag(z)
>=0.
```

---

## Theorem EWM3 — recovery from edgewise decoupling is convex

`R(d)` is convex over the feasible decoupling box.

Along any one-edge direction,

```text
partial^2 R/partial d_e^2
=2 z_e^2 b_e^T M^(-1)b_e
>=0.
```

It is strictly positive whenever the edge currently carries nonzero optimized disagreement.

### Interpretation

Decoupling has increasing returns in the declared quadratic network model.

As an edge is released, the functions it connects can diverge more, which increases the marginal recovery available from releasing that edge further.

This is a mechanistic positive-feedback route from weak decoupling to sharper modular separation.

---

## 4. Architecture cost and the edge marginality rule

Let architecture cost for decoupling vector `d` be

```text
K(d).
```

The net architecture gain relative to the reference is

```text
Phi(d)=R(d)-K(d).
```

For an interior edge strength,

```text
partial Phi/partial d_e
=z_e^2-partial K/partial d_e.
```

---

## Theorem EWM4 — edgewise marginal balance condition

Any interior stationary architecture satisfies, for every partially decoupled edge,

```text
(x_i*-x_j*)^2
=
partial K/partial d_e.
```

Thus:

```text
marginal recovered conflict loss
=
marginal architecture cost
```

edge by edge.

For a constrained local maximum under standard differentiability conditions, the boundary KKT receipts are:

```text
d_e=0
-> z_e^2 <= partial K/partial d_e
   for a stable lower-bound edge;

0<d_e<c_e^0
-> z_e^2 = partial K/partial d_e;

d_e=c_e^0
-> z_e^2 >= partial K/partial d_e
   for a stable fully released edge.
```

These inequalities are necessary local conditions; global sufficiency requires additional curvature assumptions.

---

## 5. Linear edge costs produce a discrete architecture optimum

Suppose decoupling cost is additive and linear:

```text
K(d)=sum_e k_e d_e.
```

Then

```text
Phi(d)=R(d)-sum_e k_e d_e.
```

Because `R(d)` is convex and the cost term is affine,

```text
Phi(d)
```

is convex on the box

```text
0<=d_e<=c_e^0.
```

---

## Theorem EWM5 — bang-bang modularization under linear decoupling cost

There exists a global maximizer of `Phi(d)` at a vertex of the feasible box.

Therefore at least one globally optimal architecture satisfies, for every edge,

```text
d_e in {0,c_e^0}.
```

Equivalently, every edge in that optimal representative is either

```text
retained at its reference coupling
```

or

```text
released as far as allowed.
```

### Proof

A convex function on a compact polytope attains its maximum at at least one extreme point. The feasible box has vertices exactly at the binary edge-release vectors. QED.

### Interpretation

Discrete modular topology can emerge even though the model initially permits continuously variable coupling strengths.

The discreteness here is not imposed by mutation. It follows from:

```text
convex recovery from decoupling
+
linear architecture cost.
```

This is a model-specific bang-bang result, not a universal law of modularity.

---

## Corollary EWM5.1 — topology selection becomes a subset problem

Under linear edge costs, one may search the vertex architectures as subsets of released edges:

```text
S subseteq E.
```

For each subset:

```text
1. set d_e=c_e^0 for e in S,
2. set d_e=0 otherwise,
3. optimize phenotype x,
4. compute recovered loss R(S),
5. subtract sum_{e in S} k_e c_e^0.
```

The best subset is an intrinsic modular topology candidate.

Recovery is generally nonadditive across edges, so this is not reducible to ranking edges independently by their initial `z_e^2`.

---

## 6. When can partial edge strengths be globally selected?

If architecture cost is sufficiently convex, partial edge strengths can become globally stable.

Since

```text
H(Phi)=H(R)-H(K),
```

a sufficient condition for strict concavity of net architecture gain throughout a domain is

```text
H(K)-H(R) > 0.
```

Under that condition, the net architecture optimum is unique. Interior edges satisfy the exact marginality equation

```text
z_e^2=partial K/partial d_e.
```

Thus the contrast between discrete and graded modularity is controlled by curvature competition:

```text
convex biological recovery
versus
convex architecture cost.
```

---

## 7. Connection to the scalar continuous architecture theorem

The scalar recovery model in `CONTINUOUS_ARCHITECTURE_ESS.md` uses total recovered loss `r` as a one-dimensional architecture coordinate and a convex cost schedule `C(r)`.

The edgewise model explains where such a scalar path can come from:

```text
edge decoupling vector d
        |
        v
optimized phenotype x*(d)
        |
        v
total recovery R(d)
        |
        v
scalar architecture coordinate r=R(d)
```

But different edge-release vectors can have the same total recovery while carrying different topology and ecological consequences.

Therefore `r` is sufficient only along a declared one-dimensional release path or when topology-specific effects are negligible.

---

## 8. Handoff to the multi-architecture game

Each vertex topology `S` can be assigned intrinsic payoff

```text
b_S=R(S)-K(S)
```

relative to the reference architecture.

Those topology payoffs then enter `MULTI_ARCHITECTURE_GAME.md` with pairwise ecological feedback

```text
H_ST.
```

So topology evolution separates into:

```text
within-architecture phenotype optimization
-> edgewise recovery / topology payoff
-> population game among topologies.
```

This is the natural graph-level continuation of the PAYOFF transport principle.

---

# Prior-art and claim boundary

Envelope-theorem sensitivity, concavity of value functions, KKT conditions, and extreme-point properties of convex maximization are standard mathematics. Network modularity and evolving coupling are established biological ideas.

PAYOFF should claim only the architecture-specific derivation:

> In the declared quadratic coupling model, the marginal fitness penalty on a functional coupling edge is exactly the squared optimized trait disagreement across that edge; recovery is convex in edgewise decoupling, and linear decoupling costs therefore admit a globally optimal vertex architecture with fully retained or maximally released edges.

Do not claim that real biological modularity universally evolves by binary edge deletion or that all architecture-cost functions are linear.
