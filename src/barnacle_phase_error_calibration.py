"""Barnacle-goose phase reconstruction reliability helpers.

This module reproduces the registered latitude-dependent GDD + logistic-jerk
phenology transform and fixed-transition phase-retention slope used by the
PAYOFF-B movement-phenology programme. It is intentionally source-agnostic:
POWER and ERA5 daily mean temperature can be passed through the same functions.

Network access is kept outside this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, log, sqrt
from statistics import mean, stdev
from typing import Iterable, Sequence


EARLY_JERK_FRACTION = 0.5 - sqrt(6.0) / 6.0
EARLY_JERK_LOGIT = log(
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


@dataclass(frozen=True)
class TransitionControllerFit:
    n: int
    n_individuals: int
    lambda_hat: float
    lambda_cluster_se: float
    p_vs_one: float
    stopover_slope: float
    stopover_cluster_se: float
    stopover_cluster_p: float
    origin_phase_sd: float


@dataclass(frozen=True)
class ReplicateDifferenceSummary:
    n: int
    mean: float
    median: float
    sample_sd: float
    equal_independent_replicate_error_sd: float


def latitude_base_temperature(latitude_deg: float) -> float:
    lat = float(latitude_deg)
    if not isfinite(lat) or not -90.0 <= lat <= 90.0:
        raise ValueError("latitude must be finite and within [-90,90]")
    return -0.25 * lat + 13.0


def fit_gdd_jerk(
    mean_daily_temperature_c: Iterable[float],
    latitude_deg: float,
    *,
    min_r_squared: float = 0.95,
) -> GDDJerkFit:
    """Fit annual cumulative GDD and return the early positive jerk peak."""

    try:
        import numpy as np
        from scipy.optimize import curve_fit
    except ImportError as exc:
        raise RuntimeError(
            "barnacle GDD calibration requires numpy and scipy"
        ) from exc

    temp = np.asarray(list(mean_daily_temperature_c), dtype=float)
    if temp.ndim != 1 or temp.size < 360:
        raise ValueError("annual temperature series requires >=360 daily values")
    if not np.all(np.isfinite(temp)):
        raise ValueError("daily temperatures must be finite")

    t_base = latitude_base_temperature(latitude_deg)
    gdu = np.maximum(temp - t_base, 0.0)
    gdd = np.cumsum(gdu)
    max_gdd = float(gdd[-1])
    if not isfinite(max_gdd) or max_gdd <= 1.0:
        raise ValueError("annual GDD accumulation too small")

    days = np.arange(1, len(gdd) + 1, dtype=float)

    def logistic(day, asymptote, rate, midpoint):
        z = np.clip(-rate * (day - midpoint), -700.0, 700.0)
        return asymptote / (1.0 + np.exp(z))

    target = max_gdd / 2.0
    midpoint_guess = float(days[np.argmin(np.abs(gdd - target))])
    popt, _ = curve_fit(
        logistic,
        days,
        gdd,
        p0=(max_gdd, 0.03, midpoint_guess),
        bounds=(
            (0.5 * max_gdd, 0.001, 1.0),
            (2.0 * max_gdd, 1.0, float(len(gdd))),
        ),
        maxfev=50000,
    )
    asymptote, rate, midpoint = [float(v) for v in popt]
    prediction = logistic(days, *popt)
    residual_ss = float(np.sum((gdd - prediction) ** 2))
    total_ss = float(np.sum((gdd - np.mean(gdd)) ** 2))
    r_squared = (
        1.0 - residual_ss / total_ss
        if total_ss > 0.0
        else float("nan")
    )
    onset = midpoint + EARLY_JERK_LOGIT / rate

    if not isfinite(r_squared) or r_squared < min_r_squared:
        raise ValueError(
            f"GDD logistic fit below r2 gate: {r_squared:.6f}"
        )
    if not 1.0 <= onset <= len(gdd):
        raise ValueError(
            f"GDD jerk onset outside annual support: {onset:.3f}"
        )

    return GDDJerkFit(
        asymptote=asymptote,
        rate=rate,
        midpoint_day=midpoint,
        onset_day=float(onset),
        r_squared=r_squared,
        t_base=t_base,
    )


def fit_fixed_transition_controller(
    records,
    *,
    origin_phase_column: str,
    destination_phase_column: str,
) -> TransitionControllerFit:
    """Fit destination phase ~ origin phase with animal-clustered uncertainty."""

    try:
        import numpy as np
        import pandas as pd
        import statsmodels.formula.api as smf
        from scipy.stats import norm
    except ImportError as exc:
        raise RuntimeError(
            "barnacle controller fitting requires empirical dependencies"
        ) from exc

    if not isinstance(records, pd.DataFrame):
        raise TypeError("records must be a pandas DataFrame")

    required = {
        "individual_id",
        "origin_stopover_days",
        origin_phase_column,
        destination_phase_column,
    }
    missing = required.difference(records.columns)
    if missing:
        raise ValueError(
            "transition records missing columns: "
            + ", ".join(sorted(missing))
        )
    data = records.dropna(
        subset=[
            origin_phase_column,
            destination_phase_column,
            "origin_stopover_days",
        ]
    ).copy()
    if len(data) < 4:
        raise ValueError("at least four transition rows are required")
    if data["individual_id"].nunique() < 2:
        raise ValueError("at least two individuals are required")

    data["origin_phase"] = data[origin_phase_column].astype(float)
    data["destination_phase"] = data[destination_phase_column].astype(float)
    data["individual_id"] = data["individual_id"].astype(str)

    phase = smf.ols(
        "destination_phase ~ origin_phase",
        data=data,
    ).fit().get_robustcov_results(
        cov_type="cluster",
        groups=data["individual_id"],
    )
    names = list(phase.model.exog_names)
    i = names.index("origin_phase")
    lam = float(phase.params[i])
    lam_se = float(phase.bse[i])
    p_vs_one = float(
        2.0 * norm.sf(abs((lam - 1.0) / lam_se))
    )

    stop = smf.ols(
        "origin_stopover_days ~ origin_phase",
        data=data,
    ).fit().get_robustcov_results(
        cov_type="cluster",
        groups=data["individual_id"],
    )
    j = list(stop.model.exog_names).index("origin_phase")

    return TransitionControllerFit(
        n=int(len(data)),
        n_individuals=int(data["individual_id"].nunique()),
        lambda_hat=lam,
        lambda_cluster_se=lam_se,
        p_vs_one=p_vs_one,
        stopover_slope=float(stop.params[j]),
        stopover_cluster_se=float(stop.bse[j]),
        stopover_cluster_p=float(stop.pvalues[j]),
        origin_phase_sd=float(
            np.std(data["origin_phase"].to_numpy(dtype=float), ddof=1)
        ),
    )


def summarize_replicate_differences(
    values: Iterable[float],
) -> ReplicateDifferenceSummary:
    rows = tuple(float(v) for v in values)
    if len(rows) < 2:
        raise ValueError("at least two replicate differences are required")
    if any(not isfinite(v) for v in rows):
        raise ValueError("replicate differences must be finite")
    ordered = sorted(rows)
    n = len(ordered)
    midpoint = n // 2
    median_value = (
        ordered[midpoint]
        if n % 2
        else 0.5 * (ordered[midpoint - 1] + ordered[midpoint])
    )
    sample_sd = stdev(rows)
    return ReplicateDifferenceSummary(
        n=n,
        mean=mean(rows),
        median=median_value,
        sample_sd=sample_sd,
        equal_independent_replicate_error_sd=sample_sd / sqrt(2.0),
    )
