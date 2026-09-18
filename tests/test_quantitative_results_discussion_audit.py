from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs" / "QUANTITATIVE_RESULTS_DISCUSSION_AUDIT_V1.md"
LEDGER = ROOT / "docs" / "QUANTITATIVE_CLAIM_LEDGER_V1.md"


def test_quantitative_results_discussion_audit_has_three_column_contract() -> None:
    text = AUDIT.read_text(encoding="utf-8")
    assert "| Qualitative claim | Quantitative claim licensed | Ceiling / not licensed |" in text


def test_audit_preserves_payoff_b_model_predictions() -> None:
    ledger = LEDGER.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")
    for token in (
        "1.60611529880277",
        "0.13248753945",
        "1+\\frac1v+O(v^{-2})",
        "m_*\\tau\\to1",
    ):
        assert token in ledger
        assert token in audit


def test_audit_keeps_field_calibration_unestimated() -> None:
    text = AUDIT.read_text(encoding="utf-8")
    assert "FIELD_OPTIMUM_DISTRIBUTION = NOT_ESTIMATED" in text
    assert "CROSS_SYSTEM_EFFECT_SIZE = NOT_ESTIMATED" in text
    assert "biological observations analyzed: none" in text.lower()
    assert "model prediction" in text.lower()


def test_audit_registers_asymptotic_error_checkpoints_without_validity_cutoff() -> None:
    ledger = LEDGER.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")
    for token in (
        "0.0226%",
        "0.933%",
        "0.00995%",
        "0.0144%",
        "0.736%",
        "0.00530%",
        "nine-point",
        "no validity cutoff",
        "MODEL-PREDICTION",
    ):
        assert token in ledger
        assert token in audit
