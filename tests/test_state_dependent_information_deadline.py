import pytest

from src.state_dependent_information_deadline import (
    conditional_threshold_shift,
    expected_context_delay_cost,
    expected_state_dependent_delay_cost,
    hidden_deadline_decision,
    state_dependent_information_threshold,
    state_dependent_pair_window_width,
)


def test_equal_state_costs_recover_fixed_D_theorem():
    result = state_dependent_information_threshold(
        0.4,
        2.0,
        1.0,
        delay_cost_normal=0.10,
        delay_cost_early=0.10,
    )
    assert result.expected_delay_cost == pytest.approx(0.10)
    assert result.wait_threshold == pytest.approx(0.8125)


def test_hidden_state_cost_is_prior_weighted():
    assert expected_state_dependent_delay_cost(
        0.4, 0.10, 0.30
    ) == pytest.approx(0.18)


def test_generic_hidden_context_uses_commitment_time_expectation():
    assert expected_context_delay_cost(
        [0.75, 0.25], [0.10, 0.50]
    ) == pytest.approx(0.20)


def test_state_dependent_cost_shifts_threshold_upward():
    fixed = state_dependent_information_threshold(
        0.4, 2.0, 1.0,
        delay_cost_normal=0.10,
        delay_cost_early=0.10,
    )
    variable = state_dependent_information_threshold(
        0.4, 2.0, 1.0,
        delay_cost_normal=0.10,
        delay_cost_early=0.30,
    )
    assert fixed.wait_threshold == pytest.approx(0.8125)
    assert variable.wait_threshold == pytest.approx(
        (1.20 + 0.18) / 1.60
    )
    assert variable.wait_threshold > fixed.wait_threshold


def test_pair_window_uses_expected_deadline_gap():
    width = state_dependent_pair_window_width(
        0.4, 2.0, 1.0,
        actor_1_delay_normal=0.05,
        actor_1_delay_early=0.10,
        actor_2_delay_normal=0.15,
        actor_2_delay_early=0.30,
    )
    d1 = 0.6 * 0.05 + 0.4 * 0.10
    d2 = 0.6 * 0.15 + 0.4 * 0.30
    assert width == pytest.approx((d2 - d1) / 1.60)


def test_high_expected_state_dependent_cost_can_remove_waiting():
    result = state_dependent_information_threshold(
        0.4, 2.0, 1.0,
        delay_cost_normal=0.50,
        delay_cost_early=0.50,
    )
    assert not result.ever_waits
    assert result.wait_threshold is None


def test_ex_ante_optimum_can_reverse_ex_post_in_harsh_state():
    result = hidden_deadline_decision(
        0.4,
        0.90,
        2.0,
        1.0,
        deadline_state_probabilities=[0.75, 0.25],
        deadline_state_costs=[0.10, 0.50],
    )

    # V(0.9)=0.24 and E[D]=0.20, so waiting is optimal ex ante.
    # In the harsh state D=0.50, commitment would have been better ex post.
    assert result.information_value == pytest.approx(0.24)
    assert result.expected_delay_cost == pytest.approx(0.20)
    assert result.wait_threshold == pytest.approx(0.875)
    assert result.ex_ante_decision == "wait_for_information"
    assert result.probability_ex_post_reversal == pytest.approx(0.25)
    assert result.expected_ex_post_regret == pytest.approx(
        0.25 * (0.50 - 0.24)
    )


def test_predictable_change_in_expected_deadline_cost_moves_threshold_exactly():
    shift = conditional_threshold_shift(
        0.4,
        2.0,
        1.0,
        expected_delay_cost_before=0.10,
        expected_delay_cost_after=0.30,
    )
    assert shift == pytest.approx(0.125)
