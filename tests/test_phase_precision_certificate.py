"""Independent interval oracle plus production-adapter precision/cost regressions."""
from dataclasses import replace
from fractions import Fraction as F
from itertools import product
import random

import pytest

from src.phase_precision_certificate import (
    _certificate_from_responses, certify_phase_precision,
)


def core(rows=((0, 1),), errors=(1,), phases=(False, True)):
    return _certificate_from_responses(
        tuple(f"w{i}" for i in range(len(phases))), phases,
        tuple(f"q{i}" for i in range(len(rows))), rows, errors,
        support_reference="synthetic_test_panel",
    )


def interval_oracle(rows, errors, phases, scale):
    """Enumerate compatible masks for every exact response cell, not ratios."""
    n = len(phases)
    retained = {(1 << n) - 1}
    for row, error in zip(rows, errors):
        intervals = tuple((F(y)-scale*error, F(y)+scale*error) for y in row)
        ends = sorted({v for band in intervals for v in band})
        probes = ends + [(a+b)/2 for a, b in zip(ends, ends[1:])]
        masks = {sum(1 << i for i, (lo, hi) in enumerate(intervals) if lo <= y <= hi)
                 for y in probes}
        retained = {old & mask for old in retained for mask in masks if old & mask}
    return all(len({phases[i] for i in range(n) if mask & (1 << i)}) == 1
               for mask in retained)


def test_touching_closed_intervals_fail_exactly_at_limit():
    receipt = core()
    assert receipt.critical_error_scale_exact == "1/2"
    assert receipt.identifiable_at_error_scale(F(1, 2)-F(1, 10**12))
    assert not receipt.identifiable_at_error_scale(F(1, 2))
    assert not receipt.identifiable_at_error_scale(1)
    assert receipt.common_response_at_critical == {"q0": "1/2"}
    assert receipt.blocking_pair == ("w0", "w1")
    assert not receipt.identifiable_at_declared_errors


def test_zero_error_queries_and_identical_exact_responses():
    receipt = core(((0, 1),), (0,))
    assert receipt.critical_error_scale_exact is None
    assert receipt.status == "unbounded_finite_error_scale_tolerance"
    assert receipt.identifiable_at_error_scale(10**12)
    assert receipt.blocking_pair is None
    assert receipt.common_response_at_critical is None
    identical = core(((1, 1),), (0,))
    assert identical.critical_error_scale_exact == "0"
    assert not identical.identifiable_at_error_scale(0)
    assert identical.status == "not_identifiable_even_at_zero_error"


def test_empty_vocabulary_and_constant_phase_are_distinguished():
    mixed = core((), (), (False, True))
    assert mixed.critical_error_scale_exact == "0"
    assert mixed.common_response_at_critical == {}
    assert not mixed.identifiable_at_error_scale(0)
    single = core((), (), (True, True))
    assert single.critical_error_scale_exact is None
    assert single.status == "panel_phase_already_identified"
    assert single.cross_phase_pair_count == 0
    assert single.identifiable_at_error_scale(10**12)


def test_infinitely_resolvable_pair_does_not_hide_finite_bottleneck():
    receipt = core(((0, 1, 1), (0, 0, 2)), (0, 1), (False, True, False))
    assert receipt.critical_error_scale_exact == "1"
    assert receipt.blocking_pair == ("w1", "w2")
    assert receipt.pair_limits[0].critical_error_scale_exact is None
    assert receipt.pair_limits[1].critical_error_scale_exact == "1"
    assert receipt.pair_limits[1].maximizing_queries == ("q1",)


def test_declared_errors_are_exactly_scale_one():
    assert core(((0, 3),), (1,)).identifiable_at_declared_errors
    assert not core(((0, 2),), (1,)).identifiable_at_declared_errors
    assert core(((0, 3),), (1,)).identifiable_at_error_scale("1.0")


@pytest.mark.parametrize("scale", [True, False, -1, "-1/100", "nan", "inf", float("nan"), None])
def test_invalid_scales_are_rejected(scale):
    with pytest.raises(ValueError):
        core().identifiable_at_error_scale(scale)


