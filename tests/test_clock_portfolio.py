import math

import pytest

from src.clock_portfolio import (
    clock_portfolio_precision_shares,
    clock_portfolio_minimum_cost_closed_form,
    final_variance_from_portfolio,
    flexibility_dependence_tradeoff,
    final_variance_with_process_noise,
    feedback_majority_checkpoint_threshold,
    fragility_from_feedback_share,
    opportunity_loss_fragility,
    per_use_cost_feedback_majority_threshold,
    per_use_cost_minimum_cost,
    per_use_cost_precision_shares,
    infinite_horizon_noise_floor,
    post_entry_noise_floor,
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


def test_process_noise_creates_timer_irreducible_floor():
    floor = post_entry_noise_floor(
        absolute_phase_retention=0.5,
        process_variance=4.0,
        checkpoints=3,
    )
    expected = 4.0 * (1.0 + 0.25 + 0.25**2)
    assert floor == pytest.approx(expected)

    # Making the entry timer arbitrarily precise cannot remove this component.
    final = final_variance_with_process_noise(
        1e-12,
        absolute_phase_retention=0.5,
        process_variance=4.0,
        checkpoints=3,
    )
    assert final == pytest.approx(floor, rel=1e-10, abs=1e-10)


def test_without_feedback_each_new_shock_accumulates():
    final = final_variance_with_process_noise(
        10.0,
        absolute_phase_retention=1.0,
        process_variance=3.0,
        checkpoints=4,
    )
    assert final == pytest.approx(22.0)
    assert post_entry_noise_floor(
        absolute_phase_retention=1.0,
        process_variance=3.0,
        checkpoints=4,
    ) == pytest.approx(12.0)


def test_stronger_feedback_reduces_post_entry_noise_floor():
    weak = post_entry_noise_floor(
        absolute_phase_retention=0.9,
        process_variance=2.0,
        checkpoints=5,
    )
    strong = post_entry_noise_floor(
        absolute_phase_retention=0.3,
        process_variance=2.0,
        checkpoints=5,
    )
    assert strong < weak


def test_stationary_noise_floor():
    assert infinite_horizon_noise_floor(
        absolute_phase_retention=0.5,
        process_variance=3.0,
    ) == pytest.approx(4.0)


def test_entry_precision_does_not_change_post_entry_noise_floor():
    floor = post_entry_noise_floor(
        absolute_phase_retention=0.6,
        process_variance=1.5,
        checkpoints=4,
    )
    a = final_variance_with_process_noise(
        100.0,
        absolute_phase_retention=0.6,
        process_variance=1.5,
        checkpoints=4,
    )
    b = final_variance_with_process_noise(
        10.0,
        absolute_phase_retention=0.6,
        process_variance=1.5,
        checkpoints=4,
    )
    assert (a - floor) / (b - floor) == pytest.approx(10.0)


def test_no_opportunity_loss_preserves_target_variance():
    r=opportunity_loss_fragility(
        100.0,
        4.0,
        historical_checkpoints=5,
        retained_opportunity_fraction=1.0,
        timer_cost_curvature=1.0,
        feedback_cost_curvature=1.0,
    )
    assert r.disrupted_variance == pytest.approx(4.0)
    assert r.variance_inflation_factor == pytest.approx(1.0)
    assert r.excess_log_variance == pytest.approx(0.0)


def test_full_opportunity_loss_inflates_by_feedback_precision_share():
    r=opportunity_loss_fragility(
        100.0,
        4.0,
        historical_checkpoints=5,
        retained_opportunity_fraction=0.0,
        timer_cost_curvature=1.0,
        feedback_cost_curvature=1.0,
    )
    closed=fragility_from_feedback_share(
        r.required_log_precision,
        r.historical_feedback_precision_share,
        retained_opportunity_fraction=0.0,
    )
    assert r.variance_inflation_factor == pytest.approx(closed)
    assert r.variance_inflation_factor > 1.0


def test_feedback_heavy_portfolio_is_more_fragile_to_same_opportunity_loss():
    # More historical checkpoints produce a higher feedback precision share.
    short=opportunity_loss_fragility(
        100.0,
        4.0,
        historical_checkpoints=1,
        retained_opportunity_fraction=0.5,
        timer_cost_curvature=1.0,
        feedback_cost_curvature=1.0,
    )
    long=opportunity_loss_fragility(
        100.0,
        4.0,
        historical_checkpoints=6,
        retained_opportunity_fraction=0.5,
        timer_cost_curvature=1.0,
        feedback_cost_curvature=1.0,
    )
    assert long.historical_feedback_precision_share > short.historical_feedback_precision_share
    assert long.variance_inflation_factor > short.variance_inflation_factor


def test_one_shot_timer_only_system_is_not_fragile_to_feedback_opportunity_loss():
    r=opportunity_loss_fragility(
        100.0,
        4.0,
        historical_checkpoints=0,
        retained_opportunity_fraction=0.0,
        timer_cost_curvature=1.0,
        feedback_cost_curvature=1.0,
    )
    assert r.historical_feedback_precision_share == pytest.approx(0.0)
    assert r.variance_inflation_factor == pytest.approx(1.0)


def test_closed_form_fragility_monotone_in_opportunity_loss():
    P=3.0
    s=0.8
    full=fragility_from_feedback_share(P,s,retained_opportunity_fraction=1.0)
    half=fragility_from_feedback_share(P,s,retained_opportunity_fraction=0.5)
    none=fragility_from_feedback_share(P,s,retained_opportunity_fraction=0.0)
    assert full == pytest.approx(1.0)
    assert full < half < none


def test_feedback_majority_threshold_equal_costs_is_half_checkpoint():
    nc=feedback_majority_checkpoint_threshold(
        timer_cost_curvature=1.0,
        feedback_cost_curvature=1.0,
    )
    assert nc == pytest.approx(0.5)


def test_precision_share_flips_across_feedback_majority_threshold():
    a=1.0
    b=16.0
    nc=feedback_majority_checkpoint_threshold(
        timer_cost_curvature=a,
        feedback_cost_curvature=b,
    )
    assert nc == pytest.approx(2.0)
    timer1,feed1=clock_portfolio_precision_shares(
        checkpoints=2,
        timer_cost_curvature=a,
        feedback_cost_curvature=b,
    )
    timer2,feed2=clock_portfolio_precision_shares(
        checkpoints=3,
        timer_cost_curvature=a,
        feedback_cost_curvature=b,
    )
    assert feed1 == pytest.approx(0.5)
    assert feed2 > 0.5
    assert timer2 < 0.5


def test_minimum_cost_decreases_with_checkpoint_number():
    P=3.0
    costs=[
        clock_portfolio_minimum_cost_closed_form(
            P,
            checkpoints=n,
            timer_cost_curvature=1.0,
            feedback_cost_curvature=1.0,
        )
        for n in [0.0,1.0,2.0,4.0]
    ]
    assert costs[0] > costs[1] > costs[2] > costs[3]


def test_opportunity_loss_fragility_increases_with_checkpoint_number():
    P=3.0
    rows=[
        flexibility_dependence_tradeoff(
            P,
            checkpoints=n,
            retained_opportunity_fraction=0.5,
            timer_cost_curvature=1.0,
            feedback_cost_curvature=1.0,
        )
        for n in [0.0,1.0,2.0,4.0]
    ]
    infl=[r.opportunity_loss_variance_inflation for r in rows]
    assert infl[0] < infl[1] < infl[2] < infl[3]


def test_flexibility_dependence_tradeoff_moves_in_opposite_directions():
    low=flexibility_dependence_tradeoff(
        2.5,
        checkpoints=1.0,
        retained_opportunity_fraction=0.4,
        timer_cost_curvature=1.0,
        feedback_cost_curvature=2.0,
    )
    high=flexibility_dependence_tradeoff(
        2.5,
        checkpoints=5.0,
        retained_opportunity_fraction=0.4,
        timer_cost_curvature=1.0,
        feedback_cost_curvature=2.0,
    )
    assert high.minimum_intact_cost < low.minimum_intact_cost
    assert high.feedback_precision_share > low.feedback_precision_share
    assert high.opportunity_loss_variance_inflation > low.opportunity_loss_variance_inflation


def test_per_use_cost_feedback_share_still_increases_with_checkpoints():
    shares=[
        per_use_cost_precision_shares(
            checkpoints=n,
            timer_cost_curvature=1.0,
            feedback_use_cost_curvature=4.0,
        )[1]
        for n in [0,1,2,4]
    ]
    assert shares[0] < shares[1] < shares[2] < shares[3]


def test_per_use_cost_feedback_majority_threshold():
    nc=per_use_cost_feedback_majority_threshold(
        timer_cost_curvature=1.0,
        feedback_use_cost_curvature=8.0,
    )
    assert nc == pytest.approx(2.0)
    _,at=per_use_cost_precision_shares(
        checkpoints=2,
        timer_cost_curvature=1.0,
        feedback_use_cost_curvature=8.0,
    )
    _,above=per_use_cost_precision_shares(
        checkpoints=3,
        timer_cost_curvature=1.0,
        feedback_use_cost_curvature=8.0,
    )
    assert at == pytest.approx(0.5)
    assert above > 0.5


def test_per_use_cost_minimum_cost_decreases_with_more_checkpoints():
    P=3.0
    costs=[
        per_use_cost_minimum_cost(
            P,
            checkpoints=n,
            timer_cost_curvature=1.0,
            feedback_use_cost_curvature=2.0,
        )
        for n in [0,1,2,5]
    ]
    assert costs[0] > costs[1] > costs[2] > costs[3]
