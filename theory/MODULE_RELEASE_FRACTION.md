# Module release fraction — hard partitions preserve the exact `R=sL` bridge

BITA's two-function quadratic bridge uses

```text
R=sL,
```

where `L` is fully shared conflict load and `s` is the recoverable fraction under the declared differentiated architecture.

The hard-module partition model gives an exact many-function interpretation of the same form.

---

## 1. Definition

Let

```text
L
```

be the fully shared one-coordinate conflict load for all functions.

For hard partition

```text
P,
```

let

```text
D_P*
```

be the optimized within-module residual conflict and

```text
R(P)=L-D_P*.
```

For `L>0`, define

```text
s_P
=R(P)/L
=1-D_P*/L.
```

Then trivially but exactly

```text
R(P)=s_P L.
```

The important point is that `s_P` has a concrete variance-decomposition meaning rather than being an arbitrary fitted scale factor.

---

## Theorem MRF1 — module release fraction is the between-conflict fraction

From `HARD_MODULE_PARTITION.md`,

```text
R(P)
=sum_M A_M(mu_M-mu)^2.
```

Therefore

```text
s_P
=
[sum_M A_M(mu_M-mu)^2]
/
[sum_i a_i(theta_i-mu)^2].
```

Equivalently,

```text
s_P
=
[sum_{M<N} A_M A_N(mu_M-mu_N)^2]
/
[sum_{i<j} a_i a_j(theta_i-theta_j)^2].
```

The common total-weight denominator in the two pairwise-disagreement identities cancels.

Thus:

```text
s_P
= fraction of total weighted disagreement lying between modules;

1-s_P
= fraction remaining within modules.
```

---

## Corollary MRF1.1 — exact hard-partition architecture gap

With any hard-partition architecture cost

```text
K(P),
```

the static architecture gap relative to full sharing is

```text
Phi(P)
=s_P L-K(P).
```

For the per-extra-module specialization

```text
K(P)=kappa(|P|-1),
```

```text
Phi(P)
=s_P L-kappa(|P|-1).
```

So the original three-world algebra survives unchanged after replacing one binary differentiated state by a many-function module partition.

---

## 2. Endpoints

For the one-module fully shared partition,

```text
D_P*=L,
R=0,
s_P=0.
```

For the all-singleton fully differentiated partition,

```text
D_P*=0,
R=L,
s_P=1.
```

Intermediate hard partitions satisfy

```text
0<s_P<1
```

whenever they recover some but not all conflict.

Thus module architecture gives a literal path between the SCH shared endpoint and the fully differentiated BITA endpoint.

---

## 3. Registered three-function example

For

```text
theta=(0,1,3),
a=(1,1,1),
```

fully shared conflict is

```text
L=14/3.
```

For

```text
P={0,1}|{2},
```

residual within-module conflict is

```text
D_P*=1/2.
```

Therefore

```text
R(P)
=14/3-1/2
=25/6,
```

and

```text
s_P
=(25/6)/(14/3)
=25/28.
```

The residual conflict fraction is

```text
1-s_P=3/28.
```

So this partition releases about 89.3% of the original shared conflict while retaining about 10.7% inside module `{0,1}`.

With `kappa=1`,

```text
K(P)=1
```

and

```text
Phi(P)
=s_P L-K
=25/6-1
=19/6>0.
```

The outer module split is therefore BITA-favored, while `RECURSIVE_MODULE_BALANCE.md` shows the remaining `{0}|{1}` split is still locally inside BALANCE because its own conflict `1/2` is below the next module cost `1`.

---

## 4. Relation to empirical `s`

The module release fraction is architecture-specific:

```text
s_P
```

depends on the declared partition.

It should not be confused with an empirically identified two-axis separation ratio unless the models and scales are explicitly matched.

What is shared is the architecture logic:

```text
fully shared conflict L
-> architecture recovers fraction s
-> recovered value R=sL
-> subtract architecture cost K.
```

The hard-module model supplies one exact many-function construction of such an `s`.

---

## 5. Claim boundary

The identity `R=sL` follows from the definition `s=R/L`. The nontrivial content here is the exact interpretation

```text
s_P=between-module conflict / total conflict
```

under the hard-partition weighted quadratic model.

Appropriate claim:

> In the declared hard-module architecture, BITA's recovery fraction is exactly the weighted fraction of shared conflict that lies between module centroids rather than within modules.
