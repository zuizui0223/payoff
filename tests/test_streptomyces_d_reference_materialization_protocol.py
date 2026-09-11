import json
from pathlib import Path


PATH = Path("validation/streptomyces_d_reference_materialization_protocol_v1.json")


def data():
    return json.loads(PATH.read_text())


def test_primary_materialization_source_is_frozen_and_retyping_is_all_available_isolates():
    d = data()
    assert d["source_cohort_frozen_before_retyping"]
    assert d["source_cohort"] == "ZHANG_2020_M145_DERIVED_30_MUTANT_PFGE_PHENOTYPE_COHORT"
    assert d["retyping_scope"] == "ALL_PHYSICALLY_AVAILABLE_SOURCE_COHORT_ISOLATES"
    assert d["candidate_hunting_after_retyping_forbidden"]
    assert d["candidate_outcomes_may_not_influence_retyping_or_inclusion"]


def test_registered_marker_panel_and_class_definitions_are_predeclared():
    d = data()
    assert d["retyping_panel"] == [
        "SCO7662_cmlR2",
        "SCO7350",
        "SCO7036_argG",
        "SCO3879_dnaA_core",
    ]
    assert set(d["registered_classes"]) == {"entry", "intermediate", "deep"}
    assert d["minimum_independent_references_per_class"] == 2


def test_entry_shortfall_cannot_be_repaired_by_relaxing_or_posthoc_candidate_hunting():
    d = data()
    assert d["entry_shortfall_contingency"] == (
        "STOP_REFERENCE_PANEL_QUALIFICATION_DO_NOT_RELAX_MINIMUM_OR_POSTHOC_HUNT_NEW_COHORT"
    )
    assert not d["delta_ftsK_SC_may_substitute"]
    assert d["background_rule"] == "M145_DERIVED_ONLY_FOR_PRIMARY_PANEL"


def test_materialization_protocol_freeze_does_not_mean_materialization_or_result():
    d = data()
    status = d["current_status"]
    assert status["protocol_frozen_preoutcome"]
    assert not status["physical_source_cohort_availability_verified"]
    assert not status["retyping_executed"]
    assert not status["panel_materialized"]
    assert not status["panel_qualified"]
    assert not status["d_band_available"]
    assert not any(d["claim_ceiling"].values())
