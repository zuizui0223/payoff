"""Offline reconstruction of annual peak instantaneous rate of green-up.

The module accepts already extracted pixel-year NDVI observations. Downloading
or sampling MODIS is a separate provenance layer.

Registered processing follows the Aikens/Merkle/Bischof workflow family:
quality-screened NDVI, snow-informed winter flooring, the 2.5-percent snow-free
baseline, a three-observation moving median, an upper 92.5-percent scaling
reference, an annual double logistic, and peak IRG as the day with maximum
positive first derivative.

SciPy is imported only inside the nonlinear fitting function. Core PAYOFF
therefore remains dependency-free.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log, sqrt
from statistics import median
from typing import Iterable


@dataclass(frozen=True)
class NDVIObservation:
    doy: int
    ndvi: float
    snow_free: bool | None
    quality_good: bool = True

    def __post_init__(self) -> None:
        if not 1 <= self.doy <= 366:
            raise ValueError("doy must lie in [1,366]")
        if not isfinite(self.ndvi):
            raise ValueError("ndvi must be finite")
        if not -1.0 <= self.ndvi <= 1.0:
            raise ValueError("ndvi must lie in [-1,1]")


@dataclass(frozen=True)
class ProcessedNDVI:
    doy: tuple[int, ...]
    scaled_ndvi: tuple[float, ...]
    winter_baseline: float
    upper_scale_reference: float
    snow_release_doy: int
    valid_observations: int


@dataclass(frozen=True)
class DoubleLogisticParameters:
    alpha: float
    beta: float
    gamma: float
    delta: float
    epsilon: float
    theta: float

    @property
    def spring_scale_days(self) -> float:
        if self.gamma <= 0.0:
            raise ValueError("gamma must be positive")
        return log(3.0) / self.gamma


@dataclass(frozen=True)
class PeakIRGFit:
    parameters: DoubleLogisticParameters
    peak_irg_doy: int
    peak_irg_value: float
    spring_scale_days: float
    fit_rmse: float
    processed: ProcessedNDVI
    optimizer_success: bool
    optimizer_message: str


def _quantile(values: list[float], probability: float) -> float:
    if not values:
        raise ValueError("cannot take a quantile of an empty sequence")
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must lie in [0,1]")
    x = sorted(values)
    if len(x) == 1:
        return x[0]
    position = probability * (len(x) - 1)
    lower = int(position)
    upper = min(lower + 1, len(x) - 1)
    fraction = position - lower
    return x[lower] * (1.0 - fraction) + x[upper] * fraction


def _moving_median_three(values: list[float]) -> list[float]:
    result: list[float] = []
    for index in range(len(values)):
        lower = max(0, index - 1)
        upper = min(len(values), index + 2)
        result.append(float(median(values[lower:upper])))
    return result


def preprocess_ndvi(
    observations: Iterable[NDVIObservation],
    *,
    baseline_quantile: float = 0.025,
    upper_quantile: float = 0.925,
    snow_search_start_doy: int = 60,
    require_snow_flags: bool = True,
) -> ProcessedNDVI:
    """Apply frozen annual preprocessing before the nonlinear fit."""

    rows = sorted(
        (row for row in observations if row.quality_good),
        key=lambda row: row.doy,
    )
    if len(rows) < 8:
        raise ValueError(
            "at least eight valid NDVI composites are required"
        )
    if len({row.doy for row in rows}) != len(rows):
        raise ValueError("duplicate day-of-year observations are not allowed")

    if require_snow_flags and any(
        row.snow_free is None for row in rows
    ):
        raise ValueError(
            "study-faithful preprocessing requires snow_free flags"
        )

    snow_free_values = [
        row.ndvi for row in rows if row.snow_free is True
    ]
    if not snow_free_values:
        if require_snow_flags:
            raise ValueError("no snow-free observations are available")
        snow_free_values = [row.ndvi for row in rows]

    baseline = _quantile(
        snow_free_values,
        baseline_quantile,
    )

    release_index: int | None = None
    for index in range(len(rows) - 1):
        first = rows[index]
        second = rows[index + 1]
        if first.doy < snow_search_start_doy:
            continue
        if first.snow_free is True and second.snow_free is True:
            release_index = index
            break

    if release_index is None:
        if require_snow_flags:
            raise ValueError(
                "no two-consecutive-composite snow-free release found"
            )
        release_index = 0

    floored: list[float] = []
    for index, row in enumerate(rows):
        value = max(row.ndvi, baseline)
        if index < release_index:
            value = baseline
        floored.append(value)

    smoothed = _moving_median_three(floored)
    upper_reference = _quantile(
        smoothed,
        upper_quantile,
    )
    if upper_reference <= baseline:
        raise ValueError(
            "NDVI scaling interval is non-positive"
        )

    scaled = [
        min(
            1.0,
            max(
                0.0,
                (value - baseline)
                / (upper_reference - baseline),
            ),
        )
        for value in smoothed
    ]

    return ProcessedNDVI(
        doy=tuple(row.doy for row in rows),
        scaled_ndvi=tuple(scaled),
        winter_baseline=baseline,
        upper_scale_reference=upper_reference,
        snow_release_doy=rows[release_index].doy,
        valid_observations=len(rows),
    )


def _logistic_increasing(
    t: float,
    rate: float,
    midpoint: float,
) -> float:
    z = rate * (t - midpoint)
    if z >= 0.0:
        q = exp(-z)
        return 1.0 / (1.0 + q)
    q = exp(z)
    return q / (1.0 + q)


def _logistic_decreasing(
    t: float,
    rate: float,
    midpoint: float,
) -> float:
    return 1.0 - _logistic_increasing(
        t,
        rate,
        midpoint,
    )


def double_logistic_ndvi(
    t: float,
    params: DoubleLogisticParameters,
) -> float:
    spring = _logistic_increasing(
        t,
        params.gamma,
        params.delta,
    )
    autumn = _logistic_decreasing(
        t,
        params.epsilon,
        params.theta,
    )
    return params.alpha + (
        params.beta - params.alpha
    ) * (spring + autumn - 1.0)


def double_logistic_derivative(
    t: float,
    params: DoubleLogisticParameters,
) -> float:
    spring = _logistic_increasing(
        t,
        params.gamma,
        params.delta,
    )
    autumn = _logistic_decreasing(
        t,
        params.epsilon,
        params.theta,
    )
    spring_derivative = (
        params.gamma * spring * (1.0 - spring)
    )
    autumn_derivative = (
        -params.epsilon * autumn * (1.0 - autumn)
    )
    return (
        params.beta - params.alpha
    ) * (spring_derivative + autumn_derivative)


def peak_irg_day_from_parameters(
    params: DoubleLogisticParameters,
    *,
    first_doy: int = 1,
    last_doy: int = 366,
) -> tuple[int, float]:
    if params.beta <= params.alpha:
        raise ValueError("beta must exceed alpha")
    if params.gamma <= 0.0 or params.epsilon <= 0.0:
        raise ValueError("logistic rates must be positive")
    if params.theta <= params.delta:
        raise ValueError(
            "autumn midpoint must follow spring midpoint"
        )

    values = [
        (
            doy,
            double_logistic_derivative(
                float(doy),
                params,
            ),
        )
        for doy in range(first_doy, last_doy + 1)
    ]
    return max(values, key=lambda item: item[1])


def _midpoint_guess(
    doy: tuple[int, ...],
    values: tuple[float, ...],
    *,
    descending: bool,
) -> float:
    peak_index = max(
        range(len(values)),
        key=lambda index: values[index],
    )
    indices = (
        range(peak_index, len(values))
        if descending
        else range(0, peak_index + 1)
    )
    return float(
        doy[
            min(
                indices,
                key=lambda index: abs(
                    values[index] - 0.5
                ),
            )
        ]
    )


def fit_peak_irg(
    processed: ProcessedNDVI,
) -> PeakIRGFit:
    """Fit the annual double logistic with the optional SciPy dependency."""

    try:
        import numpy as np
        from scipy.optimize import least_squares
    except ImportError as exc:
        raise RuntimeError(
            "IRG fitting requires the optional project dependency group irg"
        ) from exc

    x = np.asarray(processed.doy, dtype=float)
    y = np.asarray(
        processed.scaled_ndvi,
        dtype=float,
    )

    spring_midpoint = _midpoint_guess(
        processed.doy,
        processed.scaled_ndvi,
        descending=False,
    )
    autumn_midpoint = _midpoint_guess(
        processed.doy,
        processed.scaled_ndvi,
        descending=True,
    )
    if autumn_midpoint <= spring_midpoint + 20.0:
        autumn_midpoint = min(
            330.0,
            spring_midpoint + 140.0,
        )

    initial = np.array(
        [
            0.0,
            1.0,
            0.05,
            spring_midpoint,
            0.03,
            autumn_midpoint,
        ],
        dtype=float,
    )
    lower = np.array(
        [-0.20, 0.20, 0.001, 1.0, 0.001, 100.0],
        dtype=float,
    )
    upper = np.array(
        [0.40, 1.40, 1.0, 260.0, 1.0, 366.0],
        dtype=float,
    )
    initial = np.minimum(
        np.maximum(initial, lower),
        upper,
    )

    def residuals(vector):
        (
            alpha,
            amplitude,
            gamma,
            delta,
            epsilon,
            theta,
        ) = vector
        params = DoubleLogisticParameters(
            alpha=float(alpha),
            beta=float(alpha + amplitude),
            gamma=float(gamma),
            delta=float(delta),
            epsilon=float(epsilon),
            theta=float(theta),
        )
        prediction = np.asarray(
            [
                double_logistic_ndvi(
                    float(day),
                    params,
                )
                for day in x
            ],
            dtype=float,
        )
        ordering_penalty = max(
            0.0,
            delta + 20.0 - theta,
        )
        return np.concatenate(
            [
                prediction - y,
                np.asarray([ordering_penalty]),
            ]
        )

    fit = least_squares(
        residuals,
        initial,
        bounds=(lower, upper),
        max_nfev=5000,
    )

    (
        alpha,
        amplitude,
        gamma,
        delta,
        epsilon,
        theta,
    ) = fit.x
    params = DoubleLogisticParameters(
        alpha=float(alpha),
        beta=float(alpha + amplitude),
        gamma=float(gamma),
        delta=float(delta),
        epsilon=float(epsilon),
        theta=float(theta),
    )
    if params.theta <= params.delta + 5.0:
        raise ValueError(
            "fitted autumn midpoint does not follow spring midpoint"
        )

    prediction = [
        double_logistic_ndvi(
            float(day),
            params,
        )
        for day in processed.doy
    ]
    rmse = sqrt(
        sum(
            (observed - fitted) ** 2
            for observed, fitted in zip(
                processed.scaled_ndvi,
                prediction,
            )
        )
        / len(prediction)
    )
    peak_doy, peak_value = (
        peak_irg_day_from_parameters(params)
    )

    return PeakIRGFit(
        parameters=params,
        peak_irg_doy=peak_doy,
        peak_irg_value=peak_value,
        spring_scale_days=params.spring_scale_days,
        fit_rmse=rmse,
        processed=processed,
        optimizer_success=bool(fit.success),
        optimizer_message=str(fit.message),
    )
