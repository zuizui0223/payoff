# Migration–phenology tracking extension

## Question

This lane asks a different question from the existing spatial and temporal
invasion theorems:

**When environmental change can be tracked either by moving in space or by
shifting seasonal timing, when are those axes substitutes, when is a mixed
response favored, and when can abiotic tracking succeed while an interaction
partner is lost?**

The current implementation now spans deterministic strategy payoffs,
mutation-selection occupancy, finite-N weak-mutation evolution, two-species
coevolution, seed-explicit stochastic forcing, density-regulated demographic
extinction, explicit one- and two-dimensional moving landscapes, stochastic
integer patch demography, heterogeneous connectivity geometry, and
reproducible sharded sweeps.

## Shared moving demand

Let environmental demand move at constant velocity:

    D_t = v t.

The focal lineage can respond through spatial displacement x and phenological
shift z. A conversion scale s puts both responses on one common
climate-equivalent coordinate:

    y = x + s z.

The abiotic mismatch is

    e = D_t - y.

This is the key substitution assumption: one unit of spatial tracking and one
converted unit of phenological tracking can close the same environmental
mismatch.

## Two heritable tracking rates

Let m be the migration/spatial tracking rate and h the phenological tracking
rate. Their total response capacity is m+h. The fraction of current mismatch
closed in one generation is

    q = 1 - exp[-(m+h)].

The correction is partitioned between the two axes according to their relative
rates:

    x_(t+1) = x_t + q e_t m/(m+h),

    z_(t+1) = z_t + q e_t h/[(m+h)s].

Therefore, when costs and interactions are absent, strategies with the same
m+h have the same abiotic tracking dynamics. This is a direct unit test in the
implementation.

## Interaction partner

The partner experiences the same moving demand but can partition its tracking
differently. Let a be its spatial share and f its total tracking fraction:

    partner demand = f D_t - lag,

    x_partner = a * partner demand,

    s z_partner = (1-a) * partner demand.

The focal lineage can therefore track the abiotic environment successfully but
separate from the partner in space, phenology, or both.

This is the new biological quantity absent from a pure moving-optimum model:
**axis mismatch between interactors**.

## Payoff

Per-generation Malthusian payoff is

    g = g0
        - 0.5 A e^2
        - 0.5 I[(x-x_partner)^2 + s^2(z-z_partner)^2]
        - c_m m^2
        - c_h h^2
        - c_mh m h.

The implementation also records the abiotic-only payoff with the interaction
term removed. This creates a falsifiable category:

    abiotic-only growth >= 0
    but full growth < 0

which is labeled interaction_failure.

Thus a lineage can solve the climate problem and still fail because it solved
it on a different axis from its partner.

## Outcomes

The baseline classifier returns:

- migration: viable and at least two thirds of tracking rate lies on the
  spatial axis;
- phenology: viable and at least two thirds lies on the phenological axis;
- mixed: viable and neither axis dominates;
- stasis: viable with effectively zero tracking;
- interaction_failure: abiotic-only payoff is viable but partner mismatch
  makes full payoff negative;
- failure: even the abiotic-only payoff is negative.

The dominance cutoff is a reporting convention, not a biological threshold.

## Evolutionary accessibility

The function evolve_tracking_strategy implements a deterministic rare-mutation
adaptive walk. At each evolutionary step the resident is compared against all
one-step axial and diagonal mutants. The best strictly improving mutant fixes.

This is an accessibility benchmark. It is not yet a Moran process, explicit
finite population, or quantitative-genetic diffusion.

The full grid optimizer is kept separately so local accessibility and global
payoff optimum do not become the same estimand.

## Population mutation-selection occupancy

The deterministic payoff surface is promoted to a population distribution on a
regular migration x phenology strategy lattice.

Selection uses exponential payoff weighting,

    w_i = exp(beta g_i),

followed by symmetric mutation proposals in the four axial lattice directions.
Each directional proposal has probability mu/4. At a boundary, an invalid
proposal remains in the parental state.

That boundary rule is deliberate: the mutation matrix is symmetric and doubly
stochastic. Therefore beta=0 has an exact uniform stationary distribution over
the strategy lattice rather than an artificial edge bias.

The stationary occupancy reports:

- mean migration and phenology rates;
- mean migration share;
- stationary mean growth;
- entropy and effective number of occupied strategies;
- highest-mass strategy;
- stationary mass in interaction-failure and abiotic-failure states.

