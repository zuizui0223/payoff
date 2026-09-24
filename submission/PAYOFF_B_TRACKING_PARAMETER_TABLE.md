# PAYOFF-B tracking theory — methods parameter map

Updated: **2026-09-24**

Manuscript:

`manuscript/PAYOFF_B_TRACKING_THEORY_V1.md`

Scope:

This table compresses the model hierarchy used in the standalone synthetic
tracking-theory manuscript. It separates mathematical quantities from synthetic
design choices, sensitivity-only settings, and reporting conventions.

**None of the numeric design values below are empirical estimates.** They are
model units or declared synthetic grids unless explicitly identified as an
exact mathematical boundary.

## A. Core model quantities

| Quantity | Meaning | Role in manuscript | Status |
|---|---|---|---|
| `D_t = v t` | moving environmental demand | common forcing for open-loop landscape models | analytic definition |
| `v` | environmental/climate velocity | forcing strength | synthetic design axis |
| `x_j` | fixed spatial coordinate of patch `j` | converts redistribution into environmental tracking | analytic state geometry |
| `g` | spatial gradient converting position to environmental units | puts space and timing on a common mismatch scale | analytic conversion |
| `z_t` | phenological shift | temporal tracking state | analytic state variable |
| `s` | conversion of phenology to environmental units | makes spatial and temporal correction comparable | analytic conversion |
| `e_j(t)=D_t-g x_j-s z_t` | local abiotic mismatch | drives low-density fitness and feedback | analytic definition |
| `m` | baseline migration / redistribution rate | spatial tracking capacity | evolving synthetic strategy |
| `h` | independent phenology tracking rate | temporal tracking capacity | evolving synthetic strategy |
| `z_max` | absolute phenology bound | creates finite temporal-bypass capacity | synthetic constraint |
| `A` | abiotic mismatch penalty strength | converts mismatch to low-density growth loss | synthetic model coefficient |
| `I` | partner-mismatch interaction strength | creates dependence on interspecific matching | synthetic model coefficient |
| `g0_j` | patch low-density growth | evolutionary fitness estimand | analytic estimand |
| `d N/K` | local density penalty | abundance regulation only | demographic term; excluded from evolutionary fitness |
| `M^2` | climate-equivalent partner separation | interaction mismatch in space and phenology | analytic interaction metric |
| `N` | finite population size | controls stochastic evolutionary concentration | synthetic finite-N axis |
| `beta` | selection-strength scale | maps growth difference to relative Moran fitness | synthetic finite-N axis |

## B. Closed-loop controller quantities

| Quantity | Meaning | Exact result or design role | Status |
|---|---|---|---|
| `q_m` | movement-mediated restoring feedback | enters local mismatch recurrence | analytic controller variable |
| `q_h=1-exp(-h)` | timing-mediated restoring feedback | maps timing rate to feedback fraction | analytic mapping |
| `K=q_m+q_h` | total restoring gain | local space–time substitution coordinate | analytic definition |
| `0<K<2` | stable local-controller region | monotone for `K<1`, oscillatory but stable for `1<K<2` | exact boundary |
| `e*=r/K` | equilibrium mismatch under residual forcing `r` | local controller equilibrium | exact result |
| `c_m,c_h` | quadratic feedback costs | allocate fixed total gain across movement and timing | synthetic cost coefficients |
| `q_m*=K c_h/(c_m+c_h)` | minimum-cost movement allocation | fixed-`K` solution | exact result |
| `q_h*=K c_m/(c_m+c_h)` | minimum-cost timing allocation | fixed-`K` solution | exact result |
| `K*=[A r^2/c_eff]^(1/4)` | unconstrained optimal total gain | valid only inside stability/feasibility region | exact conditional result |

The equal-cost numerical witness uses `c_m=c_h=A=1`. Cost-asymmetry witnesses
use `(c_m,c_h)=(4,1)` and `(1,4)`. These values illustrate the exact
allocation result; they are not estimated natural costs.

## C. Canonical one-dimensional moving-landscape design

Primary source:
`docs/PAYOFF_B_MOVING_LANDSCAPE_RESULTS_20260920.md`

