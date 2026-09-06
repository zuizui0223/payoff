# Spatial metapopulation PAYOFF game

This note extends PAYOFF from a single well-mixed population to a network of patches connected by migration.

The purpose is deliberately narrow:

> carry the already defined architecture payoff gap `phi=sL-K` and frequency feedback `eta` into a spatially structured population without claiming that spatial evolutionary game theory itself is new.

For patch `j`, let

```text
p_j = differentiated-architecture frequency in patch j.
```

Local selection is the PAYOFF replicator field

```text
f(p)
= p(1-p)[phi+eta(2p-1)].
```

Patches are connected by a symmetric weighted graph with weights `w_jk=w_kj>=0`. Migration rate is `m>=0`:

```text
dp_j/dt
= f(p_j)
+ m sum_k w_jk(p_k-p_j).
```

Writing `L_G` for the graph Laplacian,

```text
dp/dt = f(p) - m L_G p.
```

The migration layer is conservative: it redistributes architecture frequencies among patches but does not create or destroy differentiated individuals in the patch mean.

---

## Theorem 1 — migration cancels exactly from the global mean

Let

```text
p_bar = (1/M) sum_j p_j.
```

For an undirected weighted graph,

```text
d p_bar/dt
= (1/M) sum_j f(p_j).
```

The migration term contributes exactly zero.

### Proof

Summing migration over patches gives

```text
sum_j sum_k w_jk(p_k-p_j).
```

For every undirected edge `(j,k)`, the contribution

```text
w_jk(p_k-p_j)
```

is cancelled by

```text
w_kj(p_j-p_k).
```

Therefore only the local selection terms remain. QED.

### Interpretation

Migration does not directly change the metapopulation mean, but it can change future mean selection by changing the spatial distribution of `p_j`.

---

## Theorem 2 — exact spatial-moment correction to well-mixed selection

Define

```text
mu = p_bar,
V  = mean_j (p_j-mu)^2,
T  = mean_j (p_j-mu)^3.
```

Then

```text
mean_j f(p_j)
= f(mu)
+ V[eta(3-6mu)-phi]
- 2 eta T.
```

Hence

```text
dmu/dt
= f(mu)
+ V[eta(3-6mu)-phi]
- 2 eta T.
```

### Proof

Expand the cubic selection field:

```text
f(p)
= phi(p-p^2)
+ eta(3p^2-2p^3-p).
```

Use

```text
E[p^2]=mu^2+V,
E[p^3]=mu^3+3mu V+T.
```

Substitution and collection of terms yields the result. QED.

### Consequence 2.1 — spatial heterogeneity is not equivalent to changing `eta`

The correction depends separately on

```text
V,
T,
mu,
phi,
eta.
```

Therefore fitting a well-mixed model to a spatially heterogeneous population can absorb spatial moment effects into an apparent frequency-feedback parameter.

A spatial PAYOFF analysis should estimate or experimentally control patch heterogeneity rather than silently reinterpret it as `eta`.

### Consequence 2.2 — exact midpoint result for a symmetric patch distribution

If

```text
mu=1/2,
T=0,
```

then

```text
dmu/dt
= phi(1/4-V).
```

The frequency-feedback term cancels exactly at this symmetric midpoint.

Since `0<=V<=1/4`, spatial segregation weakens the instantaneous effect of the static architecture gap without reversing its sign. At maximal segregation `V=1/4`—for example half the patches at `p=0` and half at `p=1`—the instantaneous mean selection term is zero even if `phi!=0`.

Migration can subsequently lower `V`, restoring mean selection.

---

## Theorem 3 — graph-spectrum control of patch synchronization

Suppose every patch is at the same equilibrium `p*`, so

```text
f(p*)=0.
```

Linearize around the synchronous state. Let

```text
0=lambda_1 < lambda_2 <= ... <= lambda_M
```

be the Laplacian eigenvalues of a connected patch graph.

The growth rate of graph mode `k` is

```text
r_k
= f'(p*) - m lambda_k.
```

### Proof

The Jacobian at the synchronous state is

```text
J=f'(p*) I - m L_G.
```

Because `L_G` is symmetric, its eigenvectors form an orthogonal basis. Acting on a Laplacian eigenvector with eigenvalue `lambda_k` gives the stated scalar growth rate. QED.

### Corollary 3.1 — migration cannot change global stability of a synchronous state

The uniform mode has

```text
lambda_1=0,
```

so

```text
r_1=f'(p*).
```

Migration therefore cannot stabilize a synchronous equilibrium that is unstable to a spatially uniform perturbation. It can only damp transverse differences among patches.

This is especially important in the coordination regime.

### Corollary 3.2 — exact synchronization threshold

If

```text
f'(p*)>0,
```

the slowest transverse mode is damped iff

```text
m > m_sync
```

with

```text
m_sync = f'(p*)/lambda_2.
```

If `f'(p*)<=0`, transverse perturbations already decay and `m_sync=0`.

Thus graph algebraic connectivity `lambda_2` controls how much migration is required to synchronize patch architecture frequencies.

