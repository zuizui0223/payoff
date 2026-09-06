# Multifunction module synthesis — from one shared trait to optimal module number

This document compresses the current many-function architecture layer into one chain.

The key advance over a binary shared/differentiated comparison is that PAYOFF can now generate an intermediate **module partition** directly from function-specific conflict geometry.

---

## 1. Fully shared conflict

For scalar function optima `theta_i` and positive curvatures `a_i`, the one-coordinate SCH load is

```text
L
=sum_i a_i(theta_i-mu)^2
```

with weighted mean

```text
mu=sum_i a_i theta_i / sum_i a_i.
```

This is the total conflict budget available for any architecture to recover under the declared quadratic model.

---

## 2. Hard partition as partial differentiation

For hard partition

```text
P={M_1,...,M_k},
```

each module receives one independently adjustable coordinate but functions inside a module still share that coordinate.

Optimized residual conflict is

```text
D_P*
=sum_M sum_{i in M} a_i(theta_i-mu_M)^2.
```

Recovery is

```text
R(P)=L-D_P*.
```

Weighted variance decomposition gives

```text
R(P)
=sum_M A_M(mu_M-mu)^2.
```

Therefore define

```text
s_P=R(P)/L.
```

Then exactly

```text
R(P)=s_P L.
```

and `s_P` is the fraction of total shared conflict lying between modules.

---

## 3. Costed module architecture

With one constant cost per extra independently adjustable module,

```text
K(P)=kappa(k-1).
```

The static architecture gap relative to full sharing is

```text
Phi(P)
=s_P L-kappa(k-1).
```

Thus the original SCH/BALANCE/BITA bridge survives in many-function form:

```text
conflict L
-> architecture-specific release fraction s_P
-> recovery s_P L
-> subtract module cost.
```

---

## 4. Every candidate split is a recursive three-world problem

For a proposed split

```text
C -> A|B,
```

the exact recovered conflict is

```text
L_node
=[A_A A_B/(A_A+A_B)](mu_A-mu_B)^2.
```

Hard separation has

```text
s_node=1,
```

so

```text
Phi_node=L_node-kappa.
```

Hence:

```text
L_node=0
-> no coarse conflict;

0<L_node<kappa
-> recursive BALANCE inside the retained module;

L_node>kappa
-> recursive BITA split.
```

A retained module therefore need not be conflict-free. It can be a local BALANCE state.

---

## 5. Global partition is solved independently of the local split story

For scalar optima, an optimal hard partition can be chosen as contiguous blocks after sorting `theta_i`.

The exact penalized optimum is obtained by

```text
F(j)
=min_{i<j}{F(i)+W(i+1,j)+kappa},
```

where `W` is within-block weighted squared loss.

Thus the global hard-module architecture is computable exactly without enumerating all set partitions.

The optimal module count is nonincreasing as `kappa` increases.

This global DP result must be kept distinct from any historical split sequence.

---

## 6. Architecture accessibility is a separate quantity

For target partition `P*`, define

```text
kappa_access(P*)
=max over compatible binary split trees
 min split gain on the tree.
```

Then

```text
kappa<kappa_access
```

means at least one all-uphill one-module-at-a-time route exists.

A greedy largest-current-gain split can still miss that route.

Therefore:

```text
global optimum
!= greedy endpoint
!= existence of any monotone split path.
```

This is the hard-module analogue of the edgewise local/global accessibility distinction.

---

## 7. Soft modules refine the hard prediction

If a predicted module retains finite internal coupling rather than exact equality, its optimized loss satisfies

```text
D_soft*(lambda,P)
<=D_hard*(P),
```

and approaches the hard loss as within-module integration becomes arbitrarily strong.

Therefore

```text
R_soft(lambda,P)
>=R_hard(P).
```

The hard model is the strong-within-module integration endpoint; edgewise finite coupling refines it when residual integration is measured.

---

## 8. Module cost is empirically identifiable from direct worldlines

For any measured hard partition `P`, BALANCE's direct worldline gap gives

```text
Delta_W(P)
=W_P*-W_S*.
```

The hard-module model predicts

```text
Delta_W(P)
=R(P)-kappa(|P|-1).
```

Thus

```text
kappa_P
=[R(P)-Delta_W(P)]/(|P|-1).
```

Multiple partitions overidentify the constant-cost model.

Stronger still:

```text
fit kappa on one architecture
-> freeze it
-> predict a different direct architecture margin.
```

This provides a non-circular falsification route.

---

## 9. Uncertainty lanes

PAYOFF now supports three levels:

```text
point receipts
-> kappa_hat and exact partition;

bounded intervals
-> partition-specific kappa intervals
-> common-intersection test
-> held-out prediction interval;

bootstrap/posterior draws
-> propagate through architecture prediction when a joint sample is available.
```

No interval or bootstrap procedure can rescue unidentified function-specific optima or an unjustified module-cost decomposition.

---

## 10. Registered three-function synthesis

For

```text
theta=(0,1,3),
a=(1,1,1),
```

```text
L=14/3.
```

At

```text
kappa=1,
```

the hard optimum is

```text
P*={0,1}|{2}.
```

Receipts:

```text
D_P*=1/2,
R=25/6,
s_P=25/28,
K=1,
Phi=19/6.
```

The outer split has

```text
L_node=25/6>1
```

and pays.

The retained `{0,1}` internal split has

```text
L_node=1/2<1
```

and remains in recursive BALANCE with reserve

```text
rho_node=1/2.
```

The global target has split-accessibility threshold

```text
kappa_access=25/6,
```

so `kappa=1` admits a monotone split route.

If a direct two-module worldline gives

```text
Delta_W=19/6,
```

then it identifies

```text
kappa=1.
```

That frozen cost predicts the held-out full-separation margin

```text
14/3-2=8/3.
```

This synthetic example therefore closes the chain

```text
function optima
-> conflict
-> module recovery
-> cost identification
-> global module prediction
-> accessibility
-> held-out architecture margin.
```

---

## 11. Empirical ladder

The practical sequence is now:

```text
coarse lane
SCH theta_i,a_i
+ module-level cost/worldline
-> hard module partition

strict lane
+ measured coupling graph c_e
+ edge release costs k_e
-> soft edgewise topology
-> conflict-transfer cascade

population lane
+ symmetric architecture interactions
-> canonical phi,eta
-> invasion/fixation/occupancy

space/time lane
-> spatial spectral and temporal Floquet transport.
```

---

## 12. Main interpretation

The many-function result is no longer merely

> more conflict favors more modularity.

It is:

> **the amount of shared conflict lying between prospective module centroids determines the recoverable value of that partition; explicit module costs determine how many independent coordinates pay; and accessibility determines whether the global architecture can be reached by locally favorable module additions.**

All claims remain conditional on the declared quadratic shared-coordinate and hard-module assumptions.
