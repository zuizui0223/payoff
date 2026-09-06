from math import ceil, exp, isclose

from src.finite_population import (
    classify_weak_selection_mutant_advantage,
    cumulative_gap,
    deterministic_coordination_threshold,
    finite_payoff_gap,
    finite_payoffs,
    finite_zero_gap_count,
    minimum_initial_d_for_fixation_probability,
    moran_fixation_probability_d,
    moran_fixation_probability_from_i,
    moran_fixation_probability_s,
    moran_log_fixation_ratio_d_over_s,
    weak_selection_advantage_flags,
    weak_selection_cost_thresholds,
)


def test_finite_gap_matches_payoff_difference():
    for n in [3, 7, 20]:
        for i in range(1, n):
            pi_s, pi_d = finite_payoffs(i, n, phi=0.4, eta=-0.8)
            assert isclose(
                pi_d - pi_s,
                finite_payoff_gap(i, n, 0.4, -0.8),
                rel_tol=1e-12,
                abs_tol=1e-12,
            )


def test_cumulative_gap_closed_form_matches_sum():
    n = 17
    phi = 0.31
    eta = -0.72
    running = 0.0
    assert cumulative_gap(0, n, phi, eta) == 0.0
    for k in range(1, n):
        running += finite_payoff_gap(k, n, phi, eta)
        assert isclose(
            running,
            cumulative_gap(k, n, phi, eta),
            rel_tol=1e-12,
            abs_tol=1e-12,
        )


def test_neutral_fixation_probability_is_initial_frequency():
    for n in [2, 5, 25, 100]:
        for initial_d in [0, 1, n // 2, n]:
            rho = moran_fixation_probability_from_i(
                initial_d, n, phi=2.0, eta=-4.0, beta=0.0
            )
            assert isclose(rho, initial_d / n, rel_tol=1e-12, abs_tol=1e-12)


def test_single_mutant_wrapper_matches_general_formula():
    rho_general = moran_fixation_probability_from_i(1, 31, 0.2, -0.7, 0.4)
    rho_single = moran_fixation_probability_d(31, 0.2, -0.7, 0.4)
    assert isclose(rho_general, rho_single, rel_tol=1e-12, abs_tol=1e-12)


def test_fixation_probability_is_strictly_increasing_with_initial_count():
    n = 40
    values = [moran_fixation_probability_from_i(i, n, 0.15, 0.8, 0.7) for i in range(n + 1)]
    assert all(left < right for left, right in zip(values, values[1:]))


def test_neutral_minimum_count_is_ceiling_target_times_n():
    n = 37
    for target in [0.1, 0.25, 0.5, 0.9, 1.0]:
        observed = minimum_initial_d_for_fixation_probability(
            n, phi=9.0, eta=-4.0, beta=0.0, target=target
        )
        assert observed == ceil(target * n)


def test_coordination_critical_mass_tracks_finite_zero_gap_threshold():
    n = 100
    phi = 0.2
    eta = 1.0
    zero_gap = finite_zero_gap_count(n, phi, eta)
    critical_50 = minimum_initial_d_for_fixation_probability(
        n, phi, eta, beta=5.0, target=0.5
    )
    assert abs(critical_50 - zero_gap) <= 1.0


def test_exact_reciprocal_fixation_ratio():
    for n in [3, 8, 31]:
        for phi in [-0.7, -0.1, 0.0, 0.25, 1.2]:
            for eta in [-1.4, 0.0, 0.9]:
                beta = 0.37
                rho_d = moran_fixation_probability_d(n, phi, eta, beta)
                rho_s = moran_fixation_probability_s(n, phi, eta, beta)
                expected = exp(moran_log_fixation_ratio_d_over_s(n, phi, beta))
                assert isclose(rho_d / rho_s, expected, rel_tol=1e-11, abs_tol=1e-12)


def test_frequency_feedback_changes_absolute_but_not_relative_ordering():
    n = 20
    phi = 0.2
    beta = 0.5
    ratios = []
    rho_ds = []
    for eta in [-2.0, -0.5, 0.0, 0.5, 2.0]:
        rho_d = moran_fixation_probability_d(n, phi, eta, beta)
        rho_s = moran_fixation_probability_s(n, phi, eta, beta)
        ratios.append(rho_d / rho_s)
        rho_ds.append(rho_d)
    assert max(ratios) - min(ratios) < 1e-11
    assert max(rho_ds) - min(rho_ds) > 1e-4


def test_weak_selection_scores_match_small_beta_direction():
    n = 50
    beta = 1e-7
    cases = [
        (0.4, 1.0),
        (0.2, 1.0),
        (0.0, -1.0),
        (-0.4, 1.0),
    ]
    for phi, eta in cases:
        rho_d = moran_fixation_probability_d(n, phi, eta, beta)
        d_adv, _ = weak_selection_advantage_flags(phi, eta)
        assert (rho_d > 1.0 / n) == d_adv


def test_one_third_rule_for_coordination_game():
    eta = 1.0

    phi_favored = 0.4
    p_star = deterministic_coordination_threshold(phi_favored, eta)
    assert p_star < 1.0 / 3.0
    assert weak_selection_advantage_flags(phi_favored, eta)[0]

    phi_disfavored = 0.2
    p_star = deterministic_coordination_threshold(phi_disfavored, eta)
    assert p_star > 1.0 / 3.0
    assert not weak_selection_advantage_flags(phi_disfavored, eta)[0]


def test_weak_selection_phase_refinement():
    assert classify_weak_selection_mutant_advantage(phi=0.05, eta=-1.0) == "both_mutants_advantageous"
    assert classify_weak_selection_mutant_advantage(phi=0.05, eta=1.0) == "neither_mutant_advantageous"
    assert classify_weak_selection_mutant_advantage(phi=0.5, eta=1.0) == "d_mutant_advantageous"
    assert classify_weak_selection_mutant_advantage(phi=-0.5, eta=1.0) == "s_mutant_advantageous"


def test_fixation_cost_thresholds_have_one_third_width():
    recovery = 2.5
    eta = 0.9
    k_d, k_s = weak_selection_cost_thresholds(recovery, eta)
    assert isclose(k_s - k_d, 2.0 * eta / 3.0, rel_tol=1e-12)
    assert isclose((k_d + k_s) / 2.0, recovery, rel_tol=1e-12)
