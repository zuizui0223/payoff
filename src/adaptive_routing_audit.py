"""Structural routing audit for adaptive finite-panel PAYOFF phase designs.

PAYOFF's bounded-adversarial finite-panel design does not assign probabilities to
worlds or responses.  This module therefore does NOT invent Shannon bits.  It
records whether the first response changes the immediate continuation query and
whether that branch dependence accompanies a worst-path acquisition saving.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .adaptive_phase_design import AdaptivePhaseReceipt, plan_adaptive_phase_budget
from .phase_observation_budget import ArchitectureWorld, ContrastQuery


@dataclass(frozen=True)
class PhaseRoutingBranch:
    lower_exact: str
    upper_exact: str
    lower_closed: bool
    upper_closed: bool
    next_query: str
    remaining_world_names: tuple[str, ...]
    phase_already_resolved: bool


@dataclass(frozen=True)
class PhaseRoutingAudit:
    status: str
    root_query: str | None
    branches: tuple[PhaseRoutingBranch, ...]
    distinct_next_actions: tuple[str, ...]
    branch_dependent_continuation: bool
    root_alone_resolves_phase_on_every_outcome: bool
    adaptive_worst_case_cost_saving: int | None
    routing_without_direct_phase_resolution: bool
    adaptive_receipt: AdaptivePhaseReceipt
    scope: str = (
        "finite_panel_set_valued_branch_routing_audit_no_world_probabilities_"
        "no_continuous_region_certificate"
    )


def audit_adaptive_phase_routing(
    worlds: Sequence[ArchitectureWorld],
    queries: Sequence[ContrastQuery],
    *,
    budget: int,
    support_reference: str,
    matched_contrasts_declared: bool,
    length: object = 1,
    max_search_states: int = 50_000,
) -> PhaseRoutingAudit:
    """Report whether root outcomes require different continuation measurements.

    ``__stop__`` is treated as a continuation action.  A routing witness requires
    three separate facts:

    1. at least two possible root outcomes lead to different immediate next
       actions;
    2. the root alone does not resolve phase on every outcome;
    3. the exact adaptive solver saves positive worst-path acquisition cost over
       the minimum resolving fixed bundle.

    This is a structural finite-panel statement, not target information in bits.
    """
    receipt = plan_adaptive_phase_budget(
        worlds,
        queries,
        budget=budget,
        support_reference=support_reference,
        matched_contrasts_declared=matched_contrasts_declared,
        length=length,
        max_search_states=max_search_states,
    )
    root = receipt.selected_policy
    if root is None or root.query is None:
        return PhaseRoutingAudit(
            "no_affordable_nonterminal_selected_root",
            None,
            (),
            (),
            False,
            False,
            receipt.worst_case_cost_saving,
            False,
            receipt,
        )

    rows = []
    for branch in root.branches:
        child = branch.child
        next_action = child.query if child.query is not None else "__stop__"
        rows.append(PhaseRoutingBranch(
            branch.lower_exact,
            branch.upper_exact,
            branch.lower_closed,
            branch.upper_closed,
            next_action,
            child.remaining_world_names,
            child.frozen_resident_barrier is not None,
        ))
    actions = tuple(sorted({row.next_query for row in rows}))
    branch_dependent = len(actions) > 1
    root_resolves = bool(rows) and all(row.phase_already_resolved for row in rows)
    saving = receipt.worst_case_cost_saving
    routing = branch_dependent and not root_resolves and saving is not None and saving > 0
    return PhaseRoutingAudit(
        "phase_routing_audit_complete",
        root.query,
        tuple(rows),
        actions,
        branch_dependent,
        root_resolves,
        saving,
        routing,
        receipt,
    )
