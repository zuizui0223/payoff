# Topology decision robustness — why the first constrained edge can be more stable than the final module partition

The uncertainty ensemble shows that the first predicted release edge can have stronger support than the final global topology.

This note gives a deterministic reason why that can happen.

---

## 1. First-edge decision

At a reference architecture define each edge's marginal net-release score

```text
m_e
=(x_i^*-x_j^*)^2-k_e.
```

Let

```text
e*
```

be the unique largest score, with

```text
m*=m_e*>0,
```

and let

```text
m_2
```

be the second-largest score.

The registered greedy rule chooses `e*` as the first release edge.

---

## Theorem R1 — exact sufficient perturbation radius for first-edge identity

Suppose each edge score is perturbed independently but uniformly bounded:

```text
|m_tilde_e-m_e| <= epsilon.
```

Then `e*` remains positive and remains the unique largest score whenever

```text
epsilon
< min[
    m*,
    (m*-m_2)/2
  ].
```

### Proof

Positivity of the original leading edge is preserved if

```text
m_tilde_e*
>=m*-epsilon
>0,
```

which requires

```text
epsilon<m*.
```

For every competitor `j`,

```text
m_tilde_e*
>=m*-epsilon
```

and

```text
m_tilde_j
<=m_j+epsilon
<=m_2+epsilon.
```

Therefore `e*` remains strictly above every competitor when

```text
m*-epsilon>m_2+epsilon,
```

or

```text
epsilon<(m*-m_2)/2.
```

Both conditions together give the stated radius. QED.

Define

```text
rho_first
=min[m*,(m*-m_2)/2].
```

This is a score-space robustness receipt for the first edge decision.

---

## 2. Global best topology

Let vertex topology `S*` have highest intrinsic payoff

```text
b_1
```

and runner-up payoff

```text
b_2<b_1.
```

Define the global topology reserve

```text
rho_global=b_1-b_2.
```

---

## Theorem R2 — uniform payoff perturbation radius for the global topology identity

Suppose every topology payoff is perturbed by at most

```text
epsilon.
```

Then `S*` remains strictly globally best whenever

```text
epsilon<rho_global/2.
```

### Proof

The worst case moves the best payoff down by `epsilon` and the runner-up up by `epsilon`.

The ordering therefore remains strict if

```text
b_1-epsilon>b_2+epsilon,
```

which is equivalent to

```text
epsilon<(b_1-b_2)/2.
```

QED.

Define

```text
rho_best-uniform=rho_global/2.
```

---

## 3. Three-function worked example

At

```text
theta=(0,1,3),
k=0.4,
```

the reference edge margins are

```text
m_01=-27/80,
m_02= 13/80,
m_12=-3/20.
```

Thus

```text
m*=13/80,
m_2=-3/20,
m*-m_2=5/16.
```

The first-edge perturbation radius is

```text
rho_first
=min(13/80,5/32)
=5/32
=0.15625.
```

The global best topology is

```text
011={F1,F2}|{F3}
```

and its runner-up is full release `111`, with global reserve

```text
rho_global=1/15.
```

Hence the uniform global-topology perturbation radius is

```text
rho_best-uniform
=1/30
~=0.0333333.
```

Under these registered score perturbation models, the first-edge identity has a substantially larger deterministic stability radius than the final topology identity.

This is consistent with the five-draw ensemble fixture:

```text
first edge F1-F3: support 1.0
best topology 011: support 0.8.
```

---

## 4. Do not compare unlike perturbation scales blindly

`rho_first` is measured on an edge marginal-score scale:

```text
fitness change per unit edge decoupling.
```

`rho_global/2` is measured on a whole-topology payoff scale.

They are numerically directly comparable only when edge decoupling is dimensionless or otherwise normalized onto a common declared step scale, as in the registered unit-coupling worked example.

In empirical applications the main use is within-level robustness:

```text
is the first-edge decision far from its own ranking/sign boundary?
```

and

```text
is the final topology far from the runner-up payoff boundary?
```

rather than interpreting their raw numerical ratio as a universal biological quantity.

---

## 5. Connection to uncertainty ensembles

Bootstrap/posterior support is a finite-sample propagation of the full nonlinear input uncertainty.

The deterministic radii above are complementary local certificates.

A useful reporting combination is

```text
first-edge support
+ rho_first

best-topology support
+ rho_global

local vertex reserve rho_local.
```

These three pairs answer:

```text
How stable is the initial mechanism prediction?
How stable is the global endpoint ranking?
How stable is the endpoint once formed against local edge changes?
```

---

## 6. Claim boundary

The radii are sufficient guarantees under bounded additive perturbations of the declared decision scores. They are not Bayesian posterior probabilities and do not replace the ensemble calculation.

Appropriate:

> The first-edge decision has a larger registered score-space perturbation radius than the final topology ranking, consistent with stronger ensemble support for the initial conflict-release edge.

Avoid:

> The first edge is universally five times more certain than the final topology.