| Design element | Frozen setting | Purpose |
|---|---|---|
| landscape | 41 patches | explicit redistribution along a finite range |
| patch spacing | 1 model distance unit | spatial scale |
| spatial climate gradient `g` | 0.20 | converts patch position to mismatch units |
| simulation horizon | 160 generations | declared finite directional-forcing horizon |
| climate velocity grid | 0.010 to 0.080 by 0.005 | persistence frontier |
| phenology limit `z_max` | 0, 1, 2, 3, 4, 5 | temporal-capacity axis |
| strategy grid | 7 migration rates x 7 phenology rates | canonical frontier optimization |
| strategy-resolution check | 11 x 11 | checks frontier robustness |

The six frozen persistence brackets are:

| `z_max` | max persisted `v` | first failed `v` |
|---:|---:|---:|
| 0 | 0.030 | 0.035 |
| 1 | 0.035 | 0.040 |
| 2 | 0.045 | 0.050 |
| 3 | 0.050 | 0.055 |
| 4 | 0.055 | 0.060 |
| 5 | 0.065 | 0.070 |

These brackets are finite-grid synthetic outcomes, **not** empirical climate
thresholds.

## D. One-dimensional coordination-barrier design

Primary source:
`docs/PAYOFF_B_MOVING_LANDSCAPE_RESULTS_20260920.md`

| Design axis | Frozen values | Classification |
|---|---|---|
| interaction strength | 0, 0.2, 0.5, 1.0 | mechanism axis |
| partner cost bias | -0.08, 0, +0.08 | strategy-cost asymmetry |
| climate velocity | 0.02, 0.04, 0.05 | forcing axis |
| phenology limit | 1, 2, 4 | temporal-opportunity axis |
| coarse unilateral mutation step | 0.2 | canonical accessibility grid |
| fine unilateral mutation step | 0.1 | resolution sensitivity |
| coarse cells | 108 | design size |
| fine positive-interaction cells | 81 | resolution rerun subset |

The mutation step is an evolutionary-neighborhood definition, not a biological
mutation-effect estimate.

## E. Canonical two-dimensional connectivity designs

Primary source:
`docs/PAYOFF_B_2D_CONNECTIVITY_RESULTS_20260920.md`

### E1. Corridor and temporal-bypass layer

| Design element | Frozen setting | Purpose |
|---|---|---|
| landscape | 31 x 15 regular grid | route geometry |
| local movement | four cardinal neighbors | baseline movement graph |
| primary strategy grid | 7 x 7 | migration–phenology optimization |
| corridor gap widths | 1, 3, 15 | connectivity geometry |
| phenology limits for high-velocity corridor frontier | 2, 4 | temporal buffering |
| zigzag figure velocities | 0.04, 0.05, 0.06, 0.07 | temporal bypass to spatial re-entry |
| zigzag comparison phenology limits | 0, 2, 4 | route-cost buffering |

### E2. Two-species coordination layer

| Design axis | Frozen values | Purpose |
|---|---|---|
| interaction strength | 0, 0.5, 1.0 | partner-matching dependence |
| geometry | open, straight two-wall, zigzag two-wall | connectivity robustness |
| climate velocity | 0.05, 0.06 | forcing contrast |
| phenology limit | 2, 4 | alternate tracking capacity |
| coarse unilateral mutation step | 0.2 | first gate map |
| fine unilateral mutation step | 0.1 | barrier-resolution check |
| fine positive-interaction cells | 24 | confirmatory synthetic subset |
| fine frozen outcome | 22/24 barriers; 21/24 persistence rescues | result, not a design parameter |

The direct gate uses resident `(m,h)=(0.2,0)` and coordinated adjacent
strategy `(0.2,0.2)`. These are diagnostic strategy coordinates, not proposed
natural optima.

### E3. Sensitivity-only 2D settings

