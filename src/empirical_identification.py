"""Conditional two-stage calibration of the triangular PAYOFF extension.

Inputs are payoff contrasts, not architecture frequencies. Two fit points per
stage identify parameters only within the predeclared quadratic/triangular
family. Separate held-out contrasts audit compatibility; they do not establish
that this is the uniquely correct biological kernel.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from math import isfinite, sqrt
from typing import Sequence

Point = tuple[float, float]


@dataclass(frozen=True)
class CalibrationReceipt:
    common_scale: str
    matched_context: str
    absolute_payoff_scale_known: bool
    parameter_scope: str
    alpha: float
    kappa: float
    gamma: float
    epsilon: float
    intrinsic_optimum: float
    E: float
    g: float
    max_holdout_error: float | None
    status: str
    frozen_resident_barrier: bool | None
    mutation_radius_identified: bool = False


def _points(values: Sequence[Point], length: float) -> tuple[Point, ...]:
    points = tuple((float(x), float(y)) for x, y in values)
    if any(not isfinite(x) or not isfinite(y) or not 0 < x <= length
           for x, y in points):
        raise ValueError("contrasts need finite values and 0 < coordinate <= length")
    return points


def _line(points: tuple[Point, ...], power: int) -> tuple[float, float]:
    if len(points) != 2:
        raise ValueError("exact calibration requires two predeclared fit points per stage")
    (x1, z1), (x2, z2) = points
    if abs(x2 - x1) <= 1e-10 * max(abs(x1), abs(x2)):
        raise ValueError("rank-deficient or numerically unresolved fit distances")
    y1, y2 = z1 / x1**power, z2 / x2**power
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1
    if not all(isfinite(v) for v in (slope, intercept)):
        raise ValueError("calibration overflow; rescale coordinates/payoffs")
    return intercept, slope


def calibrate_triangular(
    intrinsic_fit: Sequence[Point],
    interaction_fit: Sequence[Point],
    *,
    common_scale: str,
    matched_context: str,
    matched_contrasts_declared: bool,
    length: float = 1.0,
    absolute_payoff_scale_known: bool = False,
    intrinsic_holdout: Sequence[Point] = (),
    interaction_holdout: Sequence[Point] = (),
    absolute_error_tolerance: float = 1e-9,
) -> CalibrationReceipt:
    """Invert two intrinsic and two positive interior interaction contrasts.

    Intrinsic: B(r)=alpha*r-kappa*r**2/2 (relative to r=0).
    Interaction: A(d)=G*d**2*max(0,1-d/epsilon), G=-gamma>0.
    Thus B(r)/r and A(d)/d**2 are affine in their respective coordinates.

    Inputs designated as holdouts must use new coordinates. For the qualified
    receipt require an intrinsic holdout and interaction holdouts both inside
    and outside the fitted support. The tolerance is a predeclared discrepancy
    rule, NOT a confidence interval. Neither schema nor residual checks verify
    the caller's biological matching or scale-calibration declarations.
    """
    L, tol = float(length), float(absolute_error_tolerance)
    if not isfinite(L) or L <= 0 or not isfinite(tol) or tol < 0:
        raise ValueError("length must be positive and tolerance finite/nonnegative")
    if (not isinstance(common_scale, str) or not common_scale.strip()
            or not isinstance(matched_context, str) or not matched_context.strip()
            or matched_contrasts_declared is not True):
        raise ValueError("declare the common scale, matched context and matched contrasts")
    if type(absolute_payoff_scale_known) is not bool:
        raise ValueError("absolute_payoff_scale_known must be a boolean")
    bfit, afit = _points(intrinsic_fit, L), _points(interaction_fit, L)
    bh, ah = _points(intrinsic_holdout, L), _points(interaction_holdout, L)
    for fit, holdout in ((bfit, bh), (afit, ah)):
        if {x for x, _ in fit} & {x for x, _ in holdout}:
            raise ValueError("holdout coordinates must not reuse calibration coordinates")
    alpha, b_slope = _line(bfit, 1)
    G, a_slope = _line(afit, 2)
    kappa = -2 * b_slope
    if alpha <= 0 or kappa <= 0 or G <= 0 or a_slope >= 0:
        raise ValueError("calibration incompatible with positive curvature/negative feedback")
    epsilon = -G / a_slope
    if not isfinite(epsilon) or any(y <= 0 or d >= epsilon for d, y in afit):
        raise ValueError("interaction fit points must both be positive and inside support")
    optimum = alpha / kappa
    E, g = epsilon / optimum, G / kappa
    if not all(isfinite(v) for v in (kappa, optimum, E, g)):
        raise ValueError("derived parameters overflow; rescale inputs")
    errors = [abs(y - (alpha*r - 0.5*kappa*r*r)) for r, y in bh]
    errors += [abs(y - G*d*d*max(0.0, 1-d/epsilon)) for d, y in ah]
    error = max(errors) if errors else None
    sufficient_holdouts = (bool(bh) and any(d < epsilon for d, _ in ah)
                           and any(d > epsilon for d, _ in ah))
    status = "calibration_only"
    if error is not None and error > tol:
        status = "holdout_inconsistent"
    elif sufficient_holdouts:
        status = "holdout_consistent_with_declared_family"
    phase = None
    if status == "holdout_consistent_with_declared_family" and optimum <= L and 0 < E < 1:
        # Rationalized contact root avoids cancellation for narrow ranges.
        x = 4*E / (3 + sqrt(9-8*E))
        lower = 1/E-1
        upper = (1-x)*(3-x)/(2*x*x)
        phase = lower < g < upper
    elif status == "holdout_consistent_with_declared_family":
        status = "outside_registered_phase_domain"
    return CalibrationReceipt(
        common_scale, matched_context, absolute_payoff_scale_known,
        "absolute_scale_declared" if absolute_payoff_scale_known else "working_scale_only",
        alpha, kappa, -G, epsilon, optimum, E, g, error, status, phase,
    )


def synthetic_example() -> dict:
    b = lambda r: 0.5*r - 0.5*r*r
    a = lambda d: 2*d*d*max(0.0, 1-d/0.3)
    receipt = calibrate_triangular(
        [(r, b(r)) for r in (0.2, 0.4)],
        [(d, a(d)) for d in (0.05, 0.15)],
        common_scale="synthetic payoff units", matched_context="synthetic fixed environment",
        matched_contrasts_declared=True,
        intrinsic_holdout=[(0.6, b(0.6))],
        interaction_holdout=[(0.2, a(0.2)), (0.4, a(0.4))],
    )
    return {"data_kind": "synthetic_exact_witness", "receipt": asdict(receipt)}


if __name__ == "__main__":
    print(json.dumps(synthetic_example(), indent=2, allow_nan=False))
