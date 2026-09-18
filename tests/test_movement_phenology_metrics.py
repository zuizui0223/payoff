import math

import pytest

from analysis.movement_phenology.metrics import (
    directional_alignment,
    directional_alignment_degrees,
    log_speed_ratio,
    normalized_vector_mismatch,
    payoff_b_reference_interval,
    quadratic_optimum,
    speed_ratio,
    timing_gradient_to_front_velocity,
)


def test_speed_ratio_is_dimensionless_and_unit_invariant():
    assert speed_ratio(60.0, 40.0) == pytest.approx(1.5)
    assert speed_ratio(60_000.0, 40_000.0) == pytest.approx(1.5)
    assert log_speed_ratio(60.0, 40.0) == pytest.approx(math.log(1.5))


def test_perfect_vector_matching_is_zero():
    assert directional_alignment(0.4, 0.4) == pytest.approx(1.0)
    assert normalized_vector_mismatch(50.0, 50.0, 0.4, 0.4) == pytest.approx(0.0)


def test_opposite_directions_are_not_matching_even_at_equal_speed():
    assert directional_alignment(0.0, math.pi) == pytest.approx(-1.0)
    assert directional_alignment_degrees(0.0, 180.0) == pytest.approx(-1.0)
    assert directional_alignment_degrees(350.0, 10.0) == pytest.approx(math.cos(math.radians(340.0)))
    assert normalized_vector_mismatch(50.0, 50.0, 0.0, math.pi) == pytest.approx(2.0)


def test_bad_speeds_are_rejected():
    for animal, environment in [(0, 1), (1, 0), (-1, 2), (2, -1)]:
        with pytest.raises(ValueError):
            speed_ratio(animal, environment)


def test_quadratic_vertex_maps_back_to_positive_ratio():
    q_star, u_star = quadratic_optimum(-2.0, 1.0)
    assert q_star == pytest.approx(1.0)
    assert u_star == pytest.approx(math.e)
    with pytest.raises(ValueError):
        quadratic_optimum(1.0, 0.0)


def test_payoff_b_reference_interval_is_order_one():
    lo, hi = payoff_b_reference_interval()
    assert lo == pytest.approx(1.0)
    assert hi == pytest.approx(1.60611529880277)
    assert lo < hi


def test_timing_gradient_recovers_front_speed_and_direction():
    vx, vy, speed = timing_gradient_to_front_velocity(0.02, 0.0)
    assert vx == pytest.approx(50.0)
    assert vy == pytest.approx(0.0)
    assert speed == pytest.approx(50.0)

    vx, vy, speed = timing_gradient_to_front_velocity(0.03, 0.04)
    assert vx == pytest.approx(12.0)
    assert vy == pytest.approx(16.0)
    assert speed == pytest.approx(20.0)


def test_zero_timing_gradient_has_no_defined_front_velocity():
    with pytest.raises(ValueError):
        timing_gradient_to_front_velocity(0.0, 0.0)
