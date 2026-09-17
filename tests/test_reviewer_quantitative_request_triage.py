from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC_SUFFIX = "." + "md"
TRIAGE = ROOT / "docs" / f"REVIEWER_QUANTITATIVE_REQUEST_TRIAGE_V1{DOC_SUFFIX}"
AUDIT = ROOT / "docs" / f"QUANTITATIVE_RESULTS_DISCUSSION_AUDIT_V1{DOC_SUFFIX}"


def test_reviewer_quantitative_triage_declares_decision_contract() -> None:
    text = TRIAGE.read_text(encoding="utf-8")
    assert "| Reviewer request | Decision | Quantitative value gained | Trigger / boundary |" in text
    for decision in ("DO_NOW", "DO_IF_REQUESTED", "DECLINE"):
        assert f"`{decision}`" in text


def test_payoff_triage_prioritizes_theorem_usability_not_sweeps() -> None:
    text = TRIAGE.read_text(encoding="utf-8")
    for token in (
        "asymptotic error table",
        "formula/implementation verification",
        "phase-lag or asymmetric migration",
        "broad parameter sweep",
        "field management calibration",
    ):
        assert token in text


def test_payoff_triage_preserves_benchmark_ceiling() -> None:
    audit = AUDIT.read_text(encoding="utf-8")
    triage = TRIAGE.read_text(encoding="utf-8")
    for token in (
        "FIELD_OPTIMUM_DISTRIBUTION = NOT_ESTIMATED",
        "CROSS_SYSTEM_EFFECT_SIZE = NOT_ESTIMATED",
        "Biological observations analyzed: none",
        "model prediction",
    ):
        assert token.lower() in audit.lower()
        assert token.lower() in triage.lower()
