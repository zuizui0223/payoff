import math

import pytest

from src.continuous_information_actionability import (
    continuous_actionability_balance,
    exponential_actionability_value,
    exponential_information_actionability_optimum,
)


def test_general_first_order_decomposition_is_exact():
    point = continuous_actionability_balance(
        0.40,
        2.0,
        1.0,
        cue_accuracy=0.85,
        retained_actionability=0.60,
        cue_accuracy_rate=0.04,
        actionability_rate=-0.03,
        cumulative_wait_cost=0.02,
        marginal_wait_cost_rate=0.01,
    )
    assert point.canonical_information_value > 0.0
    assert point.actionable_information_value > 0.0
    assert point.net_derivative == pytest.approx(
        point.actionable_information_value * point.balance_residual
    )


def test_continuous_balance_fails_closed_at_actionability_kink():
    with pytest.raises(ValueError, match="actionable cue kink"):
        continuous_actionability_balance(
            0.40,
            2.0,
            1.0,
            cue_accuracy=0.75,
            retained_actionability=1.0,
            cue_accuracy_rate=0.1,
            actionability_rate=-0.1,
        )


@pytest.mark.parametrize(
    ("alpha", "beta"),
    [
        (0.25, 0.10),
        (0.50, 0.50),
        (1.00, 0.20),
        (2.00, 1.50),
    ],
)
def test_exponential_optimum_matches_closed_form_balance(alpha, beta):
    result = exponential_information_actionability_optimum(
        0.40,
        2.0,
        1.0,
        information_rate=alpha,
        recourse_decay_rate=beta,
    )
    expected_t = math.log1p(alpha / beta) / alpha
    assert result.optimal_time == pytest.approx(expected_t)
    assert result.relative_information_gain_rate == pytest.approx(beta)
    assert result.recourse_attrition_rate == pytest.approx(beta)


@pytest.mark.parametrize(
    ("alpha", "beta"),
    [
        (0.25, 0.10),
        (0.50, 0.50),
        (1.00, 0.20),
    ],
)
def test_exponential_closed_form_is_local_and_global_maximum(alpha, beta):
    result = exponential_information_actionability_optimum(
        0.40,
        2.0,
        1.0,
        information_rate=alpha,
        recourse_decay_rate=beta,
    )
    t = result.optimal_time
    center = exponential_actionability_value(
        0.40,
        2.0,
        1.0,
        information_rate=alpha,
        recourse_decay_rate=beta,
        time=t,
    )
    before = exponential_actionability_value(
        0.40,
        2.0,
        1.0,
        information_rate=alpha,
        recourse_decay_rate=beta,
        time=max(0.0, t - 1e-4),
    )
    after = exponential_actionability_value(
        0.40,
        2.0,
        1.0,
        information_rate=alpha,
        recourse_decay_rate=beta,
        time=t + 1e-4,
    )
    far_early = exponential_actionability_value(
        0.40,
        2.0,
        1.0,
        information_rate=alpha,
        recourse_decay_rate=beta,
        time=0.0,
    )
    far_late = exponential_actionability_value(
        0.40,
        2.0,
        1.0,
        information_rate=alpha,
        recourse_decay_rate=beta,
        time=t + 100.0 / min(alpha, beta),
    )

    assert center == pytest.approx(result.maximum_actionable_information_value)
    assert center >= before
    assert center >= after
    assert center > far_early
    assert center > far_late


def test_faster_information_acquisition_moves_optimum_earlier_when_attrition_fixed():
    slow = exponential_information_actionability_optimum(
        0.40,
        2.0,
        1.0,
        information_rate=0.2,
        recourse_decay_rate=0.5,
    )
    fast = exponential_information_actionability_optimum(
        0.40,
        2.0,
        1.0,
        information_rate=1.0,
        recourse_decay_rate=0.5,
    )
    assert fast.optimal_time < slow.optimal_time
    assert fast.maximum_actionable_information_value > slow.maximum_actionable_information_value


def test_faster_recourse_loss_moves_optimum_earlier_and_reduces_value():
    slow_loss = exponential_information_actionability_optimum(
        0.40,
        2.0,
        1.0,
        information_rate=0.5,
        recourse_decay_rate=0.1,
    )
    fast_loss = exponential_information_actionability_optimum(
        0.40,
        2.0,
        1.0,
        information_rate=0.5,
        recourse_decay_rate=1.0,
    )
    assert fast_loss.optimal_time < slow_loss.optimal_time
    assert (
        fast_loss.maximum_actionable_information_value
        < slow_loss.maximum_actionable_information_value
    )


def test_equal_information_and_recourse_rates_have_simple_optimum():
    result = exponential_information_actionability_optimum(
        0.40,
        2.0,
        1.0,
        information_rate=1.0,
        recourse_decay_rate=1.0,
    )
    assert result.optimal_time == pytest.approx(math.log(2.0))
    assert result.optimal_cue_accuracy == pytest.approx(0.875)
    assert result.optimal_recourse == pytest.approx(0.5)
    # Canonical q0=0.75, S=1.6 => max = 0.5*1.6*(0.875-0.75)=0.1.
    assert result.maximum_actionable_information_value == pytest.approx(0.1)
