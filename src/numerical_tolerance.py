"""Shared scale-relative numerical tolerance helpers for PAYOFF."""

from __future__ import annotations

from math import isfinite
from sys import float_info
from typing import Iterable


DEFAULT_RELATIVE_TOL = 64.0 * float_info.epsilon


def relative_band(values: Iterable[float], tol: float = DEFAULT_RELATIVE_TOL) -> float:
    """Return a roundoff band relative to the supplied commensurate values.

    ``tol`` is dimensionless.  No physical-unit floor is introduced: if every
    supplied value is exactly zero, the returned band is exactly zero.
    """

    tol = float(tol)
    if not isfinite(tol) or tol < 0.0:
        raise ValueError("tol must be finite and non-negative")
    numeric = tuple(float(value) for value in values)
    if not numeric:
        return 0.0
    if not all(isfinite(value) for value in numeric):
        raise ValueError("numerical comparison values must be finite")
    return tol * max(abs(value) for value in numeric)
