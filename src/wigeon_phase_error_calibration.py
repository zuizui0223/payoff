"""Source-faithful wigeon phase-error calibration helpers.

This module is outcome-audit infrastructure for the PAYOFF-B GEB programme.
It compares the frozen NASA POWER phase reconstruction with an independent
ERA5-Land replicate while preserving the exact wigeon controller estimand.

No network operations live here. The Open-Meteo retrieval layer is implemented
separately so all scientific transformations are unit-testable offline.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from math import isfinite, sqrt
from statistics import mean, median, stdev
from typing import Iterable, Sequence

from src.phase_retention_recovery import (
    corrected_lambda_from_known_error,
    lower_tail_null_probability,
    recovery_design_from_observed_predictor_sd,
    simulate_lambda_recovery,
    simulate_naive_lambda_once,
)


@dataclass(frozen=True)
class ReplicateDisagreement:
    n: int
    mean: float
    median: float
    sample_sd: float
    q025: float
    q25: float
    q75: float
    q975: float

    @property
    def equal_independent_replicate_error_sd(self) -> float:
        return self.sample_sd / sqrt(2.0)


@dataclass(frozen=True)
class ControllerFit:
    n_pairs: int
    n_individuals: int
    lambda_hat: float
    lambda_cluster_se: float
    lambda_naive_p_vs_one: float
    beta_phase_change: float
    beta_cluster_p: float
    raw_origin_phase_sd: float
    residualized_origin_phase_sd: float
    predictor_covariate_r_squared: float
    process_residual_sample_sd: float
    stopover_slope: float
    stopover_cluster_se: float
    stopover_cluster_p: float
    travel_log_speed_slope: float | None
    travel_log_speed_cluster_se: float | None
    travel_log_speed_cluster_p: float | None


@dataclass(frozen=True)
class LambdaOneNullScenario:
    name: str
    status: str
    predictor_error_sd: float
    error_correlation: float
    observed_residualized_predictor_sd: float
    inferred_latent_predictor_sd: float | None
    expected_naive_lambda_under_true_one: float | None
    eiv_corrected_observed_lambda: float | None
    process_noise_sd: float
    replicates: int
    seed: int
    null_mean_lambda_hat: float | None
    null_sd_lambda_hat: float | None
    null_q025: float | None
    null_q50: float | None
    null_q975: float | None
    lower_tail_probability_at_observed_lambda: float | None
    reason: str | None = None


def _quantile(values: Sequence[float], probability: float) -> float:
    if not values:
        raise ValueError("quantile requires at least one value")
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must lie in [0,1]")
    ordered = sorted(float(v) for v in values)
    position = probability * (len(ordered) - 1)
    lo = int(position)
    hi = min(lo + 1, len(ordered) - 1)
    frac = position - lo
    return ordered[lo] * (1.0 - frac) + ordered[hi] * frac


def tgs_onset_from_daily_mean(
    dates: Iterable[str | date | datetime],
    mean_temperature_c: Iterable[float],
    *,
    threshold_c: float = 5.0,
) -> int:
    """Apply the published Jan--Jul cumulative-minimum TGS rule."""

    rows = []
    for raw_date, raw_temp in zip(dates, mean_temperature_c):
        if isinstance(raw_date, datetime):
            day = raw_date.date()
        elif isinstance(raw_date, date):
            day = raw_date
        else:
            day = date.fromisoformat(str(raw_date))
        temp = float(raw_temp)
        if not isfinite(temp):
            raise ValueError("daily temperature values must be finite")
        if day.month >= 8:
            raise ValueError(
                "TGS calibration input must be restricted to January-July"
            )
        rows.append((day, temp))

    if len(rows) < 30:
        raise ValueError("at least 30 Jan-Jul daily temperatures are required")
    if len({day for day, _ in rows}) != len(rows):
        raise ValueError("duplicate daily dates are not allowed")
    rows.sort(key=lambda row: row[0])
    years = {day.year for day, _ in rows}
    if len(years) != 1:
        raise ValueError("one TGS series must contain exactly one year")

    cumulative = 0.0
    minimum = None
    minimum_day = None
    for day, temperature in rows:
        cumulative += temperature - threshold_c
        if minimum is None or cumulative < minimum:
            minimum = cumulative
            minimum_day = day

    assert minimum_day is not None
    return minimum_day.timetuple().tm_yday


def summarize_replicate_disagreement(
    values: Iterable[float],
) -> ReplicateDisagreement:
    rows = tuple(float(v) for v in values)
    if len(rows) < 2:
        raise ValueError("at least two paired discrepancies are required")
    if any(not isfinite(v) for v in rows):
        raise ValueError("paired discrepancies must be finite")
    return ReplicateDisagreement(
        n=len(rows),
        mean=mean(rows),
        median=median(rows),
        sample_sd=stdev(rows),
        q025=_quantile(rows, 0.025),
        q25=_quantile(rows, 0.25),
        q75=_quantile(rows, 0.75),
        q975=_quantile(rows, 0.975),
    )


def _term(model, name: str) -> tuple[float, float, float]:
    names = list(model.model.exog_names)
    index = names.index(name)
    return (
        float(model.params[index]),
        float(model.bse[index]),
        float(model.pvalues[index]),
    )


def fit_source_faithful_controller(
    records,
    *,
    origin_phase_column: str,
    destination_phase_column: str,
) -> ControllerFit:
    """Fit the exact frozen wigeon partial-slope controller."""

    try:
        import numpy as np
        import pandas as pd
        import statsmodels.formula.api as smf
        from scipy.stats import norm
    except ImportError as exc:
        raise RuntimeError(
            "wigeon phase-error calibration requires empirical dependencies"
        ) from exc

    if not isinstance(records, pd.DataFrame):
        raise TypeError("records must be a pandas DataFrame")

    required = {
        "individual_id",
        "year",
        "origin_progress_km",
        "endpoint_distance_km",
        "origin_stopover_days",
        "travel_speed_km_day",
        origin_phase_column,
        destination_phase_column,
    }
    missing = required.difference(records.columns)
    if missing:
        raise ValueError(
            "controller records missing columns: "
            + ", ".join(sorted(missing))
        )

    data = records.copy()
    data["individual_id"] = data["individual_id"].astype(str)
    data["year"] = data["year"].astype(int)
    data["origin_phase"] = data[origin_phase_column].astype(float)
    data["destination_phase"] = data[destination_phase_column].astype(float)
    data["phase_change"] = data["destination_phase"] - data["origin_phase"]

    for column in ("origin_progress_km", "endpoint_distance_km"):
        values = data[column].astype(float)
        sd = float(values.std(ddof=0))
        if sd <= 0.0 or not isfinite(sd):
            raise ValueError(f"{column} has no usable variation")
        zname = (
            "z_progress"
            if column == "origin_progress_km"
            else "z_endpoint"
        )
        data[zname] = (values - float(values.mean())) / sd

    base = smf.ols(
        "phase_change ~ origin_phase + z_progress + z_endpoint "
        "+ z_progress:z_endpoint + C(year)",
        data=data,
    ).fit()
    robust = base.get_robustcov_results(
        cov_type="cluster",
        groups=data["individual_id"],
    )
    beta, beta_se, beta_p = _term(robust, "origin_phase")
    lambda_hat = 1.0 + beta
    lambda_p = float(
        2.0 * norm.sf(abs(beta / beta_se))
    )

    nuisance = smf.ols(
        "origin_phase ~ z_progress + z_endpoint "
        "+ z_progress:z_endpoint + C(year)",
        data=data,
    ).fit()
    predictor_residual = np.asarray(nuisance.resid, dtype=float)

    stop = smf.ols(
        "origin_stopover_days ~ origin_phase + z_progress + z_endpoint "
        "+ C(year)",
        data=data,
    ).fit().get_robustcov_results(
        cov_type="cluster",
        groups=data["individual_id"],
    )
    stop_beta, stop_se, stop_p = _term(stop, "origin_phase")

    speed = data[
        np.isfinite(data["travel_speed_km_day"].astype(float))
        & (data["travel_speed_km_day"].astype(float) > 0.0)
    ].copy()
    if len(speed) >= 20 and speed["individual_id"].nunique() >= 8:
        speed["log_travel_speed"] = np.log(
            speed["travel_speed_km_day"].astype(float)
        )
        speed_fit = smf.ols(
            "log_travel_speed ~ origin_phase + z_progress + z_endpoint "
            "+ C(year)",
            data=speed,
        ).fit().get_robustcov_results(
            cov_type="cluster",
            groups=speed["individual_id"],
        )
        speed_beta, speed_se, speed_p = _term(
            speed_fit, "origin_phase"
        )
    else:
        speed_beta = speed_se = speed_p = None

    return ControllerFit(
        n_pairs=int(len(data)),
        n_individuals=int(data["individual_id"].nunique()),
        lambda_hat=float(lambda_hat),
        lambda_cluster_se=float(beta_se),
        lambda_naive_p_vs_one=lambda_p,
        beta_phase_change=float(beta),
        beta_cluster_p=float(beta_p),
        raw_origin_phase_sd=float(data["origin_phase"].std(ddof=1)),
        residualized_origin_phase_sd=float(
            np.std(predictor_residual, ddof=1)
        ),
        predictor_covariate_r_squared=float(nuisance.rsquared),
        process_residual_sample_sd=float(
            np.std(base.resid, ddof=1)
        ),
        stopover_slope=float(stop_beta),
        stopover_cluster_se=float(stop_se),
        stopover_cluster_p=float(stop_p),
        travel_log_speed_slope=(
            None if speed_beta is None else float(speed_beta)
        ),
        travel_log_speed_cluster_se=(
            None if speed_se is None else float(speed_se)
        ),
        travel_log_speed_cluster_p=(
            None if speed_p is None else float(speed_p)
        ),
    )


def simulate_true_lambda_one_null(
    *,
    name: str,
    observed_lambda_hat: float,
    observed_residualized_predictor_sd: float,
    predictor_error_sd: float,
    error_correlation: float,
    process_noise_sd: float,
    n_pairs: int,
    replicates: int,
    seed: int,
) -> LambdaOneNullScenario:
    """Run the frozen FWL residual-scale true-lambda=1 sensitivity null."""

    try:
        design = recovery_design_from_observed_predictor_sd(
            true_lambda=1.0,
            observed_predictor_sd=observed_residualized_predictor_sd,
            predictor_error_sd=predictor_error_sd,
            outcome_error_sd=predictor_error_sd,
            error_correlation=error_correlation,
            process_noise_sd=process_noise_sd,
            n_pairs=n_pairs,
        )
    except ValueError as exc:
        return LambdaOneNullScenario(
            name=name,
            status="NOT_IDENTIFIABLE",
            predictor_error_sd=predictor_error_sd,
            error_correlation=error_correlation,
            observed_residualized_predictor_sd=(
                observed_residualized_predictor_sd
            ),
            inferred_latent_predictor_sd=None,
            expected_naive_lambda_under_true_one=None,
            eiv_corrected_observed_lambda=None,
            process_noise_sd=process_noise_sd,
            replicates=replicates,
            seed=seed,
            null_mean_lambda_hat=None,
            null_sd_lambda_hat=None,
            null_q025=None,
            null_q50=None,
            null_q975=None,
            lower_tail_probability_at_observed_lambda=None,
            reason=str(exc),
        )

    summary = simulate_lambda_recovery(
        design,
        replicates=replicates,
        seed=seed,
    )
    draws = tuple(
        simulate_naive_lambda_once(
            design,
            seed=seed + index * 1_000_003,
        )
        for index in range(replicates)
    )
    p_lower = lower_tail_null_probability(
        observed_lambda_hat,
        draws,
    )
    error_covariance = (
        error_correlation
        * predictor_error_sd
        * predictor_error_sd
    )
    corrected = corrected_lambda_from_known_error(
        naive_lambda=observed_lambda_hat,
        observed_predictor_variance=(
            observed_residualized_predictor_sd**2
        ),
        predictor_error_variance=(
            predictor_error_sd**2
        ),
        predictor_outcome_error_covariance=error_covariance,
    )

    return LambdaOneNullScenario(
        name=name,
        status="COMPLETE",
        predictor_error_sd=predictor_error_sd,
        error_correlation=error_correlation,
        observed_residualized_predictor_sd=(
            observed_residualized_predictor_sd
        ),
        inferred_latent_predictor_sd=design.latent_phase_sd,
        expected_naive_lambda_under_true_one=(
            summary.expected_naive_lambda
        ),
        eiv_corrected_observed_lambda=corrected,
        process_noise_sd=process_noise_sd,
        replicates=replicates,
        seed=seed,
        null_mean_lambda_hat=summary.mean_naive_lambda,
        null_sd_lambda_hat=summary.sd_naive_lambda,
        null_q025=summary.q025,
        null_q50=summary.q50,
        null_q975=summary.q975,
        lower_tail_probability_at_observed_lambda=p_lower,
    )
