import pytest

from src.prospective_mechanism_probe import (
    ProspectiveMechanismProbeReceipt,
    adjudicate_prospective_mechanism_probe,
)


def ready_probe(**overrides):
    data = dict(
        system_id="TEST",
        probe_id="P",
        comparator_id="C",
        mediator_id="M",
        support_reference="SUPPORT",
        matched_comparator_background_declared=True,
        focal_mediator_perturbation_declared=True,
        mediator_suppression_confirmed_declared=True,
        gross_growth_comparable_declared=True,
        gross_sporulation_comparable_declared=True,
        direct_generation_rate_assay_available_in_principle_declared=True,
        known_probe_specificity_caveat="registered caveat",
        direct_generation_rate_reduction_measured_declared=False,
        post_generation_realization_matched_declared=False,
        net_task_preserved_declared=False,
        stable_or_heritable_s_unit_declared=False,
        independent_of_game_result_declared=True,
        independent_of_raw_availability_declared=True,
    )
    data.update(overrides)
    return ProspectiveMechanismProbeReceipt(**data)


def test_probe_can_be_ready_while_matched_s_remains_false():
    r = adjudicate_prospective_mechanism_probe(ready_probe())
    assert r.mechanism_probe_ready
    assert not r.matched_s_certified
    assert r.probe_blockers == ()
    assert set(r.matched_s_blockers) == {
        "DIFFERENTIATION_GENERATION_REDUCTION_NOT_MEASURED",
        "POST_GENERATION_REALIZATION_NOT_MATCHED",
        "NET_TASK_NOT_PRESERVED",
        "STABLE_OR_HERITABLE_S_UNIT_NOT_ESTABLISHED",
    }
    assert not r.generic_game_promoted
    assert not r.architecture_mapping_promoted
    assert not r.architecture_frequency_claim_promoted


def test_generation_rate_result_alone_still_does_not_make_matched_s():
    r = adjudicate_prospective_mechanism_probe(
        ready_probe(direct_generation_rate_reduction_measured_declared=True)
    )
    assert r.mechanism_probe_ready
    assert not r.matched_s_certified
    assert "DIFFERENTIATION_GENERATION_REDUCTION_NOT_MEASURED" not in r.matched_s_blockers
    assert "NET_TASK_NOT_PRESERVED" in r.matched_s_blockers


def test_full_hypothetical_matched_s_can_certify_only_after_all_extra_gates():
    r = adjudicate_prospective_mechanism_probe(
        ready_probe(
            direct_generation_rate_reduction_measured_declared=True,
            post_generation_realization_matched_declared=True,
            net_task_preserved_declared=True,
            stable_or_heritable_s_unit_declared=True,
        )
    )
    assert r.mechanism_probe_ready
    assert r.matched_s_certified
    assert r.matched_s_blockers == ()


def test_gross_developmental_pleiotropy_blocks_probe_readiness():
    r = adjudicate_prospective_mechanism_probe(
        ready_probe(gross_sporulation_comparable_declared=False)
    )
    assert not r.mechanism_probe_ready
    assert "GROSS_SPORULATION_NOT_COMPARABLE" in r.probe_blockers


def test_unmatched_background_blocks_probe_readiness():
    r = adjudicate_prospective_mechanism_probe(
        ready_probe(matched_comparator_background_declared=False)
    )
    assert not r.mechanism_probe_ready
    assert "COMPARATOR_BACKGROUND_NOT_MATCHED" in r.probe_blockers


def test_game_or_raw_dependent_probe_qualification_is_rejected():
    with pytest.raises(ValueError):
        adjudicate_prospective_mechanism_probe(
            ready_probe(independent_of_game_result_declared=False)
        )
    with pytest.raises(ValueError):
        adjudicate_prospective_mechanism_probe(
            ready_probe(independent_of_raw_availability_declared=False)
        )
