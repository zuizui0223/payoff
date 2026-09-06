# Hard module partition — exact between-module recovery and module-count thresholds

The edgewise model permits finite residual coupling inside a topology. This note studies the complementary **hard-module limit**:

- every function inside one module is forced to use one common coordinate;
- different modules may use independent coordinates.

This is the clean partition-level continuation of SCH's shared-coordinate geometry.

The model is not intended to replace finite-coupling topology. It provides an exact limiting architecture in which the value of creating modules can be written in closed form.

---

## 1. Setup

There are `n` functions with scalar preferred coordinates

```text
theta_i
```

and positive fitness curvatures

```text
a_i>0.
```

A module partition is

```text
P={M_1,...,M_k}
```

where the modules are non-empty, disjoint, and cover all functions.

Each module `M` receives one common coordinate `z_M`. The loss is

```text
D_P(z)
= sum_{M in P} sum_{i in M} a_i (z_M-theta_i)^2.
```

Define module weight and module optimum mean

```text
A_M = sum_{i in M} a_i,
mu_M = [sum_{i in M} a_i theta_i]/A_M.
```

Let total weight and the fully shared weighted mean be

```text
A = sum_i a_i,
mu = [sum_i a_i theta_i]/A.
```

---

## Theorem HMP1 — exact optimized loss of a hard module partition

For every module `M`, the unique optimal module coordinate is

```text
z_M*=mu_M.
```

Therefore

```text
D_P*
= sum_{M in P} L(M),
```

where

```text
L(M)
= sum_{i in M} a_i(theta_i-mu_M)^2.
```

### Proof

The objective separates by module. Each module minimizes a positive weighted quadratic in one scalar coordinate. Its unique minimizer is the weighted mean `mu_M`. Summing the minimized within-module losses gives the result. QED.

---

## Theorem HMP2 — modular recovery is exactly between-module disagreement

Let the fully shared one-module conflict load be

```text
L_all
= sum_i a_i(theta_i-mu)^2.
```

Define recovery of partition `P` relative to the fully shared architecture by

```text
R(P)=L_all-D_P*.
```

Then

```text
R(P)
= sum_{M in P} A_M(mu_M-mu)^2.
```

Equivalently,

```text
R(P)
= [1/A]
  sum_{M<N} A_M A_N (mu_M-mu_N)^2.
```

### Proof

Weighted ANOVA gives

```text
sum_i a_i(theta_i-mu)^2
=
sum_M sum_{i in M} a_i(theta_i-mu_M)^2
+
sum_M A_M(mu_M-mu)^2.
```

The first term is `D_P*`, so the second is `R(P)`.

Applying SCH's weighted pairwise-disagreement identity to the module means with weights `A_M` gives the pairwise form. QED.

### Interpretation

This is the module-level recursion of SCH:

```text
within-module disagreement
    remains as compromise loss;

between-module disagreement
    is exactly what modularization recovers.
```

No new fitness scale is introduced.

---

## Theorem HMP3 — exact value of splitting one module

Suppose a current module `C` is split into two non-empty groups

```text
C=A union B,
A intersect B=empty.
```

Let their weights and means be

```text
A_A, mu_A,
A_B, mu_B.
```

The reduction in optimized loss caused by this split is exactly

```text
G(A,B)
=
[A_A A_B/(A_A+A_B)](mu_A-mu_B)^2.
```

Equivalently,

```text
L(C)
= L(A)+L(B)+G(A,B).
```

### Proof

Apply the two-group weighted variance decomposition inside module `C`. QED.

### Interpretation

A proposed module split has a local receipt with exactly the same form as the original two-function SCH conflict load, except the two "functions" are now module centroids.

The theory is therefore recursive:

```text
function conflict
-> module conflict
-> super-module conflict.
```

---

## Corollary HMP3.1 — split-cost threshold

If creating one additional module costs a fixed amount

```text
kappa>0
```

on the same fitness scale, then splitting `C` into `A|B` improves static architecture payoff iff

```text
G(A,B)>kappa.
```

The local split-neutral surface is

```text
kappa=G(A,B).
```

This is a hard-module analogue of `R-K=0`.

---

## 2. Penalized global module partition

Let every additional module beyond the first cost `kappa`. The static partition payoff relative to full sharing is

```text
Phi(P)
= R(P)-kappa(|P|-1).
```

Since `L_all` is constant, maximizing `Phi(P)` is equivalent to minimizing

```text
J(P)
= D_P*+kappa |P|.
```

The additive constant `-kappa` does not change the optimizer.

---

## Theorem HMP4 — for scalar optima an optimal partition can be chosen contiguous

Sort functions so that

```text
theta_(1) <= ... <= theta_(n).
```

For the squared-loss hard-module model, there exists a globally optimal partition whose modules are contiguous blocks in this sorted order.

### Proof sketch

For any fixed set of module centers, squared-distance assignment in one dimension assigns each point to a nearest center, producing interval/Voronoi cells. Replacing each center by the weighted mean of its assigned points cannot increase loss. Therefore an optimum exists with contiguous sorted blocks.

### Prior-art boundary

This is the standard one-dimensional weighted k-means / segmentation structure. PAYOFF does not claim this computational fact as new.

---

