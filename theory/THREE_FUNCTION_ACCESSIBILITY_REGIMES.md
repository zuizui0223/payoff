# Three-function accessibility regimes — global modularity versus evolutionary reachability

The worked example in `THREE_FUNCTION_TOPOLOGY_EXAMPLE.md` has

```text
theta=(0,1,3),
a_i=1,
reference triangle couplings c_e=1,
common edge-release cost k.
```

This note varies `k` and separates three questions:

```text
1. Which topology has the highest intrinsic payoff?
2. Can infinitesimal decoupling start from the fully coupled reference?
3. If not, can a finite single-edge mutation move uphill?
```

Those questions have different exact thresholds.

---

## 1. Exact intrinsic payoffs of the key topologies

Write release topology bits in edge order

```text
(01,02,12),
```

where `1` means released.

Three states organize the global phase diagram.

### Fully coupled reference

```text
000:
b_000=0.
```

### Two-module state

```text
011:
released 02 and 12,
retained 01,
modules {0,1}|{2}.
```

Its recovery is `19/6`, so

```text
b_011
=19/6-2k.
```

### Fully released state

```text
111:
b_111
=7/2-3k.
```

---

## Theorem A1 — exact global topology phases

The two-module state beats full release iff

```text
19/6-2k > 7/2-3k
```

which reduces to

```text
k>1/3.
```

It beats the fully coupled reference iff

```text
19/6-2k>0
```

which reduces to

```text
k<19/12.
```

Direct comparison with the other five vertex topologies shows they do not exceed `011` inside this interval.

Therefore the exact global phases are

```text
k<1/3
-> full differentiation 111;

1/3<k<19/12
-> two-module optimum 011={0,1}|{2};

k>19/12
-> fully coupled reference 000.
```

At `k=1/3` and `k=19/12` the adjacent phases tie.

---

## 2. Infinitesimal accessibility from the reference

At the fully connected reference, edge pressures are

```text
pressure_01=1/16,
pressure_02=9/16,
pressure_12=1/4.
```

The largest is `9/16` on edge `02`.

Thus some infinitesimal edge release is selected from the reference iff

```text
k<9/16.
```

Inside the two-module global phase, this gives the first accessibility boundary

```text
k_local=9/16.
```

When `1/3<k<9/16`, the exact pressure path is

```text
000 -> 010 -> 011.
```

After releasing `02`, the retained `12` pressure rises to `49/64`, which is automatically above `k` throughout this interval, so the second release remains locally accessible.

---

## 3. Finite single-edge mutation accessibility

Even when infinitesimal release is selected against, a mutation may change an edge by a finite amount.

The best one-edge neighbor of `000` is `010`, whose payoff is

```text
b_010
=9/8-k.
```

Therefore a complete release of edge `02` is uphill iff

```text
k<9/8.
```

This gives a second accessibility boundary

```text
k_flip=9/8.
```

Hence

```text
9/16<k<9/8
```

has the unusual property

```text
all infinitesimal release directions are initially selected against,

but

a finite full release of edge 02 increases payoff.
```

This is a concrete finite-jump modularization regime.

Once `010` is reached, moving to the global module `011` is strongly uphill throughout this interval because

```text
b_011-b_010
=49/24-k>0.
```

---

## 4. Single-edge fitness-valley regime

For

```text
k>9/8,
```

even the best one-edge neighbor `010` lies below the reference:

```text
b_010=9/8-k<0=b_000.
```

All other one-edge neighbors are lower still.

But the global two-module topology remains above the reference until

```text
k=19/12.
```

Therefore

```text
9/8<k<19/12
```

is an exact architecture accessibility paradox:

```text
global optimum = 011={0,1}|{2},
reference 000 is a strict one-edge local optimum.
```

Any single-edge mutation path from `000` to `011` must initially descend in intrinsic payoff.

---

## Theorem A2 — exact best-path valley depth

The best first step is always

```text
000 -> 010,
```

with bottleneck payoff

```text
9/8-k.
```

The source payoff is zero, so the intrinsic valley depth is

```text
B_valley
=0-(9/8-k)
=k-9/8.
```

Thus in the valley regime

```text
boxed: B_valley=k-9/8.
```

It grows linearly from zero at the finite-edge-flip threshold to

```text
19/12-9/8
=11/24
```

as the two-module global phase approaches its upper boundary.

---

## 5. Complete accessibility atlas within one global phase

The same global topology `011` therefore contains three distinct evolutionary-accessibility regimes:

```text
1/3 < k < 9/16
    global module 011
    + infinitesimal pressure path available;

9/16 < k < 9/8
    global module 011
    + infinitesimal release blocked
    + finite full-edge mutation uphill;

9/8 < k < 19/12
    global module 011
    + every one-edge mutation initially downhill
    + positive fitness valley required.
```

So

```text
same architecture optimum
!=
same evolutionary accessibility.
```

---

## 6. Biological interpretation

This creates a useful distinction among three mechanisms that can all end at the same module partition.

### Gradual modularization

When `k<9/16`, marginal selection already points toward edge release.

### Saltational / finite-effect modularization

When `9/16<k<9/8`, the local derivative points backward, but a sufficiently large architectural mutation crosses the convex-recovery barrier and lands at higher payoff.

### Valley-crossing modularization

When `9/8<k<19/12`, even a complete one-edge change is deleterious. Reaching the global module requires drift, multi-edge mutation, recombination, environmental change, or another mechanism capable of crossing a fitness valley.

PAYOFF therefore separates

```text
what architecture is best
```

from

```text
what mutational step sizes and population processes can reach it.
```

---

## 7. Relation to BALANCE

The upper module boundary

```text
k=19/12
```

is a static payoff comparison: above it, the fully coupled architecture wins.

The lower accessibility boundaries

```text
9/16,
9/8
```

answer different questions about local and finite mutational reachability.

Thus an architecture can be globally BITA-like

```text
release would pay overall
```

while remaining dynamically trapped in a BALANCE-like integrated state because the accessible mutation neighborhood does not contain an improving move.

This is an architecture-space analogue of the broader PAYOFF rule:

```text
static advantage != invasion/accessibility.
```

---

## 8. Claim boundary

These thresholds are exact for the declared three-function quadratic example and common linear edge-release cost.

They are not universal constants of modular evolution. Their role is to demonstrate that the PAYOFF machinery can distinguish global architecture value from gradual, finite-step, and valley-crossing accessibility using quantities computed from the same upstream conflict geometry.
