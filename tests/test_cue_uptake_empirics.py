import pytest

from src.cue_uptake_empirics import (
    ThresholdCandidateScore,
    mean_standard_error,
    select_threshold_one_se,
)


def score(q, mean, se=0.01):
    return ThresholdCandidateScore(q, mean, se)


def test_mean_standard_error():
    mean, se = mean_standard_error([1.0, 2.0, 3.0, 4.0])
    assert mean == pytest.approx(2.5)
    assert se == pytest.approx(0.6454972244)


def test_identifies_strict_interior_threshold():
    result = select_threshold_one_se(
        [
            score(0.50, 0.52),
            score(0.55, 0.48),
            score(0.60, 0.40, 0.01),
            score(0.65, 0.46),
            score(0.70, 0.50),
        ],
        no_threshold_mean_log_loss=0.45,
    )
    assert result.status == "BEHAVIORAL_THRESHOLD_IDENTIFIED"
    assert result.selected_q == pytest.approx(0.60)


def test_boundary_optimum_fails_closed():
    result = select_threshold_one_se(
        [
            score(0.50, 0.39),
            score(0.55, 0.42),
            score(0.60, 0.44),
        ],
        no_threshold_mean_log_loss=0.45,
    )
    assert result.status == "THRESHOLD_NOT_IDENTIFIED"
    assert result.reason == "best_candidate_on_grid_boundary"


def test_threshold_must_beat_continuous_no_threshold_model():
    result = select_threshold_one_se(
        [
            score(0.50, 0.50),
            score(0.55, 0.44),
            score(0.60, 0.50),
        ],
        no_threshold_mean_log_loss=0.43,
    )
    assert result.status == "THRESHOLD_NOT_IDENTIFIED"
    assert result.reason == (
        "best_threshold_does_not_beat_no_threshold_model"
    )


def test_adjacent_point_within_one_se_is_a_tie():
    result = select_threshold_one_se(
        [
            score(0.50, 0.50),
            score(0.55, 0.411),
            score(0.60, 0.400, 0.012),
            score(0.65, 0.48),
            score(0.70, 0.52),
        ],
        no_threshold_mean_log_loss=0.45,
    )
    assert result.status == "THRESHOLD_NOT_IDENTIFIED"
    assert result.reason == "adjacent_grid_point_tied_within_one_se"
