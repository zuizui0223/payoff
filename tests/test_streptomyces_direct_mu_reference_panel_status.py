import json
from pathlib import Path

from src.direct_mu_reference_panel_qualification import adjudicate_reference_panel


PATH = Path("validation/streptomyces_direct_mu_reference_panel_status_v1.json")
REALIZATION = Path("validation/streptomyces_direct_mu_realization_design_v1.json")
ASSAY = Path("validation/streptomyces_congener_assay_scale_status_v1.json")


def test_empty_registered_panel_recomputes_as_not_ready():
    data = json.loads(PATH.read_text())
    ready, blockers, qualifications = adjudicate_reference_panel(())
    assert not ready
    assert qualifications == ()
    assert set(blockers) == {
        "ENTRY_CLASS_QUALIFIED_REFERENCE_COUNT_BELOW_2",
        "INTERMEDIATE_CLASS_QUALIFIED_REFERENCE_COUNT_BELOW_2",
        "DEEP_CLASS_QUALIFIED_REFERENCE_COUNT_BELOW_2",
    }
    assert data["candidate_references"] == []
    assert not data["panel_materialized"]
    assert not data["panel_qualified"]
    assert not data["d_band_available"]


def test_reference_panel_status_matches_realization_design():
    data = json.loads(PATH.read_text())
    design = json.loads(REALIZATION.read_text())
    assert data["minimum_independent_references_per_class"] == design["reference_panel_rule"]["minimum_independent_references_per_class"]
    assert data["panel_materialized"] == design["status"]["reference_panel_materialized"]
    assert data["panel_qualified"] == design["status"]["reference_panel_qualified"]
    assert data["d_band_available"] == design["status"]["d_band_available"]


def test_realization_not_ready_keeps_direct_mu_not_ready():
    status = json.loads(PATH.read_text())
    assay = json.loads(ASSAY.read_text())
    assert not status["panel_qualified"]
    assert not assay["direct_mu_scale"]["direct_mu_realization_channel_ready"]
    assert not assay["direct_mu_scale"]["direct_mu_fully_ready"]
    assert not assay["direct_mu_scale"]["qualified_for_outcome_opening"]


def test_reference_panel_work_does_not_promote_architecture_claims():
    ceiling = json.loads(PATH.read_text())["claim_ceiling"]
    assert not ceiling["direct_mu_outcome_available"]
    assert not ceiling["matched_generalist_shared_architecture_recovered"]
    assert not ceiling["matched_s_certified"]
    assert not ceiling["architecture_mapping_certified"]
    assert not ceiling["generic_game_promoted"]
    assert not ceiling["eta_promoted"]
    assert not ceiling["e1_promoted"]
