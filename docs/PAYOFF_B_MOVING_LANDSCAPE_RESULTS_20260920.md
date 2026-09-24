# PAYOFF-B explicit moving-landscape synthetic results receipt

Frozen: 2026-09-20

This receipt records the canonical synthetic results from the explicit
moving-climate landscape extension of PAYOFF-B migration–phenology tracking.

These are synthetic model results under the declared designs. They are not
natural frequencies, calibrated ecological thresholds, or predictions for a
named species.

## 1. Canonical model boundary

Patches have fixed spatial coordinates x_j. Environmental demand moves as

    D_t = v t,

and local climatic mismatch is

    e_j(t) = D_t - g x_j - s z_t.

Spatial tracking is emergent:

    local environmental selection
    + conservative nearest-neighbor dispersal
    -> movement of the abundance centroid.

Phenological tracking changes z_t from the abundance-weighted residual mismatch
and is bounded by

    |z_t| <= z_max.

Two species interact through a climate-equivalent distance

    M^2
    = [g(xbar_A-xbar_B)]^2
      + [s(z_A-z_B)]^2.

Evolutionary fitness is low-density growth,

    g0_j
    = baseline
      - architecture cost
      - abiotic mismatch penalty
      - interaction mismatch penalty.

Density-regulated realized growth is kept separate:

    g_j = g0_j - d N/K.

This separation is canonical. Strategy optimization and coevolution use g0,
whereas abundance dynamics use g.

## 2. Superseded pre-fix runs

An early spatial implementation mistakenly used density-regulated realized
growth as evolutionary fitness. That creates a spurious incentive for costly
tracking strategies to lower abundance and thereby relax competition.

The following successful exploratory runs are therefore explicitly superseded
and must not be used for scientific claims:

- moving-landscape pilot run 35472485844;
- landscape-frontier pilot run 35472609750;
- landscape-frontier resolution run 35472709087.

The fitness boundary was then corrected and regression-tested. Only runs after
that correction are canonical below.

## 3. Moving-landscape persistence frontier

### 3.1 Canonical 7 x 7 strategy grid

Workflow run: 35472802030
Artifact: 10593885973
Digest: sha256:78dd1e229f469a7e315468bbf83e761ad4627e4505159494f8af8333303f4901

Design:

    climate velocity:
      0.010 to 0.080 in increments of 0.005

    phenology limit:
      0, 1, 2, 3, 4, 5

    spatial landscape:
      41 patches
      patch spacing = 1
      climate gradient = 0.20
      final time = 160 generations

    strategy grid:
      7 migration rates x 7 phenology rates.

For every phenology limit, persistence was monotone non-increasing across the
sampled climate-velocity grid.

The finite-grid persistence frontier was:

| phenology limit | max persisted velocity | first failed velocity |
|---:|---:|---:|
| 0 | 0.030 | 0.035 |
| 1 | 0.035 | 0.040 |
| 2 | 0.045 | 0.050 |
| 3 | 0.050 | 0.055 |
| 4 | 0.055 | 0.060 |
| 5 | 0.065 | 0.070 |

Every frontier strategy was migration-dominant. Thus increased phenological
capacity expands the range of climate velocities that can be survived, but
spatial redistribution remains necessary near the persistence boundary.

### 3.2 Strategy-grid resolution check

Workflow run: 35472806452
Artifact: 10593036709
Digest: sha256:de80b90512071c92e335b41ee356ebea2b7d3ef2e684dde842244011460599b7

The strategy grid was refined from 7 x 7 to 11 x 11. All six persistence
brackets were unchanged.

The 11 x 11 frontier strategies were:

| phenology limit | migration rate | phenology rate |
|---:|---:|---:|
| 0 | 0.3 | 0.0 |
| 1 | 0.4 | 0.1 |
| 2 | 0.4 | 0.1 |
| 3 | 0.4 | 0.1 |
| 4 | 0.3 | 0.1 |
| 5 | 0.2 | 0.1 |

The finite-grid frontier is therefore not an artefact of the coarser strategy
lattice used in the first canonical run.

## 4. A geometric capacity law approximates the frontier

