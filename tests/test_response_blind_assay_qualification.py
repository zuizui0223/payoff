import pytest

from src.response_blind_assay_qualification import (
    CanonicalTaskScaleReceipt,
    ResponseBlindGenotoxicityQualificationReceipt,
    adjudicate_genotoxicity_assay,
)


def test_canonical_task_scale_requires_direct_function_and_preoutcome_freeze():
    r = CanonicalTaskScaleReceipt(
        scale_id="B_SUBTILIS_INHIBITION_ZONE_AREA_MM2",
        support_reference="ZHANG_2020_SCI_ADV",
        focal_task="external competitor inhibition",
        higher_is_better_declared=True,
        direct_external_function_readout_declared=True,
        assay_protocol_preoutcome_frozen=True,
        candidate_outcomes_used_to_select_scale=False,
        fitness_guardrail_kept_separate=True,
    )
    assert r.task_scale_qualified


def make_genotoxic(**overrides):
    data = dict(
        assay_id="candidate_assay",
        support_reference="QUALIFICATION_ONLY",
        focal_system_id="STREPTOMYCES_COELICOLOR",
        candidate_outcomes_blinded_declared=True,
        positive_genotoxic_control_declared=True,
        negative_control_declared=True,
        positive_control_response_certified=False,
        negative_control_specificity_certified=False,
        repeatability_certified=False,
        assay_direction_frozen_declared=False,
        assay_unit_frozen_declared=False,
        sampling_context_frozen_declared=False,
        distinct_from_direct_mu_outcome_declared=True,
        not_pigment_amount_only_declared=True,
        not_ros_amount_only_declared=True,
    )
    data.update(overrides)
    return ResponseBlindGenotoxicityQualificationReceipt(**data)


def test_unqualified_genotoxic_assay_stays_blocked_before_primary_outcomes():
    got = adjudicate_genotoxicity_assay(make_genotoxic())
    assert not got.qualified
    assert "POSITIVE_CONTROL_RESPONSE_NOT_CERTIFIED" in got.blockers
    assert "NEGATIVE_CONTROL_SPECIFICITY_NOT_CERTIFIED" in got.blockers
    assert "REPEATABILITY_NOT_CERTIFIED" in got.blockers
    assert not got.congener_outcomes_opened
    assert not got.matched_s_promoted
    assert not got.architecture_mapping_promoted
    assert not got.generic_game_promoted


def test_control_qualified_direct_damage_assay_can_define_scale_without_claim_promotion():
    got = adjudicate_genotoxicity_assay(
        make_genotoxic(
            positive_control_response_certified=True,
            negative_control_specificity_certified=True,
            repeatability_certified=True,
            assay_direction_frozen_declared=True,
            assay_unit_frozen_declared=True,
            sampling_context_frozen_declared=True,
        )
    )
    assert got.qualified
    assert got.blockers == ()
    assert not got.congener_outcomes_opened
    assert not got.matched_s_promoted
    assert not got.architecture_mapping_promoted
    assert not got.generic_game_promoted


def test_pigment_or_ros_only_readouts_are_not_genotoxicity_scales():
    pigment = adjudicate_genotoxicity_assay(
        make_genotoxic(not_pigment_amount_only_declared=False)
    )
    assert not pigment.qualified
    assert "PIGMENT_AMOUNT_ONLY_IS_NOT_GENOTOXICITY" in pigment.blockers

    ros = adjudicate_genotoxicity_assay(
        make_genotoxic(not_ros_amount_only_declared=False)
    )
    assert not ros.qualified
    assert "ROS_AMOUNT_ONLY_IS_NOT_GENOTOXICITY" in ros.blockers


def test_postoutcome_assay_selection_is_rejected():
    with pytest.raises(ValueError):
        adjudicate_genotoxicity_assay(
            make_genotoxic(candidate_outcomes_blinded_declared=False)
        )
