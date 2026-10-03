import pytest

from src.two_clock_identification import (
    first_order_controller_difference,
    infer_information_and_effective_gain,
    reduced_actionability_from_gates,
    separate_readiness_and_decision_gain,
    two_clock_forward,
    two_clock_retention_sensitivity,
)


def test_forward_two_clock_retention_uses_effective_gain_product():
    result = two_clock_forward(
        passive_retention=1.0,
        readiness_gate=0.5,
        decision_gain=1.2,
        information_weight=0.8,
    )
    assert result.effective_gain == pytest.approx(0.6)
    assert result.mean_phase_retention == pytest.approx(1.0 - 0.6 * 0.8)
    assert result.innovation_free_variance_retention == pytest.approx(
        1.0 - 0.8 * 0.6 * 1.4
    )


def test_same_effective_gain_is_observationally_equivalent_without_readiness_data():
    a = two_clock_forward(
        passive_retention=0.9,
        readiness_gate=1.0,
        decision_gain=0.5,
        information_weight=0.7,
    )
    b = two_clock_forward(
        passive_retention=0.9,
        readiness_gate=0.5,
        decision_gain=1.0,
        information_weight=0.7,
    )
    assert a.effective_gain == pytest.approx(b.effective_gain)
    assert a.mean_phase_retention == pytest.approx(b.mean_phase_retention)
    assert a.innovation_free_variance_retention == pytest.approx(
        b.innovation_free_variance_retention
    )


def test_mean_and_variance_recover_information_and_effective_gain_not_G_and_g():
    P = 100.0
    Q = 4.0
    fwd = two_clock_forward(
        passive_retention=1.0,
        readiness_gate=0.5,
        decision_gain=1.2,
        information_weight=0.8,
    )
    inv = infer_information_and_effective_gain(
        P,
        fwd.innovation_free_variance_retention * P + Q,
        process_variance=Q,
        passive_retention=1.0,
        mean_phase_retention=fwd.mean_phase_retention,
    )
    assert inv.inferred_information_weight == pytest.approx(0.8)
    assert inv.inferred_effective_gain == pytest.approx(0.6)


def test_effective_gain_alone_cannot_separate_two_clocks():
    with pytest.raises(ValueError, match="not separately identified"):
        separate_readiness_and_decision_gain(0.6)


def test_independent_readiness_identifies_decision_gain():
    result = separate_readiness_and_decision_gain(
        0.6,
        readiness_gate=0.5,
    )
    assert result.decision_gain == pytest.approx(1.2)
    assert result.identified_from == "independent_readiness_gate"


def test_independent_decision_gain_identifies_readiness():
    result = separate_readiness_and_decision_gain(
        0.6,
        decision_gain=1.2,
    )
    assert result.readiness_gate == pytest.approx(0.5)
    assert result.identified_from == "independent_decision_gain"


def test_inconsistent_two_clock_components_are_rejected():
    with pytest.raises(ValueError, match="do not match"):
        separate_readiness_and_decision_gain(
            0.6,
            readiness_gate=0.5,
            decision_gain=1.0,
        )


def test_reduced_actionability_is_weighted_gate_average():
    r = reduced_actionability_from_gates(
        [1.0, 0.5, 0.0],
        weights=[2.0, 1.0, 1.0],
    )
    assert r == pytest.approx(0.625)


def test_information_has_no_phase_control_effect_when_readiness_is_closed():
    s = two_clock_retention_sensitivity(
        passive_retention=1.0,
        readiness_gate=0.0,
        decision_gain=1.0,
        information_weight=0.8,
    )
    assert s.d_lambda_d_K == pytest.approx(0.0)
    assert s.d_lambda_d_g == pytest.approx(0.0)


