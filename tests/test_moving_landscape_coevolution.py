from src.moving_climate_landscape import MovingLandscapeScenario
from src.moving_landscape_coevolution import (
    coevolve_moving_landscape_pair,
    landscape_coordination_barrier_diagnostic,
    landscape_local_coordination_gate,
)
from src.tracking_coevolution import SpeciesTrackingParameters


def test_landscape_coevolution_substitutions_improve_mutating_species():
    parameters = SpeciesTrackingParameters(
        interaction_strength=0.4,
        migration_cost=0.03,
        phenology_cost=0.03,
        baseline_growth=0.35,
    )
    scenario = MovingLandscapeScenario(
        patches=21,
        spatial_gradient=0.20,
        climate_velocity=0.03,
        max_abs_phenology_shift=2.0,
        carrying_capacity=400.0,
        density_coefficient=0.35,
        steps=60,
        burn_in=15,
        species_a=parameters,
        species_b=parameters,
    )
    result = coevolve_moving_landscape_pair(
        scenario,
        mutation_step=0.2,
        max_migration_rate=0.8,
        max_phenology_rate=0.8,
        max_cycles=20,
    )

    assert len(result.path) > 1
    for previous, current in zip(
        result.path,
        result.path[1:],
    ):
        changed_a = current.strategy_a != previous.strategy_a
        changed_b = current.strategy_b != previous.strategy_b
        assert changed_a != changed_b
        if changed_a:
            assert (
                current.mean_log_growth_a
                > previous.mean_log_growth_a
            )
        else:
            assert (
                current.mean_log_growth_b
                > previous.mean_log_growth_b
            )


def test_static_landscape_has_no_coordination_barrier_when_tracking_only_costs():
    parameters = SpeciesTrackingParameters(
        interaction_strength=1.0,
        migration_cost=0.05,
        phenology_cost=0.05,
        baseline_growth=0.30,
    )
    scenario = MovingLandscapeScenario(
        patches=21,
        climate_velocity=0.0,
        max_abs_phenology_shift=2.0,
        carrying_capacity=400.0,
        density_coefficient=0.30,
        steps=50,
        burn_in=10,
        species_a=parameters,
        species_b=parameters,
    )
    diagnostic = landscape_coordination_barrier_diagnostic(
        scenario,
        mutation_step=0.2,
        max_migration_rate=0.8,
        max_phenology_rate=0.8,
        max_cycles=20,
    )

    assert diagnostic.local.converged
    assert not diagnostic.barrier
    assert diagnostic.accessibility_gap < 1e-10
    assert diagnostic.local.final.strategy_a.migration_rate == 0.0
    assert diagnostic.local.final.strategy_a.phenology_rate == 0.0
    assert diagnostic.matched_optimum.strategy_a.migration_rate == 0.0
    assert diagnostic.matched_optimum.strategy_a.phenology_rate == 0.0


def test_landscape_barrier_diagnostic_returns_matched_global_benchmark():
    parameters = SpeciesTrackingParameters(
        interaction_strength=0.6,
        migration_cost=0.02,
        phenology_cost=0.08,
        baseline_growth=0.35,
    )
    scenario = MovingLandscapeScenario(
        patches=21,
        spatial_gradient=0.20,
        climate_velocity=0.03,
        max_abs_phenology_shift=2.0,
        carrying_capacity=400.0,
        density_coefficient=0.35,
        steps=60,
        burn_in=15,
        species_a=parameters,
        species_b=parameters,
    )
    diagnostic = landscape_coordination_barrier_diagnostic(
        scenario,
        mutation_step=0.2,
        max_migration_rate=0.8,
        max_phenology_rate=0.8,
        max_cycles=20,
    )

    assert diagnostic.local.converged
    assert diagnostic.accessibility_gap >= 0.0
    assert (
        diagnostic.matched_optimum.strategy_a
        == diagnostic.matched_optimum.strategy_b
    )
    assert (
        diagnostic.matched_optimum.mean_joint_growth
        + 1e-12
        >= diagnostic.local.final.mean_joint_growth
    )


def test_local_coordination_gate_is_absent_without_beneficial_joint_step():
    parameters = SpeciesTrackingParameters(
        interaction_strength=1.0,
        migration_cost=0.05,
        phenology_cost=0.05,
        baseline_growth=0.30,
    )
    scenario = MovingLandscapeScenario(
        patches=21,
        climate_velocity=0.0,
        max_abs_phenology_shift=2.0,
        carrying_capacity=400.0,
        density_coefficient=0.30,
        steps=50,
        burn_in=10,
        species_a=parameters,
        species_b=parameters,
    )
    gate = landscape_local_coordination_gate(
        scenario,
        TrackingStrategy(0.0, 0.0),
        mutation_step=0.2,
        max_migration_rate=0.8,
        max_phenology_rate=0.8,
    )
    assert not gate.blocked
    assert gate.coordinated_gain <= 1e-10


def test_local_coordination_gate_blocks_jointly_beneficial_phenology_step():
    parameters = SpeciesTrackingParameters(
        interaction_strength=0.5,
        migration_cost=0.10,
        phenology_cost=0.02,
        baseline_growth=0.30,
    )
    scenario = MovingLandscapeScenario(
        patches=31,
        spatial_gradient=0.20,
        climate_velocity=0.05,
        max_abs_phenology_shift=4.0,
        carrying_capacity=800.0,
        density_coefficient=0.30,
        steps=120,
        burn_in=30,
        species_a=parameters,
        species_b=parameters,
    )
    resident = TrackingStrategy(0.2, 0.0)
    gate = landscape_local_coordination_gate(
        scenario,
        resident,
        mutation_step=0.2,
        max_migration_rate=1.0,
        max_phenology_rate=1.0,
    )

    assert gate.blocked
    assert gate.coordinated_neighbor == TrackingStrategy(0.2, 0.2)
    assert gate.coordinated_gain > 0.5
    assert gate.unilateral_gain_a <= 0.0
    assert gate.unilateral_gain_b <= 0.0
    assert gate.unilateral_mismatch_a > 0.0
    assert gate.unilateral_mismatch_b > 0.0
