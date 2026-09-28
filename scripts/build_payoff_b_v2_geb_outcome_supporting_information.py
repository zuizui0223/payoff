#!/usr/bin/env python3
"""Render the registered Aikens result into PAYOFF-B V2 Supporting Information only."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_payoff_b_v2_geb_supporting_information import (
    build_supporting_information as build_preoutcome_si,
)
from render_aikens_lambda_manuscript import classify_result, render_blocks


PENDING_HEADING = "## Appendix S8. Registered industrial-development supplement — pending"


def build_supporting_information(result_json: Path) -> tuple[str, dict]:
    payload = json.loads(result_json.read_text(encoding="utf-8"))
    result_class = classify_result(payload)
    results, discussion, _, _, claim_state = render_blocks(payload)

    base = build_preoutcome_si()
    start = base.find(PENDING_HEADING)
    if start < 0:
        raise ValueError("V2 PREOUTCOME SI pending Aikens appendix not found")
    end = base.find("## Source and claim boundary", start)
    if end < 0:
        raise ValueError("V2 PREOUTCOME SI source boundary not found")

    appendix = f"""## Appendix S8. Registered industrial-development phase-retention result

**Registered result class: {result_class}.**

{results}

### Interpretation

{discussion}

This result is retained as a within-taxon Supplementary Information test. It
does not alter the title, structured abstract, main information-deadline
theorem, perfect-information recovery-failure result, seven main figures or the
claim boundaries of the broad-bird, flycatcher and wigeon analyses.

"""
    text = base[:start] + appendix + base[end:]
    text = text.replace(
        "Status: working PREOUTCOME supplement. The registered industrial-development\n"
        "phase-retention result remains unopened.",
        "Status: outcome-rendered Supporting Information.",
        1,
    )

    forbidden = (
        "remains unopened",
        "PREOUTCOME",
        "pending",
        "Pending",
    )
    residual = [token for token in forbidden if token in text]
    if residual:
        raise ValueError(
            "unresolved preoutcome language remains in V2 outcome SI: "
            + ", ".join(residual)
        )

    claim_state = dict(claim_state)
    claim_state.update(
        {
            "result_source": str(result_json),
            "canonical_main_text_changed": False,
            "main_figures_changed": False,
            "retuning_permitted": False,
            "result_location": "Supporting Information only",
            "v2_headline_changed": False,
        }
    )
    return text, claim_state


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result-json", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--claim-state-output", type=Path, required=True)
    args = parser.parse_args()

    text, claim_state = build_supporting_information(args.result_json)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    args.claim_state_output.parent.mkdir(parents=True, exist_ok=True)
    args.claim_state_output.write_text(
        json.dumps(claim_state, indent=2) + "\n",
        encoding="utf-8",
    )
    print(args.output)
    print(args.claim_state_output)
    print("PAYOFF_B_V2_AIKENS_RESULT=" + claim_state["scientific_result"])


if __name__ == "__main__":
    main()
