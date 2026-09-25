from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "submission" / "PAYOFF_B_INTEGRATED_PREOUTCOME_PACKAGE_AUDIT_20260925.md"
READY = ROOT / "submission" / "PAYOFF_B_INTEGRATED_PREOUTCOME_READINESS_20260925.md"
PUB = ROOT / "docs" / "PUBLICATION_STATUS.md"


def test_integrated_preoutcome_package_audit_is_canonical_and_blocked() -> None:
    text = AUDIT.read_text(encoding="utf-8")
    assert "run = 36118090547" in text
    assert "artifact_id = 10856440257" in text
    assert "b5628da1383960bdbbb637960d78d4f9c71588269f0ddee3111be37bba3fffc8" in text
    assert "file_count = 31" in text
    assert "figure_count = 6" in text
    assert "aikens_outcome_opened = false" in text
    assert "does **not** promote the package to final-submission eligibility" in text


def test_readiness_and_publication_status_reference_package_audit() -> None:
    ready = READY.read_text(encoding="utf-8")
    pub = PUB.read_text(encoding="utf-8")
    assert "PAYOFF_B_INTEGRATED_PREOUTCOME_PACKAGE_AUDIT_20260925.md" in ready
    assert "10851908495" in ready
    assert "Aikens fixed-24 h" in ready and "adjudication" in ready
    assert "10851908495" in pub
    assert "zero identity leaks" in pub
    assert "Aikens fixed-24 h" in pub and "adjudication" in pub
