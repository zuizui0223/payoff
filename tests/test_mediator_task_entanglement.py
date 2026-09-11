import pytest

from src.mediator_task_entanglement import (
    MediatorTaskEntanglementReceipt,
    adjudicate_mediator_task_entanglement,
)


def receipt(**overrides):
    values = dict(
        system_id="TEST",
        mediator_id="M",
        perturbation_id="P",
        focal_task_id="TASK",
        support_reference="SUPPORT",
        perturbation_changes_mediator_declared=True,
        perturbation_changes_focal_task_output_declared=False,
        task_directly_preserved_declared=True,
        separation_of_function_intervention_declared=False,
        separation_of_function_preserves_task_declared=False,
        orthogonal_task_rescue_declared=False,
        orthogonal_task_rescue_verified_declared=False,
        rescue_independent_of_generation_path_declared=False,
        same_mediator_addback_only_declared=False,
        task_assay_same_context_declared=True,
        task_match_defined_before_game_outcome_declared=True,
        task_match_independent_of_frequency_game_declared=True,
    )
    values.update(overrides)
    return MediatorTaskEntanglementReceipt(**values)


def test_direct_preservation_can_qualify_task_match():
    r = adjudicate_mediator_task_entanglement(receipt())
    assert not r.mediator_task_entangled
    assert r.direct_task_preservation_qualified
    assert r.task_match_qualified
    assert r.blockers == ()


def test_entangled_mediator_knockout_does_not_qualify_without_rescue():
    r = adjudicate_mediator_task_entanglement(
        receipt(
            perturbation_changes_focal_task_output_declared=True,
            task_directly_preserved_declared=False,
        )
    )
    assert r.mediator_task_entangled
    assert not r.task_match_qualified
    assert "MEDIATOR_AND_TASK_OUTPUT_ENTANGLED" in r.blockers
    assert "NO_QUALIFIED_TASK_MATCH_ROUTE" in r.blockers


def test_separation_of_function_can_qualify_despite_entanglement():
    r = adjudicate_mediator_task_entanglement(
        receipt(
            perturbation_changes_focal_task_output_declared=True,
            task_directly_preserved_declared=False,
            separation_of_function_intervention_declared=True,
            separation_of_function_preserves_task_declared=True,
        )
    )
    assert r.mediator_task_entangled
    assert r.separation_of_function_qualified
    assert r.task_match_qualified


def test_verified_orthogonal_rescue_can_qualify_despite_entanglement():
    r = adjudicate_mediator_task_entanglement(
        receipt(
            perturbation_changes_focal_task_output_declared=True,
            task_directly_preserved_declared=False,
            orthogonal_task_rescue_declared=True,
            orthogonal_task_rescue_verified_declared=True,
            rescue_independent_of_generation_path_declared=True,
        )
    )
    assert r.orthogonal_rescue_qualified
    assert r.task_match_qualified


def test_same_mediator_addback_cannot_be_relabeled_orthogonal():
    with pytest.raises(ValueError):
        adjudicate_mediator_task_entanglement(
            receipt(
                perturbation_changes_focal_task_output_declared=True,
                task_directly_preserved_declared=False,
                orthogonal_task_rescue_declared=True,
                orthogonal_task_rescue_verified_declared=True,
                rescue_independent_of_generation_path_declared=True,
                same_mediator_addback_only_declared=True,
            )
        )


def test_unverified_orthogonal_rescue_stays_blocked():
    r = adjudicate_mediator_task_entanglement(
        receipt(
            perturbation_changes_focal_task_output_declared=True,
            task_directly_preserved_declared=False,
            orthogonal_task_rescue_declared=True,
            orthogonal_task_rescue_verified_declared=False,
            rescue_independent_of_generation_path_declared=False,
        )
    )
    assert not r.task_match_qualified
    assert "ORTHOGONAL_TASK_RESCUE_NOT_VERIFIED" in r.blockers
    assert "RESCUE_INDEPENDENCE_FROM_GENERATION_PATH_NOT_VERIFIED" in r.blockers


def test_gate_never_promotes_architecture_or_game_by_itself():
    r = adjudicate_mediator_task_entanglement(receipt())
    assert not r.matched_s_promoted
    assert not r.architecture_mapping_promoted
    assert not r.generic_game_promoted
    assert not r.eta_identified
    assert not r.e1_promoted


def test_game_independence_is_mandatory():
    with pytest.raises(ValueError):
        adjudicate_mediator_task_entanglement(
            receipt(task_match_independent_of_frequency_game_declared=False)
        )
