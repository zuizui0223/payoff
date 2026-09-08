"""Set-valued phase identification from reciprocal invasion sign evidence.

This is the qualitative companion to reciprocal_invasion_identification.py.
It is intended for evidence such as published directional tests where one
oriented invasion sign may be certified while the other remains unresolved.
No numerical payoff magnitude, phi, eta, fixation, or causal mechanism is
identified from sign categories alone.
"""
from __future__ import annotations

from dataclasses import dataclass


_STRICT_PHASE = {
    ("positive", "positive"): "stable_architecture_coexistence",
    ("negative", "negative"): "coordination_bistability",
    ("positive", "negative"): "differentiated_dominance",
    ("negative", "positive"): "shared_dominance",
}
_ALL_STRICT_PHASES = tuple(sorted(set(_STRICT_PHASE.values())))
_ALLOWED = frozenset(("positive", "negative", "zero", "unresolved"))
_EXPANSION = {
    "positive": ("positive",),
    "negative": ("negative",),
    "zero": ("zero",),
    "unresolved": ("negative", "zero", "positive"),
}


@dataclass(frozen=True)
class ReciprocalSignPartialReceipt:
    support_reference: str
    differentiated_into_shared_sign_evidence: str
    shared_into_differentiated_sign_evidence: str
    compatible_strict_phases: tuple[str, ...]
    excluded_strict_phases: tuple[str, ...]
    boundary_compatible: bool
    strict_phase_certified: bool
    certified_strict_phase: str | None
    numerical_phi_eta_identified: bool = False
    finite_population_fixation_identified: bool = False
    historical_causation_identified: bool = False
    scope: str = "qualitative_reciprocal_invasion_sign_partial_identification"


def _state(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a sign-evidence string")
    value = value.strip().lower()
    if value not in _ALLOWED:
        raise ValueError(
            f"{name} must be one of positive, negative, zero, unresolved"
        )
    return value


def identify_phase_from_sign_evidence(
    differentiated_into_shared_sign_evidence: str,
    shared_into_differentiated_sign_evidence: str,
    *,
    support_reference: str,
) -> ReciprocalSignPartialReceipt:
    """Return all strict PAYOFF phases still compatible with oriented sign evidence.

    `unresolved` means the evidence does not certify positive, negative, or exact
    zero. It therefore expands to all three logical possibilities. `zero` is an
    exact boundary statement and is not treated as a strict phase.
    """
    if not isinstance(support_reference, str) or not support_reference.strip():
        raise ValueError("declare support provenance")

    u = _state(
        differentiated_into_shared_sign_evidence,
        "differentiated_into_shared_sign_evidence",
    )
    v = _state(
        shared_into_differentiated_sign_evidence,
        "shared_into_differentiated_sign_evidence",
    )

    compatible = set()
    boundary = False
    for us in _EXPANSION[u]:
        for vs in _EXPANSION[v]:
            if "zero" in (us, vs):
                boundary = True
                continue
            compatible.add(_STRICT_PHASE[(us, vs)])

    compatible_tuple = tuple(sorted(compatible))
    excluded = tuple(p for p in _ALL_STRICT_PHASES if p not in compatible)
    certified = len(compatible_tuple) == 1 and not boundary

    return ReciprocalSignPartialReceipt(
        support_reference=support_reference.strip(),
        differentiated_into_shared_sign_evidence=u,
        shared_into_differentiated_sign_evidence=v,
        compatible_strict_phases=compatible_tuple,
        excluded_strict_phases=excluded,
        boundary_compatible=boundary,
        strict_phase_certified=certified,
        certified_strict_phase=compatible_tuple[0] if certified else None,
    )
