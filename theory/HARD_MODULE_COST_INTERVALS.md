# Hard-module cost intervals — preserve uncertainty across the cost bridge

Point estimates are insufficient when SCH conflict geometry and BALANCE direct worldlines are reported with uncertainty intervals.

This note gives an interval version of the hard-module cost bridge.

---

## 1. Partition-specific cost interval

For partition `P_j`, suppose

```text
R_j in [R_j^-,R_j^+]
```

and direct matched worldline gap

```text
Delta_j in [Delta_j^-,Delta_j^+].
```

Let

```text
q_j=|P_j|-1>0.
```

Under

```text
Delta_j=R_j-kappa q_j,
```

the implied cost interval is

```text
kappa_j
in
[(R_j^- - Delta_j^+)/q_j,
 (R_j^+ - Delta_j^-)/q_j].
```

If architecture cost is constrained non-negative, intersect this interval with `[0,infinity)`.

The formula follows because `kappa` increases with recovery and decreases with direct margin.

---

## Theorem HMCI-I1 — interval intersection is a compatibility test

For multiple partitions, define their implied intervals

```text
K_j=[kappa_j^-,kappa_j^+].
```

A common constant `kappa` is interval-compatible iff

```text
intersection_j K_j
```

is non-empty.

Equivalently,

```text
max_j kappa_j^-
<=
min_j kappa_j^+.
```

If the inequality fails, no single non-negative per-extra-module cost is simultaneously compatible with all supplied partition intervals.

This is an interval-level falsification of the constant-cost specialization, conditional on the supplied uncertainty bounds and common fitness scale.

---

## 2. Held-out prediction interval

Suppose fit partitions identify a common cost interval

```text
kappa in [kappa^-,kappa^+].
```

For held-out partition `Q` with

```text
R_Q in [R_Q^-,R_Q^+]
```

and

```text
q_Q=|Q|-1,
```

the frozen prediction is

```text
Delta_hat_Q
in
[R_Q^- - q_Q kappa^+,
 R_Q^+ - q_Q kappa^-].
```

Compare this predicted interval with the independently observed held-out direct-margin interval.

If they do not overlap, the held-out architecture is incompatible with the fitted hard-module cost model at the declared interval level.

---

## 3. Registered numerical example

Suppose two fit architectures imply

```text
K_1=[0.70,1.30]
K_2=[0.85,1.15].
```

Then the common interval is

```text
[0.85,1.15].
```

For a three-module held-out architecture with

```text
R_Q in [4.5,4.8],
q_Q=2,
```

the direct-margin prediction is

```text
[4.5-2(1.15), 4.8-2(0.85)]
=[2.2,3.1].
```

Any held-out confidence interval entirely above `3.1` or below `2.2` would be disjoint from the prediction.

---

## 4. Why interval compatibility is not posterior probability

The intersection rule is set-based. It does not assign probabilities within the intervals and does not account for correlation among `R`, `Delta`, or partitions.

Use bootstrap/posterior draws when those joint distributions are available.

The interval lane is appropriate when the sister repositories export bounded receipts such as lower/upper confidence limits but not a joint sample.

---

## 5. Cross-repository use

The preferred order is

```text
SCH
-> interval for function-level geometry / partition recovery

BALANCE direct worldline
-> interval for Delta_W

PAYOFF
-> kappa interval per partition
-> common intersection
-> held-out predicted interval

BITA / architecture assay
-> independent cost evidence when available.
```

Do not collapse non-overlapping intervals into one averaged point estimate merely to preserve the bridge.

---

## 6. Claim boundary

This interval propagation is worst-case algebra over supplied bounds. It is not a replacement for a full joint uncertainty model.

Appropriate statement:

> The supplied partition intervals admit / do not admit a common constant per-module cost under the declared hard-module model.
