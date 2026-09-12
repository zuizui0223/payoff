import pytest

from src.direct_mu_single_reference_execution import (
    ClosedBand,
    DirectMuReferenceExecutionReceipt,
    adjudicate_reference_execution,
    ratio_band,
)


def _receipt(**overrides):
    values = dict(
        reference_id="M5_T0",
        deletion_class="ENTRY_CLASS",
        origin_cluster_id="ZHANG2022_SINGLE_MUTANT_PARENT",
        support_reference="ZHANG_ET_AL_2022_NAT_COMM_DOI_10.1038_s41467-022-29924-y",
        physical_stock_access_confirmed=True,
        marker_pattern_verified=True,
        core_reference_present=True,
        pre_existing_at_72h=True,
        same_medium_and_context=True,
        independently_derived_from_direct_mu_candidate_outcome=True,
        candidate_outcomes_used_for_selection=False,
        viable_at_72h=True,
        measurable_at_120h=True,
        gross_secondary_rearrangement_unresolved=False,
        measurement_unit="CALIBRATED_CORE_CHROMOSOME_EQUIVALENTS",
        interval_start_h=72.0,
        interval_end_h=120.0,
        context_id="SFM_DIRECT_MU_CONTEXT_V1",
        intact_comparator_id="M145_MATCHED_INTACT_REFERENCE",
        d_mass_72h=ClosedBand(90.0, 110.0),
        d_mass_120h=ClosedBand(135.0, 165.0),
    )
    values.update(overrides)
    return DirectMuReferenceExecutionReceipt(**values)


def test_ratio_band_uses_exact_opposite_corners():
    band = ratio_band(ClosedBand(135.0, 165.0), ClosedBand(90.0, 110.0))
    assert band.lower == pytest.approx(135.0 / 110.0)
    assert band.upper == pytest.approx(165.0 / 90.0)


def test_hypothetical_complete_m5_packet_can_qualify_one_reference():
    out = adjudicate_reference_execution(_receipt())
    assert out.quantitative_receipt_valid
    assert out.semantic_qualification.qualified
    assert out.qualified_reference
    assert out.blockers == ()
    assert out.d_realization_band is not None


def test_realization_band_cannot_be_created_from_zero_or_negative_start_mass():
    out = adjudicate_reference_execution(
        _receipt(d_mass_72h=ClosedBand(0.0, 110.0))
    )
    assert not out.quantitative_receipt_valid
    assert not out.qualified_reference
    assert "VALID_CLOSED_D_REALIZATION_BAND_NOT_DERIVABLE" in out.blockers
    assert "REALIZATION_BAND_NOT_AVAILABLE" in out.blockers


def test_wrong_interval_blocks_qualification_even_if_semantic_fields_pass():
    out = adjudicate_reference_execution(_receipt(interval_end_h=144.0))
    assert not out.quantitative_receipt_valid
    assert not out.qualified_reference
    assert "REALIZATION_INTERVAL_NOT_REGISTERED_72_TO_120_H" in out.blockers


def test_unverified_marker_pattern_blocks_qualification():
    out = adjudicate_reference_execution(_receipt(marker_pattern_verified=False))
    assert out.quantitative_receipt_valid
    assert not out.semantic_qualification.qualified
    assert not out.qualified_reference
    assert "REGISTERED_MARKER_PATTERN_NOT_VERIFIED" in out.blockers


def test_candidate_outcome_selection_blocks_reference():
    out = adjudicate_reference_execution(
        _receipt(candidate_outcomes_used_for_selection=True)
    )
    assert not out.qualified_reference
    assert "CANDIDATE_OUTCOME_USED_FOR_REFERENCE_SELECTION" in out.blockers


def test_gross_secondary_rearrangement_must_be_resolved():
    out = adjudicate_reference_execution(
        _receipt(gross_secondary_rearrangement_unresolved=True)
    )
    assert not out.qualified_reference
    assert "GROSS_SECONDARY_REARRANGEMENT_UNRESOLVED" in out.blockers
