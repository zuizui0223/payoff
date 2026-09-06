# Hard-module cost identification — direct worldlines identify `kappa`

The hard-module partition model uses one extra-module cost

```text
kappa
```

through

```text
K(P)=kappa(|P|-1).
```

`HARD_MODULE_HANDOFF.md` correctly warns that a generic total architecture cost `K` does not automatically identify `kappa`.

However, BALANCE's direct worldline route provides an identification strategy when one or more hard-module architectures can be constructed or assayed on the same fitness scale.

---

## 1. Direct architecture gap

Let

```text
W_S*
```

be optimized fully shared fitness and

```text
W_P*
```

be optimized fitness under hard partition `P`.

Define the direct worldline gap

```text
Delta_W(P)
=W_P*-W_S*.
```

SCH geometry plus the hard-module theorem predicts pre-cost recovery

```text
R(P).
```

Under the constant per-extra-module cost model,

```text
Delta_W(P)
=R(P)-kappa(|P|-1).
```

---

## Theorem HMCI1 — one nontrivial partition identifies `kappa`

For any partition with

```text
|P|>1,
```

```text
kappa_P
=
[R(P)-Delta_W(P)]/(|P|-1).
```

If the hard-module cost model is correct and all quantities share one fitness scale, then

```text
kappa_P=kappa.
```

### Interpretation

The per-module cost is not inferred from topology geometry alone. It is the amount of predicted conflict recovery that fails to appear in the direct optimized worldline gap, divided by the number of added independently tunable modules.

---

## Theorem HMCI2 — multiple partitions overidentify the constant-cost model

Suppose direct worldline gaps are measured for partitions

```text
P_1,...,P_m
```

with at least two distinct nonzero values of

```text
q_j=|P_j|-1.
```

Define

```text
y_j=R(P_j)-Delta_W(P_j).
```

The constant per-module model predicts

```text
y_j=kappa q_j.
```

Thus every partition-specific receipt

```text
kappa_j=y_j/q_j
```

should agree up to estimation uncertainty.

A systematic dependence of `kappa_j` on module count or partition identity falsifies the constant-`kappa` cost specialization even if individual partitions remain compatible with some positive architecture cost.

---

## Corollary HMCI2.1 — weighted least-squares estimate

Given positive analysis weights `w_j`, the zero-intercept weighted least-squares estimate is

```text
kappa_hat
=
[sum_j w_j q_j y_j]
/
[sum_j w_j q_j^2].
```

Predicted direct gaps are

```text
Delta_hat_j
=R(P_j)-kappa_hat q_j.
```

The residual

```text
delta_j
=Delta_W(P_j)-Delta_hat_j
```

is a hard-module bridge residual.

Do not average a systematic residual away. Audit:

1. fitness-scale mismatch;
2. partition implementation mismatch;
3. omitted architecture costs or benefits;
4. non-additive cost by module count;
5. partition-specific ecological channels;
6. only then, failure of the hard-module approximation itself.

---

## 2. Connection to the three-world programme

The identification chain is

```text
SCH
-> theta_i,a_i
-> predict R(P)

BALANCE direct worldline assay
-> observe Delta_W(P)

PAYOFF hard-module identification
-> infer kappa_P
-> test constant-kappa restriction

BITA / architecture-cost assay
-> independently measure architecture cost when possible
-> compare with inferred kappa(|P|-1).
```

This creates an overidentified bridge rather than defining architecture cost solely from the theory.

---

## 3. Registered three-function example

For

```text
theta=(0,1,3), a=(1,1,1),
P={0,1}|{2},
```

hard-module recovery is

```text
R(P)=25/6.
```

If a matched direct worldline experiment observed

```text
Delta_W(P)=19/6,
```

then

```text
kappa
=25/6-19/6
=1.
```

That inferred cost predicts the hard-module optimum

```text
{0,1}|{2}
```

because

```text
1/2<1<25/6.
```

A second direct assay of the fully separated three-module architecture would then be an out-of-sample cost-model check rather than another parameter fit.

---

## 4. Claim boundary

This identification is conditional on the declared hard-module architecture and additive constant cost per extra module.

Appropriate claim:

> Given independently reconstructed partition recovery and a matched direct worldline gap, the declared constant per-module cost is algebraically identified and can be checked across additional partitions.

Avoid:

> Every biological module has one universal fixed cost.
