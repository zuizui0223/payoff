"""Conservative triangular PAYOFF phase certificates under bounded response error.

This optional route encloses, rather than point-estimates, the inverse map. It
uses exact rational arithmetic for signs; floats in the receipt are rounded
outward. The target is the frozen-resident ridge/better-outside phase, NOT
resident-updated evolutionary trapping. Kernel, coordinate and matching remain
assumptions. Measurement bands are simultaneous error bounds, not automatic CIs.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction as F
from itertools import product
import json
from math import inf, isfinite, nextafter
from typing import Sequence

Band = tuple[object, object, object]  # (exact coordinate, response lower, upper)


def _q(value: object) -> F:
    if isinstance(value, bool):
        raise ValueError("boolean is not a numeric bound")
    try:
        return F(value)
    except (TypeError, ValueError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError("bounds must be finite real rational-compatible numbers") from exc


def _bands(values: Sequence[Band], length: F) -> tuple[tuple[F, F, F], ...]:
    rows = tuple(tuple(_q(v) for v in row) for row in values)
    if any(len(row) != 3 for row in rows):
        raise ValueError("bands require coordinate, lower and upper")
    if any(not 0 < x <= length or lo > hi for x, lo, hi in rows):
        raise ValueError("require 0 < coordinate <= length and lower <= upper")
    if len({row[0] for row in rows}) != len(rows):
        raise ValueError("coordinates must be distinct within each stage")
    return rows


def _line(x1: F, y1: F, x2: F, y2: F, power: int) -> tuple[F, F]:
    slope = (y2 / x2**power - y1 / x1**power) / (x2 - x1)
    return y1 / x1**power - slope * x1, slope


def _vertices(rows, power):
    if len(rows) != 2:
        raise ValueError("two distinct calibration coordinates are required per stage")
    (x1, lo1, hi1), (x2, lo2, hi2) = rows
    return tuple(_line(x1, y1, x2, y2, power)
                 for y1, y2 in product((lo1, hi1), (lo2, hi2)))


def _hull(values):
    vals = tuple(values)
    return min(vals), max(vals)


def _convex_hull(points):
    pts = sorted(set(points))
    if len(pts) <= 1:
        return tuple(pts)
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lower, upper = [], []
    for point in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    for point in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return tuple(lower[:-1]+upper[:-1])


def _clip(polygon, a: F, b: F, c: F):
    """Intersect a closed convex polygon/segment/point with a*x+b*y <= c."""
    if not polygon:
        return ()
    out = []
    previous = polygon[-1]
    fp = a*previous[0]+b*previous[1]-c
    for current in polygon:
        fc = a*current[0]+b*current[1]-c
        if (fp <= 0) != (fc <= 0):
            t = fp/(fp-fc)
            out.append(tuple(p+t*(q-p) for p, q in zip(previous, current)))
        if fc <= 0:
            out.append(current)
        previous, fp = current, fc
    return _convex_hull(out)


def _compatible_polygons(bf, af, bh, ah):
    bp = _convex_hull((a, -2*m) for a, m in _vertices(bf, 1))
    ap = _convex_hull((a, -m) for a, m in _vertices(af, 2))
    for r, lo, hi in bh:
        bp = _clip(bp, r, -r*r/2, hi)
        bp = _clip(bp, -r, r*r/2, -lo)
    # A(d)=max(0,G*d^2-lambda*d^3). For hi>=0 the upper constraint
    # is linear; the lower constraint is needed only when lo>0. Thus even
    # support-crossing validation bands preserve convex feasibility here.
    for d, lo, hi in ah:
        if hi < 0:
            return bp, ()
        ap = _clip(ap, d*d, -d**3, hi)
        if lo > 0:
            ap = _clip(ap, -d*d, d**3, -lo)
    return bp, ap


def _outward(value: F, upper: bool) -> float:
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError("output overflow; rescale input units") from exc
    if not isfinite(result):
        raise ValueError("output overflow; rescale input units")
    if (F(result) < value if upper else F(result) > value):
        result = nextafter(result, inf if upper else -inf)
    if not isfinite(result):
        raise ValueError("outward enclosure overflow; rescale inputs")
    return result


def _discriminant(E: F, g: F) -> F:
    # Positive multiple of the discriminant of
    # -g*x^3/E + (g-1/2)*x^2 + x-1/2.
    return 2*E*E*(2*g-1)**2 + 2*E*(18*g-1) - 27*g


def _box_phase(E, g) -> str:
    elo, ehi = E
    glo, ghi = g
    on = lambda e: 1/e - 1
    # Both exact boundary curves decrease with E. No sqrt is needed for signs.
    if glo > on(elo) and _discriminant(ehi, ghi) < 0:
        return "certified_barrier"
    if ghi <= on(ehi):
        return "certified_no_ridge"
    if glo > on(elo) and _discriminant(elo, glo) >= 0:
        return "certified_ridge_not_below_outside_optimum"
    return "unresolved_outer_box"


@dataclass(frozen=True)
class BoundedCalibrationReceipt:
    status: str
    box_status: str
    bounds: dict[str, tuple[float, float]]
    exact_bounds: dict[str, tuple[str, str]]
    feasible_witness_compatible: bool
    feasible_witness_parameters: dict[str, str]
    vertex_counts: tuple[int, int]
    holdout_coverage: bool
    frozen_resident_barrier: bool | None
    common_scale: str
    matched_context: str
    scope: str = "conditional_on_simultaneous_bands_and_declared_quadratic_triangular_family"
    mutation_radius_identified: bool = False


def certify_bounded_triangular(
    intrinsic_fit: Sequence[Band], interaction_fit: Sequence[Band], *,
    common_scale: str, matched_context: str, matched_contrasts_declared: bool,
    intrinsic_holdout: Sequence[Band] = (), interaction_holdout: Sequence[Band] = (),
    length: object = 1,
) -> BoundedCalibrationReceipt:
    """Certify a phase only if its conservative enclosure lies in one regime.

    Fit bands form an outer Cartesian error set, not an independence model.
    Exact half-plane intersections retain every compatible parameter within
    that set. A feasible witness verifies nonemptiness after conditioning on
    separately declared validation bands. Once assimilated, these observations
    are constraints, NOT fresh independent validation of the resulting set.
    Validation coordinates are not used
    to choose the kernel, matching assumptions or error thresholds.
    Require new intrinsic, inside-support and outside-support validation points.

    ``None`` is unresolved, not absence. No probability is assigned to the box.
    Decimal strings/Fractions preserve decimal values exactly; floats preserve
    their actual binary values. Coordinates themselves are assumed error-free.
    """
    if (not isinstance(common_scale, str) or not common_scale.strip()
            or not isinstance(matched_context, str) or not matched_context.strip()
            or matched_contrasts_declared is not True):
        raise ValueError("declare common scale, matched context and matched contrasts")
    L = _q(length)
    if L <= 0:
        raise ValueError("length must be positive")
    bf, af = _bands(intrinsic_fit, L), _bands(interaction_fit, L)
    bh, ah = _bands(intrinsic_holdout, L), _bands(interaction_holdout, L)
    for fit, hold in ((bf, bh), (af, ah)):
        if {x for x, _, _ in fit} & {x for x, _, _ in hold}:
            raise ValueError("holdout coordinates must not reuse fit coordinates")
    bounds = {}
    bv, av = _compatible_polygons(bf, af, bh, ah)
    witness_parameters = {}

    def receipt(status, box, witness=False, coverage=False, phase=None):
        return BoundedCalibrationReceipt(
            status, box,
            {key: (_outward(lo, False), _outward(hi, True))
             for key, (lo, hi) in bounds.items()},
            {key: (str(lo), str(hi)) for key, (lo, hi) in bounds.items()},
            witness, dict(witness_parameters), (len(bv), len(av)),
            coverage, phase, common_scale, matched_context,
        )

    if any(lo <= 0 for _, lo, hi in af):
        return receipt("positive_interior_calibration_not_certified", "not_evaluated")
    if not bv or not av:
        return receipt("inconsistent_response_bands", "not_evaluated")
    alpha, kappa = _hull(a for a, k in bv), _hull(k for a, k in bv)
    G, lam = _hull(a for a, lam in av), _hull(lam for a, lam in av)
    bounds.update(alpha=alpha, kappa=kappa, G=G, G_over_epsilon=lam)
    if min(alpha[0], kappa[0], G[0], lam[0]) <= 0:
        return receipt("coefficient_domain_unresolved", "not_evaluated")
    # Linear-fractional extrema over each nonempty compatible polygon occur at
    # vertices. Retaining pairing is sharper than ratios of marginal hulls.
    rstar = _hull(a/k for a, k in bv)
    epsilon = _hull(a/lam for a, lam in av)
    E = epsilon[0]/rstar[1], epsilon[1]/rstar[0]
    g = G[0]/kappa[1], G[1]/kappa[0]
    bounds.update(rstar=rstar, epsilon=epsilon, E=E, g=g)
    if (any(lo <= 0 for _, lo, hi in af)
            or max(x for x, _, _ in af) >= epsilon[0]
            or rstar[1] > L or not 0 < E[0] <= E[1] < 1):
        return receipt("phase_or_support_domain_unresolved", "not_evaluated")
    box = _box_phase(E, g)
    a0 = sum(a for a, k in bv)/len(bv)
    k0 = sum(k for a, k in bv)/len(bv)
    G0 = sum(a for a, lam in av)/len(av)
    lam0 = sum(lam for a, lam in av)/len(av)
    e0 = G0/lam0
    witness_parameters.update(alpha=str(a0), kappa=str(k0), G=str(G0), epsilon=str(e0))
    bp = lambda r: a0*r - k0*r*r/2
    ap = lambda d: G0*d*d*max(F(0), 1-d/e0)
    witness = (all(lo <= bp(x) <= hi for x, lo, hi in bf+bh)
               and all(lo <= ap(x) <= hi for x, lo, hi in af+ah))
    coverage = (bool(bh) and any(d < epsilon[0] for d, _, _ in ah)
                and any(d > epsilon[1] for d, _, _ in ah))
    if not witness:
        raise ArithmeticError("exact polygon centroid failed the original measurement bands")
    if not coverage:
        return receipt("calibration_only_missing_holdout_coverage", box, True, False)
    phase = True if box == "certified_barrier" else (
        False if box.startswith("certified_") else None)
    return receipt("bounded_error_audit_complete", box, True, True, phase)


def synthetic_example() -> dict:
    b = lambda r: r/2-r*r/2
    a = lambda d: 2*d*d*max(F(0), 1-d/F("0.3"))
    outputs = []
    for error in ("0", "0.00001", "0.0001", "0.001"):
        u = F(error)
        band = lambda x, fun: (x, fun(x)-u, fun(x)+u)
        r = certify_bounded_triangular(
            [band(F(x), b) for x in ("0.2", "0.4")],
            [band(F(x), a) for x in ("0.05", "0.15")],
            intrinsic_holdout=[band(F("0.6"), b)],
            interaction_holdout=[band(F(x), a) for x in ("0.2", "0.4")],
            common_scale="synthetic payoff units", matched_context="synthetic fixed context",
            matched_contrasts_declared=True,
        )
        outputs.append({"absolute_response_error": error, **asdict(r)})
    return {"data_kind": "synthetic_bounded_error", "audits": outputs}


if __name__ == "__main__":
    print(json.dumps(synthetic_example(), indent=2, allow_nan=False))
