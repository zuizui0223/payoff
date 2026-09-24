from math import isclose

import pytest

from src.spatiotemporal_tracking import (
    TrackingScenario,
    TrackingStrategy,
    evolve_tracking_strategy,
    optimize_tracking_strategy,
    simulate_tracking,
    tracking_phase_diagram,
)


def test_abiotic_tracking_depends_on_total_rate_not_axis_when_costs_and_interactions_are_off():
    scenario = TrackingScenario(
        interaction_strength=0.0,
        migration_cost=0.0,
        phenology_cost=0.0,
        joint_cost=0.0,
        steps=120,
        burn_in=20,
    )
    migration = simulate_tracking(
        TrackingStrategy(0.6, 0.0), scenario
    )
    phenology = simulate_tracking(
        TrackingStrategy(0.0, 0.6), scenario
    )

    assert isclose(
        migration.mean_log_growth,
        phenology.mean_log_growth,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )
    assert isclose(
        migration.rms_abiotic_mismatch,
        phenology.rms_abiotic_mismatch,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )


@pytest.mark.parametrize(
    ("partner_spatial_share", "expected_outcome"),
    [(1.0, "migration"), (0.5, "mixed"), (0.0, "phenology")],
)
def test_partner_tracking_axis_selects_corresponding_optimal_response(
    partner_spatial_share,
    expected_outcome,
):
    scenario = TrackingScenario(
        climate_velocity=0.04,
        partner_spatial_share=partner_spatial_share,
        interaction_strength=0.3,
        migration_cost=0.03,
        phenology_cost=0.03,
        baseline_growth=0.3,
        steps=120,
        burn_in=30,
    )
    best = optimize_tracking_strategy(
        scenario, max_rate=1.0, points=21
    )
    assert best.outcome == expected_outcome


def test_environmental_tracking_can_succeed_while_interaction_mismatch_causes_failure():
    scenario = TrackingScenario(
        climate_velocity=0.05,
        partner_spatial_share=1.0,
        interaction_strength=1.5,
        migration_cost=0.01,
        phenology_cost=0.01,
        baseline_growth=0.25,
        steps=150,
        burn_in=30,
    )
    result = simulate_tracking(
        TrackingStrategy(0.0, 0.8), scenario
    )

    assert result.abiotic_only_mean_log_growth > 0.0
    assert result.mean_log_growth < 0.0
    assert result.outcome == "interaction_failure"
    assert result.interaction_limited


def test_adaptive_walk_is_monotone_and_converges_to_partner_matching_axis():
    scenario = TrackingScenario(
        climate_velocity=0.04,
        partner_spatial_share=1.0,
        interaction_strength=0.3,
        migration_cost=0.03,
        phenology_cost=0.03,
        baseline_growth=0.3,
        steps=120,
        burn_in=30,
    )
    result = evolve_tracking_strategy(
        scenario,
        mutation_step=0.1,
        max_rate=1.0,
        max_evolution_steps=30,
    )

    growth = [row.mean_log_growth for row in result.path]
    assert result.converged
    assert all(b > a for a, b in zip(growth, growth[1:]))
    assert result.final.outcome == "migration"


def test_phase_diagram_returns_each_predeclared_design_cell():
    scenario = TrackingScenario(steps=60, burn_in=10)
    rows = tracking_phase_diagram(
        scenario,
        climate_velocities=[0.02, 0.04],
        partner_spatial_shares=[0.0, 0.5, 1.0],
        max_rate=0.8,
        points=9,
    )
    assert len(rows) == 6
    assert {
        row["partner_spatial_share"] for row in rows
    } == {0.0, 0.5, 1.0}


def test_invalid_partner_share_is_rejected():
    with pytest.raises(ValueError):
        TrackingScenario(partner_spatial_share=1.2)
