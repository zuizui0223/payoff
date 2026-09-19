"""Published-parameter reconstruction of the van Toor et al. (2021) wigeon HMM.

The constants below are copied from the rendered output in the published
Additional file 2. The purpose is reproducibility: apply the fitted 4-state
model to the public hourly relocation release without re-optimising the HMM.

States:
  1 rest
  2 non-flight
  3 local
  4 migratory

Data streams:
  sqrt(step_km) ~ zero-inflated Gamma(mean, sd)
  turning angle ~ wrapped Cauchy(mean, concentration)

Transition probabilities:
  multinomial logit with diagonal state as reference and
  cosinor(solar.time, 24) covariates.

This module does not claim that the published model is optimal for later data.
"""

from __future__ import annotations

from datetime import datetime
import math
from typing import Iterable

import numpy as np
from scipy.special import gammaln


STATE_NAMES = ("rest", "non-flight", "local", "migratory")

# Published fitted natural-scale emission parameters.
STEP_MEAN = np.array(
    [0.128664858, 0.1858785, 0.6784584, 5.94177657], dtype=float
)
STEP_SD = np.array(
    [0.055641704, 0.09139112, 0.5206647, 3.43782467], dtype=float
)
STEP_ZEROMASS = np.array(
    [0.001096904, 0.00008297645, 2.496826e-08, 0.00050036],
    dtype=float,
)
ANGLE_MEAN = np.array(
    [3.0379532, 3.0818308, -3.1311348, -0.01804231], dtype=float
)
ANGLE_CONCENTRATION = np.array(
    [0.2437448, 0.2235447, 0.1759502, 0.70656025], dtype=float
)

# Published fitted initial distribution.
INITIAL = np.array(
    [0.2615390, 0.000007038665, 0.6574345, 0.08101948], dtype=float
)
INITIAL = INITIAL / INITIAL.sum()

# Off-diagonal transition coefficient order printed by momentuHMM:
# 1->2,1->3,1->4,2->1,2->3,2->4,3->1,3->2,3->4,4->1,4->2,4->3
TRANSITION_PAIRS = (
    (0, 1), (0, 2), (0, 3),
    (1, 0), (1, 2), (1, 3),
    (2, 0), (2, 1), (2, 3),
    (3, 0), (3, 1), (3, 2),
)
BETA_INTERCEPT = np.array(
    [
        -8.205742, 15.533307, 16.893860,
        -24.9059645, -1.68437037, -24.09154,
        -19.8808075, -0.69363916, -3.5941067,
        -9.697017, -5.696363, -1.3335465,
    ],
    dtype=float,
)
BETA_COS = np.array(
    [
        -5.504056, -21.802332, -26.561837,
        1.5919918, 0.32587907, 13.23344,
        1.8852942, 0.35518817, 1.3532394,
        5.109482, 1.819372, -0.7719263,
    ],
    dtype=float,
)
BETA_SIN = np.array(
    [
        -1.811885, 4.432808, 6.646195,
        0.5268574, 0.09330654, -18.32243,
        -0.2829929, -0.02313476, -0.3926681,
        -7.741996, 4.757073, 1.7081092,
    ],
    dtype=float,
)

EARTH_KM = 6371.0088


def _log_gamma_mean_sd(x: float, mean: float, sd: float) -> float:
    shape = (mean / sd) ** 2
    scale = sd * sd / mean
    return (
        (shape - 1.0) * math.log(x)
        - x / scale
        - gammaln(shape)
        - shape * math.log(scale)
    )


def _log_wrapped_cauchy(x: float, mean: float, rho: float) -> float:
    den = 1.0 + rho * rho - 2.0 * rho * math.cos(x - mean)
    return math.log1p(-(rho * rho)) - math.log(2.0 * math.pi) - math.log(den)


def emission_log_prob(step_sqrt: float, angle: float) -> np.ndarray:
    """Log emission probability for one observation in all four states.

    Missing streams contribute a multiplicative factor of one, matching the
    usual HMM treatment of missing observations.
    """
    out = np.zeros(4, dtype=float)

    if step_sqrt is not None and math.isfinite(float(step_sqrt)):
        x = float(step_sqrt)
        for k in range(4):
            zm = float(STEP_ZEROMASS[k])
            if x <= 0.0:
                out[k] += math.log(max(zm, 1e-300))
            else:
                out[k] += math.log(max(1.0 - zm, 1e-300))
                out[k] += _log_gamma_mean_sd(
                    x, float(STEP_MEAN[k]), float(STEP_SD[k])
                )

    if angle is not None and math.isfinite(float(angle)):
        x = float(angle)
        for k in range(4):
            out[k] += _log_wrapped_cauchy(
                x, float(ANGLE_MEAN[k]), float(ANGLE_CONCENTRATION[k])
            )
    return out


def transition_matrix(solar_time_hours: float) -> np.ndarray:
    """Published multinomial-logit transition matrix at local solar time."""
    h = float(solar_time_hours) % 24.0
    theta = 2.0 * math.pi * h / 24.0
    eta = BETA_INTERCEPT + BETA_COS * math.cos(theta) + BETA_SIN * math.sin(theta)

    mat = np.zeros((4, 4), dtype=float)
    by_row: dict[int, list[tuple[int, float]]] = {i: [] for i in range(4)}
    for (i, j), value in zip(TRANSITION_PAIRS, eta):
        by_row[i].append((j, float(value)))

    for i in range(4):
        logits = np.zeros(4, dtype=float)  # diagonal is the reference category
        for j, value in by_row[i]:
            logits[j] = value
        mx = float(np.max(logits))
        weights = np.exp(logits - mx)
        mat[i] = weights / weights.sum()
    return mat


