# Spatial PAYOFF empirical handoff

This note freezes what must be measured before the spatial/metapopulation layer is interpreted biologically.

## Upstream receipts

```text
SCH
- common reproductive fitness scale
- conflict-active context
- compromise geometry
- conflict load L

BITA
- dimensional release s or direct recovery R
- residual coupling / mechanism evidence when available

BALANCE
- architecture cost K on the same fitness scale
- direct shared-versus-differentiated worldline check when available

PAYOFF nonspatial
- phi=sL-K or direct WD*-WS*
- frequency feedback eta from architecture-frequency manipulation
```

Only after those quantities are frozen should the spatial layer add

```text
patch frequencies p_j
migration/connectivity graph W
migration-rate scale m
patch number M
```

or a justified stochastic analogue.

## Primary spatial predictions

For the deterministic patch model

```text
dp_j/dt
= p_j(1-p_j)[phi+eta(2p_j-1)]
+ m sum_k w_jk(p_k-p_j),
```

PAYOFF predicts three distinct spatial receipts.

### 1. Mean-selection receipt

Measure across patches

```text
mu = mean(p_j)
V  = variance(p_j)
T  = third central moment(p_j).
```

Then

```text
dmu/dt
= f(mu)
+ V[eta(3-6mu)-phi]
- 2eta T.
```

This can be tested without reconstructing the whole graph if patch frequencies and short-term mean change are available.

### 2. Synchronization receipt

For a connected undirected patch graph with Laplacian algebraic connectivity `lambda_2`, a synchronous equilibrium `p*` has transverse mode threshold

```text
m_sync=max(0,f'(p*)/lambda_2).
```

A strong test varies connectivity or migration while holding local payoff parameters fixed and asks whether patch-to-patch deviations change sign at the registered threshold.

### 3. Two-patch coordination receipt

For the symmetric two-patch control

```text
phi=0,
eta>0,
```

polarized equilibria satisfy

```text
p_low = 1/2-sqrt(1/4-m/eta)
p_high= 1/2+sqrt(1/4-m/eta)
```

for

```text
m<eta/4.
```

They are locally stable only for

```text
m<eta/6.
```

This supplies a clean proof-of-mechanism experiment for migration-eroded architecture mosaics.

## Identification order

Do not infer `eta` from spatial patch mosaics alone.

The exact mean equation shows that patch variance and skewness alter mean selection even at fixed `eta`. Therefore the preferred order is

```text
1. estimate phi from upstream architecture geometry;
2. estimate eta in a well-mixed or spatially controlled frequency manipulation;
3. register the patch graph and migration scale;
4. predict spatial moments / synchronization / polarization out of sample.
```

A fit in which `phi`, `eta`, migration, and patch heterogeneity are all inferred from the same spatial time series is exploratory rather than a decisive cross-repository test.

## Falsification targets

The spatial bridge fails, or at least requires extension, if any of the following persist after measurement error is accounted for:

```text
- symmetric migration changes the global mean directly beyond local selection;
- the observed mean-selection residual disagrees with the V,T correction;
- synchronized-state transverse growth rates do not scale with graph Laplacian modes;
- a registered two-patch phi=0 experiment retains a stable polarized branch above m=eta/6;
- the polarized branch remains present above m=eta/4.
```

Possible causes include directed migration, unequal patch sizes, nonlinear frequency feedback, environmental heterogeneity among patches, density dependence, nonconservative dispersal, or incorrect upstream `phi`/`eta` receipts.

## Claim ceiling

Spatial evolutionary games and migration-coupled bistable systems are established theory. The spatial PAYOFF claim should be limited to the consequences of carrying the ecology-derived architecture quantities

```text
L -> R=sL -> phi=R-K -> eta
```

into the declared conservative patch-network model.
