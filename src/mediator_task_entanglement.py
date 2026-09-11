"""Lane-A gate for mediator perturbations that also alter the focal biological task.

A perturbation can be an informative mechanism probe without being a valid
matched architecture counterfactual.  This module asks only whether the focal
net task is matched independently enough to allow downstream architecture
comparison.  It never promotes Lane G, eta, or E1.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MediatorTaskEntanglementReceipt:
    system_id: str
    mediator_id: str
    perturbation_id: str
    focal_task_id: str
    support_reference: str
    perturbation_changes_mediator_declared: bool
    perturbation_changes_focal_task_output_declared: bool
    task_directly_preserved_declared: bool
    separation_of_function_intervention_declared: bool
    separation_of_function_preserves_task_declared: bool
    orthogonal_task_rescue_declared: bool
    orthogonal_task_rescue_verified_declared: bool
    rescue_independent_of_generation_path_declared: bool
    same_mediator_addback_only_declared: bool
    task_assay_same_context_declared: bool
    task_match_defined_before_game_outcome_declared: bool
    task_match_independent_of_frequency_game_declared: bool


@dataclass(frozen=True)
class MediatorTaskEntanglementAdjudication:
    mediator_task_entangled: bool
    direct_task_preservation_qualified: bool
    separation_of_function_qualified: bool
    orthogonal_rescue_qualified: bool
    task_match_qualified: bool
    blockers: tuple[str, ...]
    matched_s_promoted: bool = False
    architecture_mapping_promoted: bool = False
    generic_game_promoted: bool = False
    eta_identified: bool = False
    e1_promoted: bool = False
    scope: str = "PAYOFF_mediator_task_entanglement_gate_v1"


def _nonempty(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def adjudicate_mediator_task_entanglement(
    receipt: MediatorTaskEntanglementReceipt,
) -> MediatorTaskEntanglementAdjudication:
    for name in (
        "system_id",
        "mediator_id",
        "perturbation_id",
        "focal_task_id",
        "support_reference",
    ):
        _nonempty(getattr(receipt, name), name)

    if not receipt.task_match_defined_before_game_outcome_declared:
        raise ValueError("task matching must be defined before Lane G outcome")
    if not receipt.task_match_independent_of_frequency_game_declared:
        raise ValueError("task matching must be independent of frequency-game result")
    if receipt.same_mediator_addback_only_declared and receipt.orthogonal_task_rescue_declared:
        raise ValueError("same-mediator add-back cannot be declared orthogonal rescue")

    entangled = (
        receipt.perturbation_changes_mediator_declared
        and receipt.perturbation_changes_focal_task_output_declared
    )

    direct = (
        receipt.task_directly_preserved_declared
        and receipt.task_assay_same_context_declared
        and not receipt.perturbation_changes_focal_task_output_declared
    )
    separation = all(
        (
            receipt.separation_of_function_intervention_declared,
            receipt.separation_of_function_preserves_task_declared,
            receipt.task_assay_same_context_declared,
        )
    )
    orthogonal = all(
        (
            receipt.orthogonal_task_rescue_declared,
            receipt.orthogonal_task_rescue_verified_declared,
            receipt.rescue_independent_of_generation_path_declared,
            receipt.task_assay_same_context_declared,
            not receipt.same_mediator_addback_only_declared,
        )
    )
    qualified = direct or separation or orthogonal

    blockers: list[str] = []
    if not receipt.task_assay_same_context_declared:
        blockers.append("TASK_ASSAY_CONTEXT_NOT_MATCHED")
    if entangled and not qualified:
        blockers.append("MEDIATOR_AND_TASK_OUTPUT_ENTANGLED")
    if not direct and not separation and not orthogonal:
        blockers.append("NO_QUALIFIED_TASK_MATCH_ROUTE")
    if receipt.same_mediator_addback_only_declared:
        blockers.append("SAME_MEDIATOR_ADDBACK_NOT_ORTHOGONAL")
    if receipt.orthogonal_task_rescue_declared and not receipt.orthogonal_task_rescue_verified_declared:
        blockers.append("ORTHOGONAL_TASK_RESCUE_NOT_VERIFIED")
    if receipt.orthogonal_task_rescue_declared and not receipt.rescue_independent_of_generation_path_declared:
        blockers.append("RESCUE_INDEPENDENCE_FROM_GENERATION_PATH_NOT_VERIFIED")
    if receipt.separation_of_function_intervention_declared and not receipt.separation_of_function_preserves_task_declared:
        blockers.append("SEPARATION_OF_FUNCTION_TASK_PRESERVATION_NOT_VERIFIED")

    return MediatorTaskEntanglementAdjudication(
        mediator_task_entangled=entangled,
        direct_task_preservation_qualified=direct,
        separation_of_function_qualified=separation,
        orthogonal_rescue_qualified=orthogonal,
        task_match_qualified=qualified,
        blockers=tuple(dict.fromkeys(blockers)),
    )
