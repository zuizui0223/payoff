# Environment mosaics, source-sink rescue, and architecture invasion

This note lets the upstream architecture quantities vary among habitat patches.

For patch `j`, define

```text
phi_j = s_j L_j - K_j,
```

where `L_j` is the local shared-coordinate conflict load, `s_j` the recoverable fraction of that load, and `K_j` the local cost of differentiated architecture.

Let `eta_j` be the local frequency-feedback coefficient. The local PAYOFF field is

```text
f_j(p)
= p(1-p)[phi_j+eta_j(2p-1)].
```

Patches are connected by a symmetric weighted migration graph with Laplacian `L_G` and migration rate `m>=0`:

```text
dp_j/dt
= f_j(p_j)
- m (L_G p)_j.
```

The aim is to distinguish three different spatial questions:

```text
local static architecture quality      phi_j,
local rare-type growth                 phi_j-eta_j or -phi_j-eta_j,
metapopulation rare-type growth        principal eigenvalue after migration.
```

They should not be collapsed into one landscape-average number.

---

## Theorem 1 — exact heterogeneous mean-selection decomposition

Define

```text
g_j = p_j(1-p_j),
h_j = p_j(1-p_j)(2p_j-1).
```

Because symmetric migration cancels from the patch mean,

```text
d p_bar/dt
= mean_j [phi_j g_j + eta_j h_j].
```

Writing bars for patch means and `Cov` for equal-patch covariance,

```text
d p_bar/dt
= phi_bar g_bar
+ Cov(phi,g)
+ eta_bar h_bar
+ Cov(eta,h).
```

### Proof

Use

```text
mean(phi g)=mean(phi)mean(g)+Cov(phi,g)
```

and the same identity for `eta h`. Migration cancels edge-by-edge on an undirected graph. QED.

### Consequence 1.1 — environmental heterogeneity creates covariance selection

Even when

```text
phi_bar=0,
eta_bar=0,
```

the metapopulation mean can change if

```text
Cov(phi,g) + Cov(eta,h) != 0.
```

Thus a landscape-average static architecture gap is not sufficient to predict short-term global frequency change.

The new terms have a direct ecological interpretation:

```text
Cov(phi,g)
= whether patches with stronger static D advantage also contain more selectable polymorphism;

Cov(eta,h)
= whether frequency-feedback strength is spatially aligned with frequency asymmetry.
```

---

## Theorem 2 — rare differentiated architecture is a principal-eigenvalue problem

Linearize around the all-shared state

```text
p_j=0.
```

For rare `D`,

```text
f_j(p_j)
= (phi_j-eta_j)p_j + O(p_j^2).
```

Define the local rare-D margins

```text
r_j^D = phi_j-eta_j.
```

Then the linearized metapopulation dynamics are

```text
dp/dt
= [diag(r^D)-mL_G]p.
```

Because the matrix is symmetric, rare `D` grows iff

```text
Lambda_D(m)
= lambda_max[diag(r^D)-mL_G]
> 0.
```

It is neutral at `Lambda_D=0` and decays when `Lambda_D<0`.

### Rare shared architecture

Let

```text
q_j=1-p_j
```

near the all-differentiated state. Then

```text
dq/dt
= [diag(r^S)-mL_G]q + O(||q||^2),
```

with

```text
r_j^S = -phi_j-eta_j.
```

Therefore

```text
Lambda_S(m)
= lambda_max[diag(r^S)-mL_G]
```

is the reciprocal spatial invasion exponent.

### Interpretation

The nonspatial endpoint contrasts

```text
phi-eta
and
-phi-eta
```

become vectors across patches, and migration couples them through the graph Laplacian. The correct spatial invasion estimand is the principal eigenvalue, not the arithmetic mean of local margins.

---

## Theorem 3 — migration interpolates between the best source patch and the landscape mean

Let

```text
A(m)=diag(r)-mL_G
```

for a connected undirected patch graph, with local margins `r_j`.

Then

```text
Lambda(m)=lambda_max[A(m)]
```

has the following properties:

```text
Lambda(0)=max_j r_j,

Lambda(m) is nonincreasing in m,

lim_{m->infinity} Lambda(m)=r_bar.
```

If the margins are not all identical, `Lambda(m)` is strictly decreasing.

### Proof

At `m=0`, the matrix is diagonal, so its largest eigenvalue is `max r_j`.

For `m_2>m_1`,

```text
A(m_2)=A(m_1)-(m_2-m_1)L_G.
```

Since `L_G` is positive semidefinite, the Rayleigh quotient cannot increase; hence `Lambda` is nonincreasing.

If equality held at two distinct migration rates for heterogeneous `r`, a maximizing vector would have to lie in the null space of `L_G`, which on a connected graph is the uniform vector. But the uniform vector is an eigenvector of `diag(r)` only if every `r_j` is identical. Thus heterogeneity gives strict decrease.

For large `m`, any maximizing vector with a nonuniform component pays an unbounded negative Laplacian penalty. The maximizing direction therefore approaches the uniform vector, whose Rayleigh quotient is `r_bar`. QED.

---

## Corollary 3.1 — exact source-sink rescue criterion

Suppose the landscape has

```text
max_j r_j > 0
```

but

```text
r_bar < 0.
```

Then there exists one and only one finite migration threshold

```text
m_c>0
```

such that

```text
0 <= m < m_c   -> Lambda(m)>0,
m = m_c        -> Lambda(m)=0,
m > m_c        -> Lambda(m)<0.
```

Thus a favorable source patch can maintain metapopulation invasion only below a critical mixing rate when the strongly mixed landscape is unfavorable on average.

This is the cleanest PAYOFF source-sink result.

