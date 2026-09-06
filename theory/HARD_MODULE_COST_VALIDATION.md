# Hard-module cost validation — identify on one architecture, predict another

`HARD_MODULE_COST_IDENTIFICATION.md` shows how direct worldlines identify the constant per-extra-module cost `kappa`.

The stronger use is prospective or held-out validation:

```text
fit kappa on one set of module architectures
-> freeze kappa
-> predict direct margins for different module architectures
-> compare with held-out worldlines.
```

This avoids using every observed architecture to both estimate and validate the cost model.

---

## 1. Fit set

For fit partitions `P_j`, use

```text
y_j
=R(P_j)-Delta_W(P_j)
=kappa(|P_j|-1)
```

and estimate `kappa` by the registered zero-intercept weighted fit.

Freeze

```text
kappa_hat.
```

No held-out direct margin is used at this stage.

---

## 2. Held-out prediction

For a held-out partition `Q`, SCH/hard-module geometry supplies

```text
R(Q).
```

The constant-cost model predicts

```text
Delta_hat_W(Q)
=R(Q)-kappa_hat(|Q|-1).
```

After the prediction is frozen, compare with the independently observed

```text
Delta_W(Q).
```

Define held-out residual

```text
delta_holdout(Q)
=Delta_W(Q)-Delta_hat_W(Q).
```

A nonzero residual should be audited as a model discrepancy, not absorbed by refitting `kappa` unless the analysis is explicitly moved back to an exploratory stage.

---

## 3. Registered three-function fixture

Use

```text
theta=(0,1,3),
a=(1,1,1).
```

### Fit architecture

For

```text
P_fit={0,1}|{2},
```

```text
R(P_fit)=25/6.
```

Suppose the direct worldline gap is

```text
Delta_W(P_fit)=19/6.
```

Then

```text
kappa_hat
=25/6-19/6
=1.
```

### Held-out architecture

For full separation

```text
Q={0}|{1}|{2},
```

```text
R(Q)=14/3
```

and the frozen model predicts

```text
Delta_hat_W(Q)
=14/3-2(1)
=8/3.
```

The registered synthetic held-out fixture sets

```text
Delta_W(Q)=8/3,
```

so the held-out residual is zero.

This fixture demonstrates the workflow only; it is not empirical support for the model.

---

## 4. Strong empirical use

A strong experiment can use different architecture manipulations for fit and validation:

```text
SCH
-> identify theta_i,a_i
-> compute R(P) for all preregistered partitions

architecture assay A
-> direct W_P*-W_S* for one simple split
-> identify kappa

architecture assay B
-> implement a different module count / partition
-> predict direct margin before observing outcome
-> held-out test.
```

Multiple held-out partitions are even stronger because they test both module count scaling and partition-specific recovery.

---

## 5. Interpretation of failure

If held-out residuals exclude the expected estimation uncertainty, possible failures include:

```text
constant per-extra-module cost is false;
module cost depends on partition identity;
hard within-module sharing is too strict;
function-specific theta_i or a_i are misidentified;
direct worldlines are on a different fitness scale;
new ecological channels appear after architecture change.
```

The residual does not tell which explanation is correct by itself.

---

## 6. Claim boundary

The validation design does not make the hard-module model true. It makes the model testable without circular reuse of the same direct architecture gap for both cost estimation and confirmation.
