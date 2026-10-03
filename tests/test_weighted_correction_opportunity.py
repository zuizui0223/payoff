import pytest

from src.weighted_correction_opportunity import (
    disrupted_weighted_portfolio,
    effective_opportunity_retention,
    effective_opportunity_retention_from_feedback_shares,
    optimal_weighted_clock_portfolio,
    shared_capacity_clock_portfolio,
    weighted_route_leverage,
)


def test_equal_checkpoints_recover_per_use_checkpoint_scaling():
    p = optimal_weighted_clock_portfolio(
        100.0,
        10.0,
        timer_cost_curvature=2.0,
        checkpoint_leverages=[1.0, 1.0, 1.0],
        checkpoint_cost_curvatures=[4.0, 4.0, 4.0],
    )
    # L = n/b = 3/4
    expected = 4.0 * 2.0 * (3.0 / 4.0) / (1.0 + 4.0 * 2.0 * (3.0 / 4.0))
    assert p.feedback_precision_share == pytest.approx(expected)
    assert p.timer_precision_share + p.feedback_precision_share == pytest.approx(1.0)
    assert p.achieved_variance == pytest.approx(10.0)


def test_high_leverage_checkpoint_receives_quadratically_more_precision_share():
    p = optimal_weighted_clock_portfolio(
        100.0,
        10.0,
        timer_cost_curvature=1.0,
        checkpoint_leverages=[1.0, 2.0],
        checkpoint_cost_curvatures=[1.0, 1.0],
    )
    # downstream contribution weight is c^2/b, so ratio is 1:4
    s1, s2 = p.checkpoint_feedback_shares
    assert s2 / s1 == pytest.approx(4.0)


def test_effective_retention_is_not_named_site_fraction():
    omega = effective_opportunity_retention(
        [1.0, 3.0],
        [1.0, 1.0],
        [1.0, 0.0],
    )
    # retain low-leverage site only: 1/(1+9)
    assert omega == pytest.approx(0.1)


def test_losing_high_leverage_site_is_more_fragile_than_losing_low_one():
    p = optimal_weighted_clock_portfolio(
        100.0,
        10.0,
        timer_cost_curvature=1.0,
        checkpoint_leverages=[1.0, 3.0],
        checkpoint_cost_curvatures=[1.0, 1.0],
    )
    lose_low = disrupted_weighted_portfolio(
        p,
        checkpoint_retention=[0.0, 1.0],
    )
    lose_high = disrupted_weighted_portfolio(
        p,
        checkpoint_retention=[1.0, 0.0],
    )
    assert lose_high.effective_opportunity_loss > lose_low.effective_opportunity_loss
    assert lose_high.variance_inflation_factor > lose_low.variance_inflation_factor


def test_full_substitution_retention_has_no_inflation():
    p = optimal_weighted_clock_portfolio(
        100.0,
        10.0,
        timer_cost_curvature=1.0,
        checkpoint_leverages=[1.0, 2.0],
        checkpoint_cost_curvatures=[1.0, 2.0],
    )
    d = disrupted_weighted_portfolio(
        p,
        checkpoint_retention=[1.0, 1.0],
    )
    assert d.effective_opportunity_retention == pytest.approx(1.0)
    assert d.variance_inflation_factor == pytest.approx(1.0)
    assert d.disrupted_variance == pytest.approx(10.0)


def test_equal_checkpoints_effective_retention_is_mean_retention():
    omega = effective_opportunity_retention(
        [1.0, 1.0, 1.0, 1.0],
        [2.0, 2.0, 2.0, 2.0],
        [1.0, 1.0, 0.0, 0.0],
    )
    assert omega == pytest.approx(0.5)


def test_weighted_route_leverage_penalizes_expensive_checkpoints():
    L = weighted_route_leverage(
        [2.0, 2.0],
        [1.0, 4.0],
    )
    assert L == pytest.approx(4.0 + 1.0)


def test_shared_capacity_recovers_n_squared_scaling():
    n = 4
    a = 2.0
    b = 3.0
    p = shared_capacity_clock_portfolio(
        100.0,
        10.0,
        timer_cost_curvature=a,
        feedback_capacity_cost_curvature=b,
        checkpoint_leverages=[1.0] * n,
    )
    expected = 4.0 * a * n * n / (b + 4.0 * a * n * n)
    assert p.feedback_precision_share == pytest.approx(expected)


def test_invalid_retention_length_rejected():
    p = optimal_weighted_clock_portfolio(
        100.0,
        10.0,
        timer_cost_curvature=1.0,
        checkpoint_leverages=[1.0, 1.0],
        checkpoint_cost_curvatures=[1.0, 1.0],
    )
    with pytest.raises(ValueError, match="match"):
        disrupted_weighted_portfolio(
            p,
            checkpoint_retention=[1.0],
        )


def test_share_based_effective_retention_matches_optimum_weighting():
    p = optimal_weighted_clock_portfolio(
        100.0,
        10.0,
        timer_cost_curvature=1.0,
        checkpoint_leverages=[1.0, 3.0],
        checkpoint_cost_curvatures=[1.0, 1.0],
    )
    o = [1.0, 0.0]
    from_shares = effective_opportunity_retention_from_feedback_shares(
        p.checkpoint_feedback_shares,
        o,
    )
    from_model = effective_opportunity_retention(
        p.checkpoint_leverages,
        p.checkpoint_cost_curvatures,
        o,
    )
    assert from_shares == pytest.approx(from_model)


def test_share_based_retention_is_cost_independent():
    # Historical checkpoint shares are already the sufficient weights.
    omega = effective_opportunity_retention_from_feedback_shares(
        [0.05, 0.15, 0.30],
        [1.0, 0.0, 0.5],
    )
    assert omega == pytest.approx((0.05 + 0.15) / 0.50)


def test_zero_feedback_share_makes_opportunity_loss_irrelevant():
    omega = effective_opportunity_retention_from_feedback_shares(
        [0.0, 0.0],
        [0.0, 0.0],
    )
    assert omega == pytest.approx(1.0)
