from datetime import date

import pytest

from src.racing_chronological_split import chronological_date_split


def test_split_uses_earliest_dates_for_train_and_latest_for_test():
    dates = [date(2026, 1, d) for d in range(1, 11)]
    out = chronological_date_split(dates, train_fraction=0.7)
    assert len(out.train_dates) == 7
    assert len(out.test_dates) == 3
    assert max(out.train_dates) < min(out.test_dates)
    assert out.assignment[date(2026, 1, 1)] == "train"
    assert out.assignment[date(2026, 1, 10)] == "test"


def test_duplicate_dates_do_not_change_boundary():
    dates = [
        date(2026, 1, 1),
        date(2026, 1, 1),
        date(2026, 1, 2),
        date(2026, 1, 3),
    ]
    out = chronological_date_split(dates, train_fraction=2 / 3)
    assert out.train_dates == (date(2026, 1, 1), date(2026, 1, 2))
    assert out.test_dates == (date(2026, 1, 3),)


def test_small_panel_keeps_one_date_in_each_split():
    out = chronological_date_split(
        [date(2026, 1, 1), date(2026, 1, 2)],
        train_fraction=0.9,
    )
    assert len(out.train_dates) == 1
    assert len(out.test_dates) == 1


def test_invalid_fraction_fails_closed():
    with pytest.raises(ValueError, match="strictly between"):
        chronological_date_split(
            [date(2026, 1, 1), date(2026, 1, 2)],
            train_fraction=1.0,
        )
