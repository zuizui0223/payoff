from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "manuscript" / "PAYOFF_B_INFORMATION_COORDINATION_V2_PREOUTCOME.md"
STATUS = ROOT / "docs" / "PUBLICATION_STATUS.md"
RELATION = ROOT / "docs" / "PAYOFF_B_V1_V2_PUBLICATION_RELATION_20260927.md"
ARCHITECTURE = ROOT / "docs" / "PAYOFF_B_TWO_PAPER_PUBLICATION_ARCHITECTURE_20260925.md"
REFRAME = ROOT / "docs" / "PAYOFF_B_POST_BAYESIAN_PUBLICATION_REFRAME_20260926.md"
PACKAGE_AUDIT = ROOT / "submission" / "PAYOFF_B_V2_GEB_PREOUTCOME_PACKAGE_AUDIT_20260927.md"


def _abstract(text: str) -> str:
    start = text.index("## Abstract") + len("## Abstract")
    end = text.index("**Keywords:**", start)
    return text[start:end].strip()


def _word_count(text: str) -> int:
    return len(re.findall(r"\b[\w’'-]+\b", text))


def test_v2_is_the_only_active_paper2_source():
    status = STATUS.read_text(encoding="utf-8")
    relation = RELATION.read_text(encoding="utf-8")
    architecture = ARCHITECTURE.read_text(encoding="utf-8")
    reframe = REFRAME.read_text(encoding="utf-8")

    assert "CANONICAL_SOURCE = PAYOFF_B_INFORMATION_COORDINATION_V2_PREOUTCOME.md" in status
    assert "V1_STATUS = FROZEN_PROVENANCE_ONLY" in status
    assert "CURRENT_V2_PREOUTCOME_PACKAGE = READY" in status
    assert "CURRENT_V2_PREOUTCOME_BUILD_RUN = 36402882222" in status
    assert "CURRENT_V2_PREOUTCOME_ARTIFACT = 10961191453" in status
    assert "CURRENT_V2_PREOUTCOME_ARCHIVE_SHA256 = fee2e34729bc3659a1ff21f05e572f269b7230d670bc1bd48168ac2a98c133a4" in status
    assert "CURRENT_V2_FINAL_SUBMISSION_PACKAGE = ACCESS_BLOCKED_SCIENCE_CLOSED_PORTAL_BLOCKED" in status
    assert "CURRENT_V2_ACCESS_BLOCKED_PACKAGE = READY" in status
    assert "AIKENS_LAMBDA_OUTCOME_OPENED = false" in status
    assert "E6 information-distance triangulation" in status
    assert "sole active integrated ecology manuscript" in relation
    assert "No V1 and V2 dual submission is allowed." in relation
    assert "2026-09-27 canonical amendment" in architecture
    assert "ADOPTED for Paper 2" in reframe

    package_audit = PACKAGE_AUDIT.read_text(encoding="utf-8")
    assert "PASS — canonical V2 PREOUTCOME working package ready" in package_audit
    assert "structured_abstract_words = 272" in package_audit
    assert "main_body_words = 4633" in package_audit
    assert "references = 16" in package_audit
    assert "display_pieces = 7" in package_audit
    assert "package_file_count = 17" in package_audit
    assert "FINAL_SUBMISSION_ELIGIBLE = false" in package_audit


def test_v2_abstract_keeps_only_the_core_deadline_and_recovery_story():
    text = V2.read_text(encoding="utf-8")
    abstract = _abstract(text)
    words = _word_count(abstract)

    assert 150 <= words <= 210
    assert "information deadlines" in abstract
    assert "different delay costs" in abstract
    assert "better information increases" in abstract
    assert "strict Nash equilibria" in abstract
    assert "perfect cue accuracy does not recover" in abstract
    assert "Theory predicts that environmental information can recover before ecological coordination does." in abstract
    assert "Natural evidence supports pieces of this mechanism rather than the full hysteresis process" in abstract

    # Important secondary results stay in Results/Discussion rather than
    # competing with T1-T3 and T7-T8 in the abstract.
    for secondary in (
        "minimum temporary informed seed",
        "topology-dependent",
        "network cut",
        "rescue leverage",
        "half uptake",
    ):
        assert secondary not in abstract
