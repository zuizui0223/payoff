from math import isclose

from src.anti_phase_temporal import (
    anti_phase_temporal_premium,
    exact_max_premium,
    exact_optimal_migration,
    weak_contrast_shape,
)
from src.temporal_reciprocal_game import (
    classify_reciprocal_temporal_state,
    effective_coordination_strength,
    exact_coordination_can_be_overcome,
    exact_reciprocal_invasion_capacity,
    exact_reciprocal_switch_migrations,
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


def test_exact_switch_solver_returns_two_unique_boundaries():
    phi_bar = 0.0
    eta = 0.15
    x = 1.5
    tau = 1.0
    switches = exact_reciprocal_switch_migrations(eta, phi_bar, x, tau)
    assert switches is not None
    lower, upper = switches
    m_star = exact_optimal_migration(x, tau)
    assert 0.0 < lower < m_star < upper
    assert isclose(
        anti_phase_temporal_premium(x, lower, tau),
        eta,
        rel_tol=1e-10,
        abs_tol=1e-10,
    )
    assert isclose(
        anti_phase_temporal_premium(x, upper, tau),
        eta,
        rel_tol=1e-10,
        abs_tol=1e-10,
    )
    assert (
        classify_reciprocal_temporal_state(phi_bar, eta, x, 0.5 * lower, tau)
        == "mutual_noninvasion"
    )
    assert (
        classify_reciprocal_temporal_state(phi_bar, eta, x, m_star, tau)
        == "reciprocal_invasion"
    )
    assert (
        classify_reciprocal_temporal_state(phi_bar, eta, x, upper * 2.0, tau)
        == "mutual_noninvasion"
    )


def test_exact_reciprocal_capacity_includes_static_gap_penalty():
    eta = 0.1
    x = 1.2
    tau = 1.0
    peak = exact_max_premium(x, tau)
    assert isclose(
        exact_reciprocal_invasion_capacity(eta, 0.2, x, tau),
        peak - 0.3,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )


def test_exact_coordination_overcome_matches_exact_peak():
    x = 1.0
    tau = 1.0
    peak = exact_max_premium(x, tau)
    assert exact_coordination_can_be_overcome(peak * 0.9, x, tau)
    assert not exact_coordination_can_be_overcome(peak * 1.1, x, tau)


def test_no_exact_reciprocal_band_when_target_exceeds_peak():
    x = 0.8
    tau = 1.2
    peak = exact_max_premium(x, tau)
    assert exact_reciprocal_switch_migrations(peak * 1.01, 0.0, x, tau) is None
    assert exact_reciprocal_switch_migrations(0.1, peak, x, tau) is None


def test_exact_general_phi_band_requires_premium_above_eta_plus_abs_phi():
    eta = 0.05
    phi_bar = 0.08
    x = 1.2
    tau = 1.0
    switches = exact_reciprocal_switch_migrations(eta, phi_bar, x, tau)
    assert switches is not None
    lower, upper = switches
    target = eta + abs(phi_bar)
    assert isclose(anti_phase_temporal_premium(x, lower, tau), target, abs_tol=1e-10)
    assert isclose(anti_phase_temporal_premium(x, upper, tau), target, abs_tol=1e-10)
    mid = exact_optimal_migration(x, tau)
    assert classify_reciprocal_temporal_state(phi_bar, eta, x, mid, tau) == "reciprocal_invasion"


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
    assert (
        classify_reciprocal_temporal_state(0.0, eta, x, 0.5 * (m_lo + m_hi), tau)
        == "reciprocal_invasion"
    )
