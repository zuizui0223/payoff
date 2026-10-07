"""Outcome-blind chronological split for the PAYOFF-B racing test."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from math import floor, isfinite
from typing import Iterable, Mapping


@dataclass(frozen=True)
class ChronologicalDateSplit:
    train_dates: tuple[date, ...]
    test_dates: tuple[date, ...]
    assignment: Mapping[date, str]
    train_fraction: float


def chronological_date_split(
    race_dates: Iterable[date],
    *,
    train_fraction: float = 0.70,
) -> ChronologicalDateSplit:
    """Assign whole race dates to train/test without reading outcomes.

    Unique dates are sorted.  The earliest floor(fraction * n_dates) dates are
    train, subject to at least one date in each split.
    """

    fraction = float(train_fraction)
    if not isfinite(fraction) or not 0.0 < fraction < 1.0:
        raise ValueError("train_fraction must lie strictly between zero and one")

    dates = sorted(set(race_dates))
    if len(dates) < 2:
        raise ValueError("at least two distinct race dates are required")

    n_train = floor(fraction * len(dates))
    n_train = max(1, min(n_train, len(dates) - 1))
    train = tuple(dates[:n_train])
    test = tuple(dates[n_train:])
    assignment = {
        d: ("train" if d in set(train) else "test")
        for d in dates
    }
    return ChronologicalDateSplit(
        train_dates=train,
        test_dates=test,
        assignment=assignment,
        train_fraction=fraction,
    )