This layer separates "which point maximizes payoff?" from "where does a
mutation-selection population spend its time?"

## Finite-N weak-mutation occupancy

The strategy lattice also has a finite-population weak-mutation interpretation
that is distinct from the recurrent-mutation replicator-mutator layer.

Assume a monomorphic resident strategy i and a one-step mutant j. Treat the
declared tracking payoff g as a frequency-independent Malthusian score and use

    r_ji = exp[beta (g_j - g_i)]

as the mutant/resident relative fitness in a Moran process of size N.

The exact one-mutant fixation probability is

    rho(j|i)
    = [1 - exp(-beta Delta g)]
      / [1 - exp(-N beta Delta g)],

with neutral limit 1/N.

For symmetric nearest-neighbor mutation proposals,

    rho(j|i) / rho(i|j)
    = exp[beta (N-1)(g_j-g_i)],

so detailed balance gives the exact stationary law

    Pi_i
    proportional to
    exp[beta (N-1) g_i].

This is the tracking analogue of PAYOFF's existing Gibbs-form weak-mutation
architecture occupancy. Population size acts as an inverse-temperature
multiplier:

- small N spreads occupancy across multiple migration/phenology strategies;
- large N concentrates occupancy near high-payoff tracking strategies;
- beta=0 gives exact uniform occupancy over the symmetric lattice.

The implementation includes both the exact stationary distribution and an
explicit stochastic substitution chain. Therefore deterministic optimum,
recurrent-mutation occupancy, and finite-N weak-mutation occupancy remain
separate estimands rather than being collapsed into one "evolved strategy."

The finite-N phase sweep is

    python scripts/migration_phenology_finite_occupancy.py

## Two-species coevolution and coordination barriers

A second implementation lets both interacting lineages carry their own
heritable migration and phenology tracking rates. Both see the same moving
environment, and interaction loss depends on their spatial and phenological
separation.

Evolution proceeds as alternating rare substitutions:

    mutate A while B is fixed
    -> best improving A mutant fixes
    -> mutate B while new A is fixed
    -> best improving B mutant fixes.

The first CI-tested result exposes an important accessibility effect. When
interaction matching is sufficiently important, two lineages can remain on a
matched mixed strategy even when both species have the same intrinsic cost
bias toward one axis. A unilateral move toward the cheaper axis temporarily
creates partner mismatch and can be selected against.

Thus the model contains a direct analogue of PAYOFF's broader distinction
between global value and local accessibility:

    jointly better matched architecture
    !=
    architecture reachable by unilateral small mutations.

This is a coevolutionary coordination barrier, not a claim that mixed tracking
is generally stable in nature. Its phase boundary still needs systematic
mapping.

## Stochastic forcing and scalable sweeps

The stochastic layer adds:

    noisy climate increments,
    time-varying partner spatial share,
    partner-demand noise.

Every realization is seed-explicit. Strategy comparisons use common random
numbers: all strategies within one parameter point are evaluated against the
same environmental realizations.

Large sweeps are index-addressable and shardable:

    sample_index % shard_count == shard_index.

This makes results independent of worker count and execution order. The CLI
also supports resume and dry-run workload accounting:

    python scripts/migration_phenology_stochastic_sweep.py --dry-run

The counted work unit is one ecological update of one strategy in one
replicate. For S parameter points, G grid points per axis, R stochastic
replicates and T ecological steps, planned work is

    S * G^2 * R * T.

This is the layer that can legitimately be scaled into a multi-day or
month-scale computational experiment.

## Density regulation and demographic extinction

The tracking payoff is now transported into explicit integer population
dynamics rather than interpreting negative mean growth as extinction by
definition.

For abundance N_t, the current demographic layer uses

    E[N_(t+1) | N_t]
    = N_t * exp[g_t - d N_t / K],

followed by Poisson demographic sampling.

Here:

- g_t is the same low-density Malthusian tracking payoff defined above;
- d is the density-regulation coefficient;
- K is the abundance scale;
- zero abundance is absorbing.

Thus the causal chain is explicit:

    environmental movement
    -> spatial/phenological mismatch
    -> interaction mismatch
    -> low-density growth
    -> density-regulated integer abundance
    -> persistence or extinction.

No new hidden "extinction score" is introduced.

For the two-species coevolution model, joint-system persistence is measured
until the first partner extinction. The current model intentionally stops there
because post-partner-loss growth has not yet been specified. It therefore
estimates persistence of the interacting pair, not secondary dynamics after
one partner disappears.

