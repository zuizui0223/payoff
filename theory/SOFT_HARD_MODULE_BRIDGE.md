# Soft-hard module bridge — finite residual integration converges to the hard partition

PAYOFF now has two module descriptions:

```text
hard module partition
    all functions inside a module share exactly one coordinate;

edgewise / soft topology
    functions inside a module may retain finite residual coupling and therefore need not be identical.
```

This note connects them formally.

---

## 1. Fixed partition with internal coupling graphs

Let

```text
P={M_1,...,M_k}
```

be a fixed module partition.

For each non-singleton module `M`, choose a connected weighted internal graph with Laplacian

```text
L_M.
```

There are no coupling edges between different modules.

For common integration scale

```text
lambda>=0,
```

define soft loss

```text
D_lambda,P(x)
=
sum_i a_i(x_i-theta_i)^2
+lambda sum_M x_M^T L_M x_M.
```

The hard partition from `HARD_MODULE_PARTITION.md` imposes instead

```text
x_i=z_M
```

exactly for every `i in M`.

---

## Theorem SH1 — soft loss is bounded above by hard-module loss

Let

```text
D_soft*(lambda,P)
```

be the optimized finite-coupling loss and

```text
D_hard*(P)
```

be the optimized hard-partition loss.

Then for every finite `lambda>=0`,

```text
D_soft*(lambda,P)
<= D_hard*(P).
```

### Proof

Every phenotype satisfying the hard equalities has zero internal coupling penalty, because every connected edge joins equal coordinates.

Therefore every hard-feasible phenotype is also feasible in the soft optimization with exactly the same base loss. The soft problem minimizes over a larger set, so its optimum cannot be worse. QED.

---

## Theorem SH2 — increasing internal integration monotonically approaches the hard partition

For fixed partition and internal graphs,

```text
D_soft*(lambda,P)
```

is nondecreasing in `lambda`.

If at least one module contains non-identical function-specific optima, the increase is strict for finite `lambda` in the corresponding connected block.

Moreover,

```text
lim_{lambda->infinity}
D_soft*(lambda,P)
=
D_hard*(P).
```

### Proof

Each block is the network-coupling model from `NETWORK_EXTENSION.md` restricted to one module.

Increasing a non-negative coupling penalty cannot reduce the optimized objective. In a connected module, the envelope derivative is

```text
x_M*^T L_M x_M*>=0,
```

with equality at finite `lambda` only when the optimized coordinates are constant. If the module optima differ, finite exact constancy would contradict the first-order condition.

As `lambda->infinity`, any nonzero within-module disagreement would incur unbounded penalty while a constant module phenotype has finite loss. Thus each module collapses onto its weighted mean, exactly the hard-partition optimum. Summing blocks gives the limit. QED.

---

## Corollary SH2.1 — hard recovery is a lower bound on soft recovery

Use the same fully shared conflict load

```text
L_all
```

as baseline and define

```text
R_soft(lambda,P)
=L_all-D_soft*(lambda,P),
```

```text
R_hard(P)
=L_all-D_hard*(P).
```

Then

```text
R_soft(lambda,P)
>=R_hard(P),
```

and

```text
R_soft(lambda,P)
->R_hard(P)
```

as internal coupling becomes arbitrarily strong.

At `lambda=0`, every coordinate is independent and

```text
D_soft*=0,
R_soft=L_all.
```

Thus for a fixed declared partition,

```text
L_all
>= R_soft(lambda,P)
>= R_hard(P).
```

---

## 2. Soft-flexibility reserve

Define

```text
F_soft(P,lambda)
=
D_hard*(P)-D_soft*(lambda,P)
>=0.
```

This is the extra conflict loss avoided because retained module members are allowed finite relative movement rather than exact equality.

It is not a new architecture benefit relative to full sharing; it is the difference between two within-module integration assumptions for the same grouping.

`F_soft` decreases to zero as `lambda` increases.

---

## 3. Registered three-function example

For

```text
theta=(0,1,3),
a=(1,1,1),
P={0,1}|{2},
```

the hard module loss is

```text
D_hard*=1/2.
```

Keep only edge `(0,1)` with finite coupling `lambda=1`; function `2` is independent.

The soft optimized phenotype is

```text
x=(1/3,2/3,3),
```

with

```text
D_soft*=1/3.
```

Hence

```text
F_soft=1/2-1/3=1/6.
```

The functions belong to the same module in both descriptions, but finite within-module flexibility recovers an additional `1/6` of the hard residual conflict.

As the retained `(0,1)` coupling tends to infinity,

```text
x_0,x_1 -> 1/2
```

and the soft loss tends to `1/2`.

---

## 4. Biological interpretation

The hard model asks:

> If functions in one module are effectively locked to one coordinate, which grouping pays?

The soft model asks:

> Given a specific residual integration graph, how much within-module relative movement remains worthwhile?

Therefore a hard-module prediction can be used before edge-specific coupling is known, while the edgewise lane refines it once residual integration is measurable.

A hard split not paying does **not** imply that all within-module functions should be phenotypically identical. Finite internal flexibility can still have positive value without creating a separate module.

---

## 5. Claim boundary

This bridge follows directly from nested feasible sets and the network monotonicity theorem. It is not a claim that biological modules literally have infinite internal coupling.

Appropriate interpretation:

> The hard partition is the strong-within-module integration endpoint of the finite-coupling block model, and therefore provides a conservative lower bound on pre-cost recovery for the same grouping.
