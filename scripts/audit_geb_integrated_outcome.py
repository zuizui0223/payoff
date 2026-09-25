#!/usr/bin/env python3
"""Audit an outcome-rendered GEB overlay for the integrated PAYOFF-B paper."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from audit_geb_integrated_preoutcome import (
    REQUIRED_HEADINGS,
    cited,
    reference_records,
    section,
    words,
)
from render_aikens_lambda_manuscript import classify_result


def audit(
    manuscript: Path,
    result_json: Path,
    claim_state_json: Path,
    figure_manifest_json: Path,
) -> dict:
    text = manuscript.read_text(encoding="utf-8")
    payload = json.loads(result_json.read_text(encoding="utf-8"))
    claim = json.loads(claim_state_json.read_text(encoding="utf-8"))
    figures = json.loads(figure_manifest_json.read_text(encoding="utf-8"))
    result_class = classify_result(payload)

    abstract = section(text, "## Abstract", "---")
    abstract_for_count = re.sub(
        r"\*\*Keywords:\*\*.*", "", abstract, flags=re.S
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
    rows = reference_records(refs)
    pre_refs = text.split("## References", 1)[0]
    uncited = [
        {"surname": s, "year": y}
        for s, y in rows
        if not cited(pre_refs, s, y)
    ]
    fig_nums = re.findall(r"^\*\*Figure\s+(\d+)\.", text, flags=re.M)

    markers_ok = all(
        text.count(f"<!-- AIKENS_LAMBDA_{name}_START -->") == 1
        and text.count(f"<!-- AIKENS_LAMBDA_{name}_END -->") == 1
        for name in ("ABSTRACT", "RESULTS", "DISCUSSION", "CONCLUSION")
    )

    blind_patterns = (
        r"\bZHANG\b",
        r"\bRuiqi\b",
        r"張瑞琪",
        r"zuizui0223",
        r"github\.com/zuizui0223",
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    )
    no_identity = not any(
        re.search(p, text, flags=re.I) for p in blind_patterns
    )
    internal_tokens = (
        "**Status:**",
        "**Publication architecture:**",
        "**Evidence boundary:**",
        "## Claim ceiling",
        "## Figure architecture",
        "## Prior-art boundary",
    )
    no_internal = not any(x in text for x in internal_tokens)

    expected_opened = bool(
        payload.get(
            "lambda_outcome_opened",
            result_class != "NOT_ESTIMABLE",
        )
    )
    phrase = {
        "PASS": "prediction of greater phase retention under large development passed",
        "FAIL_WRONG_DIRECTION": "prediction failed in direction",
        "FAIL_INSUFFICIENT_SUPPORT": "did not pass the inferential support gate",
        "NOT_ESTIMABLE": "was not estimable under the frozen reconstruction",
    }[result_class]

    hard = {
        "structured_abstract_complete": not headings_missing,
        "abstract_at_most_300_words": len(words(abstract_for_count)) <= 300,
        "main_body_at_most_5000_words": len(words(main)) <= 5000,
        "reference_count_at_most_50": len(rows) <= 50,
        "all_references_cited": not uncited,
        "exactly_six_display_pieces": fig_nums == [str(i) for i in range(1, 7)],
        "keywords_6_to_10": 6 <= len(keywords) <= 10,
        "keywords_alphabetical": keywords == sorted(keywords, key=str.casefold),
        "running_title_under_40_chars": 0 < len(running_title) < 40,
        "no_identity_leak": no_identity,
        "no_internal_submission_tokens": no_internal,
        "aikens_marker_pairs_preserved": markers_ok,
        "no_pending_placeholders": "PENDING" not in text,
        "registered_result_language_present": phrase in text,
        "stable_reviewer_link_placeholder_present": (
            "[ANONYMOUS STABLE REVIEWER LINK — REQUIRED BEFORE SUBMISSION]"
            in text
        ),
        "claim_state_matches_result": claim["scientific_result"] == result_class,
        "no_retuning": claim["retuning_permitted"] is False,
        "cross_taxon_synthesis_unchanged": (
            claim["aikens_added_to_cross_taxon_lambda_synthesis"] is False
            and claim["cross_taxon_lambda_synthesis_changed"] is False
        ),
        "figure_result_present": figures.get("aikens_result_present") is True,
        "figure_outcome_opened_state_correct": (
            figures.get("aikens_outcome_opened") is expected_opened
        ),
        "relationship_to_existing_literature_in_discussion": (
            "### 5.8 Relationship to existing literature" in main
            and "### 5.9 Limitations" in main
        ),
    }

    return {
        "state": "GEB_OUTCOME_RENDERED",
        "scientific_result": result_class,
        "aikens_lambda_outcome_opened": expected_opened,
        "metrics": {
            "abstract_words": len(words(abstract_for_count)),
            "main_body_words": len(words(main)),
            "reference_count": len(rows),
            "display_pieces": len(fig_nums),
            "keyword_count": len(keywords),
            "running_title_chars": len(running_title),
        },
        "uncited_references": uncited,
        "hard_outcome_gates": hard,
        "all_outcome_hard_gates_pass": all(hard.values()),
        "science_ready_for_geb_finalization": all(hard.values()),
        "final_submission_eligible": False,
        "remaining_portal_blockers": [
            "anonymous stable reviewer archive link",
            "author-controlled title-page and declaration metadata",
        ],
        "retuning_permitted": False,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--manuscript", type=Path, required=True)
    p.add_argument("--result-json", type=Path, required=True)
    p.add_argument("--claim-state-json", type=Path, required=True)
    p.add_argument("--figure-manifest-json", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--fail-on-gate-failure", action="store_true")
    args = p.parse_args()
    result = audit(
        args.manuscript,
        args.result_json,
        args.claim_state_json,
        args.figure_manifest_json,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if args.fail_on_gate_failure and not result["all_outcome_hard_gates_pass"]:
        raise SystemExit("GEB outcome-rendered audit failed")


if __name__ == "__main__":
    main()
