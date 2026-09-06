# Topology PAYOFF game — pairwise reduction from modular graphs to the canonical architecture game

The edgewise modularization model produces discrete architecture topologies when linear decoupling costs make vertex architectures relevant. This note places those topologies into the multi-architecture evolutionary game.

The central result is simple:

> Every pair of topology strategies reduces exactly to the original two-strategy PAYOFF game, with intrinsic topology payoff difference as `phi` and topology-distance-weighted ecological feedback as `eta`.

---

## 1. Topology strategies

Represent a vertex architecture by a binary release vector

```text
s=(s_1,...,s_E),
s_e in {0,1},
```

where

```text
s_e=0  reference coupling retained,
s_e=1  edge maximally released.
```

Let its intrinsic optimized architecture payoff relative to the reference be

```text
b_s=R(s)-K(s).
```

These values can be generated directly by `EDGEWISE_MODULARIZATION.md`.

---

## 2. Weighted topology distance

Let edge weights

```text
w_e>0
```

measure the ecological or functional salience of disagreement about edge `e`.

Define squared feature distance

```text
q(s,t)
=sum_e w_e(s_e-t_e)^2.
```

Since the topology coordinates are binary, this is weighted Hamming distance.

Use symmetric ecological feedback

```text
H(s,t)=-gamma q(s,t).
```

Thus:

```text
gamma>0
-> unlike topologies are penalized
-> positive-frequency / coordination-like feedback;

gamma<0
-> unlike topologies are favored
-> negative-frequency / diversity-promoting feedback.
```

The many-topology symmetric payoff kernel is

```text
A_st=b_s+b_t-gamma q(s,t).
```

---

## Theorem TP1 — every topology pair is exactly the canonical PAYOFF game

Choose two topologies `S` and `T` with

```text
Delta_b=b_T-b_S,
q=q(S,T)>0.
```

Subtract the common constant `2b_S` from all entries of their 2x2 subgame. The resulting matrix is

```text
          S                         T
S         0                Delta_b-gamma q
T   Delta_b-gamma q               2Delta_b.
```

Therefore it is exactly PAYOFF's canonical matrix with

```text
phi_ST=Delta_b,
eta_ST=gamma q.
```

### Proof

The original pairwise entries are

```text
A_SS=2b_S,
A_ST=b_S+b_T-gamma q,
A_TT=2b_T.
```

Subtracting `2b_S` gives the stated matrix. Common additive payoff shifts do not affect relative selection. QED.

---

## Corollary TP1.1 — topology-frequency payoff gap

Let `p` be frequency of topology `T` in the pairwise population. Then

```text
Delta_ST(p)
=pi_T-pi_S
=Delta_b+gamma q(2p-1).
```

So topology distance scales the effective frequency-feedback coefficient.

---

## Corollary TP1.2 — exact reciprocal topology invasion conditions

Rare `T` invades resident `S` iff

```text
Delta_b-gamma q>0.
```

Rare `S` invades resident `T` iff

```text
-Delta_b-gamma q>0.
```

Hence:

### Dissimilarity-favoring feedback (`gamma<0`)

Both topologies invade each other iff

```text
|Delta_b|<|gamma| q.
```

This gives stable pairwise topology coexistence under the canonical replicator model.

### Similarity-favoring feedback (`gamma>0`)

Neither topology invades the other iff

```text
|Delta_b|<gamma q.
```

This gives pairwise coordination / bistability.

Outside those middle regions, the topology with sufficient intrinsic advantage dominates.

---

## Corollary TP1.3 — topology-normalized interaction threshold

For any topology pair with `q>0`, define intrinsic payoff slope per topology distance

```text
sigma_ST
=|b_T-b_S|/q(S,T).
```

Then a frequency-generated middle region exists exactly when

```text
|gamma|>sigma_ST.
```

The sign of `gamma` determines whether that region is coexistence or coordination.

Thus topology pairs with large architectural distance require less interaction strength per unit intrinsic payoff difference to enter a frequency-dependent middle regime.

---

## 3. Pairwise finite-population receipts

Because every topology pair maps exactly to

```text
phi=Delta_b,
eta=gamma q,
```

all finite Moran results transport immediately.

---

## Theorem TP2 — reciprocal fixation ordering ignores topology-distance feedback under exponential Moran fitness

For population size `N` and exponential selection strength `beta`,

```text
rho(T|S)/rho(S|T)
=
exp[beta(N-2)(b_T-b_S)].
```

The topology-distance feedback `gamma q` cancels from this reciprocal ratio.

Therefore

```text
rho(T|S)>rho(S|T)
iff
b_T>b_S.
```

### Interpretation

Topology distance strongly affects whether rare mutants grow initially and their absolute fixation probabilities, but in the declared exponential Moran process it does not reverse which member of a reciprocal topology pair has the larger single-mutant fixation probability.

---

## Corollary TP2.1 — weak-selection single-topology mutant criterion

A single `T` mutant has fixation probability above neutral iff

```text
3(b_T-b_S)>gamma q(S,T).
```

A single `S` mutant has fixation probability above neutral iff

```text
-3(b_T-b_S)>gamma q(S,T).
```

Thus deterministic topology invasion and stochastic topology fixation use different thresholds, exactly as in the original binary PAYOFF game.

---

## 4. Many-topology potential

For population frequencies `p_s`, the topology game is symmetric, so the standard multi-architecture potential applies:

```text
V=p^T A p.
```

Under replicator dynamics,

```text
dV/dt
=2 sum_s p_s(pi_s-pi_bar)^2
>=0.
```

For the weighted Hamming kernel, if

```text
m_e=Pr(s_e=1)
```

is marginal frequency of release at edge `e`, then for two independent draws

```text
E[q(s,t)]
=2 sum_e w_e m_e(1-m_e).
```

Therefore mean game payoff is

```text
V
=2E[b_s]
-2gamma sum_e w_e m_e(1-m_e).
```

### Interpretation

`gamma>0` penalizes edge-topology diversity; `gamma<0` rewards it. Intrinsic recovery payoff `E[b_s]` can remain strongly nonadditive because edge-release benefits interact through phenotype optimization.

---

## 5. Additive-topology null benchmark

If intrinsic topology payoff were additive,

```text
b_s=sum_e beta_e s_e,
```

then the potential separates edge by edge:

```text
V
=2 sum_e beta_e m_e
-2gamma sum_e w_e m_e(1-m_e).
```

For `gamma<0`, each edge has interior marginal coexistence frequency

```text
m_e*
=1/2 + beta_e/[2(-gamma)w_e]
```

when

```text
|beta_e|<(-gamma)w_e.
```

For `gamma>0`, the edge-level potential is convex and favors boundary release states.

This additive benchmark is useful as a negative control. Real edgewise PAYOFF recovery is generally nonadditive, so departures from this factorized prediction quantify topology interaction.

---

# Main interpretation

The topology game completes another PAYOFF loop:

```text
functional conflict
-> edgewise phenotype optimization
-> topology intrinsic payoff b_s
-> topology distance q(s,t)
-> pairwise PAYOFF parameters
   phi=b_t-b_s
   eta=gamma q
-> invasion / fixation / coexistence / coordination.
```

The binary game is therefore reusable at every pairwise level of a graph-architecture state space.

# Claim boundary

Weighted-Hamming games, symmetric potential games, and pairwise strategy reductions are standard constructions. PAYOFF's architecture-specific claim is the exact mapping from optimized coupling-topology payoffs and topology distance into the already registered `phi,eta` population receipts.
