import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data" / "payoff_b_ortega_variance_funnel_contract_20261003.json"
RESULT = ROOT / "data" / "payoff_b_ortega_variance_funnel_result_20261003.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_ortega_variance_funnel_source_and_scope_are_frozen():
    contract = load(CONTRACT)
    result = load(RESULT)
    assert result["frozen_submission_affected"] is False
    assert result["source"]["source_data_sha256"] == contract["source"]["source_data_sha256"]
    assert result["phase"]["n"] == 152
    assert result["bootstrap"]["unique_animals"] == 72
    assert result["bootstrap"]["replicates_completed"] == 10000


def test_ortega_phase_variance_funnel_is_directionally_robust():
    result = load(RESULT)
    assert result["phase"]["variance_ratio_end_over_start"] < 1.0
    assert result["phase"]["within_year_variance_ratio"] < 1.0
    assert result["bootstrap"]["variance_ratio_ci95"][1] < 1.0
    assert result["bootstrap"]["within_year_variance_ratio_ci95"][1] < 1.0


def test_ortega_signed_actuator_directions_hold_in_cluster_bootstrap():
    result = load(RESULT)
    boot = result["bootstrap"]
    assert boot["movement_rate_slope_ci95"][0] > 0.0
    assert boot["movement_rate_within_year_slope_ci95"][0] > 0.0
    assert boot["stopover_slope_ci95"][1] < 0.0
    assert boot["stopover_within_year_slope_ci95"][1] < 0.0


def test_ortega_result_does_not_claim_latent_controller_identification():
    result = load(RESULT)
    boundary = " ".join(result["boundaries"])
    assert "no K, g, phi, r or D_eff is estimated" in boundary
    assert "prior art" in boundary