@pytest.mark.parametrize("kwargs", [
    {"world_names": ()}, {"world_names": ("a", "a")},
    {"world_names": ("", "b")}, {"phases": (0, 1)},
    {"phases": (True,)}, {"query_names": ("",)},
    {"query_names": ("q", "q")}, {"response_rows": ((0,),)},
    {"error_bounds": (-1,)}, {"error_bounds": (True,)},
    {"error_bounds": ("nan",)}, {"support_reference": " "},
])
def test_invalid_response_panels_are_rejected(kwargs):
    arguments = dict(world_names=("a", "b"), phases=(False, True),
                     query_names=("q",), response_rows=((0, 1),),
                     error_bounds=(1,), support_reference="synthetic")
    arguments.update(kwargs)
    with pytest.raises(ValueError):
        _certificate_from_responses(**arguments)


def test_random_response_panels_match_exhaustive_interval_oracle():
    rng = random.Random(202609071)
    for _ in range(120):
        n, m = rng.randint(2, 5), rng.randint(0, 3)
        phases = tuple(bool(rng.randrange(2)) for _ in range(n))
        rows = tuple(tuple(F(rng.randrange(-5, 6), 3) for _ in range(n))
                     for _ in range(m))
        errors = tuple(F(rng.randrange(0, 4), 5) for _ in range(m))
        receipt = core(rows, errors, phases)
        scales = {F(0), F(1), F(10)}
        if receipt.critical_error_scale_exact is not None:
            limit = F(receipt.critical_error_scale_exact)
            scales.update((limit/2, limit, limit+1))
        for scale in scales:
            assert receipt.identifiable_at_error_scale(scale) == interval_oracle(
                rows, errors, phases, scale)
        if receipt.blocking_pair is not None:
            i, j = (int(w[1:]) for w in receipt.blocking_pair)
            assert phases[i] != phases[j]
            limit = F(receipt.critical_error_scale_exact)
            for q, (row, e) in enumerate(zip(rows, errors)):
                shared = F(receipt.common_response_at_critical[f"q{q}"])
                assert abs(shared-row[i]) <= limit*e
                assert abs(shared-row[j]) <= limit*e


def test_precision_radius_is_monotone_under_error_and_vocabulary_changes():
    baseline = core(((0, 1),), (1,))
    noisier = core(((0, 1),), (2,))
    extra = core(((0, 1), (0, 4)), (1, 1))
    assert F(noisier.critical_error_scale_exact) <= F(baseline.critical_error_scale_exact)
    assert F(extra.critical_error_scale_exact) >= F(baseline.critical_error_scale_exact)


def witness():
    from src.phase_observation_budget import ArchitectureWorld, ContrastQuery
    worlds = (
        ArchitectureWorld("low_alpha_wide", "1/2", 1, "16/9", "2/5"),
        ArchitectureWorld("low_alpha_middle", "1/2", 1, 2, "3/10"),
        ArchitectureWorld("high_alpha_middle", "19/20", 1, 2, "3/10"),
        ArchitectureWorld("high_alpha_narrow", "19/20", 1, "10/3", "1/4"),
    )
    queries = (
        ContrastQuery("B_half", "intrinsic", "1/2", "1/1000"),
        ContrastQuery("A_fifth", "interaction", "1/5", "1/1000"),
        ContrastQuery("A_tenth", "interaction", "1/10", "1/1000"),
    )
    return worlds, queries


def certify(worlds, queries, **kwargs):
    return certify_phase_precision(worlds, queries,
        support_reference="synthetic_regression", matched_contrasts_declared=True, **kwargs)


def optimize(worlds, queries):
    from src.adaptive_phase_design import plan_adaptive_phase_budget
    return plan_adaptive_phase_budget(worlds, queries, budget=sum(q.cost for q in queries),
        support_reference="synthetic_regression", matched_contrasts_declared=True)


def test_integration_registered_worlds_have_exact_precision_limit():
    worlds, queries = witness()
    receipt = certify(worlds, queries)
    assert tuple(receipt.phase_by_world.values()) == (False, True, False, True)
    assert receipt.critical_error_scale_exact == "10/3"
    assert receipt.blocking_pair == ("high_alpha_middle", "high_alpha_narrow")
    assert receipt.common_response_at_critical == {
        "B_half": "7/20", "A_fifth": "2/75", "A_tenth": "1/60"}
    assert receipt.identifiable_at_declared_errors
    assert not receipt.continuous_region_certified
    assert not receipt.mutation_radius_identified


