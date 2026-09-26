import importlib.util
from pathlib import Path

import pandas as pd


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "payoff_b_cv24c_cue_driver.py"
)
spec = importlib.util.spec_from_file_location(
    "payoff_b_cv24c_cue_driver",
    MODULE_PATH,
)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def frame(years, values):
    return pd.DataFrame(
        {
            "target_year": years,
            "connectivity_rho": values,
        }
    )


def test_decline_then_recovery_passes_when_segmented_signal_is_strong():
    years = list(range(1988, 2011))
    values = []
    for year in years:
        if year < 1999:
            values.append(0.8 - 0.08 * (year - 1988))
        else:
            values.append(-0.08 + 0.07 * (year - 1999))

    result = module._detect_reversal(
        frame(years, values),
        min_segment_years=6,
    )

    assert result["status"] == "INFORMATION_REVERSAL"
    assert result["segmented"]["left_slope"] < 0
    assert result["segmented"]["right_slope"] > 0
    assert result["segmented"]["delta_aicc_vs_linear"] >= 4
    assert result["segmented"]["recovery_fraction"] >= 0.5


def test_peak_then_decline_is_not_misclassified_as_recovery():
    years = list(range(1988, 2011))
    values = []
    for year in years:
        if year < 1999:
            values.append(-0.5 + 0.07 * (year - 1988))
        else:
            values.append(0.27 - 0.06 * (year - 1999))

    result = module._detect_reversal(
        frame(years, values),
        min_segment_years=6,
    )

    assert result["status"] == "NO_CUE_DRIVER_REVERSAL"
    assert result["segmented"]["left_slope"] > 0
    assert result["segmented"]["right_slope"] < 0


def test_nearly_linear_connectivity_fails_aicc_gate():
    years = list(range(1988, 2011))
    values = [
        0.4 - 0.02 * (year - 1988)
        for year in years
    ]

    result = module._detect_reversal(
        frame(years, values),
        min_segment_years=6,
    )

    assert result["status"] == "NO_CUE_DRIVER_REVERSAL"


def test_history_model_is_not_opened_without_reversal_gate():
    annual = pd.DataFrame(
        {
            "year": list(range(1980, 2011)),
            "selection_gradient": [0.0] * 31,
        }
    )
    connectivity = frame(
        list(range(1988, 2011)),
        [0.1] * 23,
    )

    result = module._fit_history_if_licensed(
        annual,
        connectivity,
        {"status": "NO_CUE_DRIVER_REVERSAL"},
    )

    assert result["status"] == "NOT_RUN"
