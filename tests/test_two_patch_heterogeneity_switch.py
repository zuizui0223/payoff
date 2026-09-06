from math import isclose

from src.spatial_environment_gradient import (
    classify_two_patch_midpoint,
    two_patch_coordination_switch_rate,
    two_patch_midpoint_exponent,
)


def test_low_migration_reciprocal_invasion_requires_contrast_above_two_eta():
    eta = 0.5
    assert two_patch_midpoint_exponent(1.2, -0.2, eta, 0.0) > 0.0
    assert two_patch_midpoint_exponent(0.4, -0.2, eta, 0.0) < 0.0


def test_exact_switch_rate_solves_midpoint_exponent():
    phi_1 = 1.2
    phi_2 = -0.4
    eta = 0.5
    m_switch = two_patch_coordination_switch_rate(phi_1, phi_2, eta)
    expected = ((phi_1 - phi_2) ** 2 - 4.0 * eta**2) / (8.0 * eta)
    assert isclose(m_switch, expected, abs_tol=1e-12)
    assert abs(two_patch_midpoint_exponent(phi_1, phi_2, eta, m_switch)) < 1e-12


def test_switch_classification_changes_once():
    phi_1 = 1.0
    phi_2 = -0.6
    eta = 0.4
    m_switch = two_patch_coordination_switch_rate(phi_1, phi_2, eta)
    assert classify_two_patch_midpoint(phi_1, phi_2, eta, 0.5 * m_switch) == "reciprocal_spatial_invasion"
    assert classify_two_patch_midpoint(phi_1, phi_2, eta, m_switch) == "spatial_coordination_switch_boundary"
    assert classify_two_patch_midpoint(phi_1, phi_2, eta, 2.0 * m_switch) == "mutual_spatial_noninvasion"


def test_dimensionless_formula():
    eta = 0.8
    chi = 1.75
    delta_phi = 2.0 * eta * chi
    m_switch = two_patch_coordination_switch_rate(delta_phi / 2.0, -delta_phi / 2.0, eta)
    assert isclose(m_switch / eta, (chi**2 - 1.0) / 2.0, abs_tol=1e-12)


def test_switch_rate_requires_sufficient_patch_contrast():
    eta = 1.0
    try:
        two_patch_coordination_switch_rate(0.9, -0.9, eta)
    except ValueError:
        pass
    else:
        raise AssertionError("expected insufficient contrast to reject a positive switch rate")