## Theorem HMP5 — exact O(n^2) penalized dynamic programme

For sorted functions, define the within-block cost

```text
W(i,j)
= min_z sum_{t=i}^j a_t(z-theta_t)^2.
```

With prefix sums, `W(i,j)` is available in constant time:

```text
W(i,j)
= sum a_t theta_t^2
  - [sum a_t theta_t]^2/[sum a_t].
```

Let

```text
F(j)
```

be the minimum value of

```text
within loss + kappa * number of modules
```

for the first `j` sorted functions. Then

```text
F(0)=0,
```

and

```text
F(j)
= min_{0<=i<j}
  {F(i)+W(i+1,j)+kappa}.
```

Backtracking gives an exact globally optimal hard-module partition.

The recurrence takes `O(n^2)` time and `O(n)` state once segment costs are evaluated from prefix sums.

---

## 3. Optimal module count as architecture cost changes

Let

```text
W_k
```

be the minimum possible hard-partition within loss among all partitions with exactly `k` modules.

The best `k`-module penalized objective is

```text
J_k(kappa)
= W_k+kappa(k-1).
```

---

## Theorem HMP6 — optimal module count cannot increase with module cost

If

```text
kappa_2>kappa_1>=0,
```

and an optimal partition at `kappa_r` uses `m_r` modules, then one can choose optima such that

```text
m_2<=m_1.
```

### Proof

Optimality gives

```text
W_m1+kappa_1(m1-1)
<= W_m2+kappa_1(m2-1)
```

and

```text
W_m2+kappa_2(m2-1)
<= W_m1+kappa_2(m1-1).
```

Adding and simplifying yields

```text
(kappa_2-kappa_1)(m2-m1)<=0.
```

Since `kappa_2-kappa_1>0`, `m2<=m1`. QED.

### Interpretation

Increasing the cost of maintaining separate modules can collapse modules, but it cannot make the globally optimal hard architecture require more modules.

This is a module-count no-reentry theorem. It does **not** imply that the identity of optimal module boundaries is hierarchically nested as `kappa` changes.

---

## Theorem HMP7 — exact module-count support interval

For a candidate module count `k`, compare its line

```text
J_k(kappa)=W_k+kappa(k-1)
```

with every other count.

The count `k` is globally optimal on the interval

```text
lower_k
= max_{l>k} (W_k-W_l)/(l-k),
```

```text
upper_k
= min_{l<k} (W_l-W_k)/(k-l),
```

with absent lower/upper comparisons interpreted as `0`/`+infinity` respectively.

If

```text
lower_k<=upper_k,
```

then `k` lies on the lower envelope and is optimal for at least one non-negative module cost. Otherwise that module count is skipped entirely by the penalized optimum.

---

## 4. Registered three-function hard-partition example

Use

```text
theta=(0,1,3),
a=(1,1,1).
```

The exact minimum within losses are

```text
W_1=14/3,
W_2=1/2,
W_3=0.
```

The best two-module partition is

```text
{0,1}|{2}.
```

The module-count phase boundaries are

```text
kappa=1/2
```

and

```text
kappa=25/6.
```

Therefore

```text
0 <= kappa < 1/2
-> 3 modules
-> {0}|{1}|{2}

1/2 < kappa < 25/6
-> 2 modules
-> {0,1}|{2}

kappa > 25/6
-> 1 module
-> {0,1,2}.
```

At the upper boundary, splitting the fully shared module into `{0,1}|{2}` recovers

```text
G({0,1},{2})
= [2*1/3](3-1/2)^2
=25/6.
```

At the lower boundary, splitting `{0,1}` into singletons recovers

```text
G({0},{1})
=[1*1/2](1-0)^2
=1/2.
```

So the two global phase boundaries are exactly the two recursive SCH-style split receipts.

---

## 5. Relation to finite-coupling edgewise topology

This hard-partition model is a limiting architecture:

```text
within a module: exact shared coordinate;
between modules: complete release.
```

`EDGEWISE_MODULARIZATION.md` instead allows finite residual coupling and therefore predicts soft modules, release cascades, and topology-specific conflict transfer.

The two models answer different questions:

```text
hard partition
-> what module grouping is optimal if within-module sharing is exact?

edgewise finite coupling
-> which concrete connections should weaken from a measured reference graph?
```

They should not be numerically conflated.

---

## 6. Empirical handoff

The hard-partition lane needs only

```text
function-specific theta_i,
fitness curvature a_i,
per-extra-module cost kappa.
```

It does not require a reference coupling graph.

This makes it useful as a coarse architecture prediction when SCH can identify function-specific optima and the architecture assay can estimate a module-level cost but edge-specific coupling strengths remain unavailable.

The stricter identification warning remains:

```text
state-specific SCH optima
!= automatically pure/function-specific theta_i.
```

Use the hard-partition lane only when the function-specific optimum interpretation is independently justified.

---

## 7. Claim boundary

Weighted variance decomposition is standard mathematics. Optimal one-dimensional k-means/segmentation by dynamic programming is established prior art.

PAYOFF's candidate contribution is the biological estimand bridge:

> a hard module split recovers exactly the SCH-style weighted disagreement between the two daughter-module optima, allowing the same conflict scale to rank module partitions and compare each extra module with an explicit architecture cost.
