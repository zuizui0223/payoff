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
    assert "final_submission_eligible = false" in text
    assert "Aikens fixed-24h lambda adjudication" in text


def test_readiness_and_publication_status_reference_package_audit() -> None:
    ready = READY.read_text(encoding="utf-8")
    pub = PUB.read_text(encoding="utf-8")
    assert "PAYOFF_B_INTEGRATED_PREOUTCOME_PACKAGE_AUDIT_20260925.md" in ready
    assert "10856440257" in ready
    assert "Aikens fixed-24 h" in ready and "adjudication" in ready
    assert "LEGACY_V1_PREOUTCOME_ARTIFACT = 10856440257" in pub
    assert "LEGACY_V1_PREOUTCOME_BUILD_RUN = 36118090547" in pub
    assert "zero identity leaks" in pub
    assert "CURRENT_V2_PREOUTCOME_PACKAGE = READY" in pub
    assert "CURRENT_V2_PREOUTCOME_BUILD_RUN = 36472958953" in pub
    assert "CURRENT_V2_PREOUTCOME_ARTIFACT = 10992297519" in pub
    assert "CURRENT_V2_PREOUTCOME_ARCHIVE_SHA256 = d7b8227d65ef8968f06a49ebf7578bef3c647c7ad98e69dcab9d4593ee45c0b6" in pub
    assert "Aikens fixed-24 h" in pub and "adjudication" in pub
