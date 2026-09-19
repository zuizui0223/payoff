from src.moving_climate_landscape_2d import (
    MovingLandscape2DScenario,
    multiple_vertical_barriers_habitat,
)
from src.moving_landscape_2d_coevolution import (
    audit_landscape_2d_coordination_gate,
    coevolve_moving_landscape_2d_pair,
    landscape_2d_coordination_barrier_diagnostic,
)
from src.spatiotemporal_tracking import TrackingStrategy
from src.tracking_coevolution import SpeciesTrackingParameters


def test_2d_coevolution_substitutions_improve_mutating_species():
    parameters = SpeciesTrackingParameters(
        interaction_strength=0.4,
        migration_cost=0.03,
        phenology_cost=0.03,
        baseline_growth=0.35,
    )
    scenario = MovingLandscape2DScenario(
        width=15,
        height=9,
        climate_velocity=0.025,
        max_abs_phenology_shift=2.0,
        steps=50,
        burn_in=10,
        species_a=parameters,
        species_b=parameters,
    )
    result = coevolve_moving_landscape_2d_pair(
        scenario,
        mutation_step=0.2,
        max_migration_rate=0.8,
        max_phenology_rate=0.8,
        max_cycles=20,
    )
    assert result.converged
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


def test_static_2d_landscape_has_no_tracking_coordination_barrier():
    parameters = SpeciesTrackingParameters(
        interaction_strength=1.0,
        migration_cost=0.05,
        phenology_cost=0.05,
        baseline_growth=0.30,
    )
    scenario = MovingLandscape2DScenario(
        width=15,
        height=9,
        climate_velocity=0.0,
        max_abs_phenology_shift=2.0,
        steps=40,
        burn_in=10,
        species_a=parameters,
        species_b=parameters,
    )
    diagnostic = landscape_2d_coordination_barrier_diagnostic(
        scenario,
        mutation_step=0.2,
        max_migration_rate=0.8,
        max_phenology_rate=0.8,
        max_cycles=20,
    )
    assert diagnostic.local.converged
    assert not diagnostic.barrier
    assert diagnostic.accessibility_gap < 1e-10
    assert diagnostic.local.final.strategy_a == TrackingStrategy(
        0.0,
        0.0,
    )
    assert diagnostic.matched_optimum.strategy_a == TrackingStrategy(
        0.0,
        0.0,
    )


def test_2d_barrier_diagnostic_matched_benchmark_is_not_worse():
    width = 15
    height = 11
    center_y = height // 2
    habitat = multiple_vertical_barriers_habitat(
        width,
        height,
        barriers=(
            (9, 1, center_y + 3),
            (12, 1, center_y - 3),
        ),
    )
    parameters = SpeciesTrackingParameters(
        interaction_strength=0.6,
        migration_cost=0.02,
        phenology_cost=0.08,
        baseline_growth=0.35,
    )
    scenario = MovingLandscape2DScenario(
        width=width,
        height=height,
        climate_velocity=0.03,
        max_abs_phenology_shift=2.0,
        habitat_quality=habitat,
        steps=50,
        burn_in=10,
        species_a=parameters,
        species_b=parameters,
    )
    diagnostic = landscape_2d_coordination_barrier_diagnostic(
        scenario,
        mutation_step=0.2,
        max_migration_rate=0.8,
        max_phenology_rate=0.8,
        max_cycles=20,
    )
    assert diagnostic.local.converged
    assert diagnostic.accessibility_gap >= 0.0
    assert (
        diagnostic.matched_optimum.mean_joint_growth
        + 1e-12
        >= diagnostic.local.final.mean_joint_growth
    )
    assert (
        diagnostic.matched_optimum.strategy_a
        == diagnostic.matched_optimum.strategy_b
    )


def test_2d_gate_audit_detects_declared_sign_pattern_when_present():
    parameters = SpeciesTrackingParameters(
        interaction_strength=1.0,
        migration_cost=0.10,
        phenology_cost=0.02,
        baseline_growth=0.35,
    )
    scenario = MovingLandscape2DScenario(
        width=15,
        height=9,
        climate_velocity=0.035,
        max_abs_phenology_shift=3.0,
        steps=50,
        burn_in=10,
        species_a=parameters,
        species_b=parameters,
    )
    audit = audit_landscape_2d_coordination_gate(
        scenario,
        TrackingStrategy(0.2, 0.0),
        TrackingStrategy(0.2, 0.2),
    )
    # The audit object always reconstructs gains exactly from the four runs.
    assert audit.coordinated_joint_gain == (
        audit.coordinated.mean_joint_growth
        - audit.resident.mean_joint_growth
    )
    assert audit.unilateral_gain_a == (
        audit.unilateral_a.mean_log_growth_a
        - audit.resident.mean_log_growth_a
    )
    assert audit.unilateral_gain_b == (
        audit.unilateral_b.mean_log_growth_b
        - audit.resident.mean_log_growth_b
    )
