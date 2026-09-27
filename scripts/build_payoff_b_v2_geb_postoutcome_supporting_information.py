#!/usr/bin/env python3
"""Render the frozen Aikens outcome into PAYOFF-B V2 Supporting Information.

The canonical V2 main text and figures are outcome-invariant. The registered
industrial-development result is rendered only into Supporting Information and
a machine-readable claim-state receipt.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_payoff_b_v2_geb_supporting_information import (
    build_supporting_information as build_preoutcome_si,
)
from render_aikens_lambda_manuscript import render_blocks


PENDING_HEADING = (
    "## Appendix S8. Registered industrial-development supplement — pending"
)


def render_supporting_information(payload: dict) -> tuple[str, dict]:
    preoutcome = build_preoutcome_si()
    preoutcome_status = (
        "Status: working PREOUTCOME supplement. The registered industrial-development\n"
        "phase-retention result remains unopened."
    )
    resolved_status = (
        "Status: outcome-rendered supplement. The registered industrial-development\n"
        "phase-retention gate has been adjudicated under the frozen contract; the\n"
        "result class is reported in Appendix S8."
    )
    if preoutcome_status not in preoutcome:
        raise ValueError("PREOUTCOME Supporting Information status marker not found")
    preoutcome = preoutcome.replace(
        preoutcome_status,
        resolved_status,
        1,
    )
    if PENDING_HEADING not in preoutcome:
        raise ValueError("PREOUTCOME Supporting Information lacks Appendix S8 marker")

    results, discussion, _abstract, _conclusion, claim_state = render_blocks(
        payload
    )
    result_class = claim_state["scientific_result"]

    preoutcome_status = (
        "Status: working PREOUTCOME supplement. The registered industrial-development\n"
        "phase-retention result remains unopened."
    )
    postoutcome_status = (
        "Status: postoutcome supplement. The registered industrial-development\n"
        f"phase-retention gate is resolved as **{result_class}**."
    )
    if preoutcome_status not in preoutcome:
        raise ValueError("PREOUTCOME Supporting Information status line changed")
    preoutcome = preoutcome.replace(
        preoutcome_status,
        postoutcome_status,
        1,
    )

    prefix, _ = preoutcome.split(PENDING_HEADING, 1)
    replacement = f"""## Appendix S8. Registered industrial-development phase-retention result

Frozen outcome class: **{result_class}**

### Registered result

{results}

### Interpretation

{discussion}

### Outcome-blindness contract

This result was rendered after the V2 title, structured abstract, main-text
information-deadline theorem, perfect-information recovery-failure result,
natural-evidence hierarchy and seven main figures had already been frozen.

The Aikens result does not enter the cross-taxon lambda synthesis and does not
retune the main-paper claims.

## Source and claim boundary

All exact statements are restricted to their declared finite models. Natural
data support individual edges of the mechanism rather than a directly observed
full degradation–recovery network hysteresis sequence.
"""

    # Preserve S1-S7 exactly and replace the pending S8 + old final boundary.
    rendered = prefix.rstrip() + "\n\n" + replacement.strip() + "\n"

    claim_state = dict(claim_state)
    claim_state.update(
        {
            "render_surface": "V2 Supporting Information only",
            "main_text_changed_by_result": False,
            "figures_changed_by_result": False,
            "title_changed_by_result": False,
            "structured_abstract_changed_by_result": False,
            "retuning_permitted": False,
        }
    )
    return rendered, claim_state


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result-json", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--claim-state-output", type=Path, required=True)
    args = parser.parse_args()

    payload = json.loads(args.result_json.read_text(encoding="utf-8"))
    text, claim_state = render_supporting_information(payload)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    args.claim_state_output.parent.mkdir(parents=True, exist_ok=True)
    args.claim_state_output.write_text(
        json.dumps(claim_state, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"AIKENS_V2_SI_RESULT={claim_state['scientific_result']}")
    print(args.output)
    print(args.claim_state_output)


if __name__ == "__main__":
    main()
