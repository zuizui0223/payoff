"""Fixed-interval phase-pair reconstruction for environmental tracking tests.

This layer assumes environmental extraction has already attached a local peak
date/time to each movement location. It then freezes the temporal sampling
geometry before lambda is estimated.

No lambda model is fit here. The output is a table of fixed-interval phase
pairs that can be passed to a preregistered regression / contrast model.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from math import isfinite
from typing import Iterable


@dataclass(frozen=True)
class PhaseLocation:
    animal_id: str
    animal_year: str
    group: str
    timestamp: datetime
    local_peak_timestamp: datetime

    def __post_init__(self) -> None:
        for name in ("animal_id", "animal_year", "group"):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} must be non-empty")

    @property
    def phase_error_days(self) -> float:
        return (
            self.timestamp - self.local_peak_timestamp
        ).total_seconds() / 86400.0


@dataclass(frozen=True)
class FixedIntervalPhasePoint:
    animal_id: str
    animal_year: str
    group: str
    target_index: int
    target_timestamp: datetime
    observed_timestamp: datetime
    deviation_seconds: float
    phase_error_days: float


@dataclass(frozen=True)
class FixedIntervalPhasePair:
    animal_id: str
    animal_year: str
    group: str
    start_target_index: int
    start_timestamp: datetime
    end_timestamp: datetime
    phase_before: float
    phase_after: float


@dataclass(frozen=True)
class PhasePairReconstruction:
    target_interval_seconds: float
    max_target_deviation_seconds: float
    animal_years_seen: int
    animal_years_with_pairs: int
    matched_phase_points: int
    phase_pairs: tuple[FixedIntervalPhasePair, ...]

    @property
    def groups(self) -> tuple[str, ...]:
        return tuple(
            dict.fromkeys(pair.group for pair in self.phase_pairs)
        )


def _closest_observation(
    rows: tuple[PhaseLocation, ...],
    target: datetime,
    max_deviation_seconds: float,
) -> PhaseLocation | None:
    candidates = [
        (
            abs((row.timestamp - target).total_seconds()),
            row,
        )
        for row in rows
    ]
    if not candidates:
        return None
    deviation, row = min(
        candidates,
        key=lambda item: item[0],
    )
    if deviation > max_deviation_seconds:
        return None
    return row


def reconstruct_fixed_interval_phase_pairs(
    observations: Iterable[PhaseLocation],
    *,
    target_interval_seconds: float = 86400.0,
    max_target_deviation_seconds: float = 10800.0,
) -> PhasePairReconstruction:
    """Create consecutive fixed-interval phase pairs within animal-years.

    The target grid is anchored at each animal-year's earliest valid location.
    A target receives the nearest observation only when it falls within the
    predeclared temporal tolerance.

    Pairs are formed only between adjacent target indices. A missing target
    breaks the chain rather than stretching a longer interval into the declared
    segment scale.
    """

    if (
        not isfinite(target_interval_seconds)
        or target_interval_seconds <= 0.0
    ):
        raise ValueError(
            "target_interval_seconds must be positive and finite"
        )
    if (
        not isfinite(max_target_deviation_seconds)
        or max_target_deviation_seconds < 0.0
    ):
        raise ValueError(
            "max_target_deviation_seconds must be non-negative and finite"
        )
    if (
        2.0 * max_target_deviation_seconds
        >= target_interval_seconds
    ):
        raise ValueError(
            "target matching windows must not overlap adjacent targets"
        )

    rows = tuple(observations)
    by_year: dict[str, list[PhaseLocation]] = {}
    for row in rows:
        by_year.setdefault(row.animal_year, []).append(row)

    matched_points: list[FixedIntervalPhasePoint] = []
    pairs: list[FixedIntervalPhasePair] = []
    years_with_pairs: set[str] = set()

    interval = timedelta(seconds=target_interval_seconds)

    for animal_year, year_rows_list in by_year.items():
        year_rows = tuple(
            sorted(
                year_rows_list,
                key=lambda row: row.timestamp,
            )
        )
        if len(year_rows) < 2:
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

        points_by_index: dict[int, FixedIntervalPhasePoint] = {}
        index = 0
        target = anchor
        while target <= last:
            matched = _closest_observation(
                year_rows,
                target,
                max_target_deviation_seconds,
            )
            if matched is not None:
                deviation = (
                    matched.timestamp - target
                ).total_seconds()
                point = FixedIntervalPhasePoint(
                    animal_id=animal_id,
                    animal_year=animal_year,
                    group=group,
                    target_index=index,
                    target_timestamp=target,
                    observed_timestamp=matched.timestamp,
                    deviation_seconds=deviation,
                    phase_error_days=matched.phase_error_days,
                )
                points_by_index[index] = point
                matched_points.append(point)

            index += 1
            target = anchor + index * interval

        for start_index in sorted(points_by_index):
            end_index = start_index + 1
            if end_index not in points_by_index:
                continue
            start = points_by_index[start_index]
            end = points_by_index[end_index]
            pairs.append(
                FixedIntervalPhasePair(
                    animal_id=animal_id,
                    animal_year=animal_year,
                    group=group,
                    start_target_index=start_index,
                    start_timestamp=start.target_timestamp,
                    end_timestamp=end.target_timestamp,
                    phase_before=start.phase_error_days,
                    phase_after=end.phase_error_days,
                )
            )
            years_with_pairs.add(animal_year)

    return PhasePairReconstruction(
        target_interval_seconds=target_interval_seconds,
        max_target_deviation_seconds=max_target_deviation_seconds,
        animal_years_seen=len(by_year),
        animal_years_with_pairs=len(years_with_pairs),
        matched_phase_points=len(matched_points),
        phase_pairs=tuple(pairs),
    )
