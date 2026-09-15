from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "PAYOFF_B_THEORETICAL_ECOLOGY_BRIEF_V1.md"


def word_count(text: str) -> int:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"\\\[.*?\\\]", " ", text, flags=re.S)
    text = re.sub(r"\\\(.*?\\\)", " ", text, flags=re.S)
    return len(re.findall(r"\b[\w’'–-]+\b", text))


def check() -> dict[str, int | str]:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    title = text.splitlines()[0].removeprefix("# ").strip()
    abstract = text.split("## Abstract", 1)[1].split("**Keywords:**", 1)[0]
    main = text.split("## 1. Introduction", 1)[1].split("## References", 1)[0]

    assert "The closed-form growth exponent is not claimed as new" in text
    assert "Benaïm et al. (2023)" in text
    assert "exactly one stationary point" in text
    assert "1.60611529880277" in text
    assert "m_*\\tau\\to1" in text
    assert "arbitrary periodic environments" not in text.lower()

    refs = [
        "Abbott KC (2011)",
        "Benaïm M, Lobry C, Sari T, Strickler É (2023)",
        "Benaïm M, Lobry C, Sari T, Strickler É (2025)",
        "Holt RD (1985)",
        "Katriel G (2022)",
        "Liu S, Wang H (2025)",
    ]
    for ref in refs:
        assert ref in text

    abstract_words = word_count(abstract)
    main_words = word_count(main)
    assert abstract_words <= 250
    assert main_words <= 4000

    return {
        "title_chars": len(title),
        "abstract_words": abstract_words,
        "main_words_pre_references": main_words,
        "references": len(refs),
        "status": "PASS",
    }


if __name__ == "__main__":
    result = check()
    for key, value in result.items():
        print(f"{key}={value}")
