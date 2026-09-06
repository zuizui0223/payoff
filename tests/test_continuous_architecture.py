from math import isclose, isinf

from src.continuous_architecture import (
    branching_regime,
    direct_mean_game_payoff,
    distribution_moments,
    endpoint_mixture_frequency,
    endpoint_mixture_mutant_relative_payoff,
    endpoint_subgame_coexistence_frequency,
    endpoint_subgame_parameters,
    global_potential_optimum,
    interior_singular_recovery,
    mean_game_payoff_from_moments,
    monomorphic_selection_gradient,
    mutant_invasion_fitness,
    no_feedback_optimum,
    no_feedback_regime,
    singular_invasion_curvature,
    singular_mutant_fitness_exact,
    two_function_coupling_for_recovery,
    two_function_recovery_from_coupling,
)


def test_no_feedback_three_regimes():
    L = 2.0
    kappa = 1.0
    assert no_feedback_regime(L, 1.2, kappa) == "shared"
    assert isclose(no_feedback_optimum(L, 1.2, kappa), 0.0)

    # alpha=0.6 -> r0=0.6 inside [0,2].
    assert no_feedback_regime(L, 0.4, kappa) == "partial_modularity"
    assert isclose(no_feedback_optimum(L, 0.4, kappa), 0.6)

    # alpha=2.5 -> clipped to L.
    assert no_feedback_regime(L, -1.5, kappa) == "full_differentiation"
    assert isclose(no_feedback_optimum(L, -1.5, kappa), L)


def test_symmetric_feedback_does_not_shift_selection_gradient():
    x = 0.7
    c1 = 0.3
    kappa = 1.4
    expected = 0.7 - 1.4 * x
    assert isclose(monomorphic_selection_gradient(x, c1, kappa), expected)
    # Numerical mutant slopes agree for very different gamma values.
    for gamma in [-3.0, -0.2, 0.0, 2.0]:
        eps = 1e-6
        slope = mutant_invasion_fitness(x + eps, x, c1, kappa, gamma) / eps
        assert isclose(slope, expected, rel_tol=5e-6, abs_tol=5e-6)


def test_exact_branching_threshold_and_singular_fitness_identity():
    L = 2.0
    c1 = 0.4
    kappa = 1.0
    r0 = interior_singular_recovery(L, c1, kappa)
    assert r0 is not None
    assert isclose(r0, 0.6)

    assert branching_regime(kappa, -0.4) == "monomorphic_ess"
    assert branching_regime(kappa, -0.5) == "neutral_variance_threshold"
    assert branching_regime(kappa, -0.8) == "branching_compatible"
    assert isclose(singular_invasion_curvature(kappa, -0.5), 0.0)

    for gamma in [-0.3, -0.5, -0.9]:
        for mutant in [0.0, 0.2, 1.1, 2.0]:
            direct = mutant_invasion_fitness(mutant, r0, c1, kappa, gamma)
            closed = singular_mutant_fitness_exact(mutant, r0, kappa, gamma)
            assert isclose(direct, closed, rel_tol=1e-12, abs_tol=1e-12)


def test_moment_potential_matches_direct_discrete_game():
    recoveries = [0.0, 0.4, 1.3, 2.0]
    frequencies = [0.15, 0.25, 0.35, 0.25]
    c1 = 0.2
    kappa = 1.1
    gamma = -0.4
    mean, variance = distribution_moments(recoveries, frequencies)
    moment = mean_game_payoff_from_moments(mean, variance, c1, kappa, gamma)
    direct = direct_mean_game_payoff(recoveries, frequencies, c1, kappa, gamma)
    assert isclose(moment, direct, rel_tol=1e-12, abs_tol=1e-12)


def test_weak_dissimilarity_feedback_gives_monomorphic_partial_optimum():
    result = global_potential_optimum(
        max_recovery=2.0,
        linear_cost_slope=0.4,
        curvature=1.0,
        gamma=-0.3,
    )
    assert result["regime"] == "monomorphic"
    assert isclose(result["mean_recovery"], 0.6)
    assert isclose(result["variance_recovery"], 0.0)


def test_threshold_flattens_variance_at_fixed_optimal_mean():
    L = 2.0
    c1 = 0.4
    kappa = 1.0
    gamma = -0.5
    r0 = 0.6

    monomorphic = mean_game_payoff_from_moments(r0, 0.0, c1, kappa, gamma)
    # Endpoint mixture with the same mean pL=r0 has maximal possible variance.
    p = r0 / L
    variance = p * (1.0 - p) * L * L
    endpoints = mean_game_payoff_from_moments(r0, variance, c1, kappa, gamma)
    assert isclose(monomorphic, endpoints, rel_tol=1e-12, abs_tol=1e-12)


def test_strong_dissimilarity_feedback_yields_endpoint_polymorphism():
    L = 2.0
    c1 = 0.4
    kappa = 1.0
    gamma = -0.8
    result = global_potential_optimum(L, c1, kappa, gamma)
    assert result["regime"] == "endpoint_polymorphism"
    p = endpoint_mixture_frequency(L, c1, kappa, gamma)
    assert 0.0 < p < 1.0
    assert isclose(result["endpoint_d_frequency"], p)
    assert isclose(result["mean_recovery"], p * L)
    assert isclose(result["variance_recovery"], p * (1.0 - p) * L * L)


def test_endpoint_mixture_is_protected_against_all_intermediate_recoveries():
    L = 2.0
    c1 = 0.4
    kappa = 1.0
    gamma = -0.8
    p = endpoint_mixture_frequency(L, c1, kappa, gamma)

    # Endpoints have equal payoff at the protected mixture.
    rel_d = endpoint_mixture_mutant_relative_payoff(L, L, p, c1, kappa, gamma)
    assert isclose(rel_d, 0.0, abs_tol=1e-12)

    for y in [0.05, 0.2, 0.5, 0.9, 1.4, 1.95]:
        assert endpoint_mixture_mutant_relative_payoff(
            y, L, p, c1, kappa, gamma
        ) < 0.0


def test_endpoint_subgame_exactly_recovers_continuous_endpoint_frequency():
    L = 2.0
    c1 = 0.4
    kappa = 1.0
    gamma = -0.8
    phi, eta = endpoint_subgame_parameters(L, c1, kappa, gamma)
    assert isclose(phi, 0.6 * L - 0.5 * kappa * L * L)
    assert isclose(eta, gamma * L * L)

    continuous_p = endpoint_mixture_frequency(L, c1, kappa, gamma)
    game_p = endpoint_subgame_coexistence_frequency(L, c1, kappa, gamma)
    assert game_p is not None
    assert isclose(continuous_p, game_p, rel_tol=1e-12, abs_tol=1e-12)


def test_two_function_recovery_coupling_round_trip():
    a, b, L = 2.0, 3.0, 1.7
    for recovery in [0.1, 0.4, 0.9, 1.3, L]:
        coupling = two_function_coupling_for_recovery(a, b, L, recovery)
        observed = two_function_recovery_from_coupling(a, b, L, coupling)
        assert isclose(observed, recovery, rel_tol=1e-12, abs_tol=1e-12)

    assert isinf(two_function_coupling_for_recovery(a, b, L, 0.0))
    assert isclose(two_function_coupling_for_recovery(a, b, L, L), 0.0)
