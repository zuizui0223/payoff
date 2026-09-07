from fractions import Fraction as F

from src.adaptive_phase_design import routing_witness
from src.adaptive_routing_audit import audit_adaptive_phase_routing
from src.phase_observation_budget import ArchitectureWorld, ContrastQuery


def test_registered_routing_witness_changes_next_distance_and_saves_one_acquisition():
    worlds, queries = routing_witness()
    audit = audit_adaptive_phase_routing(
        worlds,
        queries,
        budget=2,
        support_reference="synthetic four-world routing witness",
        matched_contrasts_declared=True,
    )
    assert audit.status == "phase_routing_audit_complete"
    assert audit.root_query == "intrinsic_r_0.5"
    assert audit.branch_dependent_continuation
    assert not audit.root_alone_resolves_phase_on_every_outcome
    assert audit.adaptive_worst_case_cost_saving == 1
    assert audit.routing_without_direct_phase_resolution
    assert set(audit.distinct_next_actions) == {
        "interaction_d_0.1",
        "interaction_d_0.2",
    }
    assert all(not row.phase_already_resolved for row in audit.branches)


def test_directly_resolving_root_is_not_routing_only_value():
    worlds = (
        ArchitectureWorld("barrier", "0.5", 1, 2, "0.3"),
        ArchitectureWorld("nonbarrier", "0.5", 1, F(16, 9), "0.4"),
    )
    queries = (
        ContrastQuery("direct_d_0.3", "interaction", "0.3", "0.001"),
        ContrastQuery("extra_d_0.1", "interaction", "0.1", "0.001"),
    )
    audit = audit_adaptive_phase_routing(
        worlds,
        queries,
        budget=1,
        support_reference="synthetic direct-resolution control",
        matched_contrasts_declared=True,
    )
    assert audit.root_query == "direct_d_0.3"
    assert audit.root_alone_resolves_phase_on_every_outcome
    assert not audit.branch_dependent_continuation
    assert audit.adaptive_worst_case_cost_saving == 0
    assert not audit.routing_without_direct_phase_resolution


def test_insufficient_budget_returns_no_selected_root_without_inventing_routing_value():
    worlds, queries = routing_witness()
    audit = audit_adaptive_phase_routing(
        worlds,
        queries,
        budget=1,
        support_reference="synthetic insufficient-budget control",
        matched_contrasts_declared=True,
    )
    assert audit.status == "no_affordable_nonterminal_selected_root"
    assert audit.root_query is None
    assert not audit.routing_without_direct_phase_resolution
