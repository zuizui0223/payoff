from math import exp, isclose

from src.finite_population import moran_log_fixation_ratio_d_over_s
from src.topology_game import (
    classify_pairwise_topology_game,
    expected_topology_distance,
    mean_topology_game_payoff,
    normalized_intrinsic_slope,
    pairwise_payoff_gap,
    pairwise_payoff_parameters,
    reciprocal_fixation_probabilities,
    reciprocal_invasion_margins,
    topology_distance,
    topology_marginal_release_frequencies,
)


def test_weighted_hamming_distance():
    s = (0, 1, 0, 1)
    t = (1, 1, 0, 0)
    assert isclose(topology_distance(s, t), 2.0)
    assert isclose(topology_distance(s, t, [2.0, 3.0, 5.0, 7.0]), 9.0)


def test_pairwise_topology_mapping_is_exact_canonical_payoff():
    s = (0, 0, 1)
    t = (1, 0, 0)
    b_s = 0.2
    b_t = 0.7
    gamma = -0.3
    weights = [2.0, 1.0, 4.0]
    q = topology_distance(s, t, weights)
    phi, eta = pairwise_payoff_parameters(b_s, b_t, s, t, gamma, weights)
    assert isclose(phi, 0.5)
    assert isclose(eta, gamma * q)
    for p in [0.0, 0.2, 0.5, 0.8, 1.0]:
        expected = phi + eta * (2.0 * p - 1.0)
        assert isclose(
            pairwise_payoff_gap(p, b_s, b_t, s, t, gamma, weights),
            expected,
            abs_tol=1e-12,
        )


def test_negative_gamma_pairwise_mutual_invasion_threshold():
    s = (0, 0)
    t = (1, 1)
    b_s = 0.0
    b_t = 0.6
    q = topology_distance(s, t)
    gamma = -0.5
    assert abs(b_t - b_s) < abs(gamma) * q
    assert (
        classify_pairwise_topology_game(b_s, b_t, s, t, gamma)
        == "stable_pairwise_coexistence"
    )
    t_margin, s_margin = reciprocal_invasion_margins(b_s, b_t, s, t, gamma)
    assert t_margin > 0.0 and s_margin > 0.0


def test_positive_gamma_pairwise_coordination_threshold():
    s = (0, 0)
    t = (1, 1)
    b_s = 0.0
    b_t = 0.6
    gamma = 0.5
    assert (
        classify_pairwise_topology_game(b_s, b_t, s, t, gamma)
        == "coordination_bistability"
    )


def test_normalized_intrinsic_slope_matches_middle_region_threshold():
    s = (0, 0, 0)
    t = (1, 0, 1)
    weights = [2.0, 1.0, 3.0]
    b_s, b_t = 0.1, 0.6
    slope = normalized_intrinsic_slope(b_s, b_t, s, t, weights)
    q = topology_distance(s, t, weights)
    assert isclose(slope, abs(b_t - b_s) / q)
    assert (
        classify_pairwise_topology_game(
            b_s, b_t, s, t, gamma=-1.1 * slope, edge_weights=weights
        )
        == "stable_pairwise_coexistence"
    )


def test_reciprocal_fixation_ratio_depends_only_on_intrinsic_topology_gap():
    s = (0, 0, 0)
    t = (1, 1, 0)
    b_s = -0.15
    b_t = 0.35
    n = 20
    beta = 0.7
    for gamma in [-2.0, -0.3, 0.0, 0.8, 3.0]:
        rho_t, rho_s = reciprocal_fixation_probabilities(
            n, beta, b_s, b_t, s, t, gamma
        )
        observed = rho_t / rho_s
        expected = exp(beta * (n - 2) * (b_t - b_s))
        assert isclose(observed, expected, rel_tol=1e-11, abs_tol=1e-12)
        assert isclose(
            moran_log_fixation_ratio_d_over_s(n, b_t - b_s, beta),
            beta * (n - 2) * (b_t - b_s),
        )


def test_expected_weighted_distance_from_edge_marginals():
    frequencies = {
        (0, 0): 0.2,
        (1, 0): 0.3,
        (0, 1): 0.1,
        (1, 1): 0.4,
    }
    weights = [2.0, 5.0]
    marginals = topology_marginal_release_frequencies(frequencies)
    assert isclose(marginals[0], 0.7)
    assert isclose(marginals[1], 0.5)
    expected = 2.0 * (
        2.0 * marginals[0] * (1.0 - marginals[0])
        + 5.0 * marginals[1] * (1.0 - marginals[1])
    )
    assert isclose(expected_topology_distance(frequencies, weights), expected)


def test_mean_topology_payoff_decomposes_into_intrinsic_and_distance_terms():
    intrinsic = {
        (0, 0): 0.0,
        (1, 0): 0.2,
        (0, 1): 0.5,
        (1, 1): 0.9,
    }
    frequencies = {
        (0, 0): 0.2,
        (1, 0): 0.3,
        (0, 1): 0.1,
        (1, 1): 0.4,
    }
    gamma = -0.7
    mean_b = sum(frequencies[topology] * intrinsic[topology] for topology in frequencies)
    expected = 2.0 * mean_b - gamma * expected_topology_distance(frequencies)
    assert isclose(
        mean_topology_game_payoff(intrinsic, frequencies, gamma),
        expected,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )
