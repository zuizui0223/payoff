import pytest

from src.routewise_phase_control import (
    gaussian_phase_update,
    optimal_quadratic_phase_correction,
    proportional_phase_step,
    routewise_gaussian_phase_control,
)


def test_checkpoint_information_reduces_phase_uncertainty():
    result = gaussian_phase_update(
        prior_mean=0.0,
        prior_variance=4.0,
        observation=10.0,
        observation_variance=1.0,
    )
    assert result.kalman_gain == pytest.approx(0.8)
    assert result.posterior_mean == pytest.approx(8.0)
    assert result.posterior_variance == pytest.approx(0.8)


def test_perfect_checkpoint_cue_reveals_phase_error():
    result = gaussian_phase_update(
        prior_mean=-5.0,
        prior_variance=9.0,
        observation=3.0,
        observation_variance=0.0,
    )
    assert result.kalman_gain == pytest.approx(1.0)
    assert result.posterior_mean == pytest.approx(3.0)
    assert result.posterior_variance == pytest.approx(0.0)


def test_quadratic_controller_speeds_up_when_late_and_slows_when_early():
    late = optimal_quadratic_phase_correction(
        10.0,
        1.0,
        control_weight=1.0,
        residual_weight=3.0,
        advance_capacity=20.0,
        delay_capacity=20.0,
    )
    early = optimal_quadratic_phase_correction(
        -10.0,
        1.0,
        control_weight=1.0,
        residual_weight=3.0,
        advance_capacity=20.0,
        delay_capacity=20.0,
    )
    assert late.unconstrained_gain == pytest.approx(0.75)
    assert late.correction == pytest.approx(7.5)
    assert early.correction == pytest.approx(-7.5)
    assert late.mode == "speed_up_or_compress"
    assert early.mode == "slow_or_wait"


def test_phase_retention_decomposes_into_passive_retention_and_feedback_gain():
    step = proportional_phase_step(
        10.0,
        10.0,
        control_gain=0.4,
        passive_retention=0.8,
        route_shift=0.0,
        advance_capacity=100.0,
        delay_capacity=100.0,
    )
    assert step.correction == pytest.approx(4.0)
    assert step.next_phase_error == pytest.approx(4.8)
    assert step.unclipped_closed_loop_lambda == pytest.approx(0.48)
    assert step.next_phase_error / step.phase_error == pytest.approx(
        step.unclipped_closed_loop_lambda
    )


def test_gain_one_resets_checkpoint_phase_error_when_target_does_not_shift():
    step = proportional_phase_step(
        -12.0,
        -12.0,
        control_gain=1.0,
        passive_retention=0.9,
        route_shift=0.0,
        advance_capacity=100.0,
        delay_capacity=100.0,
    )
    assert step.correction == pytest.approx(-12.0)
    assert step.next_phase_error == pytest.approx(0.0)
    assert step.unclipped_closed_loop_lambda == pytest.approx(0.0)


def test_gain_above_one_produces_phase_overshoot_and_negative_lambda():
    step = proportional_phase_step(
        10.0,
        10.0,
        control_gain=1.25,
        passive_retention=0.8,
        route_shift=0.0,
        advance_capacity=100.0,
        delay_capacity=100.0,
    )
    assert step.next_phase_error == pytest.approx(-2.0)
    assert step.unclipped_closed_loop_lambda == pytest.approx(-0.2)


def test_capacity_limit_prevents_full_schedule_recovery():
    step = proportional_phase_step(
        20.0,
        20.0,
        control_gain=1.0,
        passive_retention=1.0,
        route_shift=0.0,
        advance_capacity=6.0,
        delay_capacity=6.0,
    )
    assert step.correction == pytest.approx(6.0)
    assert step.next_phase_error == pytest.approx(14.0)


def test_routewise_feedback_can_reduce_large_departure_error_across_checkpoints():
    route = routewise_gaussian_phase_control(
        initial_true_error=12.0,
        initial_prior_mean=10.0,
        initial_prior_variance=4.0,
        observations=[11.0, 5.0, 2.0],
        observation_variances=[1.0, 1.0, 0.5],
        passive_retentions=[1.0, 1.0, 1.0],
        route_shifts=[0.0, 0.0, 0.0],
        process_variances=[0.5, 0.5, 0.5],
        control_weight=1.0,
        residual_weight=4.0,
        advance_capacities=[5.0, 5.0, 5.0],
        delay_capacities=[5.0, 5.0, 5.0],
    )
    assert len(route) == 3
    assert abs(route[-1].next_true_phase_error) < abs(route[0].true_phase_error)
    assert route[0].correction > 0.0


def test_route_target_shift_can_recreate_error_after_successful_correction():
    step = proportional_phase_step(
        8.0,
        8.0,
        control_gain=1.0,
        passive_retention=1.0,
        route_shift=3.0,
        advance_capacity=20.0,
        delay_capacity=20.0,
    )
    assert step.residual_before_propagation == pytest.approx(0.0)
    assert step.next_phase_error == pytest.approx(3.0)
