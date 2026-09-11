import pytest

from src.mechanism_to_architecture_promotion import (
    MechanismToArchitecturePromotionReceipt,
    adjudicate_mechanism_to_architecture_promotion,
)


def make_receipt(**overrides):
    values = dict(
        system_id="TEST",
        mechanism_id="M",
        candidate_shared_id="S",
        candidate_differentiated_id="D",
        support_reference="TEST_SUPPORT",
        triangulated_generation_reduction_declared=True,
        preoutcome_probe_rule_respected_declared=True,
        candidate_shared_unit_exists_declared=True,
        same_strategic_unit_level_declared=True,
        same_net_task_preserved_or_rescued_declared=True,
        task_match_independent_of_differentiation_mechanism_declared=True,
        matched_background_declared=True,
        focal_architecture_difference_isolated_declared=True,
        shared_generalist_only_state_verified_declared=True,
        differentiated_state_verified_declared=True,
        both_units_stable_over_assay_declared=True,
        promotion_independent_of_game_result_declared=True,
        promotion_independent_of_raw_availability_declared=True,
    )
    values.update(overrides)
    return MechanismToArchitecturePromotionReceipt(**values)


def test_gate_can_open_in_principle_only_when_mechanism_and_architecture_counterfactual_both_pass():
    result = adjudicate_mechanism_to_architecture_promotion(make_receipt())
    assert result.mechanism_support_certified
    assert result.task_matched_architecture_counterfactual_certified
    assert result.matched_s_promotion_licensed
    assert result.blockers == ()
    assert not result.generic_game_promoted
    assert not result.eta_identified
    assert not result.e1_promoted


def test_positive_mechanism_is_not_enough_when_net_task_changes():
    result = adjudicate_mechanism_to_architecture_promotion(
        make_receipt(same_net_task_preserved_or_rescued_declared=False)
    )
    assert result.mechanism_support_certified
    assert not result.task_matched_architecture_counterfactual_certified
    assert not result.matched_s_promotion_licensed
    assert "NET_TASK_NOT_PRESERVED_OR_RESCUED" in result.blockers


def test_positive_mechanism_is_not_enough_without_matched_shared_unit():
    result = adjudicate_mechanism_to_architecture_promotion(
        make_receipt(
            candidate_shared_unit_exists_declared=False,
            shared_generalist_only_state_verified_declared=False,
        )
    )
    assert result.mechanism_support_certified
    assert not result.matched_s_promotion_licensed
    assert "MATCHED_SHARED_UNIT_NOT_RECOVERED" in result.blockers
    assert "SHARED_GENERALIST_ONLY_STATE_NOT_VERIFIED" in result.blockers


def test_architecture_counterfactual_is_not_enough_without_triangulated_mechanism_result():
    result = adjudicate_mechanism_to_architecture_promotion(
        make_receipt(triangulated_generation_reduction_declared=False)
    )
    assert not result.mechanism_support_certified
    assert result.task_matched_architecture_counterfactual_certified
    assert not result.matched_s_promotion_licensed
    assert "TRIANGULATED_GENERATION_REDUCTION_NOT_ESTABLISHED" in result.blockers


def test_game_result_cannot_be_used_to_choose_architecture_mapping():
    with pytest.raises(ValueError):
        adjudicate_mechanism_to_architecture_promotion(
            make_receipt(promotion_independent_of_game_result_declared=False)
        )


def test_raw_availability_cannot_choose_architecture_mapping():
    with pytest.raises(ValueError):
        adjudicate_mechanism_to_architecture_promotion(
            make_receipt(promotion_independent_of_raw_availability_declared=False)
        )


def test_candidate_ids_must_be_distinct():
    with pytest.raises(ValueError):
        adjudicate_mechanism_to_architecture_promotion(
            make_receipt(candidate_shared_id="D")
        )
