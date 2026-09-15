from __future__ import annotations

import re

from scripts.build_payoff_b_submission_source import build_submission_source


def word_count(text: str) -> int:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"\\\[.*?\\\]", " ", text, flags=re.S)
    text = re.sub(r"\\\(.*?\\\)", " ", text, flags=re.S)
    return len(re.findall(r"\b[\w’'–-]+\b", text))


def check() -> dict[str, int | str]:
    text = build_submission_source()
    title = text.splitlines()[0].removeprefix("# ").strip()
    abstract = text.split("## Abstract", 1)[1].split("**Keywords:**", 1)[0]
    keyword_line = text.split("**Keywords:**", 1)[1].splitlines()[0].strip()
    keywords = [item.strip() for item in keyword_line.split(";") if item.strip()]
    main = text.split("## 1. Introduction", 1)[1].split("## References", 1)[0]

    assert "**Target:**" not in text
    assert "The closed-form growth exponent is not claimed as new" in text
    assert "Benaïm et al. (2023)" in text
    assert "exactly one stationary point" in text
    assert "1.60611529880277" in text
    assert "m_*\\tau\\to1" in text
    assert "arbitrary periodic environments" not in text.lower()

    for field in (
        "**Authors:**",
        "**Affiliations:**",
        "**Corresponding author:**",
        "**Corresponding-author email:**",
        "**ORCID(s):**",
    ):
        assert field in text

    for heading in (
        "## Statements and Declarations",
        "### Funding",
        "### Competing Interests",
        "### Author Contributions",
        "### Data and code availability",
        "### Use of generative AI tools",
    ):
        assert heading in text

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
    assert 150 <= abstract_words <= 250
    assert 4 <= len(keywords) <= 6
    assert main_words <= 4000

    return {
        "title_chars": len(title),
        "abstract_words": abstract_words,
        "keyword_count": len(keywords),
        "main_words_pre_references": main_words,
        "references": len(refs),
        "internal_target_line_removed": "true",
        "declarations_present": "true",
        "status": "PASS",
    }


if __name__ == "__main__":
    result = check()
    for key, value in result.items():
        print(f"{key}={value}")
