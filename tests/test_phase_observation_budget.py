from dataclasses import replace
from fractions import Fraction as F
from itertools import combinations, product
import random
import pytest

from src.phase_observation_budget import (
    ArchitectureWorld, ContrastQuery, condition_on_phase_bundle,
    plan_phase_observation_budget, retain_worlds_in_bands,
)


def worlds():
    return (ArchitectureWorld('barrier', '0.5', 1, 2, '0.3'),
            ArchitectureWorld('other', '0.5', 1, F(16, 9), '0.4'))


def plan(ws=None, qs=None, budget=1):
    return plan_phase_observation_budget(ws or worlds(), qs or (), budget=budget,
        support_reference='synthetic explicitly enumerated panel', matched_contrasts_declared=True)


def new_query(error='0.005', cost=1):
    return ContrastQuery('new', 'interaction', '0.3', error, cost)


def test_same_old_measurement_opposite_phase_and_new_measurement_resolves():
    r = plan(qs=(ContrastQuery('old', 'interaction', '0.1', '0.005'), new_query()))
    assert r.phase_by_world == {'barrier': True, 'other': False}
    assert r.separating_pairs_by_query['old'] == ()
    assert r.optimal_bundles[0].query_names == ('new',)
    assert r.status == 'guaranteed_panel_phase_resolution'
    assert not r.continuous_region_certified


def test_repeating_unchanged_distance_cannot_guarantee_resolution():
    qs = tuple(ContrastQuery(str(i), 'interaction', '0.1', '0.00001') for i in range(8))
    r = plan(qs=qs, budget=8)
    assert r.optimal_bundles[0].cost == 0
    assert r.ambiguity_witness['shared_possible_observation_vector'] == {}
    assert r.optimal_bundles[0].unresolved_cross_phase_pairs == 1


def test_touching_closed_response_intervals_are_not_separated():
    assert plan(qs=(new_query('0.02'),)).status.startswith('no_guaranteed')
    assert plan(qs=(new_query('0.019999'),)).status == 'guaranteed_panel_phase_resolution'


def test_budget_cannot_buy_unaffordable_query():
    assert plan(qs=(new_query(cost=2),), budget=1).optimal_bundles[0].query_names == ()
    assert plan(qs=(new_query(cost=2),), budget=2).optimal_bundles[0].query_names == ('new',)


def test_zero_budget_and_empty_vocabulary_are_not_absence():
    for qs in ((), (new_query(),)):
        r = plan(qs=qs, budget=0)
        assert not r.optimal_bundles[0].guarantees_panel_phase
        assert r.status.startswith('no_guaranteed')


def test_already_same_phase_needs_no_observation():
    r = plan(ws=worlds()[:1], qs=(new_query(),))
    assert r.status == 'panel_phase_already_identified'
    assert r.optimal_bundles[0].query_names == ()


def test_band_filter_uses_exact_old_response_and_does_not_claim_continuous_support():
    kept = retain_worlds_in_bands(worlds(), interaction_bands=[('0.1', F(1, 75), F(1, 75))])
    assert len(kept) == 2
    assert len(retain_worlds_in_bands(worlds(), interaction_bands=[('0.3', '0', '0.005')])) == 1
    with pytest.raises(ValueError, match='no supplied'):
        retain_worlds_in_bands(worlds(), interaction_bands=[('0.3', '1', '2')])


def test_selected_outcomes_retain_true_world_and_resolve_panel():
    r = condition_on_phase_bundle(worlds(), [new_query()], {'new': '0'})
    assert r['remaining_world_names'] == ('barrier',)
    assert r['frozen_resident_barrier'] is True
    r = condition_on_phase_bundle(worlds(), [new_query()], {'new': '0.04'})
    assert r['frozen_resident_barrier'] is False


