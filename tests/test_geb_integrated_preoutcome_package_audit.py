from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "submission" / "GEB_INTEGRATED_PREOUTCOME_PACKAGE_AUDIT_20260925.md"
TARGETING = ROOT / "submission" / "PAYOFF_B_INTEGRATED_JOURNAL_TARGETING_20260925.md"
HANDOFF = ROOT / "submission" / "GEB_INTEGRATED_PORTAL_HANDOFF_PREOUTCOME.md"


def test_geb_preoutcome_package_audit_records_passing_artifact() -> None:
    text = AUDIT.read_text(encoding="utf-8")
    assert "run = 36109813368" in text
    assert "artifact_id = 10852587229" in text
    assert "d5ac9123d9d90b4216d37b02b42db543f4d93443f254cc7fb3c035653d51580d" in text
    assert "5a7743af95734532b6f3515c09ea3493584b9f9617dda3b949962c078e8469cf" in text
    assert "run = 36109813351" in text
    assert "status = PASS" in text
    assert "structured_abstract_words = 222" in text
    assert "main_body_words = 3690" in text


def test_geb_first_shot_and_blockers_are_synchronized() -> None:
    targeting = TARGETING.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")
    assert "FIRST_SHOT = Global Ecology and Biogeography / Research Article" in targeting
    assert "JOURNAL = Global Ecology and Biogeography" in handoff
    for phrase in (
        "Aikens",
        "anonymous stable reviewer archive link",
        "author-controlled title-page",
    ):
        assert phrase in audit
