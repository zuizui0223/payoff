"""Retrospective calendar-duration sensitivity for phase retention.

The primary empirical estimator remains a segment-scale coefficient:

    E_next = Z gamma + lambda E_current + error.

This module compares it with the restricted monotone calendar-time model:

    E_next = Z gamma + exp(-k * delta_t) E_current + error.

Both models have the same number of fitted parameters. The duration model is a
diagnostic only; it is not used to overwrite registered lambda results.
"""

from __future__ import annotations

import math
from typing import Iterable

import numpy as np


def _array(values, name: str) -> np.ndarray:
    out = np.asarray(values, dtype=float)
    if out.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    if not np.all(np.isfinite(out)):
        raise ValueError(f"{name} must be finite")
    return out


def _matrix(values, n: int) -> np.ndarray:
    out = np.asarray(values, dtype=float)
    if out.ndim == 1:
        out = out[:, None]
    if out.ndim != 2 or out.shape[0] != n:
        raise ValueError("nuisance matrix must have one row per observation")
    if not np.all(np.isfinite(out)):
        raise ValueError("nuisance matrix must be finite")
    return out


def _cluster_covariance(jacobian, residual, groups):
    jacobian = np.asarray(jacobian, dtype=float)
    residual = _array(residual, "residual")
    groups = np.asarray(tuple(str(x) for x in groups), dtype=object)
    if len(groups) != len(residual):
        raise ValueError("groups length mismatch")

    unique = np.unique(groups)
    if len(unique) < 2:
        raise ValueError("at least two clusters are required")

    bread = np.linalg.pinv(jacobian.T @ jacobian)
    meat = np.zeros((jacobian.shape[1], jacobian.shape[1]), dtype=float)
    for group in unique:
        mask = groups == group
        score = jacobian[mask].T @ residual[mask]
        meat += np.outer(score, score)

    n = len(residual)
    p = jacobian.shape[1]
    correction = 1.0
    if n > p:
        correction = (len(unique) / (len(unique) - 1.0)) * ((n - 1.0) / (n - p))
    return bread @ meat @ bread * correction


def fit_constant_segment_retention(
    *,
    origin_phase,
    destination_phase,
    nuisance,
    groups,
):
    x = _array(origin_phase, "origin_phase")
    y = _array(destination_phase, "destination_phase")
    if len(x) != len(y):
        raise ValueError("phase arrays must have equal length")
    z = _matrix(nuisance, len(x))
    design = np.column_stack([x, z])
    coef = np.linalg.lstsq(design, y, rcond=None)[0]
    residual = y - design @ coef
    cov = _cluster_covariance(design, residual, groups)
    return {
        "lambda_hat": float(coef[0]),
        "lambda_cluster_se": float(math.sqrt(max(float(cov[0, 0]), 0.0))),
        "sse": float(residual @ residual),
        "rmse": float(math.sqrt(float(residual @ residual) / len(y))),
        "n": int(len(y)),
        "n_parameters": int(design.shape[1]),
        "n_clusters": int(len(np.unique(np.asarray(groups, dtype=str)))),
    }


def _solve_exponential_at_k(k, x, y, dt, z):
    retention = np.exp(-float(k) * dt)
    gamma = np.linalg.lstsq(z, y - retention * x, rcond=None)[0]
    residual = y - retention * x - z @ gamma
    return float(residual @ residual), gamma, residual, retention


def _bounded_minimize(objective, lower: float, upper: float) -> float:
    if not (math.isfinite(lower) and math.isfinite(upper) and lower < upper):
        raise ValueError("invalid optimization bounds")

    grid = np.linspace(lower, upper, 1001)
    scores = np.asarray([objective(float(k)) for k in grid], dtype=float)
    index = int(np.argmin(scores))
    if index == 0:
        a, b = float(grid[0]), float(grid[1])
    elif index == len(grid) - 1:
        a, b = float(grid[-2]), float(grid[-1])
    else:
        a, b = float(grid[index - 1]), float(grid[index + 1])

    phi = (math.sqrt(5.0) - 1.0) / 2.0
    c = b - phi * (b - a)
    d = a + phi * (b - a)
    fc = objective(c)
    fd = objective(d)
    for _ in range(100):
        if abs(b - a) < 1e-11:
            break
        if fc <= fd:
            b, d, fd = d, c, fc
            c = b - phi * (b - a)
            fc = objective(c)
        else:
            a, c, fc = c, d, fd
            d = a + phi * (b - a)
            fd = objective(d)
    candidates = [(a, objective(a)), (b, objective(b)), ((a + b) / 2.0, objective((a + b) / 2.0))]
    return float(min(candidates, key=lambda row: row[1])[0])


