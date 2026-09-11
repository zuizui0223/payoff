import json
from pathlib import Path


PATH = Path("validation/streptomyces_d_reference_candidate_pool_v1.json")


def data():
    return json.loads(PATH.read_text())


def classify(kb):
    if 178 < kb < 503:
        return "entry"
    if 503 <= kb < 841:
        return "intermediate"
    if kb >= 841:
        return "deep"
    return "not_registered_D"


def test_wgs_deletion_sizes_recompute_registered_class_counts():
    d = data()
    counts = {"entry": 0, "intermediate": 0, "deep": 0}
    for kb in d["zhang_2020_wgs_right_arm_deletion_kb"]:
        c = classify(kb)
        if c in counts:
            counts[c] += 1
    assert counts == d["zhang_2020_wgs_class_counts"] == {
        "entry": 1,
        "intermediate": 5,
        "deep": 2,
    }


def test_exact_wgs_pool_has_entry_shortfall_under_frozen_two_per_class_rule():
    d = data()
    minimum = d["minimum_independent_references_per_class"]
    counts = d["zhang_2020_wgs_class_counts"]
    assert counts["entry"] < minimum
    assert counts["intermediate"] >= minimum
    assert counts["deep"] >= minimum
    assert d["current_primary_bottleneck"] == "ENTRY_REFERENCE_SHORTFALL_IN_EXACTLY_CLASSIFIABLE_WGS_POOL"


def test_pfge_pool_is_candidate_source_not_exact_reference_panel_without_retyping():
    row = data()["additional_candidate_sources"]["zhang_2020_pfge_30_mutants"]
    assert row["available_as_candidate_source"]
    assert not row["exact_entry_vs_intermediate_assignable_without_SCO7350_retyping"]
    assert not row["qualified_reference_panel"]


def test_delta_ftsk_marker_class_support_cannot_be_promoted_across_backgrounds():
    row = data()["additional_candidate_sources"]["wang_2007_delta_ftsK_SC"]
    assert row["available_as_biological_marker_class_support"]
    assert not row["same_focal_background_for_realization_panel"]
    assert not row["qualified_reference_panel"]
    assert row["exclusion_reason"] == "BACKGROUND_MISMATCH_DELTA_FTSK_SC"


def test_candidate_recovery_does_not_equal_materialization_or_any_payoff_claim():
    d = data()
    status = d["status"]
    ceiling = d["claim_ceiling"]
    assert status["literature_candidate_pool_recovered"]
    assert not status["reference_panel_materialized"]
    assert not status["reference_panel_qualified"]
    assert not status["d_band_available"]
    assert not status["direct_mu_measurement_ready"]
    assert not any(ceiling.values())