def test_contradictory_or_unselected_outcomes_fail_closed():
    for response in ({'new': 99}, {}, {'new': 0, 'unselected': 0}):
        with pytest.raises(ValueError):
            condition_on_phase_bundle(worlds(), [new_query()], response)
    with pytest.raises(ValueError):
        condition_on_phase_bundle(worlds(), [], {})


def test_common_scale_requires_scaling_the_error_bounds_too():
    original = plan(qs=[new_query()])
    scaled = tuple(replace(w, alpha=F(w.alpha)*7, kappa=F(w.kappa)*7,
                           feedback_strength=F(w.feedback_strength)*7) for w in worlds())
    other = plan(ws=scaled, qs=[new_query(F('0.005')*7)])
    assert original.phase_by_world == other.phase_by_world
    assert original.optimal_bundles == other.optimal_bundles


@pytest.mark.parametrize('budget', [-1, True, 1.5])
def test_invalid_budgets_rejected(budget):
    with pytest.raises(ValueError):
        plan(budget=budget)


@pytest.mark.parametrize('query', [new_query(-1), new_query(cost=0),
    ContrastQuery('bad', 'unknown', '.2', 0), ContrastQuery('bad', 'intrinsic', 0, 0)])
def test_invalid_queries_rejected(query):
    with pytest.raises(ValueError):
        plan(qs=[query])


def test_duplicate_worlds_or_queries_rejected():
    with pytest.raises(ValueError, match='unique'):
        plan(ws=worlds()+worlds()[:1])
    with pytest.raises(ValueError, match='duplicate parameter'):
        plan(ws=worlds()+(replace(worlds()[0], name='duplicate'),))
    with pytest.raises(ValueError, match='unique'):
        plan(qs=[new_query(), new_query()])


def test_outside_registered_domain_rejected():
    with pytest.raises(ValueError):
        plan(ws=(replace(worlds()[0], epsilon='0.6'),))


def test_cartesian_observation_cells_independently_verify_pair_cover_theorem():
    # Exhaust all endpoints and open cells of the two observation axes.
    for e in (F(0), F('0.01'), F('0.02'), F('0.03')):
        qs = (new_query(e), ContrastQuery('far', 'interaction', '0.4', e))
        r = plan(qs=qs, budget=2)
        axes = []
        for q in qs:
            ys = [F(w.feedback_strength)*F(q.coordinate)**2*
                  max(F(0), 1-F(q.coordinate)/F(w.epsilon)) for w in worlds()]
            ends = sorted(set(y+s*e for y in ys for s in (-1, 1)))
            axes.append(ends+[(a+b)/2 for a,b in zip(ends,ends[1:])])
        ambiguous = False
        for vector in product(*axes):
            try:
                posterior = condition_on_phase_bundle(worlds(), qs, dict(zip((q.name for q in qs), vector)))
            except ValueError:
                continue
            ambiguous |= not posterior['panel_phase_identified']
        assert r.optimal_bundles[0].guarantees_panel_phase == (not ambiguous)


def test_seeded_finite_bundle_search_matches_independent_subset_enumeration():
    rng = random.Random(9037)
    for _ in range(30):
        qs = tuple(ContrastQuery(str(j), 'interaction', F(rng.randint(1, 40), 100),
                                 F(rng.randint(0, 20), 1000), rng.randint(1, 3)) for j in range(5))
        budget = rng.randint(0, 6)
        result = plan(qs=qs, budget=budget)
        expected = []
        for flags in product((0,1), repeat=len(qs)):
            selected = [q for q,flag in zip(qs,flags) if flag]
            cost = sum(q.cost for q in selected)
            if cost > budget:
                continue
            unresolved = 1
            for q in selected:
                d=F(q.coordinate)
                y=[F(w.feedback_strength)*d*d*max(F(0),1-d/F(w.epsilon)) for w in worlds()]
                if abs(y[0]-y[1])>2*F(q.error_bound): unresolved=0
            expected.append((unresolved,cost))
        assert (result.optimal_bundles[0].unresolved_cross_phase_pairs,
                result.optimal_bundles[0].cost)==min(expected)
