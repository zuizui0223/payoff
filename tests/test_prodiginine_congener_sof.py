import pytest

from src.prodiginine_congener_sof import (
    ProdiginineCongenerProbeReceipt,
    adjudicate_prodiginine_congener_probe,
)


def make(**overrides):
    data = dict(
        probe_id="probe",
        support_reference="REF",
        same_background_declared=True,
        congener_profile_changed_declared=True,
        prodiginine_output_not_fully_abolished_declared=True,
        candidate_selected_before_mu_outcome_declared=True,
        gross_development_matched_declared=False,
        focal_antibacterial_task_preserved_declared=False,
        dna_damage_or_genotoxicity_difference_measured_declared=False,
        direct_mu_difference_measured_declared=False,
        focal_task_assay_same_context_declared=False,
        mu_assay_same_context_declared=False,
    )
    data.update(overrides)
    return ProdiginineCongenerProbeReceipt(**data)


def test_biochemical_probe_can_be_ready_without_sof_certification():
    r = adjudicate_prodiginine_congener_probe(make())
    assert r.biochemical_congener_probe_ready
    assert not r.task_preservation_supported
    assert not r.genotoxic_branch_supported
    assert not r.separation_of_function_certified
    assert "FOCAL_ANTIBACTERIAL_TASK_PRESERVATION_NOT_MEASURED" in r.blockers
    assert "GENOTOXICITY_DIFFERENCE_NOT_MEASURED" in r.blockers
    assert "DIRECT_MU_DIFFERENCE_NOT_MEASURED" in r.blockers


def test_full_sof_requires_task_and_genotoxic_mu_branches():
    r = adjudicate_prodiginine_congener_probe(
        make(
            gross_development_matched_declared=True,
            focal_antibacterial_task_preserved_declared=True,
            dna_damage_or_genotoxicity_difference_measured_declared=True,
            direct_mu_difference_measured_declared=True,
            focal_task_assay_same_context_declared=True,
            mu_assay_same_context_declared=True,
        )
    )
    assert r.separation_of_function_certified
    assert r.blockers == ()
    assert not r.matched_s_promoted
    assert not r.architecture_mapping_promoted
    assert not r.generic_game_promoted
    assert not r.eta_promoted
    assert not r.e1_promoted


def test_task_preservation_alone_is_not_sof():
    r = adjudicate_prodiginine_congener_probe(
        make(
            gross_development_matched_declared=True,
            focal_antibacterial_task_preserved_declared=True,
            focal_task_assay_same_context_declared=True,
        )
    )
    assert r.task_preservation_supported
    assert not r.genotoxic_branch_supported
    assert not r.separation_of_function_certified


def test_genotoxic_mu_branch_alone_is_not_sof():
    r = adjudicate_prodiginine_congener_probe(
        make(
            dna_damage_or_genotoxicity_difference_measured_declared=True,
            direct_mu_difference_measured_declared=True,
            mu_assay_same_context_declared=True,
        )
    )
    assert r.genotoxic_branch_supported
    assert not r.task_preservation_supported
    assert not r.separation_of_function_certified


def test_full_red_knockout_cannot_count_as_congener_probe():
    r = adjudicate_prodiginine_congener_probe(
        make(prodiginine_output_not_fully_abolished_declared=False)
    )
    assert not r.biochemical_congener_probe_ready
    assert not r.separation_of_function_certified


def test_posthoc_candidate_selection_rejected():
    with pytest.raises(ValueError):
        adjudicate_prodiginine_congener_probe(
            make(candidate_selected_before_mu_outcome_declared=False)
        )


@pytest.mark.parametrize("field", ["probe_id", "support_reference"])
def test_provenance_fields_required(field):
    kwargs = {field: " "}
    with pytest.raises(ValueError):
        adjudicate_prodiginine_congener_probe(make(**kwargs))