### Static special case

If frequency dependence is absent,

```text
eta_j=0,
r_j^D=phi_j=s_jL_j-K_j.
```

Then a landscape can have

```text
mean(phi_j)<0
```

—an average static BALANCE-like landscape—yet still permit differentiated architecture to invade when

```text
max(phi_j)>0
```

and migration is sufficiently weak.

In ecological language:

```text
local BITA source patches
can spatially rescue D
inside a landscape whose average static architecture gap favors S.
```

Strong migration removes the rescue by forcing the rare type to experience the negative landscape-average margin.

---

## Corollary 3.2 — no-source and all-source regimes

For any connected graph:

```text
max_j r_j <= 0
-> Lambda(m)<=0 for every m>=0;
```

no spatial mixing can create invasion in this time-independent symmetric-migration model if no patch is a source at zero migration.

Conversely,

```text
r_bar>0
-> Lambda(m)>0 for all sufficiently large m,
```

and since `Lambda` is nonincreasing from `max r_j>=r_bar>0`, invasion occurs for every migration rate.

This restriction is model-specific. Time-varying environments, asymmetric movement, non-conservative migration, or nonlinear demographic coupling can generate more complicated dispersal effects and are not covered by this theorem.

---

## Theorem 4 — exact two-patch source-sink threshold

For two unit-coupled patches with margins `r_1,r_2`,

```text
A(m)
= [[r_1-m, m],
   [m, r_2-m]].
```

The principal invasion exponent is

```text
Lambda_+(m)
= 1/2 [r_1+r_2-2m
       + sqrt((r_1-r_2)^2+4m^2)].
```

Suppose

```text
r_1>0>r_2
```

and

```text
r_1+r_2<0.
```

Then the exact rescue threshold is

```text
m_c
= r_1 r_2/(r_1+r_2)
> 0.
```

### Proof

At the neutral crossing, the largest eigenvalue is zero. The determinant condition is

```text
(r_1-m)(r_2-m)-m^2=0,
```

which reduces to

```text
r_1r_2-m(r_1+r_2)=0.
```

Solving gives the result. Under the stated sign conditions, `m_c>0`, and the second eigenvalue is negative at the crossing. QED.

### Example interpretation

With `eta=0`, let

```text
phi_1>0
```

be a local differentiated source and

```text
phi_2<0
```

a shared-favored sink, while

```text
phi_1+phi_2<0.
```

Then

```text
m_c=phi_1 phi_2/(phi_1+phi_2).
```

Below this migration rate, local dimensional-release benefit in the source patch can spatially maintain rare `D`; above it, mixing into the stronger sink eliminates invasion.

---

## 5. Reciprocal spatial invasion creates a landscape-level game classification

Define

```text
Lambda_D(m)
= lambda_max[diag(phi_j-eta_j)-mL_G],

Lambda_S(m)
= lambda_max[diag(-phi_j-eta_j)-mL_G].
```

Then the heterogeneous landscape has four reciprocal-invasion classes:

```text
Lambda_D<0, Lambda_S>0
-> spatial shared dominance;

Lambda_D>0, Lambda_S<0
-> spatial differentiated dominance;

Lambda_D>0, Lambda_S>0
-> reciprocal spatial invasion, a coexistence-compatible regime;

Lambda_D<0, Lambda_S<0
-> mutual spatial non-invasion, a coordination/history-dependent regime.
```

As in the well-mixed PAYOFF model, reciprocal invasion is a local criterion around the two monomorphic landscape states. It does not by itself prove a unique global attractor or historical transition.

---

## 6. Empirical handoff

A landscape-level PAYOFF test can be staged without fitting all quantities simultaneously.

```text
Per patch, upstream receipts:
    L_j
    s_j or R_j
    K_j
    -> phi_j=s_jL_j-K_j

PAYOFF frequency receipt:
    eta_j

Spatial receipt:
    migration graph W
    migration scale m.
```

The registered prediction is then

```text
Lambda_D(m)
= lambda_max[diag(phi_j-eta_j)-mL_G]
```

and, separately,

```text
Lambda_S(m)
= lambda_max[diag(-phi_j-eta_j)-mL_G].
```

A strong falsification design estimates the local quantities first, freezes them, and then tests whether a rare introduced architecture grows across the patch network at the predicted sign and rate.

The exact heterogeneous mean equation gives a second independent target:

```text
d p_bar/dt
= phi_bar g_bar + Cov(phi,g)
+ eta_bar h_bar + Cov(eta,h).
```

Thus patchwise spatial data can test both linear rare-invasion predictions and nonlinear aggregate selection predictions.

---

## 7. Prior-art boundary

Principal-eigenvalue persistence criteria, source-sink metapopulations, and dispersal thresholds are established ecological theory. Examples include source-sink network persistence analyses and patch models in which dominant/principal eigenvalues determine growth versus extinction.

Relevant anchors include:

- Arino, Bajeux & Kirkland (2019), *Number of Source Patches Required for Population Persistence in a Source-Sink Metapopulation with Explicit Movement*, Bulletin of Mathematical Biology, DOI `10.1007/s11538-019-00593-1`.
- Recent network source-sink analyses also characterize persistence by the maximal eigenvalue of movement-plus-local-growth operators.

PAYOFF does not claim to invent principal-eigenvalue persistence or source-sink rescue. Its contribution is the upstream substitution

```text
r_j^D
= phi_j-eta_j
= s_jL_j-K_j-eta_j
```

and the reciprocal shared-architecture margin

```text
r_j^S
= -s_jL_j+K_j-eta_j,
```

which carry empirically calibrated trait-architecture quantities into that established spatial machinery.
