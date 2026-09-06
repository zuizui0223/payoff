"""Canonical PAYOFF coordinates for arbitrary symmetric 2x2 architecture games."""

from __future__ import annotations

from typing import Tuple


def canonical_parameters(a: float, b: float, d: float) -> Tuple[float, float]:
    """Return (phi,eta) for symmetric matrix [[a,b],[b,d]]."""

    return 0.5 * (d - a), 0.5 * (a + d - 2.0 * b)


def canonical_shifted_matrix(a: float, b: float, d: float) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """Return matrix after subtracting common payoff a from all entries."""

    phi, eta = canonical_parameters(a, b, d)
    return ((0.0, phi - eta), (phi - eta, 2.0 * phi))


def symmetric_pair_gap(p: float, a: float, b: float, d: float) -> float:
    """Return T-minus-S payoff gap at T frequency p."""

    if not 0.0 <= p <= 1.0:
        raise ValueError("p must lie in [0,1]")
    phi, eta = canonical_parameters(a, b, d)
    return phi + eta * (2.0 * p - 1.0)


def architecture_pair_parameters(
    intrinsic_s: float,
    intrinsic_t: float,
    h_ss: float,
    h_st: float,
    h_tt: float,
) -> Tuple[float, float]:
    """Return canonical parameters for A_ij=b_i+b_j+H_ij."""

    a = 2.0 * intrinsic_s + h_ss
    b = intrinsic_s + intrinsic_t + h_st
    d = 2.0 * intrinsic_t + h_tt
    return canonical_parameters(a, b, d)


def endpoint_margins(a: float, b: float, d: float) -> Tuple[float, float]:
    """Return (T_into_S, S_into_T) reciprocal rare-invasion margins."""

    # T into S = b-a; S into T = b-d.
    return b - a, b - d
