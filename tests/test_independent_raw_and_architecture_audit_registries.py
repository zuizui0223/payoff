import json
from pathlib import Path


RAW = Path("validation/raw_archive_reconstruction_status_v1.json")
ARCH = Path("validation/architecture_mapping_status_v1.json")


def test_raw_registry_is_provenance_only_and_all_current_targets_remain_r0():
    data = json.loads(RAW.read_text())
    assert data["lane"] == "R"
    assert data["archives"]
    assert not data["semantic_claims_allowed"]
    assert not data["generic_game_claims_allowed_from_this_registry_alone"]
    assert not data["architecture_mapping_claims_allowed_from_this_registry_alone"]
    for row in data["archives"]:
        assert row["source_identity_verified"]
        assert row["r_level"] == "R0"
        assert not row["bytes_acquired"]
        assert not row["checksum_verified"]
        assert not row["manifest_reconstructed"]
        assert not row["schema_reconstructed"]
        assert not row["transformations_reconstructed"]
        assert not row["raw_analysis_reproduced"]


def test_beck_r0_receipt_pins_repository_object_without_claiming_local_bytes():
    data = json.loads(RAW.read_text())
    beck = next(x for x in data["archives"] if x["system_id"] == "BECK_SYNTHETIC_ECOLI")
    assert beck["source_filename"] == "22_0519_SupplementaryDataSets.xlsx"
    assert beck["repository_object_id"] == "0ed48b34713d08dbdb17d9ca626387d63c673dbf"
    assert beck["repository_object_id_type"] == "git_blob_sha1"
    assert beck["reported_byte_size"] == 1112530
    assert not beck["bytes_acquired"]


def test_architecture_registry_is_independent_and_no_current_mapping_is_certified():
    data = json.loads(ARCH.read_text())
    assert data["lane"] == "A"
    assert not data["frequency_game_evidence_used_to_certify_mapping"]
    assert not data["any_mapping_certified"]
    assert data["systems"]
    assert not any(row["mapping_certified"] for row in data["systems"])


def test_streptomyces_mapping_stops_at_missing_matched_s_and_unit_consistency():
    data = json.loads(ARCH.read_text())
    row = next(x for x in data["systems"] if x["system_id"] == "STREPTOMYCES_COELICOLOR")
    assert row["differentiated_released_candidate"] == "strong"
    assert not row["matched_generalist_only_comparator_recovered"]
    assert not row["unit_consistency"]
    assert not row["mapping_certified"]
    assert "MATCHED_S_ARCHITECTURE_NOT_RECOVERED" in row["primary_blockers"]


def test_evolved_ecoli_mapping_stops_at_multigenotype_strategic_unit():
    data = json.loads(ARCH.read_text())
    row = next(x for x in data["systems"] if x["system_id"] == "EVOLVED_ECOLI_CROSSFEEDING")
    assert row["integrated_shared_candidate"] == "strong"
    assert row["differentiated_released_candidate"] == "strong_ecological_consortium_level"
    assert row["matched_generalist_only_comparator_recovered"]
    assert not row["heritable_or_stable_strategic_pair"]
    assert not row["mapping_certified"]
    assert "MULTIGENOTYPE_D_STRATEGIC_UNIT_NOT_CERTIFIED" in row["primary_blockers"]
