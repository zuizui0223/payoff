from math import isclose

from src.spatiotemporal_tracking import TrackingScenario
from src.tracking_mutation_selection import (
    StrategyLattice,
    replicator_mutator_step,
    stationary_tracking_occupancy,
    symmetric_mutation_step,
)


def test_neutral_symmetric_mutation_preserves_uniform_distribution():
    lattice = StrategyLattice(max_rate=1.0, points=5)
    uniform = tuple(1.0 / lattice.size for _ in range(lattice.size))
    mutated = symmetric_mutation_step(
        uniform, lattice, mutation_rate=0.4
    )
    for observed, expected in zip(mutated, uniform):
        assert isclose(
            observed,
            expected,
            rel_tol=1e-12,
            abs_tol=1e-12,
        )


def test_neutral_stationary_occupancy_is_uniform():
    scenario = TrackingScenario(
        climate_velocity=0.04,
        steps=80,
        burn_in=20,
    )
    lattice = StrategyLattice(max_rate=1.0, points=5)
    result = stationary_tracking_occupancy(
        scenario,
        lattice,
        selection_strength=0.0,
        mutation_rate=0.2,
    )
    expected = 1.0 / lattice.size
    assert result.converged
    assert all(
        isclose(
            probability,
            expected,
            rel_tol=1e-10,
            abs_tol=1e-10,
        )
        for probability in result.probabilities
    )


def test_selection_changes_occupancy_toward_high_growth_region():
    scenario = TrackingScenario(
        climate_velocity=0.04,
        partner_spatial_share=1.0,
        interaction_strength=0.35,
        migration_cost=0.03,
        phenology_cost=0.03,
        baseline_growth=0.3,
        steps=100,
        burn_in=20,
    )
    lattice = StrategyLattice(max_rate=1.0, points=7)
    result = stationary_tracking_occupancy(
        scenario,
        lattice,
        selection_strength=30.0,
        mutation_rate=0.03,
    )
    summary = result.summary()

    assert result.converged
    assert summary["mean_migration_rate"] > summary["mean_phenology_rate"]
    assert summary["top_probability"] > 1.0 / lattice.size


def test_partner_axis_rotates_stationary_tracking_allocation():
    common = dict(
        climate_velocity=0.04,
        interaction_strength=0.35,
        migration_cost=0.03,
        phenology_cost=0.03,
        baseline_growth=0.3,
        steps=100,
        burn_in=20,
    )
    lattice = StrategyLattice(max_rate=1.0, points=7)

    spatial = stationary_tracking_occupancy(
        TrackingScenario(
            partner_spatial_share=1.0,
            **common,
        ),
        lattice,
        selection_strength=25.0,
        mutation_rate=0.04,
    ).summary()
    temporal = stationary_tracking_occupancy(
        TrackingScenario(
            partner_spatial_share=0.0,
            **common,
        ),
        lattice,
        selection_strength=25.0,
        mutation_rate=0.04,
    ).summary()

    assert spatial["mean_migration_share"] > 0.5
    assert temporal["mean_migration_share"] < 0.5


def test_replicator_mutator_step_preserves_total_mass():
    lattice = StrategyLattice(max_rate=1.0, points=3)
    probabilities = tuple(
        1.0 / lattice.size for _ in range(lattice.size)
    )
    growth = tuple(float(i) / 10.0 for i in range(lattice.size))
    updated = replicator_mutator_step(
        probabilities,
        growth,
        lattice,
        selection_strength=5.0,
        mutation_rate=0.2,
    )
    assert isclose(sum(updated), 1.0, abs_tol=1e-12)
    assert all(value >= 0.0 for value in updated)


def test_summary_reports_interaction_failure_mass_when_present():
    scenario = TrackingScenario(
        climate_velocity=0.06,
        partner_spatial_share=1.0,
        interaction_strength=1.5,
        migration_cost=0.01,
        phenology_cost=0.01,
        baseline_growth=0.2,
        steps=120,
        burn_in=20,
    )
    lattice = StrategyLattice(max_rate=1.0, points=5)
    result = stationary_tracking_occupancy(
        scenario,
        lattice,
        selection_strength=2.0,
        mutation_rate=0.2,
    )
    summary = result.summary()
    assert 0.0 <= summary["interaction_failure_mass"] <= 1.0
