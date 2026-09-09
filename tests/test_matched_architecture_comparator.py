import pytest

from src.matched_architecture_comparator import (
    MatchedArchitectureComparatorReceipt,
    adjudicate_matched_architecture_comparator,
)


def receipt(**overrides):
    base = dict(
        system_id="SYS",
        shared_candidate_id="S",
        differentiated_candidate_id="D",
        architecture_unit_id="COLONY",
        support_reference="TEST_V1",
        same_strategic_unit_level_declared=True,
        same_net_task_declared=True,
        matched_background_declared=True,
        focal_architecture_difference_isolated_declared=True,
        shared_generalist_only_state_verified_declared=True,
        differentiated_state_verified_declared=True,
        both_units_stable_over_assay_declared=True,
        common_task_assay_available_declared=True,
        comparator_selection_independent_of_game_result_declared=True,
        comparator_selection_independent_of_raw_availability_declared=True,
    )
    base.update(overrides)
    return MatchedArchitectureComparatorReceipt(**base)


def test_complete_matched_pair_certifies_without_promoting_game():
    r = adjudicate_matched_architecture_comparator(receipt())
    assert r.unit_match_certified
    assert r.contrast_isolation_certified
    assert r.matched_comparator_certified
    assert r.blockers == ()
    assert not r.generic_game_promoted
    assert not r.architecture_frequency_feedback_promoted


def test_strong_d_without_verified_s_does_not_certify_pair():
    r = adjudicate_matched_architecture_comparator(
        receipt(shared_generalist_only_state_verified_declared=False)
    )
    assert r.unit_match_certified
    assert not r.contrast_isolation_certified
    assert not r.matched_comparator_certified
    assert "SHARED_GENERALIST_ONLY_STATE_NOT_VERIFIED" in r.blockers


def test_large_background_change_blocks_matched_comparator():
    r = adjudicate_matched_architecture_comparator(
        receipt(
            matched_background_declared=False,
            focal_architecture_difference_isolated_declared=False,
        )
    )
    assert not r.contrast_isolation_certified
    assert "BACKGROUND_NOT_MATCHED" in r.blockers
    assert "FOCAL_ARCHITECTURE_DIFFERENCE_NOT_ISOLATED" in r.blockers


def test_cell_vs_colony_unit_mismatch_blocks_pair():
    r = adjudicate_matched_architecture_comparator(
        receipt(same_strategic_unit_level_declared=False)
    )
    assert not r.unit_match_certified
    assert "STRATEGIC_UNIT_LEVEL_NOT_MATCHED" in r.blockers


def test_common_task_and_stability_are_required():
    r = adjudicate_matched_architecture_comparator(
        receipt(
            same_net_task_declared=False,
            both_units_stable_over_assay_declared=False,
            common_task_assay_available_declared=False,
        )
    )
    assert not r.unit_match_certified
    assert "NET_TASK_NOT_MATCHED" in r.blockers
    assert "BOTH_UNITS_NOT_STABLE_OVER_ASSAY" in r.blockers
    assert "COMMON_TASK_ASSAY_NOT_AVAILABLE" in r.blockers


def test_game_outcome_cannot_be_used_to_choose_comparator():
    with pytest.raises(ValueError):
        adjudicate_matched_architecture_comparator(
            receipt(comparator_selection_independent_of_game_result_declared=False)
        )


def test_raw_availability_cannot_define_architecture_pair():
    with pytest.raises(ValueError):
        adjudicate_matched_architecture_comparator(
            receipt(comparator_selection_independent_of_raw_availability_declared=False)
        )


def test_same_candidate_id_rejected():
    with pytest.raises(ValueError):
        adjudicate_matched_architecture_comparator(
            receipt(differentiated_candidate_id="S")
        )