The demographic coordination-barrier comparison holds the ecological scenario,
population design and replicate seeds fixed while contrasting:

    locally accessible coevolution endpoint

against

    coordinated matched optimum.

This yields two linked quantities:

    accessibility gap
    = matched mean payoff - local mean payoff,

and

    persistence gain
    = matched joint-persistence fraction
      - local joint-persistence fraction.

A coordination barrier can therefore be classified as demographically cryptic
or as carrying a measurable persistence cost.

The dedicated sweep is

    python scripts/migration_phenology_population_barrier_sweep.py

and can be sharded across the interaction-strength x cost-bias x climate-speed
design.

## Phase diagram

The first sweep varies:

- climate velocity v;
- partner spatial share a.

Each design cell is optimized over m x h and classified into migration,
phenology, mixed, stasis, interaction failure, or failure.

The command-line entry point is:

    python scripts/migration_phenology_phase_sweep.py

The default output is:

    outputs/migration_phenology_phase_sweep.csv

## Relationship to existing PAYOFF space and time theory

The existing spatial PAYOFF layer transports local architecture margins through
migration on a patch graph. The temporal PAYOFF layer studies Floquet growth
under seasonally changing patch quality.

This extension is different. Migration and phenological change are themselves
heritable response axes competing to close one moving ecological mismatch.

The old theory therefore asks how a given architecture is transported through
space and time. This extension asks which spatial-versus-temporal tracking
architecture is selected in the first place.

## Relationship to izu-core

This model must not be used as another version of conditional island response
geometry.

The boundary is:

    izu-core:
    plant starting state x realized pollinator community
    -> response branch after community reorganization.

    PAYOFF migration-phenology:
    spatial tracking x phenological tracking
    -> adaptive route under a moving environment
    -> possible partner-axis mismatch.

Pollinator composition is not the focal stochastic variable in this model.

## Important finite-horizon boundary

Under directional environmental change, two interactors that allocate tracking
to different axes can diverge cumulatively. Consequently the interaction
penalty can grow with time.

The simulation horizon is therefore part of the declared design. The current
tracking and coevolution layers are finite-horizon ecological experiments, not
stationary-equilibrium theorems for directional climate change.

Bounded seasonal forcing, moving climatic envelopes, and explicit demographic
regulation remain routes to genuinely stationary long-run ecological regimes.

## Scaling path

Current progression:

1. deterministic two-axis benchmark — implemented;
2. stochastic environmental forcing — implemented;
3. mutation-selection population occupancy over the strategy lattice —
   implemented;
4. partner coevolution — implemented as alternating rare substitutions;
5. reproducible sharded large replicated parameter sweeps — implemented;
6. density regulation and demographic extinction — implemented;
7. finite-N weak-mutation evolutionary drift and exact occupancy — implemented;
8. one-dimensional explicit moving landscapes — implemented;
9. stochastic integer patch demography and alternative dispersal/boundary
   conditions — implemented;
10. two-dimensional habitat connectivity and route geometry — implemented;
11. one- and two-dimensional coevolutionary coordination barriers —
    implemented and resolution-checked;
12. anisotropic movement kernels and algebraic observation-to-parameter maps —
    implemented; named-system calibration remains pending.

The implemented layers already provide a reproducible route to very large run
counts. The next major upgrade is empirical parameterization rather than merely
adding more synthetic computational scale.

## Explicit moving-climate landscape

The spatial extension now makes range tracking explicit rather than treating
migration as a direct climate-equivalent displacement.

Patches have fixed coordinates x_j. Environmental demand moves as

    D_t = v t,

and local mismatch for a lineage with phenology z is

    e_j(t)
    = D_t - g x_j - s z_t,

where g converts spatial position into climate-equivalent units and s converts
phenological shift into the same units.

Spatial tracking emerges from two operations:

1. local reproduction is higher in better matched patches;
2. offspring disperse conservatively between neighboring patches.

For migration parameter m, the per-generation nearest-neighbor dispersal
fraction is

    q_m = 1 - exp(-m).

Reflecting boundaries conserve abundance under movement alone. Therefore a
range centroid moves only through the combination of environmental selection
and dispersal; the model does not push populations toward the moving climate
optimum by construction.

Phenology changes from the abundance-weighted residual mismatch with response

    q_h = 1 - exp(-h),

but is clipped to

    |z| <= z_max.

