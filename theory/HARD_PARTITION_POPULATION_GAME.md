# Hard-partition population game — module architectures as canonical PAYOFF strategies

> **Candidate-set scope update:** HPG2 below is exact only for the restricted
> three-state set `{S,M,F}`. Three functions admit five partitions. The omitted
> `{0}|{1,2}` partition invades this restricted solution for `h>1`; the complete
> five-partition game has boundaries `1/2, 1, 13/6` and a four-way coexistence
> regime. See [the complete-candidate audit](FULL_PARTITION_EQUILIBRIUM_AUDIT.md)
> for all-invader proofs, corrected full-game frequencies, degeneracy treatment
> and the tested KKT solver. The restricted formulas remain below as provenance.

The hard-module layer generates discrete architecture states without requiring a reference edgewise coupling graph. This note gives those partitions a natural architecture distance and transports them into the PAYOFF population game.

---

## 1. Co-membership feature representation

For partition `P`, define one binary feature for every unordered pair of functions:

```text
c_ij(P)=1  if i and j belong to the same module,
          0  otherwise.
```

Thus a partition becomes a binary co-membership vector

```text
c(P).
```

For positive pair weights `w_ij`, define partition distance

```text
q(P,Q)
=sum_{i<j} w_ij [c_ij(P)-c_ij(Q)]^2.
```

With unit weights this is the number of function pairs whose same-module versus different-module status changes between the two architectures.

Because the full co-membership vector uniquely identifies a set partition, `q` is a squared Euclidean / weighted Hamming distance on the finite partition state space.

---

## 2. Intrinsic hard-partition payoff

For hard partition `P`, let

```text
b(P)
=R(P)-K(P).
```

Under constant per-extra-module cost,

```text
b(P)
=s_P L-kappa(|P|-1).
```

This quantity is fixed before population-frequency feedback is added.

---

## 3. Symmetric partition-distance feedback

Use

```text
H(P,Q)
=-gamma q(P,Q).
```

The symmetric game kernel is

```text
A(P,Q)
=b(P)+b(Q)-gamma q(P,Q).
```

Since

```text
q(P,P)=0,
```

same-partition ecological feedback is zero in this registered kernel.

---

## Theorem HPG1 — every hard-partition pair is an exact canonical PAYOFF game

For two partitions `P,Q`, define

```text
phi_PQ=b(Q)-b(P),
eta_PQ=gamma q(P,Q).
```

Then their two-strategy subgame is exactly PAYOFF's canonical form, up to one common additive payoff shift:

```text
[[0, phi-eta],
 [phi-eta, 2phi]].
```

Therefore all existing deterministic invasion and finite-population receipts apply pairwise.

In particular:

```text
gamma<0 and |b(Q)-b(P)|<|gamma|q(P,Q)
-> stable pairwise coexistence;

gamma>0 and |b(Q)-b(P)|<gamma q(P,Q)
-> coordination bistability.
```

---

## 4. Multi-partition potential geometry

Let `p_P` be a population distribution over hard partitions. Define pairwise co-membership frequency

```text
m_ij
= sum_P p_P c_ij(P).
```

For two independent population draws,

```text
E[(c_ij(P)-c_ij(Q))^2]
=2m_ij(1-m_ij).
```

Therefore the mean symmetric-game payoff is

```text
V(p)
=2 sum_P p_P b(P)
 -2 gamma sum_{i<j} w_ij m_ij(1-m_ij).
```

For

```text
gamma<0,
```

the second term rewards diversity in module co-membership states.

For

```text
gamma>0,
```

it penalizes co-membership variance and favors architectural coordination.

### Geometric consequence

Because squared Euclidean distance matrices are conditionally negative semidefinite,

```text
z^T Q z<=0
```

for every coefficient vector `z` with `sum z=0`.

Thus when `gamma<0`, the quadratic population potential is concave on the strategy simplex, and strictly concave whenever the active partition feature vectors are affinely independent.

So negative partition-distance feedback produces a well-behaved diversity-maximization problem rather than arbitrary cyclic game dynamics.

---

# Registered three-function architecture game

Use the hard-module example

```text
theta=(0,1,3),
a=(1,1,1),
kappa=1.
```

Consider three nested architecture states:

```text
S = {0,1,2}       fully shared
M = {0,1}|{2}     optimal two-module architecture
F = {0}|{1}|{2}   fully separated.
```

Their intrinsic payoffs relative to `S` are

```text
b_S=0,
b_M=19/6,
b_F=8/3.
```

Using co-membership features ordered as `(01,02,12)`:

```text
c(S)=(1,1,1),
c(M)=(1,0,0),
c(F)=(0,0,0).
```

Hence unit-weight distances are

