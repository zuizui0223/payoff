import math

import pytest

from src.continuous_information_actionability import (
    continuous_actionability_balance,
    dimensionless_information_actionability,
    dimensionless_maximum_log_derivative,
    dimensionless_scaled_time_derivative,
    exponential_actionability_value,
    exponential_information_actionability_optimum,
    exponential_mechanism_sensitivity,
    exponential_pair_desynchronization,
    normalized_pairwise_cue_gap,
    pairwise_commitment_time_gap,
    pairwise_information_rate_geometry,
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



@pytest.mark.parametrize("chi", [0.01, 0.1, 1.0, 10.0, 100.0])
def test_dimensionless_maximum_is_strictly_increasing(chi):
    assert dimensionless_maximum_log_derivative(chi) > 0.0


@pytest.mark.parametrize("chi", [0.01, 0.1, 1.0, 10.0, 100.0])
def test_scaled_optimal_time_is_strictly_decreasing(chi):
    assert dimensionless_scaled_time_derivative(chi) < 0.0


def test_dimensionless_derivatives_match_finite_differences():
    chi = 2.5
    eps = 1e-6
    left = dimensionless_information_actionability(chi - eps)
    right = dimensionless_information_actionability(chi + eps)

    finite_log_g = (
        math.log(right.normalized_maximum_value)
        - math.log(left.normalized_maximum_value)
    ) / (2.0 * eps)
    finite_tau = (
        right.scaled_optimal_time_beta_t
        - left.scaled_optimal_time_beta_t
    ) / (2.0 * eps)

    assert finite_log_g == pytest.approx(
        dimensionless_maximum_log_derivative(chi),
        rel=1e-6,
    )
    assert finite_tau == pytest.approx(
        dimensionless_scaled_time_derivative(chi),
        rel=1e-6,
    )



def test_pairwise_time_gap_shrinks_with_faster_information():
    beta1 = 0.2
    beta2 = 1.0
    gaps = [
        pairwise_commitment_time_gap(alpha, beta1, beta2)
        for alpha in (0.05, 0.2, 1.0, 5.0, 20.0)
    ]
    assert gaps == sorted(gaps, reverse=True)


def test_pairwise_time_gap_has_correct_slow_information_limit():
    beta1 = 0.2
    beta2 = 1.0
    geometry = pairwise_information_rate_geometry(beta1, beta2)
    tiny = pairwise_commitment_time_gap(1e-7, beta1, beta2)
    assert tiny == pytest.approx(
        geometry.slow_information_time_gap_limit,
        rel=1e-6,
    )


def test_pairwise_time_gap_tends_to_zero_for_fast_information():
    gap = pairwise_commitment_time_gap(
        1e8,
        0.2,
        1.0,
    )
    assert gap < 1e-6


def test_pairwise_cue_gap_peaks_at_geometric_mean_information_rate():
    beta1 = 0.25
    beta2 = 4.0
    geometry = pairwise_information_rate_geometry(beta1, beta2)
    alpha_peak = geometry.cue_gap_peak_information_rate
    assert alpha_peak == pytest.approx(1.0)

    center = normalized_pairwise_cue_gap(alpha_peak, beta1, beta2)
    left = normalized_pairwise_cue_gap(alpha_peak * 0.5, beta1, beta2)
    right = normalized_pairwise_cue_gap(alpha_peak * 2.0, beta1, beta2)

    assert center > left
    assert center > right
    assert center == pytest.approx(
        geometry.maximum_cue_accuracy_gap_fraction
    )


def test_pairwise_cue_gap_peak_has_closed_form_square_root_ratio():
    beta1 = 1.0
    beta2 = 9.0
    geometry = pairwise_information_rate_geometry(beta1, beta2)
    # |3-1|/(3+1)=0.5.
    assert geometry.maximum_cue_accuracy_gap_fraction == pytest.approx(0.5)
    assert geometry.cue_gap_peak_information_rate == pytest.approx(3.0)


def test_equal_recourse_rates_have_zero_pairwise_geometry():
    geometry = pairwise_information_rate_geometry(0.7, 0.7)
    assert geometry.maximum_cue_accuracy_gap_fraction == pytest.approx(0.0)
    assert geometry.slow_information_time_gap_limit == pytest.approx(0.0)
    assert pairwise_commitment_time_gap(1.2, 0.7, 0.7) == pytest.approx(0.0)
    assert normalized_pairwise_cue_gap(1.2, 0.7, 0.7) == pytest.approx(0.0)



@pytest.mark.parametrize(
    ("alpha", "beta"),
    [(0.2, 0.5), (0.5, 0.5), (1.0, 0.2), (2.0, 1.5)],
)
def test_mechanism_sensitivities_have_expected_signs(alpha, beta):
    result = exponential_mechanism_sensitivity(
        0.40,
        2.0,
        1.0,
        information_rate=alpha,
        recourse_decay_rate=beta,
    )
    assert result.dt_d_information_rate < 0.0
    assert result.dt_d_recourse_decay_rate < 0.0
    assert result.dq_d_information_rate > 0.0
    assert result.dq_d_recourse_decay_rate < 0.0


def test_faster_information_and_faster_deadline_both_advance_but_change_q_oppositely():
    base = exponential_information_actionability_optimum(
        0.40,
        2.0,
        1.0,
        information_rate=0.5,
        recourse_decay_rate=0.5,
    )
    faster_info = exponential_information_actionability_optimum(
        0.40,
        2.0,
        1.0,
        information_rate=1.0,
        recourse_decay_rate=0.5,
    )
    faster_deadline = exponential_information_actionability_optimum(
        0.40,
        2.0,
        1.0,
        information_rate=0.5,
        recourse_decay_rate=1.0,
    )

    assert faster_info.optimal_time < base.optimal_time
    assert faster_deadline.optimal_time < base.optimal_time

    assert faster_info.optimal_cue_accuracy > base.optimal_cue_accuracy
    assert faster_deadline.optimal_cue_accuracy < base.optimal_cue_accuracy


def test_mechanism_derivatives_match_finite_differences():
    alpha = 0.7
    beta = 0.4
    eps = 1e-6
    exact = exponential_mechanism_sensitivity(
        0.40,
        2.0,
        1.0,
        information_rate=alpha,
        recourse_decay_rate=beta,
    )

    a_left = exponential_information_actionability_optimum(
        0.40, 2.0, 1.0,
        information_rate=alpha - eps,
        recourse_decay_rate=beta,
    )
    a_right = exponential_information_actionability_optimum(
        0.40, 2.0, 1.0,
        information_rate=alpha + eps,
        recourse_decay_rate=beta,
    )
    b_left = exponential_information_actionability_optimum(
        0.40, 2.0, 1.0,
        information_rate=alpha,
        recourse_decay_rate=beta - eps,
    )
    b_right = exponential_information_actionability_optimum(
        0.40, 2.0, 1.0,
        information_rate=alpha,
        recourse_decay_rate=beta + eps,
    )

    dt_da = (a_right.optimal_time - a_left.optimal_time) / (2 * eps)
    dq_da = (
        a_right.optimal_cue_accuracy - a_left.optimal_cue_accuracy
    ) / (2 * eps)
    dt_db = (b_right.optimal_time - b_left.optimal_time) / (2 * eps)
    dq_db = (
        b_right.optimal_cue_accuracy - b_left.optimal_cue_accuracy
    ) / (2 * eps)

    assert dt_da == pytest.approx(exact.dt_d_information_rate, rel=1e-6)
    assert dq_da == pytest.approx(exact.dq_d_information_rate, rel=1e-6)
    assert dt_db == pytest.approx(exact.dt_d_recourse_decay_rate, rel=1e-6)
    assert dq_db == pytest.approx(exact.dq_d_recourse_decay_rate, rel=1e-6)
