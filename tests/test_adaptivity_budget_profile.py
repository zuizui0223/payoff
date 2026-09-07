from fractions import Fraction as F

from src.adaptive_phase_design import routing_witness
from src.adaptivity_budget_profile import phase_adaptivity_budget_profile
from src.phase_observation_budget import ArchitectureWorld, ContrastQuery


def test_registered_routing_witness_has_single_intermediate_adaptive_only_budget():
    worlds, queries = routing_witness()
    profile = phase_adaptivity_budget_profile(
        worlds,
        queries,
        budgets=(0, 1, 2, 3, 4),
        support_reference="synthetic PAYOFF adaptivity budget window",
        matched_contrasts_declared=True,
    )
    assert profile.minimum_adaptive_worst_path_cost == 2
    assert profile.minimum_fixed_resolving_cost == 3
    assert profile.cost_saving == 1
    assert profile.adaptive_only_budgets == (2,)
    by_budget = {row.budget: row for row in profile.rows}
    assert not by_budget[1].adaptive_guarantees_phase
    assert by_budget[2].adaptive_guarantees_phase
    assert not by_budget[2].fixed_bundle_guarantees_phase
    assert by_budget[3].adaptive_guarantees_phase
    assert by_budget[3].fixed_bundle_guarantees_phase


def test_direct_resolution_control_has_no_adaptive_only_window():
    worlds = (
        ArchitectureWorld("barrier", "0.5", 1, 2, "0.3"),
        ArchitectureWorld("nonbarrier", "0.5", 1, F(16, 9), "0.4"),
    )
    queries = (
        ContrastQuery("direct_d_0.3", "interaction", "0.3", "0.001"),
        ContrastQuery("extra_d_0.1", "interaction", "0.1", "0.001"),
    )
    profile = phase_adaptivity_budget_profile(
        worlds,
        queries,
        budgets=(0, 1, 2),
        support_reference="synthetic direct resolution budget control",
        matched_contrasts_declared=True,
    )
    assert profile.minimum_adaptive_worst_path_cost == 1
    assert profile.minimum_fixed_resolving_cost == 1
    assert profile.cost_saving == 0
    assert profile.adaptive_only_budgets == ()


def test_profile_rejects_duplicate_negative_or_empty_budget_lists():
    worlds, queries = routing_witness()
    kwargs = dict(
        worlds=worlds,
        queries=queries,
        support_reference="synthetic budget validation",
        matched_contrasts_declared=True,
    )
    for budgets in ((2, 2), (-1, 0), ()):
        try:
            phase_adaptivity_budget_profile(budgets=budgets, **kwargs)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid budgets must fail")
