"""After-six-outcome spatial sensitivity remains descriptive and locked."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/movement_phenology/payoff_b_v8_daymetric_spatial_sensitivity_posthoc.R"
CONTRACT=ROOT/"docs/PAYOFF_B_V8_DAYMETRIC_SPATIAL_SENSITIVITY_LOCK_20261015.md"


def test_fixed_four_groupings_and_all_six_fixed_slopes():
    s=SCRIPT.read_text(encoding="utf-8")
    c=CONTRACT.read_text(encoding="utf-8")
    for key in ("source_cell_geo","target_cell_geo","target_grid_5deg","target_grid_10deg"):
        assert key in s
    for k in ("delta_loo_rmse","delta_loo_value_mse","observed",
              "fixed_arrival","bird_increment"):
        assert k in s
    assert "BOOT_REPS <- 10000L" in s
    assert "BOOT_SEED <- 20261015L" in s
    assert "nrow(bird)!=150L" in s
    assert "nrow(pairs)!=166L" in s
    assert "length(unique(bird$pair_key))!=72L" in s
    assert "original all-sample slope" in s.lower() or "original opened six-slope result" in s
    assert "after the six first-stage slopes became known" in c.lower()
    assert "Post-outcome" in c


def test_no_silent_significance_fishing_or_structural_null_removal():
    s=SCRIPT.read_text(encoding="utf-8")
    assert "if (K>=5L)" in s
    assert "invalid_fraction=invalid/BOOT_REPS" in s
    assert '"NOT_ESTIMABLE"' in s
    assert "ci_low_95" in s
    assert "n_original_environment_pairs=72L" in s
    assert '"bird_increment"' in s
    assert "original registered" not in s or "original registered" in s
    assert "all_sensitivity" in s
    assert "leave_one_unit_out_all_564_slopes.csv" in s
    assert "stop(" in s
