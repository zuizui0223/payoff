#!/usr/bin/env python3
"""Submission audit for the blinded GEB movement-phenology manuscript."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


DEFAULT = Path("manuscript/PAYOFF_B_MOVEMENT_PHENOLOGY_GEB_V2.md")
OUT = Path("outputs/movement_phenology")


def words(text: str) -> list[str]:
    return re.findall(r"\b[\w’'-]+\b", text, flags=re.UNICODE)


def section(text: str, start: str, end: str | None = None) -> str:
    i = text.find(start)
    if i < 0:
        return ""
    i += len(start)
    if end is None:
        return text[i:]
    j = text.find(end, i)
    return text[i:] if j < 0 else text[i:j]


def first_author(author_text: str) -> str:
    """First surname, preserving particles such as 'van Toor'."""
    x = author_text.strip()
    x = re.sub(r"\bet\s+al\.?", "", x, flags=re.I).strip()
    x = x.split("&", 1)[0].strip()
    x = re.sub(r"^(?:see|from|by|using|based\s+on)\s+", "", x, flags=re.I).strip()
    return x


def citation_keys(body: str) -> set[tuple[str, int]]:
    keys: set[tuple[str, int]] = set()

    # Parenthetical groups:
    # (Bischof et al., 2012; Torstenson & Shaw, 2025)
    for group in re.findall(r"\(([^()]*(?:19|20)\d{2}[^()]*)\)", body):
        for clause in group.split(";"):
            hit = re.search(r"(.+?),\s*((?:19|20)\d{2})\b", clause.strip())
            if hit:
                author = first_author(hit.group(1))
                if author:
                    keys.add((author, int(hit.group(2))))

    # Narrative forms:
    # Amaral et al. (2025); van Toor et al. (2021)
    narrative = re.compile(
        r"\b(?:(van|von|de|del|der|di|da)\s+)?"
        r"([A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ'’\-]+)"
        r"(?:\s+et\s+al\.)?\s*"
        r"\(((?:19|20)\d{2})\)"
    )
    for hit in narrative.finditer(body):
        particle = (hit.group(1) or "").strip()
        surname = hit.group(2).strip()
        author = f"{particle} {surname}".strip()
        keys.add((author, int(hit.group(3))))

    return keys


def reference_keys(refs: str) -> set[tuple[str, int]]:
    out: set[tuple[str, int]] = set()
    for line in refs.splitlines():
        if not line.startswith("- "):
            continue
        hit = re.match(r"-\s+([^,]+),.*?\((\d{4})\)", line)
        if hit:
            out.add((hit.group(1).strip(), int(hit.group(2))))
    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--manuscript", default=str(DEFAULT))
    p.add_argument("--output", default=str(OUT / "geb_submission_audit.json"))
    args = p.parse_args()

    path = Path(args.manuscript)
    text = path.read_text(encoding="utf-8")
    abstract = section(text, "## Abstract", "## Introduction")
    main_text = section(
        text, "## Introduction", "## Data and Code Availability Statement"
    )
    refs = section(text, "## References", "## Claim ceiling")
    pre_refs = (
        text[: text.find("## References")]
        if "## References" in text
        else text
    )

    required_abstract = [
        "**Aim:**",
        "**Location:**",
        "**Time period:**",
        "**Major taxa studied:**",
        "**Methods:**",
        "**Results:**",
        "**Main conclusions:**",
    ]
    missing_abstract = [x for x in required_abstract if x not in abstract]

    kw_match = re.search(r"\*\*Keywords:\*\*\s*(.+)", abstract)
    keywords = (
        [x.strip() for x in kw_match.group(1).split(",") if x.strip()]
        if kw_match
        else []
    )

    # GEB's 300-word limit applies to the abstract, not the keyword list.
    abstract_for_count = re.sub(
        r"\*\*Keywords:\*\*.*", "", abstract, flags=re.S
    )

    cited = citation_keys(pre_refs)
    referenced = reference_keys(refs)
    missing_refs = sorted(cited - referenced)
    uncited_refs = sorted(referenced - cited)

    blind_patterns = {
        "author_name": r"\bZHANG\b|\bRuiqi\b|張瑞琪",
        "author_repo": r"github\.com/zuizui0223|zuizui0223",
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    }
    blind_hits = {
        name: bool(re.search(pattern, pre_refs, flags=re.I))
        for name, pattern in blind_patterns.items()
    }

    figure_legends = len(
        re.findall(r"^\*\*Figure\s+\d+\.", text, flags=re.M)
    )
    table_legends = len(
        re.findall(r"^\*\*Table\s+\d+\.", text, flags=re.M)
    )
    display_pieces = figure_legends + table_legends

    result = {
        "manuscript": str(path),
        "abstract_words": len(words(abstract_for_count)),
        "main_text_words": len(words(main_text)),
        "reference_count": len(referenced),
        "keyword_count": len(keywords),
        "keywords": keywords,
        "figure_legends": figure_legends,
        "table_legends": table_legends,
        "display_pieces": display_pieces,
        "citation_count_unique_first_author_year": len(cited),
        "missing_reference_keys": [
            {"author": author, "year": year}
            for author, year in missing_refs
        ],
        "uncited_reference_keys": [
            {"author": author, "year": year}
            for author, year in uncited_refs
        ],
        "missing_structured_abstract_headings": missing_abstract,
        "blind_text_hits": blind_hits,
    }

    hard = {
        "structured_abstract_complete": not missing_abstract,
        "abstract_at_most_300_words": result["abstract_words"] <= 300,
        "keywords_between_6_and_10": 6 <= len(keywords) <= 10,
        "no_missing_references": not missing_refs,
        "no_identity_leak_in_blinded_text": not any(blind_hits.values()),
        "display_pieces_between_6_and_8": 6 <= display_pieces <= 8,
    }
    result["hard_gates"] = hard
    result["all_hard_gates_pass"] = all(hard.values())
    result["soft_checks"] = {
        "main_text_near_5000_words": 3000 <= result["main_text_words"] <= 6000,
        "reference_core_at_least_12": result["reference_count"] >= 12,
        "uncited_references_zero": len(uncited_refs) == 0,
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(result, indent=2))
    if not result["all_hard_gates_pass"]:
        raise SystemExit("GEB manuscript hard gate failed")


if __name__ == "__main__":
    main()
