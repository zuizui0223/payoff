import pytest

from src.direct_mu_marker_reconstruction import (
    MarkerReconstructionInput,
    reconstruct_registered_marker_pattern,
)


def make_input(**overrides):
    values = dict(
        candidate_id="M5_T0",
        sequence_sample_map_qualified=True,
        primary_short_read_run="SRR16954696",
        reference_accession="NC_003888.3",
        normalization_panel_id="FROZEN_CENTRAL_CORE_PANEL_V1",
        thresholds_frozen_preoutcome=True,
        absence_max_ratio=0.10,
        presence_min_ratio=0.80,
        normalized_marker_ratios={
            "SCO7662": 0.01,
            "SCO7350": 0.02,
            "SCO7036": 0.01,
            "SCO3879": 1.00,
        },
    )
    values.update(overrides)
    return MarkerReconstructionInput(**values)


def test_exact_deep_pattern_can_be_verified_only_with_all_gates():
    result = reconstruct_registered_marker_pattern(make_input())
    assert result.marker_pattern_verified
    assert result.registered_class == "DEEP_CLASS"
    assert result.marker_states == {
        "SCO7662": "ABSENT",
        "SCO7350": "ABSENT",
        "SCO7036": "ABSENT",
        "SCO3879": "PRESENT",
    }
    assert result.blockers == ()
    assert not result.physical_material_identity_established
    assert not result.gross_rearrangement_audit_completed
    assert not result.realization_band_available
    assert not result.reference_qualified


def test_gray_zone_is_unresolved_not_forced_to_present_or_absent():
    inp = make_input(
        normalized_marker_ratios={
            "SCO7662": 0.01,
            "SCO7350": 0.40,
            "SCO7036": 0.01,
            "SCO3879": 1.00,
        }
    )
    result = reconstruct_registered_marker_pattern(inp)
    assert result.marker_states["SCO7350"] == "UNRESOLVED"
    assert not result.marker_pattern_verified
    assert result.registered_class is None
    assert "AT_LEAST_ONE_REGISTERED_MARKER_UNRESOLVED" in result.blockers


def test_core_loss_or_unresolved_core_blocks_registered_class():
    inp = make_input(
        normalized_marker_ratios={
            "SCO7662": 0.01,
            "SCO7350": 0.01,
            "SCO7036": 0.01,
            "SCO3879": 0.02,
        }
    )
    result = reconstruct_registered_marker_pattern(inp)
    assert not result.marker_pattern_verified
    assert "CORE_SCO3879_NOT_VERIFIED_PRESENT" in result.blockers


def test_sample_mapping_must_be_qualified_before_sequence_call_is_admissible():
    result = reconstruct_registered_marker_pattern(make_input(sequence_sample_map_qualified=False))
    assert not result.marker_pattern_verified
    assert "SEQUENCE_SAMPLE_MAP_NOT_QUALIFIED" in result.blockers


def test_thresholds_must_be_frozen_before_marker_outcomes():
    result = reconstruct_registered_marker_pattern(make_input(thresholds_frozen_preoutcome=False))
    assert not result.marker_pattern_verified
    assert "MARKER_CALL_THRESHOLDS_NOT_FROZEN_PREOUTCOME" in result.blockers


def test_registered_entry_and_intermediate_patterns_are_distinct():
    entry = reconstruct_registered_marker_pattern(
        make_input(
            normalized_marker_ratios={
                "SCO7662": 0.01,
                "SCO7350": 0.95,
                "SCO7036": 0.98,
                "SCO3879": 1.00,
            }
        )
    )
    assert entry.registered_class == "ENTRY_CLASS"

    intermediate = reconstruct_registered_marker_pattern(
        make_input(
            normalized_marker_ratios={
                "SCO7662": 0.01,
                "SCO7350": 0.02,
                "SCO7036": 0.98,
                "SCO3879": 1.00,
            }
        )
    )
    assert intermediate.registered_class == "INTERMEDIATE_CLASS"


def test_non_D_pattern_does_not_get_a_registered_class():
    result = reconstruct_registered_marker_pattern(
        make_input(
            normalized_marker_ratios={
                "SCO7662": 0.95,
                "SCO7350": 0.95,
                "SCO7036": 0.95,
                "SCO3879": 1.00,
            }
        )
    )
    assert result.registered_class is None
    assert not result.marker_pattern_verified
    assert "RIGHT_ARM_PATTERN_NOT_A_REGISTERED_D_CLASS" in result.blockers


def test_invalid_threshold_order_is_rejected():
    with pytest.raises(ValueError):
        reconstruct_registered_marker_pattern(make_input(absence_max_ratio=0.8, presence_min_ratio=0.1))


def test_missing_or_extra_markers_are_rejected():
    with pytest.raises(ValueError):
        reconstruct_registered_marker_pattern(
            make_input(normalized_marker_ratios={"SCO7662": 0.0, "SCO3879": 1.0})
        )
