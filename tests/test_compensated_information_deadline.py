import pytest

from src.compensated_information_deadline import (
    adaptive_state_expected_effective_cost,
    compensated_pair_window_width,
    linear_compensated_information_threshold,
    linear_effective_deadline_cost,
    precommitted_state_expected_effective_cost,
    threshold_slope_with_raw_delay,
)


def test_no_compensation_recovers_raw_linear_delay_cost():
    c, residual, cost = linear_effective_deadline_cost(
        0.30,
        compensation_capacity=0.0,
        compensation_cost_per_unit=0.20,
        residual_loss_per_unit=1.0,
    )
    assert c == pytest.approx(0.0)
    assert residual == pytest.approx(0.30)
    assert cost == pytest.approx(0.30)


def test_cheap_compensation_is_used_to_capacity():
    c, residual, cost = linear_effective_deadline_cost(
        0.30,
        compensation_capacity=0.20,
        compensation_cost_per_unit=0.20,
        residual_loss_per_unit=1.0,
    )
    assert c == pytest.approx(0.20)
    assert residual == pytest.approx(0.10)
    assert cost == pytest.approx(0.14)


def test_expensive_compensation_is_not_used():
    c, residual, cost = linear_effective_deadline_cost(
        0.30,
        compensation_capacity=0.30,
        compensation_cost_per_unit=1.20,
        residual_loss_per_unit=1.0,
    )
    assert c == pytest.approx(0.0)
    assert residual == pytest.approx(0.30)
    assert cost == pytest.approx(0.30)


def test_free_full_compensation_reduces_threshold_to_cue_actionability_boundary():
    result = linear_compensated_information_threshold(
        0.4,
        2.0,
        1.0,
        raw_delay=0.30,
        compensation_capacity=0.30,
        compensation_cost_per_unit=0.0,
        residual_loss_per_unit=1.0,
    )
    assert result.effective_delay_cost == pytest.approx(0.0)
    assert result.wait_threshold == pytest.approx(0.75)


def test_partial_compensation_lowers_information_use_threshold():
    uncompensated = linear_compensated_information_threshold(
        0.4,
        2.0,
        1.0,
        raw_delay=0.30,
        compensation_capacity=0.0,
        compensation_cost_per_unit=0.20,
        residual_loss_per_unit=1.0,
    )
    compensated = linear_compensated_information_threshold(
        0.4,
        2.0,
        1.0,
        raw_delay=0.30,
        compensation_capacity=0.20,
        compensation_cost_per_unit=0.20,
        residual_loss_per_unit=1.0,
    )
    assert uncompensated.wait_threshold == pytest.approx(0.9375)
    assert compensated.effective_delay_cost == pytest.approx(0.14)
    assert compensated.wait_threshold == pytest.approx(0.8375)
    assert compensated.wait_threshold < uncompensated.wait_threshold


def test_capacity_heterogeneity_creates_threshold_heterogeneity_at_same_raw_delay():
    width = compensated_pair_window_width(
        0.4,
        2.0,
        1.0,
        actor_1=(0.30, 0.00, 0.20, 1.0),
        actor_2=(0.30, 0.20, 0.20, 1.0),
    )
    # Effective-cost gap = 0.30 - 0.14 = 0.16; A+L = 1.60.
    assert width == pytest.approx(0.10)


def test_threshold_slope_has_capacity_kink_when_compensation_is_cheaper():
    # S=A+L=1.6. Before capacity is exhausted slope=kappa/S;
    # afterwards it is mu/S.
    before = threshold_slope_with_raw_delay(
        compensation_capacity=0.20,
        compensation_cost_per_unit=0.20,
        residual_loss_per_unit=1.0,
        total_prior_loss=1.60,
        raw_delay=0.10,
    )
    after = threshold_slope_with_raw_delay(
        compensation_capacity=0.20,
        compensation_cost_per_unit=0.20,
        residual_loss_per_unit=1.0,
        total_prior_loss=1.60,
        raw_delay=0.30,
    )
    assert before == pytest.approx(0.125)
    assert after == pytest.approx(0.625)

    with pytest.raises(ValueError, match="capacity kink"):
        threshold_slope_with_raw_delay(
            compensation_capacity=0.20,
            compensation_cost_per_unit=0.20,
            residual_loss_per_unit=1.0,
            total_prior_loss=1.60,
            raw_delay=0.20,
        )


