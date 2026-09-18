"""Growing-degree-day jerk reconstruction following van Wijk et al. logic.

The empirical recipe is:
1. latitude-dependent T_base = -0.25*latitude + 13 °C;
2. daily GDU = max(T_mean - T_base, 0);
3. cumulative GDD from 1 January;
4. fit a logistic sigmoid to annual cumulative GDD;
5. define onset of spring as the early-season positive maximum of the third
   derivative of the fitted sigmoid (GDD jerk).

The fit is a reproducible modern reconstruction, not byte-identical recovery of
the original authors' historical ECA/NOAA temperature inputs.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable

import numpy as np
from scipy.optimize import curve_fit


EARLY_JERK_FRACTION = 0.5 - math.sqrt(6.0) / 6.0
EARLY_JERK_LOGIT = math.log(
    EARLY_JERK_FRACTION / (1.0 - EARLY_JERK_FRACTION)
)


@dataclass(frozen=True)
class GDDJerkFit:
    asymptote: float
    rate: float
    midpoint_day: float
    onset_day: float
    r_squared: float
    t_base: float


def latitude_base_temperature(latitude_deg: float) -> float:
    """van Wijk latitude-dependent plant-growth base temperature (°C)."""
    lat = float(latitude_deg)
    if not math.isfinite(lat) or lat < -90 or lat > 90:
        raise ValueError("latitude must be finite and within [-90, 90]")
    return -0.25 * lat + 13.0


def growing_degree_days(
    mean_daily_temperature_c: Iterable[float],
    latitude_deg: float,
) -> np.ndarray:
    """Cumulative GDD from Jan 1 with negative daily GDU truncated at zero."""
    temp = np.asarray(list(mean_daily_temperature_c), dtype=float)
    if temp.ndim != 1 or temp.size < 10:
        raise ValueError("temperature series must be one-dimensional and nontrivial")
    if not np.all(np.isfinite(temp)):
        raise ValueError("temperature series must be finite")
    tbase = latitude_base_temperature(latitude_deg)
    gdu = np.maximum(temp - tbase, 0.0)
    return np.cumsum(gdu)


def logistic_gdd(day, asymptote, rate, midpoint_day):
    day = np.asarray(day, dtype=float)
    z = np.clip(-rate * (day - midpoint_day), -700, 700)
    return asymptote / (1.0 + np.exp(z))


def logistic_third_derivative(day, asymptote, rate, midpoint_day):
    """Third derivative d^3 GDD / d day^3 of the fitted logistic."""
    day = np.asarray(day, dtype=float)
    f = 1.0 / (
        1.0 + np.exp(np.clip(-rate * (day - midpoint_day), -700, 700))
    )
    return (
        asymptote
        * rate**3
        * f
        * (1.0 - f)
        * (1.0 - 6.0 * f + 6.0 * f**2)
    )


def early_jerk_peak_day(rate: float, midpoint_day: float) -> float:
    """Analytic early positive maximum of logistic third derivative."""
    k = float(rate)
    t0 = float(midpoint_day)
    if not math.isfinite(k) or not math.isfinite(t0) or k <= 0:
        raise ValueError("rate must be positive and parameters finite")
    return t0 + EARLY_JERK_LOGIT / k


def fit_gdd_jerk(
    mean_daily_temperature_c: Iterable[float],
    latitude_deg: float,
    *,
    min_r_squared: float = 0.95,
) -> GDDJerkFit:
    """Fit annual GDD sigmoid and return the spring GDD-jerk onset day."""
    temp = np.asarray(list(mean_daily_temperature_c), dtype=float)
    gdd = growing_degree_days(temp, latitude_deg)
    days = np.arange(1, len(gdd) + 1, dtype=float)

    max_gdd = float(gdd[-1])
    if not math.isfinite(max_gdd) or max_gdd <= 1.0:
        raise ValueError("annual GDD accumulation is too small for sigmoid fitting")

    target = max_gdd / 2.0
    midpoint_guess = float(days[np.argmin(np.abs(gdd - target))])

    popt, _ = curve_fit(
        logistic_gdd,
        days,
        gdd,
        p0=(max_gdd, 0.03, midpoint_guess),
        bounds=(
            (0.5 * max_gdd, 0.001, 1.0),
            (2.0 * max_gdd, 1.0, float(len(gdd))),
        ),
        maxfev=50000,
    )
    asymptote, rate, midpoint = [float(x) for x in popt]
    pred = logistic_gdd(days, *popt)
    residual_ss = float(np.sum((gdd - pred) ** 2))
    total_ss = float(np.sum((gdd - np.mean(gdd)) ** 2))
    r2 = 1.0 - residual_ss / total_ss if total_ss > 0 else float("nan")
    onset = early_jerk_peak_day(rate, midpoint)

    if not math.isfinite(r2) or r2 < min_r_squared:
        raise ValueError(f"GDD logistic fit below r2 gate: {r2:.4f}")
    if onset < 1 or onset > len(gdd):
        raise ValueError(f"spring jerk onset outside annual support: {onset:.2f}")

    return GDDJerkFit(
        asymptote=asymptote,
        rate=rate,
        midpoint_day=midpoint,
        onset_day=onset,
        r_squared=r2,
        t_base=latitude_base_temperature(latitude_deg),
    )
