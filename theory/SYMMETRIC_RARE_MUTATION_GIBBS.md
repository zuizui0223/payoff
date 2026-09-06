# Symmetric rare-mutation Gibbs law — self-play scores control monomorphic stationary abundance

`TOPOLOGY_RARE_MUTATION.md` derived a simple stationary law for the zero-diagonal topology-distance game. The result extends much further.

For any finite symmetric architecture game, the rare-mutation monomorphic stationary distribution under symmetric mutation and exponential Moran fitness depends only on the strategies' self-play payoffs.

Off-diagonal ecological interactions affect deterministic game dynamics and substitution kinetics, but cancel from the reversible stationary weights.

---

## 1. General symmetric architecture game

Let there be architecture strategies

```text
i=1,...,M
```

with a symmetric payoff matrix

```text
A=A^T.
```

For every strategy define its self-play score

```text
u_i=A_ii/2.
```

Take a pair `i,j`. Its symmetric 2x2 subgame is

```text
[[A_ii,A_ij],
 [A_ij,A_jj]].
```

By `SYMMETRIC_GAME_CANONICALIZATION.md`, its canonical endpoint-centered coordinate is

```text
phi_ij
=(A_jj-A_ii)/2
=u_j-u_i.
```

The interaction-curvature coordinate is

```text
eta_ij
=(A_ii+A_jj-2A_ij)/2.
```

---

## Theorem SRMG1 — reciprocal fixation ratio depends only on self-play score difference

Under the declared self-excluding exponential-fitness Moran process,

```text
rho(j|i)/rho(i|j)
=
exp[beta(N-2)(u_j-u_i)].
```

The off-diagonal pair payoff `A_ij`, and therefore `eta_ij`, cancels exactly.

### Proof

The registered two-strategy result is

```text
rho_D/rho_S
=exp[beta(N-2)phi].
```

Canonicalization gives `phi=u_j-u_i`. QED.

---

## 2. Rare symmetric architecture mutation

Assume mutations connect the finite strategy set by a connected graph and are symmetric on every allowed link:

```text
mu_ij=mu_ji>0.
```

In the rare-mutation limit, monomorphic substitution rate is

```text
Q_ij=mu_ij rho(j|i).
```

---

## Theorem SRMG2 — exact Gibbs stationary law for any symmetric game

The monomorphic substitution chain is reversible with stationary distribution

```text
Pi_i
=
exp[beta(N-2)u_i]
/
sum_k exp[beta(N-2)u_k].
```

Equivalently,

```text
Pi_i
propto
exp[beta(N-2)A_ii/2].
```

### Proof

For an allowed pair,

```text
Pi_i Q_ij / (Pi_j Q_ji)
=
exp[beta(N-2)(u_i-u_j)]
*mu_ij/mu_ji
*rho(j|i)/rho(i|j)
=1.
```

Thus detailed balance holds. Connectedness gives the unique stationary law. QED.

---

## Corollary SRMG2.1 — off-diagonal ecology controls dynamics but not symmetric weak-mutation monomorphic weights

Changing

```text
A_ij, i!=j
```

while holding all diagonal entries fixed can change:

```text
rare-invasion signs,
coexistence versus coordination,
interior equilibria,
absolute fixation probabilities,
substitution rates,
and absorption times.
```

But it does not change the stationary monomorphic probabilities in Theorem SRMG2.

This is a sharp separation between:

```text
interaction dynamics
and
long-run monomorphic state weights
```

under the declared order of limits.

---

## Corollary SRMG2.2 — architecture decomposition

For

```text
A_ij=b_i+b_j+H_ij,
```

one has

```text
u_i
=b_i+H_ii/2.
```

Therefore

```text
Pi_i
propto
exp{beta(N-2)[b_i+H_ii/2]}.
```

If same-type ecological feedback is registered as zero,

```text
H_ii=0,
```

then

```text
Pi_i
propto
exp[beta(N-2)b_i].
```

This recovers the topology Gibbs law.

---

## Corollary SRMG2.3 — equal diagonal feedback leaves only intrinsic architecture payoff

If

```text
H_ii=h0
```

is the same for every architecture, the common factor

```text
exp[beta(N-2)h0/2]
```

cancels in normalization. Hence stationary weights again depend only on `b_i`.

---

## Theorem SRMG3 — reversible mutation bias acts as a prior over self-play scores

Suppose mutation is not symmetric but is reversible with positive weights `nu_i`:

```text
nu_i mu_ij
=nu_j mu_ji.
```

Then

```text
Pi_i
propto
nu_i exp[beta(N-2)u_i].
```

So

```text
log Pi_i
=constant
+log nu_i
+beta(N-2)u_i.
```

Mutation bias and self-play selection add on the log-occupancy scale.

---

## 3. Strong-selection and neutral limits

At

```text
beta=0,
```

symmetric mutation gives uniform monomorphic occupancy across connected states.

As

```text
beta(N-2)->infinity,
```

stationary mass concentrates on strategies maximizing

```text
u_i=A_ii/2.
```

If there is one unique self-play maximizer, its stationary probability tends to one.

If several strategies tie for the maximum and mutation is symmetric, the limiting mass is shared equally among the tied maxima.

---

## 4. Order-of-limits warning

The Gibbs law is a **rare-mutation monomorphic substitution** result.

It should not be confused with:

```text
deterministic replicator equilibrium,
quasi-stationary polymorphism,
or the full stationary distribution under recurrent mutation.
```

In particular, strong negative-frequency dependence can create a stable deterministic polymorphism and a very long finite-population absorption time. If mutations occur before absorption, the monomorphic chain is not the right model and the Gibbs law need not describe observed architecture frequencies.

---

# PAYOFF interpretation

This theorem identifies a broad invariant of the PAYOFF transport programme:

```text
symmetric pair game
        |
        v
canonical phi
=(self-play difference)
        |
        v
reciprocal fixation ratio
        |
        v
rare-mutation Gibbs weight.
```

Interaction curvature `eta` governs what happens **between** monomorphic endpoints; self-play score controls their reciprocal fixation ordering and symmetric rare-mutation stationary weighting.

# Prior-art / claim boundary

Reversible Markov chains, weak-mutation substitution processes, and Gibbs-like stationary laws are standard stochastic-process ideas. PAYOFF's useful statement is the exact architecture-game mapping that makes the self-play/off-diagonal separation explicit under the registered exponential Moran process.
