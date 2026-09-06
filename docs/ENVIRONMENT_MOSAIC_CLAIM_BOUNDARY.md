# Environment-mosaic claim boundary

The environment-mosaic layer is a spatial extension of PAYOFF, not a claim to invent source-sink ecology or principal-eigenvalue persistence theory.

## What is established under the declared model

For equal-weight patches on a connected undirected migration graph:

```text
phi_j=s_jL_j-K_j,
r_j^D=phi_j-eta_j,
r_j^S=-phi_j-eta_j.
```

The model establishes:

1. exact heterogeneous mean-selection decomposition

```text
d p_bar/dt
= phi_bar g_bar + Cov(phi,g)
+ eta_bar h_bar + Cov(eta,h);
```

2. exact rare-D invasion operator

```text
diag(r^D)-mL_G;
```

3. exact rare-S invasion operator

```text
diag(r^S)-mL_G;
```

4. invasion iff the relevant largest eigenvalue is positive;
5. for time-independent symmetric migration, the largest eigenvalue decreases from `max r_j` at `m=0` toward `mean r_j` as `m->infinity`;
6. with heterogeneous margins and a connected graph this decline is strict;
7. if `max r_j>0>mean r_j`, one finite critical migration threshold exists;
8. for two unit-coupled source-sink patches the threshold is

```text
m_c=r_1r_2/(r_1+r_2)
```

under `r_1>0>r_2` and `r_1+r_2<0`.

## What is not established

### Principal-eigenvalue source-sink theory is prior art

Using dominant/principal eigenvalues to classify persistence in patch networks is established mathematical ecology. PAYOFF's contribution is only to supply the architecture-specific local margins

```text
s_jL_j-K_j-eta_j
```

and their reciprocal shared-architecture counterparts.

### Safe symmetric migration is a restrictive movement model

The monotone rescue-loss theorem assumes:

```text
time-independent local margins,
undirected symmetric conservative migration,
equal patch weighting,
connected graph.
```

Asymmetric dispersal, mortality during movement, temporal environmental variation, directed networks, patch-size differences, or state-dependent migration can violate the monotonicity and strong-migration limit used here.

### Low-migration rescue is not historical causation

Showing that a differentiated architecture can currently be maintained by one or more source patches does not establish that those patches caused its historical origin.

### Landscape-average BALANCE is descriptive shorthand only

When

```text
mean(phi_j)<0,
```

this may be described as an average static shared-favored landscape, but it does not turn BALANCE into a landscape-level chapter definition. Local BALANCE/BITA ownership remains patch/context specific.

### Reciprocal invasion does not prove stable coexistence globally

`Lambda_D>0` and `Lambda_S>0` establish reciprocal local invasibility of the two monomorphic landscape states. Nonlinear global dynamics can still depend on migration, heterogeneity, and higher-order spatial structure.

## Preferred language

Preferred:

> Under the declared symmetric patch model, local architecture source patches can permit differentiated architecture to invade even when the landscape-average static architecture gap is negative, provided migration is below a principal-eigenvalue threshold.

Avoid:

> Spatial structure always rescues differentiated architecture in BALANCE landscapes.

Preferred:

> The spatial invasion exponent is the largest eigenvalue of the migration-coupled local architecture margins.

Avoid:

> PAYOFF discovers the principal-eigenvalue theory of source-sink persistence.

Preferred:

> In the two-patch source-sink special case, the critical migration rate has the closed form `r_1r_2/(r_1+r_2)`.

Avoid:

> This migration threshold is universal across spatial evolutionary games.