---

## Corollary 3.3 — coordination threshold remains globally unstable

For an interior PAYOFF equilibrium

```text
p*=(1-phi/eta)/2
```

with `eta!=0`, the local derivative is

```text
f'(p*)=2 eta p*(1-p*).
```

Therefore:

```text
eta<0
-> f'(p*)<0
-> the coexistence equilibrium is stable in both uniform and transverse modes;

eta>0
-> f'(p*)>0
-> the coordination threshold is unstable in the uniform mode for every migration rate.
```

For `eta>0`, sufficiently strong migration can synchronize patches around the threshold, but it cannot make the threshold itself an attractor.

This separates two ideas that are often conflated:

```text
synchronization of patch states
!=
stabilization of the global architecture threshold.
```

---

## Theorem 4 — exact two-patch polarization branch at the symmetric architecture crossing

Consider two patches with one unit-weight migration edge:

```text
dp_1/dt=f(p_1)+m(p_2-p_1),
dp_2/dt=f(p_2)+m(p_1-p_2).
```

Set

```text
phi=0,
eta>0.
```

The anti-symmetric manifold

```text
p_1=1/2+x,
p_2=1/2-x
```

is invariant. On it,

```text
dx/dt
= (eta/2-2m)x - 2eta x^3.
```

Besides `x=0`, polarized equilibria exist iff

```text
m<eta/4
```

and satisfy

```text
x^2=1/4-m/eta.
```

Thus

```text
p_low = 1/2-sqrt(1/4-m/eta),
p_high= 1/2+sqrt(1/4-m/eta).
```

### Proof

At `phi=0`,

```text
f(1/2+x)
= eta(1/4-x^2)(2x)
= eta x/2 - 2eta x^3.
```

Migration contributes

```text
m[(1/2-x)-(1/2+x)]
= -2mx.
```

Combining terms gives the amplitude equation. Nonzero equilibria solve the stated quadratic relation. QED.

### Interpretation

At zero migration, the polarized states are exactly

```text
(p_1,p_2)=(0,1)
```

and its mirror. Increasing migration pulls the patch states toward one another until the polarized branch disappears at `m=eta/4`.

---

## Theorem 5 — stability of the two-patch polarized branch

At the polarized equilibrium, the two linear eigenvalues are

```text
r_uniform    = 6m-eta,
r_transverse = 4m-eta.
```

Therefore:

```text
0 <= m < eta/6
-> polarized branch is locally stable;

m = eta/6
-> uniform-mode stability boundary;

eta/6 < m < eta/4
-> polarized branch exists but is a saddle;

m = eta/4
-> polarized branch collides with p_1=p_2=1/2;

m > eta/4
-> no polarized equilibrium.
```

### Proof

At `p=1/2+-x`,

```text
f'(p)=eta/2-6eta x^2.
```

Using

```text
x^2=1/4-m/eta
```

gives

```text
f'(p)=6m-eta.
```

The two-patch migration Laplacian has eigenvalues `0` and `2`, so the Jacobian rates are

```text
f'(p)
```

and

```text
f'(p)-2m.
```

Substitution gives the result. QED.

### New PAYOFF interpretation

Positive frequency dependence can support **spatial architecture mosaics** even when the nonspatial system admits only the two pure attractors. Migration erodes that mosaic in two stages:

```text
m=eta/6  loss of full local stability,
m=eta/4  loss of the polarized equilibrium itself.
```

The thresholds are exact for the declared two-patch symmetric model, not universal constants for arbitrary spatial evolutionary games.

---

## 6. Relation to SCH, BALANCE, and BITA

The spatial layer does not change ownership of the upstream quantities:

```text
SCH       -> conflict load L
BITA      -> recoverable fraction s or recovery R
BALANCE   -> static architecture comparison and cost K
PAYOFF    -> phi=sL-K and frequency feedback eta
SPATIAL   -> patch frequencies, migration m, graph L_G.
```

The main new chain is

```text
L -> R=sL -> phi=R-K
        |
        v
local game f(p)
        |
        v
patch network + migration
        |
        +-> mean correction through V,T
        +-> graph synchronization through lambda_2
        +-> spatial polarization under coordination.
```

A strong empirical test should therefore estimate `phi` and `eta` independently before using spatial structure to explain patch mosaics.

---

## 7. Prior-art boundary

Spatial evolutionary games, evolutionary games on graphs, migration-coupled populations, synchronization, and bistable patch dynamics are established theory. PAYOFF should not claim those ideas as novel.

Relevant anchors include Ohtsuki et al. (2006) on evolutionary games on graphs and Ohtsuki & Nowak (2006) on graph/cycle evolutionary dynamics. Migration-coupled bistable metapopulations are also a mature dynamical-systems topic.

PAYOFF's contribution is narrower:

```text
measured shared-trait conflict L
-> measured/derived recovery sL
-> costed architecture gap phi=sL-K
-> frequency feedback eta
-> exact spatial moment and synchronization consequences
```

for the declared architecture game.
