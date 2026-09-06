from math import isclose, isinf

from src.payoff_game import (
    QuadraticTraitArchitecture,
    architecture_payoffs,
    architecture_phi,
    classify_lke_phase,
    classify_phase,
    game_matrix,
    infer_recovery_feedback_from_cost_thresholds,
    interior_equilibrium,
    invasion_cost_surfaces,
    invasion_margins,
    linear_environment_thresholds,
    middle_cost_interval,
    n_function_conflict,
    payoff_gap,
    pure_ess,
    replicator_rhs,
    switching_action,
    switching_hysteresis_band,
)


def test_shared_conflict_load_and_optimum():
    m = QuadraticTraitArchitecture(a=2.0, b=3.0, theta1=4.0, theta2=1.0)
    assert isclose(m.shared_optimum, 2.2)
    assert isclose(m.conflict_load, (2.0 * 3.0 / 5.0) * 9.0)


def test_exact_recovery_identity():
    m = QuadraticTraitArchitecture(
        a=2.0,
        b=5.0,
        theta1=3.0,
        theta2=-1.0,
        coupling=1.7,
        architecture_cost=0.4,
    )
    assert isclose(
        m.recovered_loss,
        m.recovered_loss_via_bridge,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )


def test_separation_fraction_matches_realized_optimum_separation():
    m = QuadraticTraitArchitecture(
        a=1.3, b=2.1, theta1=5.0, theta2=2.0, coupling=0.8
    )
    x, y = m.differentiated_optima
    realized = abs(x - y) / abs(m.theta1 - m.theta2)
    assert isclose(realized, m.separation_fraction, rel_tol=1e-12, abs_tol=1e-12)


def test_full_release_at_zero_coupling():
    m = QuadraticTraitArchitecture(
        a=1.0, b=4.0, theta1=2.0, theta2=-2.0, coupling=0.0
    )
    assert m.differentiated_optima == (2.0, -2.0)
    assert isclose(m.separation_fraction, 1.0)
    assert isclose(m.differentiated_loss, 0.0)
    assert isclose(m.recovered_loss, m.conflict_load)


def test_recovery_decreases_with_coupling():
    weak = QuadraticTraitArchitecture(
        a=2.0, b=3.0, theta1=2.0, theta2=0.0, coupling=0.2
    )
    strong = QuadraticTraitArchitecture(
        a=2.0, b=3.0, theta1=2.0, theta2=0.0, coupling=4.0
    )
    assert weak.separation_fraction > strong.separation_fraction
    assert weak.recovered_loss > strong.recovered_loss


def test_n_function_pairwise_identity():
    z, variance_load, pairwise_load = n_function_conflict(
        weights=[1.0, 2.0, 4.0, 3.0],
        optima=[-1.0, 0.5, 2.0, 4.0],
    )
    assert -1.0 < z < 4.0
    assert isclose(variance_load, pairwise_load, rel_tol=1e-12, abs_tol=1e-12)


def test_phi_equals_sL_minus_K():
    m = QuadraticTraitArchitecture(
        a=2.0,
        b=3.0,
        theta1=2.0,
        theta2=-1.0,
        coupling=0.5,
        architecture_cost=1.1,
    )
    expected = m.separation_fraction * m.conflict_load - 1.1
    assert isclose(m.phi, expected, rel_tol=1e-12, abs_tol=1e-12)
    assert isclose(
        architecture_phi(m.conflict_load, m.separation_fraction, 1.1), expected
    )


def test_critical_coupling_cases():
    base = QuadraticTraitArchitecture(a=2.0, b=3.0, theta1=2.0, theta2=-1.0)
    L = base.conflict_load

    free = QuadraticTraitArchitecture(
        a=2.0,
        b=3.0,
        theta1=2.0,
        theta2=-1.0,
        architecture_cost=0.0,
    )
    assert isinf(free.critical_coupling())

    impossible = QuadraticTraitArchitecture(
        a=2.0,
        b=3.0,
        theta1=2.0,
        theta2=-1.0,
        architecture_cost=L + 1.0,
    )
    assert impossible.critical_coupling() is None

    crossing = QuadraticTraitArchitecture(
        a=2.0,
        b=3.0,
        theta1=2.0,
        theta2=-1.0,
        architecture_cost=L / 2.0,
    )
    ccrit = crossing.critical_coupling()
    assert ccrit is not None
    at_crossing = QuadraticTraitArchitecture(
        a=2.0,
        b=3.0,
        theta1=2.0,
        theta2=-1.0,
        coupling=ccrit,
        architecture_cost=L / 2.0,
    )
    assert isclose(at_crossing.phi, 0.0, abs_tol=1e-12)


def test_symmetric_payoff_representation_matches_declared_gap():
    matrix = game_matrix(phi=0.3, eta=-0.7)
    assert matrix[0][1] == matrix[1][0]
    for p in [0.0, 0.2, 0.5, 0.9, 1.0]:
        pi_s, pi_d = architecture_payoffs(p, phi=0.3, eta=-0.7)
        assert isclose(pi_d - pi_s, payoff_gap(p, 0.3, -0.7), abs_tol=1e-12)


def test_negative_frequency_dependence_stable_coexistence():
    phi = 0.2
    eta = -1.0
    pstar = interior_equilibrium(phi, eta)
    assert pstar is not None
    assert classify_phase(phi, eta) == "stable_architecture_coexistence"
    assert isclose(replicator_rhs(pstar, phi, eta), 0.0, abs_tol=1e-12)
    assert replicator_rhs(pstar - 0.05, phi, eta) > 0
    assert replicator_rhs(pstar + 0.05, phi, eta) < 0
    assert pure_ess(phi, eta) == (False, False)


