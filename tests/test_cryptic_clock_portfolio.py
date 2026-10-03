import math

import pytest

from src.cryptic_clock_portfolio import (
    critical_opportunity_retention,
    cryptic_portfolio_pair_divergence,
    disrupted_portfolio_variance,
    pairwise_mismatch_variance_inflation,
)


def test_timer_only_portfolio_is_insensitive_to_opportunity_loss():
    r=disrupted_portfolio_variance(
        historical_target_variance=4.0,
        precision_budget=3.0,
        feedback_share=0.0,
        opportunity_retained=0.0,
    )
    assert r.inflation_factor==pytest.approx(1.0)
    assert r.disrupted_variance==pytest.approx(4.0)


def test_feedback_heavy_portfolio_inflates_more_under_same_loss():
    timer=disrupted_portfolio_variance(
        historical_target_variance=1.0,
        precision_budget=4.0,
        feedback_share=0.25,
        opportunity_retained=0.5,
    )
    feedback=disrupted_portfolio_variance(
        historical_target_variance=1.0,
        precision_budget=4.0,
        feedback_share=0.75,
        opportunity_retained=0.5,
    )
    assert feedback.inflation_factor>timer.inflation_factor


def test_equal_historical_precision_can_diverge_after_common_loss():
    r=cryptic_portfolio_pair_divergence(
        historical_target_variance_1=2.0,
        precision_budget_1=3.0,
        feedback_share_1=0.8,
        opportunity_retained_1=0.6,
        historical_target_variance_2=2.0,
        precision_budget_2=3.0,
        feedback_share_2=0.2,
        opportunity_retained_2=0.6,
    )
    expected=(1.0-0.6)*3.0*(0.8-0.2)
    assert r.log_variance_ratio_after==pytest.approx(expected)
    assert r.variance_ratio_after==pytest.approx(math.exp(expected))


def test_identical_hidden_portfolios_remain_equal_under_common_loss():
    r=cryptic_portfolio_pair_divergence(
        historical_target_variance_1=1.0,
        precision_budget_1=2.5,
        feedback_share_1=0.4,
        opportunity_retained_1=0.3,
        historical_target_variance_2=1.0,
        precision_budget_2=2.5,
        feedback_share_2=0.4,
        opportunity_retained_2=0.3,
    )
    assert r.log_variance_ratio_after==pytest.approx(0.0)
    assert r.variance_ratio_after==pytest.approx(1.0)


def test_feedback_heavy_portfolio_has_higher_critical_retention_threshold():
    timer=critical_opportunity_retention(
        precision_budget=4.0,
        feedback_share=0.25,
        tolerated_variance_inflation=math.exp(0.5),
    )
    feedback=critical_opportunity_retention(
        precision_budget=4.0,
        feedback_share=0.75,
        tolerated_variance_inflation=math.exp(0.5),
    )
    assert timer is not None
    assert feedback is not None
    assert feedback>timer


def test_no_threshold_for_timer_only_portfolio():
    assert critical_opportunity_retention(
        precision_budget=4.0,
        feedback_share=0.0,
        tolerated_variance_inflation=2.0,
    ) is None


def test_pairwise_mismatch_identity_for_independent_errors():
    r=pairwise_mismatch_variance_inflation(
        historical_variance_each=3.0,
        historical_correlation=0.0,
        inflation_factor_1=2.0,
        inflation_factor_2=4.0,
    )
    assert r.mismatch_inflation_ratio==pytest.approx(3.0)
    assert r.asymmetry_penalty==pytest.approx(0.0)


def test_correlated_partners_pay_extra_asymmetry_penalty():
    equal=pairwise_mismatch_variance_inflation(
        historical_variance_each=1.0,
        historical_correlation=0.8,
        inflation_factor_1=3.0,
        inflation_factor_2=3.0,
    )
    unequal=pairwise_mismatch_variance_inflation(
        historical_variance_each=1.0,
        historical_correlation=0.8,
        inflation_factor_1=5.0,
        inflation_factor_2=1.0,
    )
    assert equal.asymmetry_penalty==pytest.approx(0.0)
    assert unequal.asymmetry_penalty>0.0
    assert unequal.mismatch_inflation_ratio > unequal.mean_inflation_component


def test_perfectly_correlated_historical_pair_is_singular_for_ratio():
    with pytest.raises(ValueError,match="correlation"):
        pairwise_mismatch_variance_inflation(
            historical_variance_each=1.0,
            historical_correlation=1.0,
            inflation_factor_1=2.0,
            inflation_factor_2=2.0,
        )
