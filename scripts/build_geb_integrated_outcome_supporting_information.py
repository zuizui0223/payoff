#!/usr/bin/env python3
"""Build outcome-rendered Supporting Information for the integrated GEB paper."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_integrated_tracking_supporting_information import (
    build_supporting_information as build_preoutcome_si,
)
from render_aikens_lambda_manuscript import classify_result, render_blocks


PREOUTCOME_HEADER = "**PREOUTCOME working Supporting Information - 2026-09-25**"
PREOUTCOME_SENTENCE = (
    "**PREOUTCOME STATE: the Aikens lambda outcome is unopened.** The final "
    "Supporting Information must be rebuilt after registered adjudication. "
    "Supported, wrong-direction, insufficient-support and non-estimable "
    "outcomes are all licensed by the frozen renderer without narrative retuning."
)


def outcome_summary(payload: dict) -> str:
    result_class = classify_result(payload)
    results, _, _, _, _ = render_blocks(payload)
    return (
        f"**REGISTERED AIKENS OUTCOME: {result_class}.** "
        + results.replace("\n", " ").strip()
        + " This within-taxon result does not alter the cross-taxon synthesis."
    )


def build_supporting_information(result_json: Path) -> str:
    payload = json.loads(result_json.read_text(encoding="utf-8"))
    text = build_preoutcome_si()
    text = text.replace(
        PREOUTCOME_HEADER,
        "**OUTCOME-RENDERED Supporting Information**",
        1,
    )
    if PREOUTCOME_SENTENCE not in text:
        raise ValueError("preoutcome Aikens SI marker text not found")
    text = text.replace(PREOUTCOME_SENTENCE, outcome_summary(payload), 1)
    if "PREOUTCOME STATE" in text:
        raise ValueError("unresolved PREOUTCOME state remains in outcome SI")
    if "Aikens lambda outcome is unopened" in text:
        raise ValueError("unresolved unopened statement remains in outcome SI")
    return text


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--result-json", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    content = build_supporting_information(args.result_json)
    args.output.write_text(content, encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
