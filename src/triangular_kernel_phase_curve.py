"""Dimensionless phase curve for the triangular-kernel accessibility barrier.

For an unconstrained intrinsic optimum ``r*=alpha/kappa``, define

    E = epsilon/r* in (0,1),
    g = G/kappa = -gamma/kappa > 0.

The global-better-across-barrier phase can be read either as a feedback window
at fixed interaction range or as an interaction-range window at fixed feedback.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt
from typing import Sequence


@dataclass(frozen=True)
class DimensionlessTriangularWindow:
    E: float
    contact_x: float
    g_on: float
    g_hi: float
    width: float


@dataclass(frozen=True)
class DimensionlessRangeWindow:
    g: float
    E_lower: float
    E_upper: float
    contact_x_upper: float
    width: float


def dimensionless_triangular_window(E: float) -> DimensionlessTriangularWindow:
    """Return the universal feedback window for ``0<E<1``."""
    e = float(E)
    if not isfinite(e) or not 0.0 < e < 1.0:
        raise ValueError("E must lie strictly in (0,1)")
    x = (3.0 - sqrt(9.0 - 8.0 * e)) / 2.0
    g_on = 1.0 / e - 1.0
    g_hi = (1.0 - x) * (3.0 - x) / (2.0 * x * x)
    width = g_hi - g_on
    if not (0.0 < x < e and width > 0.0):
        raise RuntimeError("dimensionless barrier branch left its admissible region")
    return DimensionlessTriangularWindow(e, x, g_on, g_hi, width)


def interaction_range_window_at_feedback(g: float) -> DimensionlessRangeWindow:
    """Return the exact ``E`` interval supporting the barrier at fixed ``g``.

    The ridge-onset inequality ``g > 1/E-1`` gives

        E > E_lower = 1/(1+g).

    The upper boundary solves ``g=g_hi``.  In the contact coordinate ``x`` this
    becomes

        (2g-1)x^2 + 4x - 3 = 0.

    For ``g=1/2`` the quadratic term vanishes and ``x=3/4``.  Otherwise the
    admissible root is

        x=[sqrt(1+6g)-2]/(2g-1).

    The corresponding interaction range is ``E=x(3-x)/2``.  Hence the barrier
    exists exactly for ``E_lower < E < E_upper``.
    """
    value = float(g)
    if not isfinite(value) or value <= 0.0:
        raise ValueError("g must be finite and positive")
    E_lower = 1.0 / (1.0 + value)
    if abs(2.0 * value - 1.0) < 1e-12:
        x = 0.75
    else:
        x = (sqrt(1.0 + 6.0 * value) - 2.0) / (2.0 * value - 1.0)
    E_upper = x * (3.0 - x) / 2.0
    if not (0.0 < E_lower < E_upper < 1.0 and 0.0 < x < 1.0):
        raise RuntimeError("fixed-feedback interaction-range branch left admissible region")
    return DimensionlessRangeWindow(
        g=value,
        E_lower=E_lower,
        E_upper=E_upper,
        contact_x_upper=x,
        width=E_upper - E_lower,
    )


def dimensionless_phase_curve(E_values: Sequence[float]) -> tuple[DimensionlessTriangularWindow, ...]:
    """Evaluate the universal feedback boundaries on declared interaction ranges."""
    return tuple(dimensionless_triangular_window(E) for E in E_values)


def near_intrinsic_optimum_asymptotic_ratios(E: float) -> tuple[float, float, float]:
    """Ratios approaching (1,2,1) as ``E -> 1-``."""
    row = dimensionless_triangular_window(E)
    d = 1.0 - row.E
    return row.g_on / d, row.g_hi / d, row.width / d


def narrow_range_asymptotic_ratios(E: float) -> tuple[float, float, float]:
    """Ratios approaching (1,27/8,27/8) as ``E -> 0+``."""
    row = dimensionless_triangular_window(E)
    return E * row.g_on, E * E * row.g_hi, E * E * row.width
