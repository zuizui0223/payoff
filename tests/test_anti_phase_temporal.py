from math import isclose

from src.anti_phase_temporal import (
    anti_phase_floquet_exponent,
    anti_phase_temporal_premium,
    fast_switching_premium,
    rescue_condition,
    small_migration_slope,
    strong_migration_premium_asymptotic,
    weak_contrast_max_premium_approx,
    weak_contrast_optimal_dimensionless_migration,
    weak_contrast_optimal_migration,
    weak_contrast_shape,
)
from src.two_patch_floquet import two_season_closed_form


def test_anti_phase_formula_matches_general_two_season_closed_form():
    rbar = -0.2
    x = 1.7
    m = 0.35
    tau = 0.8
    seasons = [(rbar + x, rbar - x, tau), (rbar - x, rbar + x, tau)]
    expected = two_season_closed_form(seasons, m)
    observed = anti_phase_floquet_exponent(rbar, x, m, tau)
    assert isclose(observed, expected, rel_tol=1e-11, abs_tol=1e-11)


def test_time_averaged_exponent_is_mean_margin():
    for rbar in [-1.0, -0.1, 0.0, 0.7]:
        observed = anti_phase_floquet_exponent(rbar, 0.0, 0.4, 0.8)
        assert isclose(observed, rbar, abs_tol=1e-12)


def test_temporal_premium_zero_without_migration_or_contrast():
    assert isclose(anti_phase_temporal_premium(1.2, 0.0, 0.7), 0.0, abs_tol=1e-12)
    assert isclose(anti_phase_temporal_premium(0.0, 0.4, 0.7), 0.0, abs_tol=1e-12)


def test_temporal_premium_strictly_positive_at_noncommuting_gate():
    for m in [0.01, 0.1, 0.5, 2.0, 10.0]:
        assert anti_phase_temporal_premium(1.3, m, 0.7) > 0.0


def test_small_migration_slope_matches_exact_limit():
    x = 1.3
    tau = 0.7
    slope = small_migration_slope(x, tau)
    for m in [1e-2, 5e-3, 1e-3]:
        observed = anti_phase_temporal_premium(x, m, tau) / m
        assert isclose(observed, slope, rel_tol=3e-4, abs_tol=1e-8)


def test_fast_switching_approximation():
    x = 1.1
    m = 0.45
    for tau in [0.05, 0.02, 0.01]:
        exact = anti_phase_temporal_premium(x, m, tau)
        approx = fast_switching_premium(x, m, tau)
        assert isclose(exact, approx, rel_tol=5e-4, abs_tol=1e-10)


def test_strong_migration_asymptotic():
    x = 1.3
    tau = 0.7
    for m in [30.0, 60.0, 100.0]:
        exact = anti_phase_temporal_premium(x, m, tau)
        approx = strong_migration_premium_asymptotic(x, m, tau)
        assert isclose(exact, approx, rel_tol=2e-3, abs_tol=1e-8)


def test_intermediate_migration_can_rescue_negative_mean_margin():
    rbar = -0.08
    x = 1.5
    tau = 1.0
    assert not rescue_condition(rbar, x, 0.0, tau)
    assert rescue_condition(rbar, x, 0.3, tau)
    assert not rescue_condition(rbar, x, 100.0, tau)


def test_temporal_premium_has_an_interior_peak_in_representative_case():
    x = 1.5
    tau = 1.0
    low = anti_phase_temporal_premium(x, 1e-6, tau)
    middle = max(
        anti_phase_temporal_premium(x, m, tau)
        for m in [0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2]
    )
    high = anti_phase_temporal_premium(x, 100.0, tau)
    assert middle > low
    assert middle > high


def test_weak_contrast_universal_optimum_constant():
    u_star = weak_contrast_optimal_dimensionless_migration()
    assert isclose(u_star, 1.60611529880277, rel_tol=1e-12, abs_tol=1e-12)
    assert isclose(
        weak_contrast_shape(u_star),
        0.1324875394468274,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )


def test_weak_contrast_shape_is_maximized_at_u_star():
    u_star = weak_contrast_optimal_dimensionless_migration()
    peak = weak_contrast_shape(u_star)
    for u in [0.05, 0.2, 0.5, 1.0, 2.0, 4.0, 10.0]:
        assert peak > weak_contrast_shape(u)


def test_weak_contrast_optimal_migration_scales_as_inverse_season_duration():
    u_star = weak_contrast_optimal_dimensionless_migration()
    for tau in [0.5, 1.0, 2.0, 4.0]:
        assert isclose(
            weak_contrast_optimal_migration(tau) * tau,
            u_star,
            rel_tol=1e-12,
            abs_tol=1e-12,
        )


def test_weak_contrast_max_premium_approximation_matches_exact_small_contrast():
    tau = 1.0
    x = 0.05
    m = weak_contrast_optimal_migration(tau)
    exact = anti_phase_temporal_premium(x, m, tau)
    approx = weak_contrast_max_premium_approx(x, tau)
    assert isclose(exact, approx, rel_tol=1e-4, abs_tol=1e-10)