def test_positive_frequency_dependence_coordination_bistability():
    phi = 0.2
    eta = 1.0
    pstar = interior_equilibrium(phi, eta)
    assert pstar is not None
    assert classify_phase(phi, eta) == "coordination_bistability"
    assert replicator_rhs(pstar - 0.05, phi, eta) < 0
    assert replicator_rhs(pstar + 0.05, phi, eta) > 0
    assert pure_ess(phi, eta) == (True, True)


def test_dominance_regions():
    assert classify_phase(phi=-2.0, eta=0.5) == "shared_dominance"
    assert classify_phase(phi=2.0, eta=0.5) == "differentiated_dominance"
    assert classify_phase(phi=-0.2, eta=0.0) == "shared_dominance"
    assert classify_phase(phi=0.2, eta=0.0) == "differentiated_dominance"


def test_invasion_surfaces_split_static_crossing():
    L = 2.0
    s = 0.5
    R = 1.0

    k_d, k_s = invasion_cost_surfaces(L, s, eta=0.3)
    assert isclose(k_d, 0.7)
    assert isclose(k_s, 1.3)
    assert isclose(k_s - k_d, 0.6)

    lower, upper = middle_cost_interval(L, s, eta=0.3)
    assert isclose(lower, 0.7)
    assert isclose(upper, 1.3)
    assert isclose(upper - lower, 0.6)

    recovered, inferred_eta = infer_recovery_feedback_from_cost_thresholds(k_d, k_s)
    assert isclose(recovered, R)
    assert isclose(inferred_eta, 0.3)


def test_negative_eta_reverses_signed_threshold_order_not_middle_width():
    k_d, k_s = invasion_cost_surfaces(2.0, 0.5, eta=-0.3)
    assert isclose(k_d, 1.3)
    assert isclose(k_s, 0.7)
    assert isclose(k_s - k_d, -0.6)

    lower, upper = middle_cost_interval(2.0, 0.5, eta=-0.3)
    assert isclose(lower, 0.7)
    assert isclose(upper, 1.3)

    recovered, inferred_eta = infer_recovery_feedback_from_cost_thresholds(k_d, k_s)
    assert isclose(recovered, 1.0)
    assert isclose(inferred_eta, -0.3)


def test_eta_zero_collapses_both_invasion_surfaces_to_static_crossing():
    k_d, k_s = invasion_cost_surfaces(3.0, 0.4, eta=0.0)
    assert isclose(k_d, 1.2)
    assert isclose(k_s, 1.2)


def test_static_balance_can_admit_differentiated_invasion():
    L, s, K, eta = 2.0, 0.4, 1.0, -0.5
    phi = architecture_phi(L, s, K)
    i_d, i_s = invasion_margins(L, s, K, eta)
    assert phi < 0.0
    assert i_d > 0.0
    assert i_s > 0.0
    assert classify_lke_phase(L, s, K, eta) == "stable_architecture_coexistence"


def test_static_bita_advantage_can_face_coordination_barrier():
    L, s, K, eta = 2.0, 0.6, 1.0, 0.5
    phi = architecture_phi(L, s, K)
    i_d, i_s = invasion_margins(L, s, K, eta)
    assert phi > 0.0
    assert i_d < 0.0
    assert i_s < 0.0
    assert classify_lke_phase(L, s, K, eta) == "coordination_bistability"


def test_lke_phase_boundaries_match_exact_cost_wedge():
    L, s = 2.0, 0.5
    assert classify_lke_phase(L, s, 1.3, eta=-0.2) == "shared_dominance"
    assert classify_lke_phase(L, s, 1.0, eta=-0.2) == "stable_architecture_coexistence"
    assert classify_lke_phase(L, s, 0.7, eta=-0.2) == "differentiated_dominance"
    assert classify_lke_phase(L, s, 1.0, eta=0.2) == "coordination_bistability"


def test_linear_environment_threshold_width():
    low, e0, high = linear_environment_thresholds(
        static_crossing=10.0, phi_slope=0.4, eta=-0.8
    )
    assert isclose(low, 8.0)
    assert isclose(e0, 10.0)
    assert isclose(high, 12.0)
    assert isclose(high - low, 2.0 * 0.8 / 0.4)

    low2, e02, high2 = linear_environment_thresholds(
        static_crossing=10.0, phi_slope=-0.4, eta=0.8
    )
    assert isclose(low2, 8.0)
    assert isclose(e02, 10.0)
    assert isclose(high2, 12.0)


def test_switching_hysteresis():
    lower, upper = switching_hysteresis_band(c_sd=0.6, c_ds=0.3, horizon=3.0)
    assert isclose(lower, -0.1)
    assert isclose(upper, 0.2)

    assert (
        switching_action(
            "S", 0.5, phi=0.05, eta=0.0, c_sd=0.6, c_ds=0.3, horizon=3.0
        )
        == "S"
    )
    assert (
        switching_action(
            "D", 0.5, phi=0.05, eta=0.0, c_sd=0.6, c_ds=0.3, horizon=3.0
        )
        == "D"
    )

    assert (
        switching_action(
            "S", 0.5, phi=0.4, eta=0.0, c_sd=0.6, c_ds=0.3, horizon=3.0
        )
        == "D"
    )
    assert (
        switching_action(
            "D", 0.5, phi=-0.2, eta=0.0, c_sd=0.6, c_ds=0.3, horizon=3.0
        )
        == "S"
    )
