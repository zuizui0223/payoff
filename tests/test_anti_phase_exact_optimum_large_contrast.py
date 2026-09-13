from math import isclose, isfinite

from src.anti_phase_temporal import (
    dimensionless_premium,
    dimensionless_premium_derivative,
    exact_optimal_dimensionless_migration,
)


def test_large_contrast_derivative_is_finite() -> None:
    for v in (300.0, 400.0, 1000.0):
        value = dimensionless_premium_derivative(1.0, v)
        assert isfinite(value)


def test_large_contrast_exact_optimum_remains_finite_and_stationary() -> None:
    for v in (300.0, 400.0, 1000.0):
        u_star = exact_optimal_dimensionless_migration(v)
        assert isfinite(u_star)
        assert 1.0 < u_star < 1.01
        assert abs(dimensionless_premium_derivative(u_star, v)) < 1e-10


def test_large_contrast_exact_optimum_is_a_local_and_global_peak() -> None:
    for v in (300.0, 1000.0):
        u_star = exact_optimal_dimensionless_migration(v)
        peak = dimensionless_premium(u_star, v)
        for multiplier in (0.25, 0.5, 0.9, 1.1, 2.0, 4.0):
            assert peak > dimensionless_premium(multiplier * u_star, v)


def test_exact_optimum_preserves_preoverflow_regime() -> None:
    # Anchor the stable implementation to a value already reachable by the
    # original direct-hyperbolic implementation.
    observed = exact_optimal_dimensionless_migration(100.0)
    assert isclose(observed, 1.01010048963146, rel_tol=1e-11, abs_tol=1e-12)
