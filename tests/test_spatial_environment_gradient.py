from math import isclose

from src.spatial_environment_gradient import (
    baseline_spatial_exponents,
    critical_environments,
    environmental_invasion_exponents,
    environmental_phis,
    no_frequency_feedback_zero_migration_window,
    signed_reciprocal_environment_width,
    spatial_environment_summary,
    strong_migration_thresholds,
)


def test_environmental_phis_common_shift():
    observed = environmental_phis([0.4, -0.2, 0.1], environment=3.0, reference_environment=1.0, slope=0.25)
    expected = [0.9, 0.3, 0.6]
    assert all(isclose(a, b, abs_tol=1e-12) for a, b in zip(observed, expected))


def test_exact_principal_eigenvalue_environment_shift():
    base_phis = [0.5, -0.3, 0.1]
    etas = [-0.2, 0.4, -0.1]
    adjacency = [
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
    ]
    m = 0.37
    e0 = 2.0
    alpha = 0.6
    lambda_d0, lambda_s0 = baseline_spatial_exponents(base_phis, etas, adjacency, m)
    for environment in [-1.0, 0.0, 2.0, 4.5]:
        lambda_d, lambda_s = environmental_invasion_exponents(
            base_phis, etas, adjacency, m, environment, e0, alpha
        )
        shift = alpha * (environment - e0)
        assert isclose(lambda_d, lambda_d0 + shift, rel_tol=1e-11, abs_tol=1e-11)
        assert isclose(lambda_s, lambda_s0 - shift, rel_tol=1e-11, abs_tol=1e-11)


def test_critical_environments_make_reciprocal_exponents_zero():
    base_phis = [0.7, -0.4]
    etas = [-0.3, 0.2]
    adjacency = [[0.0, 1.0], [1.0, 0.0]]
    m = 0.25
    e0 = 1.5
    alpha = 0.8
    e_d, e_s = critical_environments(base_phis, etas, adjacency, m, e0, alpha)
    d_at_d, _ = environmental_invasion_exponents(base_phis, etas, adjacency, m, e_d, e0, alpha)
    _, s_at_s = environmental_invasion_exponents(base_phis, etas, adjacency, m, e_s, e0, alpha)
    assert abs(d_at_d) < 1e-10
    assert abs(s_at_s) < 1e-10


def test_migration_compresses_signed_environment_window():
    base_phis = [0.8, -0.6, 0.2]
    etas = [0.0, 0.0, 0.0]
    adjacency = [
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
    ]
    alpha = 0.7
    widths = [
        signed_reciprocal_environment_width(base_phis, etas, adjacency, m, alpha)
        for m in [0.0, 0.1, 1.0, 10.0, 1000.0]
    ]
    assert all(widths[i] > widths[i + 1] for i in range(len(widths) - 1))
    assert widths[0] > 0.0
    assert abs(widths[-1]) < 1e-3


def test_no_frequency_feedback_zero_migration_window_is_phi_range_over_slope():
    base_phis = [0.9, -0.4, 0.1, -0.1]
    alpha = 0.5
    expected = (max(base_phis) - min(base_phis)) / alpha
    assert isclose(
        no_frequency_feedback_zero_migration_window(base_phis, alpha),
        expected,
        abs_tol=1e-12,
    )


def test_homogeneous_patch_special_case_recovers_well_mixed_width():
    base_phis = [0.2, 0.2, 0.2]
    eta = -0.6
    etas = [eta, eta, eta]
    adjacency = [
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
    ]
    alpha = 0.4
    expected_signed = -2.0 * eta / alpha
    for m in [0.0, 0.1, 2.0, 100.0]:
        width = signed_reciprocal_environment_width(base_phis, etas, adjacency, m, alpha)
        assert isclose(width, expected_signed, rel_tol=1e-10, abs_tol=1e-10)


def test_strong_migration_thresholds_depend_only_on_mean_phi_and_eta():
    base_phis = [0.8, -0.5, 0.2]
    etas = [-0.3, 0.1, 0.4]
    e0 = 2.2
    alpha = 0.9
    e_d_inf, e_s_inf = strong_migration_thresholds(base_phis, etas, e0, alpha)
    mean_phi = sum(base_phis) / len(base_phis)
    mean_eta = sum(etas) / len(etas)
    assert isclose(e_d_inf, e0 - (mean_phi - mean_eta) / alpha, abs_tol=1e-12)
    assert isclose(e_s_inf, e0 + (-mean_phi - mean_eta) / alpha, abs_tol=1e-12)


def test_d_environment_threshold_rises_with_migration_in_source_sink_case():
    base_phis = [0.6, -1.0]
    etas = [0.0, 0.0]
    adjacency = [[0.0, 1.0], [1.0, 0.0]]
    e0 = 0.0
    alpha = 1.0
    thresholds = [
        critical_environments(base_phis, etas, adjacency, m, e0, alpha)[0]
        for m in [0.0, 0.1, 0.5, 2.0]
    ]
    assert all(thresholds[i] < thresholds[i + 1] for i in range(len(thresholds) - 1))


def test_spatial_environment_summary_consistent():
    base_phis = [0.5, -0.1]
    etas = [-0.2, -0.2]
    adjacency = [[0.0, 1.0], [1.0, 0.0]]
    summary = spatial_environment_summary(base_phis, etas, adjacency, 0.3, 1.0, 0.5)
    assert isclose(
        summary["signed_reciprocal_width"],
        summary["environment_s_neutral"] - summary["environment_d_neutral"],
        abs_tol=1e-12,
    )
