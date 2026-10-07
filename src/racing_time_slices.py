"""Deterministic pre-race time-slice selection for irregular odds snapshots.

JRA-VAN time-series odds are recorded at irregular 5--10 minute intervals.
For a target T-k, the primary rule is:

    choose the latest snapshot at or before post_time - k minutes,

never borrowing information from after the target time.

A maximum staleness gate can then exclude races where the previous snapshot is
too old for the declared slice.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from math import isfinite
from typing import Mapping, Sequence


@dataclass(frozen=True)
class OddsSnapshot:
    observed_at: datetime
    decimal_odds: Mapping[str, float]


@dataclass(frozen=True)
class SelectedTimeSlice:
    label: str
    target_at: datetime | None
    observed_at: datetime
    staleness_minutes: float | None
    decimal_odds: Mapping[str, float]


def _validate_snapshots(
    post_time: datetime,
    snapshots: Sequence[OddsSnapshot],
) -> list[OddsSnapshot]:
    if not snapshots:
        raise ValueError("at least one odds snapshot is required")
    out = sorted(snapshots, key=lambda x: x.observed_at)
    for snap in out:
        if snap.observed_at.tzinfo != post_time.tzinfo:
            # datetime equality between differently-aware objects can be valid,
            # but explicit consistency prevents accidental local/UTC mixing.
            raise ValueError("post_time and snapshot timezone awareness must match")
        if snap.observed_at >= post_time:
            raise ValueError("all primary snapshots must be strictly pre-post")
        if not snap.decimal_odds:
            raise ValueError("snapshot odds must not be empty")
        for value in snap.decimal_odds.values():
            odds = float(value)
            if not isfinite(odds) or odds <= 1.0:
                raise ValueError("decimal odds must be finite and greater than one")
    return out


def select_target_slice(
    *,
    post_time: datetime,
    snapshots: Sequence[OddsSnapshot],
    minutes_before_post: float,
    max_staleness_minutes: float = 10.0,
) -> SelectedTimeSlice | None:
    """Select latest snapshot at or before T-k, subject to a staleness gate."""

    minutes = float(minutes_before_post)
    stale_max = float(max_staleness_minutes)
    if not isfinite(minutes) or minutes < 0.0:
        raise ValueError("minutes_before_post must be finite and non-negative")
    if not isfinite(stale_max) or stale_max < 0.0:
        raise ValueError("max_staleness_minutes must be finite and non-negative")

    ordered = _validate_snapshots(post_time, snapshots)
    target = post_time - timedelta(minutes=minutes)
    eligible = [snap for snap in ordered if snap.observed_at <= target]
    if not eligible:
        return None

    chosen = eligible[-1]
    staleness = (target - chosen.observed_at).total_seconds() / 60.0
    if staleness > stale_max:
        return None

    label = f"T-{minutes:g}"
    return SelectedTimeSlice(
        label=label,
        target_at=target,
        observed_at=chosen.observed_at,
        staleness_minutes=staleness,
        decimal_odds=chosen.decimal_odds,
    )


def select_last_preclose_slice(
    *,
    post_time: datetime,
    snapshots: Sequence[OddsSnapshot],
) -> SelectedTimeSlice:
    """Select the latest available snapshot strictly before post."""

    ordered = _validate_snapshots(post_time, snapshots)
    chosen = ordered[-1]
    return SelectedTimeSlice(
        label="LAST",
        target_at=None,
        observed_at=chosen.observed_at,
        staleness_minutes=None,
        decimal_odds=chosen.decimal_odds,
    )


def select_primary_time_slices(
    *,
    post_time: datetime,
    snapshots: Sequence[OddsSnapshot],
    targets_minutes: Sequence[float] = (30, 15, 10, 5),
    max_staleness_minutes: float = 10.0,
) -> dict[str, SelectedTimeSlice] | None:
    """Return the retrospective primary panel, or None if any target is missing.

    The default starts at T-30 because the historical accumulated TM category-7
    score corresponds to the final pre-race forecast but does not preserve the
    original realtime release timestamp.  Earlier slices can be supplied
    explicitly for prospectively archived forecasts.
    """

    selected: dict[str, SelectedTimeSlice] = {}
    for minutes in targets_minutes:
        out = select_target_slice(
            post_time=post_time,
            snapshots=snapshots,
            minutes_before_post=minutes,
            max_staleness_minutes=max_staleness_minutes,
        )
        if out is None:
            return None
        selected[out.label] = out
    last = select_last_preclose_slice(post_time=post_time, snapshots=snapshots)
    selected[last.label] = last
    return selected
