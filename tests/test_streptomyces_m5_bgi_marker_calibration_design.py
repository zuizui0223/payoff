import json
from pathlib import Path


PATH = Path("validation/streptomyces_m5_bgi_marker_calibration_design_v1.json")


def load():
    return json.loads(PATH.read_text())


def test_m5_runs_are_hard_excluded_from_calibration():
    data = load()
    target_runs = set(data["forbidden_target_runs_in_calibration"])
    assert target_runs == {"SRR16954720", "SRR16954696"}
    control_runs = {
        run
        for row in data["calibration_candidates"]
        for run in (row["pacbio_run"], row["bgi_run"])
    }
    assert not target_runs & control_runs
    assert data["target_bgi_ratios_opened_for_calibration"] is False


def test_all_non_m5_t0_controls_plus_wt_are_frozen():
    rows = load()["calibration_candidates"]
    assert [x["candidate_id"] for x in rows] == [
        "WT_ancestor", "M1_T0", "M2_T0", "M3_T0", "M4_T0", "M6_T0"
    ]
    assert [x["bgi_run"] for x in rows] == [
        "SRR16954701", "SRR16954700", "SRR16954699",
        "SRR16954698", "SRR16954697", "SRR16954695"
    ]


def test_core_panel_excludes_registered_markers():
    data = load()
    assert not set(data["central_core_panel"]) & set(data["registered_markers"])
    assert len(data["central_core_panel"]) == 9


def test_pacbio_labels_are_extreme_and_bgi_cutoff_is_fail_closed():
    data = load()
    labels = data["pacbio_control_label_rule"]
    assert labels["absent_control"] == "coverage_pct == 0"
    assert labels["present_control"] == "coverage_pct == 100"
    assert labels["otherwise"] == "CONTROL_STATE_UNRESOLVED"
    rule = data["threshold_rule"]
    assert rule["qualification_condition"] == "absence_max_ratio < presence_min_ratio"
    assert rule["touch_or_overlap"] == "CALIBRATION_NOT_QUALIFIED"


def test_calibration_does_not_promote_m5_or_architecture_claims():
    data = load()
    assert not data["calibration_qualified"]
    assert not data["m5_bgi_marker_class_opened"]
    ceiling = data["claim_ceiling"]
    assert not ceiling["m5_marker_class_qualified"]
    assert ceiling["qualified_d_reference_count_increment"] == 0
    assert not ceiling["architecture_specific_inference_open"]
    assert not ceiling["eta_architecture_specific"]
    assert not ceiling["e1"]
