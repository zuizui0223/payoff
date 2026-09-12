import json
from pathlib import Path

RECEIPT = Path("validation/streptomyces_direct_mu_sequence_material_separation_v1.json")


def load():
    return json.loads(RECEIPT.read_text())


def test_public_wgs_does_not_imply_material_access():
    data = load()
    assert data["public_sequence_lane"]["T0_M1_to_M6_WGS_reported"]
    assert data["physical_material_lane"]["archived_stocks_reported"]
    assert not data["physical_material_lane"]["public_culture_collection_accession_recovered"]
    assert not data["physical_material_lane"]["physical_stock_identity_reconfirmed"]
    assert not data["physical_material_lane"]["material_available_for_registered_72_120_assay"]


def test_exact_priority_candidate_public_sequence_mapping_is_recovered():
    seq = load()["public_sequence_lane"]
    assert seq["bioproject"] == "PRJNA780771"
    assert seq["study_accession"] == "SRP346308"
    assert seq["sample_to_candidate_accession_mapping_recovered"]
    runs = seq["priority_candidate_runs"]
    assert runs["M5_T0"]["pacbio"]["run"] == "SRR16954720"
    assert runs["M5_T0"]["bgi"]["run"] == "SRR16954696"
    assert runs["M1_T0"]["pacbio"]["run"] == "SRR16954714"
    assert runs["M1_T0"]["bgi"]["run"] == "SRR16954700"
    assert runs["M5_T0"]["pacbio"]["library_name"] == "M5_T0_PacBio"
    assert runs["M1_T0"]["bgi"]["library_name"] == "M1_T0_BGI"


def test_shared_platform_biosample_is_not_used_as_candidate_identity():
    seq = load()["public_sequence_lane"]
    runs = seq["priority_candidate_runs"]
    assert runs["M5_T0"]["pacbio"]["biosample"] == runs["M1_T0"]["pacbio"]["biosample"]
    assert runs["M5_T0"]["bgi"]["biosample"] == runs["M1_T0"]["bgi"]["biosample"]
    assert "experiment/run alias" in seq["identity_guardrail"]


def test_marker_and_rearrangement_reconstruction_are_still_pending():
    seq = load()["public_sequence_lane"]
    assert not seq["marker_class_reconstructed"]
    assert not seq["gross_rearrangement_audit_completed"]


def test_sequence_lane_cannot_promote_direct_mu_or_architecture_claims():
    assert all(value is False for value in load()["claim_ceiling"].values())
