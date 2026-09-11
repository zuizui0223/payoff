import json
from pathlib import Path


PATH = Path("validation/streptomyces_published_D_reference_source_audit_v1.json")


def test_published_sources_exist_but_none_currently_qualify():
    data = json.loads(PATH.read_text())
    conclusion = data["current_conclusion"]
    assert conclusion["published_candidate_sources_exist"]
    assert not conclusion["published_material_directly_satisfying_current_reference_panel_gate"]
    assert conclusion["qualified_reference_count_ENTRY_CLASS"] == 0
    assert conclusion["qualified_reference_count_INTERMEDIATE_CLASS"] == 0
    assert conclusion["qualified_reference_count_DEEP_CLASS"] == 0
    assert not conclusion["reference_panel_materialized"]
    assert not conclusion["reference_panel_qualified"]
    assert not conclusion["d_band_available"]


def test_no_source_is_silently_promoted_to_a_qualified_reference():
    data = json.loads(PATH.read_text())
    assert all(source["currently_qualified_reference_count"] == 0 for source in data["sources"])
    ceiling = data["claim_ceiling"]
    assert not ceiling["direct_mu_outcome_available"]
    assert not ceiling["matched_generalist_shared_architecture_recovered"]
    assert not ceiling["matched_s_certified"]
    assert not ceiling["architecture_mapping_certified"]
    assert not ceiling["eta_promoted"]
    assert not ceiling["e1_promoted"]
