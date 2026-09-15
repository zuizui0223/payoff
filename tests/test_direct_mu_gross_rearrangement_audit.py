import pytest

from src.direct_mu_gross_rearrangement_audit import (
    GrossAuditEvidence,
    GrossEvent,
    adjudicate_gross_rearrangement_audit,
)


def make_evidence(**overrides):
    values = dict(
        candidate_id="M5_T0",
        target_pacbio_run="SRR16954720",
        wt_control_run="SRR16954715",
        reference_accession="NC_003888.3",
        coverage_bin_bp=10_000,
        gross_event_min_bp=50_000,
        m5_central_depth=100.0,
        wt_central_depth=100.0,
        coverage_segmentation_completed=True,
        left_terminal_boundary_resolved=True,
        right_terminal_boundary_resolved=True,
        long_read_sv_calling_completed=True,
        wt_control_processed_same_pipeline=True,
        all_detected_gross_events_catalogued=True,
        events=(
            GrossEvent("LEFT", "LEFT_TERMINAL_LOSS", 200_000, "DEPTH", True),
            GrossEvent("RIGHT", "RIGHT_TERMINAL_LOSS", 900_000, "DEPTH", True),
        ),
    )
    values.update(overrides)
    return GrossAuditEvidence(**values)


def test_resolved_means_catalogued_not_clean_genome():
    evidence = make_evidence(
        events=(
            GrossEvent("LEFT", "LEFT_TERMINAL_LOSS", 200_000, "DEPTH", True),
            GrossEvent("RIGHT", "RIGHT_TERMINAL_LOSS", 900_000, "DEPTH", True),
            GrossEvent("INV1", "INVERSION", 120_000, "SNIFFLES", True),
        )
    )
    result = adjudicate_gross_rearrangement_audit(evidence)
    assert result.audit_completed
    assert not result.gross_secondary_rearrangement_unresolved
    assert result.event_count == 3
    assert result.additional_gross_event_count == 1
    assert not result.qualified_d_reference


def test_unresolved_detected_event_keeps_reference_blocked():
    evidence = make_evidence(
        events=(GrossEvent("SV1", "INVERSION", 100_000, "SNIFFLES", False),)
    )
    result = adjudicate_gross_rearrangement_audit(evidence)
    assert not result.audit_completed
    assert result.gross_secondary_rearrangement_unresolved
    assert "GROSS_EVENT_UNRESOLVED:SV1" in result.blockers


def test_terminal_boundaries_are_mandatory_even_when_sv_calling_finished():
    result = adjudicate_gross_rearrangement_audit(
        make_evidence(right_terminal_boundary_resolved=False)
    )
    assert "RIGHT_TERMINAL_BOUNDARY_UNRESOLVED" in result.blockers


def test_wt_control_and_depth_floor_are_mandatory():
    result = adjudicate_gross_rearrangement_audit(
        make_evidence(wt_control_processed_same_pipeline=False, m5_central_depth=4.0)
    )
    assert "WT_CONTROL_NOT_PROCESSED_THROUGH_SAME_PIPELINE" in result.blockers
    assert "M5_CENTRAL_PACBIO_DEPTH_BELOW_FLOOR" in result.blockers


def test_incomplete_event_catalog_fails_closed():
    result = adjudicate_gross_rearrangement_audit(
        make_evidence(all_detected_gross_events_catalogued=False)
    )
    assert "DETECTED_GROSS_EVENTS_NOT_FULLY_CATALOGUED" in result.blockers


def test_wrong_target_or_resolution_contract_is_rejected():
    with pytest.raises(ValueError):
        adjudicate_gross_rearrangement_audit(make_evidence(candidate_id="M1_T0"))
    with pytest.raises(ValueError):
        adjudicate_gross_rearrangement_audit(make_evidence(coverage_bin_bp=20_000))
    with pytest.raises(ValueError):
        adjudicate_gross_rearrangement_audit(make_evidence(gross_event_min_bp=49_999))


def test_subthreshold_events_cannot_be_smuggled_into_gross_catalog():
    with pytest.raises(ValueError):
        adjudicate_gross_rearrangement_audit(
            make_evidence(events=(GrossEvent("tiny", "DEL", 40_000, "SNIFFLES", True),))
        )
