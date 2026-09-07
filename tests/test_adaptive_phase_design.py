from dataclasses import replace
from fractions import Fraction as F
import pytest

from src.adaptive_phase_design import (
    PhaseSearchLimitError, _response_cells, plan_adaptive_phase_budget,
    execute_phase_policy, routing_witness,
)
from src.phase_observation_budget import ArchitectureWorld, ContrastQuery, _panel, _response


def plan(worlds=None, queries=None, **changes):
    base_worlds, base_queries = routing_witness()
    kwargs = dict(budget=2, support_reference='synthetic tests', matched_contrasts_declared=True)
    kwargs.update(changes)
    return plan_adaptive_phase_budget(base_worlds if worlds is None else worlds,
        base_queries if queries is None else queries, **kwargs)


def test_actual_triangular_worlds_need_three_fixed_but_two_adaptive_queries():
    r = plan()
    assert r.minimum_worst_case_cost == 2
    assert r.minimum_fixed_resolving_cost == 3
    assert r.worst_case_cost_saving == 1
    assert r.optimal_first_queries == ('intrinsic_r_0.5',)
    assert list(r.phase_by_world.values()) == [False, True, False, True]
    assert r.selected_policy.query == 'intrinsic_r_0.5'
    assert not r.continuous_region_certified
    assert not r.mutation_radius_identified


@pytest.mark.parametrize('world_index,error_fraction', [(i, e) for i in range(4) for e in (-1, 0, 1)])
def test_all_actual_worlds_and_closed_error_endpoints_follow_valid_two_query_path(world_index, error_fraction):
    worlds, queries = routing_witness()
    _, pars, _, _ = _panel(worlds, 1)
    requested = []
    lookup = {q.name: q for q in queries}
    def observe(name):
        requested.append(name)
        q = lookup[name]
        return _response(pars[world_index], q.kind, q.coordinate)+error_fraction*F(q.error_bound)
    r = plan()
    execution = execute_phase_policy(r, observe)
    assert execution.frozen_resident_barrier == r.phase_by_world[worlds[world_index].name]
    assert worlds[world_index].name in execution.remaining_world_names
    assert execution.acquisition_cost == 2
    assert requested[1] == ('interaction_d_0.2' if world_index < 2 else 'interaction_d_0.1')


def test_insufficient_budget_is_not_absent_identifiability():
    r = plan(budget=1)
    assert r.minimum_worst_case_cost == 2
    assert r.status.startswith('insufficient_budget')
    assert r.selected_policy is None
    with pytest.raises(ValueError, match='no affordable'):
        execute_phase_policy(r, lambda q: F(0))


def test_empty_vocabulary_has_constructive_inseparable_pair():
    r = plan(queries=())
    assert r.status == 'not_identifiable_with_declared_query_vocabulary'
    assert r.minimum_worst_case_cost is None
    a, b = r.inseparable_pair_witness['world_names']
    assert r.phase_by_world[a] != r.phase_by_world[b]
    assert r.inseparable_pair_witness['common_response_vector_for_entire_vocabulary'] == {}


def test_touching_closed_intervals_are_not_discriminated_by_any_policy():
    worlds, _ = routing_witness()
    qs = (ContrastQuery('touch', 'interaction', '0.3', '0.02'),)
    r = plan(worlds[:2], qs)
    assert r.minimum_worst_case_cost is None
    assert r.inseparable_pair_witness['common_response_vector_for_entire_vocabulary']['touch'] == '1/50'


def test_cell_partition_keeps_singleton_contact_separate_from_open_regions():
    cells = _response_cells(3, ((F(0), F(1)), (F(1), F(2))))
    assert (F(1), F(1), True, True, 3) in cells
    assert (F(0), F(1), False, False, 1) in cells
    assert (F(1), F(2), False, False, 2) in cells


def test_exact_cells_do_not_use_a_floating_observation_grid():
    d = F(1, 10**70)
    cells = _response_cells(3, ((F(1), F(1)+d), (F(1)+2*d, F(1)+3*d)))
    assert all(c[4] in (1, 2) for c in cells)
    assert any(c[0] == 1+2*d for c in cells)


def test_incompatible_actual_observation_aborts():
    with pytest.raises(ValueError, match='contradicts'):
        execute_phase_policy(plan(), lambda q: '999')


def test_uniform_phase_needs_zero_queries_and_no_callback():
    worlds, queries = routing_witness()
    r = plan((worlds[0], worlds[2]), queries, budget=0)
    assert r.minimum_worst_case_cost == 0
    execution = execute_phase_policy(r, lambda q: pytest.fail('no observation needed'))
    assert execution.frozen_resident_barrier is False
    assert execution.acquisition_cost == 0
    assert len(execution.remaining_world_names) == 2


