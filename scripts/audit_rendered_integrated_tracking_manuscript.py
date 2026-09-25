#!/usr/bin/env python3
"""Audit an outcome-rendered integrated PAYOFF-B manuscript."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from audit_integrated_tracking_manuscript import (
    cited_in_body,
    reference_records,
    section,
    words,
)
from render_aikens_lambda_manuscript import classify_result

ROOT = Path(__file__).resolve().parents[1]


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

    abstract = section(text, "## Abstract", "**Keywords:**")
    kw_hit = re.search(r"\*\*Keywords:\*\*\s*(.+)", text)
    keywords = (
        [x.strip() for x in kw_hit.group(1).split(";") if x.strip()]
        if kw_hit
        else []
    )
    refs = section(text, "## References", "## Figure architecture")
    pre_refs = text.split("## References", 1)[0]
    records = reference_records(refs)
    uncited = [
        {"surname": r["surname"], "year": r["year"]}
        for r in records
        if not cited_in_body(pre_refs, r["surname"], r["year"])
    ]
    fig_block = section(text, "## Figure architecture", "## Claim ceiling")
    figure_numbers = re.findall(r"^\*\*Figure\s+(\d+)\s+—", fig_block, flags=re.M)

    markers_ok = True
    for name in ("ABSTRACT", "RESULTS", "DISCUSSION", "CONCLUSION"):
        markers_ok = markers_ok and (
            text.count(f"<!-- AIKENS_LAMBDA_{name}_START -->") == 1
            and text.count(f"<!-- AIKENS_LAMBDA_{name}_END -->") == 1
        )

    blind_patterns = (
        r"\bZHANG\b",
        r"\bRuiqi\b",
        r"張瑞琪",
        r"zuizui0223",
        r"github\.com/zuizui0223",
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    )
    no_identity_leak = not any(
        re.search(pattern, text, flags=re.I) for pattern in blind_patterns
    )

    expected_opened = bool(
        payload.get(
            "lambda_outcome_opened",
            result_class != "NOT_ESTIMABLE",
        )
    )

    required_phrase = {
        "PASS": "**passed**",
        "FAIL_WRONG_DIRECTION": "**failed in direction**",
        "FAIL_INSUFFICIENT_SUPPORT": "**failed the support gate**",
        "NOT_ESTIMABLE": "**not estimable**",
    }[result_class]

    hard = {
        "status_is_outcome_rendered": (
            "**Status:** integrated ecology manuscript v1, OUTCOME-RENDERED" in text
        ),
        "all_pending_placeholders_removed": "PENDING" not in text,
        "aikens_marker_pairs_preserved": markers_ok,
        "result_specific_language_present": required_phrase in text,
        "abstract_at_most_300_words": len(words(abstract)) <= 300,
        "keywords_between_6_and_10": 6 <= len(keywords) <= 10,
        "all_references_cited": not uncited,
        "six_main_figures_exactly": figure_numbers == ["1", "2", "3", "4", "5", "6"],
        "no_identity_leak": no_identity_leak,
        "claim_state_matches_result": claim["scientific_result"] == result_class,
        "no_retuning": claim["retuning_permitted"] is False,
        "not_added_to_cross_taxon_synthesis": (
            claim["aikens_added_to_cross_taxon_lambda_synthesis"] is False
            and claim["cross_taxon_lambda_synthesis_changed"] is False
        ),
        "actuator_result_not_rewritten": claim["actuator_result_changed"] is False,
        "figure_result_present": figures["aikens_result_present"] is True,
        "figure_outcome_opened_state_correct": (
            figures["aikens_outcome_opened"] is expected_opened
        ),
        "universal_lambda_still_prohibited": (
            "a universal lambda or universal actuator" in text
            and "formal cross-taxon meta-analytic controller coefficient" in text
        ),
    }

    return {
        "manuscript": str(manuscript),
        "scientific_result": result_class,
        "aikens_lambda_outcome_opened": expected_opened,
        "metrics": {
            "abstract_words": len(words(abstract)),
            "keyword_count": len(keywords),
            "reference_count": len(records),
            "main_figure_count": len(figure_numbers),
        },
        "uncited_references": uncited,
        "hard_postoutcome_gates": hard,
        "all_postoutcome_hard_gates_pass": all(hard.values()),
        "final_submission_science_ready": all(hard.values()),
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
    if args.fail_on_gate_failure and not result["all_postoutcome_hard_gates_pass"]:
        raise SystemExit("rendered integrated manuscript audit failed")


if __name__ == "__main__":
    main()
