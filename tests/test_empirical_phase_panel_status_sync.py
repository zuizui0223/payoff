import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "data" / "payoff_b_empirical_phase_panel_status_20260921.json"
RELIABILITY = ROOT / "data" / "payoff_b_cross_system_lambda_reliability_gate_20260924.json"
STANDARD = ROOT / "data" / "payoff_b_phase_retention_interval_standardization_result_20260925.json"
DOC = ROOT / "docs" / "PAYOFF_B_EMPIRICAL_PHASE_PANEL_STATUS_20260921.md"
README = ROOT / "README.md"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_current_panel_status_matches_canonical_reliability_gate():
    status = load(STATUS)
    gate = load(RELIABILITY)["gate"]
    m = status["measurement_error_status"]

    assert m["taxa_with_any_reliability_calibration"] == gate["taxa_with_any_reliability_calibration"] == 2
    assert m["source_specific_error_identified_taxa"] == gate["taxa_with_source_specific_error_identification"] == 0
    assert m["cross_system_latent_magnitude_comparison_licensed"] is False
    assert m["barnacle_goose_reliability_calibration"]["status"] == "COMPLETE_ASSUMPTION_CONDITIONAL"


def test_current_panel_status_uses_interval_standardization_as_secondary():
    status = load(STATUS)
    standard = load(STANDARD)
    m = status["measurement_error_status"]["interval_standardization"]

    assert m["status"] == standard["status"]
    assert m["role"] == "secondary_cross_system_comparison_only"
    assert m["raw_lambda_role"] == "system_specific_primary_segment_scale_estimator"
    assert m["universal_migration_wide_correction_fraction_licensed"] is False
    assert 0.13 < m["wigeon_power_typical_path_retention"] < 0.14
    assert 0.23 < m["wigeon_era5_typical_path_retention"] < 0.24
    assert 0.62 < m["wigeon_conservative_simex_typical_path_retention"] < 0.63


def test_broad_bird_falsification_is_primary_cross_system_result():
    status = load(STATUS)
    broad = status["broad_bird_falsification"]
    assert broad["observations"] == 5816
    assert broad["species"] == 55
    assert broad["universal_speed_ratio_supported"] is False
    assert broad["primary_cross_system_result"] is True


def test_current_status_surfaces_do_not_restore_old_raw_lambda_claim():
    doc = DOC.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")

    assert "phase retention is a portable response coordinate across migratory systems" not in doc
    assert "Broad falsification is the primary cross-system result" in doc
    assert "raw lambda magnitudes are interval-scale" in doc.lower()

    assert "lambda = 0.85994" not in readme
    assert "POWER lambda = 0.749768" in readme
    assert "ERA5  lambda = 0.811312" in readme
    assert "R_path(7) = 0.133" in readme
    assert "Raw lambda is nevertheless **segment-scale dependent**" in readme
