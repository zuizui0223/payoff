"""Barnacle-goose environmental-replicate reliability helpers.

This module reproduces the frozen latitude-dependent GDD + logistic-jerk
phenology transform used in the PAYOFF-B POWER reconstruction and fits the
fixed-route phase-transfer slope

    phase_destination = a + lambda * phase_origin + error

with individual-clustered uncertainty.

No network access lives here.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable


EARLY_JERK_FRACTION = 0.5 - math.sqrt(6.0) / 6.0
EARLY_JERK_LOGIT = math.log(
    EARLY_JERK_FRACTION / (1.0 - EARLY_JERK_FRACTION)
)


@dataclass(frozen=True)
class GDDJerkFit:
    onset_day: float
    r_squared: float
    t_base_c: float


@dataclass(frozen=True)
class FixedRouteLambdaFit:
    n_pairs: int
    n_individuals: int
    lambda_hat: float
    cluster_se: float
    p_vs_one: float


def latitude_base_temperature(latitude_deg: float) -> float:
    lat = float(latitude_deg)
    if not math.isfinite(lat) or not -90.0 <= lat <= 90.0:
        raise ValueError("latitude must be finite and within [-90,90]")
    return -0.25 * lat + 13.0


def fit_gdd_jerk(
    mean_daily_temperature_c: Iterable[float],
    latitude_deg: float,
    *,
    min_r_squared: float = 0.95,
) -> GDDJerkFit:
    try:
        import numpy as np
        from scipy.optimize import curve_fit
    except ImportError as exc:
        raise RuntimeError(
            "barnacle-goose ERA5 calibration requires numpy/scipy"
        ) from exc

    temp = np.asarray(tuple(float(v) for v in mean_daily_temperature_c))
    if temp.ndim != 1 or temp.size < 360:
        raise ValueError("annual daily temperature series is incomplete")
    if not np.all(np.isfinite(temp)):
        raise ValueError("daily temperature series must be finite")

    t_base = latitude_base_temperature(latitude_deg)
    gdd = np.cumsum(np.maximum(temp - t_base, 0.0))
    max_gdd = float(gdd[-1])
    if not math.isfinite(max_gdd) or max_gdd <= 1.0:
        raise ValueError("annual GDD accumulation is too small")

    days = np.arange(1, len(gdd) + 1, dtype=float)

    def logistic(day, asymptote, rate, midpoint_day):
        z = np.clip(
            -rate * (day - midpoint_day),
            -700,
            700,
        )
        return asymptote / (1.0 + np.exp(z))

    target = max_gdd / 2.0
    midpoint_guess = float(
        days[np.argmin(np.abs(gdd - target))]
    )
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
    asymptote, rate, midpoint = [float(x) for x in popt]
    pred = logistic(days, *popt)
    residual_ss = float(np.sum((gdd - pred) ** 2))
    total_ss = float(np.sum((gdd - np.mean(gdd)) ** 2))
    r_squared = (
        1.0 - residual_ss / total_ss
        if total_ss > 0
        else float("nan")
    )
    onset = midpoint + EARLY_JERK_LOGIT / rate

    if not math.isfinite(r_squared) or r_squared < min_r_squared:
        raise ValueError(
            f"GDD logistic fit below r2 gate: {r_squared:.4f}"
        )
    if onset < 1.0 or onset > len(gdd):
        raise ValueError(
            f"spring jerk onset outside annual support: {onset:.2f}"
        )

    del asymptote
    return GDDJerkFit(
        onset_day=float(onset),
        r_squared=float(r_squared),
        t_base_c=float(t_base),
    )


def fit_fixed_route_lambda(
    records,
    *,
    origin_phase_column: str,
    destination_phase_column: str,
) -> FixedRouteLambdaFit:
    try:
        import pandas as pd
        import statsmodels.formula.api as smf
        from scipy.stats import norm
    except ImportError as exc:
        raise RuntimeError(
            "barnacle-goose route fitting requires empirical dependencies"
        ) from exc

    if not isinstance(records, pd.DataFrame):
        raise TypeError("records must be a pandas DataFrame")
    required = {
        "individual_id",
        origin_phase_column,
        destination_phase_column,
    }
    missing = required.difference(records.columns)
    if missing:
        raise ValueError(
            "route records missing columns: "
            + ", ".join(sorted(missing))
        )
    if len(records) < 3:
        raise ValueError("at least three route transitions are required")

    data = records.copy()
    data["individual_id"] = data["individual_id"].astype(str)
    data["origin_phase"] = data[origin_phase_column].astype(float)
    data["destination_phase"] = data[destination_phase_column].astype(float)

    base = smf.ols(
        "destination_phase ~ origin_phase",
        data=data,
    ).fit()
    robust = base.get_robustcov_results(
        cov_type="cluster",
        groups=data["individual_id"],
    )
    names = list(robust.model.exog_names)
    index = names.index("origin_phase")
    lam = float(robust.params[index])
    se = float(robust.bse[index])
    p_vs_one = float(
        2.0 * norm.sf(abs((lam - 1.0) / se))
    )
    return FixedRouteLambdaFit(
        n_pairs=int(len(data)),
        n_individuals=int(data["individual_id"].nunique()),
        lambda_hat=lam,
        cluster_se=se,
        p_vs_one=p_vs_one,
    )
