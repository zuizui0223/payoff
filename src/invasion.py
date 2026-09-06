"""Reciprocal invasion diagnostics for the PAYOFF architecture game."""

from __future__ import annotations

from typing import Tuple


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


def invasion_regime(phi: float, eta: float, tol: float = 1e-12) -> str:
    """Classify reciprocal invasion behavior under strict inequalities."""

    d_margin, s_margin = invasion_margins(phi, eta)
    if abs(d_margin) <= tol or abs(s_margin) <= tol:
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
