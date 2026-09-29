import pytest

from src.state_dependent_information_deadline import (
    expected_state_dependent_delay_cost,
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