def solar_time_hours(timestamp_utc: datetime, longitude_deg: float) -> float:
    """Approximate apparent solar time using the NOAA equation-of-time formula.

    maptools::solarnoon was used in the published R code. This implementation
    provides a transparent near-equivalent for the transition covariate.
    """
    if timestamp_utc.tzinfo is None:
        raise ValueError("timestamp must be timezone-aware UTC")
    lon = float(longitude_deg)
    doy = timestamp_utc.timetuple().tm_yday
    hour = (
        timestamp_utc.hour
        + timestamp_utc.minute / 60.0
        + timestamp_utc.second / 3600.0
    )
    gamma = 2.0 * math.pi / 365.0 * (doy - 1 + (hour - 12.0) / 24.0)
    eqtime_min = 229.18 * (
        0.000075
        + 0.001868 * math.cos(gamma)
        - 0.032077 * math.sin(gamma)
        - 0.014615 * math.cos(2 * gamma)
        - 0.040849 * math.sin(2 * gamma)
    )
    return (hour + lon / 15.0 + eqtime_min / 60.0) % 24.0


def haversine_km(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    p1 = math.radians(float(lat1))
    p2 = math.radians(float(lat2))
    dp = p2 - p1
    dl = math.radians(float(lon2) - float(lon1))
    a = (
        math.sin(dp / 2.0) ** 2
        + math.cos(p1) * math.cos(p2) * math.sin(dl / 2.0) ** 2
    )
    return 2.0 * EARTH_KM * math.asin(min(1.0, math.sqrt(a)))


def initial_bearing_rad(
    lon1: float, lat1: float, lon2: float, lat2: float
) -> float:
    p1 = math.radians(float(lat1))
    p2 = math.radians(float(lat2))
    dl = math.radians(float(lon2) - float(lon1))
    y = math.sin(dl) * math.cos(p2)
    x = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    return math.atan2(y, x)


def wrap_angle(x: float) -> float:
    return (float(x) + math.pi) % (2.0 * math.pi) - math.pi


def movement_streams(
    longitude: Iterable[float],
    latitude: Iterable[float],
) -> tuple[np.ndarray, np.ndarray]:
    """Reproduce momentuHMM prepData alignment for LL step/turn streams.

    For n locations:
      step[t] is the distance from t to t+1, with final step missing;
      angle[t] is turn (t-1,t,t+1), with first/final angle missing.
    """
    lon = np.asarray(list(longitude), dtype=float)
    lat = np.asarray(list(latitude), dtype=float)
    if lon.shape != lat.shape or lon.ndim != 1:
        raise ValueError("longitude and latitude must be matching 1-D arrays")
    n = len(lon)
    step = np.full(n, np.nan)
    angle = np.full(n, np.nan)

    for i in range(n - 1):
        if np.all(np.isfinite([lon[i], lat[i], lon[i + 1], lat[i + 1]])):
            step[i] = haversine_km(lon[i], lat[i], lon[i + 1], lat[i + 1])

    for i in range(1, n - 1):
        if np.all(
            np.isfinite(
                [
                    lon[i - 1], lat[i - 1],
                    lon[i], lat[i],
                    lon[i + 1], lat[i + 1],
                ]
            )
        ):
            b1 = initial_bearing_rad(lon[i - 1], lat[i - 1], lon[i], lat[i])
            b2 = initial_bearing_rad(lon[i], lat[i], lon[i + 1], lat[i + 1])
            angle[i] = wrap_angle(b2 - b1)
    return step, angle


def viterbi_published(
    step_sqrt: Iterable[float],
    angle: Iterable[float],
    solar_time: Iterable[float],
) -> np.ndarray:
    """Viterbi state sequence, returned as 1..4 published state numbers."""
    step = np.asarray(list(step_sqrt), dtype=float)
    ang = np.asarray(list(angle), dtype=float)
    sol = np.asarray(list(solar_time), dtype=float)
    if not (len(step) == len(ang) == len(sol)):
        raise ValueError("all streams must have equal length")
    n = len(step)
    if n == 0:
        return np.array([], dtype=int)

    log_emit = np.vstack(
        [
            emission_log_prob(step[i], ang[i])
            for i in range(n)
        ]
    )

    score = np.full((n, 4), -np.inf)
    back = np.zeros((n, 4), dtype=np.int8)
    score[0] = np.log(INITIAL) + log_emit[0]

    for t in range(1, n):
        trans = np.log(np.maximum(transition_matrix(sol[t - 1]), 1e-300))
        prev = score[t - 1][:, None] + trans
        back[t] = np.argmax(prev, axis=0)
        score[t] = np.max(prev, axis=0) + log_emit[t]

    states = np.zeros(n, dtype=int)
    states[-1] = int(np.argmax(score[-1]))
    for t in range(n - 1, 0, -1):
        states[t - 1] = int(back[t, states[t]])
    return states + 1
