import json
from pathlib import Path

from src.differentiation_suppression_identifiability import (
    DifferentiationSuppressionReceipt,
    adjudicate_differentiation_suppression,
)


REGISTRY = Path("validation/streptomyces_matched_s_candidate_search_v1.json")


def load_registry():
    return json.loads(REGISTRY.read_text())


def receipt_from_row(row):
    keys = {
        "observed_specialist_frequency_reduced_declared",
        "direct_generation_rate_measured_declared",
        "generation_rate_reduced_declared",
        "post_generation_survival_or_realization_matched_declared",
        "generalist_growth_matched_declared",
        "generalist_sporulation_matched_declared",
        "net_task_preserved_declared",
        "ecological_context_matched_declared",
        "background_matched_declared",
        "focal_differentiation_mechanism_isolated_declared",
        "stable_or_heritable_unit_declared",
        "independent_of_game_result_declared",
        "independent_of_raw_availability_declared",
    }
    return DifferentiationSuppressionReceipt(
        system_id="STREPTOMYCES_COELICOLOR",
        perturbation_id=row["perturbation_id"],
        support_reference=row["support_reference"],
        **{k: row[k] for k in keys},
    )


def test_all_registered_candidates_recompute_as_not_matched_s():
    data = load_registry()
    assert data["lane"] == "A"
    assert data["candidates"]
    for row in data["candidates"]:
        result = adjudicate_differentiation_suppression(receipt_from_row(row))
        assert result.matched_s_candidate_certified == row["expected_matched_s_candidate_certified"]
        assert not result.matched_s_candidate_certified
        assert not result.generic_game_promoted
        assert not result.architecture_frequency_claim_promoted
    assert not data["any_matched_s_candidate_certified"]


def test_delta_pare_is_survivor_filter_not_generation_suppression():
    row = next(x for x in load_registry()["candidates"] if x["perturbation_id"] == "DELTA_parE")
    result = adjudicate_differentiation_suppression(receipt_from_row(row))
    assert row["observed_specialist_frequency_reduced_declared"]
    assert not result.generation_suppression_identified
    assert "DIRECT_DIFFERENTIATION_GENERATION_RATE_NOT_MEASURED" in result.blockers
    assert "POST_GENERATION_SURVIVAL_OR_REALIZATION_NOT_MATCHED" in result.blockers
    assert "GENERALIST_GROWTH_NOT_MATCHED" in result.blockers
    assert "GENERALIST_SPORULATION_NOT_MATCHED" in result.blockers


def test_opposite_direction_genetic_instability_candidates_are_not_promoted():
    data = load_registry()
    for perturbation in ("tap_or_tpg_disruption", "DELTA_ftsK_SC", "DELTA_sco2730"):
        row = next(x for x in data["candidates"] if x["perturbation_id"] == perturbation)
        result = adjudicate_differentiation_suppression(receipt_from_row(row))
        assert not row["observed_specialist_frequency_reduced_declared"]
        assert not result.matched_s_candidate_certified


def test_context_reduction_is_not_a_stable_s_architecture():
    row = next(
        x for x in load_registry()["candidates"]
        if x["perturbation_id"] == "SUB_MIC_tetracycline_or_gentamicin_context"
    )
    result = adjudicate_differentiation_suppression(receipt_from_row(row))
    assert row["observed_specialist_frequency_reduced_declared"]
    assert not row["ecological_context_matched_declared"]
    assert not row["stable_or_heritable_unit_declared"]
    assert "ECOLOGICAL_CONTEXT_NOT_MATCHED" in result.blockers
    assert "STABLE_OR_HERITABLE_S_UNIT_NOT_ESTABLISHED" in result.blockers


def test_large_genome_reduction_does_not_isolate_the_architecture_axis():
    row = next(
        x for x in load_registry()["candidates"]
        if x["perturbation_id"] == "ARTIFICIAL_CIRCULARIZATION_OR_LARGE_GENOME_REDUCTION"
    )
    result = adjudicate_differentiation_suppression(receipt_from_row(row))
    assert not row["background_matched_declared"]
    assert not row["focal_differentiation_mechanism_isolated_declared"]
    assert "BACKGROUND_NOT_MATCHED" in result.blockers
    assert "FOCAL_DIFFERENTIATION_MECHANISM_NOT_ISOLATED" in result.blockers


def test_registry_does_not_claim_exhaustive_nonexistence():
    data = load_registry()
    assert data["claim_status"] == "MATCHED_GENERALIST_ONLY_STREPTOMYCES_ARCHITECTURE_NOT_YET_RECOVERED"
    assert "does_not_exist" not in data["claim_status"].lower()
