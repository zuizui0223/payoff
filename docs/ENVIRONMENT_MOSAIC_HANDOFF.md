# Environment-mosaic empirical handoff

This note freezes the empirical interface for spatially heterogeneous PAYOFF tests.

## Patch-level inputs

For every patch `j`, estimate upstream quantities before fitting the spatial invasion model:

```text
SCH:
    local conflict load L_j

BITA:
    local dimensional recovery s_j or R_j

BALANCE / architecture comparison:
    local architecture cost K_j

PAYOFF frequency experiment:
    local frequency feedback eta_j.
```

Then register

```text
phi_j=s_jL_j-K_j,

r_j^D=phi_j-eta_j,
r_j^S=-phi_j-eta_j.
```

These patch-specific rare-type margins are the inputs to the spatial layer.

## Spatial inputs

The patch graph must be specified independently:

```text
W=(w_jk)
```

with symmetric non-negative movement weights for the exact model in `theory/ENVIRONMENT_MOSAIC_SOURCE_SINK.md`.

A migration scale `m` converts the registered graph into the Laplacian coupling

```text
mL_G.
```

The spatial model should not infer `W`, `m`, `phi_j`, and `eta_j` simultaneously from the same architecture-frequency time series unless the analysis is explicitly labeled exploratory.

## Primary predictions

The rare-D invasion prediction is

```text
Lambda_D(m)
= lambda_max[diag(phi_j-eta_j)-mL_G].
```

The reciprocal rare-S prediction is

```text
Lambda_S(m)
= lambda_max[diag(-phi_j-eta_j)-mL_G].
```

Interpretation:

```text
Lambda>0   rare architecture grows,
Lambda=0   neutral spatial invasion boundary,
Lambda<0   rare architecture declines.
```

For a source-sink landscape with

```text
max r_j^D>0>mean r_j^D,
```

register the predicted critical migration rate `m_c` before the invasion experiment.

## Two-patch exact receipt

For two unit-coupled patches with one D source and one D sink,

```text
r_1>0>r_2,
r_1+r_2<0,
```

the exact threshold is

```text
m_c=r_1r_2/(r_1+r_2).
```

A simple experiment can therefore vary migration across this registered threshold and test the sign change of metapopulation growth.

## Aggregate nonlinear prediction

For arbitrary patch frequencies define

```text
g_j=p_j(1-p_j),
h_j=p_j(1-p_j)(2p_j-1).
```

Then the exact predicted mean change is

```text
d p_bar/dt
= phi_bar g_bar + Cov(phi,g)
+ eta_bar h_bar + Cov(eta,h).
```

This is a second target distinct from rare invasion.

The terms should be computed separately rather than replacing all patch heterogeneity by one fitted effective `eta`.

## Key falsification cases

### F1 — source-sink threshold failure

The model is challenged if a registered landscape with

```text
max r_j^D>0>mean r_j^D
```

does not show the predicted monotone decline of the rare-D spatial growth exponent with migration.

### F2 — bridge failure

Estimate the spatial invasion exponent directly and compare it with the prediction built from

```text
phi_j=s_jL_j-K_j.
```

A mismatch can indicate failure of the shared fitness scale, incorrect architecture cost, unmeasured frequency feedback, asymmetric movement, patch-size weighting, or the linear rare-type approximation.

### F3 — aggregation failure

Freeze `phi_j,eta_j` and patch frequencies, then test

```text
observed d p_bar/dt
?
phi_bar g_bar + Cov(phi,g)+eta_bar h_bar+Cov(eta,h).
```

This is an exact instantaneous identity under the declared deterministic patch model.

## Strong ecological prediction

With `eta_j=0`, a landscape can satisfy

```text
mean(phi_j)<0
```

while still allowing rare differentiated architecture to invade at low migration if

```text
max(phi_j)>0.
```

Thus a local BITA source can rescue differentiated architecture inside an average BALANCE-like landscape. Increasing migration eventually removes the rescue when the mean margin is negative.

This is a spatial population prediction, not a redefinition of the local BALANCE or BITA chapters.
