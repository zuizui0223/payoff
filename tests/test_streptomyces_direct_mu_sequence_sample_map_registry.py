import json
from pathlib import Path


MAP = Path("validation/streptomyces_direct_mu_sequence_sample_map_v1.json")
SEPARATION = Path("validation/streptomyces_direct_mu_sequence_material_separation_v1.json")


def load(path):
    return json.loads(path.read_text())


def test_sample_map_registry_is_synchronized_with_resolved_run_mapping():
    data = load(MAP)
    rows = {x["candidate_id"]: x for x in data["priority_candidates"]}

    m5 = rows["M5_T0"]
    assert m5["runs"]["pacbio"]["run"] == "SRR16954720"
    assert m5["runs"]["bgi"]["run"] == "SRR16954696"
    assert m5["source_metadata_names_candidate"]
    assert m5["mapping_independently_crosschecked"]
    assert m5["sequence_marker_reconstruction_allowed"]
    assert m5["current_blockers"] == []

    m1 = rows["M1_T0"]
    assert m1["runs"]["pacbio"]["run"] == "SRR16954714"
    assert m1["runs"]["bgi"]["run"] == "SRR16954700"
    assert m1["sequence_marker_reconstruction_allowed"]


def test_sample_map_agrees_with_sequence_material_separation_registry():
    mapping = load(MAP)
    separation = load(SEPARATION)["public_sequence_lane"]
    map_rows = {x["candidate_id"]: x for x in mapping["priority_candidates"]}

    for candidate_id in ("M5_T0", "M1_T0"):
        assert map_rows[candidate_id]["runs"] == separation["priority_candidate_runs"][candidate_id]

    assert mapping["claim_boundary"]["sequence_sample_map_qualified"]
    assert mapping["claim_boundary"]["sequence_marker_reconstruction_allowed"]


def test_resolved_run_mapping_does_not_promote_marker_or_reference_claims():
    boundary = load(MAP)["claim_boundary"]
    assert not boundary["marker_class_reconstructed"]
    assert not boundary["gross_rearrangement_audit_completed"]
    assert not boundary["physical_material_identity_established"]
    assert not boundary["candidate_reference_qualified"]
    assert not boundary["d_band_available"]
    assert not boundary["direct_mu_outcome_available"]
    assert not boundary["architecture_mapping_certified"]
    assert not boundary["eta_promoted"]
    assert not boundary["e1_promoted"]
