"""Predictive-connectivity coordinates for PAYOFF-B.

The Bayesian timing extension distinguishes the environmental state that is
available when a migrant commits from the future state that will be realized at
the next destination.  This module provides small, dependency-free estimators
for that information link.

The primary empirical coordinate is a signed Pearson correlation between
*detrended* origin and destination seasonal-state series.  Detrending each
location separately prevents a shared long-term trend from being counted as
interannual predictive information.

For prospective analyses, trailing-window estimates use only years strictly
before the outcome year.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import asin, isfinite, pi, sqrt
from typing import Iterable, Sequence


@dataclass(frozen=True)
class PredictiveConnectivity:
    n_pairs: int
    rho: float
    r_squared: float
    gaussian_binary_agreement: float
    gaussian_optimal_binary_accuracy: float


def _finite_tuple(values: Iterable[float], name: str) -> tuple[float, ...]:
    rows = tuple(float(value) for value in values)
    if any(not isfinite(value) for value in rows):
        raise ValueError(f"{name} values must be finite")
    return rows


def pearson_correlation(
    x: Iterable[float],
    y: Iterable[float],
) -> float:
    """Return ordinary Pearson correlation without external dependencies."""

    xs = _finite_tuple(x, "x")
    ys = _finite_tuple(y, "y")
    if len(xs) != len(ys):
        raise ValueError("x and y must have the same length")
    if len(xs) < 3:
        raise ValueError("at least three paired values are required")

    xbar = sum(xs) / len(xs)
    ybar = sum(ys) / len(ys)
    sxx = sum((value - xbar) ** 2 for value in xs)
    syy = sum((value - ybar) ** 2 for value in ys)
    if sxx <= 0.0 or syy <= 0.0:
        raise ValueError("correlation is unidentified with zero variance")
    sxy = sum(
        (x_value - xbar) * (y_value - ybar)
        for x_value, y_value in zip(xs, ys)
    )
    rho = sxy / sqrt(sxx * syy)
    return max(-1.0, min(1.0, rho))


def linear_residuals(
    predictor: Iterable[float],
    response: Iterable[float],
) -> tuple[float, ...]:
    """Residualize response on intercept + one linear predictor."""

    xs = _finite_tuple(predictor, "predictor")
    ys = _finite_tuple(response, "response")
    if len(xs) != len(ys):
        raise ValueError("predictor and response must have the same length")
    if len(xs) < 3:
        raise ValueError("at least three rows are required")

    xbar = sum(xs) / len(xs)
    ybar = sum(ys) / len(ys)
    sxx = sum((value - xbar) ** 2 for value in xs)
    if sxx <= 0.0:
        raise ValueError("linear trend is unidentified with zero predictor variance")
    sxy = sum(
        (x_value - xbar) * (y_value - ybar)
        for x_value, y_value in zip(xs, ys)
    )
    slope = sxy / sxx
    intercept = ybar - slope * xbar
    return tuple(
        y_value - (intercept + slope * x_value)
        for x_value, y_value in zip(xs, ys)
    )


def gaussian_binary_agreement_from_correlation(rho: float) -> float:
    """Map Gaussian correlation to same-sign binary agreement probability.

    For two centered standard-normal variables with correlation rho,

        P(sign X == sign Y) = 1/2 + asin(rho)/pi.

    This is a model-conditional bridge to the binary cue game, not the primary
    empirical estimand.
    """

    value = float(rho)
    if not isfinite(value) or not -1.0 <= value <= 1.0:
        raise ValueError("rho must be finite and lie in [-1,1]")
    return 0.5 + asin(value) / pi


def gaussian_optimal_binary_accuracy_from_correlation(rho: float) -> float:
    """Return best binary accuracy if an inverse cue can be learned."""

    agreement = gaussian_binary_agreement_from_correlation(rho)
    return max(agreement, 1.0 - agreement)


def detrended_predictive_connectivity(
    years: Iterable[float],
    origin_state: Iterable[float],
    destination_state: Iterable[float],
    *,
    min_pairs: int = 6,
) -> PredictiveConnectivity:
    """Estimate interannual predictive connectivity after separate detrending."""

    if min_pairs < 4:
        raise ValueError("min_pairs must be at least 4")
    year_rows = _finite_tuple(years, "years")
    origin_rows = _finite_tuple(origin_state, "origin_state")
    destination_rows = _finite_tuple(destination_state, "destination_state")
    if not (
        len(year_rows) == len(origin_rows) == len(destination_rows)
    ):
        raise ValueError("years and state series must have equal length")
    if len(year_rows) < min_pairs:
        raise ValueError("insufficient paired years for predictive connectivity")
    if len(set(year_rows)) != len(year_rows):
        raise ValueError("years must be unique within one connectivity series")

    origin_residual = linear_residuals(year_rows, origin_rows)
    destination_residual = linear_residuals(year_rows, destination_rows)
    rho = pearson_correlation(origin_residual, destination_residual)
    agreement = gaussian_binary_agreement_from_correlation(rho)
    return PredictiveConnectivity(
        n_pairs=len(year_rows),
        rho=rho,
        r_squared=rho * rho,
        gaussian_binary_agreement=agreement,
        gaussian_optimal_binary_accuracy=max(
            agreement,
            1.0 - agreement,
        ),
    )


def trailing_precommitment_connectivity(
    years: Sequence[int],
    origin_state: Sequence[float],
    destination_state: Sequence[float],
    *,
    target_year: int,
    window_years: int = 8,
    min_pairs: int = 6,
) -> PredictiveConnectivity:
    """Use only a trailing calendar window strictly before target_year.

    The declared window is

        target_year - window_years <= year < target_year.

    The current target year is therefore never used to estimate its own
    predictive-connectivity covariate.
    """

    if window_years < 4:
        raise ValueError("window_years must be at least 4")
    if not (len(years) == len(origin_state) == len(destination_state)):
        raise ValueError("years and state series must have equal length")

    selected = [
        (float(year), float(origin), float(destination))
        for year, origin, destination in zip(
            years,
            origin_state,
            destination_state,
        )
        if target_year - window_years <= int(year) < target_year
    ]
    if len(selected) < min_pairs:
        raise ValueError("insufficient pre-outcome years in trailing window")

    return detrended_predictive_connectivity(
        [row[0] for row in selected],
        [row[1] for row in selected],
        [row[2] for row in selected],
        min_pairs=min_pairs,
    )
