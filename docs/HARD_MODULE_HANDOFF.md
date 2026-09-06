# Hard-module handoff — coarse architecture prediction before edgewise coupling is identified

This document defines the coarse partition lane complementary to `SCH_BITA_BALANCE_TOPOLOGY_HANDOFF.md`.

Use this lane when function-specific conflict geometry is available but the reference edgewise coupling graph is not yet empirically identified.

---

## 1. Required inputs

The executable interface is

```text
scripts/predict_hard_module_partition.py
```

with

```text
functions.csv
function_id,optimum,weight
```

and one scalar

```text
extra_module_cost = kappa.
```

Meanings:

```text
optimum
    function-specific preferred coordinate theta_i;

weight
    local quadratic fitness curvature a_i>0;

kappa
    added fitness-scale cost per extra independently tunable module.
```

The hard-module model assumes all functions inside one module share one exact coordinate, while different modules use independent coordinates.

---

## 2. SCH ownership and the same strict optimum gate

The required `theta_i` are function-specific optima.

SCH's default state-specific

```text
z_P*, z_G*, z_C*
```

must not automatically be inserted into this schema as different functions.

Valid lanes are:

1. SCH's context-stable component-optimum upgrade;
2. an equivalent independent experiment identifying function-specific optima;
3. an explicitly labeled scenario analysis.

Likewise, `weight=a_i` is a local fitness curvature, not a generic statistical precision weight.

---

## 3. Architecture-cost ownership

The scalar three-world programme often uses one total differentiated-architecture cost

```text
K.
```

The hard-module specialization uses

```text
K(P)=kappa(|P|-1).
```

This is an additional cost model.

Therefore a measured total `K` does **not** automatically identify `kappa` unless the biological architecture assay supports the per-extra-module decomposition.

Allowed lanes are:

```text
identified module cost
-> empirical hard-partition prediction;

frozen kappa scenarios
-> cost-sensitivity / theory prediction.
```

Do not silently set

```text
kappa=K/(n-1)
```

without a registered decomposition assumption.

---

## 4. PAYOFF output

For every candidate hard partition `P`, PAYOFF defines

```text
D_P*
= within-module conflict remaining after module-specific optimization;

R(P)
= fully shared conflict load - D_P*;

Phi(P)
= R(P)-kappa(|P|-1).
```

The CLI writes

```text
fixed_module_counts.csv
module_count_intervals.csv
summary.json.
```

`fixed_module_counts.csv` contains the exact best partition for each possible module count.

`module_count_intervals.csv` reports the exact cost range over which each module count lies on the penalized lower envelope.

`summary.json` reports the global optimum for the supplied `kappa`.

---

## 5. Why this lane is useful

The strict edgewise lane needs

```text
theta_i,a_i,c_e,k_e.
```

The hard-module lane needs only

```text
theta_i,a_i,kappa.
```

Thus the hard-module lane is useful when the biological question is already

> which functions should remain locked together versus receive independent coordinates?

but edge-specific residual integration remains unmeasured.

It gives a coarser prediction than edgewise topology and should be labeled accordingly.

---

## 6. Exact split receipt

For a proposed split of one module into daughter groups `A|B`, the recovered loss is

```text
G(A,B)
=
[A_A A_B/(A_A+A_B)](mu_A-mu_B)^2.
```

Therefore a local split pays iff

```text
G(A,B)>kappa.
```

This is the same weighted-conflict form as SCH, applied recursively to module centroids.

A strong experiment can therefore freeze a predicted split and test whether enabling one additional independently adjustable module improves common-scale fitness by the predicted amount.

---

## 7. Relation to the strict edgewise lane

```text
hard module
within-module coupling = effectively infinite
between-module coupling = zero

edgewise topology
retained couplings may remain finite
released couplings are manipulated edge by edge.
```

The hard-module optimum and finite-coupling topology are not expected to have identical numerical payoffs.

Agreement in grouping is useful corroboration. Disagreement can indicate that residual within-module flexibility materially changes architecture ranking.

---

## 8. Registered three-function example

Using

```text
theta=(0,1,3),
a=(1,1,1),
kappa=1,
```

PAYOFF predicts

```text
{F1,F2}|{F3}.
```

The fixed-module losses are

```text
W_1=14/3,
W_2=1/2,
W_3=0,
```

and exact module-cost phases are

```text
kappa<1/2
-> three modules;

1/2<kappa<25/6
-> {F1,F2}|{F3};

kappa>25/6
-> one shared module.
```

This is a synthetic theory fixture, not an empirical result.

---

## 9. Current claim ceiling

Correct status:

```text
HARD_MODULE_PARTITION_THEORY_READY
HARD_MODULE_DP_READY
HARD_MODULE_HANDOFF_SCHEMA_READY
FUNCTION_SPECIFIC_OPTIMA_REQUIRED
PER_EXTRA_MODULE_COST_NOT_YET_GENERALLY_IDENTIFIED.
```
