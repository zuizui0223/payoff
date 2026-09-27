from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "manuscript" / "PAYOFF_B_INFORMATION_COORDINATION_V2_PREOUTCOME.md"
STATUS = ROOT / "docs" / "PUBLICATION_STATUS.md"
RELATION = ROOT / "docs" / "PAYOFF_B_V1_V2_PUBLICATION_RELATION_20260927.md"
ARCHITECTURE = ROOT / "docs" / "PAYOFF_B_TWO_PAPER_PUBLICATION_ARCHITECTURE_20260925.md"
REFRAME = ROOT / "docs" / "PAYOFF_B_POST_BAYESIAN_PUBLICATION_REFRAME_20260926.md"


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
    assert "CURRENT_V2_JOURNAL_PACKAGE = REBUILD_REQUIRED" in status
    assert "sole active integrated ecology manuscript" in relation
    assert "No V1 and V2 dual submission is allowed." in relation
    assert "2026-09-27 canonical amendment" in architecture
    assert "ADOPTED for Paper 2" in reframe


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
    assert "Environmental information can recover before ecological coordination does." in abstract

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
