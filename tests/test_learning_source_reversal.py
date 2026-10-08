"""Only synthetic Gaussian counterexamples. No tracked crane data used."""

from math import isclose
import random

import pytest

from src.learning_source_reversal import (
    compare_learning_sources,
    minimum_mean_drift_for_fresh_advantage,
)


def test_historical_knowledge_advantage_before_shift_and_reversal_after():
    r = compare_learning_sources(
        historical_correlation=.3, current_correlation=.8,
        seasonal_mean_drift=1., fresh_source_error_variance=.25,
        fresh_source_acquisition_cost=.1,
    )
    assert r.historical_rule_was_better_before_shift
    assert r.historical_rule_loss == pytest.approx(1.61)
    assert r.fresh_rule_loss == pytest.approx(.71)
    assert r.net_fresh_advantage == pytest.approx(.90)
    assert r.fresh_source_preferred


def test_no_source_reversal_when_environment_is_stationary():
    r = compare_learning_sources(
        historical_correlation=.3, current_correlation=.3,
        seasonal_mean_drift=0., fresh_source_error_variance=.25,
        fresh_source_acquisition_cost=.1,
    )
    assert r.historical_rule_loss == pytest.approx(.91)
    assert r.net_fresh_advantage == pytest.approx(-.35)
    assert not r.fresh_source_preferred


def test_more_environmental_correlation_does_not_guarantee_old_rule_wins():
    r = compare_learning_sources(
        historical_correlation=.3, current_correlation=.8,
        seasonal_mean_drift=0., fresh_source_error_variance=.20,
        fresh_source_acquisition_cost=.03,
    )
    assert r.net_fresh_advantage == pytest.approx(.02)
    assert r.fresh_source_preferred


def test_threshold_is_exact_and_strict():
    threshold = minimum_mean_drift_for_fresh_advantage(
        historical_correlation=.3, current_correlation=.8,
        fresh_source_error_variance=.49,
        fresh_source_acquisition_cost=.01,
    )
    assert threshold == pytest.approx(.5)
    for drift, expected in [(threshold-.001, False),
                            (threshold, False),
                            (threshold+.001, True),
                            (-threshold-.001, True)]:
        r = compare_learning_sources(
            historical_correlation=.3, current_correlation=.8,
            seasonal_mean_drift=drift, fresh_source_error_variance=.49,
            fresh_source_acquisition_cost=.01)
        assert r.fresh_source_preferred == expected


def test_learning_source_noise_or_cost_can_prevent_reversal():
    r = compare_learning_sources(
        historical_correlation=.3, current_correlation=.8,
        seasonal_mean_drift=.6, fresh_source_error_variance=1.,
        fresh_source_acquisition_cost=.5)
    assert not r.fresh_source_preferred


def test_no_benefit_from_fresh_source_at_equal_forecast_and_zero_noise():
    r = compare_learning_sources(
        historical_correlation=.5, current_correlation=.5,
        seasonal_mean_drift=0., fresh_source_error_variance=0.,
        fresh_source_acquisition_cost=0.)
    assert r.net_fresh_advantage == pytest.approx(0.)
    assert not r.fresh_source_preferred


def test_monte_carlo_matches_squared_loss_and_source_noise():
    rng = random.Random(20261008)
    old, new, drift, fresh_var, cost = .3, .8, 1., .25, .1
    r = compare_learning_sources(
        historical_correlation=old, current_correlation=new,
        seasonal_mean_drift=drift, fresh_source_error_variance=fresh_var,
        fresh_source_acquisition_cost=cost)
    n = 40000
    err_old = 0.0
    err_new = 0.0
    for _ in range(n):
        x = rng.gauss(0,1)
        epsilon = rng.gauss(0,1)
        zeta = rng.gauss(0, fresh_var ** .5)
        h = drift + new*x + (1-new*new)**.5*epsilon
        err_old += (h - old*x)**2
        err_new += (h - (drift + new*x + zeta))**2 + cost
    assert err_old/n == pytest.approx(r.historical_rule_loss, abs=.04)
    assert err_new/n == pytest.approx(r.fresh_rule_loss, abs=.04)


def test_invalid_correlations_variance_and_cost_fail_closed():
    for kwargs in [
        dict(historical_correlation=1.1, current_correlation=.5),
        dict(historical_correlation=.3, current_correlation=-1.2),
        dict(historical_correlation=.3, current_correlation=.5, fresh_source_error_variance=-1),
        dict(historical_correlation=.3, current_correlation=.5, fresh_source_acquisition_cost=-.1),
        dict(historical_correlation=.3, current_correlation=.5, seasonal_mean_drift=float("nan")),
    ]:
        defaults=dict(
            historical_correlation=.3, current_correlation=.8,
            seasonal_mean_drift=0., fresh_source_error_variance=.2,
            fresh_source_acquisition_cost=0.)
        defaults.update(kwargs)
        with pytest.raises(ValueError):
            compare_learning_sources(**defaults)


def test_adult_memory_can_update_and_avoid_a_false_trap():
    from src.learning_source_reversal import compare_recalibrating_memory
    p = dict(
        historical_correlation=.3, current_correlation=.8,
        seasonal_mean_drift=1., fresh_source_error_variance=.25,
        fresh_source_acquisition_cost=.1)
    old = compare_recalibrating_memory(**p, recalibration_fraction=0)
    halfway = compare_recalibrating_memory(**p, recalibration_fraction=.5)
    refreshed = compare_recalibrating_memory(**p, recalibration_fraction=1)
    assert old.fresh_source_preferred
    assert halfway.recalibrated_memory_loss < old.recalibrated_memory_loss
    assert halfway.recalibrated_memory_loss == pytest.approx(.36 + .25 * 1.25)
    assert not refreshed.fresh_source_preferred
    assert refreshed.recalibrated_memory_loss == pytest.approx(.36)


def test_learning_update_threshold_reverses_source_ranking():
    from src.learning_source_reversal import compare_recalibrating_memory
    p=dict(
        historical_correlation=.3, current_correlation=.8,
        seasonal_mean_drift=1., fresh_source_error_variance=.25,
        fresh_source_acquisition_cost=.1)
    # D=1.25 and source overhead=.35. Critical w=1-sqrt(.35/1.25)
    threshold=1-(.35/1.25)**.5
    less = compare_recalibrating_memory(**p, recalibration_fraction=threshold-.01)
    more = compare_recalibrating_memory(**p, recalibration_fraction=threshold+.01)
    assert less.fresh_source_preferred
    assert not more.fresh_source_preferred


def test_no_fresh_advantage_if_social_signal_merely_repeats_updated_memory():
    from src.learning_source_reversal import compare_recalibrating_memory
    p=dict(
        historical_correlation=.3, current_correlation=.8,
        seasonal_mean_drift=1., fresh_source_error_variance=0.,
        fresh_source_acquisition_cost=0.)
    fully = compare_recalibrating_memory(**p, recalibration_fraction=1)
    assert fully.fresh_advantage == pytest.approx(0)
    assert not fully.fresh_source_preferred
    with pytest.raises(ValueError):
        compare_recalibrating_memory(**p, recalibration_fraction=1.2)
