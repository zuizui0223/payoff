from math import isclose

from src.anti_phase_temporal import (
    anti_phase_temporal_premium,
    weak_contrast_shape,
)
from src.temporal_reciprocal_game import (
    classify_reciprocal_temporal_state,
    effective_coordination_strength,
    reciprocal_exponents,
    temporal_middle_half_width,
    weak_contrast_coordination_can_be_overcome,
    weak_contrast_switch_migrations,
    weak_contrast_threshold_ratio,
)


def test_reciprocal_exponents_share_same_temporal_premium():
    phi_bar = 0.2
    eta = 0.4
    x = 1.2
    m = 0.5
    tau = 0.8
    premium = anti_phase_temporal_premium(x, m, tau)
    lambda_d, lambda_s = reciprocal_exponents(phi_bar, eta, x, m, tau)
    assert isclose(lambda_d, phi_bar - eta + premium, abs_tol=1e-12)
    assert isclose(lambda_s, -phi_bar - eta + premium, abs_tol=1e-12)
    assert isclose((lambda_d + lambda_s) / 2.0, premium - eta, abs_tol=1e-12)


def test_effective_eta_is_eta_minus_temporal_premium():
    eta = 0.25
    x = 1.1
    m = 0.7
    tau = 0.9
    premium = anti_phase_temporal_premium(x, m, tau)
    assert isclose(
        effective_coordination_strength(eta, x, m, tau),
        eta - premium,
        abs_tol=1e-12,
    )
    assert isclose(
        temporal_middle_half_width(eta, x, m, tau),
        abs(eta - premium),
        abs_tol=1e-12,
    )


def test_intermediate_migration_can_flip_coordination_to_reciprocal_invasion():
    phi_bar = 0.0
    eta = 0.15
    x = 1.5
    tau = 1.0
    assert (
        classify_reciprocal_temporal_state(phi_bar, eta, x, 0.0, tau)
        == "mutual_noninvasion"
    )
    assert (
        classify_reciprocal_temporal_state(phi_bar, eta, x, 1.0, tau)
        == "reciprocal_invasion"
    )
    assert (
        classify_reciprocal_temporal_state(phi_bar, eta, x, 100.0, tau)
        == "mutual_noninvasion"
    )


def test_temporal_boundary_at_premium_equal_eta():
    eta = 0.1
    x = 1.0
    tau = 1.0
    # Find a numerical crossing by bisection on the rising branch.
    lo, hi = 0.0, 2.0
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if anti_phase_temporal_premium(x, mid, tau) < eta:
            lo = mid
        else:
            hi = mid
    m = 0.5 * (lo + hi)
    lambda_d, lambda_s = reciprocal_exponents(0.0, eta, x, m, tau)
    assert abs(lambda_d) < 1e-10
    assert abs(lambda_s) < 1e-10


def test_weak_contrast_threshold_ratio_constant():
    assert isclose(
        weak_contrast_threshold_ratio(),
        7.547879628343014,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )


def test_weak_contrast_switches_exist_only_above_rescue_capacity_threshold():
    tau = 1.0
    x = 0.1
    # max premium ~=0.13249*x^2*tau ~=0.0013249
    assert weak_contrast_coordination_can_be_overcome(0.001, x, tau)
    assert not weak_contrast_coordination_can_be_overcome(0.002, x, tau)


def test_weak_contrast_switch_roots_bracket_intermediate_reciprocal_band():
    tau = 1.0
    x = 0.1
    eta = 0.001
    switches = weak_contrast_switch_migrations(eta, x, tau)
    assert switches is not None
    m_lo, m_hi = switches
    assert 0.0 < m_lo < m_hi
    target = eta / (x * x * tau)
    assert isclose(weak_contrast_shape(m_lo * tau), target, rel_tol=1e-10, abs_tol=1e-10)
    assert isclose(weak_contrast_shape(m_hi * tau), target, rel_tol=1e-10, abs_tol=1e-10)

    # Exact weak-contrast model should agree on the qualitative middle band.
    assert (
        classify_reciprocal_temporal_state(0.0, eta, x, 0.5 * (m_lo + m_hi), tau)
        == "reciprocal_invasion"
    )
