from math import isclose, isinf

from src.payoff_game import (
    QuadraticTraitArchitecture,
    architecture_payoffs,
    classify_phase,
    interior_equilibrium,
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
    assert isclose(m.recovered_loss, m.recovered_loss_via_bridge, rel_tol=1e-12, abs_tol=1e-12)


def test_separation_fraction_matches_realized_optimum_separation():
    m = QuadraticTraitArchitecture(a=1.3, b=2.1, theta1=5.0, theta2=2.0, coupling=0.8)
    x, y = m.differentiated_optima
    realized = abs(x - y) / abs(m.theta1 - m.theta2)
    assert isclose(realized, m.separation_fraction, rel_tol=1e-12, abs_tol=1e-12)


def test_full_release_at_zero_coupling():
    m = QuadraticTraitArchitecture(a=1.0, b=4.0, theta1=2.0, theta2=-2.0, coupling=0.0)
    assert m.differentiated_optima == (2.0, -2.0)
    assert isclose(m.separation_fraction, 1.0)
    assert isclose(m.differentiated_loss, 0.0)
    assert isclose(m.recovered_loss, m.conflict_load)


def test_recovery_decreases_with_coupling():
    weak = QuadraticTraitArchitecture(a=2.0, b=3.0, theta1=2.0, theta2=0.0, coupling=0.2)
    strong = QuadraticTraitArchitecture(a=2.0, b=3.0, theta1=2.0, theta2=0.0, coupling=4.0)
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


def test_critical_coupling_cases():
    base = QuadraticTraitArchitecture(a=2.0, b=3.0, theta1=2.0, theta2=-1.0)
    L = base.conflict_load

    free = QuadraticTraitArchitecture(a=2.0, b=3.0, theta1=2.0, theta2=-1.0, architecture_cost=0.0)
    assert isinf(free.critical_coupling())

    impossible = QuadraticTraitArchitecture(
        a=2.0, b=3.0, theta1=2.0, theta2=-1.0, architecture_cost=L + 1.0
    )
    assert impossible.critical_coupling() is None

    crossing = QuadraticTraitArchitecture(
        a=2.0, b=3.0, theta1=2.0, theta2=-1.0, architecture_cost=L / 2.0
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


def test_payoff_representation_matches_declared_gap():
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


def test_switching_hysteresis():
    lower, upper = switching_hysteresis_band(c_sd=0.6, c_ds=0.3, horizon=3.0)
    assert isclose(lower, -0.1)
    assert isclose(upper, 0.2)

    assert switching_action("S", 0.5, phi=0.05, eta=0.0, c_sd=0.6, c_ds=0.3, horizon=3.0) == "S"
    assert switching_action("D", 0.5, phi=0.05, eta=0.0, c_sd=0.6, c_ds=0.3, horizon=3.0) == "D"

    assert switching_action("S", 0.5, phi=0.4, eta=0.0, c_sd=0.6, c_ds=0.3, horizon=3.0) == "D"
    assert switching_action("D", 0.5, phi=-0.2, eta=0.0, c_sd=0.6, c_ds=0.3, horizon=3.0) == "S"
