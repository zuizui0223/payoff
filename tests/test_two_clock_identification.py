import pytest

from src.two_clock_identification import (
    infer_information_and_effective_gain,
    reduced_actionability_from_gates,
    separate_readiness_and_decision_gain,
    two_clock_forward,
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