def test_more_capacity_cannot_raise_linear_effective_cost_when_compensation_is_cheaper():
    costs = []
    for capacity in (0.0, 0.05, 0.10, 0.20, 0.30):
        _, _, cost = linear_effective_deadline_cost(
            0.30,
            compensation_capacity=capacity,
            compensation_cost_per_unit=0.20,
            residual_loss_per_unit=1.0,
        )
        costs.append(cost)
    assert costs == sorted(costs, reverse=True)


def test_state_contingent_compensation_information_has_nonnegative_value():
    adaptive = adaptive_state_expected_effective_cost(
        [0.5, 0.5],
        raw_delay=0.30,
        compensation_capacity=0.30,
        compensation_costs_per_unit=[0.10, 2.0],
        residual_losses_per_unit=[1.0, 1.0],
    )
    precommitted = precommitted_state_expected_effective_cost(
        [0.5, 0.5],
        raw_delay=0.30,
        compensation_capacity=0.30,
        compensation_costs_per_unit=[0.10, 2.0],
        residual_losses_per_unit=[1.0, 1.0],
    )

    assert adaptive == pytest.approx(0.165)
    assert precommitted == pytest.approx(0.30)
    assert adaptive <= precommitted


def test_direct_wait_cost_survives_full_free_timing_compensation():
    result = linear_compensated_information_threshold(
        0.4,
        2.0,
        1.0,
        raw_delay=0.30,
        compensation_capacity=0.30,
        compensation_cost_per_unit=0.0,
        residual_loss_per_unit=1.0,
        direct_wait_cost_per_unit=0.40,
    )
    # All 0.30 units of timing delay are recovered for free, but direct
    # waiting cost remains 0.40*0.30 = 0.12.
    assert result.optimal_compensation == pytest.approx(0.30)
    assert result.residual_delay == pytest.approx(0.0)
    assert result.direct_wait_cost == pytest.approx(0.12)
    assert result.effective_delay_cost == pytest.approx(0.12)
    assert result.wait_threshold == pytest.approx((1.20 + 0.12) / 1.60)
    assert result.wait_threshold > 0.75


def test_direct_wait_cost_adds_to_both_sides_of_capacity_kink():
    before = threshold_slope_with_raw_delay(
        compensation_capacity=0.20,
        compensation_cost_per_unit=0.20,
        residual_loss_per_unit=1.0,
        direct_wait_cost_per_unit=0.40,
        total_prior_loss=1.60,
        raw_delay=0.10,
    )
    after = threshold_slope_with_raw_delay(
        compensation_capacity=0.20,
        compensation_cost_per_unit=0.20,
        residual_loss_per_unit=1.0,
        direct_wait_cost_per_unit=0.40,
        total_prior_loss=1.60,
        raw_delay=0.30,
    )
    assert before == pytest.approx((0.40 + 0.20) / 1.60)
    assert after == pytest.approx((0.40 + 1.00) / 1.60)


def test_pair_window_can_be_created_by_direct_wait_cost_difference_only():
    width = compensated_pair_window_width(
        0.4,
        2.0,
        1.0,
        actor_1=(0.20, 0.20, 0.0, 1.0, 0.10),
        actor_2=(0.20, 0.20, 0.0, 1.0, 0.50),
    )
    # Timing delay fully recovered in both actors. D_eff is direct cost only:
    # 0.02 vs 0.10, so Delta q = 0.08/1.60.
    assert width == pytest.approx(0.05)
