from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "data" / "payoff_b_temporal_buffering_bird_holdout_registration_20260925.json"
PREFLIGHT = ROOT / "analysis" / "movement_phenology" / "temporal_buffering_bird_preflight.R"


def test_temporal_buffering_bird_registration_is_frozen_before_readout() -> None:
    payload = json.loads(REG.read_text(encoding="utf-8"))
    assert payload["status"] == "FROZEN_BEFORE_HOLDOUT_READOUT"
    assert payload["hypothesis"]["primary_parameter"] == "beta_q2_x_timing_gain"
    assert payload["hypothesis"]["expected_direction"] == "negative"
    assert payload["split_rule"]["retuning_after_preflight"] is False
    assert payload["primary_model"]["support_gate"] == {
        "direction": "coefficient < 0",
        "max_p_value": 0.05,
    }
    assert payload["estimability_gate"]["min_eligible_species"] == 15
    assert payload["estimability_gate"]["min_holdout_rows"] == 1000


def test_preflight_cannot_open_tracking_outcomes() -> None:
    text = PREFLIGHT.read_text(encoding="utf-8")
    for forbidden in (
        "arr_GAM_mean",
        "gr_mn",
        "vArrMag",
        "vGrMag",
        "signed_lag",
        "abs_mismatch",
        "log_speed_ratio",
    ):
        assert forbidden not in text
    assert 'required <- c("year", "species", "cell")' in text
    assert "outcome_columns_inspected=FALSE" in text
