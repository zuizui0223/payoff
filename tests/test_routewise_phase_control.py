import pytest

from src.closed_loop_tracking import simulate_closed_loop_tracking
from src.routewise_phase_control import (
    gaussian_phase_update,
    infer_phase_information_weight,
    open_loop_phase_variance_step,
    population_phase_variance_step,
    stationary_gaussian_phase_variance,
    variance_retention_from_mean_phase,
    variance_retention_from_phase_moments,
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


def test_routewise_step_recovers_existing_closed_loop_tracking_recurrence():
    existing = simulate_closed_loop_tracking(
        residual_forcing=0.2,
        movement_feedback_gain=0.4,
        phenology_feedback_gain=0.0,
        initial_mismatch=1.5,
        steps=1,
        burn_in=0,
    )
    step = proportional_phase_step(
        1.5,
        1.5,
        control_gain=0.4,
        passive_retention=1.0,
        route_shift=0.2,
        advance_capacity=100.0,
        delay_capacity=100.0,
    )
    assert step.next_phase_error == pytest.approx(existing.final_mismatch)
    assert step.unclipped_closed_loop_lambda == pytest.approx(
        existing.phase_retention_lambda
    )


def test_individual_feedback_contracts_population_variance_beyond_open_loop():
    closed = population_phase_variance_step(
        100.0,
        observation_variance=25.0,
        control_gain=0.6,
        passive_retention=1.0,
        process_variance=0.0,
    )
    opened = open_loop_phase_variance_step(
        100.0,
        passive_retention=1.0,
        process_variance=0.0,
    )
    assert closed.kalman_gain == pytest.approx(0.8)
    assert closed.closed_loop_variance_multiplier == pytest.approx(
        1.0 - 0.8 * 0.6 * 1.4
    )
    assert closed.next_variance < opened


def test_uninformative_checkpoint_cannot_create_individual_variance_contraction():
    result = population_phase_variance_step(
        100.0,
        observation_variance=1e30,
        control_gain=1.0,
        passive_retention=0.9,
        process_variance=2.0,
    )
    opened = open_loop_phase_variance_step(
        100.0,
        passive_retention=0.9,
        process_variance=2.0,
    )
    assert result.kalman_gain == pytest.approx(0.0, abs=1e-12)
    assert result.next_variance == pytest.approx(opened)


def test_perfect_checkpoint_information_with_deadbeat_gain_removes_incoming_variance():
    result = population_phase_variance_step(
        100.0,
        observation_variance=0.0,
        control_gain=1.0,
        passive_retention=1.0,
        process_variance=3.0,
    )
    assert result.kalman_gain == pytest.approx(1.0)
    assert result.prepropagation_residual_variance == pytest.approx(0.0)
    assert result.next_variance == pytest.approx(3.0)


def test_same_mean_phase_retention_can_have_different_variance_funnels():
    # Hold observed mean lambda=phi(1-gK)=0.6 fixed while changing K.
    informative = population_phase_variance_step(
        100.0,
        observation_variance=25.0,  # K=0.8
        control_gain=0.5,           # gK=0.4
        passive_retention=1.0,
        process_variance=0.0,
    )
    noisy = population_phase_variance_step(
        100.0,
        observation_variance=100.0, # K=0.5
        control_gain=0.8,            # gK=0.4
        passive_retention=1.0,
        process_variance=0.0,
    )
    lam_a, rho_a = variance_retention_from_phase_moments(
        passive_retention=1.0,
        control_gain=0.5,
        information_weight=0.8,
    )
    lam_b, rho_b = variance_retention_from_phase_moments(
        passive_retention=1.0,
        control_gain=0.8,
        information_weight=0.5,
    )
    assert lam_a == pytest.approx(0.6)
    assert lam_b == pytest.approx(0.6)
    assert informative.next_variance / 100.0 == pytest.approx(rho_a)
    assert noisy.next_variance / 100.0 == pytest.approx(rho_b)
    assert informative.next_variance < noisy.next_variance


def test_feedback_gain_above_two_expands_variance_under_informative_cues():
    result = population_phase_variance_step(
        100.0,
        observation_variance=0.0,
        control_gain=2.5,
        passive_retention=1.0,
        process_variance=0.0,
    )
    assert result.closed_loop_variance_multiplier > 1.0
    assert result.next_variance > result.prior_variance


def test_stationary_variance_solves_homogeneous_variance_recursion():
    fixed = stationary_gaussian_phase_variance(
        observation_variance=25.0,
        control_gain=0.6,
        passive_retention=1.0,
        process_variance=4.0,
    )
    step = population_phase_variance_step(
        fixed.stationary_variance,
        observation_variance=25.0,
        control_gain=0.6,
        passive_retention=1.0,
        process_variance=4.0,
    )
    assert step.next_variance == pytest.approx(
        fixed.stationary_variance,
        rel=1e-10,
        abs=1e-10,
    )


def test_stationary_variance_rejects_asymptotically_unstable_feedback():
    with pytest.raises(ValueError, match="finite stationary variance"):
        stationary_gaussian_phase_variance(
            observation_variance=25.0,
            control_gain=3.0,
            passive_retention=1.0,
            process_variance=4.0,
        )


def test_noisy_mean_and_variance_retention_bridge_is_exact():
    lam, rho = variance_retention_from_phase_moments(
        passive_retention=1.0,
        control_gain=0.5,
        information_weight=0.8,
    )
    bridged = variance_retention_from_mean_phase(
        passive_retention=1.0,
        mean_phase_retention=lam,
        information_weight=0.8,
    )
    assert lam == pytest.approx(0.6)
    assert rho == pytest.approx(0.4)
    assert bridged == pytest.approx(rho)


def test_phase_sense_inverse_recovers_information_gain_and_observation_variance():
    p = 100.0
    phi = 1.0
    g = 0.5
    k = 0.8
    qvar = 4.0
    lam, rho = variance_retention_from_phase_moments(
        passive_retention=phi,
        control_gain=g,
        information_weight=k,
    )
    pnext = rho * p + qvar
    inv = infer_phase_information_weight(
        p,
        pnext,
        process_variance=qvar,
        passive_retention=phi,
        mean_phase_retention=lam,
    )
    assert lam == pytest.approx(0.6)
    assert inv.inferred_information_weight == pytest.approx(k)
    assert inv.inferred_control_gain == pytest.approx(g)
    assert inv.inferred_observation_variance == pytest.approx(25.0)


def test_phase_sense_inverse_rejects_moments_outside_declared_feedback_envelope():
    with pytest.raises(ValueError, match="outside|incompatible"):
        infer_phase_information_weight(
            100.0,
            150.0,
            process_variance=0.0,
            passive_retention=1.0,
            mean_phase_retention=0.6,
        )


def test_phase_sense_inverse_requires_nonzero_observable_feedback_product():
    with pytest.raises(ValueError, match="not separately identified"):
        infer_phase_information_weight(
            100.0,
            100.0,
            process_variance=0.0,
            passive_retention=1.0,
            mean_phase_retention=1.0,
        )
