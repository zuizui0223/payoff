from math import log

import pytest

from src.competitive_information_value import (
    competitive_balance_derivative,
    exponential_competitive_information_peak,
)


def test_zero_cost_balance_adds_actionability_and_exclusivity_hazards():
    # Canonical geometry: q0=0.75, S=1.6.
    # At q=0.875, V_A=0.2.
    # Relative information gain = 1.6 * 0.025 / 0.2 = 0.2.
    # Choose actionability loss 0.075 and exclusivity loss 0.125.
    out = competitive_balance_derivative(
        0.4,
        2.0,
        1.0,
        cue_accuracy=0.875,
        cue_accuracy_rate=0.025,
        retained_actionability=0.8,
        actionability_rate=-0.06,
        retained_exclusivity=0.8,
        exclusivity_rate=-0.10,
        marginal_wait_cost=0.0,
    )
    assert out.relative_information_gain == pytest.approx(0.2)
    assert out.relative_actionability_loss == pytest.approx(0.075)
    assert out.relative_exclusivity_loss == pytest.approx(0.125)
    assert out.net_derivative == pytest.approx(0.0)


def test_racing_limit_has_interior_peak_without_actionability_loss():
    out = exponential_competitive_information_peak(
        0.5,
        1.0,
        1.0,
        cue_gain_amplitude=0.5,
        alpha_information_rate=1.0,
        beta_actionability_decay=0.0,
        gamma_exclusivity_decay=1.0,
    )
    assert out.optimal_time == pytest.approx(log(2.0))
    assert out.optimal_cue_accuracy == pytest.approx(0.75)
    assert out.retained_actionability_at_optimum == pytest.approx(1.0)
    assert 0.0 < out.retained_exclusivity_at_optimum < 1.0


def test_ecological_limit_recovers_existing_actionability_peak():
    out = exponential_competitive_information_peak(
        0.5,
        1.0,
        1.0,
        cue_gain_amplitude=0.5,
        alpha_information_rate=1.0,
        beta_actionability_decay=1.0,
        gamma_exclusivity_decay=0.0,
    )
    assert out.optimal_time == pytest.approx(log(2.0))
    assert out.retained_exclusivity_at_optimum == pytest.approx(1.0)


def test_only_sum_of_decay_hazards_identifies_peak_time():
    one = exponential_competitive_information_peak(
        0.5,
        1.0,
        1.0,
        cue_gain_amplitude=0.5,
        alpha_information_rate=1.0,
        beta_actionability_decay=0.25,
        gamma_exclusivity_decay=0.75,
    )
    two = exponential_competitive_information_peak(
        0.5,
        1.0,
        1.0,
        cue_gain_amplitude=0.5,
        alpha_information_rate=1.0,
        beta_actionability_decay=0.60,
        gamma_exclusivity_decay=0.40,
    )
    assert one.total_value_decay == pytest.approx(1.0)
    assert two.total_value_decay == pytest.approx(1.0)
    assert one.optimal_time == pytest.approx(two.optimal_time)
    assert one.maximum_gross_information_value == pytest.approx(
        two.maximum_gross_information_value
    )


def test_faster_market_absorption_moves_value_peak_earlier():
    slow = exponential_competitive_information_peak(
        0.5,
        1.0,
        1.0,
        cue_gain_amplitude=0.5,
        alpha_information_rate=1.0,
        beta_actionability_decay=0.0,
        gamma_exclusivity_decay=0.2,
    )
    fast = exponential_competitive_information_peak(
        0.5,
        1.0,
        1.0,
        cue_gain_amplitude=0.5,
        alpha_information_rate=1.0,
        beta_actionability_decay=0.0,
        gamma_exclusivity_decay=2.0,
    )
    assert fast.optimal_time < slow.optimal_time
    assert fast.optimal_cue_accuracy < slow.optimal_cue_accuracy


def test_no_value_loss_hazard_has_no_finite_peak():
    with pytest.raises(ValueError, match="at least one"):
        exponential_competitive_information_peak(
            0.5,
            1.0,
            1.0,
            cue_gain_amplitude=0.5,
            alpha_information_rate=1.0,
            beta_actionability_decay=0.0,
            gamma_exclusivity_decay=0.0,
        )
