from math import exp, isclose, log

from src.mutation_stationary import (
    detailed_balance_residuals,
    mutation_shifted_cost_crossing,
    mutation_shifted_static_crossing,
    mutation_transition_probabilities,
    rare_mutation_boundary_probability_d,
    rare_mutation_log_boundary_odds,
    stationary_distribution,
    stationary_modes,
    stationary_summary,
)


def test_boundary_mutation_transitions_are_exact():
    n = 20
    t_plus, t_minus = mutation_transition_probabilities(
        0, n, phi=0.4, eta=-0.7, beta=2.0, u_sd=0.03, u_ds=0.08
    )
    assert isclose(t_plus, 0.03)
    assert isclose(t_minus, 0.0)

    t_plus, t_minus = mutation_transition_probabilities(
        n, n, phi=0.4, eta=-0.7, beta=2.0, u_sd=0.03, u_ds=0.08
    )
    assert isclose(t_plus, 0.0)
    assert isclose(t_minus, 0.08)


def test_stationary_distribution_is_normalized_and_detailed_balanced():
    params = dict(n=31, phi=0.23, eta=-0.9, beta=0.7, u_sd=0.015, u_ds=0.027)
    probs = stationary_distribution(**params)
    assert len(probs) == params["n"] + 1
    assert all(p > 0.0 for p in probs)
    assert isclose(sum(probs), 1.0, rel_tol=1e-12, abs_tol=1e-12)

    residuals = detailed_balance_residuals(probs, **params)
    assert max(abs(value) for value in residuals) < 1e-12


def test_neutral_symmetric_mutation_has_symmetric_stationary_distribution():
    probs = stationary_distribution(
        n=24,
        phi=0.0,
        eta=0.0,
        beta=1.0,
        u_sd=0.04,
        u_ds=0.04,
    )
    for i in range(len(probs)):
        assert isclose(probs[i], probs[-1 - i], rel_tol=1e-12, abs_tol=1e-12)

    summary = stationary_summary(probs)
    assert isclose(summary["mean_d_frequency"], 0.5, abs_tol=1e-12)
    assert isclose(summary["p_all_s"], summary["p_all_d"], abs_tol=1e-12)


def test_neutral_mutation_bias_shifts_stationary_mean():
    toward_d = stationary_distribution(
        n=30, phi=0.0, eta=0.0, beta=1.0, u_sd=0.06, u_ds=0.01
    )
    toward_s = stationary_distribution(
        n=30, phi=0.0, eta=0.0, beta=1.0, u_sd=0.01, u_ds=0.06
    )
    assert stationary_summary(toward_d)["mean_d_frequency"] > 0.5
    assert stationary_summary(toward_s)["mean_d_frequency"] < 0.5


def test_rare_mutation_boundary_odds_match_exact_limit():
    n = 23
    phi = 0.17
    eta = 1.1
    beta = 0.6
    r_sd = 2.5
    r_ds = 0.7
    eps = 1e-8
    probs = stationary_distribution(
        n=n,
        phi=phi,
        eta=eta,
        beta=beta,
        u_sd=eps * r_sd,
        u_ds=eps * r_ds,
    )
    observed = log(probs[-1] / probs[0])
    expected = rare_mutation_log_boundary_odds(n, phi, beta, r_sd, r_ds)
    assert isclose(observed, expected, rel_tol=1e-6, abs_tol=1e-6)


def test_eta_cancels_from_rare_boundary_odds_but_not_finite_stationary_shape():
    n = 20
    phi = 0.12
    beta = 0.8
    eps = 1e-8
    log_odds = []
    for eta in [-2.0, 0.0, 2.0]:
        probs = stationary_distribution(
            n=n, phi=phi, eta=eta, beta=beta, u_sd=eps, u_ds=eps
        )
        log_odds.append(log(probs[-1] / probs[0]))
    assert max(log_odds) - min(log_odds) < 1e-6

    moderate = []
    for eta in [-2.0, 0.0, 2.0]:
        probs = stationary_distribution(
            n=n, phi=phi, eta=eta, beta=beta, u_sd=0.04, u_ds=0.04
        )
        moderate.append(stationary_summary(probs)["interior_mass"])
    assert max(moderate) - min(moderate) > 1e-4


def test_rare_two_state_probability_matches_boundary_conditioning():
    n = 40
    phi = -0.08
    eta = -0.9
    beta = 0.5
    r_sd = 1.8
    r_ds = 0.6
    eps = 1e-8
    probs = stationary_distribution(
        n=n,
        phi=phi,
        eta=eta,
        beta=beta,
        u_sd=eps * r_sd,
        u_ds=eps * r_ds,
    )
    observed = probs[-1] / (probs[0] + probs[-1])
    expected = rare_mutation_boundary_probability_d(n, phi, beta, r_sd, r_ds)
    assert isclose(observed, expected, rel_tol=1e-6, abs_tol=1e-6)


def test_mutation_shifted_crossing_equalizes_rare_boundary_odds():
    n = 18
    beta = 0.9
    r_sd = 4.0
    r_ds = 1.0
    phi_cross = mutation_shifted_static_crossing(n, beta, r_sd, r_ds)
    assert isclose(
        rare_mutation_log_boundary_odds(n, phi_cross, beta, r_sd, r_ds),
        0.0,
        abs_tol=1e-12,
    )

    recovery = 1.7
    k_cross = mutation_shifted_cost_crossing(n, recovery, beta, r_sd, r_ds)
    assert isclose(recovery - k_cross, phi_cross, abs_tol=1e-12)


def test_stationary_modes_are_valid_local_maxima():
    probs = stationary_distribution(
        n=35, phi=0.0, eta=1.4, beta=1.5, u_sd=0.002, u_ds=0.002
    )
    modes = stationary_modes(probs)
    assert modes
    for i in modes:
        if i > 0:
            assert probs[i] >= probs[i - 1] - 1e-15
        if i + 1 < len(probs):
            assert probs[i] >= probs[i + 1] - 1e-15
