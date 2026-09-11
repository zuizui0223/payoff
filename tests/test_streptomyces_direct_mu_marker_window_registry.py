import json
from pathlib import Path

from src.direct_mu_marker_window import (
    DirectMuMarkerWindowReceipt,
    adjudicate_direct_mu_marker_window,
)


PATH = Path("validation/streptomyces_direct_mu_marker_window_v1.json")


def load_receipt():
    return json.loads(PATH.read_text())


def recompute(data):
    entry = data["state_channel"]["entry_marker"]
    severity = data["state_channel"]["severity_markers"]
    core = data["state_channel"]["core_reference"]
    window = data["primary_interval"]
    realization = data["realization_channel"]
    calibration = data["dosage_calibration"]
    return DirectMuMarkerWindowReceipt(
        entry_marker_id=f'{entry["locus"]}_{entry["gene"]}_{entry["approx_distance_from_right_end_kb"]}kb_from_right_end',
        intermediate_marker_id=f'{severity[0]["locus"]}_{severity[0]["approx_distance_from_right_end_kb"]}kb_from_right_end',
        deep_marker_id=f'{severity[1]["locus"]}_{severity[1]["gene"]}_{severity[1]["approx_distance_from_right_end_kb"]}kb_from_right_end',
        core_reference_id=f'{core["locus"]}_{core["gene"]}_{core["region"]}',
        start_hour=window["start_hour"],
        end_hour=window["end_hour"],
        whole_biomass_state_channel_declared=data["state_channel"]["whole_biomass_state_channel_declared"],
        genotype_time_matched_intact_baseline_declared=(
            calibration["baseline"]
            == "genotype_and_time_matched_intact_baseline_verified_present_at_all_registered_markers"
        ),
        terminal_core_dosage_calibration_declared=calibration["required"],
        entry_marker_nearest_terminal_declared=(
            entry["approx_distance_from_right_end_kb"]
            < severity[0]["approx_distance_from_right_end_kb"]
        ),
        severity_order_declared=(
            entry["approx_distance_from_right_end_kb"]
            < severity[0]["approx_distance_from_right_end_kb"]
            < severity[1]["approx_distance_from_right_end_kb"]
        ),
        candidate_outcomes_used_to_select_panel=data["state_channel"]["candidate_outcomes_used_to_select_panel"],
        candidate_outcomes_used_to_select_window=window["candidate_outcomes_used_to_select_window"],
        realization_channel_independent_declared=realization["independent_from_final_state_fraction_required"],
        realization_channel_frozen_preoutcome=realization["frozen_preoutcome"],
    )


def test_registry_recomputes_frozen_state_channel_but_not_full_mu_readiness():
    data = load_receipt()
    receipt = recompute(data)
    state_ready, full_ready, blockers = adjudicate_direct_mu_marker_window(receipt)
    assert state_ready is data["adjudication"]["state_channel_frozen"] is True
    assert full_ready is data["adjudication"]["direct_mu_fully_ready"] is False
    assert blockers == ("REALIZATION_CHANNEL_NOT_FROZEN",)


def test_registered_deletion_ladder_is_monotone_from_terminal_to_deep():
    data = load_receipt()
    entry = data["state_channel"]["entry_marker"]
    severity = data["state_channel"]["severity_markers"]
    distances = [
        entry["approx_distance_from_right_end_kb"],
        severity[0]["approx_distance_from_right_end_kb"],
        severity[1]["approx_distance_from_right_end_kb"],
    ]
    assert distances == [178, 503, 841]
    assert distances == sorted(distances)
    assert data["state_channel"]["entry_and_severity_kept_distinct"]


def test_primary_interval_is_first_registered_adjacent_time_course_interval():
    window = load_receipt()["primary_interval"]
    assert (window["start_hour"], window["end_hour"], window["duration_hours"]) == (72, 120, 48)
    assert window["frozen_preoutcome"]
    assert not window["candidate_outcomes_used_to_select_window"]


def test_dosage_calibration_is_genotype_and_time_matched_not_universal_m145_only():
    calibration = load_receipt()["dosage_calibration"]
    assert calibration["required"]
    assert not calibration["universal_M145_only_baseline_sufficient"]
    assert "genotype_and_time_matched" in calibration["baseline"]


def test_claim_ceiling_remains_unpromoted():
    ceiling = load_receipt()["claim_ceiling"]
    assert not ceiling["direct_mu_outcome_available"]
    assert not ceiling["matched_generalist_shared_architecture_recovered"]
    assert not ceiling["matched_s_certified"]
    assert not ceiling["architecture_mapping_certified"]
    assert not ceiling["generic_game_promoted"]
    assert not ceiling["eta_promoted"]
    assert not ceiling["e1_promoted"]
