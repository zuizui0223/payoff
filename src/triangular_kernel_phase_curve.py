"""Dimensionless phase curve for the triangular-kernel accessibility barrier.

For an unconstrained intrinsic optimum ``r*=alpha/kappa``, define

    E = epsilon/r* in (0,1),
    g = G/kappa = -gamma/kappa.

The global-better-across-barrier phase is bounded by two universal curves that
depend only on E.
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


def dimensionless_triangular_window(E: float) -> DimensionlessTriangularWindow:
    """Return the universal feedback window for ``0<E<1``.

    The onset is

        g_on = 1/E - 1.

    At the upper boundary, eliminating feedback strength between stationarity
    and equal payoff gives

        x^2 - 3x + 2E = 0,

    with the admissible root

        x=(3-sqrt(9-8E))/2.

    Using ``E=x(3-x)/2`` simplifies the upper curve to

        g_hi=(1-x)(3-x)/(2x^2).
    """
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


def dimensionless_phase_curve(E_values: Sequence[float]) -> tuple[DimensionlessTriangularWindow, ...]:
    """Evaluate the universal barrier boundaries on declared interaction ranges."""
    return tuple(dimensionless_triangular_window(E) for E in E_values)


def near_intrinsic_optimum_asymptotic_ratios(E: float) -> tuple[float, float, float]:
    """Ratios approaching (1,2,1) as ``E -> 1-``.

    Returns ``g_on/(1-E)``, ``g_hi/(1-E)``, and ``width/(1-E)``.
    """
    row = dimensionless_triangular_window(E)
    d = 1.0 - row.E
    return row.g_on / d, row.g_hi / d, row.width / d


def narrow_range_asymptotic_ratios(E: float) -> tuple[float, float, float]:
    """Ratios approaching (1,27/8,27/8) as ``E -> 0+``.

    Returns ``E*g_on``, ``E^2*g_hi``, and ``E^2*width``.  The onset grows only
    as ``1/E``, so its contribution is lower order in the last ratio.
    """
    row = dimensionless_triangular_window(E)
    return E * row.g_on, E * E * row.g_hi, E * E * row.width
