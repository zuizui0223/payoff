"""Minimax placement of no-refit interior-frequency holdouts for PAYOFF.

This module designs frequencies only. It does not use observed interior responses
and therefore cannot leak holdout outcomes back into endpoint fitting.

Two alternative classes are deliberately separated:

1. Lipschitz residual class. Let r(p)=observed_frequency_gap(p)-canonical_line(p),
   with r(0)=r(1)=0 and |r(x)-r(y)| <= L|x-y|. For m strict interior samples,
   the worst unsampled residual envelope is L times the covering radius of
   {0, samples..., 1}. Equal spacing p_i=i/(m+1) uniquely minimizes that radius.

2. Uniform signed curvature class. If r'' >= kappa everywhere or r'' <= -kappa
   everywhere, r(0)=r(1)=0, then |r(p)| >= kappa*p*(1-p)/2. A single holdout at
   p=1/2 maximizes this guaranteed departure, giving kappa/8.

Neither result is an optimality statement over arbitrary nonlinear alternatives.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from typing import Sequence

from .reciprocal_invasion_identification import _q


def _positive_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _nonnegative(value: object, name: str) -> F:
    x = _q(value)
    if x < 0:
        raise ValueError(f"{name} must be nonnegative")
    return x


def covering_radius(points: Sequence[object]) -> F:
    """Exact covering radius on [0,1], including the fixed endpoint anchors."""
    ps = tuple(_q(p) for p in points)
    if any(not F(0) < p < F(1) for p in ps):
        raise ValueError("design points must be strictly interior")
    if tuple(sorted(ps)) != ps or len(set(ps)) != len(ps):
        raise ValueError("design points must be unique and strictly increasing")
    anchors = (F(0),) + ps + (F(1),)
    return max((b-a)/2 for a, b in zip(anchors, anchors[1:]))


@dataclass(frozen=True)
class LipschitzHoldoutDesignReceipt:
    holdout_count: int
    optimal_frequencies_exact: tuple[str, ...]
    maximum_gap_exact: str
    minimax_covering_radius_exact: str
    residual_lipschitz_bound_exact: str | None
    worst_unsampled_residual_envelope_exact: str | None
    optimality: str = "global_minimax_over_all_strict_interior_m_point_designs"
    holdout_outcomes_used_for_design: bool = False
    arbitrary_nonlinearity_identified: bool = False


@dataclass(frozen=True)
class SignedCurvatureOnePointReceipt:
    optimal_frequency_exact: str
    curvature_lower_bound_exact: str
    guaranteed_departure_at_optimum_exact: str
    alternative_class: str = "uniform_one_sign_second_derivative_magnitude_at_least_kappa"
    holdout_outcomes_used_for_design: bool = False
    arbitrary_nonlinearity_identified: bool = False


def design_lipschitz_holdouts(
    holdout_count: int, *, residual_lipschitz_bound: object | None = None,
) -> LipschitzHoldoutDesignReceipt:
    """Return the exact minimax m-point coverage design on [0,1].

    With endpoints already fixed by reciprocal invasion, m interior holdouts split
    [0,1] into m+1 gaps. Any design has a gap at least 1/(m+1), hence covering
    radius at least 1/(2(m+1)). Equal spacing attains the bound.
    """
    m = _positive_int(holdout_count, "holdout_count")
    denom = m + 1
    ps = tuple(F(i, denom) for i in range(1, denom))
    radius = F(1, 2*denom)
    L = None if residual_lipschitz_bound is None else _nonnegative(
        residual_lipschitz_bound, "residual_lipschitz_bound")
    envelope = None if L is None else L*radius
    return LipschitzHoldoutDesignReceipt(
        m, tuple(map(str, ps)), str(F(1, denom)), str(radius),
        None if L is None else str(L), None if envelope is None else str(envelope),
    )


def design_one_point_for_signed_curvature(
    curvature_lower_bound: object,
) -> SignedCurvatureOnePointReceipt:
    """Optimal one-point test against a uniformly signed curvature departure.

    If r'' has one declared sign and |r''| >= kappa throughout [0,1], with endpoint
    residuals zero, then |r(p)| >= kappa*p*(1-p)/2. The factor p(1-p) is uniquely
    maximized at p=1/2, so the guaranteed departure is kappa/8.
    """
    kappa = _nonnegative(curvature_lower_bound, "curvature_lower_bound")
    return SignedCurvatureOnePointReceipt("1/2", str(kappa), str(kappa/F(8)))
