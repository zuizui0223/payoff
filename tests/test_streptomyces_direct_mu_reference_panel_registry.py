import json
from pathlib import Path

from src.direct_mu_reference_panel_qualification import adjudicate_reference_panel


PATH = Path("validation/streptomyces_direct_mu_reference_panel_qualification_v1.json")
REALIZATION = Path("validation/streptomyces_direct_mu_realization_design_v1.json")


def test_reference_qualification_rules_are_frozen_but_no_panel_is_materialized():
    data = json.loads(PATH.read_text())
    assert data["qualification_rules_frozen_preoutcome"]
    assert data["minimum_qualified_references_per_class"] == 2
    status = data["current_status"]
    assert not status["reference_candidates_materialized"]
    assert status["qualified_reference_count_ENTRY_CLASS"] == 0
    assert status["qualified_reference_count_INTERMEDIATE_CLASS"] == 0
    assert status["qualified_reference_count_DEEP_CLASS"] == 0
    assert not status["reference_panel_qualified"]
    assert not status["d_band_available"]
    assert not status["realization_channel_ready"]


def test_empty_current_panel_fails_all_three_predeclared_classes():
    ready, blockers, qualifications = adjudicate_reference_panel(())
    assert not ready
    assert len(blockers) == 3
    assert qualifications == ()


def test_realization_registry_links_frozen_qualification_receipt_without_promotion():
    q = json.loads(PATH.read_text())
    r = json.loads(REALIZATION.read_text())
    assert r["reference_panel_qualification_receipt"] == q["receipt_id"]
    assert r["reference_panel_rule"]["qualification_rules_frozen_preoutcome"]
    assert r["status"]["reference_panel_qualification_rules_frozen_preoutcome"]
    assert not r["status"]["reference_panel_materialized"]
    assert not r["status"]["reference_panel_qualified"]
    assert not r["status"]["d_band_available"]
    assert not r["status"]["absolute_mass_route_ready"]


def test_claim_ceiling_stays_closed():
    ceiling = json.loads(PATH.read_text())["claim_ceiling"]
    assert not ceiling["direct_mu_outcome_available"]
    assert not ceiling["matched_generalist_shared_architecture_recovered"]
    assert not ceiling["matched_s_certified"]
    assert not ceiling["architecture_mapping_certified"]
    assert not ceiling["generic_game_promoted"]
    assert not ceiling["eta_promoted"]
    assert not ceiling["e1_promoted"]
