# General graph: habitat heterogeneity versus positive-frequency coordination

This note generalizes the exact two-patch coordination-switch result to any connected undirected patch graph.

Assume every patch shares one positive frequency-feedback coefficient

```text
eta>0,
```

but has a patch-specific reference static architecture gap

```text
phi_j=s_jL_j-K_j.
```

Let environmental forcing shift every `phi_j` by the same amount. The signed reciprocal environmental width is proportional to

```text
F(m)
= Lambda_D(m)+Lambda_S(m),
```

where

```text
Lambda_D(m)
= lambda_max[diag(phi_j-eta)-mL_G],

Lambda_S(m)
= lambda_max[diag(-phi_j-eta)-mL_G].
```

For a positive common environmental slope `alpha`,

```text
W_e,spatial(m)=F(m)/alpha.
```

---

## Theorem 1 — exact zero-migration heterogeneity criterion

At zero migration,

```text
Lambda_D(0)=max_j phi_j-eta,
Lambda_S(0)=-min_j phi_j-eta.
```

Therefore

```text
F(0)
= max phi-min phi-2eta.
```

Thus a positive reciprocal environmental invasion window exists at zero migration iff

```text
max_j phi_j-min_j phi_j
> 2eta.
```

Equivalently,

```text
range(phi)>2eta.
```

Substituting the upstream architecture quantities,

```text
range(s_jL_j-K_j)>2eta.
```

### Interpretation

Positive frequency dependence favors coordination and resists invasion from rarity. Spatial environmental contrast counters that effect because the patch most favorable to D and the patch most favorable to S need not be the same place.

The contrast must exceed twice the coordination coefficient to make both monomorphic landscape states locally invasible when patches are uncoupled.

---

## Theorem 2 — strong migration always restores a negative signed width when eta>0

For a connected graph,

```text
Lambda_D(m)
-> mean(phi)-eta,

Lambda_S(m)
-> -mean(phi)-eta
```

as `m->infinity`.

Hence

```text
F(infinity)=-2eta<0.
```

Thus sufficiently strong conservative mixing always removes any reciprocal-invasion environmental window generated solely by static patch heterogeneity when the common frequency feedback is positive.

The strong-migration limit is a mutual-non-invasion / coordination interval of signed environmental width

```text
-2eta/alpha
```

for `alpha>0`.

---

## Theorem 3 — a unique migration-driven window-collapse threshold exists

Assume

```text
eta>0,
range(phi)>2eta,
```

and the graph is connected.

The vectors

```text
phi_j-eta
```

and

```text
-phi_j-eta
```

are heterogeneous whenever `phi_j` is heterogeneous. By the spatial spectral-reduction theorem, each principal exponent is strictly decreasing with migration. Therefore

```text
F(m)=Lambda_D(m)+Lambda_S(m)
```

is strictly decreasing.

From Theorems 1 and 2,

```text
F(0)>0,
F(infinity)<0.
```

By continuity there exists exactly one

```text
m_window>0
```

such that

```text
F(m_window)=0.
```

Consequently, for a positive common environmental slope,

```text
m<m_window
-> positive reciprocal-invasion environmental window;

m=m_window
-> the two reciprocal environmental thresholds coincide;

m>m_window
-> negative signed width, i.e. mutual-non-invasion coordination interval.
```

This is a general graph existence-and-uniqueness theorem. The value of `m_window` depends on the entire placement of patch architecture gaps on the movement graph.

---

## Corollary 3.1 — if range(phi)<=2eta, migration cannot create the reciprocal window

If

```text
range(phi)<=2eta,
```

then

```text
F(0)<=0.
```

Since `F(m)` is nonincreasing,

```text
F(m)<=0
```

for every migration rate.

Thus in the declared time-independent symmetric movement model, movement cannot generate reciprocal spatial invasibility if environmental contrast is already too weak to overcome positive frequency coordination in isolated patches.

This statement is not expected to survive arbitrary directed, state-dependent, or temporally varying dispersal.

---

## 4. Two-patch closed form recovered

For two unit-coupled patches,

```text
Delta_phi=phi_1-phi_2.
```

The general contrast condition becomes

```text
|Delta_phi|>2eta.
```

The unique graph threshold has the exact closed form

```text
m_window
= [Delta_phi^2-4eta^2]/(8eta).
```

Thus `TWO_PATCH_HETEROGENEITY_COORDINATION_SWITCH.md` is the two-node closed-form corollary of the general spectral theorem.

---

## 5. Architecture interpretation

Because

```text
phi_j=s_jL_j-K_j,
```

the decisive habitat contrast is not environment per se. It is variation in the **net payoff to dimensional release**:

```text
range_j(s_jL_j-K_j).
```

Large patch variation can come from any combination of:

```text
conflict load L_j,
recoverable fraction s_j,
architecture cost K_j.
```

Hence two habitats with similar abiotic conditions need not have similar architecture-game roles if the local ecological conflict or cost of maintaining additional trait dimensions differs.

---

## 6. Empirical prediction

A spatial test can freeze patchwise

```text
phi_j=s_jL_j-K_j
```

and a common `eta`, then manipulate migration.

Before any spatial architecture-frequency data are collected, compute

```text
F(m)
= lambda_max[diag(phi-eta)-mL_G]
+ lambda_max[diag(-phi-eta)-mL_G].
```

The preregistered prediction is a single sign change when

```text
range(phi)>2eta.
```

The observed D and S reciprocal invasion thresholds across environment should merge at the predicted `m_window`.

This creates a spatial falsification test of the upstream architecture bridge rather than a post hoc fit of spatial frequencies.

---

## 7. Claim boundary

The monotonicity and principal-eigenvalue machinery are applications of established source-sink/reduction-principle theory. PAYOFF's model-specific result is the threshold comparison

```text
range_j(s_jL_j-K_j)
versus
2eta
```

and the resulting architecture interpretation of the unique migration-driven reciprocal-window collapse.
