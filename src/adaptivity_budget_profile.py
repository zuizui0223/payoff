"""Budget window in which adaptive PAYOFF phase design resolves before fixed bundles.

The finite-panel adaptive solver already returns the minimum worst-path adaptive
cost and minimum resolving fixed-bundle cost.  This module exposes their
budget-indexed implication without inventing probabilities or information bits.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .adaptive_phase_design import plan_adaptive_phase_budget
from .phase_observation_budget import ArchitectureWorld, ContrastQuery


@dataclass(frozen=True)
class PhaseBudgetRow:
    budget: int
    adaptive_guarantees_phase: bool
    fixed_bundle_guarantees_phase: bool
    adaptive_only_resolution: bool


@dataclass(frozen=True)
class PhaseAdaptivityBudgetProfile:
    minimum_adaptive_worst_path_cost: int | None
    minimum_fixed_resolving_cost: int | None
    cost_saving: int | None
    rows: tuple[PhaseBudgetRow, ...]
    adaptive_only_budgets: tuple[int, ...]
    scope: str = (
        "finite_panel_budget_window_from_exact_minimum_adaptive_and_fixed_"
        "phase_resolution_costs"
    )


def phase_adaptivity_budget_profile(
    worlds: Sequence[ArchitectureWorld],
    queries: Sequence[ContrastQuery],
    *,
    budgets: Sequence[int],
    support_reference: str,
    matched_contrasts_declared: bool,
    length: object = 1,
    max_search_states: int = 50_000,
) -> PhaseAdaptivityBudgetProfile:
    """Return budgets where adaptive routing resolves but no fixed bundle can.

    The costs are acquisition-resource units.  A positive window means only that
    the declared finite panel can be phase-resolved at a lower worst-path cost by
    an outcome-contingent tree.  It is not a sample-size recommendation or a
    continuous-region certificate.
    """
    values = tuple(budgets)
    if not values or any(type(b) is not int or b < 0 for b in values):
        raise ValueError("budgets must be a nonempty sequence of nonnegative integers")
    if len(set(values)) != len(values):
        raise ValueError("budgets must be unique")
    values = tuple(sorted(values))
    # The solver computes the minimum costs independently of affordability; use
    # the largest declared budget only to ensure a selected tree is emitted when
    # the adaptive optimum lies within the requested profile range.
    receipt = plan_adaptive_phase_budget(
        worlds,
        queries,
        budget=max(values),
        support_reference=support_reference,
        matched_contrasts_declared=matched_contrasts_declared,
        length=length,
        max_search_states=max_search_states,
    )
    adaptive_cost = receipt.minimum_worst_case_cost
    fixed_cost = receipt.minimum_fixed_resolving_cost
    rows = []
    for budget in values:
        adaptive = adaptive_cost is not None and budget >= adaptive_cost
        fixed = fixed_cost is not None and budget >= fixed_cost
        rows.append(PhaseBudgetRow(budget, adaptive, fixed, adaptive and not fixed))
    window = tuple(row.budget for row in rows if row.adaptive_only_resolution)
    saving = None if adaptive_cost is None or fixed_cost is None else fixed_cost - adaptive_cost
    return PhaseAdaptivityBudgetProfile(
        adaptive_cost, fixed_cost, saving, tuple(rows), window
    )
