import pytest

from src.racing_information_absorption import (
    RaceForecast,
    evaluate_time_slice,
    fit_form_weight,
    logarithmic_opinion_pool,
    market_probabilities_from_decimal_odds,
    mean_log_loss,
)


def _race(race_id, winner, form, market):
    return RaceForecast(
        race_id=race_id,
        winner_id=winner,
        form_probabilities=form,
        market_probabilities=market,
    )


def test_reciprocal_odds_are_normalized_within_race():
    out = market_probabilities_from_decimal_odds(
        {"A": 2.0, "B": 4.0, "C": 4.0}
    )
    assert sum(out.values()) == pytest.approx(1.0)
    assert out["A"] == pytest.approx(0.5)
    assert out["B"] == pytest.approx(0.25)
    assert out["C"] == pytest.approx(0.25)


def test_log_pool_endpoints_recover_market_and_form():
    form = {"A": 0.7, "B": 0.3}
    market = {"A": 0.4, "B": 0.6}
    at_zero = logarithmic_opinion_pool(form, market, 0.0)
    at_one = logarithmic_opinion_pool(form, market, 1.0)
    assert at_zero == pytest.approx(market)
    assert at_one == pytest.approx(form)


def test_training_prefers_form_when_form_is_consistently_better():
    races = [
        _race("r1", "A", {"A": 0.8, "B": 0.2}, {"A": 0.4, "B": 0.6}),
        _race("r2", "B", {"A": 0.2, "B": 0.8}, {"A": 0.6, "B": 0.4}),
        _race("r3", "A", {"A": 0.75, "B": 0.25}, {"A": 0.45, "B": 0.55}),
    ]
    weight, _ = fit_form_weight(races, grid_points=101)
    assert weight > 0.9


def test_training_prefers_market_when_market_is_consistently_better():
    races = [
        _race("r1", "A", {"A": 0.4, "B": 0.6}, {"A": 0.8, "B": 0.2}),
        _race("r2", "B", {"A": 0.6, "B": 0.4}, {"A": 0.2, "B": 0.8}),
        _race("r3", "A", {"A": 0.45, "B": 0.55}, {"A": 0.75, "B": 0.25}),
    ]
    weight, _ = fit_form_weight(races, grid_points=101)
    assert weight < 0.1


def test_market_absorption_pattern_can_reduce_incremental_form_value():
    # The fixed form model is informative at both times.  Early market forecasts
    # omit that signal, while late market forecasts have largely absorbed it.
    train_early = [
        _race("tr1", "A", {"A": 0.75, "B": 0.25}, {"A": 0.50, "B": 0.50}),
        _race("tr2", "B", {"A": 0.25, "B": 0.75}, {"A": 0.50, "B": 0.50}),
        _race("tr3", "A", {"A": 0.70, "B": 0.30}, {"A": 0.52, "B": 0.48}),
        _race("tr4", "B", {"A": 0.70, "B": 0.30}, {"A": 0.48, "B": 0.52}),
    ]
    train_late = [
        _race("tr1", "A", {"A": 0.75, "B": 0.25}, {"A": 0.73, "B": 0.27}),
        _race("tr2", "B", {"A": 0.25, "B": 0.75}, {"A": 0.27, "B": 0.73}),
        _race("tr3", "A", {"A": 0.70, "B": 0.30}, {"A": 0.69, "B": 0.31}),
        _race("tr4", "B", {"A": 0.70, "B": 0.30}, {"A": 0.31, "B": 0.69}),
    ]
    test_early = [
        _race("te1", "A", {"A": 0.72, "B": 0.28}, {"A": 0.51, "B": 0.49}),
        _race("te2", "B", {"A": 0.28, "B": 0.72}, {"A": 0.49, "B": 0.51}),
    ]
    test_late = [
        _race("te1", "A", {"A": 0.72, "B": 0.28}, {"A": 0.71, "B": 0.29}),
        _race("te2", "B", {"A": 0.28, "B": 0.72}, {"A": 0.29, "B": 0.71}),
    ]

    early = evaluate_time_slice(
        "T-60",
        train_early,
        test_early,
        grid_points=101,
    )
    late = evaluate_time_slice(
        "LAST",
        train_late,
        test_late,
        grid_points=101,
    )

    assert early.fitted_form_weight > late.fitted_form_weight
    assert (
        early.incremental_form_value_over_market
        > late.incremental_form_value_over_market
    )
    assert late.test_market_log_loss < early.test_market_log_loss


def test_hybrid_log_loss_uses_held_out_races_only():
    training = [
        _race("tr", "A", {"A": 0.8, "B": 0.2}, {"A": 0.5, "B": 0.5}),
    ]
    test = [
        _race("te", "B", {"A": 0.4, "B": 0.6}, {"A": 0.3, "B": 0.7}),
    ]
    out = evaluate_time_slice("T-30", training, test, grid_points=11)
    assert out.test_races == 1
    assert out.test_hybrid_log_loss == pytest.approx(
        mean_log_loss(test, source="hybrid", form_weight=out.fitted_form_weight)
    )


def test_runner_set_mismatch_fails_closed():
    with pytest.raises(ValueError, match="share runner ids"):
        logarithmic_opinion_pool(
            {"A": 0.5, "B": 0.5},
            {"A": 0.4, "C": 0.6},
            0.5,
        )



def test_paired_bootstrap_recovers_positive_absorption_contrasts():
    from src.racing_information_absorption import paired_test_bootstrap

    first = [
        _race("te1", "A", {"A": 0.72, "B": 0.28}, {"A": 0.51, "B": 0.49}),
        _race("te2", "B", {"A": 0.28, "B": 0.72}, {"A": 0.49, "B": 0.51}),
    ]
    last = [
        _race("te1", "A", {"A": 0.72, "B": 0.28}, {"A": 0.71, "B": 0.29}),
        _race("te2", "B", {"A": 0.28, "B": 0.72}, {"A": 0.29, "B": 0.71}),
    ]
    out = paired_test_bootstrap(
        first,
        last,
        first_form_weight=0.9,
        last_form_weight=0.0,
        replicates=200,
        seed=7,
    )
    assert out.market_improvement_mean > 0.0
    assert out.incremental_value_decline_mean > 0.0
    assert out.market_improvement_positive_fraction == pytest.approx(1.0)
    assert out.incremental_value_decline_positive_fraction == pytest.approx(1.0)


def test_paired_bootstrap_requires_identical_race_ids():
    from src.racing_information_absorption import paired_test_bootstrap

    first = [
        _race("te1", "A", {"A": 0.7, "B": 0.3}, {"A": 0.5, "B": 0.5}),
    ]
    last = [
        _race("other", "A", {"A": 0.7, "B": 0.3}, {"A": 0.6, "B": 0.4}),
    ]
    with pytest.raises(ValueError, match="identical race ids"):
        paired_test_bootstrap(
            first,
            last,
            first_form_weight=0.5,
            last_form_weight=0.5,
            replicates=10,
        )
