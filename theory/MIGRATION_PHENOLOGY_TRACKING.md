# Migration–phenology tracking extension

## Question

This lane asks a different question from the existing spatial and temporal
invasion theorems:

**When environmental change can be tracked either by moving in space or by
shifting seasonal timing, when are those axes substitutes, when is a mixed
response favored, and when can abiotic tracking succeed while an interaction
partner is lost?**

The v0.1 implementation is intentionally minimal. It defines a deterministic
benchmark before adding stochastic demography, coevolution, and large
parameter sweeps.

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

Pollinator composition is not the focal stochastic variable in this v0.1
model.

## Important finite-horizon boundary

Under directional environmental change, two interactors that allocate tracking
to different axes can diverge cumulatively. Consequently the interaction
penalty can grow with time.

The simulation horizon is therefore part of the declared design. v0.1 is a
finite-horizon tracking experiment, not a stationary-equilibrium theorem.

A later version can add bounded seasonal forcing, moving climatic envelopes,
or partner coevolution to ask when long-run stationary regimes exist.

## Scaling path

The intended progression is:

1. deterministic two-axis benchmark;
2. stochastic environmental velocity and partner lag;
3. mutation-selection population occupancy over the strategy lattice;
4. explicit density and extinction;
5. partner coevolution;
6. spatial landscape with local climatic velocity;
7. large replicated parameter sweeps.

Only stages 3-7 justify the very large run counts discussed for a future
month-scale simulation programme.

## Claim ceiling

The current implementation supports mechanism exploration and code-level
predictions about the declared model. It does not show that migration and
phenology are universally substitutable in nature, that the partner spatial
share is directly measurable as one scalar, or that any natural system occupies
one of the synthetic phase regions.
