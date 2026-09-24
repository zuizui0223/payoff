import pytest

from src.tracking_empirical_split import deterministic_group_split


def test_group_split_is_invariant_to_input_order():
    groups = ["A", "B", "C", "D", "E"]
    first = deterministic_group_split(
        groups,
        holdout_fraction=0.4,
        seed="x",
    )
    second = deterministic_group_split(
        list(reversed(groups)),
        holdout_fraction=0.4,
        seed="x",
    )
    assert first == second


def test_group_split_has_no_leakage_and_complete_coverage():
    groups = ["A", "B", "C", "D", "E", "F"]
    split = deterministic_group_split(
        groups,
        holdout_fraction=0.33,
        seed="mule-deer",
    )
    training = set(split.training_groups)
    held = set(split.held_out_groups)

    assert training.isdisjoint(held)
    assert training | held == set(groups)
    assert len(training) >= 1
    assert len(held) >= 1


def test_group_split_requires_at_least_two_groups():
    with pytest.raises(ValueError):
        deterministic_group_split(
            ["A"],
            holdout_fraction=0.2,
        )


def test_group_split_realized_fraction_is_reported():
    split = deterministic_group_split(
        ["A", "B", "C", "D", "E"],
        holdout_fraction=0.4,
        seed="x",
    )
    assert split.realized_holdout_fraction == pytest.approx(0.4)
