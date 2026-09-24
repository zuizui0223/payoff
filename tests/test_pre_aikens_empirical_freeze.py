import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "data" / "payoff_b_pre_aikens_empirical_freeze_20260924.json"
WIGEON = ROOT / "data" / "wigeon_era5_sourcefaithful_calibration_result_20260924.json"
BARNACLE = ROOT / "data" / "barnacle_era5_reliability_result_20260924.json"
RELIABILITY = ROOT / "data" / "payoff_b_cross_system_lambda_reliability_gate_20260924.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_pre_aikens_freeze_matches_wigeon_reliability_result():
    freeze=load(FREEZE)
    source=load(WIGEON)
    assert freeze["Aikens_lambda_outcome_opened"] is False
    assert freeze["wigeon"]["source_faithful_POWER_lambda_hat"] == source["controller_comparison"]["power"]["lambda_hat"]
    assert freeze["wigeon"]["ERA5_lambda_hat"] == source["controller_comparison"]["era5"]["lambda_hat"]
    assert freeze["wigeon"]["phase_contraction_replicated_across_environmental_surfaces"] is True
    assert freeze["wigeon"]["stopover_reconstruction_robust"] is False


def test_pre_aikens_freeze_matches_barnacle_reliability_result():
    freeze=load(FREEZE)
    source=load(BARNACLE)
    by_transition={row["transition"]:row for row in freeze["barnacle_goose"]["preregistered_ERA5_transitions"]}
    greenland=source["flyways"][0]
    barents=source["flyways"][1]
    assert by_transition["Greenland_R2_R3"]["POWER_lambda_hat"] == greenland["power"]["lambda_hat"]
    assert by_transition["Greenland_R2_R3"]["ERA5_lambda_hat"] == greenland["era5"]["lambda_hat"]
    assert by_transition["Barents_R1_R2"]["POWER_lambda_hat"] == barents["power"]["lambda_hat"]
    assert by_transition["Barents_R1_R2"]["ERA5_lambda_hat"] == barents["era5"]["lambda_hat"]
    assert all(row["response_reconstruction_robust"] for row in by_transition.values())
    assert all(row["actuator_reconstruction_robust"] for row in by_transition.values())


def test_pre_aikens_freeze_preserves_cross_system_claim_ceiling():
    freeze=load(FREEZE)
    gate=load(RELIABILITY)["gate"]
    assert freeze["cross_system_reliability"]["taxa_with_any_assumption_conditional_reliability_calibration"] == gate["taxa_with_any_reliability_calibration"] == 2
    assert freeze["cross_system_reliability"]["taxa_with_source_specific_error_identification"] == gate["taxa_with_source_specific_error_identification"] == 0
    assert freeze["cross_system_reliability"]["latent_magnitude_comparison_licensed"] is False
    assert gate["latent_magnitude_comparison_licensed"] is False


def test_geb_simulation_role_is_estimator_validation_not_generality_by_sweep_size():
    freeze=load(FREEZE)
    role=freeze["simulation_role_for_GEB"]
    assert "lambda estimator recovery" in role["use"]
    assert any("large synthetic coevolution sweeps" in row for row in role["exclude"])
    assert "mechanical fourth-taxon expansion" in freeze["explicitly_not_priority"]
