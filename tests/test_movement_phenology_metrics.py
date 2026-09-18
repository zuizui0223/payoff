import math

import pytest

from analysis.movement_phenology.metrics import (
    directional_alignment,
    log_speed_ratio,
    normalized_vector_mismatch,
    payoff_b_reference_interval,
    quadratic_optimum,
    speed_ratio,
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
