import pytest

from src.mechanism_probe_triangulation import (
    MechanismProbeOutcome,
    adjudicate_two_probe_triangulation,
)

P1 = "M1141_VS_M1142_RED_CLUSTER_DIFFERENCE"
P2 = "M145_VS_redU_SINGLE_MUTANT"
PRIMARY = (P1, P2)


def outcome(probe_id, result, **kwargs):
    data = dict(
        probe_id=probe_id,
        support_reference=f"RESULT_{probe_id}",
        generation_result=result,
        direct_generation_measurement_declared=True,
        post_generation_realization_separated_declared=True,
        predeclared_primary_probe=True,
    )
    data.update(kwargs)
    return MechanismProbeOutcome(**data)


def adjudicate(r1, r2, **kwargs):
    return adjudicate_two_probe_triangulation(
        (outcome(P1, r1, **kwargs), outcome(P2, r2, **kwargs)),
        primary_probe_ids=PRIMARY,
    )


def test_two_reductions_are_required_for_triangulated_support():
    r = adjudicate("reduced", "reduced")
    assert r.status == "TRIANGULATED_MEDIATOR_GENERATION_REDUCTION"
    assert r.mediator_generation_effect_triangulated
    assert r.reduced_probe_count == 2
    assert not r.matched_s_promoted
    assert not r.architecture_mapping_promoted
    assert not r.generic_game_promoted
    assert not r.architecture_frequency_claim_promoted


def test_two_material_exclusions_reject_registered_red_route():
    r = adjudicate("material_reduction_excluded", "material_reduction_excluded")
    assert r.status == "REGISTERED_MEDIATOR_ROUTE_NOT_SUPPORTED"
    assert r.registered_route_not_supported
    assert not r.mediator_generation_effect_triangulated


def test_opposite_interpretable_results_are_discordant_not_cherry_picked():
    r = adjudicate("reduced", "material_reduction_excluded")
    assert r.status == "PROBE_DISCORDANCE_MECHANISM_UNRESOLVED"
    assert r.probe_discordance
    assert not r.mediator_generation_effect_triangulated
    assert not r.registered_route_not_supported


def test_one_reduced_and_one_unresolved_is_not_triangulation():
    r = adjudicate("reduced", "unresolved")
    assert r.status == "INCOMPLETE_OR_UNRESOLVED_TRIANGULATION"
    assert r.reduced_probe_count == 1
    assert r.unresolved_probe_count == 1
    assert not r.mediator_generation_effect_triangulated


def test_non_direct_result_is_forced_to_unresolved_even_if_label_says_reduced():
    o1 = outcome(P1, "reduced", direct_generation_measurement_declared=False)
    o2 = outcome(P2, "reduced")
    r = adjudicate_two_probe_triangulation((o1, o2), primary_probe_ids=PRIMARY)
    assert r.status == "INCOMPLETE_OR_UNRESOLVED_TRIANGULATION"
    assert r.reduced_probe_count == 1
    assert r.unresolved_probe_count == 1


def test_failure_to_separate_post_generation_realization_is_forced_unresolved():
    o1 = outcome(P1, "reduced", post_generation_realization_separated_declared=False)
    o2 = outcome(P2, "reduced")
    r = adjudicate_two_probe_triangulation((o1, o2), primary_probe_ids=PRIMARY)
    assert not r.mediator_generation_effect_triangulated
    assert r.unresolved_probe_count == 1


def test_unregistered_or_duplicate_probe_cannot_replace_a_primary_probe():
    with pytest.raises(ValueError):
        adjudicate_two_probe_triangulation(
            (outcome(P1, "reduced"), outcome("OTHER", "reduced")),
            primary_probe_ids=PRIMARY,
        )
    with pytest.raises(ValueError):
        adjudicate_two_probe_triangulation(
            (outcome(P1, "reduced"), outcome(P1, "reduced")),
            primary_probe_ids=PRIMARY,
        )


def test_nonsignificance_must_not_be_encoded_as_material_exclusion_automatically():
    # The API intentionally has no `nonsignificant` category. Such a result must
    # first satisfy an external predeclared material-effect exclusion criterion,
    # otherwise it belongs in `unresolved`.
    with pytest.raises(ValueError):
        adjudicate_two_probe_triangulation(
            (outcome(P1, "nonsignificant"), outcome(P2, "reduced")),
            primary_probe_ids=PRIMARY,
        )
