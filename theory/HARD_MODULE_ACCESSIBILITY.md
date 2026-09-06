# Hard-module accessibility — global optimum, greedy splitting, and true split valleys

`HARD_MODULE_PARTITION.md` gives the globally optimal hard partition for a fixed per-extra-module cost. That does not by itself say whether the optimum can be reached by a sequence of individually favorable module-splitting mutations.

This note separates three objects:

```text
global partition optimum,
greedy split path,
existence of any all-uphill split path.
```

They are not equivalent.

---

## 1. Split-only architecture path

Start from one fully shared hard module.

A mutation may split one current module into two daughter modules. If the split gain is

```text
G(A,B)
```

and the extra module costs

```text
kappa,
```

then that one mutation is uphill iff

```text
G(A,B)>kappa.
```

For a declared target partition

```text
P*={M_1,...,M_k}
```

with contiguous modules in sorted-optimum order, there are generally many compatible binary split trees that end at the same target.

---

## Definition — split accessibility threshold

For a compatible binary split tree `T`, let

```text
b(T)=min_{v in T} G_v
```

be its weakest internal split gain.

Define

```text
kappa_access(P*)
= max_T b(T).
```

Then:

```text
kappa < kappa_access
-> at least one target-compatible binary split sequence has every step strictly uphill;

kappa > kappa_access
-> every target-compatible split tree contains at least one downhill split.
```

At equality, the best route contains a neutral split.

---

## Theorem HMA1 — exact maximin dynamic programme

Order the target modules by scalar optimum. For any consecutive target-module interval

```text
[i,j)
```

let

```text
B(i,j)
```

be the best achievable weakest split gain for refining the union of those target modules down to the declared target blocks.

Base case:

```text
B(i,i+1)=+infinity.
```

For a longer interval,

```text
B(i,j)
=
max_{i<q<j}
min{
  G(M_i...M_{q-1}, M_q...M_{j-1}),
  B(i,q),
  B(q,j)
}.
```

Then

```text
kappa_access(P*)=B(0,k).
```

### Proof

Every compatible binary tree has one root cut `q`. Its weakest split is the minimum of the root split gain and the weakest split in each daughter subtree. Choosing the root cut that maximizes that minimum gives the recurrence. Optimal substructure applies recursively. QED.

The algorithm uses `O(k^2)` interval states and at most `O(k)` cuts per state, so the direct implementation is `O(k^3)` for a target with `k` final modules.

---

## 2. Greedy splitting is a different object

A natural heuristic repeatedly chooses the currently available split with the largest positive

```text
G-kappa.
```

Every accepted step is guaranteed uphill, but the largest current gain need not lie on a route to the global partition optimum.

Therefore:

```text
greedy endpoint != global optimum
```

can occur even when the global optimum is fully accessible through another all-uphill sequence.

---

## Registered four-function counterexample

Take

```text
theta=(0,1,2,3),
a=(2,1,1,2),
kappa=3/4.
```

The fully shared loss is

```text
L_all=19/2.
```

### Greedy first split

The largest initial split is

```text
{0,1}|{2,3}
```

with gain

```text
49/6.
```

Each resulting pair has remaining split gain

```text
2/3<3/4,
```

so greedy splitting stops at

```text
P_greedy={0,1}|{2,3}.
```

Its residual within loss is

```text
4/3
```

and its penalized residual objective is

```text
4/3+3/4=25/12.
```

### Global optimum

The exact dynamic programme instead selects

```text
P*={0}|{1,2}|{3}.
```

Its within loss is

```text
1/2
```

and its two extra modules cost

```text
3/2.
```

Thus its penalized residual objective is

```text
1/2+3/2=2,
```

which is lower than `25/12` by

```text
1/12.
```

### But the global optimum is not valley-blocked

One compatible route is

```text
{0,1,2,3}
-> {0}|{1,2,3}
-> {0}|{1,2}|{3}.
```

The two split gains are

```text
27/4
```

and

```text
9/4.
```

Therefore

```text
kappa_access(P*)=9/4.
```

Since

```text
3/4<9/4,
```

both steps are strongly uphill.

So the greedy failure is a **choice-of-path failure**, not a fitness-valley barrier.

---

## 3. Accessibility and optimality are separate estimands

A target can be:

```text
globally optimal and split-accessible;

globally optimal but split-inaccessible at the declared kappa;

split-accessible but not globally optimal;

neither.
```

For example, in the registered three-function system

```text
theta=(0,1,3), a=(1,1,1),
```

the fully separated target has best split-tree threshold

```text
kappa_access=2.
```

But it is the global penalized optimum only for

```text
kappa<1/2.
```

Thus for

```text
1/2<kappa<2
```

full separation can be reached by a sequence of favorable splits even though another partition has higher final payoff.

This distinction matters if module formation is path dependent or reversibility is limited.

---

## 4. Relation to topology accessibility

The edgewise topology layer already separates

```text
global topology value
```

from

```text
single-edge mutational accessibility.
```

The hard-module maximin threshold is the coarse partition analogue.

The two should not be numerically equated:

```text
edgewise path
changes individual coupling edges;

hard-module path
adds independently tunable module coordinates by binary splits.
```

---

## 5. Empirical interpretation

If module creation is approximately one-at-a-time, a strong prediction should report both

```text
global optimal partition
```

and

```text
kappa_access(global optimum).
```

Then a measured or scenario module cost can distinguish:

```text
kappa < kappa_access
-> at least one monotone split path exists;

kappa > kappa_access
-> reaching the global target requires a neutral/downhill split, a larger mutation, a cost change, or a different architecture mechanism.
```

Greedy split simulations alone cannot establish the second conclusion.

---

## 6. Claim boundary

The maximin tree recursion is a dynamic-programming construction over the declared binary refinement process. PAYOFF should claim the architecture-specific accessibility diagnostic, not a universal theorem about the historical evolution of biological modules.
