from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_payoff_b_asymptotic_error_table.py"
CSV = ROOT / "data" / "PAYOFF_B_ASYMPTOTIC_ERROR_TABLE_V1.csv"
DOC = ROOT / "docs" / "PAYOFF_B_ASYMPTOTIC_ERROR_TABLE_V1.md"

REGISTERED_V = (0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0)


def _load_module():
    assert SCRIPT.exists(), "PAYOFF-B asymptotic-error builder is missing"
    spec = importlib.util.spec_from_file_location("payoff_b_asymptotic_error", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_registered_error_table_uses_small_fixed_contrast_grid() -> None:
    module = _load_module()
    report = module.build_report()
    assert tuple(report["registered_v"]) == REGISTERED_V
    assert len(report["rows"]) == len(REGISTERED_V)
    assert report["role"] == "MODEL_PREDICTION_DIAGNOSTIC_NOT_THEOREM_PROOF"
    assert report["validity_cutoff_declared"] is False


def test_error_table_recovers_endpoint_convergence_without_arbitrary_cutoff() -> None:
    module = _load_module()
    report = module.build_report()
    by_v = {row["v"]: row for row in report["rows"]}

    assert by_v[0.1]["weak_u_relative_error_pct"] < 0.03
    assert by_v[10.0]["strong_u_relative_error_pct"] < 1.0
    assert by_v[100.0]["strong_u_relative_error_pct"] < 0.02

    assert by_v[0.01]["weak_max_F_relative_error_pct"] < 0.001
    assert by_v[10.0]["strong_max_F_relative_error_pct"] < 1.0
    assert by_v[100.0]["strong_max_F_relative_error_pct"] < 0.01


def test_rendered_error_receipts_preserve_claim_boundary() -> None:
    assert CSV.exists(), "PAYOFF-B asymptotic-error CSV is missing"
    assert DOC.exists(), "PAYOFF-B asymptotic-error Markdown receipt is missing"
    text = DOC.read_text(encoding="utf-8")
    for token in (
        "REGISTERED_V_POINTS = 9",
        "WEAK_U_RELATIVE_ERROR_AT_V_0.1_PCT",
        "STRONG_U_RELATIVE_ERROR_AT_V_10_PCT",
        "STRONG_U_RELATIVE_ERROR_AT_V_100_PCT",
        "no empirical calibration",
        "no validity cutoff",
        "MODEL-PREDICTION",
        "theorem does not depend on this table",
    ):
        assert token in text
