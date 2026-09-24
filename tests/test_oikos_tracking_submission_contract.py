import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "PAYOFF_B_TRACKING_THEORY_V1.md"


def abstract_text():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    start = text.index("## Abstract") + len("## Abstract")
    end = text.index("**Keywords:**", start)
    return text[start:end].strip()


def test_oikos_abstract_is_within_300_words():
    abstract = abstract_text()
    words = re.findall(r"\b[\w’'–-]+\b", abstract)
    assert len(words) == 295
    assert len(words) <= 300


def test_oikos_abstract_has_no_references_or_acronyms():
    abstract = abstract_text()
    assert "et al." not in abstract
    assert "doi" not in abstract.lower()
    assert re.search(r"\b(?:19|20)\d{2}\b", abstract) is None
    assert re.findall(r"\b[A-Z]{2,}\b", abstract) == []
