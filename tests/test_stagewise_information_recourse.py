import pytest

from src.stagewise_information_recourse import (
    actionability_profile,
    binary_actionability_value,
    binary_schrodinger_spring,
    finite_signal_recourse,
    signed_linear_phase_recourse,
)


def test_late_actor_speeds_up_when_correction_is_cheaper_than_residual_loss():
    result = signed_linear_phase_recourse(
        20.0,
        advance_capacity=15.0,
        delay_capacity=15.0,
        correction_cost_per_unit=0.2,
        residual_loss_per_unit=1.0,
    )
    assert result.mode == "speed_up_or_compress"
    assert result.optimal_correction == pytest.approx(15.0)
    assert result.residual_phase_error == pytest.approx(5.0)
    assert result.effective_cost == pytest.approx(8.0)


def test_early_actor_slows_or_waits_under_same_recourse_rule():
    result = signed_linear_phase_recourse(
        -30.0,
        advance_capacity=20.0,
        delay_capacity=20.0,
        correction_cost_per_unit=0.2,
        residual_loss_per_unit=1.0,
    )
    assert result.mode == "slow_or_wait"
    assert result.optimal_correction == pytest.approx(-20.0)
    assert result.residual_phase_error == pytest.approx(-10.0)
    assert result.effective_cost == pytest.approx(14.0)


def test_expensive_recourse_is_not_used_in_either_direction():
    late = signed_linear_phase_recourse(
        10.0,
        advance_capacity=10.0,
        delay_capacity=10.0,
        correction_cost_per_unit=1.2,
        residual_loss_per_unit=1.0,
    )
    early = signed_linear_phase_recourse(
        -10.0,
        advance_capacity=10.0,
        delay_capacity=10.0,
        correction_cost_per_unit=1.2,
        residual_loss_per_unit=1.0,
    )
    assert late.mode == "none"
    assert early.mode == "none"
    assert late.optimal_correction == pytest.approx(0.0)
    assert early.optimal_correction == pytest.approx(0.0)


def test_more_signed_recourse_capacity_cannot_raise_effective_cost():
    early_small = signed_linear_phase_recourse(
        -20.0,
        advance_capacity=0.0,
        delay_capacity=5.0,
        correction_cost_per_unit=0.2,
        residual_loss_per_unit=1.0,
    )
    early_large = signed_linear_phase_recourse(
        -20.0,
        advance_capacity=0.0,
        delay_capacity=15.0,
        correction_cost_per_unit=0.2,
        residual_loss_per_unit=1.0,
    )
    late_small = signed_linear_phase_recourse(
        20.0,
        advance_capacity=5.0,
        delay_capacity=0.0,
        correction_cost_per_unit=0.2,
        residual_loss_per_unit=1.0,
    )
    late_large = signed_linear_phase_recourse(
        20.0,
        advance_capacity=15.0,
        delay_capacity=0.0,
        correction_cost_per_unit=0.2,
        residual_loss_per_unit=1.0,
    )
    assert early_large.effective_cost < early_small.effective_cost
    assert late_large.effective_cost < late_small.effective_cost


@pytest.mark.parametrize(
    ("q", "expected_risk", "expected_value"),
    [
        (0.5, 0.5, 0.0),
        (0.75, 0.25, 0.25),
        (1.0, 0.0, 0.5),
    ],
)
def test_schrodinger_spring_exact_binary_value(q, expected_risk, expected_value):
    result = binary_schrodinger_spring(q)
    assert result.no_signal_risk == pytest.approx(0.5)
    assert result.post_signal_risk == pytest.approx(expected_risk)
    assert result.signal_value == pytest.approx(expected_value)


def test_information_has_zero_behavioral_value_after_complete_irreversibility():
    result = binary_schrodinger_spring(
        1.0,
        allowed_actions=[0],
    )
    assert result.no_signal_risk == pytest.approx(0.5)
    assert result.post_signal_risk == pytest.approx(0.5)
    assert result.perfect_information_risk == pytest.approx(0.5)
    assert result.signal_value == pytest.approx(0.0)
    assert result.perfect_information_value == pytest.approx(0.0)


