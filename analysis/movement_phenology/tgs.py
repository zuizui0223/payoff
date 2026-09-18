"""Thermal growing season onset used in van Toor et al. (2021).

The published supplementary code defines TGS onset for a daily mean-temperature
series x and day labels d as:

    cum.t = cumsum(x - 5)
    tgs = d[which.min(cum.t)]

The onset is therefore the day after which cumulative thermal surplus relative
to 5 °C begins to recover from its winter minimum. Negative daily values are
NOT truncated for this TGS-onset calculation.

This module reproduces that declared transformation. It is separate from the
GDD-jerk method used for the Svalbard goose analysis.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


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
    temp = np.asarray(list(mean_daily_temperature_c), dtype=float)
    if temp.ndim != 1 or temp.size < 30:
        raise ValueError("temperature series must be one-dimensional and >=30 days")
    if not np.all(np.isfinite(temp)):
        raise ValueError("temperature series must contain only finite values")

    if day_of_year is None:
        doy = np.arange(1, temp.size + 1, dtype=int)
    else:
        doy = np.asarray(list(day_of_year), dtype=int)
        if doy.shape != temp.shape:
            raise ValueError("day_of_year must match temperature length")
        if np.any(np.diff(doy) <= 0):
            raise ValueError("day_of_year must be strictly increasing")

    threshold = float(threshold_c)
    if not np.isfinite(threshold):
        raise ValueError("threshold must be finite")

    cumulative = np.cumsum(temp - threshold)
    idx = int(np.argmin(cumulative))
    return ThermalGrowingSeasonOnset(
        onset_day=int(doy[idx]),
        onset_index=idx,
        threshold_c=threshold,
        cumulative_minimum=float(cumulative[idx]),
    )
