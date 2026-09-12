"""Govern the first qualified direct-mu D-reference milestone.

This gate does not replace the full reference-panel qualification. It prevents
PAYOFF from treating literature-candidate accumulation as progress while the
realization channel still has zero qualified matched-D references, and it makes
one qualified D reference a necessary (not sufficient) precondition for any
architecture-specific inference.
"""
from __future__ import annotations

from dataclasses import dataclass


_PRIORITY_QUEUE = ("M5_T0", "W3_POST_DELETION", "M1_T0")
_TERMINAL_STATES = frozenset({"TERMINALLY_INACCESSIBLE", "FINAL_QUALIFICATION_FAILURE"})
_ACTIONABLE_STATES = frozenset({
    "NOT_STARTED",
    "STOCK_ACCESS_PENDING",
    "MARKER_QUALIFICATION_PENDING",
    "REALIZATION_ASSAY_PENDING",
    "QUALIFICATION_PENDING",
})


@dataclass(frozen=True)
class FirstReferenceGateInput:
    qualified_d_reference_count: int
    primary_target_id: str
    m5_state: str
    w3_state: str
    m1_state: str
    direct_mu_outcome_available: bool
    matched_s_certified: bool
    architecture_mapping_certified: bool


@dataclass(frozen=True)
class FirstReferenceGateResult:
    first_qualified_reference_recovered: bool
    candidate_literature_expansion_paused: bool
    candidate_search_restart_licensed: bool
    minimum_d_reference_precondition_satisfied: bool
    architecture_specific_inference_hard_closed: bool
    next_action: str
    blockers: tuple[str, ...]


def _validate_count(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError("qualified_d_reference_count must be a non-negative integer")
    return value


def _validate_state(value: str, name: str) -> str:
    if value not in (_TERMINAL_STATES | _ACTIONABLE_STATES | {"QUALIFIED"}):
        raise ValueError(f"{name} has unregistered state {value!r}")
    return value


def adjudicate_first_reference_gate(inp: FirstReferenceGateInput) -> FirstReferenceGateResult:
    count = _validate_count(inp.qualified_d_reference_count)
    if inp.primary_target_id not in _PRIORITY_QUEUE:
        raise ValueError("primary_target_id must come from the frozen M5 -> W3 -> M1 queue")

    states = {
        "M5_T0": _validate_state(inp.m5_state, "m5_state"),
        "W3_POST_DELETION": _validate_state(inp.w3_state, "w3_state"),
        "M1_T0": _validate_state(inp.m1_state, "m1_state"),
    }

    first_recovered = count >= 1
    queue_exhausted = all(states[target] in _TERMINAL_STATES for target in _PRIORITY_QUEUE)
    search_restart = (not first_recovered) and queue_exhausted
    candidate_paused = (not first_recovered) and (not queue_exhausted)

    minimum_precondition = first_recovered
    architecture_specific_hard_closed = not (
        minimum_precondition
        and inp.direct_mu_outcome_available
        and inp.matched_s_certified
        and inp.architecture_mapping_certified
    )

    blockers: list[str] = []
    if not first_recovered:
        blockers.append("ZERO_QUALIFIED_MATCHED_D_REFERENCES")
    if not inp.direct_mu_outcome_available:
        blockers.append("DIRECT_MU_OUTCOME_UNAVAILABLE")
    if not inp.matched_s_certified:
        blockers.append("MATCHED_S_NOT_CERTIFIED")
    if not inp.architecture_mapping_certified:
        blockers.append("ARCHITECTURE_MAPPING_NOT_CERTIFIED")
    if candidate_paused:
        blockers.append("CANDIDATE_LITERATURE_EXPANSION_PAUSED_WHILE_PRIORITY_QUEUE_ACTIONABLE")

    if first_recovered:
        next_action = "CONTINUE_REGISTERED_REFERENCE_PANEL_AND_MATCHED_S_ARCHITECTURE_GATES"
    elif queue_exhausted:
        next_action = "RESUME_BOUNDED_D_REFERENCE_SEARCH"
    else:
        for target in _PRIORITY_QUEUE:
            if states[target] not in _TERMINAL_STATES:
                next_action = f"MATERIALIZE_AND_QUALIFY_{target}"
                break
        else:  # defensive; queue_exhausted would already be true
            next_action = "RESUME_BOUNDED_D_REFERENCE_SEARCH"

    return FirstReferenceGateResult(
        first_qualified_reference_recovered=first_recovered,
        candidate_literature_expansion_paused=candidate_paused,
        candidate_search_restart_licensed=search_restart,
        minimum_d_reference_precondition_satisfied=minimum_precondition,
        architecture_specific_inference_hard_closed=architecture_specific_hard_closed,
        next_action=next_action,
        blockers=tuple(blockers),
    )
