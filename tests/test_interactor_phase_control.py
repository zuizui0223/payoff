import pytest

from src.interactor_phase_control import (
    effective_noisy_phase_retention,
    mismatch_created_from_shared_error,
    pairwise_phase_step,
    shared_passive_mismatch_from_information_control,
    shared_passive_mismatch_from_readiness_information_control,
    stationary_shared_forcing_mismatch,
)


def test_noisy_retention_recovers_perfect_information_special_case():
    lam = effective_noisy_phase_retention(
        passive_retention=0.8,
        control_gain=0.4,
        information_weight=1.0,
    )
    assert lam == pytest.approx(0.8 * 0.6)


def test_identical_controllers_do_not_create_mismatch_from_shared_error():
    assert mismatch_created_from_shared_error(
        10.0,
        lambda_1=0.4,
        lambda_2=0.4,
    ) == pytest.approx(0.0)


def test_controller_asymmetry_converts_common_error_into_mismatch():
    delta = mismatch_created_from_shared_error(
        10.0,
        lambda_1=0.8,
        lambda_2=0.3,
    )
    assert delta == pytest.approx(5.0)


def test_pairwise_common_and_differential_mode_identities():
    result = pairwise_phase_step(
        8.0,
        2.0,
        lambda_1=0.75,
        lambda_2=0.25,
        innovation_1=1.0,
        innovation_2=1.0,
    )
    assert result.mean_phase_error == pytest.approx(5.0)
    assert result.interaction_mismatch == pytest.approx(6.0)
    assert result.mean_retention == pytest.approx(0.5)
    assert result.retention_difference == pytest.approx(0.5)
    assert result.next_phase_error_1 == pytest.approx(7.0)
    assert result.next_phase_error_2 == pytest.approx(1.5)
    assert result.next_interaction_mismatch == pytest.approx(5.5)


def test_synchronized_pair_diverges_after_common_error_if_controllers_differ():
    result = pairwise_phase_step(
        6.0,
        6.0,
        lambda_1=0.8,
        lambda_2=0.2,
        innovation_1=0.0,
        innovation_2=0.0,
    )
    assert result.interaction_mismatch == pytest.approx(0.0)
    assert result.next_interaction_mismatch == pytest.approx(3.6)


def test_stationary_shared_forcing_generates_persistent_mismatch():
    result = stationary_shared_forcing_mismatch(
        2.0,
        lambda_1=0.8,
        lambda_2=0.5,
    )
    assert result.stationary_error_1 == pytest.approx(10.0)
    assert result.stationary_error_2 == pytest.approx(4.0)
    assert result.stationary_mismatch == pytest.approx(6.0)


def test_stationary_mismatch_requires_stable_controllers():
    with pytest.raises(ValueError, match="requires"):
        stationary_shared_forcing_mismatch(
            1.0,
            lambda_1=1.0,
            lambda_2=0.5,
        )


def test_information_asymmetry_alone_can_generate_mismatch():
    delta = shared_passive_mismatch_from_information_control(
        10.0,
        passive_retention=1.0,
        control_gain_1=0.8,
        information_weight_1=0.9,
        control_gain_2=0.8,
        information_weight_2=0.4,
    )
    # lambda1=0.28, lambda2=0.68, so actor 1 is 4 d less delayed next step.
    assert delta == pytest.approx(-4.0)


def test_feedback_gain_asymmetry_alone_can_generate_mismatch():
    delta = shared_passive_mismatch_from_information_control(
        10.0,
        passive_retention=1.0,
        control_gain_1=0.9,
        information_weight_1=0.8,
        control_gain_2=0.4,
        information_weight_2=0.8,
    )
    assert delta == pytest.approx(-4.0)


def test_closed_readiness_gate_removes_active_correction():
    lam = effective_noisy_phase_retention(
        passive_retention=0.8,
        readiness_gate=0.0,
        control_gain=1.0,
        information_weight=1.0,
    )
    assert lam == pytest.approx(0.8)


def test_readiness_asymmetry_alone_can_generate_mismatch():
    delta = shared_passive_mismatch_from_readiness_information_control(
        10.0,
        passive_retention=1.0,
        readiness_gate_1=1.0,
        control_gain_1=0.8,
        information_weight_1=0.8,
        readiness_gate_2=0.25,
        control_gain_2=0.8,
        information_weight_2=0.8,
    )
    # active products: 0.64 versus 0.16, so lambda1-lambda2=-0.48
    assert delta == pytest.approx(-4.8)


def test_same_readiness_but_information_difference_recovers_decision_clock_case():
    full = shared_passive_mismatch_from_readiness_information_control(
        10.0,
        passive_retention=1.0,
        readiness_gate_1=1.0,
        control_gain_1=0.8,
        information_weight_1=0.9,
        readiness_gate_2=1.0,
        control_gain_2=0.8,
        information_weight_2=0.4,
    )
    decision_only = shared_passive_mismatch_from_information_control(
        10.0,
        passive_retention=1.0,
        control_gain_1=0.8,
        information_weight_1=0.9,
        control_gain_2=0.8,
        information_weight_2=0.4,
    )
    assert full == pytest.approx(decision_only)


def test_fractional_readiness_gate_is_bounded():
    with pytest.raises(ValueError, match="readiness_gate"):
        effective_noisy_phase_retention(
            passive_retention=1.0,
            readiness_gate=1.2,
            control_gain=0.5,
            information_weight=0.5,
        )
