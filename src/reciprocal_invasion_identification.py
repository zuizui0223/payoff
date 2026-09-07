"""Identify PAYOFF phase and, conditionally, (phi, eta) from reciprocal invasion margins.

The two oriented margins are
    u = advantage of rare D in an S resident = phi-eta
    v = advantage of rare S in a D resident = -phi-eta.
Their SIGNS identify the strict deterministic phase without requiring a common
magnitude scale. Numerical reconstruction of phi and eta requires a common
positive payoff/growth scale across the two reciprocal assays.

Bands are simultaneous closed bounds. This module does not infer causation,
fixation, mutation support, or sister-program quantities.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from typing import Sequence


def _q(value: object) -> F:
    if isinstance(value, bool):
        raise ValueError("boolean is not a numeric bound")
    try:
        return F(value)
    except (TypeError, ValueError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError("bounds must be finite rational-compatible numbers") from exc


def _band(values: Sequence[object], name: str) -> tuple[F, F]:
    row = tuple(values)
    if len(row) != 2:
        raise ValueError(f"{name} requires exactly (lower, upper)")
    lo, hi = map(_q, row)
    if lo > hi:
        raise ValueError(f"{name} lower bound exceeds upper bound")
    return lo, hi


def _sign_state(lo: F, hi: F) -> str:
    if lo > 0:
        return "positive"
    if hi < 0:
        return "negative"
    if lo == hi == 0:
        return "zero"
    return "uncertain_or_boundary"


def _strict_phase(u: str, v: str) -> str | None:
    return {
        ("positive", "positive"): "stable_architecture_coexistence",
        ("negative", "negative"): "coordination_bistability",
        ("positive", "negative"): "differentiated_dominance",
        ("negative", "positive"): "shared_dominance",
    }.get((u, v))


@dataclass(frozen=True)
class ReciprocalInvasionReceipt:
    support_reference: str
    differentiated_into_shared_band_exact: tuple[str, str]
    shared_into_differentiated_band_exact: tuple[str, str]
    differentiated_into_shared_sign: str
    shared_into_differentiated_sign: str
    certified_strict_phase: str | None
    phase_certified_from_signs: bool
    common_scale_declared: bool
    phi_band_exact: tuple[str, str] | None
    eta_band_exact: tuple[str, str] | None
    phi_eta_vertices_exact: tuple[tuple[str, str], ...] | None
    eta_nonzero_certified: bool | None
    eta_sign_certified: str | None
    scope: str = "reciprocal_rare_invasion_closed_bands_deterministic_two_architecture_PAYOFF"
    finite_population_fixation_identified: bool = False
    mutation_support_identified: bool = False
    historical_causation_identified: bool = False


def identify_from_reciprocal_invasion(
    differentiated_into_shared_band: Sequence[object],
    shared_into_differentiated_band: Sequence[object],
    *,
    support_reference: str,
    resident_contexts_matched_declared: bool,
    common_scale_declared: bool,
) -> ReciprocalInvasionReceipt:
    """Return a strict phase certificate and optional canonical-coordinate bands.

    Positive `differentiated_into_shared` means rare D grows/earns more than S
    in an S-resident background. Positive `shared_into_differentiated` means rare
    S grows/earns more than D in a D-resident background. Assays must use the same
    external ecological context except for resident architecture.

    Phase identification needs only the two ORIENTED signs, so unknown separate
    positive scale multipliers do not matter. To reconstruct canonical magnitudes,
        phi=(u-v)/2, eta=-(u+v)/2,
    the two margins must be on one declared common positive scale.
    """
    if not isinstance(support_reference, str) or not support_reference.strip():
        raise ValueError("declare support provenance")
    if resident_contexts_matched_declared is not True:
        raise ValueError("declare matched reciprocal resident contexts")
    if type(common_scale_declared) is not bool:
        raise ValueError("common_scale_declared must be boolean")

    ul, uh = _band(differentiated_into_shared_band, "D-in-S band")
    vl, vh = _band(shared_into_differentiated_band, "S-in-D band")
    us, vs = _sign_state(ul, uh), _sign_state(vl, vh)
    phase = _strict_phase(us, vs)

    phi_band = eta_band = vertices = None
    eta_nonzero = None
    eta_sign = None
    if common_scale_declared:
        phi_lo, phi_hi = (ul-vh)/2, (uh-vl)/2
        eta_lo, eta_hi = -(uh+vh)/2, -(ul+vl)/2
        phi_band = (str(phi_lo), str(phi_hi))
        eta_band = (str(eta_lo), str(eta_hi))
        vertices = tuple((str((u-v)/2), str(-(u+v)/2))
                         for u in (ul, uh) for v in (vl, vh))
        eta_nonzero = eta_lo > 0 or eta_hi < 0
        eta_sign = "positive" if eta_lo > 0 else "negative" if eta_hi < 0 else None

    return ReciprocalInvasionReceipt(
        support_reference,
        (str(ul), str(uh)), (str(vl), str(vh)), us, vs,
        phase, phase is not None, common_scale_declared,
        phi_band, eta_band, vertices, eta_nonzero, eta_sign,
    )
