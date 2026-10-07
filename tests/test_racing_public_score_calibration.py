import pytest

from src.racing_public_score_calibration import (
    PublicScoreRace,
    fit_public_score_scale,
    public_score_log_loss,
    standardized_score_probabilities,
)


def test_zero_scale_is_uniform():
    out = standardized_score_probabilities(
        {"A": 80.0, "B": 20.0},
        scale=0.0,
    )
    assert out == pytest.approx({"A": 0.5, "B": 0.5})


def test_higher_score_gets_higher_probability():
    out = standardized_score_probabilities(
        {"A": 80.0, "B": 50.0, "C": 20.0},
        scale=1.0,
    )
    assert out["A"] > out["B"] > out["C"]
    assert sum(out.values()) == pytest.approx(1.0)


def test_affine_score_rescaling_does_not_change_standardized_probabilities():
    one = standardized_score_probabilities(
        {"A": 80.0, "B": 50.0, "C": 20.0},
        scale=1.3,
    )
    two = standardized_score_probabilities(
        {"A": 180.0, "B": 120.0, "C": 60.0},
        scale=1.3,
    )
    assert one == pytest.approx(two)


def test_training_finds_positive_scale_when_score_ranks_winners():
    races = [
        PublicScoreRace("r1", "A", {"A": 90.0, "B": 40.0}),
        PublicScoreRace("r2", "B", {"A": 30.0, "B": 85.0}),
        PublicScoreRace("r3", "A", {"A": 75.0, "B": 50.0}),
        PublicScoreRace("r4", "B", {"A": 45.0, "B": 80.0}),
    ]
    fitted = fit_public_score_scale(races, max_scale=3.0, grid_points=301)
    assert fitted.scale > 0.0
    assert fitted.training_log_loss < public_score_log_loss(races, scale=0.0)


def test_equal_scores_remain_uniform_at_positive_scale():
    out = standardized_score_probabilities(
        {"A": 50.0, "B": 50.0, "C": 50.0},
        scale=2.0,
    )
    assert out == pytest.approx({"A": 1 / 3, "B": 1 / 3, "C": 1 / 3})
