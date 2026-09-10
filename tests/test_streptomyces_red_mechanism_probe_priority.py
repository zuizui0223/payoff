import json
from pathlib import Path

from src.prospective_mechanism_probe import (
    ProspectiveMechanismProbeReceipt,
    adjudicate_prospective_mechanism_probe,
)


REGISTRY = Path("validation/streptomyces_red_mechanism_probe_priority_v1.json")


def data():
    return json.loads(REGISTRY.read_text())


def receipt(row):
    keys = {
        "matched_comparator_background_declared",
        "focal_mediator_perturbation_declared",
        "mediator_suppression_confirmed_declared",
        "gross_growth_comparable_declared",
        "gross_sporulation_comparable_declared",
        "direct_generation_rate_assay_available_in_principle_declared",
        "known_probe_specificity_caveat",
        "direct_generation_rate_reduction_measured_declared",
        "post_generation_realization_matched_declared",
        "net_task_preserved_declared",
        "stable_or_heritable_s_unit_declared",
        "independent_of_game_result_declared",
        "independent_of_raw_availability_declared",
    }
    return ProspectiveMechanismProbeReceipt(
        system_id="STREPTOMYCES_COELICOLOR",
        probe_id=row["probe_id"],
        comparator_id=row["comparator_id"],
        mediator_id=row["mediator_id"],
        support_reference=row["support_reference"],
        **{k: row[k] for k in keys},
    )


def test_registered_probe_statuses_recompute_exactly():
    d = data()
    ready = 0
    matched = 0
    for row in d["probes"]:
        result = adjudicate_prospective_mechanism_probe(receipt(row))
        assert result.mechanism_probe_ready == row["expected_mechanism_probe_ready"]
        assert result.matched_s_certified == row["expected_matched_s_certified"]
        ready += int(result.mechanism_probe_ready)
        matched += int(result.matched_s_certified)
        assert not result.generic_game_promoted
        assert not result.architecture_mapping_promoted
        assert not result.architecture_frequency_claim_promoted
    assert ready == d["mechanism_probe_ready_count"] == 2
    assert matched == d["matched_s_certified_count"] == 0


def test_m1141_m1142_is_ready_probe_but_not_matched_s():
    row = next(x for x in data()["probes"] if x["probe_id"].startswith("M1141_VS_M1142"))
    r = adjudicate_prospective_mechanism_probe(receipt(row))
    assert r.mechanism_probe_ready
    assert not r.matched_s_certified
    assert "DIFFERENTIATION_GENERATION_REDUCTION_NOT_MEASURED" in r.matched_s_blockers
    assert "POST_GENERATION_REALIZATION_NOT_MATCHED" in r.matched_s_blockers
    assert "NET_TASK_NOT_PRESERVED" in r.matched_s_blockers


def test_redu_is_ready_probe_with_polarity_caveat_but_not_matched_s():
    row = next(x for x in data()["probes"] if x["probe_id"] == "M145_VS_redU_SINGLE_MUTANT")
    r = adjudicate_prospective_mechanism_probe(receipt(row))
    assert r.mechanism_probe_ready
    assert "polar" in row["known_probe_specificity_caveat"].lower()
    assert not r.matched_s_certified


def test_redd_is_demoted_because_sporulation_state_is_not_comparable():
    row = next(x for x in data()["probes"] if x["probe_id"] == "M145_VS_M510_DELTA_redD")
    r = adjudicate_prospective_mechanism_probe(receipt(row))
    assert not r.mechanism_probe_ready
    assert "GROSS_SPORULATION_NOT_COMPARABLE" in r.probe_blockers
    assert not r.matched_s_certified


def test_probe_recovery_does_not_change_matched_s_claim_ceiling():
    d = data()
    assert d["claim_status"] == "PROSPECTIVE_RED_MECHANISM_PROBES_RECOVERED_MATCHED_S_NOT_YET_CERTIFIED"
    assert d["matched_s_certified_count"] == 0
