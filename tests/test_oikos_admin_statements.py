from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SIGNIFICANCE = ROOT / "submission" / "OIKOS_SIGNIFICANCE_STATEMENT.md"
DATA = ROOT / "submission" / "OIKOS_DATA_AVAILABILITY_TEMPLATE.md"
AI = ROOT / "submission" / "OIKOS_AI_USE_STATEMENT.md"


def test_oikos_significance_statement_covers_required_logic():
    text = SIGNIFICANCE.read_text(encoding="utf-8")
    assert "Oikos is an appropriate outlet" in text
    assert "adaptive capacity does not guarantee adaptive accessibility" in text
    assert "Existing work has established" in text


def test_oikos_data_availability_does_not_invent_archive():
    text = DATA.read_text(encoding="utf-8")
    assert "[ANONYMOUS REVIEW FILE UPLOAD OR ANONYMOUS REPOSITORY LINK]" in text
    assert "[PUBLIC REPOSITORY NAME, VERSION, DOI/PERSISTENT IDENTIFIER]" in text
    assert "No empirical individual-level" in text


def test_oikos_ai_statement_discloses_actual_chatgpt_use():
    text = AI.read_text(encoding="utf-8")
    assert "OpenAI ChatGPT" in text
    assert "code development and debugging" in text
    assert "drafting and editing text" in text
    assert "reviewed and validated by the authors" in text