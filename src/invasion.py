"""Reciprocal invasion diagnostics for the PAYOFF architecture game."""

from __future__ import annotations

from typing import Tuple

from .numerical_tolerance import DEFAULT_RELATIVE_TOL, relative_band


def invasion_margins(phi: float, eta: float) -> Tuple[float, float]:
    """Return (D_into_S_margin, S_into_D_margin).

    Positive values mean the rare architecture can invade the resident state.
    """

    d_into_s = phi - eta
    s_into_d = -(phi + eta)
    return d_into_s, s_into_d


def identify_phi_eta(delta0: float, delta1: float) -> Tuple[float, float]:
    """Recover (phi, eta) from Delta(0) and Delta(1)."""

    phi = 0.5 * (delta0 + delta1)
    eta = 0.5 * (delta1 - delta0)
    return phi, eta


def invasion_regime(
    phi: float, eta: float, tol: float = DEFAULT_RELATIVE_TOL
) -> str:
    """Classify reciprocal invasion behavior under strict inequalities.

    ``tol`` is a dimensionless relative numerical tolerance.  Boundary
    detection is scaled to the two reciprocal invasion margins, so multiplying
    the entire payoff game by a positive constant cannot change the regime.
    """

    d_margin, s_margin = invasion_margins(phi, eta)
    band = relative_band((d_margin, s_margin), tol)
    if abs(d_margin) <= band or abs(s_margin) <= band:
        return "invasion_boundary"

    d_invades = d_margin > 0.0
    s_invades = s_margin > 0.0

    if d_invades and s_invades:
        return "mutual_invasion"
    if (not d_invades) and (not s_invades):
        return "mutual_noninvasion"
    if d_invades:
        return "differentiated_invasion_only"
    return "shared_invasion_only"