def fit_calendar_exponential_retention(
    *,
    origin_phase,
    destination_phase,
    duration_days,
    nuisance,
    groups,
    k_bounds=(0.0, 2.0),
):
    x = _array(origin_phase, "origin_phase")
    y = _array(destination_phase, "destination_phase")
    dt = _array(duration_days, "duration_days")
    if not (len(x) == len(y) == len(dt)):
        raise ValueError("phase and duration arrays must have equal length")
    if np.any(dt <= 0.0):
        raise ValueError("duration_days must be > 0")
    z = _matrix(nuisance, len(x))

    lower, upper = [float(v) for v in k_bounds]
    k_hat = _bounded_minimize(
        lambda k: _solve_exponential_at_k(k, x, y, dt, z)[0],
        lower,
        upper,
    )
    sse, gamma, residual, retention = _solve_exponential_at_k(
        k_hat, x, y, dt, z
    )

    derivative_k = -dt * retention * x
    jacobian = np.column_stack([derivative_k, z])
    cov = _cluster_covariance(jacobian, residual, groups)
    k_se = float(math.sqrt(max(float(cov[0, 0]), 0.0)))

    median_duration = float(np.median(dt))
    return {
        "k_hat_per_day": k_hat,
        "k_cluster_se": k_se,
        "sse": sse,
        "rmse": float(math.sqrt(sse / len(y))),
        "retention_at_median_duration": float(
            math.exp(-k_hat * median_duration)
        ),
        "median_duration_days": median_duration,
        "duration_q25_days": float(np.quantile(dt, 0.25)),
        "duration_q75_days": float(np.quantile(dt, 0.75)),
        "n": int(len(y)),
        "n_parameters": int(z.shape[1] + 1),
        "n_clusters": int(len(np.unique(np.asarray(groups, dtype=str)))),
        "boundary_hit": bool(
            abs(k_hat - lower) < 1e-6 or abs(k_hat - upper) < 1e-6
        ),
    }


def compare_segment_and_duration_models(
    *,
    origin_phase,
    destination_phase,
    duration_days,
    nuisance,
    groups,
    k_bounds=(0.0, 2.0),
):
    segment = fit_constant_segment_retention(
        origin_phase=origin_phase,
        destination_phase=destination_phase,
        nuisance=nuisance,
        groups=groups,
    )
    duration = fit_calendar_exponential_retention(
        origin_phase=origin_phase,
        destination_phase=destination_phase,
        duration_days=duration_days,
        nuisance=nuisance,
        groups=groups,
        k_bounds=k_bounds,
    )
    if segment["n_parameters"] != duration["n_parameters"]:
        raise AssertionError("model comparison requires equal parameter counts")
    if segment["sse"] <= 0.0 or duration["sse"] <= 0.0:
        raise ValueError("SSE must be positive for AIC comparison")

    delta_aic = segment["n"] * math.log(duration["sse"] / segment["sse"])
    return {
        "segment_model": segment,
        "calendar_duration_model": duration,
        "sse_ratio_duration_over_segment": duration["sse"] / segment["sse"],
        "delta_aic_duration_minus_segment": float(delta_aic),
    }


def classify_duration_evidence(
    delta_aic_original: float,
    delta_aic_log_duration_adjusted: float,
    *,
    threshold: float = 2.0,
) -> str:
    values = (
        float(delta_aic_original),
        float(delta_aic_log_duration_adjusted),
    )
    if all(v >= threshold for v in values):
        return "SEGMENT_RETENTION_PREFERRED"
    if all(v <= -threshold for v in values):
        return "CALENDAR_DURATION_DECAY_SUPPORTED"
    return "SPECIFICATION_SENSITIVE_OR_INCONCLUSIVE"