| Sensitivity | Frozen values | Claim licensed |
|---|---|---|
| distribution-overlap penalty scale | 0, 0.5, 1, 2 | coordination gate survives explicit distribution-level overlap |
| transverse/axial movement-weight ratio | 1, 0.5, 0.25, 0.1 | temporal buffering survives movement anisotropy |
| anisotropy velocities | 0.05, 0.06, 0.07 | route-cost sensitivity only |
| anisotropy phenology limits | 0, 2, 4 | route-cost sensitivity only |
| partner-specific cost bias for each species | -0.08, 0, +0.08 | tests synchronization under heterogeneous intrinsic preferences |
| partner-asymmetry forcing | 0.04 and 0.06 | moderate versus strong forcing |

These settings support robustness and mechanism discrimination. They are not
additional primary hypotheses or empirical calibrations.

## F. State-dependent movement-feedback landscape

Primary source:
`docs/PAYOFF_B_MOVEMENT_FEEDBACK_LANDSCAPE_RESULTS_20260920.md`

| Design element | Frozen setting | Role |
|---|---|---|
| climate velocity | 0.02, 0.03, 0.04, 0.05, 0.06 | forcing gradient |
| movement-feedback gain `k_m` | 0, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6 | state-dependent movement-controller axis |
| independent timing rate `h` | 0, 0.25, 0.5 | timing channel |
| baseline migration rate | 0.1 | movement capacity before feedback |
| maximum migration rate | 1.5 | movement-controller ceiling |
| migration cost | 0.05 | synthetic tracking cost |
| timing cost | 0.03 | synthetic tracking cost |
| phenology limit | 4 | finite timing capacity |
| movement direction | fully biased along positive climate axis | isolates controller demand |
| landscape | open 31 x 15 grid | explicit spatial dynamics |
| simulation | 100 steps; 20-step burn-in | frozen controller comparison |
| total design cells | 105 | 5 x 7 x 3 |

The controller gain `k_m` is **not** the baseline migration rate `m` and is
**not an empirical Aikens estimate**. The baseline migration rate is likewise a
synthetic model quantity in this paper.

## G. Finite-population and demographic visibility layer

Primary source:
`docs/PAYOFF_B_TRACKING_SYNTHETIC_RESULTS_20260920.md`

The manuscript uses this layer to separate three estimands:

```text
deterministic coordination barrier
!= demographic persistence effect
!= stochastic barrier crossing
```

The retained high-replication demographic result uses 128 replicates for the
independent replication of the stress design. The initial 32-replicate
cell-level large-effect pattern is retained only as a superseded pilot
comparison.

For the finite-N drift illustration at `beta=5`, reported population sizes are
`N=10,30,100,300,1000`. These are synthetic population-size conditions used
to expose the barrier-crossing/exploration tradeoff.

## H. Reporting conventions that are not model thresholds

The following should never be described as mechanistic or biological
thresholds:

- the two-thirds rule used by the early reporting classifier to label a
  strategy migration-dominant or phenology-dominant;
- strategy-grid resolution itself;
- sampled persistence-frontier brackets;
- sampled proportions such as 22/24 coordination barriers;
- the 83% route-penalty reduction;
- a p-value or gate threshold imported from the separate GEB empirical
  programme.

The standalone theory paper reports those quantities as properties of declared
synthetic designs.

## I. Parameters deliberately left uncalibrated

The synthetic paper does not assign natural values to:

- climate velocity `v`;
- spatial gradient `g`;
- phenology conversion `s`;
- mismatch penalty `A`;
- interaction strength `I`;
- migration and timing costs;
- controller gain `k_m`;
- empirical corridor width or resistance;
- finite-population `N` for any named system.

Those quantities require a separate empirical parameterization exercise and do
not become better identified by increasing synthetic sweep size.

## J. Source-of-truth hierarchy

When the manuscript, table and implementation disagree, use this order:

1. exact definitions in
   `theory/MIGRATION_PHENOLOGY_TRACKING.md` and
   `theory/CLOSED_LOOP_MOVEMENT_PHENOLOGY_TRACKING.md`;
2. frozen 2026-09-20 JSON receipts in `data/`;
3. frozen 2026-09-20 result receipts in `docs/`;
4. `data/payoff_b_tracking_theory_claim_freeze_20260924.json`;
5. manuscript prose and figure captions.

No later empirical phase-retention result can change a synthetic design value
without an explicit new tracking-theory version.
