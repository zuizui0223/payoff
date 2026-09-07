"""Exact finite-panel phase decision trees with bounded-adversarial responses.

Each query is noninvasive, costs positive integer acquisition units, and can be
used once along a path. The parameter world is fixed throughout. The response
interval model is Cartesian across queries. This does NOT certify a continuous
parameter region, infer the biological kernel, or prove evolutionary trapping.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction as F
from functools import lru_cache
import json
from typing import Callable, Sequence

from .phase_observation_budget import (
    ArchitectureWorld, ContrastQuery, _integer, _panel, _queries, _response,
    plan_phase_observation_budget,
)
from .bounded_error_identification import _q


class PhaseSearchLimitError(RuntimeError):
    """Search was not completed; this is not evidence of nonidentifiability."""


@dataclass(frozen=True)
class PhaseResponseBranch:
    lower_exact: str
    upper_exact: str
    lower_closed: bool
    upper_closed: bool
    child: 'AdaptivePhaseNode'


@dataclass(frozen=True)
class AdaptivePhaseNode:
    query: str | None
    acquisition_cost: int
    remaining_world_names: tuple[str, ...]
    frozen_resident_barrier: bool | None
    branches: tuple[PhaseResponseBranch, ...]


@dataclass(frozen=True)
class AdaptivePhaseReceipt:
    status: str
    support_reference: str
    budget: int
    minimum_worst_case_cost: int | None
    minimum_fixed_resolving_cost: int | None
    worst_case_cost_saving: int | None
    optimal_first_queries: tuple[str, ...]
    selected_policy: AdaptivePhaseNode | None
    phase_by_world: dict[str, bool]
    inseparable_pair_witness: dict | None
    search_states: int
    scope: str = 'finite_panel_cartesian_bounded_errors_deterministic_adaptive_phase_identification'
    continuous_region_certified: bool = False
    mutation_radius_identified: bool = False


@dataclass(frozen=True)
class PhaseExecutionReceipt:
    observations_exact: tuple[tuple[str, str], ...]
    acquisition_cost: int
    remaining_world_names: tuple[str, ...]
    frozen_resident_barrier: bool
    continuous_region_certified: bool = False


def _response_cells(mask: int, intervals):
    """Partition the union into closed endpoints and open gaps, EXACTLY.

    Testing only interval interiors misses an adversary at touching endpoints.
    For every retained cell, the compatible-world mask is constant. Endpoints
    and rational midpoints form a complete finite representation, not a grid.
    """
    active = tuple(i for i in range(len(intervals)) if mask & (1 << i))
    ends = sorted({x for i in active for x in intervals[i]})
    cells = []
    for j, x in enumerate(ends):
        keep = sum(1 << i for i in active if intervals[i][0] <= x <= intervals[i][1])
        if keep:
            cells.append((x, x, True, True, keep))
        if j+1 < len(ends):
            y = ends[j+1]
            mid = (x+y)/2
            keep = sum(1 << i for i in active if intervals[i][0] <= mid <= intervals[i][1])
            if keep:
                cells.append((x, y, False, False, keep))
    return tuple(cells)


def plan_adaptive_phase_budget(
    worlds: Sequence[ArchitectureWorld], queries: Sequence[ContrastQuery], *,
    budget: int, support_reference: str, matched_contrasts_declared: bool,
    length: object = 1, max_search_states: int = 50_000,
) -> AdaptivePhaseReceipt:
    """Find the minimum WORST-PATH acquisition cost of exact panel phase recovery.

    All future observations remain hidden. The dynamic program minimizes
        C(S,R)=min_q [cost(q)+max_y C(S intersect compatible(q,y),R minus q)].
    C=0 when every retained world has the same target phase, and infinity when
    no allowed continuation resolves it. A response can be selected adversarially,
    but each nested nonempty support still contains a fixed compatible world.

    At most eight queries/64 worlds are supported. A state-cap exception never
    returns a spurious 'no design exists'. Costs are resource units, not payoff.
    The selected tree is emitted only when its worst path fits the given budget.
    """
    B = _integer(budget, 'budget')
    cap = _integer(max_search_states, 'max_search_states', 1)
    panel, pars, phases, L = _panel(worlds, length)
    qs = _queries(queries, L)
    if len(qs) > 8 or len(panel) > 64:
        raise ValueError('adaptive exact solver permits at most 8 queries and 64 worlds')
    if (not isinstance(support_reference, str) or not support_reference.strip()
            or matched_contrasts_declared is not True):
        raise ValueError('declare support provenance and matched contrasts')
    # Full-vocabulary pair coverage establishes whether ANY policy can succeed.
    # A fixed common response vector for an inseparable pair defeats every tree.
    fixed = plan_phase_observation_budget(panel, qs, budget=sum(q.cost for q in qs),
        support_reference=support_reference, matched_contrasts_declared=True, length=L)
    phases_by_name = dict(zip((w.name for w in panel), phases))
    intervals = tuple(tuple((_response(p, q.kind, q.coordinate)-_q(q.error_bound),
                             _response(p, q.kind, q.coordinate)+_q(q.error_bound))
                            for p in pars) for q in qs)
    if not fixed.optimal_bundles[0].guarantees_panel_phase:
        pair = next((i, j) for i in range(len(panel)) for j in range(i+1, len(panel))
                    if phases[i] != phases[j] and all(
                        max(iv[i][0], iv[j][0]) <= min(iv[i][1], iv[j][1]) for iv in intervals))
        i, j = pair
        vector = {q.name: str((max(iv[i][0], iv[j][0])+min(iv[i][1], iv[j][1]))/2)
                  for q, iv in zip(qs, intervals)}
        witness = {'world_names': (panel[i].name, panel[j].name),
                   'common_response_vector_for_entire_vocabulary': vector}
        return AdaptivePhaseReceipt('not_identifiable_with_declared_query_vocabulary',
            support_reference, B, None, None, None, (), None, phases_by_name, witness, 0)
    fixed_cost = fixed.optimal_bundles[0].cost
    count = {'states': 0}

    @lru_cache(None)
    def search(mask: int, remaining: int):
        count['states'] += 1
        if count['states'] > cap:
            raise PhaseSearchLimitError('adaptive phase search cap reached; no optimality conclusion')
        indices = tuple(i for i in range(len(panel)) if mask & (1 << i))
        support = tuple(panel[i].name for i in indices)
        targets = {phases[i] for i in indices}
        if len(targets) == 1:
            return 0, AdaptivePhaseNode(None, 0, support, next(iter(targets)), ()), ()
        best_cost, best_node, best_roots = None, None, []
        for j, q in enumerate(qs):
            if not remaining & (1 << j):
                continue
            cells = _response_cells(mask, intervals[j])
            if all(cell[4] == mask for cell in cells):
                continue
            child_by_mask = {cell[4]: search(cell[4], remaining ^ (1 << j)) for cell in cells}
            if any(solution[0] is None for solution in child_by_mask.values()):
                continue
            cost = q.cost+max(solution[0] for solution in child_by_mask.values())
            if best_cost is None or cost < best_cost:
                branches = tuple(PhaseResponseBranch(str(lo), str(hi), lc, uc, child_by_mask[keep][1])
                                 for lo, hi, lc, uc, keep in cells)
                best_cost = cost
                best_node = AdaptivePhaseNode(q.name, q.cost, support, None, branches)
                best_roots = [q.name]
            elif cost == best_cost:
                best_roots.append(q.name)
        return best_cost, best_node, tuple(best_roots)

    cost, node, first = search((1 << len(panel))-1, (1 << len(qs))-1)
    if cost is None or cost > fixed_cost:
        raise ArithmeticError('adaptive solver lost an available fixed resolving bundle')
    ready = cost <= B
    return AdaptivePhaseReceipt(
        'guaranteed_adaptive_panel_resolution' if ready else 'insufficient_budget_for_guaranteed_panel_resolution',
        support_reference, B, cost, fixed_cost, fixed_cost-cost, first,
        node if ready else None, phases_by_name, None, count['states'],
    )


def execute_phase_policy(receipt: AdaptivePhaseReceipt,
                         observe: Callable[[str], object]) -> PhaseExecutionReceipt:
    """Obtain only the selected response and follow its exact interval branch.

    Outside-support observations abort, rather than silently dropping the data.
    A rational/decimal-string response retains exact endpoints; a float retains
    its actual binary value. This routine does not operate a field instrument.
    """
    if receipt.selected_policy is None:
        raise ValueError('no affordable guaranteed phase policy is available')
    if not callable(observe):
        raise ValueError('observe must be a callable for the selected query')
    node, spent, trace = receipt.selected_policy, 0, []
    queried = set()
    while node.query is not None:
        if node.query in queried or node.acquisition_cost < 1 or spent+node.acquisition_cost > receipt.budget:
            raise ValueError('invalid policy: repeated query or pathwise budget violation')
        queried.add(node.query)
        value = _q(observe(node.query))
        matches = []
        for branch in node.branches:
            lo, hi = F(branch.lower_exact), F(branch.upper_exact)
            if ((value > lo or value == lo and branch.lower_closed)
                    and (value < hi or value == hi and branch.upper_closed)):
                matches.append(branch)
        if len(matches) != 1:
            raise ValueError('response contradicts the remaining panel or is not uniquely routed')
        trace.append((node.query, str(value)))
        spent += node.acquisition_cost
        node = matches[0].child
    if node.frozen_resident_barrier is None or spent > receipt.budget:
        raise ArithmeticError('invalid phase-policy terminal state or pathwise budget')
    return PhaseExecutionReceipt(tuple(trace), spent, node.remaining_world_names,
                                 node.frozen_resident_barrier)


def routing_witness():
    """Four ACTUAL quadratic/triangular worlds requiring three fixed, two adaptive queries."""
    worlds = (
        ArchitectureWorld('low_alpha_wide', '0.5', 1, F(16, 9), '0.4'),
        ArchitectureWorld('low_alpha_middle', '0.5', 1, 2, '0.3'),
        ArchitectureWorld('high_alpha_middle', '0.95', 1, 2, '0.3'),
        ArchitectureWorld('high_alpha_narrow', '0.95', 1, F(10, 3), '0.25'),
    )
    queries = (ContrastQuery('intrinsic_r_0.5', 'intrinsic', '0.5', '0.001'),
               ContrastQuery('interaction_d_0.2', 'interaction', '0.2', '0.001'),
               ContrastQuery('interaction_d_0.1', 'interaction', '0.1', '0.001'))
    return worlds, queries


def synthetic_example() -> dict:
    worlds, queries = routing_witness()
    receipt = plan_adaptive_phase_budget(worlds, queries, budget=2,
        support_reference='synthetic four-world exact triangular panel, not a continuous identified region',
        matched_contrasts_declared=True)
    trace = execute_phase_policy(receipt, {'intrinsic_r_0.5': F(1, 8),
                                         'interaction_d_0.2': F(2, 75)}.__getitem__)
    return {'data_kind': 'synthetic_quadratic_triangular_adaptive_witness',
            'plan': asdict(receipt), 'example_execution_not_field_data': asdict(trace)}


if __name__ == '__main__':
    print(json.dumps(synthetic_example(), indent=2, allow_nan=False))
