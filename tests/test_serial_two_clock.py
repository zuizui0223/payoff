import pytest

from src.serial_two_clock import (
    common_controller_timer_decay,
    controller_generated_mismatch,
    post_entry_phase_retention,
    serial_mismatch_decomposition,
)


def test_step_zero_returns_initial_timer_mismatch():
    r=serial_mismatch_decomposition(
        initial_mean_error=5.0,
        initial_mismatch=4.0,
        lambda_1=0.7,
        lambda_2=0.2,
        steps=0,
    )
    assert r.final_mismatch == pytest.approx(4.0)
    assert r.controller_generated_component == pytest.approx(0.0)
    assert r.timer_propagated_component == pytest.approx(4.0)


def test_equal_downstream_controllers_only_propagate_timer_mismatch():
    r=serial_mismatch_decomposition(
        initial_mean_error=10.0,
        initial_mismatch=6.0,
        lambda_1=0.5,
        lambda_2=0.5,
        steps=3,
    )
    assert r.controller_generated_component == pytest.approx(0.0)
    assert r.timer_propagated_component == pytest.approx(0.5**3*6.0)
    assert r.final_mismatch == pytest.approx(0.75)


def test_synchronized_entry_can_diverge_from_controller_asymmetry():
    r=serial_mismatch_decomposition(
        initial_mean_error=10.0,
        initial_mismatch=0.0,
        lambda_1=0.8,
        lambda_2=0.3,
        steps=2,
    )
    expected=(0.8**2-0.3**2)*10.0
    assert r.timer_propagated_component == pytest.approx(0.0)
    assert r.controller_generated_component == pytest.approx(expected)
    assert r.final_mismatch == pytest.approx(expected)


def test_two_components_sum_to_direct_actor_propagation():
    r=serial_mismatch_decomposition(
        initial_mean_error=-4.0,
        initial_mismatch=7.0,
        lambda_1=0.7,
        lambda_2=-0.2,
        steps=3,
    )
    assert r.final_mismatch == pytest.approx(
        r.controller_generated_component+r.timer_propagated_component
    )


def test_common_controller_decay_helper():
    assert common_controller_timer_decay(
        8.0,phase_retention=0.25,steps=2
    ) == pytest.approx(0.5)


def test_controller_generated_helper():
    assert controller_generated_mismatch(
        6.0,lambda_1=0.5,lambda_2=0.25,steps=2
    ) == pytest.approx((0.25-0.0625)*6.0)


def test_post_entry_controller_excludes_readiness_by_default():
    r=post_entry_phase_retention(
        passive_retention=1.0,
        opportunity_gate=0.8,
        information_weight=0.5,
        decision_gain=0.75,
    )
    assert r.effective_post_entry_gain == pytest.approx(0.6)
    assert r.phase_retention == pytest.approx(0.7)


def test_invalid_opportunity_gate_is_rejected():
    with pytest.raises(ValueError,match="opportunity_gate"):
        post_entry_phase_retention(
            passive_retention=1.0,
            opportunity_gate=1.2,
            information_weight=0.5,
            decision_gain=0.5,
        )
