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


def test_sequence_reconstruction_is_still_pending():
    seq = load()["public_sequence_lane"]
    assert seq["bioproject"] == "PRJNA780771"
    assert not seq["sample_to_candidate_accession_mapping_recovered"]
    assert not seq["marker_class_reconstructed"]
    assert not seq["gross_rearrangement_audit_completed"]


def test_sequence_lane_cannot_promote_direct_mu_or_architecture_claims():
    assert all(value is False for value in load()["claim_ceiling"].values())
