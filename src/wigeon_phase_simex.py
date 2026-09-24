"""Cluster/event-structure preserving SIMEX sensitivity for wigeon lambda.

The source-faithful wigeon controller uses consecutive staging transitions.
A staging event can be the destination of one transition and the origin of the
next, so observation error must be attached to event identity rather than drawn
independently for each transition endpoint.

This module adds Gaussian event-level phase error along each individual-year
staging sequence and recomputes the exact OLS point estimate of the frozen
controller. Cluster-robust uncertainty is not needed for the SIMEX mean curve;
the empirical point estimate is unchanged by the covariance estimator.

The module is a sensitivity tool. It does not estimate empirical error moments.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt
from random import Random
from statistics import mean, pstdev
from typing import Iterable


@dataclass(frozen=True)
class SimexCurvePoint:
    zeta: float
    replicates: int
    mean_lambda_hat: float
    sd_lambda_hat: float
    q025: float
    q50: float
    q975: float


@dataclass(frozen=True)
class WigeonSimexResult:
    scenario_name: str
    error_sd_days: float
    error_correlation: float
    observed_lambda_hat: float
    zeta_points: tuple[SimexCurvePoint, ...]
    quadratic_coefficients: tuple[float, float, float]
    simex_extrapolated_lambda_at_minus_one: float
    seed: int
    replicates_per_zeta: int


def _quantile(values: Iterable[float], p: float) -> float:
    rows = sorted(float(v) for v in values)
    if not rows:
        raise ValueError("quantile requires values")
    if not 0.0 <= p <= 1.0:
        raise ValueError("p must lie in [0,1]")
    if len(rows) == 1:
        return rows[0]
    position = p * (len(rows) - 1)
    lo = int(position)
    hi = min(lo + 1, len(rows) - 1)
    frac = position - lo
    return rows[lo] * (1.0 - frac) + rows[hi] * frac


def _require_columns(frame, required: set[str]) -> None:
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(
            "transition table missing columns: "
            + ", ".join(sorted(missing))
        )


def prepare_wigeon_design(frame):
    """Prepare fixed nuisance columns for the frozen controller point estimate."""

    try:
        import numpy as np
        import pandas as pd
    except ImportError as exc:
        raise RuntimeError(
            "wigeon SIMEX requires numpy and pandas"
        ) from exc

    if not isinstance(frame, pd.DataFrame):
        raise TypeError("frame must be a pandas DataFrame")
    required = {
        "individual_id",
        "year",
        "origin_segment",
        "destination_segment",
        "origin_phase",
        "destination_phase",
        "origin_progress_km",
        "endpoint_distance_km",
    }
    _require_columns(frame, required)
    data = frame.copy().reset_index(drop=True)
    data["individual_id"] = data["individual_id"].astype(str)
    data["year"] = data["year"].astype(int)
    for column in (
        "origin_phase",
        "destination_phase",
        "origin_progress_km",
        "endpoint_distance_km",
    ):
        data[column] = data[column].astype(float)
        if not np.isfinite(data[column]).all():
            raise ValueError(f"{column} must be finite")

    progress = data["origin_progress_km"].to_numpy(dtype=float)
    endpoint = data["endpoint_distance_km"].to_numpy(dtype=float)
    progress_sd = float(np.std(progress, ddof=0))
    endpoint_sd = float(np.std(endpoint, ddof=0))
    if progress_sd <= 0.0 or endpoint_sd <= 0.0:
        raise ValueError("controller covariates require variation")
    z_progress = (progress - float(np.mean(progress))) / progress_sd
    z_endpoint = (endpoint - float(np.mean(endpoint))) / endpoint_sd

    years = sorted(int(v) for v in data["year"].unique())
    year_dummies = []
    for year in years[1:]:
        year_dummies.append(
            (data["year"].to_numpy(dtype=int) == year).astype(float)
        )

    nuisance = [
        np.ones(len(data), dtype=float),
        z_progress,
        z_endpoint,
        z_progress * z_endpoint,
        *year_dummies,
    ]
    return data, tuple(nuisance)


def lambda_hat_from_phases(
    data,
    nuisance_columns,
    *,
    origin_phase,
    destination_phase,
) -> float:
    """Return lambda=1+beta_origin from the frozen wigeon OLS design."""

    import numpy as np

    origin = np.asarray(origin_phase, dtype=float)
    destination = np.asarray(destination_phase, dtype=float)
    if origin.shape != destination.shape or len(origin) != len(data):
        raise ValueError("phase arrays do not match transition table")
    phase_change = destination - origin

    # Frozen formula:
    # phase_change ~ origin_phase + z_progress + z_endpoint
    #                + z_progress:z_endpoint + C(year)
    columns = [
        nuisance_columns[0],
        origin,
        *nuisance_columns[1:],
    ]
    X = np.column_stack(columns)
    rank = int(np.linalg.matrix_rank(X))
    if rank < X.shape[1]:
        raise ValueError(
            "wigeon SIMEX controller design matrix is rank deficient"
        )
    beta, *_ = np.linalg.lstsq(
        X,
        phase_change,
        rcond=None,
    )
    return 1.0 + float(beta[1])


def _event_sequences(data):
    groups: dict[tuple[str, int], set[int]] = {}
    for row in data.itertuples(index=False):
        key = (str(row.individual_id), int(row.year))
        segments = groups.setdefault(key, set())
        segments.add(int(row.origin_segment))
        segments.add(int(row.destination_segment))
    return {
        key: tuple(sorted(segments))
        for key, segments in groups.items()
    }


def draw_event_errors(
    data,
    *,
    error_sd: float,
    error_correlation: float,
    seed: int,
) -> dict[tuple[str, int, int], float]:
    """Draw one stationary AR1 error path per individual-year."""

    if not isfinite(error_sd) or error_sd < 0.0:
        raise ValueError("error_sd must be non-negative and finite")
    if (
        not isfinite(error_correlation)
        or not -1.0 <= error_correlation <= 1.0
    ):
        raise ValueError(
            "error_correlation must lie in [-1,1]"
        )
    rng = Random(seed)
    innovation_scale = (
        error_sd
        * sqrt(max(0.0, 1.0 - error_correlation**2))
    )
    errors: dict[tuple[str, int, int], float] = {}
    for (individual_id, year), segments in sorted(
        _event_sequences(data).items()
    ):
        previous = None
        for segment in segments:
            if previous is None:
                value = rng.gauss(0.0, error_sd)
            else:
                value = (
                    error_correlation * previous
                    + rng.gauss(0.0, innovation_scale)
                )
            errors[
                (individual_id, year, int(segment))
            ] = value
            previous = value
    return errors


def perturbed_lambda_hat(
    data,
    nuisance_columns,
    *,
    added_error_sd: float,
    error_correlation: float,
    seed: int,
) -> float:
    import numpy as np

    errors = draw_event_errors(
        data,
        error_sd=added_error_sd,
        error_correlation=error_correlation,
        seed=seed,
    )
    origin = []
    destination = []
    for row in data.itertuples(index=False):
        key_origin = (
            str(row.individual_id),
            int(row.year),
            int(row.origin_segment),
        )
        key_destination = (
            str(row.individual_id),
            int(row.year),
            int(row.destination_segment),
        )
        origin.append(
            float(row.origin_phase) + errors[key_origin]
        )
        destination.append(
            float(row.destination_phase)
            + errors[key_destination]
        )
    return lambda_hat_from_phases(
        data,
        nuisance_columns,
        origin_phase=np.asarray(origin, dtype=float),
        destination_phase=np.asarray(destination, dtype=float),
    )


def run_wigeon_simex(
    frame,
    *,
    scenario_name: str,
    error_sd_days: float,
    error_correlation: float,
    zeta_values: tuple[float, ...] = (0.5, 1.0, 1.5, 2.0),
    replicates_per_zeta: int = 1000,
    seed: int = 20260923,
) -> WigeonSimexResult:
    """Run fixed-design event-level SIMEX and quadratic extrapolation."""

    if not scenario_name.strip():
        raise ValueError("scenario_name must be non-empty")
    if replicates_per_zeta <= 0:
        raise ValueError("replicates_per_zeta must be positive")
    if not zeta_values or any(
        (not isfinite(v) or v <= 0.0)
        for v in zeta_values
    ):
        raise ValueError("zeta_values must be finite and positive")

    import numpy as np

    data, nuisance = prepare_wigeon_design(frame)
    observed = lambda_hat_from_phases(
        data,
        nuisance,
        origin_phase=data["origin_phase"].to_numpy(dtype=float),
        destination_phase=data["destination_phase"].to_numpy(dtype=float),
    )

    points = []
    mean_by_zeta = []
    for zeta_index, zeta in enumerate(zeta_values):
        added_sd = sqrt(float(zeta)) * error_sd_days
        estimates = tuple(
            perturbed_lambda_hat(
                data,
                nuisance,
                added_error_sd=added_sd,
                error_correlation=error_correlation,
                seed=(
                    seed
                    + zeta_index * 100_000_007
                    + replicate * 1_000_003
                ),
            )
            for replicate in range(replicates_per_zeta)
        )
        avg = mean(estimates)
        mean_by_zeta.append(avg)
        points.append(
            SimexCurvePoint(
                zeta=float(zeta),
                replicates=replicates_per_zeta,
                mean_lambda_hat=avg,
                sd_lambda_hat=(
                    pstdev(estimates)
                    if len(estimates) > 1
                    else 0.0
                ),
                q025=_quantile(estimates, 0.025),
                q50=_quantile(estimates, 0.5),
                q975=_quantile(estimates, 0.975),
            )
        )

    x = np.asarray((0.0, *zeta_values), dtype=float)
    y = np.asarray((observed, *mean_by_zeta), dtype=float)
    coefficients = np.polyfit(x, y, deg=2)
    extrapolated = float(
        np.polyval(coefficients, -1.0)
    )

    return WigeonSimexResult(
        scenario_name=scenario_name,
        error_sd_days=float(error_sd_days),
        error_correlation=float(error_correlation),
        observed_lambda_hat=float(observed),
        zeta_points=tuple(points),
        quadratic_coefficients=tuple(
            float(value) for value in coefficients
        ),
        simex_extrapolated_lambda_at_minus_one=extrapolated,
        seed=seed,
        replicates_per_zeta=replicates_per_zeta,
    )