The phenological bound is biologically important. Without it, indefinite
directional climate change could always be absorbed by indefinite calendar
shift. With a finite seasonal window, phenological tracking can saturate and
force additional tracking into spatial redistribution.

For two interacting species the climate-equivalent interaction distance is

    M^2
    = [g(xbar_A-xbar_B)]^2
      + [s(z_A-z_B)]^2.

This preserves the previous nonspatial interaction geometry while allowing
xbar to emerge from an explicit abundance distribution.

The spatial layer keeps evolutionary fitness and density regulation separate.
Patch-level low-density fitness is

    g0_j
    = baseline
      - architecture cost
      - abiotic mismatch penalty
      - interaction mismatch penalty,

while realized demographic growth is

    g_j
    = g0_j - d N/K.

Reproduction uses g_j, so density controls abundance. Strategy optimization and
coevolution use the abundance-weighted low-density g0_j, not g_j. This prevents
a spurious evolutionary incentive to pay unnecessary tracking costs merely to
depress abundance and relax competition. A regression test freezes this
separation in static environments.

The landscape layer therefore distinguishes four failure modes that were
collapsed in the abstract model:

    insufficient phenological response,
    insufficient spatial redistribution,
    interaction-axis mismatch,
    and range-edge compression when the moving envelope approaches the
    landscape boundary.

The deterministic expected-abundance layer remains the evolutionary mechanism
benchmark, and a separate stochastic integer patch-demography layer provides
Poisson demographic realizations. Boundary leakage and a long-distance
dispersal tail have also been checked as robustness extensions.

The phase sweep is

    python scripts/migration_phenology_moving_landscape.py

and maps climate velocity x phenological shift limit to the best matched
migration/phenology tracking architecture.

## Two-dimensional habitat connectivity

The moving-landscape layer now has an explicit two-dimensional extension.
Patches occupy a rectangular grid and climate moves along a declared spatial
direction. Local mismatch remains

    e_ij(t)
    = D_t - g c_ij - s z_t,

where c_ij is the cell coordinate projected onto the climate-motion axis.

Dispersal occurs among the four cardinal neighbors. Habitat quality q_ij lies
in [0,1]:

    q_ij = 0
        -> blocked habitat / barrier cell,

    0 < q_ij <= 1
        -> local carrying capacity
           K_ij = q_ij K_local.

As in the one-dimensional model, low-density growth is the evolutionary
fitness estimand. Local density regulation changes abundance but does not
create an indirect payoff reward for costly tracking.

The scientific reason for using two dimensions is connectivity geometry rather
than dimensionality by itself. Vertical habitat walls can contain finite gaps,
and multiple walls can create routes with different path lengths:

    open:
        no wall,

    straight:
        successive gaps aligned with the climate axis,

    shifted:
        gaps displaced from the climate axis but aligned with each other,

    zigzag:
        successive gaps displaced in opposite transverse directions.

The last case creates a genuine spatial detour that cannot be represented by a
one-dimensional projection.

This allows a direct test of **space-time substitution under fragmentation**:

    low phenological capacity
        -> moving climate must be tracked mainly through spatial redistribution,

    high phenological capacity
        -> some climate displacement can be absorbed in time,
           reducing the amount or urgency of corridor crossing.

The declared diagnostic is not merely whether narrow corridors reduce
movement. That effect is mechanically expected. The higher-value comparison
is whether increasing phenological capacity changes:

- the low-density growth penalty caused by route geometry;
- the climate-velocity persistence frontier;
- the spatial fraction that must cross a barrier;
- the optimal migration-versus-phenology allocation.

The two-dimensional layer also carries the same coevolutionary accessibility
distinction as the one-dimensional model. Alternating unilateral substitutions
are compared with a coordinated matched-pair optimum, and a direct gate audit
can test

    coordinated joint gain > 0

while

    unilateral gain of species A < 0
    unilateral gain of species B < 0.

Therefore habitat connectivity can be studied separately from, and jointly
with, interaction-mediated coordination barriers.

The present 2D implementation is still a synthetic regular grid. It does not
yet claim realistic landscape resistance, species-specific habitat maps,
anisotropic dispersal estimated from movement data, or empirical corridor
widths.

The canonical two-dimensional results are frozen in
[../docs/PAYOFF_B_2D_CONNECTIVITY_RESULTS_20260920.md](../docs/PAYOFF_B_2D_CONNECTIVITY_RESULTS_20260920.md).
They retain four results:

