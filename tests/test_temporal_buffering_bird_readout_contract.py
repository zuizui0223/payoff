from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "data" / "payoff_b_temporal_buffering_bird_holdout_registration_20260925.json"
SCRIPT = ROOT / "analysis" / "movement_phenology" / "temporal_buffering_bird_holdout.R"
WORKFLOW = ROOT / ".github" / "workflows" / "payoff-b-temporal-buffering-bird-readout.yml"


def test_readout_script_matches_frozen_primary_contract() -> None:
    reg = json.loads(REG.read_text(encoding="utf-8"))
    text = SCRIPT.read_text(encoding="utf-8")
    assert "MIN_CAL_OBS <- 60L" in text
    assert "MIN_CAL_CELLS <- 5L" in text
    assert "MIN_CAL_YEARS <- 5L" in text
    assert "MIN_BASELINE_OBS <- 3L" in text
    assert "MIN_ELIGIBLE_SPECIES <- 15L" in text
    assert "MIN_HOLDOUT_ROWS <- 1000L" in text
    assert "MIN_HOLDOUT_YEARS <- 5L" in text
    assert "MAX_P <- 0.05" in text
    assert "I(log_speed_ratio^2):z_timing_gain" in text
    assert 'result_status <- "PASS"' in text
    assert 'result_status <- "FAIL_WRONG_DIRECTION"' in text
    assert 'result_status <- "FAIL_INSUFFICIENT_SUPPORT"' in text
    assert 'result_status <- "NOT_ESTIMABLE"' in text
    assert reg["primary_model"]["primary_term"] == "I(log_speed_ratio^2):z_timing_gain"


def test_readout_workflow_cannot_run_on_analysis_script_push() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "data/payoff_b_temporal_buffering_bird_preflight_receipt_20260925.json" in text
    push_block = text.split("push:", 1)[1].split("jobs:", 1)[0]
    assert "analysis/movement_phenology/temporal_buffering_bird_holdout.R" not in push_block
    assert "Require frozen preflight receipt" in text
    assert '"outcome_columns_inspected": false' in text


def test_readout_uses_calibration_only_timing_gain() -> None:
    text = SCRIPT.read_text(encoding="utf-8")
    cal_pos = text.index("# Calibration-only timing gain")
    hold_pos = text.index("# Holdout response and inputs")
    gain_pos = text.index("lm(arrival_anomaly ~ greenup_anomaly")
    assert cal_pos < gain_pos < hold_pos
    assert "log_speed_ratio" not in text[cal_pos:gain_pos]
