import pytest

from src.deadline_threshold_empirics import (
    infer_deterministic_threshold_interval,
    interval_contains_prediction,
    predicted_information_use,
    predicted_pair_asynchrony,
    threshold_prediction,
)


def test_canonical_actor_thresholds():
    low = threshold_prediction(0.4, 2.0, 1.0, 0.10)
    high = threshold_prediction(0.4, 2.0, 1.0, 0.30)

    assert low.wait_threshold == pytest.approx(0.8125)
    assert high.wait_threshold == pytest.approx(0.9375)
    assert predicted_information_use(0.82, low)
    assert not predicted_information_use(0.82, high)


@pytest.mark.parametrize(
    "q, expected",
    [
        (0.81, False),
        (0.82, True),
        (0.90, True),
        (0.93, True),
        (0.94, False),
    ],
)
def test_pairwise_asynchrony_matches_canonical_window(q, expected):
    assert predicted_pair_asynchrony(
        0.4,
        2.0,
        1.0,
        0.10,
        0.30,
        q,
    ) is expected


def test_observed_switch_brackets_exact_threshold():
    inferred = infer_deterministic_threshold_interval(
        [
            (0.75, False),
            (0.80, False),
            (0.81, False),
            (0.82, True),
            (0.90, True),
        ]
    )
    assert inferred.monotone
    assert inferred.lower_inclusive == pytest.approx(0.81)
    assert inferred.upper_exclusive == pytest.approx(0.82)
    assert interval_contains_prediction(inferred, 0.8125)


def test_tie_rule_makes_lower_bound_inclusive():
    inferred = infer_deterministic_threshold_interval(
        [(0.8125, False), (0.82, True)]
    )
    assert interval_contains_prediction(inferred, 0.8125)


def test_nonmonotone_cue_use_fails_closed():
    inferred = infer_deterministic_threshold_interval(
        [(0.70, False), (0.80, True), (0.90, False)]
    )
    assert not inferred.monotone
    assert not interval_contains_prediction(inferred, 0.80)


def test_contradictory_replicates_at_same_q_fail_closed():
    inferred = infer_deterministic_threshold_interval(
        [(0.80, False), (0.80, True)]
    )
    assert not inferred.monotone


def test_never_wait_prediction_rejects_any_observed_use():
    prediction = threshold_prediction(0.4, 2.0, 1.0, 0.50)
    assert prediction.wait_threshold is None
    inferred = infer_deterministic_threshold_interval(
        [(0.90, False), (1.00, False)]
    )
    assert interval_contains_prediction(inferred, prediction.wait_threshold)

    inferred_with_use = infer_deterministic_threshold_interval(
        [(0.90, False), (1.00, True)]
    )
    assert not interval_contains_prediction(
        inferred_with_use,
        prediction.wait_threshold,
    )
