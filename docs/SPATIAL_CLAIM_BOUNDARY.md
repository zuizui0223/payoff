# Spatial PAYOFF claim boundary

## Proved under the declared deterministic patch model

For

```text
dp_j/dt
= p_j(1-p_j)[phi+eta(2p_j-1)]
+ m sum_k w_jk(p_k-p_j),
```

with symmetric nonnegative graph weights:

```text
SPATIAL_MEAN_MIGRATION_CANCELLATION_PROVED
SPATIAL_MOMENT_CORRECTION_PROVED
GRAPH_MODE_LINEARIZATION_PROVED
ALGEBRAIC_CONNECTIVITY_SYNC_THRESHOLD_PROVED
COORDINATION_GLOBAL_MODE_REMAINS_UNSTABLE_PROVED
TWO_PATCH_POLARIZED_BRANCH_PROVED_AT_phi0
TWO_PATCH_POLARIZED_STABILITY_THRESHOLD_m_EQ_eta_OVER_6_PROVED
TWO_PATCH_POLARIZATION_EXISTENCE_THRESHOLD_m_EQ_eta_OVER_4_PROVED
```

The upstream relation

```text
phi=sL-K
```

remains conditional on the quadratic architecture bridge already declared elsewhere in PAYOFF.

## Not established by this layer

The spatial patch model does not establish:

```text
- microscopic birth-death or death-birth graph-game fixation probabilities;
- universal effects of spatial structure on architecture selection;
- universal migration thresholds for arbitrary patch networks;
- persistence of the two-patch constants eta/6 or eta/4 under asymmetric patches;
- historical evolution of spatial trait modularity;
- dispersal evolution;
- directed migration or source-sink dynamics;
- density-dependent demography.
```

## Why migration does not simply modify `eta`

Spatial heterogeneity creates the exact mean correction

```text
V[eta(3-6mu)-phi]-2eta T.
```

Therefore fitting a nonspatial affine-frequency model to spatially aggregated data can confound

```text
eta
```

with

```text
patch variance V,
patch skewness T,
and static gap phi.
```

Preferred inference keeps these quantities distinct.

## Appropriate manuscript language

Preferred:

> In a conservative patch-network extension, migration cancels from the global mean directly but alters mean selection indirectly by changing spatial moments.

Avoid:

> Migration has no effect on architecture evolution.

Preferred:

> Graph connectivity controls the damping of transverse patch differences, while the spatially uniform coordination mode remains unstable when `eta>0`.

Avoid:

> Sufficient migration stabilizes the coordination equilibrium.

Preferred:

> In the symmetric two-patch `phi=0` model, stable polarization exists for `m<eta/6` and the polarized branch disappears at `m=eta/4`.

Avoid:

> All spatial architecture mosaics disappear when migration exceeds `eta/4`.