1. phenological capacity buffers the low-density growth cost of zigzag spatial
   routes, reducing the sampled open-to-zigzag penalty by about 83% from
   z_max=0 to z_max=4;
2. the temporal bypass has a finite capacity ceiling, after which migration
   re-enters the optimal tracking strategy;
3. positive-interaction 2D coevolution retains 22/24 barriers and 21/24
   persistence rescues at mutation step 0.1 across open, straight and zigzag
   geometries;
4. the canonical gate survives an explicit distribution-level overlap penalty
   and partner-specific cost asymmetry.

The partner-asymmetry experiments further separate two regimes. At moderate
forcing, interaction synchronizes otherwise quantitatively different partner
tracking responses while persistence remains possible. At stronger forcing,
the same synchronization collapses onto a locally accessible migration-only
attractor and becomes maladaptive.

The temporal-buffering result is not restricted to isotropic four-neighbor
movement. When transverse dispersal weight is reduced from 1 to 0.1 relative
to the climate-axis direction, the sampled zigzag growth penalty becomes more
negative without phenology, but phenology limit 4 still reduces penalty
magnitude by about 75-76% across all sampled anisotropy levels. The sampled
design shows growth-cost buffering, not an anisotropy-specific persistence
rescue.

An empirical handoff now provides exact inverse maps for the directly
identifiable subset of tracking parameters under the declared kernel:
movement-component variances -> migration rate and anisotropy; environmental
wave speed x spatial gradient -> climate velocity; first-order residual
correction -> phenology response rate. A separate matched-contrast design
identifies baseline growth, abiotic and interaction mismatch strengths, and
quadratic tracking costs. These maps are model-conditional and do not yet
constitute a named-system calibration.

## Frozen synthetic evidence

The first model results are frozen in
[../docs/PAYOFF_B_TRACKING_SYNTHETIC_RESULTS_20260920.md](../docs/PAYOFF_B_TRACKING_SYNTHETIC_RESULTS_20260920.md).

The retained findings are:

1. coordination barriers occupy a substantial region of the declared synthetic
   ecological grid;
2. their demographic consequences are usually small away from persistence
   transitions;
3. an independent higher-replication demographic rerun supports a
   **demographic visibility window**, not the large cell-level effects seen in
   the initial pilot;
4. finite-N drift can cross a deterministic coordination barrier;
5. in the sampled drift regime, crossing does not improve long-run mean joint
   growth because drift also broadens occupancy into lower-payoff states.

The resulting hierarchy is therefore

    coordinated value
    != local accessibility
    != demographic visibility
    != finite-N barrier crossing
    != long-run payoff improvement.

That sequence is now the main theoretical reason to keep optimization,
accessibility, persistence, and stochastic evolutionary occupancy as separate
estimands.

The canonical explicit-landscape results are frozen separately in
[../docs/PAYOFF_B_MOVING_LANDSCAPE_RESULTS_20260920.md](../docs/PAYOFF_B_MOVING_LANDSCAPE_RESULTS_20260920.md).

The spatial layer adds three further separations.

First,

    phenological capacity
    != replacement of spatial tracking.

Across the canonical finite landscape, increasing the allowed phenological
shift expands the sampled persistence frontier from climate velocity 0.030 to
0.065, but every frontier strategy remains migration-dominant. The same six
frontier brackets are recovered on 7 x 7 and 11 x 11 strategy grids.

Second,

    coordination barrier
    != endpoint interaction mismatch.

At both the local endpoint and the coordinated optimum the two species can be
perfectly matched to one another. The barrier is transient: a unilateral move
toward the alternative tracking architecture creates mismatch before the other
species follows.

Third,

    coordinated persistence
    != unilateral evolutionary accessibility.

In the explicit landscape, a representative local endpoint at
(migration,phenology)=(0.2,0) has negative joint low-density growth and
collapses against the range edge, while a coordinated mixed strategy has
positive low-density growth and persists. The one-step audit closes the
mechanism: moving both partners together gives payoff gain +1.115, whereas
either partner moving alone gives approximately -1.427 because interaction
mismatch increases to approximately 3.189.

The expanded hierarchy is therefore

    tracking capacity
    != chosen tracking architecture
    != jointly valuable architecture
    != unilaterally accessible architecture
    != population persistence.

## Claim ceiling

The current implementation supports mechanism exploration and code-level
predictions about the declared model. It does not show that migration and
phenology are universally substitutable in nature, that the partner spatial
share is directly measurable as one scalar, or that any natural system occupies
one of the synthetic phase regions.