For the 41-patch landscape, the leading-edge position is x=20 and the spatial
climate-equivalent capacity is

    g x_edge = 0.20 x 20 = 4.

Adding phenological capacity gives

    C = 4 + z_max.

The perfect-tracking geometric ceiling is therefore

    v_zero = C / 160.

For z_max = 0,...,5 this gives

    0.02500, 0.03125, 0.03750, 0.04375, 0.05000, 0.05625.

The observed persistence frontier lies above this perfect-matching ceiling
because persistence does not require zero mismatch.

Using each 11 x 11 frontier strategy, the best-case terminal low-density growth
ceiling is approximately

    0.02982, 0.03605, 0.04230, 0.04855, 0.05482, 0.06108.

These values predict the six sampled persistence-frontier velocities with

    R^2 approximately 0.987
    mean absolute error approximately 0.0016 velocity units.

This is retained as a capacity diagnostic, not a fitted universal law.
Finite-horizon population inertia can allow persistence slightly beyond a
terminal non-negative-growth ceiling, and the model horizon is part of the
declared design.

A descriptive linear fit of the six sampled frontier points against z_max has

    slope approximately 0.00686
    R^2 approximately 0.987,

but this is not promoted as a natural scaling law.

## 5. Explicit-landscape coordination barriers

### 5.1 Coarse unilateral-mutation grid

Workflow run: 35472831211
Artifact: 10593711112
Digest: sha256:0ba5140c941d2b8099ff656805b20a1f798288ab5270f7773642fee345d77794

Design:

    interaction strength:
      0, 0.2, 0.5, 1.0

    cost bias:
      -0.08, 0, +0.08

    climate velocity:
      0.02, 0.04, 0.05

    phenology limit:
      1, 2, 4

    unilateral mutation step:
      0.2.

Across 108 cells:

    positive coordination barriers: 52
    persistence-rescue cells:       24.

A persistence-rescue cell means

    local unilateral coevolution endpoint:
      joint extinction

but

    coordinated matched optimum:
      joint persistence.

Interaction dependence was strong:

| interaction strength | barrier cells / 27 | persistence rescues / 27 |
|---:|---:|---:|
| 0.0 | 0 | 0 |
| 0.2 | 12 | 3 |
| 0.5 | 18 | 9 |
| 1.0 | 22 | 12 |

Thus the barrier is absent without interaction and becomes more prevalent as
interaction matching becomes more important.

Persistence rescue was concentrated near demanding tracking regimes rather
than slow climate change:

- at climate velocity 0.02: barriers can occur, but no persistence rescues;
- at 0.04: 15 persistence rescues across the 36-cell slice;
- at 0.05: 9 persistence rescues across the 36-cell slice.

The phenological opportunity axis also matters:

- phenology limit 1: 0 persistence rescues;
- limit 2: 9 rescues;
- limit 4: 15 rescues.

This means a larger phenological option set can increase the opportunity for a
coordination problem: a jointly valuable alternative axis exists, but one
partner moving first breaks matching.

### 5.2 Finer unilateral-mutation resolution

Workflow run: 35472957790
Artifact: 10593706469
Digest: sha256:8129ee6664bf922670f122a10a35d9d9a17ba9a205cf11e5a425d29419561064

The same positive-interaction design was rerun with mutation step 0.1 instead
of 0.2.

Across 81 cells:

    barriers:             57
    persistence rescues:  21.

For comparison, the corresponding positive-interaction subset of the coarse
design had

    barriers:             52
    persistence rescues:  24.

Therefore the explicit-landscape barrier does not disappear with a finer
mutation step.

At the finer step:

| interaction strength | barrier cells / 27 | persistence rescues / 27 |
|---:|---:|---:|
| 0.2 | 17 | 0 |
| 0.5 | 19 | 9 |
| 1.0 | 21 | 12 |

The strongest cell was unchanged in ecological position:

    interaction strength = 0.5
    cost bias             = -0.08
    climate velocity      = 0.05
    phenology limit       = 4.

The deterministic local endpoint was

    species A: migration 0.2, phenology 0
    species B: migration 0.2, phenology 0

with

    local joint low-density growth = -0.88015485281
    local joint persistence        = false.

The coordinated matched optimum at the finer strategy grid was approximately

    migration 0.1
    phenology 0.2

