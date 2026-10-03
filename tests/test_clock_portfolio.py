import math

import pytest

from src.clock_portfolio import (
    clock_portfolio_precision_shares,
    final_variance_from_portfolio,
    optimal_clock_portfolio,
)


def test_final_variance_identity():
    v = final_variance_from_portfolio(
        100.0,
        timer_effort=1.0,
        feedback_effort_per_checkpoint=0.2,
        checkpoints=3,
    )
    assert v == pytest.approx(100.0 * math.exp(-2.2))


def test_zero_checkpoints_forces_all_precision_into_entry_clock():
    r = optimal_clock_portfolio(
        100.0,
        25.0,
        checkpoints=0,
        timer_cost_curvature=2.0,
        feedback_cost_curvature=1.0,
    )
    assert r.timer_effort == pytest.approx(math.log(4.0))
    assert r.feedback_effort_per_checkpoint == pytest.approx(0.0)
    assert r.timer_precision_share == pytest.approx(1.0)
    assert r.feedback_precision_share == pytest.approx(0.0)
    assert r.achieved_variance == pytest.approx(25.0)


def test_optimal_portfolio_hits_target_exactly():
    r = optimal_clock_portfolio(
        100.0,
        10.0,
        checkpoints=4,
        timer_cost_curvature=1.5,
        feedback_cost_curvature=2.0,
    )
    assert r.achieved_variance == pytest.approx(10.0)
    assert r.timer_precision_share + r.feedback_precision_share == pytest.approx(
        1.0
    )


def test_more_checkpoints_shift_precision_toward_feedback():
    s1 = clock_portfolio_precision_shares(
        checkpoints=1,
        timer_cost_curvature=1.0,
        feedback_cost_curvature=1.0,
    )
    s5 = clock_portfolio_precision_shares(
        checkpoints=5,
        timer_cost_curvature=1.0,
        feedback_cost_curvature=1.0,
    )
    assert s5[1] > s1[1]
    assert s5[0] < s1[0]


def test_expensive_timer_shifts_portfolio_toward_feedback():
    cheap_timer = clock_portfolio_precision_shares(
        checkpoints=2,
        timer_cost_curvature=0.2,
        feedback_cost_curvature=1.0,
    )
    expensive_timer = clock_portfolio_precision_shares(
        checkpoints=2,
        timer_cost_curvature=5.0,
        feedback_cost_curvature=1.0,
    )
    assert expensive_timer[1] > cheap_timer[1]


def test_expensive_feedback_shifts_portfolio_toward_timer():
    cheap_feedback = clock_portfolio_precision_shares(
        checkpoints=2,
        timer_cost_curvature=1.0,
        feedback_cost_curvature=0.2,
    )
    expensive_feedback = clock_portfolio_precision_shares(
        checkpoints=2,
        timer_cost_curvature=1.0,
        feedback_cost_curvature=5.0,
    )
    assert expensive_feedback[0] > cheap_feedback[0]


def test_closed_form_cost():
    vref, vt = 100.0, 25.0
    n, a, b = 3, 2.0, 5.0
    r = optimal_clock_portfolio(
        vref,
        vt,
        checkpoints=n,
        timer_cost_curvature=a,
        feedback_cost_curvature=b,
    )
    P = math.log(vref / vt)
    expected = a * b * P * P / (2.0 * (b + 4.0 * n * n * a))
    assert r.minimum_cost == pytest.approx(expected)


def test_same_target_can_be_reached_by_different_portfolios():
    vref, vt = 100.0, 10.0
    timer_heavy = optimal_clock_portfolio(
        vref,
        vt,
        checkpoints=1,
        timer_cost_curvature=0.1,
        feedback_cost_curvature=5.0,
    )
    feedback_heavy = optimal_clock_portfolio(
        vref,
        vt,
        checkpoints=5,
        timer_cost_curvature=5.0,
        feedback_cost_curvature=0.1,
    )
    assert timer_heavy.achieved_variance == pytest.approx(vt)
    assert feedback_heavy.achieved_variance == pytest.approx(vt)
    assert timer_heavy.timer_precision_share > feedback_heavy.timer_precision_share
