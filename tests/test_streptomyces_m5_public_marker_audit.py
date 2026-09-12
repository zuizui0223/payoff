import json
from pathlib import Path

AUDIT = Path("validation/streptomyces_m5_public_marker_audit_v1.json")


def load():
    return json.loads(AUDIT.read_text())


def test_registered_four_locus_pattern_is_directly_scored_from_exact_m5_run():
    data = load()
    assert data["public_sequence"]["run"] == "SRR16954720"
    assert data["public_sequence"]["reference_genome"] == "NC_003888.3"
    adjudication = data["adjudication"]
    assert adjudication["registered_four_locus_pattern_directly_scored"]
    assert adjudication["core_reference_present"]
    assert adjudication["entry_marker_absent"]
    assert adjudication["intermediate_marker_absent"]
    assert adjudication["deep_marker_absent"]
    assert adjudication["registered_deletion_class"] == "DEEP_CLASS"
    assert adjudication["registered_deletion_class_verified_from_public_sequence"]


def test_core_is_present_while_all_registered_right_arm_markers_are_zero_coverage():
    rows = {x["legacy_locus"]: x for x in load()["registered_marker_coverage"]}
    core = rows["SCO3879"]
    assert core["coverage_percent"] == 100.0
    assert core["mean_depth"] == 124.526
    assert core["observed_state"] == "PRESENT"
    for locus in ("SCO7662", "SCO7350", "SCO7036"):
        assert rows[locus]["coverage_percent"] == 0.0
        assert rows[locus]["mean_depth"] == 0.0
        assert rows[locus]["observed_state"] == "ABSENT"


def test_genomic_class_verification_does_not_qualify_reference():
    data = load()
    adjudication = data["adjudication"]
    assert not adjudication["gross_secondary_rearrangement_audit_completed"]
    assert not adjudication["physical_stock_identity_established"]
    assert not adjudication["registered_72_120_realization_available"]
    assert not adjudication["qualified_d_reference"]
    ceiling = data["claim_ceiling"]
    assert ceiling["deletion_class_verified"]
    for key in (
        "qualified_reference",
        "d_band_available",
        "direct_mu_outcome_available",
        "matched_s_certified",
        "architecture_mapping_certified",
        "eta_architecture_specific",
        "e1",
    ):
        assert ceiling[key] is False, key


def test_audit_provenance_is_frozen():
    p = load()["audit_provenance"]
    assert p["workflow_commit"] == "3b98cc63e0a3c754b857b51a84a3a783a451a21f"
    assert p["workflow_run_id"] == 34667360902
    assert p["workflow_job_id"] == 103481885044
    assert p["artifact_id"] == 10289234376