def test_integration_boundary_separates_feasibility_from_budget():
    worlds, queries = witness()
    for error, costs in ((F(0), (2, 3)), (F(1, 300)-F(1, 10**9), (2, 3)),
                         (F(1, 300), (None, None)), (F(1, 100), (None, None))):
        qs = tuple(replace(q, error_bound=error) for q in queries)
        receipt = certify(worlds, qs)
        plan = optimize(worlds, qs)
        assert (plan.minimum_worst_case_cost, plan.minimum_fixed_resolving_cost) == costs
        assert receipt.identifiable_at_declared_errors == (costs[0] is not None)


def test_integration_heterogeneous_precision_thresholds_are_necessary_and_sufficient():
    worlds, queries = witness()
    limits = (F(9, 80), F(1, 225), F(1, 300))
    for multipliers in product((F(1, 2), F(1), F(3, 2)), repeat=3):
        qs = tuple(replace(q, error_bound=limit*mult)
                   for q, limit, mult in zip(queries, limits, multipliers))
        expected = all(mult < 1 for mult in multipliers)
        assert certify(worlds, qs).identifiable_at_declared_errors == expected
        assert (optimize(worlds, qs).minimum_worst_case_cost is not None) == expected


def test_integration_weighted_routing_cost_law():
    worlds, queries = witness()
    for c0, c1, c2 in product((1, 2, 5), repeat=3):
        qs = tuple(replace(q, cost=c) for q, c in zip(queries, (c0, c1, c2)))
        receipt = optimize(worlds, qs)
        assert receipt.minimum_worst_case_cost == c0+max(c1, c2)
        assert receipt.minimum_fixed_resolving_cost == c0+c1+c2
        assert receipt.worst_case_cost_saving == min(c1, c2)
        assert receipt.optimal_first_queries == ("B_half",)
        assert certify(worlds, qs).critical_error_scale_exact == "10/3"


def test_integration_random_architecture_panels_match_existing_solvers():
    from src.phase_observation_budget import ArchitectureWorld, ContrastQuery
    rng = random.Random(202609072)
    for _ in range(40):
        parameters = set()
        while len(parameters) < 4:
            alpha = F(rng.randrange(2, 10), 10)
            parameters.add((alpha, F(1), F(rng.randrange(1, 13)),
                            alpha*F(rng.randrange(2, 9), 10)))
        worlds = tuple(ArchitectureWorld(f"w{i}", *p) for i, p in enumerate(sorted(parameters)))
        queries = tuple(ContrastQuery(f"q{i}", kind, x, F(rng.randrange(0, 4), 100))
                        for i, (kind, x) in enumerate((
                            ("intrinsic", F(1, 2)), ("interaction", F(1, 5)),
                            ("interaction", F(1, 10)))))
        receipt = certify(worlds, queries)
        scales = {F(0), F(1), F(100)}
        if receipt.critical_error_scale_exact is not None:
            limit = F(receipt.critical_error_scale_exact)
            scales.update((limit/2, limit, limit+1))
        for scale in scales:
            qs = tuple(replace(q, error_bound=F(q.error_bound)*scale) for q in queries)
            plan = optimize(worlds, qs)
            assert receipt.identifiable_at_error_scale(scale) == (
                plan.minimum_worst_case_cost is not None)
            assert receipt.identifiable_at_error_scale(scale) == (
                plan.minimum_fixed_resolving_cost is not None)


def test_integration_guardrails_and_constant_phase():
    worlds, queries = witness()
    with pytest.raises(ValueError, match="matched"):
        certify_phase_precision(worlds, queries, support_reference="synthetic",
                                matched_contrasts_declared=False)
    with pytest.raises(ValueError):
        certify_phase_precision(worlds, queries, support_reference=" ",
                                matched_contrasts_declared=True)
    with pytest.raises(ValueError):
        certify(worlds, (replace(queries[0], cost=0),))
    receipt = certify((worlds[0], worlds[2]), ())
    assert receipt.status == "panel_phase_already_identified"
    assert receipt.identifiable_at_error_scale(100)
