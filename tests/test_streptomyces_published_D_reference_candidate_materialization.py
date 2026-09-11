import json
from pathlib import Path


PATH = Path("validation/streptomyces_published_D_reference_candidate_materialization_v1.json")


def test_named_candidates_are_materialized_but_none_are_qualified():
    data = json.loads(PATH.read_text())
    status = data["materialization_status"]
    assert status["named_candidate_sources_materialized"]
    assert status["named_2020_isolate_count"] == 4
    assert status["qualified_reference_count_ENTRY_CLASS"] == 0
    assert status["qualified_reference_count_INTERMEDIATE_CLASS"] == 0
    assert status["qualified_reference_count_DEEP_CLASS"] == 0
    assert not status["reference_panel_materialized_under_registered_gate"]
    assert not status["d_band_available"]


def test_every_2020_named_isolate_lacks_registered_same_context_d_band():
    data = json.loads(PATH.read_text())
    rows = [r for r in data["materialized_named_candidates"] if r["candidate_id"].startswith("ZHANG2020_")]
    assert len(rows) == 4
    assert all(not r["same_context_72_120h_d_band_available"] for r in rows)
    assert all(not r["qualified_D_reference"] for r in rows)


def test_phenotype_does_not_get_promoted_to_exact_registered_marker_class():
    data = json.loads(PATH.read_text())
    by_id = {r["candidate_id"]: r for r in data["materialized_named_candidates"]}
    assert by_id["ZHANG2020_9H1B"]["phenotypic_marker_class_reported_in_current_receipt"] == "CamS_ArgPlus"
    assert not by_id["ZHANG2020_9H1B"]["exact_registered_marker_class_verified"]
    assert by_id["ZHANG2020_9H1A"]["phenotypic_marker_class_reported_in_current_receipt"] == "CamS_ArgMinus"
    assert not by_id["ZHANG2020_9H1A"]["exact_registered_marker_class_verified"]


def test_2022_serial_transfer_lineages_are_not_reused_as_same_context_realization_refs():
    data = json.loads(PATH.read_text())
    row = next(r for r in data["materialized_named_candidates"] if r["candidate_id"] == "ZHANG2022_M1_TO_M6_T0")
    assert row["serial_transfer_fitness_and_CFU_available"]
    assert not row["context_matches_registered_state_channel"]
    assert not row["same_context_72_120h_d_band_available"]
    assert row["qualified_D_reference_count"] == 0


def test_claim_ceiling_remains_closed():
    ceiling = json.loads(PATH.read_text())["claim_ceiling"]
    assert ceiling["candidate_materialization_is_not_reference_qualification"]
    assert not ceiling["direct_mu_outcome_available"]
    assert not ceiling["matched_generalist_shared_architecture_recovered"]
    assert not ceiling["matched_s_certified"]
    assert not ceiling["architecture_mapping_certified"]
    assert not ceiling["generic_game_promoted"]
    assert not ceiling["eta_promoted"]
    assert not ceiling["e1_promoted"]
