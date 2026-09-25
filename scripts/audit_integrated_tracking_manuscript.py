#!/usr/bin/env python3
"""Audit the integrated PAYOFF-B ecology manuscript without opening Aikens."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "manuscript" / "PAYOFF_B_INTEGRATED_TRACKING_ECOLOGY_V1_PREOUTCOME.md"
BROAD = ROOT / "data" / "payoff_b_broad_bird_stage1_result_20260925.json"
PANEL = ROOT / "data" / "payoff_b_empirical_phase_panel_status_20260921.json"
FIGURE_AUDIT = ROOT / "submission" / "PAYOFF_B_INTEGRATED_SIX_FIGURE_AUDIT_20260925.md"


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


def reference_records(refs: str) -> list[dict]:
    out = []
    particles = {"van", "von", "de", "del", "der", "di", "da"}
    for line in refs.splitlines():
        if not line.startswith("- "):
            continue
        hit = re.match(r"-\s+(.+?)\s+\((\d{4})\)", line)
        if not hit:
            continue
        first_author_blob = hit.group(1).split(",", 1)[0].strip()
        toks = first_author_blob.split()
        if not toks:
            continue
        if toks[0].lower() in particles and len(toks) >= 2:
            surname = f"{toks[0]} {toks[1]}"
        else:
            surname = toks[0]
        out.append(
            {
                "surname": surname,
                "year": int(hit.group(2)),
                "line": line,
            }
        )
    return out


def cited_in_body(body: str, surname: str, year: int) -> bool:
    pattern = (
        rf"(?i)(?<![\w]){re.escape(surname)}(?![\w])"
        rf"[\s\S]{{0,180}}(?<!\d){year}(?!\d)"
    )
    return bool(re.search(pattern, body))


def audit(path: Path = DEFAULT) -> dict:
    text = path.read_text(encoding="utf-8")
    abstract_raw = section(text, "## Abstract", "**Keywords:**")
    abstract = clean_pending(abstract_raw)
    kw_hit = re.search(r"\*\*Keywords:\*\*\s*(.+)", text)
    keywords = (
        [x.strip() for x in kw_hit.group(1).split(";") if x.strip()]
        if kw_hit
        else []
    )

    main_text = section(text, "## 1. Introduction", "## Prior-art boundary")
    refs = section(text, "## References", "## Figure architecture")
    pre_refs = text.split("## References", 1)[0]
    records = reference_records(refs)
    uncited = [
        {"surname": r["surname"], "year": r["year"]}
        for r in records
        if not cited_in_body(pre_refs, r["surname"], r["year"])
    ]

    fig_block = section(text, "## Figure architecture", "## Claim ceiling")
    figures = re.findall(r"^\*\*Figure\s+(\d+)\s+—", fig_block, flags=re.M)

    marker_status = {}
    for name in ("ABSTRACT", "RESULTS", "DISCUSSION", "CONCLUSION"):
        start = f"<!-- AIKENS_LAMBDA_{name}_START -->"
        end = f"<!-- AIKENS_LAMBDA_{name}_END -->"
        marker_status[name.lower()] = {
            "start_count": text.count(start),
            "end_count": text.count(end),
        }

    blind_patterns = {
        "author_name": r"\bZHANG\b|\bRuiqi\b|張瑞琪",
        "repository_owner": r"zuizui0223|github\.com/zuizui0223",
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    }
    blind_hits = {
        name: bool(re.search(pattern, text, flags=re.I))
        for name, pattern in blind_patterns.items()
    }

    broad = json.loads(BROAD.read_text(encoding="utf-8"))
    panel = json.loads(PANEL.read_text(encoding="utf-8"))
    figure_audit = FIGURE_AUDIT.read_text(encoding="utf-8")

    aikens_pending = all(
        f"[AIKENS LAMBDA {name} PENDING" in text
        for name in ("ABSTRACT", "RESULT", "DISCUSSION", "CONCLUSION")
    )

    hard = {
        "status_is_preoutcome": "integrated ecology manuscript v1, PREOUTCOME" in text,
        "theorem_kept_separate": "exact anti-phase optimum theorem remains a separate PAYOFF-B1 paper" in text,
        "abstract_at_most_300_words": len(words(abstract)) <= 300,
        "keywords_between_6_and_10": 6 <= len(keywords) <= 10,
        "main_text_between_2500_and_5000_words": 2500 <= len(words(main_text)) <= 5000,
        "reference_count_15_to_35": 15 <= len(records) <= 35,
        "all_references_cited": len(uncited) == 0,
        "six_main_figures_exactly": figures == ["1", "2", "3", "4", "5", "6"],
        "single_aikens_marker_pairs": all(
            v["start_count"] == 1 and v["end_count"] == 1
            for v in marker_status.values()
        ),
        "aikens_outcome_still_unopened": (
            aikens_pending
            and panel["next_empirical_experiment"]["lambda_outcome_opened"] is False
        ),
        "no_identity_leak": not any(blind_hits.values()),
        "broad_test_bound_to_machine_receipt": (
            broad["sample"]["n_rows"] == 5816
            and broad["sample"]["n_species"] == 55
            and broad["source_analysis"]["workflow_artifact_id"] == 10540282539
        ),
        "broad_test_is_primary_cross_system_result": (
            panel["broad_bird_falsification"]["primary_cross_system_result"] is True
            and panel["broad_bird_falsification"]["universal_speed_ratio_supported"] is False
        ),
        "figure_set_machine_audited": (
            "Status: **PASS" in figure_audit
            and "aikens_outcome_opened = false" in figure_audit
            and "10848409538" in figure_audit
        ),
        "universal_lambda_prohibited": (
            "a universal lambda or universal actuator" in text
            and "formal cross-taxon meta-analytic controller coefficient" in text
        ),
    }

    result = {
        "manuscript": str(path.relative_to(ROOT)),
        "state": "PREOUTCOME",
        "metrics": {
            "abstract_words": len(words(abstract)),
            "keyword_count": len(keywords),
            "main_text_words": len(words(main_text)),
            "reference_count": len(records),
            "main_figure_count": len(figures),
        },
        "keywords": keywords,
        "uncited_references": uncited,
        "aikens_markers": marker_status,
        "blind_text_hits": blind_hits,
        "hard_preoutcome_gates": hard,
        "all_preoutcome_hard_gates_pass": all(hard.values()),
        "final_submission_ready": False,
        "final_submission_blockers": [
            "registered Aikens fixed-24h lambda outcome remains unopened"
        ],
        "claim_state": {
            "universal_speed_rule_supported": False,
            "universal_lambda_licensed": False,
            "aikens_lambda_outcome_opened": False,
        },
    }
    return result


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--manuscript", type=Path, default=DEFAULT)
    p.add_argument(
        "--output",
        type=Path,
        default=ROOT / "outputs" / "integrated_tracking_submission_audit.json",
    )
    p.add_argument("--fail-on-preoutcome-gate-failure", action="store_true")
    args = p.parse_args()

    result = audit(args.manuscript)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if args.fail_on_preoutcome_gate_failure and not result["all_preoutcome_hard_gates_pass"]:
        raise SystemExit("integrated manuscript PREOUTCOME audit failed")


if __name__ == "__main__":
    main()