def test_unknown_future_response_is_never_read():
    supplied = {'intrinsic_r_0.5': F(1, 8), 'interaction_d_0.2': F(2, 75)}
    r = execute_phase_policy(plan(), supplied.__getitem__)
    assert len(r.observations_exact) == 2
    assert r.frozen_resident_barrier


def test_common_scale_change_with_scaled_errors_preserves_design():
    worlds, qs = routing_witness()
    c = F(7, 3)
    scaled = tuple(replace(w, alpha=F(w.alpha)*c, kappa=F(w.kappa)*c,
                           feedback_strength=F(w.feedback_strength)*c) for w in worlds)
    scaled_q = tuple(replace(q, error_bound=F(q.error_bound)*c) for q in qs)
    r = plan(scaled, scaled_q)
    assert r.minimum_worst_case_cost == 2
    assert r.minimum_fixed_resolving_cost == 3
    assert r.phase_by_world == plan().phase_by_world


def test_unequal_costs_are_resource_units_not_payoff():
    worlds, qs = routing_witness()
    r = plan(worlds, tuple(replace(q, cost=2) for q in qs), budget=4)
    assert r.minimum_worst_case_cost == 4
    assert r.minimum_fixed_resolving_cost == 6


@pytest.mark.parametrize('changes', [
    {'budget': True}, {'budget': -1}, {'max_search_states': 0},
    {'matched_contrasts_declared': False}, {'support_reference': ''},
])
def test_invalid_contract_fails(changes):
    with pytest.raises(ValueError):
        plan(**changes)


def test_duplicate_world_or_query_rejected():
    worlds, qs = routing_witness()
    with pytest.raises(ValueError, match='unique'):
        plan(worlds+(worlds[0],), qs)
    with pytest.raises(ValueError, match='unique'):
        plan(worlds, qs+(qs[0],))


def test_search_cap_does_not_become_nonidentifiability_result():
    with pytest.raises(PhaseSearchLimitError, match='no optimality'):
        plan(max_search_states=1)


def test_negative_error_bound_rejected():
    worlds, qs = routing_witness()
    with pytest.raises(ValueError, match='negative'):
        plan(worlds, (replace(qs[0], error_bound=-1),)+qs[1:])


def test_adaptivity_saves_queries_but_cannot_overcome_exact_error_threshold():
    worlds, qs = routing_witness()
    critical = F(1, 300)
    below = tuple(replace(q, error_bound=critical-F(1, 10**9)) for q in qs)
    at = tuple(replace(q, error_bound=critical) for q in qs)
    assert plan(worlds, below).minimum_worst_case_cost == 2
    r = plan(worlds, at, budget=3)
    assert r.minimum_worst_case_cost is None
    assert r.status == 'not_identifiable_with_declared_query_vocabulary'


def test_routing_witness_is_robust_in_an_exact_parameter_neighbourhood():
    # This is a separate sufficient certificate for four DECLARED local boxes,
    # not a claim that the finite-panel API covers a data-identified continuum.
    from src.bounded_error_identification import _box_phase
    worlds, qs = routing_witness()
    rho = F(1, 10000)
    intervals = []
    for i, w in enumerate(worlds):
        a, k, g, e = map(F, (w.alpha, w.kappa, w.feedback_strength, w.epsilon))
        (al, ah), (kl, kh), (gl, gh), (el, eh) = [(x-rho, x+rho) for x in (a, k, g, e)]
        assert 0 < el < eh < al/kh and ah/kl < 1
        label = _box_phase((el*kl/ah, eh*kh/al), (gl/kh, gh/kl))
        assert label == ('certified_ridge_not_below_outside_optimum', 'certified_barrier',
                         'certified_no_ridge', 'certified_barrier')[i]
        ranges = []
        for q in qs:
            x, err = F(q.coordinate), F(q.error_bound)
            if q.kind == 'intrinsic':
                lo, hi = al*x-kh*x*x/2, ah*x-kl*x*x/2
            else:
                lo = gl*x*x*max(F(0), 1-x/el)
                hi = gh*x*x*max(F(0), 1-x/eh)
            ranges.append((lo-err, hi+err))
        intervals.append(ranges)
    # First query separates alpha groups throughout the entire four-box family.
    assert max(intervals[i][0][1] for i in (0, 1)) < min(intervals[i][0][0] for i in (2, 3))
    # The branch-specific second queries separate their targets throughout it.
    assert intervals[1][1][1] < intervals[0][1][0]
    assert intervals[2][2][1] < intervals[3][2][0]
    # The original inseparable pairs are contained in these boxes, retaining
    # the three-fixed-query lower bound, while the above bounds attain two.
