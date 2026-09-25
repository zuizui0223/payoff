#!/usr/bin/env python3
"""Audit the PREOUTCOME GEB overlay of the integrated PAYOFF-B paper."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_HEADINGS = [
    "**Aim:**",
    "**Location:**",
    "**Time period:**",
    "**Major taxa studied:**",
    "**Methods:**",
    "**Results:**",
    "**Main conclusions:**",
]


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


def clean_pending(text: str) -> str:
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"\[AIKENS LAMBDA .*? PENDING.*?\]", " ", text, flags=re.S)
    return text


def reference_records(refs: str) -> list[tuple[str, int]]:
    rows = []
    particles = {"van", "von", "de", "del", "der", "di", "da"}
    for line in refs.splitlines():
        if not line.startswith("- "):
            continue
        hit = re.match(r"-\s+(.+?)\s+\((\d{4})\)", line)
        if not hit:
            continue
        blob = hit.group(1).split(",", 1)[0].strip()
        toks = blob.split()
        if not toks:
            continue
        surname = (
            f"{toks[0]} {toks[1]}"
            if toks[0].lower() in particles and len(toks) >= 2
            else toks[0]
        )
        rows.append((surname, int(hit.group(2))))
    return rows


def cited(text: str, surname: str, year: int) -> bool:
    normalized = re.sub(r"\s+", " ", text)
    pattern = (
        rf"(?i)(?<![\w]){re.escape(surname)}(?![\w])"
        rf".{{0,180}}(?<!\d){year}(?!\d)"
    )
    return bool(re.search(pattern, normalized))


def audit(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    abstract = section(text, "## Abstract", "---")
    abstract_for_count = clean_pending(
        re.sub(r"\*\*Keywords:\*\*.*", "", abstract, flags=re.S)
    )
    headings_missing = [h for h in REQUIRED_HEADINGS if h not in abstract]

    kw = re.search(r"\*\*Keywords:\*\*\s*(.+)", abstract)
    keywords = (
        [x.strip() for x in kw.group(1).split(",") if x.strip()]
        if kw else []
    )

    run = re.search(r"\*\*Running title:\*\*\s*(.+)", text)
    running_title = run.group(1).strip() if run else ""

    main = section(text, "## 1. Introduction", "## References")
    refs = section(text, "## References", "## Data and Code Availability Statement")
    reference_rows = reference_records(refs)
    pre_refs = text.split("## References", 1)[0]
    uncited = [
        {"surname": s, "year": y}
        for s, y in reference_rows
        if not cited(pre_refs, s, y)
    ]

    figures = re.findall(r"^\*\*Figure\s+(\d+)\.", text, flags=re.M)

    marker_state = {}
    for name in ("ABSTRACT", "RESULTS", "DISCUSSION", "CONCLUSION"):
        marker_state[name.lower()] = {
            "start": text.count(f"<!-- AIKENS_LAMBDA_{name}_START -->"),
            "end": text.count(f"<!-- AIKENS_LAMBDA_{name}_END -->"),
        }

    blind_patterns = {
        "author_name": r"\bZHANG\b|\bRuiqi\b|張瑞琪",
        "repository_owner": r"zuizui0223|github\.com/zuizui0223",
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    }
    blind_hits = {
        k: bool(re.search(p, text, flags=re.I))
        for k, p in blind_patterns.items()
    }

    internal_tokens = [
        "**Status:**",
        "**Publication architecture:**",
        "**Evidence boundary:**",
        "## Claim ceiling",
        "## Figure architecture",
        "## Prior-art boundary",
    ]
    internal_hits = [x for x in internal_tokens if x in text]

    data_statement = section(
        text,
        "## Data and Code Availability Statement",
        "## Figure legends",
    )

    hard = {
        "structured_abstract_complete": not headings_missing,
        "abstract_at_most_300_words": len(words(abstract_for_count)) <= 300,
        "main_body_at_most_5000_words": len(words(main)) <= 5000,
        "reference_count_at_most_50": len(reference_rows) <= 50,
        "all_references_cited": not uncited,
        "display_pieces_6_to_8": 6 <= len(figures) <= 8,
        "exactly_six_figures_for_current_overlay": figures == [str(i) for i in range(1, 7)],
        "keywords_6_to_10": 6 <= len(keywords) <= 10,
        "keywords_alphabetical": keywords == sorted(keywords, key=str.casefold),
        "running_title_under_40_chars": 0 < len(running_title) < 40,
        "no_identity_leak": not any(blind_hits.values()),
        "no_internal_submission_tokens": not internal_hits,
        "single_aikens_marker_pairs": all(
            x["start"] == 1 and x["end"] == 1
            for x in marker_state.values()
        ),
        "aikens_preoutcome_pending": all(
            f"[AIKENS LAMBDA {name} PENDING" in text
            for name in ("ABSTRACT", "RESULT", "DISCUSSION", "CONCLUSION")
        ),
        "stable_reviewer_link_placeholder_present": (
            "[ANONYMOUS STABLE REVIEWER LINK — REQUIRED BEFORE SUBMISSION]"
            in data_statement
        ),
        "relationship_to_existing_literature_moved_into_discussion": (
            "### 5.7 Relationship to existing literature" in main
            and "### 5.8 Limitations" in main
        ),
    }

    return {
        "manuscript": str(path),
        "state": "GEB_PREOUTCOME_OVERLAY",
        "metrics": {
            "abstract_words": len(words(abstract_for_count)),
            "main_body_words": len(words(main)),
            "reference_count": len(reference_rows),
            "display_pieces": len(figures),
            "keyword_count": len(keywords),
            "running_title_chars": len(running_title),
        },
        "keywords": keywords,
        "missing_structured_headings": headings_missing,
        "uncited_references": uncited,
        "identity_hits": blind_hits,
        "internal_token_hits": internal_hits,
        "aikens_markers": marker_state,
        "hard_preoutcome_gates": hard,
        "all_preoutcome_hard_gates_pass": all(hard.values()),
        "final_submission_eligible": False,
        "final_submission_blockers": [
            "registered Aikens fixed-24h lambda adjudication",
            "anonymous stable reviewer archive link",
            "author-controlled title-page and declaration metadata",
        ],
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--manuscript", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--fail-on-gate-failure", action="store_true")
    args = p.parse_args()
    result = audit(args.manuscript)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if args.fail_on_gate_failure and not result["all_preoutcome_hard_gates_pass"]:
        raise SystemExit("GEB integrated PREOUTCOME overlay audit failed")


if __name__ == "__main__":
    main()
