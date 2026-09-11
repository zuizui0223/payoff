import json
from pathlib import Path


RAW = Path("validation/streptomyces_2020_dryad_raw_reconstruction_v1.json")
CANDIDATES = Path("validation/streptomyces_published_D_reference_candidate_materialization_v1.json")
ARCH = Path("validation/architecture_mapping_status_v1.json")


def load(path):
    return json.loads(path.read_text())


def test_r0_identity_and_manifest_are_recovered_but_bytes_are_not():
    data = load(RAW)
    status = data["reconstruction_status"]
    assert status["source_identity_recovered"]
    assert status["file_manifest_recovered"]
    assert status["current_level"] == "R0_SOURCE_IDENTITY_AND_FILE_MANIFEST_RECOVERED"
    assert not status["raw_bytes_acquired"]
    assert not status["checksum_verified"]
    assert not status["workbook_opened"]
    assert not status["sheet_manifest_reconstructed"]
    assert not status["lossless_cell_normalization_completed"]
    assert not status["numeric_analysis_reproduced"]


def test_manifest_identity_is_specific_and_single_file():
    data = load(RAW)
    archive = data["archive"]
    assert archive["dataset_doi"] == "10.5061/dryad.bnzs7h462"
    assert archive["file_count_known"] == 1
    row = archive["file_manifest"][0]
    assert row["filename"] == "Data_Dryad_DoL-Zheren_Zhang.xlsx"
    assert row["format"] == "xlsx"
    assert row["reported_size_kb"] == 81.04


def test_download_auth_block_is_not_reinterpreted_as_missing_or_negative():
    blocker = load(RAW)["current_blocker"]
    assert blocker["class"] == "DOWNLOAD_AUTHORIZATION"
    prohibited = set(blocker["must_not_be_reinterpreted_as"])
    assert {"FILE_MISSING", "DATASET_UNAVAILABLE", "NUMERIC_NEGATIVE_RESULT"} <= prohibited


def test_r_lane_does_not_promote_game_reference_or_architecture_claims():
    firewall = load(RAW)["semantic_firewall"]
    assert not firewall["generic_game_result_recovered_from_this_receipt"]
    assert not firewall["D_reference_qualified_from_this_receipt"]
    assert not firewall["matched_generalist_shared_architecture_recovered"]
    assert not firewall["matched_s_certified"]
    assert not firewall["architecture_mapping_certified"]
    assert not firewall["eta_promoted"]
    assert not firewall["e1_promoted"]

    candidate_status = load(CANDIDATES)["materialization_status"]
    assert candidate_status["qualified_reference_count_ENTRY_CLASS"] == 0
    assert candidate_status["qualified_reference_count_INTERMEDIATE_CLASS"] == 0
    assert candidate_status["qualified_reference_count_DEEP_CLASS"] == 0

    arch = load(ARCH)
    assert not arch["systems"]["STREPTOMYCES_GENOME_FRAGILITY"]["mapping_certified"]
