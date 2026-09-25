#!/usr/bin/env python3
"""Render integrated Supporting Information after registered Aikens adjudication."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_integrated_tracking_supporting_information import (
    build_supporting_information as build_preoutcome_supporting_information,
)
from render_aikens_lambda_manuscript import classify_result


def fmt(value) -> str:
    if value is None:
        return "NA"
    value = float(value)
    if value == 0:
        return "0"
    if abs(value) < 0.001:
        return f"{value:.2e}"
    return f"{value:.4f}"


def outcome_text(payload: dict) -> tuple[str, bool]:
    result_class = classify_result(payload)

    if result_class == "NOT_ESTIMABLE":
        reasons = payload.get("reasons") or []
        reason_text = "; ".join(str(x) for x in reasons) or (
            "registered support or reconstruction gate not met"
        )
        return (
            "**REGISTERED OUTCOME: NOT ESTIMABLE.** "
            "The fixed-24 h contrast did not satisfy the frozen estimability "
            f"contract ({reason_text}). No interval, tolerance, environmental "
            "product or support threshold was retuned. The pre-existing actuator "
            "contrast remains valid, but no inference is made about a shift in "
            "phase retention.",
            False,
        )

    gate = payload["gate"]
    obs = gate["observation"]
    a = obs.get("lambda_a")
    b = obs.get("lambda_b")
    delta = gate.get("lambda_difference_b_minus_a")
    p = obs.get("p_difference")
    numbers = (
        f"lambda_small={fmt(a)}, lambda_large={fmt(b)}, "
        f"Delta lambda={fmt(delta)}, p={fmt(p)}."
    )

    if result_class == "PASS":
        text = (
            "**REGISTERED OUTCOME: PASS.** "
            + numbers
            + " The preregistered prediction of greater phase retention under "
            "large-development forcing passed. This is a within-taxon forcing "
            "contrast and is not counted as another cross-taxon lambda replication."
        )
    elif result_class == "FAIL_WRONG_DIRECTION":
        text = (
            "**REGISTERED OUTCOME: FAILED IN DIRECTION.** "
            + numbers
            + " The supported movement-control attenuation did not propagate into "
            "the preregistered increase in phase retention. Actuator and phase-"
            "retention layers therefore remain empirically distinct."
        )
    else:
        text = (
            "**REGISTERED OUTCOME: INSUFFICIENT SUPPORT.** "
            + numbers
            + " The point contrast was in the preregistered direction but did not "
            "pass the frozen inferential support gate; no development-associated "
            "shift in phase retention is claimed."
        )
    return text, True


def build_supporting_information(result_json: Path) -> str:
    payload = json.loads(result_json.read_text(encoding="utf-8"))
    result_class = classify_result(payload)
    replacement, opened = outcome_text(payload)

    text = build_preoutcome_supporting_information()
    text = text.replace(
        "**PREOUTCOME working Supporting Information - 2026-09-25**",
        "**OUTCOME-RENDERED Supporting Information**",
        1,
    )
    text = text.replace(
        "S1-S8 preserve the frozen synthetic mechanism evidence dated 2026-09-20. "
        "S9-S12 document the empirical macroecological, direct-controller, "
        "reliability and perturbation layers. The registered Aikens fixed-24 h "
        "lambda outcome remains unopened; no result is inferred in advance.",
        "S1-S8 preserve the frozen synthetic mechanism evidence dated 2026-09-20. "
        "S9-S12 document the empirical macroecological, direct-controller, "
        "reliability and perturbation layers. The Aikens fixed-24 h perturbation "
        f"has been adjudicated under the frozen contract as {result_class}.",
        1,
    )

    pending = (
        "**PREOUTCOME STATE: the Aikens lambda outcome is unopened.** The final "
        "Supporting Information must be rebuilt after registered adjudication. "
        "Supported, wrong-direction, insufficient-support and non-estimable "
        "outcomes are all licensed by the frozen renderer without narrative retuning."
    )
    if pending not in text:
        raise ValueError("PREOUTCOME Aikens SI marker text not found")
    text = text.replace(pending, replacement, 1)

    text += (
        "\n## S14. Outcome-rendering state\n\n"
        f"- registered result class: {result_class}\n"
        f"- lambda outcome opened: {str(opened).lower()}\n"
        "- narrative retuning after outcome inspection: false\n"
        "- Aikens added to cross-taxon lambda synthesis: false\n"
    )
    return text


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--result-json", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    text = build_supporting_information(args.result_json)
    args.output.write_text(text, encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
