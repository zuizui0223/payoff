"""Select fixed-interval GPS targets before environmental phase is attached.

This module freezes temporal sampling geometry independently of environmental
availability. Environmental quality can invalidate a selected target later, but
it cannot cause a different GPS observation to be selected for that target.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from math import isfinite
from typing import Iterable


@dataclass(frozen=True)
class GPSObservation:
    observation_id: str
    animal_id: str
    animal_year: str
    group: str
    timestamp: datetime
    pixel_id: str

    def __post_init__(self) -> None:
        for name in (
            "observation_id",
            "animal_id",
            "animal_year",
            "group",
            "pixel_id",
        ):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} must be non-empty")


@dataclass(frozen=True)
class FixedIntervalGPSTarget:
    animal_id: str
    animal_year: str
    group: str
    target_index: int
    target_timestamp: datetime
    observation_id: str
    observed_timestamp: datetime
    deviation_seconds: float
    pixel_id: str


@dataclass(frozen=True)
class FixedIntervalGPSSelection:
    target_interval_seconds: float
    max_target_deviation_seconds: float
    raw_observations: int
    animal_years_seen: int
    animal_years_with_targets: int
    selected_targets: tuple[FixedIntervalGPSTarget, ...]


def _closest(
    rows: tuple[GPSObservation, ...],
    target: datetime,
    max_deviation_seconds: float,
) -> GPSObservation | None:
    if not rows:
        return None
    deviation, row = min(
        (
            abs((row.timestamp - target).total_seconds()),
            row,
        )
        for row in rows
    )
    if deviation > max_deviation_seconds:
        return None
    return row


def select_fixed_interval_gps_targets(
    observations: Iterable[GPSObservation],
    *,
    target_interval_seconds: float = 86400.0,
    max_target_deviation_seconds: float = 10800.0,
) -> FixedIntervalGPSSelection:
    """Select nearest raw GPS observations on an animal-year target grid.

    The grid anchor is the earliest raw spring-migration observation in each
    animal-year. Matching windows may not overlap adjacent targets.
    """

    if (
        not isfinite(target_interval_seconds)
        or target_interval_seconds <= 0.0
    ):
        raise ValueError("target_interval_seconds must be positive and finite")
    if (
        not isfinite(max_target_deviation_seconds)
        or max_target_deviation_seconds < 0.0
    ):
        raise ValueError(
            "max_target_deviation_seconds must be non-negative and finite"
        )
    if 2.0 * max_target_deviation_seconds >= target_interval_seconds:
        raise ValueError(
            "target matching windows must not overlap adjacent targets"
        )

    rows = tuple(observations)
    by_year: dict[str, list[GPSObservation]] = {}
    for row in rows:
        by_year.setdefault(row.animal_year, []).append(row)

    selected: list[FixedIntervalGPSTarget] = []
    years_with_targets: set[str] = set()
    interval = timedelta(seconds=target_interval_seconds)

    for animal_year, year_list in by_year.items():
        year_rows = tuple(sorted(year_list, key=lambda row: row.timestamp))
        if not year_rows:
            continue

        animals = {row.animal_id for row in year_rows}
        groups = {row.group for row in year_rows}
        if len(animals) != 1:
            raise ValueError(
                f"animal_year {animal_year!r} contains multiple animal IDs"
            )
        if len(groups) != 1:
            raise ValueError(
                f"animal_year {animal_year!r} contains multiple groups"
            )

        animal_id = next(iter(animals))
        group = next(iter(groups))
        anchor = year_rows[0].timestamp
        last = year_rows[-1].timestamp

        index = 0
        target = anchor
        while target <= last:
            matched = _closest(
                year_rows,
                target,
                max_target_deviation_seconds,
            )
            if matched is not None:
                selected.append(
                    FixedIntervalGPSTarget(
                        animal_id=animal_id,
                        animal_year=animal_year,
                        group=group,
                        target_index=index,
                        target_timestamp=target,
                        observation_id=matched.observation_id,
                        observed_timestamp=matched.timestamp,
                        deviation_seconds=(
                            matched.timestamp - target
                        ).total_seconds(),
                        pixel_id=matched.pixel_id,
                    )
                )
                years_with_targets.add(animal_year)
            index += 1
            target = anchor + index * interval

    return FixedIntervalGPSSelection(
        target_interval_seconds=target_interval_seconds,
        max_target_deviation_seconds=max_target_deviation_seconds,
        raw_observations=len(rows),
        animal_years_seen=len(by_year),
        animal_years_with_targets=len(years_with_targets),
        selected_targets=tuple(selected),
    )
