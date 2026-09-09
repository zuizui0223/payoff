import pytest

from src.consortium_strategic_unit import (
    ConsortiumStrategicUnitReceipt,
    adjudicate_consortium_strategic_unit,
)


def receipt(**overrides):
    base = dict(
        system_id="TEST_SYSTEM",
        candidate_unit_id="D_CONSORTIUM",
        support_reference="TEST_A_UNIT",
        member_set_predeclared=True,
        unit_boundary_predeclared=True,
        assembly_or_regeneration_protocol_declared=True,
        composition_state_reproducible_declared=True,
        propagation_or_transmission_declared=True,
        identity_retained_over_assay_horizon_declared=True,
        internal_composition_q_separated_from_external_frequency_p_declared=True,
        external_frequency_can_vary_whole_units_declared=True,
        unit_level_fitness_or_output_defined_declared=True,
        certification_independent_of_game_result_declared=True,
        certification_independent_of_raw_availability_declared=True,
    )
    base.update(overrides)
    return ConsortiumStrategicUnitReceipt(**base)


def test_all_subgates_are_required_for_strategic_unit_certification():
    r = adjudicate_consortium_strategic_unit(receipt())
    assert r.structural_identity_certified
    assert r.payoff_unit_alignment_certified
    assert r.strategic_unit_certified
    assert r.blockers == ()
    assert not r.architecture_mapping_promoted
    assert not r.generic_game_promoted


@pytest.mark.parametrize(
    "field, blocker",
    [
        ("member_set_predeclared", "MEMBER_SET_NOT_PREDECLARED"),
        ("unit_boundary_predeclared", "UNIT_BOUNDARY_NOT_PREDECLARED"),
        (
            "assembly_or_regeneration_protocol_declared",
            "ASSEMBLY_OR_REGENERATION_PROTOCOL_NOT_DECLARED",
        ),
        (
            "composition_state_reproducible_declared",
            "COMPOSITION_STATE_REPRODUCIBILITY_NOT_DECLARED",
        ),
        (
            "propagation_or_transmission_declared",
            "UNIT_PROPAGATION_OR_TRANSMISSION_NOT_DECLARED",
        ),
        (
            "identity_retained_over_assay_horizon_declared",
            "UNIT_IDENTITY_OVER_ASSAY_HORIZON_NOT_DECLARED",
        ),
        (
            "internal_composition_q_separated_from_external_frequency_p_declared",
            "INTERNAL_Q_NOT_SEPARATED_FROM_EXTERNAL_P",
        ),
        (
            "external_frequency_can_vary_whole_units_declared",
            "WHOLE_UNIT_EXTERNAL_FREQUENCY_NOT_DEFINED",
        ),
        (
            "unit_level_fitness_or_output_defined_declared",
            "UNIT_LEVEL_FITNESS_OR_OUTPUT_NOT_DEFINED",
        ),
    ],
)
def test_each_required_subgate_has_a_specific_blocker(field, blocker):
    r = adjudicate_consortium_strategic_unit(receipt(**{field: False}))
    assert not r.strategic_unit_certified
    assert blocker in r.blockers


def test_stable_internal_ratio_is_not_enough_if_external_whole_unit_frequency_is_undefined():
    r = adjudicate_consortium_strategic_unit(
        receipt(
            composition_state_reproducible_declared=True,
            external_frequency_can_vary_whole_units_declared=False,
        )
    )
    assert r.structural_identity_certified
    assert not r.payoff_unit_alignment_certified
    assert not r.strategic_unit_certified
    assert "WHOLE_UNIT_EXTERNAL_FREQUENCY_NOT_DEFINED" in r.blockers


def test_internal_member_frequency_cannot_be_reused_as_architecture_frequency():
    r = adjudicate_consortium_strategic_unit(
        receipt(
            internal_composition_q_separated_from_external_frequency_p_declared=False
        )
    )
    assert not r.payoff_unit_alignment_certified
    assert "INTERNAL_Q_NOT_SEPARATED_FROM_EXTERNAL_P" in r.blockers


def test_success_never_promotes_architecture_mapping_or_game_by_itself():
    r = adjudicate_consortium_strategic_unit(receipt())
    assert r.strategic_unit_certified
    assert not r.architecture_mapping_promoted
    assert not r.generic_game_promoted


def test_game_independence_is_a_hard_validation_rule():
    with pytest.raises(ValueError):
        adjudicate_consortium_strategic_unit(
            receipt(certification_independent_of_game_result_declared=False)
        )


def test_raw_availability_independence_is_a_hard_validation_rule():
    with pytest.raises(ValueError):
        adjudicate_consortium_strategic_unit(
            receipt(certification_independent_of_raw_availability_declared=False)
        )