```text
q(S,M)=2,
q(M,F)=1,
q(S,F)=3.
```

Let

```text
gamma=-h,
h>0.
```

Then dissimilar architecture encounters receive reward `+h q`.

---

## Theorem HPG2 — exact three-state phase sequence

For the registered `S,M,F` game:

### Phase I — monomorphic intermediate module

If

```text
0<=h<=1/2,
```

`M` is the unique global potential maximizer and the stable population state is

```text
p_M=1.
```

### Phase II — intermediate plus fully separated coexistence

If

```text
1/2<h<=19/12,
```

the stable population lies on the `M-F` edge:

```text
p_F
=(2h-1)/(4h),
```

```text
p_M
=(2h+1)/(4h),
```

```text
p_S=0.
```

### Phase III — three-way architecture coexistence

If

```text
h>19/12,
```

the unique interior stable equilibrium is

```text
p_S
=(12h-19)/(24h),
```

```text
p_M
=25/(24h),
```

```text
p_F
=(2h-1)/(4h).
```

### Proof

Relative effective payoffs, after removing the common partner intrinsic-payoff term, are

```text
u_S=2h p_M+3h p_F,
```

```text
u_M=19/6+2h p_S+h p_F,
```

```text
u_F=8/3+3h p_S+h p_M.
```

For `h<=1/2`, rare `F` against `M` has margin

```text
-1/2+h<=0,
```

while rare `S` has margin

```text
-19/6+2h<0.
```

So `M` remains stable.

For `h>1/2`, solving `u_M=u_F` on `p_S=0` gives the Phase-II frequencies. At that boundary equilibrium,

```text
u_S-u_M
=2h-19/6.
```

Thus `S` can invade exactly when

```text
h>19/12.
```

Solving `u_S=u_M=u_F` with `p_S+p_M+p_F=1` gives the Phase-III frequencies.

The co-membership feature vectors of `S,M,F` are affinely independent, so for `h>0` the squared-distance contribution makes the potential strictly concave on this three-state simplex. Therefore any KKT solution in the relevant face is the unique stable global potential maximizer. QED.

---

## Corollary HPG2.1 — strong dissimilarity feedback removes the intermediate architecture

As

```text
h->infinity,
```

Phase III gives

```text
p_S->1/2,
p_M->0,
p_F->1/2.
```

Thus very strong architecture-dissimilarity reward asymptotically favors the two extreme module states rather than the intrinsically optimal intermediate module.

This mirrors the continuous-recovery branching result in which strong negative-frequency feedback drives a protected mixture of shared and fully differentiated endpoints.

The two models are not identical, but they recover the same qualitative endpoint-diversification limit from different architecture state spaces.

---

## Corollary HPG2.2 — frequency dependence can maintain a statically suboptimal module count

At `kappa=1`, full separation has lower intrinsic payoff than `M` by

```text
b_M-b_F=1/2.
```

Nevertheless, when

```text
h>1/2,
```

full separation is maintained at positive stable frequency.

Thus

```text
static module-count optimum
!=
population architecture composition.
```

A costly extra module can persist because its rarity creates enough architecture-distance advantage.

---

## 5. Rare-mutation stationary ordering

Because

```text
H(P,P)=0,
```

self-play score is simply

```text
u_P=b(P).
```

Under symmetric rare mutation and the registered exponential Moran process,

```text
Pi(P)
propto
exp[beta(N-2)b(P)].
```

Therefore the intrinsic hard-module optimum `M` has the largest monomorphic stationary weight for every finite `h`, even in Phase III where deterministic population dynamics maintain all three partitions simultaneously.

This repeats a central PAYOFF distinction:

```text
deterministic coexistence
!=
rare-mutation monomorphic occupancy.
```

---

## 6. Biological interpretation

The co-membership kernel asks whether ecological interactions reward or penalize being architecturally different in **which functional pairs are locked together**.

It does not assume that organisms literally inspect module partitions. `gamma` is a reduced population-level interaction coefficient whose biological origin must be identified independently.

The value of this construction is that hard-module architectures generated from SCH/BITA/BALANCE receipts can enter the same canonical PAYOFF machinery without inventing a reference edge graph solely to define architecture distance.

---

## 7. Claim boundary

Squared-distance potential games and conditional negative definiteness of Euclidean distance matrices are established mathematics.

PAYOFF's candidate result is the architecture specialization:

> hard module partitions can be encoded by pairwise co-membership features; under the declared distance feedback, every partition pair inherits canonical PAYOFF coordinates, and the registered restricted three-state subgame exhibits exact transitions from one intermediate module architecture to two-state and then three-state architecture polymorphism as negative frequency feedback strengthens. The full five-partition result is in `FULL_PARTITION_EQUILIBRIUM_AUDIT.md`.
