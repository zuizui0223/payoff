from math import isclose, isfinite, log, sqrt

from src.anti_phase_temporal import anti_phase_floquet_exponent, dimensionless_premium


def test_floquet_matches_existing_finite_large_tau_value():
    observed = anti_phase_floquet_exponent(0.0, 1.0, 1.0, 500.0)
    assert isclose(observed, 0.4135204151925349, rel_tol=1e-14, abs_tol=1e-14)


def test_floquet_remains_finite_beyond_direct_sinh_overflow():
    delta = sqrt(2.0)
    for tau in [710.0, 1000.0, 10_000.0]:
        observed = anti_phase_floquet_exponent(0.0, 1.0, 1.0, tau)
        expected = -1.0 + delta + log(1.0 / delta) / tau
        assert isfinite(observed)
        assert isclose(observed, expected, rel_tol=1e-14, abs_tol=1e-14)


def test_dimensionless_premium_remains_finite_for_large_u_v():
    u = 600.0
    v = 600.0
    d = sqrt(u * u + v * v)
    observed = dimensionless_premium(u, v)
    expected = -u + d + log(u / d)
    assert isfinite(observed)
    assert isclose(observed, expected, rel_tol=1e-14, abs_tol=1e-14)


def test_log_scale_evaluation_preserves_tiny_ratio_information():
    observed = dimensionless_premium(5e-324, 710.0)
    assert observed > 0.0
    assert isfinite(observed)
