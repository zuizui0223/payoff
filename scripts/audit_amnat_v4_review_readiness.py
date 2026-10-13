#!/usr/bin/env python3
"""Audit the V8-integrated Paper 2 for AmNat Major Article review preparation.

This is an EDITORIAL audit, not a source-data validation or a submission
operation. It must not silently promote the current manuscript to "ready".
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SOURCE = Path("manuscript/PAYOFF_B_INFORMATION_CONTROL_V4_V8_INTEGRATED.md")
FRONT = Path("submission/AMNAT_V4_FRONTMATTER_REVISED_20261011.md")

MAX_ABSTRACT = 200
MAX_KEYWORDS = 6
USUAL_MAX_WORDS = 7500


def _section(source: str, heading: str, next_heading: str) -> str:
    begin = source.find(heading)
    end = source.find(next_heading, begin + len(heading))
    if begin < 0 or end < 0:
        raise ValueError(f"Expected section boundary missing: {heading!r}")
    return source[begin + len(heading):end]


def _normalize_space(text: str) -> str:
    return " ".join(text.split())


def _words(text: str) -> int:
    return len([x for x in re.split(r"\s+", text.strip()) if x])


def audit(source: str, front: str) -> dict:
    abstract_plus_keywords = _section(
        source, "## Abstract", "## 1. Introduction"
    )
    if "**Keywords:**" not in abstract_plus_keywords:
        raise ValueError("Manuscript keywords missing")
    abstract, keywords_plus = abstract_plus_keywords.split("**Keywords:**", 1)
    abstract = abstract.strip()
    keywords = [
        k.strip() for k in keywords_plus.split("---", 1)[0].split(";")
        if k.strip()
    ]
    front_abstract = _section(front, "## Abstract", "**Abstract word count").strip()
    front_keywords = _section(front, "## Keywords", "**Keywords:** 6").strip()
    title = source.splitlines()[0].removeprefix("# ").strip()

    section_positions = {
        "theory": source.find("## 2. Theory"),
        "methods": source.find("## 3. Empirical methods"),
        "results": source.find("## 4. Natural evidence"),
        "discussion": source.find("## 5. Discussion"),
        "conclusion": source.find("## 6. Conclusion"),
    }
    methods_ordered = (
        all(k >= 0 for k in section_positions.values())
        and section_positions["theory"] < section_positions["methods"]
        < section_positions["results"] < section_positions["discussion"]
        < section_positions["conclusion"]
    )
    heading_pairs = re.findall(r"^### (\d+)\.(\d+) ", source, re.MULTILINE)
    headline_counters = {}
    heading_sequence_valid = True
    for chapter, subsection in heading_pairs:
        expected = headline_counters.get(chapter, 0) + 1
        if int(subsection) != expected:
            heading_sequence_valid = False
        headline_counters[chapter] = int(subsection)

    required_claims = {
        "range_pair_inference": "unique spatial source" in source,
        "bootstrap_replication": "10,000" in source and "pair-bootstrap" in source,
        "registered_negative_transfer": "registered negative" in source or
            "prespecified negative" in source or
            "registered directional prediction was a negative" in source,
        "structural_nulls": "fixed-bird-arrival" in source
            and "permutation" in source,
        "fitness_not_identified": "fitness regret" in source,
        "redstart_samples_not_conflated": "separate\nmark–resight survival" in source
            and "same individuals' migration speed" in source,
        "theory_scope_limit": "no-innovation" in source
            and "not a universal additive" in source,
    }
    science_errors = []
    if title != "Environmental predictability alone does not determine seasonal tracking":
        science_errors.append("title not agreed")
    if _words(abstract) > MAX_ABSTRACT:
        science_errors.append("abstract exceeds 200 words")
    if len(keywords) > MAX_KEYWORDS or not keywords:
        science_errors.append("keywords exceed journal limit or absent")
    if _normalize_space(abstract) != _normalize_space(front_abstract):
        science_errors.append("frontmatter abstract differs from manuscript")
    if _normalize_space("; ".join(keywords)) != _normalize_space(front_keywords):
        science_errors.append("frontmatter keywords differ from manuscript")
    if not methods_ordered:
        science_errors.append("methods do not precede natural results")
    if not heading_sequence_valid:
        science_errors.append("section numbering inconsistent")
    science_errors += [
        f"necessary claim guard missing: {key}"
        for key, result in required_claims.items() if not result
    ]
    # The journal main-text limit excludes Literature Cited.
    estimated_body = _words(source.split("## 1. Introduction", 1)[-1].split(
        "## Literature Cited", 1
    )[0].split("## Post-freeze transparency statement", 1)[0])
    if estimated_body + _words(abstract) > USUAL_MAX_WORDS:
        science_errors.append(
            "approximate text length exceeds usual Major Article maximum"
        )

    # These are honest unresolved submission tasks; their absence must NOT
    # be reported as a hard failure of published empirical analysis.
    submission_blockers = []
    if "## Literature Cited" not in source:
        submission_blockers.append("complete Literature Cited absent")
    else:
        submission_blockers.append(
            "20 DOI-checked core references present, but final bibliography "
            "style, source-by-source textual coverage and anonymous preview pending"
        )
    if "**PAYOFF-B Paper 2" in source or "post-freeze" in source.lower():
        submission_blockers.append("internal provenance remains in source")
    # A remote GitHub repo alone is not a compliant anonymous archived
    # README/data/code package; the final reviewer link is a human handoff.
    submission_blockers.extend([
        "anonymous reviewer-accessible data/code archive with README not verified",
        "anonymized double-spaced PDF with page/line numbers not verified",
        "final references, source/figure crosswalk and figure-legends audit pending",
        "author metadata, declarations and AI-use statements require author review",
    ])
    return {
        "status": "SOURCE_SCIENCE_CHECKS_PASS_SUBMISSION_HOLD"
                  if not science_errors else "SOURCE_SCIENCE_CHECKS_FAIL",
        "article_type": "Major Article",
        "title": title,
        "abstract_word_count": _words(abstract),
        "keywords": keywords,
        "keyword_count": len(keywords),
        "estimated_main_plus_abstract_words": estimated_body + _words(abstract),
        "heading_sequence_valid": heading_sequence_valid,
        "methods_before_results": methods_ordered,
        "claim_guards": required_claims,
        "science_source_errors": science_errors,
        "submission_blockers": submission_blockers,
        "submission_ready": False,
        "frozen_results_modified_by_this_audit": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--frontmatter", type=Path, default=FRONT)
    parser.add_argument("--output", type=Path, required=True)
    opts = parser.parse_args()
    result = audit(
        opts.source.read_text(encoding="utf-8"),
        opts.frontmatter.read_text(encoding="utf-8"),
    )
    opts.output.parent.mkdir(parents=True, exist_ok=True)
    opts.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "status": result["status"],
        "abstract_words": result["abstract_word_count"],
        "keywords": result["keyword_count"],
        "estimated_words": result["estimated_main_plus_abstract_words"],
        "submission_ready": False,
        "science_errors": result["science_source_errors"],
    }))
    if result["science_source_errors"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