def test_more_recourse_actions_cannot_increase_post_signal_risk():
    # Three states, two noisy signals, and three possible recourse actions.
    prior = [0.2, 0.5, 0.3]
    signal = [
        [0.8, 0.2],
        [0.5, 0.5],
        [0.2, 0.8],
    ]
    losses = [
        [0.0, 1.0, 2.0],
        [1.0, 0.0, 1.0],
        [2.0, 1.0, 0.0],
    ]
    restricted = finite_signal_recourse(
        prior,
        signal,
        losses,
        allowed_actions=[1],
    )
    expanded = finite_signal_recourse(
        prior,
        signal,
        losses,
        allowed_actions=[0, 1, 2],
    )
    assert expanded.post_signal_risk <= restricted.post_signal_risk
    assert expanded.perfect_information_risk <= restricted.perfect_information_risk


def test_noisy_route_information_is_bounded_by_no_information_and_perfect_information():
    result = binary_schrodinger_spring(0.7)
    assert (
        result.perfect_information_risk
        <= result.post_signal_risk
        <= result.no_signal_risk
    )


def test_direct_cost_does_not_change_direction_of_optimal_recourse():
    late = signed_linear_phase_recourse(
        10.0,
        advance_capacity=10.0,
        delay_capacity=10.0,
        correction_cost_per_unit=0.1,
        residual_loss_per_unit=1.0,
        direct_commit_cost=5.0,
    )
    early = signed_linear_phase_recourse(
        -10.0,
        advance_capacity=10.0,
        delay_capacity=10.0,
        correction_cost_per_unit=0.1,
        residual_loss_per_unit=1.0,
        direct_commit_cost=5.0,
    )
    assert late.mode == "speed_up_or_compress"
    assert early.mode == "slow_or_wait"
    assert late.effective_cost == pytest.approx(6.0)
    assert early.effective_cost == pytest.approx(6.0)



def test_binary_actionability_exact_product_formula():
    result = binary_actionability_value(
        0.8,
        0.4,
        wrong_state_loss=2.0,
    )
    # V = r * W * (q - 1/2) = 0.4 * 2 * 0.3 = 0.24.
    assert result.no_signal_risk == pytest.approx(1.0)
    assert result.information_value == pytest.approx(0.24)
    assert result.post_signal_risk == pytest.approx(0.76)


def test_perfect_information_has_zero_value_after_optionality_is_gone():
    result = binary_actionability_value(
        1.0,
        0.0,
        wrong_state_loss=3.0,
    )
    assert result.no_signal_risk == pytest.approx(1.5)
    assert result.post_signal_risk == pytest.approx(1.5)
    assert result.information_value == pytest.approx(0.0)


def test_information_value_can_peak_before_information_quality_peaks():
    profile = actionability_profile(
        cue_accuracies=[0.55, 0.75, 0.95, 1.0],
        recourse_fractions=[1.0, 0.8, 0.3, 0.0],
    )
    values = [row.information_value for row in profile]
    assert values == pytest.approx([0.05, 0.20, 0.135, 0.0])
    assert profile[1].cue_accuracy < profile[2].cue_accuracy
    assert profile[1].information_value > profile[2].information_value
    assert profile[-1].cue_accuracy == pytest.approx(1.0)
    assert profile[-1].information_value == pytest.approx(0.0)


def test_full_recourse_recovers_standard_binary_information_value():
    for q in (0.5, 0.6, 0.8, 1.0):
        actionability = binary_actionability_value(q, 1.0)
        standard = binary_schrodinger_spring(q)
        assert actionability.information_value == pytest.approx(
            standard.signal_value
        )
        assert actionability.post_signal_risk == pytest.approx(
            standard.post_signal_risk
        )
