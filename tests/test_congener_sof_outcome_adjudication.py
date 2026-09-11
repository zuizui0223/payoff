from fractions import Fraction

import pytest

from src.congener_sof_outcome_adjudication import (
    adjudicate_congener_sof_outcome,
    adjudicate_genotoxic_generation_branch,
    classify_material_reduction,
    classify_task_preservation,
)


def test_task_preservation_requires_strict_noninferiority_not_nonsignificance():
    r = classify_task_preservation(("-1/20", "1/50"), material_loss_tolerance="1/10")
    assert r.task_result == "preserved"
    assert not r.boundary_contact


def test_task_material_loss_and_boundary_contact():
    lost = classify_task_preservation(("-1/4", "-1/5"), material_loss_tolerance="1/10")
    assert lost.task_result == "material_task_loss"
    contact = classify_task_preservation(("-1/10", "1/50"), material_loss_tolerance="1/10")
    assert contact.task_result == "unresolved"
    assert contact.boundary_contact


def test_material_reduction_uses_strict_closed_band_rule():
    reduced = classify_material_reduction(("3/20", "1/5"), material_reduction="1/10")
    assert reduced.result == "reduced"
    excluded = classify_material_reduction(("0", "1/20"), material_reduction="1/10")
    assert excluded.result == "material_reduction_excluded"
    contact = classify_material_reduction(("1/10", "1/5"), material_reduction="1/10")
    assert contact.result == "unresolved"
    assert contact.boundary_contact


def test_genotoxic_and_mu_both_must_reduce_for_joint_branch():
    both = adjudicate_genotoxic_generation_branch("reduced", "reduced")
    assert both.branch_result == "genotoxic_generation_reduced"
    no_route = adjudicate_genotoxic_generation_branch(
        "material_reduction_excluded", "material_reduction_excluded"
    )
    assert no_route.branch_result == "registered_route_not_supported"
    discord = adjudicate_genotoxic_generation_branch(
        "reduced", "material_reduction_excluded"
    )
    assert discord.branch_result == "genotoxic_mu_discordant"
    unresolved = adjudicate_genotoxic_generation_branch("reduced", "unresolved")
    assert unresolved.branch_result == "unresolved"


def test_four_primary_resolved_sof_quadrants_are_distinct():
    expected = {
        ("preserved", "genotoxic_generation_reduced"): "SEPARATION_OF_FUNCTION_SUPPORTED",
        ("preserved", "registered_route_not_supported"): "TASK_PRESERVED_REGISTERED_GENOTOXIC_GENERATION_ROUTE_NOT_SUPPORTED",
        ("material_task_loss", "genotoxic_generation_reduced"): "MECHANISM_SIGNAL_PRESENT_BUT_TASK_CONFOUNDED",
        ("material_task_loss", "registered_route_not_supported"): "CANDIDATE_FAILS_TASK_AND_REGISTERED_ROUTE_CRITERIA",
    }
    for pair, outcome in expected.items():
        r = adjudicate_congener_sof_outcome(*pair)
        assert r.outcome_class == outcome


def test_only_preserved_plus_joint_reduction_supports_sof():
    r = adjudicate_congener_sof_outcome("preserved", "genotoxic_generation_reduced")
    assert r.separation_of_function_supported
    assert r.mechanism_signal_supported
    assert r.task_match_supported
    assert not r.matched_s_promoted
    assert not r.architecture_mapping_promoted
    assert not r.generic_game_promoted
    assert not r.eta_promoted
    assert not r.e1_promoted


def test_task_loss_plus_reduction_is_mechanism_support_not_sof():
    r = adjudicate_congener_sof_outcome(
        "material_task_loss", "genotoxic_generation_reduced"
    )
    assert r.mechanism_signal_supported
    assert not r.task_match_supported
    assert not r.separation_of_function_supported


def test_discordance_and_uncertainty_never_support_sof():
    d = adjudicate_congener_sof_outcome("preserved", "genotoxic_mu_discordant")
    assert d.outcome_class == "GENOTOXIC_MU_DISCORDANCE_SOF_UNRESOLVED"
    assert not d.separation_of_function_supported
    u = adjudicate_congener_sof_outcome("unresolved", "genotoxic_generation_reduced")
    assert u.outcome_class == "INCOMPLETE_OR_UNRESOLVED_SOF"
    assert not u.separation_of_function_supported


def test_exact_fraction_inputs_are_retained():
    r = classify_task_preservation((Fraction(-1, 20), Fraction(1, 20)), material_loss_tolerance=Fraction(1, 10))
    assert r.performance_difference_band == (Fraction(-1, 20), Fraction(1, 20))


@pytest.mark.parametrize("delta", ["-1/100", -1])
def test_negative_materiality_thresholds_rejected(delta):
    with pytest.raises(ValueError):
        classify_task_preservation((0, 0), material_loss_tolerance=delta)
    with pytest.raises(ValueError):
        classify_material_reduction((0, 0), material_reduction=delta)


def test_invalid_categorical_inputs_rejected():
    with pytest.raises(ValueError):
        adjudicate_genotoxic_generation_branch("positive", "reduced")
    with pytest.raises(ValueError):
        adjudicate_congener_sof_outcome("same", "genotoxic_generation_reduced")
