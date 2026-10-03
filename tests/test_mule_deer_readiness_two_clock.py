import json
from pathlib import Path


ROOT=Path(__file__).resolve().parents[1]
CLASSIFICATION=ROOT/"data"/"payoff_b_two_clock_classification_20261003.json"
READINESS=ROOT/"data"/"payoff_b_mule_deer_readiness_result_20261003.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_mule_deer_upgrades_to_candidate_hybrid_but_not_h2():
    rows={row["system"]:row for row in load(CLASSIFICATION)["systems"]}
    deer=rows["Ortega mule deer"]
    assert deer["timer"]=="T3_CANDIDATE"
    assert deer["decision"]=="D2"
    assert deer["hybrid"]=="H1_CANDIDATE"
    assert "H2" in deer["boundary"]


def test_readiness_temporal_gate_has_adequate_safe_sample():
    r=load(READINESS)
    assert r["schema"]["readiness_rows_with_joinable_fat_and_timing"]==93
    assert r["schema"]["temporally_safe_rows"]==62
    assert r["safe_primary"]["n"]==62
    assert r["safe_primary"]["animals"]==40


def test_primary_readiness_slope_passes_frozen_upgrade_rule():
    r=load(READINESS)
    lo,hi=r["safe_cluster_bootstrap"]["slope_ci95"]
    assert r["safe_primary"]["slope_std_start_per_scaledIFBFat"]<0
    assert hi<0
    assert r["classification"]["timer_upgrade_passes"] is True
    assert r["classification"]["licensed_timer_label"]=="T3_CANDIDATE"
    assert r["classification"]["licensed_hybrid_label"]=="H1_CANDIDATE"


def test_readiness_sensitivities_are_not_overclaimed():
    r=load(READINESS)
    lo,hi=r["safe_cluster_bootstrap"]["year_fe_slope_ci95"]
    slo,shi=r["safe_cluster_bootstrap"]["spearman_ci95"]
    assert lo<0<hi
    assert slo<0<shi
    assert any("H2" in x for x in r["boundaries"])


def test_no_system_is_claimed_as_h2():
    p=load(CLASSIFICATION)
    assert all(row["hybrid"]!="H2" for row in p["systems"])
    assert "H2" in p["global_boundary"]
