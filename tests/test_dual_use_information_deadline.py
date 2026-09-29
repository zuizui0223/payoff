import pytest

from src.dual_use_information_deadline import (
    action_threshold_given_compensation_accuracy,
    compensation_information_value,
    dual_use_information_decision,
    residual_compensation_risk,
    shared_dual_accuracy_threshold,
)


def test_compensation_information_value_is_zero_at_chance_and_half_G_at_perfect():
    assert compensation_information_value(0.5, 0.6) == pytest.approx(0.0)
    assert compensation_information_value(1.0, 0.6) == pytest.approx(0.3)
    assert residual_compensation_risk(0.5, 0.6) == pytest.approx(0.3)
    assert residual_compensation_risk(1.0, 0.6) == pytest.approx(0.0)


def test_better_compensation_information_lowers_action_threshold():
    poor = action_threshold_given_compensation_accuracy(
        0.4,
        2.0,
        1.0,
        direct_wait_cost=0.10,
        compensation_cue_accuracy=0.50,
        wrong_compensation_cost=0.40,
    )
    good = action_threshold_given_compensation_accuracy(
        0.4,
        2.0,
        1.0,
        direct_wait_cost=0.10,
        compensation_cue_accuracy=0.90,
        wrong_compensation_cost=0.40,
    )
    assert poor == pytest.approx((1.20 + 0.30) / 1.60)
    assert good == pytest.approx((1.20 + 0.14) / 1.60)
    assert good < poor


def test_shared_dual_cue_recovers_original_threshold_when_G_is_zero():
    result = shared_dual_accuracy_threshold(
        0.4,
        2.0,
        1.0,
        direct_wait_cost=0.10,
        wrong_compensation_cost=0.0,
    )
    assert result.threshold_accuracy == pytest.approx(0.8125)


def test_shared_dual_information_can_rescue_waiting_that_action_information_alone_cannot():
    result = shared_dual_accuracy_threshold(
        0.4,
        2.0,
        1.0,
        direct_wait_cost=0.20,
        wrong_compensation_cost=0.60,
    )

    # Without compensation information the effective fixed waiting cost is
    # J + G/2 = 0.50 >= R0=0.40, so action information alone never justifies
    # waiting.  If the same information package also resolves compensation
    # state, the finite shared threshold is 2.0/2.2.
    assert result.action_only_threshold_without_compensation_information is None
    assert result.ever_waits
    assert result.threshold_accuracy == pytest.approx(2.0 / 2.2)


def test_shared_dual_threshold_matches_decision_on_both_sides():
    result = shared_dual_accuracy_threshold(
        0.4,
        2.0,
        1.0,
        direct_wait_cost=0.20,
        wrong_compensation_cost=0.60,
    )
    qstar = result.threshold_accuracy
    assert qstar is not None

    below = dual_use_information_decision(
        0.4,
        qstar - 1e-4,
        2.0,
        1.0,
        direct_wait_cost=0.20,
        compensation_cue_accuracy=qstar - 1e-4,
        wrong_compensation_cost=0.60,
    )
    above = dual_use_information_decision(
        0.4,
        qstar + 1e-4,
        2.0,
        1.0,
        direct_wait_cost=0.20,
        compensation_cue_accuracy=qstar + 1e-4,
        wrong_compensation_cost=0.60,
    )
    assert not below.waits
    assert above.waits


def test_direct_wait_cost_still_sets_perfect_information_ceiling():
    result = shared_dual_accuracy_threshold(
        0.4,
        2.0,
        1.0,
        direct_wait_cost=0.40,
        wrong_compensation_cost=10.0,
    )
    # Strict tie: J=R0 means not even perfect dual-use information induces wait.
    assert not result.ever_waits
    assert result.threshold_accuracy is None
