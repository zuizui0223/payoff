from math import isclose

from src.temporal_contrast_threshold import (
    critical_contrast_half_amplitude,
    critical_dimensionless_contrast,
    exact_max_dimensionless_premium,
    strong_barrier_critical_contrast_approx,
    weak_barrier_critical_contrast_approx,
)


def test_exact_max_dimensionless_premium_is_strictly_increasing():
    values = [exact_max_dimensionless_premium(v) for v in [0.0, 0.05, 0.2, 0.8, 1.5, 3.0, 6.0]]
    assert all(values[i] < values[i + 1] for i in range(len(values) - 1))


def test_critical_contrast_inverts_exact_maximum():
    for barrier in [1e-4, 0.01, 0.1, 0.5, 1.5, 4.0]:
        v = critical_dimensionless_contrast(barrier)
        assert isclose(
            exact_max_dimensionless_premium(v),
            barrier,
            rel_tol=2e-10,
            abs_tol=2e-10,
        )


def test_critical_contrast_increases_with_barrier():
    barriers = [0.01, 0.05, 0.2, 1.0, 3.0]
    contrasts = [critical_dimensionless_contrast(value) for value in barriers]
    assert all(contrasts[i] < contrasts[i + 1] for i in range(len(contrasts) - 1))


def test_dimensional_critical_contrast_uses_eta_plus_abs_phi():
    eta = 0.12
    phi_bar = -0.08
    tau = 1.5
    x_c = critical_contrast_half_amplitude(eta, phi_bar, tau)
    barrier = (eta + abs(phi_bar)) * tau
    assert isclose(
        exact_max_dimensionless_premium(x_c * tau),
        barrier,
        rel_tol=2e-10,
        abs_tol=2e-10,
    )


def test_weak_barrier_approximation_converges():
    for barrier in [1e-4, 5e-4, 1e-3]:
        exact = critical_dimensionless_contrast(barrier)
        approx = weak_barrier_critical_contrast_approx(barrier)
        assert isclose(exact, approx, rel_tol=3e-3, abs_tol=1e-8)


def test_strong_barrier_approximation_is_reasonable():
    for barrier in [10.0, 20.0, 40.0]:
        exact = critical_dimensionless_contrast(barrier)
        approx = strong_barrier_critical_contrast_approx(barrier)
        assert isclose(exact, approx, rel_tol=2e-2, abs_tol=1e-6)
