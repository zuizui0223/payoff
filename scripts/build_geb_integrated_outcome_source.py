#!/usr/bin/env python3
"""Build an outcome-rendered GEB source from the adjudicated integrated manuscript."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_geb_integrated_preoutcome_source import (
    ABSTRACT_END,
    ABSTRACT_START,
    RUNNING_TITLE,
    between,
    strip_rule,
    structured_abstract,
    extract_caption_body,
)
from render_aikens_lambda_manuscript import classify_result

ROOT = Path(__file__).resolve().parents[1]
DATA_TEMPLATE = ROOT / "submission" / "GEB_INTEGRATED_DATA_CODE_OUTCOME_TEMPLATE.md"


def final_data_statement() -> str:
    text = DATA_TEMPLATE.read_text(encoding="utf-8")
    review = between(
        text,
        "## Blinded review statement",
        "## Publication archive",
    )
    publication = text.split("## Publication archive", 1)[1].strip()
    return (
        "## Data and Code Availability Statement\n\n"
        + review.strip()
        + "\n\n**Publication archive:** "
        + publication.replace("\n", " ").strip()
    )


def outcome_figure_legends(payload: dict) -> str:
    base = extract_caption_body()
    if "**Figure 6." not in base:
        raise ValueError("GEB Figure 6 legend not found")
    prefix = base.split("**Figure 6.", 1)[0].rstrip()
    result_class = classify_result(payload)

    if result_class == "NOT_ESTIMABLE":
        outcome = (
            "(c) The preregistered fixed-24 h industrial-mule-deer phase-retention "
            "contrast was not estimable under the frozen reconstruction and support "
            "criteria. The interval, tolerance, environmental product and support "
            "thresholds were not changed, and no phase-retention response to "
            "development is inferred."
        )
    else:
        gate = payload["gate"]
        obs = gate["observation"]
        numeric = (
            f"(c) In the preregistered fixed-24 h industrial-mule-deer contrast, "
            f"lambda_small={float(obs['lambda_a']):.3f}, "
            f"lambda_large={float(obs['lambda_b']):.3f}, "
            f"Delta lambda={float(gate['lambda_difference_b_minus_a']):.3f}, "
            f"p={float(obs['p_difference']):.3g}. "
        )
        if result_class == "PASS":
            outcome = numeric + (
                "The registered prediction of greater phase retention under large "
                "development passed."
            )
        elif result_class == "FAIL_WRONG_DIRECTION":
            outcome = numeric + (
                "The preregistered prediction failed in direction despite the "
                "independently supported actuation contrast."
            )
        else:
            outcome = numeric + (
                "The point contrast was in the registered direction but did not "
                "pass the inferential support gate."
            )

    return (
        prefix
        + "\n\n**Figure 6. Environmental information, phase retention and actuation "
        "are distinct.** (a) Stable barnacle-goose transitions from northern "
        "European–Arctic migration routes occupy different combinations of "
        "environmental innovation and segment-scale phase retention. (b) Across "
        "all eight registered near/far definitions in the North American "
        "industrial-mule-deer perturbation, movement-control permeability is lower "
        "in the large-development population; the stronger prediction of "
        "additional temporal deterioration is not supported. "
        + outcome
    )


def build_source(source_path: Path, result_json: Path) -> str:
    source = source_path.read_text(encoding="utf-8")
    payload = json.loads(result_json.read_text(encoding="utf-8"))
    if "PENDING" in source:
        raise ValueError("outcome-rendered integrated source still contains PENDING")

    title = source.splitlines()[0].removeprefix("# ").strip()
    abstract_block = between(source, ABSTRACT_START, ABSTRACT_END)

    body_start = source.index("## 1. Introduction")
    prior_start = source.index("## Prior-art boundary")
    refs_start = source.index("## References")
    figure_start = source.index("## Figure architecture")

    body = strip_rule(source[body_start:prior_start])
    prior = strip_rule(
        source[prior_start + len("## Prior-art boundary"):refs_start]
    ).strip()
    references = strip_rule(source[refs_start:figure_start]).strip()

    limitation = "### 5.8 Limitations"
    if limitation not in body:
        raise ValueError("outcome-rendered manuscript is missing 5.8 Limitations")
    body = body.replace(
        limitation,
        "### 5.8 Relationship to existing literature\n\n"
        + prior
        + "\n\n### 5.9 Limitations",
        1,
    )

    return (
        f"# {title}\n\n"
        f"**Running title:** {RUNNING_TITLE}\n\n"
        + structured_abstract(abstract_block)
        + "\n---\n\n"
        + body.strip()
        + "\n\n---\n\n"
        + references
        + "\n\n---\n\n"
        + final_data_statement()
        + "\n\n---\n\n"
        + "## Figure legends\n\n"
        + outcome_figure_legends(payload)
        + "\n"
    )


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=Path, required=True)
    p.add_argument("--result-json", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        build_source(args.source, args.result_json),
        encoding="utf-8",
    )
    print(args.output)


if __name__ == "__main__":
    main()
