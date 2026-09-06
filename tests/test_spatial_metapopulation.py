from math import isclose

from src.spatial_metapopulation import (
    classify_two_patch_polarization,
    mean_network_rhs,
    mean_selection_decomposition,
    network_rhs,
    selection_derivative,
    selection_rhs,
    spatial_moments,
    synchronization_threshold,
    synchronous_mode_rates,
    two_patch_polarized_eigenvalues,
    two_patch_polarized_equilibria,
)


def test_symmetric_migration_cancels_from_global_mean():
    frequencies = [0.05, 0.25, 0.6, 0.9]
    adjacency = [
        [0.0, 1.0, 0.3, 0.0],
        [1.0, 0.0, 0.4, 0.2],
        [0.3, 0.4, 0.0, 0.7],
        [0.0, 0.2, 0.7, 0.0],
    ]
    phi = 0.31
    eta = -0.82
    local_mean = sum(selection_rhs(p, phi, eta) for p in frequencies) / len(frequencies)
    for migration_rate in [0.0, 0.1, 1.0, 20.0]:
        observed = mean_network_rhs(frequencies, adjacency, migration_rate, phi, eta)
        assert isclose(observed, local_mean, rel_tol=1e-12, abs_tol=1e-12)


def test_exact_spatial_moment_decomposition():
    frequencies = [0.02, 0.14, 0.47, 0.73, 0.96]
    for phi, eta in [(-0.4, -1.2), (0.3, 0.9), (0.0, 1.5)]:
        result = mean_selection_decomposition(frequencies, phi, eta)
        assert isclose(
            result["mean_selection"],
            result["reconstructed_mean_selection"],
            rel_tol=1e-12,
            abs_tol=1e-12,
        )


def test_midpoint_symmetric_distribution_has_minus_phi_variance_correction():
    frequencies = [0.0, 0.2, 0.8, 1.0]
    mu, variance, third = spatial_moments(frequencies)
    assert isclose(mu, 0.5, abs_tol=1e-12)
    assert isclose(third, 0.0, abs_tol=1e-12)

    for phi in [-0.7, 0.7]:
        result = mean_selection_decomposition(frequencies, phi=phi, eta=3.2)
        assert isclose(result["spatial_correction"], -phi * variance, abs_tol=1e-12)
        assert isclose(result["mean_selection"], phi * (0.25 - variance), abs_tol=1e-12)


def test_network_rhs_two_patch_migration_is_antisymmetric_in_mean():
    frequencies = [0.15, 0.85]
    adjacency = [[0.0, 1.0], [1.0, 0.0]]
    rhs_no_migration = network_rhs(frequencies, adjacency, 0.0, phi=0.1, eta=1.0)
    rhs_migration = network_rhs(frequencies, adjacency, 0.7, phi=0.1, eta=1.0)
    migration_only = [rhs_migration[i] - rhs_no_migration[i] for i in range(2)]
    assert isclose(migration_only[0], -migration_only[1], abs_tol=1e-12)


def test_graph_synchronization_threshold_matches_mode_rates():
    phi = 0.0
    eta = 2.0
    p_star = 0.5
    fp = selection_derivative(p_star, phi, eta)
    assert isclose(fp, eta / 2.0, abs_tol=1e-12)

    lambda2 = 2.0
    threshold = synchronization_threshold(p_star, phi, eta, lambda2)
    assert isclose(threshold, eta / 4.0, abs_tol=1e-12)

    below = synchronous_mode_rates(p_star, phi, eta, threshold * 0.9, [0.0, lambda2])
    above = synchronous_mode_rates(p_star, phi, eta, threshold * 1.1, [0.0, lambda2])
    assert below[0] > 0.0 and below[1] > 0.0
    assert above[0] > 0.0 and above[1] < 0.0


def test_negative_frequency_dependence_needs_no_migration_for_synchrony():
    phi = 0.1
    eta = -1.0
    p_star = 0.5 * (1.0 - phi / eta)
    assert 0.0 < p_star < 1.0
    assert selection_derivative(p_star, phi, eta) < 0.0
    assert synchronization_threshold(p_star, phi, eta, 0.3) == 0.0


def test_exact_two_patch_polarized_branch_solves_rhs():
    eta = 1.2
    adjacency = [[0.0, 1.0], [1.0, 0.0]]
    for migration_rate in [0.0, 0.05, eta / 6.0 * 0.9, eta / 4.0 * 0.99]:
        pair = two_patch_polarized_equilibria(eta, migration_rate)
        assert pair is not None
        rhs = network_rhs(pair, adjacency, migration_rate, phi=0.0, eta=eta)
        assert max(abs(value) for value in rhs) < 1e-12
        assert isclose(sum(pair), 1.0, abs_tol=1e-12)


def test_two_patch_polarization_existence_and_stability_thresholds():
    eta = 1.8
    assert classify_two_patch_polarization(eta, 0.0) == "stable_polarized_patches"
    assert classify_two_patch_polarization(eta, eta / 6.0) == "polarized_stability_boundary"
    assert classify_two_patch_polarization(eta, 0.2 * eta) == "polarized_saddle"
    assert classify_two_patch_polarization(eta, eta / 4.0) == "polarization_pitchfork_boundary"
    assert classify_two_patch_polarization(eta, 0.3 * eta) == "no_polarized_equilibrium"

    stable_rates = two_patch_polarized_eigenvalues(eta, 0.1 * eta)
    assert stable_rates is not None
    assert stable_rates[0] < 0.0 and stable_rates[1] < 0.0

    saddle_rates = two_patch_polarized_eigenvalues(eta, 0.2 * eta)
    assert saddle_rates is not None
    assert saddle_rates[0] > 0.0 and saddle_rates[1] < 0.0


def test_two_patch_pitchfork_matches_graph_sync_threshold():
    eta = 2.4
    p_star = 0.5
    lambda2 = 2.0
    graph_threshold = synchronization_threshold(p_star, 0.0, eta, lambda2)
    assert isclose(graph_threshold, eta / 4.0, abs_tol=1e-12)
    assert two_patch_polarized_equilibria(eta, graph_threshold) is None
