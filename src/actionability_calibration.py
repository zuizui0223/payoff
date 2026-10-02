"""Empirical calibration gate for reduced-form retained actionability.

The prospective continuous PAYOFF-B extension uses

    V_t(q) = r_t V_ref(q)

as a deliberately reduced separable model.

This module prevents a common invalid shortcut: interpreting route fraction,
number of remaining actions, stopover count, flowering duration, or phase
correction directly as r_t.

Instead, r_t is empirically licensed only when stage-specific value of
information is approximately proportional to a declared reference-stage value
across multiple cue qualities q.

For cue-quality support Q,

    r_t(q) = V_t(q) / V_ref(q).

A scalar retained-actionability weight is licensed only if:
  1. V_ref(q) is positive at enough q values;
  2. all ratios are within [0,1] up to tolerance;
  3. the ratios are sufficiently constant across q.

If these gates fail, the correct object is the full V_t(q) surface, not a
single r_t.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from statistics import mean
from typing import Sequence


@dataclass(frozen=True)
class ActionabilityCalibration:
    status: str
    cue_qualities: tuple[float, ...]
    usable_cue_qualities: tuple[float, ...]
    ratios: tuple[float, ...]
    retained_actionability: float | None
    max_abs_ratio_deviation: float | None
    ratio_min: float | None
    ratio_max: float | None
    tolerance: float
    interpretation: str


def calibrate_reduced_actionability(
    cue_qualities: Sequence[float],
    reference_information_values: Sequence[float],
    stage_information_values: Sequence[float],
    *,
    constancy_tolerance: float = 0.05,
    minimum_usable_points: int = 2,
    numerical_tolerance: float = 1e-12,
) -> ActionabilityCalibration:
    """Test whether V_stage(q) ~= r V_ref(q) supports one scalar r in [0,1]."""

    q = tuple(float(x) for x in cue_qualities)
    ref = tuple(float(x) for x in reference_information_values)
    stage = tuple(float(x) for x in stage_information_values)
    tol = float(constancy_tolerance)
    nmin = int(minimum_usable_points)
    eps = float(numerical_tolerance)

    if not q or not (len(q) == len(ref) == len(stage)):
        raise ValueError("cue qualities and information-value vectors must align")
    if nmin < 1:
        raise ValueError("minimum_usable_points must be >=1")
    if not isfinite(tol) or tol < 0.0:
        raise ValueError("constancy_tolerance must be finite and non-negative")
    if not isfinite(eps) or eps <= 0.0:
        raise ValueError("numerical_tolerance must be finite and positive")
    if any((not isfinite(x)) or x < 0.5 or x > 1.0 for x in q):
        raise ValueError("cue qualities must lie in [0.5,1]")
    if any((not isfinite(x)) or x < -eps for x in ref + stage):
        raise ValueError("information values must be finite and non-negative")

    usable_q = []
    ratios = []
    for qi, refi, stagei in zip(q, ref, stage):
        if refi <= eps:
            continue
        usable_q.append(qi)
        ratios.append(stagei / refi)

    if len(ratios) < nmin:
        return ActionabilityCalibration(
            status="NOT_IDENTIFIABLE_INSUFFICIENT_POSITIVE_REFERENCE_VOI",
            cue_qualities=q,
            usable_cue_qualities=tuple(usable_q),
            ratios=tuple(ratios),
            retained_actionability=None,
            max_abs_ratio_deviation=None,
            ratio_min=(min(ratios) if ratios else None),
            ratio_max=(max(ratios) if ratios else None),
            tolerance=tol,
            interpretation=(
                "too few cue-quality points have positive reference information "
                "value to test separable retained actionability"
            ),
        )

    r_min = min(ratios)
    r_max = max(ratios)
    r_hat = mean(ratios)
    max_dev = max(abs(x - r_hat) for x in ratios)

    if r_min < -tol or r_max > 1.0 + tol:
        return ActionabilityCalibration(
            status="FAIL_RATIO_OUTSIDE_UNIT_INTERVAL",
            cue_qualities=q,
            usable_cue_qualities=tuple(usable_q),
            ratios=tuple(ratios),
            retained_actionability=None,
            max_abs_ratio_deviation=max_dev,
            ratio_min=r_min,
            ratio_max=r_max,
            tolerance=tol,
            interpretation=(
                "stage-to-reference VOI ratio is not a retained fraction in "
                "[0,1]; use the full stage-specific information-value surface"
            ),
        )

    if max_dev > tol:
        return ActionabilityCalibration(
            status="FAIL_Q_DEPENDENT_ACTIONABILITY",
            cue_qualities=q,
            usable_cue_qualities=tuple(usable_q),
            ratios=tuple(ratios),
            retained_actionability=None,
            max_abs_ratio_deviation=max_dev,
            ratio_min=r_min,
            ratio_max=r_max,
            tolerance=tol,
            interpretation=(
                "V_stage(q)/V_ref(q) changes materially with cue quality; "
                "a scalar retained-actionability weight is not licensed"
            ),
        )

    r_clamped = min(1.0, max(0.0, r_hat))
    return ActionabilityCalibration(
        status="PASS_SEPARABLE_REDUCED_ACTIONABILITY",
        cue_qualities=q,
        usable_cue_qualities=tuple(usable_q),
        ratios=tuple(ratios),
        retained_actionability=r_clamped,
        max_abs_ratio_deviation=max_dev,
        ratio_min=r_min,
        ratio_max=r_max,
        tolerance=tol,
        interpretation=(
            "stage-specific information value is approximately a constant "
            "fraction of reference information value across the declared q support"
        ),
    )
