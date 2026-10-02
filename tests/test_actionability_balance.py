from math import exp, log

import pytest

from src.actionability_balance import (
    canonical_actionability_geometry,
    continuous_balance_derivative,
    exponential_actionability_peak,
    exponential_peak_with_linear_wait_cost,
    pairwise_exponential_commitment_gap,
)


def test_canonical_geometry_matches_paper2_example():
    g = canonical_actionability_geometry(0.4, 2.0, 1.0)
    assert g.early_action_prior_loss == pytest.approx(1.2)
    assert g.late_action_prior_loss == pytest.approx(0.4)
    assert g.total_loss_scale == pytest.approx(1.6)
    assert g.larger_prior_action_loss == pytest.approx(1.2)
    assert g.prior_bayes_risk == pytest.approx(0.4)
    assert g.actionable_cue_accuracy == pytest.approx(0.75)


def test_zero_cost_balance_is_relative_information_gain_equals_optionality_loss():
    # Canonical q0=0.75, S=1.6. At q=0.875, V_A=0.2.
    # Choose qdot=0.025 and r=0.8. The relative information gain is
    # S*qdot/V_A = 1.6*0.025/0.2 = 0.2.
    # Set rdot=-0.16, so -rdot/r = 0.2.
    d = continuous_balance_derivative(
        0.4,
        2.0,
        1.0,
        cue_accuracy=0.875,
        cue_accuracy_rate=0.025,
        retained_actionability=0.8,
        actionability_rate=-0.16,
        marginal_wait_cost=0.0,
    )
    assert d.information_value == pytest.approx(0.2)
    assert d.zero_cost_relative_information_gain == pytest.approx(0.2)
    assert d.zero_cost_relative_actionability_loss == pytest.approx(0.2)
    assert d.net_derivative == pytest.approx(0.0)


def test_positive_marginal_wait_cost_moves_same_balance_point_to_commit_side():
    d = continuous_balance_derivative(
        0.4,
        2.0,
        1.0,
        cue_accuracy=0.875,
        cue_accuracy_rate=0.025,
        retained_actionability=0.8,
        actionability_rate=-0.16,
        marginal_wait_cost=0.01,
    )
    assert d.net_derivative == pytest.approx(-0.01)


def test_derivative_fails_closed_below_actionability_boundary():
    with pytest.raises(ValueError, match="strictly above"):
        continuous_balance_derivative(
            0.4,
            2.0,
            1.0,
            cue_accuracy=0.75,
            cue_accuracy_rate=0.1,
            retained_actionability=0.8,
            actionability_rate=-0.1,
        )


def test_exponential_peak_has_exact_closed_form():
    out = exponential_actionability_peak(
        0.4,
        2.0,
        1.0,
        cue_gain_amplitude=0.20,
        alpha_information_rate=0.5,
        beta_actionability_decay=0.25,
    )
    expected = log(1.0 + 0.5 / 0.25) / 0.5
    assert out.optimal_time == pytest.approx(expected)
    assert out.optimal_time > 0.0
    assert 0.75 < out.optimal_cue_accuracy < 0.95
    assert 0.0 < out.retained_actionability_at_optimum < 1.0
    assert out.maximum_gross_information_value > 0.0


def test_faster_recourse_decay_forces_earlier_commitment_under_same_cue_path():
    slow_loss = exponential_actionability_peak(
        0.4,
        2.0,
        1.0,
        cue_gain_amplitude=0.20,
        alpha_information_rate=0.5,
        beta_actionability_decay=0.10,
    )
    fast_loss = exponential_actionability_peak(
        0.4,
        2.0,
        1.0,
        cue_gain_amplitude=0.20,
        alpha_information_rate=0.5,
        beta_actionability_decay=0.80,
    )
    assert fast_loss.optimal_time < slow_loss.optimal_time
    assert fast_loss.optimal_cue_accuracy < slow_loss.optimal_cue_accuracy


def test_pairwise_gap_is_created_by_recourse_decay_alone():
    out = pairwise_exponential_commitment_gap(
        0.4,
        2.0,
        1.0,
        cue_gain_amplitude=0.20,
        alpha_information_rate=0.5,
        actor_1_beta=0.8,
        actor_2_beta=0.1,
    )
    assert out.earlier_committing_actor == 1
    assert out.actor_1_optimal_time < out.actor_2_optimal_time
    assert out.absolute_time_gap == pytest.approx(
        out.actor_2_optimal_time - out.actor_1_optimal_time
    )


def test_equal_recourse_decay_gives_zero_pairwise_gap():
    out = pairwise_exponential_commitment_gap(
        0.4,
        2.0,
        1.0,
        cue_gain_amplitude=0.20,
        alpha_information_rate=0.5,
        actor_1_beta=0.3,
        actor_2_beta=0.3,
    )
    assert out.earlier_committing_actor is None
    assert out.absolute_time_gap == pytest.approx(0.0)


def test_zero_cost_exponential_peak_is_strictly_interior_and_not_perfect_information():
    out = exponential_actionability_peak(
        0.5,
        1.0,
        1.0,
        cue_gain_amplitude=0.5,
        alpha_information_rate=1.0,
        beta_actionability_decay=1.0,
    )
    # Symmetric q0=0.5 and q(infinity)=1.0, but the optimal commitment occurs
    # before perfect information because actionability is decaying.
    assert out.optimal_time == pytest.approx(log(2.0))
    assert out.optimal_cue_accuracy == pytest.approx(0.75)
    assert out.optimal_cue_accuracy < 1.0


def test_linear_wait_cost_moves_peak_earlier():
    no_cost = exponential_peak_with_linear_wait_cost(
        gross_scale=1.0,
        alpha_information_rate=1.0,
        beta_actionability_decay=0.5,
        marginal_wait_cost=0.0,
    )
    costly = exponential_peak_with_linear_wait_cost(
        gross_scale=1.0,
        alpha_information_rate=1.0,
        beta_actionability_decay=0.5,
        marginal_wait_cost=0.15,
    )
    assert costly.optimal_time < no_cost.optimal_time
    assert costly.optimal_time > 0.0
    assert costly.immediate_commitment is False


def test_sufficiently_large_linear_wait_cost_makes_immediate_commitment_optimal():
    # Initial marginal information value is K*alpha = 1 here.
    out = exponential_peak_with_linear_wait_cost(
        gross_scale=1.0,
        alpha_information_rate=1.0,
        beta_actionability_decay=0.5,
        marginal_wait_cost=1.0,
    )
    assert out.optimal_time == pytest.approx(0.0)
    assert out.immediate_commitment is True
    assert out.net_value_at_optimum == pytest.approx(0.0)


def test_wait_cost_peak_root_satisfies_first_order_condition():
    out = exponential_peak_with_linear_wait_cost(
        gross_scale=1.7,
        alpha_information_rate=0.8,
        beta_actionability_decay=0.3,
        marginal_wait_cost=0.2,
    )
    t = out.optimal_time
    gross_slope = (
        1.7
        * exp(-0.3 * t)
        * ((0.8 + 0.3) * exp(-0.8 * t) - 0.3)
    )
    assert gross_slope == pytest.approx(0.2, abs=1e-10)
