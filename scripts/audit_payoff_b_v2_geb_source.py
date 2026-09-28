#!/usr/bin/env python3
"""Audit the blinded GEB-facing PAYOFF-B V2 source."""

from __future__ import annotations

import json
import re
from pathlib import Path

from build_payoff_b_v2_geb_source import build_source

ABSTRACT_HEADINGS = (
    "Aim",
    "Location",
    "Time period",
    "Major taxa studied",
    "Methods",
    "Results",
    "Main conclusions",
)

INTERNAL_TOKENS = (
    "PAYOFF-B",
    "PREOUTCOME",
    "FROZEN_PROVENANCE",
    "AIKENS_LAMBDA",
    "CURRENT_V2_",
    "LEGACY_V1_",
    "zuizui0223",
    "github.com/zuizui",
    "**Status:**",
    "**Lineage:**",
    "**Evidence boundary:**",
)


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w’'-]+\b", text))


def section(text: str, start_heading: str, end_heading: str | None) -> str:
    start = text.index(start_heading) + len(start_heading)
    if end_heading is None:
        return text[start:]
    end = text.index(end_heading, start)
    return text[start:end]


def audit(text: str | None = None) -> dict:
    text = build_source() if text is None else text

    abstract = section(text, "## Abstract", "**Keywords:**")
    abstract_words = word_count(abstract)
    abstract_heading_positions = [
        abstract.find(f"### {heading}") for heading in ABSTRACT_HEADINGS
    ]
    abstract_headings_pass = (
        all(pos >= 0 for pos in abstract_heading_positions)
        and abstract_heading_positions == sorted(abstract_heading_positions)
    )

    keyword_line = re.search(r"\*\*Keywords:\*\*\s*(.+)", text)
    if keyword_line is None:
        keywords = []
    else:
        keywords = [
            item.strip()
            for item in keyword_line.group(1).split(";")
            if item.strip()
        ]
    alphabetical_keywords = keywords == sorted(
        keywords,
        key=lambda value: value.casefold(),
    )

    running = re.search(r"\*\*Running title:\*\*\s*(.+)", text)
    running_title = running.group(1).strip() if running else ""

    intro_start = text.index("## 1. Introduction")
    references_start = text.index("## References")
    main_body = text[intro_start:references_start]
    main_body_words = word_count(main_body)

    references_text = section(
        text,
        "## References",
        "## Data and Code Availability Statement",
    )
    references = [
        line for line in references_text.splitlines()
        if line.startswith("- ")
    ]

    figure_legends = re.findall(r"\*\*Figure\s+(\d+)\.", text)
    figure_numbers = [int(value) for value in figure_legends]

    internal_hits = [
        token for token in INTERNAL_TOKENS if token in text
    ]

    email_hits = re.findall(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        text,
    )

    expected_citations = (
        ("Aikens", "2017"),
        ("Aikens", "2022"),
        ("Åkesson", "2017"),
        ("Amaral", "2025"),
        ("Bauer", "2020"),
        ("Freimuth", "2022"),
        ("Helm", "2024"),
        ("Johansson", "2012"),
        ("Kharouba", "2020"),
        ("Kölzsch", "2015"),
        ("Ortega", "2023"),
        ("Samplonius", "2017"),
        ("Tomotani", "2021"),
        ("Usui", "2017"),
        ("van Toor", "2021"),
        ("Visser", "2019"),
        ("Watts", "2002"),
    )
    citation_presence = {
        f"{author}_{year}": (
            author in main_body and year in main_body
        )
        for author, year in expected_citations
    }

    metrics = {
        "abstract_words": abstract_words,
        "main_body_words": main_body_words,
        "keyword_count": len(keywords),
        "keywords": keywords,
        "running_title": running_title,
        "running_title_chars": len(running_title),
        "reference_count": len(references),
        "figure_legend_count": len(figure_numbers),
        "figure_numbers": figure_numbers,
        "internal_token_hits": internal_hits,
        "email_hits": email_hits,
        "citation_presence": citation_presence,
    }

    gates = {
        "structured_abstract": abstract_headings_pass,
        "abstract_words_le_300": abstract_words <= 300,
        "keywords_6_to_10": 6 <= len(keywords) <= 10,
        "keywords_alphabetical": alphabetical_keywords,
        "running_title_lt_40": 0 < len(running_title) < 40,
        "main_body_words_le_5000": main_body_words <= 5000,
        "references_1_to_50": 1 <= len(references) <= 50,
        "seven_display_pieces": figure_numbers == list(range(1, 8)),
        "anonymous_internal_tokens_zero": not internal_hits,
        "email_hits_zero": not email_hits,
        "expected_citations_present": all(citation_presence.values()),
        "aikens_placeholder_absent": "Aikens lambda result pending" not in text,
    }

    return {
        "status": "PASS" if all(gates.values()) else "FAIL",
        "metrics": metrics,
        "gates": gates,
        "all_preoutcome_hard_gates_pass": all(gates.values()),
    }


if __name__ == "__main__":
    result = audit()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["all_preoutcome_hard_gates_pass"] else 1)