def test_decision_gain_has_no_effect_without_information():
    s = two_clock_retention_sensitivity(
        passive_retention=1.0,
        readiness_gate=1.0,
        decision_gain=0.5,
        information_weight=0.0,
    )
    assert s.d_lambda_d_g == pytest.approx(0.0)
    assert s.d_lambda_d_G == pytest.approx(0.0)


def test_two_clock_sensitivities_match_finite_differences():
    phi, G, g, K = 0.9, 0.7, 0.6, 0.8
    eps = 1e-6
    base = two_clock_retention_sensitivity(
        passive_retention=phi,
        readiness_gate=G,
        decision_gain=g,
        information_weight=K,
    )

    def lam(p, Gx, gx, Kx):
        return two_clock_forward(
            passive_retention=p,
            readiness_gate=Gx,
            decision_gain=gx,
            information_weight=Kx,
        ).mean_phase_retention

    fd_G = (lam(phi, G + eps, g, K) - lam(phi, G - eps, g, K)) / (2 * eps)
    fd_g = (lam(phi, G, g + eps, K) - lam(phi, G, g - eps, K)) / (2 * eps)
    fd_K = (lam(phi, G, g, K + eps) - lam(phi, G, g, K - eps)) / (2 * eps)
    fd_phi = (lam(phi + eps, G, g, K) - lam(phi - eps, G, g, K)) / (2 * eps)

    assert fd_G == pytest.approx(base.d_lambda_d_G, rel=1e-6)
    assert fd_g == pytest.approx(base.d_lambda_d_g, rel=1e-6)
    assert fd_K == pytest.approx(base.d_lambda_d_K, rel=1e-6)
    assert fd_phi == pytest.approx(base.d_lambda_d_phi, rel=1e-6)


def test_first_order_difference_matches_small_exact_actor_difference():
    phi, G, g, K = 0.9, 0.7, 0.6, 0.8
    dG, dK = 1e-5, -2e-5

    approx = first_order_controller_difference(
        passive_retention=phi,
        readiness_gate=G,
        decision_gain=g,
        information_weight=K,
        delta_G=dG,
        delta_K=dK,
    )
    exact = (
        two_clock_forward(
            passive_retention=phi,
            readiness_gate=G + dG,
            decision_gain=g,
            information_weight=K + dK,
        ).mean_phase_retention
        - two_clock_forward(
            passive_retention=phi,
            readiness_gate=G,
            decision_gain=g,
            information_weight=K,
        ).mean_phase_retention
    )
    assert approx == pytest.approx(exact, rel=1e-4, abs=1e-10)


def test_closed_opportunity_gate_blocks_active_correction():
    result = two_clock_forward(
        passive_retention=1.0,
        readiness_gate=1.0,
        opportunity_gate=0.0,
        decision_gain=1.0,
        information_weight=1.0,
    )
    assert result.effective_gain == pytest.approx(0.0)
    assert result.mean_phase_retention == pytest.approx(1.0)


def test_information_has_no_effect_after_opportunity_closes():
    s = two_clock_retention_sensitivity(
        passive_retention=1.0,
        readiness_gate=1.0,
        opportunity_gate=0.0,
        decision_gain=1.0,
        information_weight=0.8,
    )
    assert s.d_lambda_d_K == pytest.approx(0.0)
    assert s.d_lambda_d_g == pytest.approx(0.0)


def test_reduced_actionability_requires_readiness_and_opportunity_overlap():
    r = reduced_actionability_from_gates(
        [1.0, 0.5, 1.0],
        opportunity_gates=[0.0, 1.0, 0.5],
        weights=[1.0, 1.0, 2.0],
    )
    # weighted usable gates: 1*0 + .5*1 + 2*1*.5 = 1.5; total weight=4
    assert r == pytest.approx(0.375)


def test_separating_readiness_requires_known_opportunity_gate():
    result = separate_readiness_and_decision_gain(
        0.3,
        readiness_gate=0.5,
        opportunity_gate=0.5,
    )
    assert result.decision_gain == pytest.approx(1.2)
