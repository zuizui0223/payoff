from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "submission" / "GEB_INTEGRATED_PREOUTCOME_PACKAGE_AUDIT_20260925.md"
TARGETING = ROOT / "submission" / "PAYOFF_B_INTEGRATED_JOURNAL_TARGETING_20260925.md"
HANDOFF = ROOT / "submission" / "GEB_INTEGRATED_PORTAL_HANDOFF_PREOUTCOME.md"


def test_geb_preoutcome_package_audit_records_passing_artifact() -> None:
    text = AUDIT.read_text(encoding="utf-8")
    assert "run = 36117335501" in text
    assert "artifact_id = 10855522438" in text
    assert "fdb5e8aeaf912aa31368ce4690f74ff9b88bb0cc5ffa846312dcdd191c44815f" in text
    assert "596ebbf63860d8faf06eb95345ed1ec6b282d6d573a5d9a17514b2f9d532f750" in text
    assert "status = PASS" in text
    assert "structured_abstract_words = 241" in text
    assert "main_body_words = 3967" in text


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
