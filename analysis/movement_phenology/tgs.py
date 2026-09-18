"""Thermal growing season onset used in van Toor et al. (2021).

Published supplementary code:
    cum.t = cumsum(x - 5)
    tgs = d[which.min(cum.t)]

Negative daily values are not truncated. This module deliberately uses only
the Python standard library so the exact transformation is testable in the
repository's minimal CI environment.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable


@dataclass(frozen=True)
class ThermalGrowingSeasonOnset:
    onset_day: int
    onset_index: int
    threshold_c: float
    cumulative_minimum: float


def thermal_growing_season_onset(
    mean_daily_temperature_c: Iterable[float],
    day_of_year: Iterable[int] | None = None,
    *,
    threshold_c: float = 5.0,
) -> ThermalGrowingSeasonOnset:
    """Return TGS onset using the exact cumulative-minimum rule."""
    temp = [float(x) for x in mean_daily_temperature_c]
    if len(temp) < 30:
        raise ValueError("temperature series must contain at least 30 days")
    if not all(math.isfinite(x) for x in temp):
        raise ValueError("temperature series must contain only finite values")

    if day_of_year is None:
        doy = list(range(1, len(temp) + 1))
    else:
        doy = [int(x) for x in day_of_year]
        if len(doy) != len(temp):
            raise ValueError("day_of_year must match temperature length")
        if any(b <= a for a, b in zip(doy, doy[1:])):
            raise ValueError("day_of_year must be strictly increasing")

    threshold = float(threshold_c)
    if not math.isfinite(threshold):
        raise ValueError("threshold must be finite")

    cumulative = []
    running = 0.0
    for value in temp:
        running += value - threshold
        cumulative.append(running)

    idx = min(range(len(cumulative)), key=cumulative.__getitem__)
    return ThermalGrowingSeasonOnset(
        onset_day=doy[idx],
        onset_index=idx,
        threshold_c=threshold,
        cumulative_minimum=cumulative[idx],
    )
