import json
from pathlib import Path


RAW = Path("validation/raw_archive_reconstruction_status_v1.json")
ARCH = Path("validation/architecture_mapping_status_v1.json")


def raw_rows():
    data = json.loads(RAW.read_text())
    return data, {row["system_id"]: row for row in data["archives"]}


def test_raw_registry_is_provenance_only_with_system_specific_r_levels():
    data, rows = raw_rows()
    assert data["lane"] == "R"
    assert data["archives"]
    assert not data["semantic_claims_allowed"]
    assert not data["generic_game_claims_allowed_from_this_registry_alone"]
    assert not data["architecture_mapping_claims_allowed_from_this_registry_alone"]

    assert rows["PSTUTZERI_2022"]["r_level"] == "R0"
    assert rows["ARABIDOPSIS_HALLERI_2017"]["r_level"] == "R0"
    assert rows["BECK_SYNTHETIC_ECOLI"]["r_level"] == "R3"


def test_unreconstructed_raw_targets_remain_r0():
    _, rows = raw_rows()
    for system_id in ("PSTUTZERI_2022", "ARABIDOPSIS_HALLERI_2017"):
        row = rows[system_id]
        assert row["source_identity_verified"]
        assert row["r_level"] == "R0"
        assert not row["bytes_acquired"]
        assert not row["checksum_verified"]
        assert not row["manifest_reconstructed"]
        assert not row["schema_reconstructed"]
        assert not row["transformations_reconstructed"]
        assert not row["raw_analysis_reproduced"]


def test_beck_r3_receipt_pins_bytes_manifest_and_lossless_normalization():
    _, rows = raw_rows()
    beck = rows["BECK_SYNTHETIC_ECOLI"]
    assert beck["source_filename"] == "22_0519_SupplementaryDataSets.xlsx"
    assert beck["repository_object_id"] == "0ed48b34713d08dbdb17d9ca626387d63c673dbf"
    assert beck["repository_object_id_type"] == "git_blob_sha1"
    assert beck["reported_byte_size"] == 1112530
    assert beck["byte_size_verified"] == 1112530
    assert beck["bytes_acquired"]
    assert beck["checksum_verified"]
    assert beck["sha256"] == "526bd7a0deebd9196762ea711639d0acd727eda9a30df29554909a7d3f5a4baa"
    assert beck["git_blob_sha1_recomputed"] == beck["repository_object_id"]
    assert beck["git_blob_match"]
    assert beck["manifest_reconstructed"]
    assert beck["schema_reconstructed"]
    assert beck["sheet_count"] == 30
    assert len(beck["sheet_names"]) == 30
    assert beck["transformations_reconstructed"]
    assert beck["normalization_type"] == "lossless_nonempty_cell_long_form_tsv"
    assert beck["normalized_nonempty_cells"] == 33125
    assert beck["normalized_tsv_sha256"] == "82fe0d7a591cb091d9efddfceede15116b55c293ffc64402f6f9c5ee0940fdc0"
    assert beck["metric_row_count"] == 63
    assert beck["metric_tsv_sha256"] == "2a139b2acdf50e357ba09935b3bc199e29738659adb7f7d29696ab35a082f087"
    assert beck["reconstruction_workflow_run_id"] == 34295583193
    assert beck["reconstruction_artifact_id"] == 10082985862
    assert beck["reconstruction_artifact_zip_sha256"] == "b2cc2ee77a0fad4141b39245367d1e765ffcc31c94df1c0e74cbe0836b69b235"
    assert not beck["raw_analysis_reproduced"]
    assert beck["r_level"] == "R3"


def test_r3_still_cannot_emit_game_or_architecture_semantics():
    data, rows = raw_rows()
    assert rows["BECK_SYNTHETIC_ECOLI"]["r_level"] == "R3"
    assert not data["semantic_claims_allowed"]
    assert not data["generic_game_claims_allowed_from_this_registry_alone"]
    assert not data["architecture_mapping_claims_allowed_from_this_registry_alone"]


def test_architecture_registry_is_independent_and_no_current_mapping_is_certified():
    data = json.loads(ARCH.read_text())
    assert data["lane"] == "A"
    assert not data["frequency_game_evidence_used_to_certify_mapping"]
    assert not data["any_mapping_certified"]
    assert data["systems"]
    assert not any(row["mapping_certified"] for row in data["systems"])


def test_streptomyces_mapping_stops_at_missing_matched_s_and_generation_suppression():
    data = json.loads(ARCH.read_text())
    row = next(x for x in data["systems"] if x["system_id"] == "STREPTOMYCES_COELICOLOR")
    assert row["differentiated_released_candidate"] == "strong"
    assert not row["matched_generalist_only_comparator_recovered"]
    assert row["matched_comparator_receipt"] == "STREPTOMYCES_MATCHED_ARCHITECTURE_COMPARATOR_V1"
    assert not row["matched_comparator_certified"]
    assert row["matched_s_candidate_search_receipt"] == "STREPTOMYCES_MATCHED_S_CANDIDATE_SEARCH_V1"
    assert not row["matched_s_generation_suppression_identified"]
    assert not row["unit_consistency"]
    assert not row["mapping_certified"]
    assert "MATCHED_S_ARCHITECTURE_NOT_RECOVERED" in row["primary_blockers"]
    assert "DIFFERENTIATION_GENERATION_SUPPRESSION_NOT_IDENTIFIED" in row["primary_blockers"]
    assert "BACKGROUND_NOT_MATCHED" in row["primary_blockers"]
    assert "FOCAL_ARCHITECTURE_DIFFERENCE_NOT_ISOLATED" in row["primary_blockers"]


def test_evolved_ecoli_mapping_stops_at_multigenotype_strategic_unit():
    data = json.loads(ARCH.read_text())
    row = next(x for x in data["systems"] if x["system_id"] == "EVOLVED_ECOLI_CROSSFEEDING")
    assert row["integrated_shared_candidate"] == "strong"
    assert row["differentiated_released_candidate"] == "strong_ecological_consortium_level"
    assert row["matched_generalist_only_comparator_recovered"]
    assert not row["heritable_or_stable_strategic_pair"]
    assert not row["mapping_certified"]
    assert "MULTIGENOTYPE_D_STRATEGIC_UNIT_NOT_CERTIFIED" in row["primary_blockers"]
