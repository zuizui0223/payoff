from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "QUANTITATIVE_CLAIM_LEDGER_V1.md"
MANUSCRIPT = ROOT / "manuscript" / "PAYOFF_B_THEORETICAL_ECOLOGY_BRIEF_V1.md"

CLASSES = (
    "EMPIRICAL",
    "LITERATURE-AUDIT",
    "THEORETICAL-WITNESS",
    "MODEL-PREDICTION",
    "NOT-ESTIMATED",
)


def test_quantitative_claim_ledger_declares_all_claim_classes() -> None:
    text = LEDGER.read_text(encoding="utf-8")
    for claim_class in CLASSES:
        assert f"`{claim_class}`" in text


def test_ledger_preserves_payoff_b_exact_predictions() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    tokens = (
        "1.60611529880277",
        "0.13248753945",
        "u_*(v)=1+\\frac1v+O(v^{-2})",
        "m_*\\tau\\to1",
        "unique global maximum",
    )
    for token in tokens:
        assert token in manuscript
        assert token in ledger


def test_ledger_marks_real_world_calibration_as_unestimated() -> None:
    text = LEDGER.read_text(encoding="utf-8")
    assert "FIELD_OPTIMUM_DISTRIBUTION = NOT_ESTIMATED" in text
    assert "CROSS_SYSTEM_EFFECT_SIZE = NOT_ESTIMATED" in text
    assert "symmetric two-patch, two-season anti-phase model" in text
