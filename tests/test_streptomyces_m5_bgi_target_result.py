import json
from pathlib import Path


PATH = Path("validation/streptomyces_m5_bgi_target_result_v1.json")


def test_m5_primary_bgi_result_is_unresolved_without_cross_channel_rescue():
    data = json.loads(PATH.read_text())
    assert data["candidate_id"] == "M5_T0"
    assert data["target_bgi_run"] == "SRR16954696"
    assert data["opening_gate"]["target_opening_allowed"] is True
    assert data["opening_gate"]["absence_max_ratio"] == 0.000818710126322
    assert data["opening_gate"]["presence_min_ratio"] == 0.40016549829

    ratios = data["target_measurement"]["normalized_marker_ratios"]
    states = data["target_measurement"]["marker_states"]
    assert states == {
        "SCO3879": "PRESENT",
        "SCO7036": "UNRESOLVED",
        "SCO7350": "ABSENT",
        "SCO7662": "ABSENT",
    }
    assert ratios["SCO7036"] > data["opening_gate"]["absence_max_ratio"]
    assert ratios["SCO7036"] < data["opening_gate"]["presence_min_ratio"]

    result = data["result"]
    assert result["marker_pattern_verified"] is False
    assert result["registered_class"] is None
    assert result["primary_bgi_class_status"] == "UNRESOLVED"
    assert set(result["blockers"]) == {
        "AT_LEAST_ONE_REGISTERED_MARKER_UNRESOLVED",
        "RIGHT_ARM_PATTERN_NOT_A_REGISTERED_D_CLASS",
    }

    cross = data["cross_channel_boundary"]
    assert cross["pacbio_four_locus_pattern_corroborates_deep_class"] is True
    assert cross["pacbio_may_rescue_primary_bgi_unresolved_call"] is False

    ceiling = data["claim_boundary"]
    assert ceiling["primary_bgi_marker_class_known"] is False
    assert ceiling["registered_deletion_class_qualified"] is False
    assert ceiling["qualified_d_reference"] is False
    assert ceiling["qualified_d_reference_count_increment"] == 0
    assert ceiling["architecture_specific_inference_open"] is False
