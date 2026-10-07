import pytest

from src.v7b_environment_manifest import (
    FeedbackRegion,
    build_feedback_appeears_manifest,
)


def _regions():
    return [
        FeedbackRegion("greenland", "R1", 54.126991, -10.208300),
        FeedbackRegion("barents", "R1", 53.473599, 6.758965),
    ]


def test_manifest_is_year_scoped_and_behavior_independent():
    out = build_feedback_appeears_manifest(
        _regions(),
        years=[2006, 2007, 2008],
    )
    assert out["region_count"] == 2
    assert out["expected_region_years"] == 6
    assert out["task_count"] == 3
    assert out["years"] == [2006, 2007, 2008]
    for task in out["tasks"]:
        assert task["region_count"] == 2
        assert len(task["task"]["params"]["coordinates"]) == 2


def test_region_ids_must_be_unique_across_flyway_region_key():
    with pytest.raises(ValueError, match="unique"):
        build_feedback_appeears_manifest(
            [
                FeedbackRegion("x", "R1", 50, 10),
                FeedbackRegion("x", "R1", 51, 11),
            ],
            years=[2008],
        )


def test_v7b_declared_years_are_not_inferred_from_behavior():
    out = build_feedback_appeears_manifest(_regions(), years=range(2006, 2012))
    assert out["expected_region_years"] == 12
    assert out["task_count"] == 6
