from math import isclose, log

import pytest

from src.closed_loop_tracking import (
    classify_closed_loop_stability,
    feedback_gain_to_phenology_rate,
    minimum_cost_feedback_allocation,
    phenology_rate_to_feedback_gain,
    route_relaxation_to_step_feedback,
    simulate_closed_loop_tracking,
    unconstrained_optimal_feedback,
)


def test_phenology_rate_feedback_round_trip():
    for rate in (0.0, 0.1, 0.5, 1.0, 2.0):
        q = phenology_rate_to_feedback_gain(rate)
        recovered = feedback_gain_to_phenology_rate(q)
        assert isclose(
            recovered,
            rate,
            rel_tol=1e-12,
            abs_tol=1e-12,
        )


def test_stability_classes_follow_total_feedback_gain():
    assert classify_closed_loop_stability(0.0) == "no_feedback"
    assert classify_closed_loop_stability(0.5) == "stable_monotone"
    assert classify_closed_loop_stability(1.0) == "deadbeat_one_step"
    assert classify_closed_loop_stability(1.5) == "stable_oscillatory"
    assert classify_closed_loop_stability(2.0) == "neutral_two_cycle"
    assert classify_closed_loop_stability(2.5) == "oscillatory_unstable"


def test_stable_simulation_converges_to_exact_equilibrium():
    result = simulate_closed_loop_tracking(
        residual_forcing=0.3,
        movement_feedback_gain=0.4,
        phenology_feedback_gain=0.2,
        initial_mismatch=-1.0,
        steps=300,
        burn_in=200,
    )
    expected = 0.3 / 0.6

    assert result.stable
    assert result.stability_class == "stable_monotone"
    assert result.theoretical_equilibrium_mismatch == pytest.approx(
        expected
    )
    assert result.final_mismatch == pytest.approx(
        expected,
        rel=1e-10,
        abs=1e-10,
    )
    assert result.mean_mismatch == pytest.approx(
        expected,
        rel=1e-8,
        abs=1e-8,
    )


def test_space_time_feedback_is_exactly_substitutable_at_fixed_total_gain():
    movement_heavy = simulate_closed_loop_tracking(
        residual_forcing=0.2,
        movement_feedback_gain=0.7,
        phenology_feedback_gain=0.1,
        initial_mismatch=1.2,
        steps=80,
        burn_in=10,
    )
    phenology_heavy = simulate_closed_loop_tracking(
        residual_forcing=0.2,
        movement_feedback_gain=0.2,
        phenology_feedback_gain=0.6,
        initial_mismatch=1.2,
        steps=80,
        burn_in=10,
    )

    assert movement_heavy.total_feedback_gain == pytest.approx(0.8)
    assert phenology_heavy.total_feedback_gain == pytest.approx(0.8)
    assert movement_heavy.final_mismatch == pytest.approx(
        phenology_heavy.final_mismatch,
        rel=1e-12,
        abs=1e-12,
    )
    assert movement_heavy.rms_mismatch == pytest.approx(
        phenology_heavy.rms_mismatch,
        rel=1e-12,
        abs=1e-12,
    )


def test_total_gain_above_one_produces_stable_oscillatory_tracking():
    result = simulate_closed_loop_tracking(
        residual_forcing=0.1,
        movement_feedback_gain=0.9,
        phenology_feedback_gain=0.6,
        initial_mismatch=2.0,
        steps=200,
        burn_in=100,
    )
    assert result.stable
    assert result.stability_class == "stable_oscillatory"
    assert result.multiplier == pytest.approx(-0.5)
    assert result.final_mismatch == pytest.approx(
        0.1 / 1.5,
        rel=1e-10,
        abs=1e-10,
    )


def test_total_gain_above_two_is_unstable():
    result = simulate_closed_loop_tracking(
        residual_forcing=0.0,
        movement_feedback_gain=1.2,
        phenology_feedback_gain=1.1,
        initial_mismatch=1.0,
        steps=20,
        burn_in=5,
    )
    assert not result.stable
    assert result.stability_class == "oscillatory_unstable"
    assert abs(result.final_mismatch) > 1.0


def test_fixed_total_feedback_allocation_minimizes_quadratic_cost():
    allocation = minimum_cost_feedback_allocation(
        0.8,
        movement_cost=4.0,
        phenology_cost=1.0,
    )
    assert allocation.movement_feedback_gain == pytest.approx(0.16)
    assert allocation.phenology_feedback_gain == pytest.approx(0.64)

    # Same total gain but equal split must cost more when movement is expensive.
    equal_cost = 0.5 * (
        4.0 * 0.4 * 0.4
        + 1.0 * 0.4 * 0.4
    )
    assert allocation.total_quadratic_cost < equal_cost


def test_unconstrained_feedback_optimum_satisfies_closed_form_first_order_condition():
    optimum = unconstrained_optimal_feedback(
        residual_forcing=0.2,
        mismatch_strength=2.0,
        movement_cost=4.0,
        phenology_cost=1.0,
    )
    c_eff = 4.0 * 1.0 / 5.0
    expected_total = (
        2.0 * 0.2 * 0.2 / c_eff
    ) ** 0.25

    assert optimum.total_feedback_gain == pytest.approx(expected_total)
    assert optimum.movement_feedback_gain + optimum.phenology_feedback_gain == pytest.approx(
        expected_total
    )
    assert optimum.stability_feasible


def test_zero_residual_forcing_has_zero_optimal_feedback():
    optimum = unconstrained_optimal_feedback(
        residual_forcing=0.0,
        mismatch_strength=1.0,
        movement_cost=1.0,
        phenology_cost=1.0,
    )
    assert optimum.total_feedback_gain == 0.0
    assert optimum.objective_value == 0.0
    assert optimum.equilibrium_mismatch == 0.0


def test_route_relaxation_maps_to_step_feedback_under_local_exponential_bridge():
    q = route_relaxation_to_step_feedback(
        local_fractional_relaxation_per_distance=0.1,
        forward_distance_per_step=5.0,
    )
    assert q == pytest.approx(1.0 - __import__("math").exp(-0.5))
    assert feedback_gain_to_phenology_rate(q) == pytest.approx(0.5)


def test_expensive_movement_shifts_fixed_total_feedback_toward_phenology():
    cheap_movement = minimum_cost_feedback_allocation(
        0.8,
        movement_cost=1.0,
        phenology_cost=4.0,
    )
    expensive_movement = minimum_cost_feedback_allocation(
        0.8,
        movement_cost=4.0,
        phenology_cost=1.0,
    )

    assert cheap_movement.movement_feedback_gain > cheap_movement.phenology_feedback_gain
    assert expensive_movement.movement_feedback_gain < expensive_movement.phenology_feedback_gain
