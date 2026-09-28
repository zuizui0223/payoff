from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "payoff_b_hoge_veluwe_gate_b.py"
CONTRACT = ROOT / "data" / "payoff_b_hoge_veluwe_network_hysteresis_contract_20260927.json"
GATE_A = ROOT / "data" / "payoff_b_hoge_veluwe_source_gate_a_result_20260928.json"


def load_module():
    scripts = ROOT / "scripts"
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))
    spec = importlib.util.spec_from_file_location("hv_gate_b", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_clear_decline_recovery_geometry_passes_with_registered_penalty():
    pytest.importorskip("numpy")
    module = load_module()
    years = list(range(1992, 2016))
    rho = []
    for year in years:
        if year < 2004:
            rho.append(1.0 - 0.1 * (year - 1992))
        else:
            rho.append(-0.1 + 0.1 * (year - 2004))

    fit = module._fit_reversal_geometry(
        years,
        rho,
        min_segment_years=6,
    )

    assert fit["estimable"] is True
    assert fit["geometry_pass"] is True
    assert fit["linear"]["k"] == 2
    assert fit["segmented"]["k"] == 5
    assert fit["segmented"]["break_year"] == 2004
    assert fit["segmented"]["left_slope"] < 0
    assert fit["segmented"]["right_slope"] > 0
    assert fit["segmented"]["delta_aicc_vs_linear"] >= 4
    assert fit["segmented"]["recovery_fraction"] >= 0.5


def test_clear_decline_recovery_is_leave_one_year_out_stable():
    pytest.importorskip("numpy")
    module = load_module()
    years = list(range(1992, 2016))
    rho = [
        1.0 - 0.1 * (year - 1992)
        if year < 2004
        else -0.1 + 0.1 * (year - 2004)
        for year in years
    ]
    full = module._fit_reversal_geometry(
        years,
        rho,
        min_segment_years=6,
    )
    stability = module._leave_one_year_out_stability(
        years,
        rho,
        full_break_year=full["segmented"]["break_year"],
        min_segment_years=6,
        slope_fraction_threshold=0.8,
        break_fraction_threshold=0.8,
        break_tolerance_years=2,
    )

    assert stability["denominator"] == 24
    assert stability["passes"] is True
    assert stability["slope_sign_fraction"] >= 0.8
    assert stability["breakpoint_within_tolerance_fraction"] >= 0.8


def test_monotonic_connectivity_does_not_pass_reversal_geometry():
    pytest.importorskip("numpy")
    module = load_module()
    years = list(range(1992, 2016))
    rho = [-0.04 * (year - 1992) for year in years]

    fit = module._fit_reversal_geometry(
        years,
        rho,
        min_segment_years=6,
    )

    assert fit["estimable"] is True
    assert fit["geometry_pass"] is False
    assert not (
        fit["segmented"]["left_slope"] < 0
        and fit["segmented"]["right_slope"] > 0
    )


def test_gate_result_uses_registered_three_state_adjudication():
    pd = pytest.importorskip("pandas")
    module = load_module()
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    years = list(range(1992, 2016))

    monotonic = pd.DataFrame(
        {
            "target_year": years,
            "connectivity_rho": [
                -0.04 * (year - 1992)
                for year in years
            ],
        }
    )
    result = module._gate_result(monotonic, contract)
    assert result["status"] == "NO_CUE_RESOURCE_REVERSAL"
    assert result["gate_b_passed"] is False

    allowed = {
        "NO_CUE_RESOURCE_REVERSAL",
        "UNSTABLE_CUE_RESOURCE_REVERSAL",
        "INFORMATION_REVERSAL_STABLE",
    }
    assert result["status"] in allowed


def test_resource_reader_requires_exact_registered_year_set(tmp_path: Path):
    pd = pytest.importorskip("pandas")
    pytest.importorskip("openpyxl")
    module = load_module()

    path = tmp_path / "resource.xlsx"
    years = [year for year in range(1985, 2021) if year != 1991]
    pd.DataFrame(
        {
            "Year": years,
            "MidDate": [40.0 + (year % 5) for year in years],
        }
    ).to_excel(path, index=False)

    frame = module._read_resource(path)
    assert frame["year"].tolist() == years
    assert list(frame.columns) == ["year", "resource_peak_april_day"]


def test_frozen_gate_a_licenses_gate_b_but_not_gate_c():
    gate_a = json.loads(GATE_A.read_text(encoding="utf-8"))
    assert gate_a["gate_b_licensed"] is True
    assert gate_a["gate_c_licensed"] is False
    assert gate_a["outcome_firewall"]["cue_resource_connectivity_computed"] is False
    assert gate_a["outcome_firewall"]["history_test_opened"] is False


def test_contract_freezes_gate_b_before_environmental_outcome_opening():
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    gate = contract["information_reversal_gate"]
    assert gate["aicc_parameter_count"]["linear"] == 2
    assert gate["aicc_parameter_count"]["segmented"] == 5
    assert gate["breakpoint_tie_rule"].startswith("if candidate segmented AICc")
    assert gate["leave_one_history_year_out_stability_gate"]["required"] is True
    assert contract["source_gate"]["gate_b_can_run_without_history_sources"] is True
    amendment = contract["source_gate"]["gate_order_amendment_20260928"]
    assert amendment["outcome_data_inspected"] is False
