import math

import pytest

from src.continuous_information_actionability import (
    continuous_actionability_balance,
    dimensionless_information_actionability,
    exponential_actionability_value,
    exponential_information_actionability_optimum,
    exponential_pair_desynchronization,
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



def test_pairwise_shared_information_different_recourse_rates_desynchronize():
    result = exponential_pair_desynchronization(
        0.40,
        2.0,
        1.0,
        information_rate=1.0,
        actor_1_recourse_decay_rate=0.25,
        actor_2_recourse_decay_rate=1.0,
    )
    expected_gap = abs(
        math.log(1.0 + 1.0 / 0.25)
        - math.log(1.0 + 1.0 / 1.0)
    )
    assert result.commitment_time_gap == pytest.approx(expected_gap)
    assert result.actor_2_optimal_time < result.actor_1_optimal_time
    assert (
        result.actor_2_optimal_cue_accuracy
        < result.actor_1_optimal_cue_accuracy
    )


def test_pairwise_equal_recourse_decay_has_zero_desynchronization():
    result = exponential_pair_desynchronization(
        0.40,
        2.0,
        1.0,
        information_rate=0.8,
        actor_1_recourse_decay_rate=0.4,
        actor_2_recourse_decay_rate=0.4,
    )
    assert result.commitment_time_gap == pytest.approx(0.0)
    assert result.cue_accuracy_gap == pytest.approx(0.0)


def test_faster_recourse_loss_commits_with_less_accurate_information():
    result = exponential_pair_desynchronization(
        0.40,
        2.0,
        1.0,
        information_rate=0.5,
        actor_1_recourse_decay_rate=0.1,
        actor_2_recourse_decay_rate=2.0,
    )
    assert result.actor_2_optimal_time < result.actor_1_optimal_time
    assert result.actor_2_optimal_cue_accuracy < result.actor_1_optimal_cue_accuracy
    assert result.commitment_time_gap > 0.0
    assert result.cue_accuracy_gap > 0.0



def test_dimensionless_ratio_matches_dimensional_solution():
    alpha = 0.6
    beta = 0.2
    chi = alpha / beta
    dimless = dimensionless_information_actionability(chi)
    dimensional = exponential_information_actionability_optimum(
        0.40,
        2.0,
        1.0,
        information_rate=alpha,
        recourse_decay_rate=beta,
    )
    assert beta * dimensional.optimal_time == pytest.approx(
        dimless.scaled_optimal_time_beta_t
    )
    assert (
        (dimensional.optimal_cue_accuracy - dimensional.actionable_cue_accuracy)
        / (1.0 - dimensional.actionable_cue_accuracy)
        == pytest.approx(dimless.cue_progress_fraction)
    )
    assert dimensional.optimal_recourse == pytest.approx(
        dimless.optimal_recourse
    )


def test_information_actionability_ratio_orders_exploitable_information():
    slow_info = dimensionless_information_actionability(0.1)
    balanced = dimensionless_information_actionability(1.0)
    fast_info = dimensionless_information_actionability(10.0)

    assert (
        slow_info.normalized_maximum_value
        < balanced.normalized_maximum_value
        < fast_info.normalized_maximum_value
    )
    assert (
        slow_info.cue_progress_fraction
        < balanced.cue_progress_fraction
        < fast_info.cue_progress_fraction
    )
    assert (
        slow_info.optimal_recourse
        < balanced.optimal_recourse
        < fast_info.optimal_recourse
    )
    assert (
        slow_info.scaled_optimal_time_beta_t
        > balanced.scaled_optimal_time_beta_t
        > fast_info.scaled_optimal_time_beta_t
    )


def test_balanced_information_actionability_ratio_has_simple_values():
    result = dimensionless_information_actionability(1.0)
    assert result.scaled_optimal_time_beta_t == pytest.approx(math.log(2.0))
    assert result.cue_progress_fraction == pytest.approx(0.5)
    assert result.optimal_recourse == pytest.approx(0.5)
    assert result.normalized_maximum_value == pytest.approx(0.25)


def test_slow_information_limit_is_close_to_chi_over_e():
    chi = 1e-5
    result = dimensionless_information_actionability(chi)
    assert result.scaled_optimal_time_beta_t == pytest.approx(1.0, rel=1e-5)
    assert result.optimal_recourse == pytest.approx(math.exp(-1.0), rel=1e-5)
    assert result.normalized_maximum_value == pytest.approx(
        chi / math.e,
        rel=2e-5,
    )


def test_fast_information_limit_approaches_full_information_before_recourse_loss():
    result = dimensionless_information_actionability(1e6)
    assert result.scaled_optimal_time_beta_t < 2e-5
    assert result.cue_progress_fraction > 0.999999 - 1e-9
    assert result.optimal_recourse > 0.99998
    assert result.normalized_maximum_value > 0.99998
