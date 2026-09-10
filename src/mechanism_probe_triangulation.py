"""Preregistered triangulation for independent mechanism probes.

This Lane-A subgate prevents choosing the favorable result after observing two
predeclared mechanism probes.  It adjudicates only direct differentiation-
generation evidence.  It never promotes a matched-S architecture, a generic
game result, or an architecture-frequency claim.
"""
from __future__ import annotations

from dataclasses import dataclass

_ALLOWED = frozenset(("reduced", "material_reduction_excluded", "unresolved"))


@dataclass(frozen=True)
class MechanismProbeOutcome:
    probe_id: str
    support_reference: str
    generation_result: str
    direct_generation_measurement_declared: bool
    post_generation_realization_separated_declared: bool
    predeclared_primary_probe: bool

    @property
    def interpretable(self) -> bool:
        return all(
            (
                self.direct_generation_measurement_declared,
                self.post_generation_realization_separated_declared,
                self.predeclared_primary_probe,
            )
        )


@dataclass(frozen=True)
class MechanismTriangulationReceipt:
    primary_probe_ids: tuple[str, str]
    status: str
    interpretable_probe_count: int
    reduced_probe_count: int
    material_reduction_excluded_probe_count: int
    unresolved_probe_count: int
    mediator_generation_effect_triangulated: bool
    registered_route_not_supported: bool
    probe_discordance: bool
    matched_s_promoted: bool = False
    architecture_mapping_promoted: bool = False
    generic_game_promoted: bool = False
    architecture_frequency_claim_promoted: bool = False
    scope: str = "PAYOFF_preregistered_two_probe_mechanism_triangulation_v1"


def _nonempty(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def adjudicate_two_probe_triangulation(
    outcomes: tuple[MechanismProbeOutcome, MechanismProbeOutcome],
    *,
    primary_probe_ids: tuple[str, str],
) -> MechanismTriangulationReceipt:
    if len(outcomes) != 2 or len(primary_probe_ids) != 2:
        raise ValueError("exactly two primary probes are required")
    if len(set(primary_probe_ids)) != 2:
        raise ValueError("primary probe ids must be distinct")

    by_id = {}
    for outcome in outcomes:
        probe_id = _nonempty(outcome.probe_id, "probe_id")
        _nonempty(outcome.support_reference, "support_reference")
        if outcome.generation_result not in _ALLOWED:
            raise ValueError("unsupported generation_result")
        if probe_id in by_id:
            raise ValueError("duplicate probe outcome")
        by_id[probe_id] = outcome

    if set(by_id) != set(primary_probe_ids):
        raise ValueError("outcomes must match the predeclared primary probe ids")

    effective = []
    for probe_id in primary_probe_ids:
        outcome = by_id[probe_id]
        # An unqualified measurement never gets interpreted in a favorable way.
        effective.append(outcome.generation_result if outcome.interpretable else "unresolved")

    reduced = sum(x == "reduced" for x in effective)
    excluded = sum(x == "material_reduction_excluded" for x in effective)
    unresolved = sum(x == "unresolved" for x in effective)
    interpretable = 2 - unresolved

    if reduced == 2:
        status = "TRIANGULATED_MEDIATOR_GENERATION_REDUCTION"
        triangulated = True
        route_not_supported = False
        discordance = False
    elif excluded == 2:
        status = "REGISTERED_MEDIATOR_ROUTE_NOT_SUPPORTED"
        triangulated = False
        route_not_supported = True
        discordance = False
    elif reduced == 1 and excluded == 1:
        status = "PROBE_DISCORDANCE_MECHANISM_UNRESOLVED"
        triangulated = False
        route_not_supported = False
        discordance = True
    else:
        status = "INCOMPLETE_OR_UNRESOLVED_TRIANGULATION"
        triangulated = False
        route_not_supported = False
        discordance = False

    return MechanismTriangulationReceipt(
        primary_probe_ids=primary_probe_ids,
        status=status,
        interpretable_probe_count=interpretable,
        reduced_probe_count=reduced,
        material_reduction_excluded_probe_count=excluded,
        unresolved_probe_count=unresolved,
        mediator_generation_effect_triangulated=triangulated,
        registered_route_not_supported=route_not_supported,
        probe_discordance=discordance,
    )
