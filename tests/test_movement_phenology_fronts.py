import math

import pytest

from analysis.movement_phenology.fronts import (
    compare_timing_fronts,
    front_velocity_from_timing_gradient,
    normalized_phase_drift_from_speed_ratio,
    normalized_phase_drift_from_timing_gradients,
)


def test_one_dimensional_timing_gradient_recovers_front_speed():
    # T=x/50 => dT/dx=1/50 day/km, so the front moves 50 km/day.
    v = front_velocity_from_timing_gradient(1 / 50, 0)
    assert v.vx == pytest.approx(50)
    assert v.vy == pytest.approx(0)
    assert v.speed == pytest.approx(50)
    assert v.angle_rad == pytest.approx(0)


def test_diagonal_timing_gradient_recovers_speed_and_direction():
    c = 40.0
    g = 1 / (c * math.sqrt(2))
    v = front_velocity_from_timing_gradient(g, g)
    assert v.speed == pytest.approx(c)
    assert v.vx == pytest.approx(c / math.sqrt(2))
    assert v.vy == pytest.approx(c / math.sqrt(2))
    assert v.angle_rad == pytest.approx(math.pi / 4)


def test_equal_timing_fronts_are_perfectly_matched():
    m = compare_timing_fronts(0.02, 0.01, 0.02, 0.01)
    assert m.speed_ratio == pytest.approx(1)
    assert m.log_speed_ratio == pytest.approx(0)
    assert m.alignment == pytest.approx(1)
    assert m.vector_mismatch == pytest.approx(0)


def test_faster_parallel_animal_front_has_expected_ratio():
    # Smaller timing gradient means faster front.
    m = compare_timing_fronts(0.01, 0, 0.02, 0)
    assert m.speed_ratio == pytest.approx(2)
    assert m.alignment == pytest.approx(1)
    assert m.vector_mismatch == pytest.approx(1)


def test_opposite_front_directions_are_penalized():
    m = compare_timing_fronts(-0.02, 0, 0.02, 0)
    assert m.speed_ratio == pytest.approx(1)
    assert m.alignment == pytest.approx(-1)
    assert m.vector_mismatch == pytest.approx(2)


def test_zero_gradient_is_not_a_finite_front():
    with pytest.raises(ValueError):
        front_velocity_from_timing_gradient(0, 0)



def test_constant_phase_offset_has_zero_spatial_phase_drift():
    # A constant timing offset changes intercept, not the timing gradient.
    d = normalized_phase_drift_from_timing_gradients(0.02, 0.01, 0.02, 0.01)
    assert d == pytest.approx(0)


def test_parallel_twofold_faster_animal_front_has_half_gradient_drift():
    # c_animal/c_env = 2, so grad(T_animal)=0.5*grad(T_env).
    d_grad = normalized_phase_drift_from_timing_gradients(0.01, 0, 0.02, 0)
    d_ratio = normalized_phase_drift_from_speed_ratio(2.0, 1.0)
    assert d_grad == pytest.approx(0.5)
    assert d_ratio == pytest.approx(0.5)


def test_phase_drift_penalizes_opposite_equal_speed_fronts():
    d = normalized_phase_drift_from_speed_ratio(1.0, -1.0)
    assert d == pytest.approx(2.0)
