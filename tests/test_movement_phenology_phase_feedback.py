import math

import pytest

from analysis.movement_phenology.phase_feedback import (
    equilibrium_phase_error_days,
    exponential_relative_speed,
    local_half_distance_km,
    local_relaxation_distance_km,
    phase_error_spatial_derivative,
)


def test_equilibrium_has_unit_relative_speed():
    u0 = 0.85
    k = 0.02
    e_star = equilibrium_phase_error_days(u0, k)
    assert exponential_relative_speed(e_star, u0, k) == pytest.approx(1.0)


def test_positive_kappa_points_toward_equilibrium():
    u0 = 0.85
    k = 0.02
    ce = 6.0
    e_star = equilibrium_phase_error_days(u0, k)
    assert phase_error_spatial_derivative(e_star + 10, ce, u0, k) < 0
    assert phase_error_spatial_derivative(e_star - 10, ce, u0, k) > 0
    assert phase_error_spatial_derivative(e_star, ce, u0, k) == pytest.approx(0)


def test_relaxation_distance_formula():
    ce = 6.0
    k = 0.02
    assert local_relaxation_distance_km(ce, k) == pytest.approx(300)
    assert local_half_distance_km(ce, k) == pytest.approx(300 * math.log(2))


def test_mule_deer_point_estimates():
    u0 = 0.8565213947916187
    k = 0.018298898170402027
    ce = 5.613683545852449
    assert equilibrium_phase_error_days(u0, k) == pytest.approx(8.463678, rel=1e-6)
    assert local_relaxation_distance_km(ce, k) == pytest.approx(306.7771, rel=1e-6)


def test_bad_parameters_fail_closed():
    with pytest.raises(ValueError):
        equilibrium_phase_error_days(1.0, 0.0)
    with pytest.raises(ValueError):
        exponential_relative_speed(0, 0, 0.1)
    with pytest.raises(ValueError):
        local_relaxation_distance_km(5, -0.1)