with

    matched joint low-density growth = 0.238272131903
    matched joint persistence        = true.

The accessibility gap was

    1.11842698471.

## 6. One-step mechanism audit

The strongest coarse cell was audited directly in the standard CI rather than
in a one-time pilot.

Workflow run: 35473142861
Job: 105977669568

Resident matched strategy:

    migration = 0.2
    phenology = 0.0.

The best coordinated one-step neighbor was

    migration = 0.2
    phenology = 0.2.

If both species make this move together:

    coordinated joint-payoff gain
    = +1.1150262299432603.

If either species makes the same phenological step alone while its partner
remains at the resident strategy:

    unilateral gain A
    = -1.427318198674544

    unilateral gain B
    = -1.427318198674544

and the resulting interaction mismatch is

    3.188946176164034.

Thus the landscape barrier is not inferred only from distant local/global
optima. The mechanism exists at one mutation step:

> the joint move is strongly beneficial, but either partner moving first is
> strongly deleterious because it temporarily breaks spatial/phenological
> matching.

This is the direct local coordination-gate receipt.

## 7. Main retained spatial interpretation

The explicit landscape adds two results that were not available in the
nonspatial tracking model.

First, phenological capacity expands the speed of environmental movement that
can be tolerated, but the persistence frontier remains spatially dominated.
Near the boundary, migration remains necessary even when phenological
adjustment is available.

Second, making spatial tracking explicit strengthens the ecological consequence
of coordination barriers. Interacting species can become locked into a matched
tracking architecture that drives them toward range-edge compression and
extinction, even though a coordinated shift into a mixed
migration-plus-phenology architecture has positive growth and persists.

The retained causal hierarchy is therefore

    moving climate envelope
    -> finite spatial + phenological tracking capacity
    -> migration-dominant persistence frontier
    -> alternate phenological axis opens
    -> interaction matching creates a coordination gate
    -> unilateral evolution cannot cross
    -> range-edge compression / extinction
    -> coordinated architecture persists.

## 8. Boundary and stochastic-demography robustness

The one-dimensional coordination barrier was also tested against two model
choices that were potential artefacts of the canonical deterministic landscape.

### 8.1 Leaky versus reflecting edges

Across a 108-cell robustness design with boundary retention 0, 0.5, or 1:

| boundary retention | barrier cells / 36 | persistence rescues / 36 | mean accessibility gap |
|---:|---:|---:|---:|
| 0.0 | 29 | 21 | 0.4050 |
| 0.5 | 29 | 21 | 0.3999 |
| 1.0 | 30 | 21 | 0.3947 |

The persistence-rescue count is unchanged across the three boundary rules.
Thus the barrier is not created by reflecting range edges.

### 8.2 Integer stochastic patch demography

The canonical strong barrier cell was then rerun with integer Poisson patch
demography and 128 replicates for each boundary-retention value.

For retention 0, 0.5, and 1:

    local endpoint persistence fraction   = 0
    matched optimum persistence fraction = 1.

The deterministic persistence rescue therefore survives demographic sampling
in this declared cell.

The corresponding artifacts are:

- boundary robustness:
  workflow 35473486671,
  artifact 10593862087,
  sha256 e5bc68c851042b78b14425f3d714446863c4041b5293628a181b254593c8e3da;

- stochastic patch validation:
  workflow 35473605692,
  artifact 10594116842,
  sha256 3947f30e4b157723fdb3c74b10d5efcba88c0c72d14d53e5544553e9265f9f57.

## 9. Claim ceiling

These results do not establish:

- natural frequencies of coordination barriers;
- a universal climate-velocity threshold;
- a universal linear gain in climate tolerance per phenology unit;
- that real partners must evolve identical tracking strategies;
- that explicit density regulation or dispersal follow this exact model;
- that a named plant–pollinator system occupies any sampled cell.

The strongest claims are synthetic mechanism claims under a declared explicit
landscape. Boundary leakage, a long-distance dispersal tail, stochastic local
demography, and two-dimensional route geometry have now been checked as
robustness extensions. The next major step is empirical parameterization of
landscape resistance, movement kernels, and partner-specific tracking costs.
