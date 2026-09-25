#!/usr/bin/env python3
"""Build deterministic outcome-rendered GEB package for integrated PAYOFF-B."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from audit_geb_integrated_outcome import audit as audit_geb_outcome
from build_geb_integrated_outcome_source import build_source as build_geb_source
from build_geb_integrated_outcome_supporting_information import (
    build_supporting_information,
)
from build_geb_integrated_preoutcome_package import deterministic_zip, sha256
from render_aikens_lambda_manuscript import classify_result
from render_geb_integrated_figures import render_all as render_geb_figures

ROOT = Path(__file__).resolve().parents[1]

STATIC_FILES = [
    "submission/GEB_INTEGRATED_TITLE_PAGE_TEMPLATE.md",
    "submission/GEB_INTEGRATED_DATA_CODE_OUTCOME_TEMPLATE.md",
    "submission/GEB_INTEGRATED_PORTAL_HANDOFF_OUTCOME.md",
    "submission/PAYOFF_B_INTEGRATED_JOURNAL_TARGETING_20260925.md",
]


def copy(rel: str, out: Path) -> dict:
    src = ROOT / rel
    dst = out / src.name
    shutil.copy2(src, dst)
    return {
        "path": dst.name,
        "source": rel,
        "bytes": dst.stat().st_size,
        "sha256": sha256(dst),
    }


def outcome_cover_letter(result_json: Path) -> str:
    payload = json.loads(result_json.read_text(encoding="utf-8"))
    result_class = classify_result(payload)
    summary = {
        "PASS": (
            "The preregistered within-taxon industrial-mule-deer perturbation "
            "supported greater retention of incoming phase error under the "
            "large-development forcing regime."
        ),
        "FAIL_WRONG_DIRECTION": (
            "The preregistered within-taxon industrial-mule-deer perturbation "
            "failed in direction, separating the supported movement-control "
            "contrast from the phase-retention response."
        ),
        "FAIL_INSUFFICIENT_SUPPORT": (
            "The preregistered within-taxon industrial-mule-deer perturbation "
            "pointed in the predicted direction but did not pass its frozen "
            "inferential support gate."
        ),
        "NOT_ESTIMABLE": (
            "The preregistered within-taxon industrial-mule-deer phase-retention "
            "contrast was not estimable under the frozen reconstruction and "
            "support criteria, and no retuning was performed."
        ),
    }[result_class]

    return f"""# GEB integrated tracking ecology — cover-letter template

Dear Editors,

Please consider our Research Article, **“Temporal buffering delays but does not
replace spatial tracking under environmental change,”**
for *Global Ecology and Biogeography*.

Environmental mismatch is often used as a summary of how organisms track
changing conditions, but the same endpoint can arise from different mixtures of
movement, seasonal timing, environmental information and behavioral actuation.
We connect theory, simulation and registered reanalyses to ask whether mismatch
identifies the tracking process that produced it.

A local controller first shows an exact identification problem: movement and
timing can produce identical mismatch dynamics through different allocations of
restoring feedback. Explicit landscapes show why the hidden allocation matters,
because timing has finite capacity, movement experiences landscape geometry, and
interacting partners can face coordination barriers. Across 5,816 observations
from 55 migratory bird species, the data do not support one portable natural
animal-speed/environmental-wave-speed optimum. A registered chronological
holdout also found that stronger historical timing responsiveness did not
weaken later movement-speed dependence; the primary moderation failed in
direction. Direct reconstructions in mule deer, barnacle geese and Eurasian
wigeon instead show phase transformation on different ecological intervals and
through different actuator architectures.

Registered perturbation result: **{result_class}**. {summary}

The broad conclusion is unchanged by the perturbation class: **temporal
buffering delays but does not permanently replace spatial tracking under
sustained environmental change**. Low mismatch can therefore conceal latent
spatial tracking demand until timing capacity is exhausted; mismatch is the
outcome of that tracking system rather than a direct measure of its remaining
capacity.

[AUTHOR-CONFIRMED statement that the work is original, approved by all authors,
and not under consideration elsewhere.]

Potential reviewers / handling editors: [AUTHOR-CONTROLLED, CONFLICT-CHECKED].

Sincerely,

[CORRESPONDING AUTHOR — AUTHOR CONTROLLED]
"""


def build(
    manuscript: Path,
    result_json: Path,
    claim_state_json: Path,
    output_dir: Path,
    zip_path: Path | None = None,
) -> dict:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    geb_source = output_dir / "GEB_INTEGRATED_BLINDED_OUTCOME.md"
    geb_source.write_text(
        build_geb_source(manuscript, result_json),
        encoding="utf-8",
    )

    si = output_dir / "GEB_INTEGRATED_SUPPORTING_INFORMATION_OUTCOME.md"
    si.write_text(
        build_supporting_information(result_json),
        encoding="utf-8",
    )

    figures_dir = output_dir / "figures"
    rendered = render_geb_figures(figures_dir, result_json)

    audit_result = audit_geb_outcome(
        geb_source,
        result_json,
        claim_state_json,
        rendered["manifest"],
    )
    if not audit_result["all_outcome_hard_gates_pass"]:
        raise ValueError("outcome-rendered GEB source does not pass hard gates")

    audit_path = output_dir / "GEB_INTEGRATED_OUTCOME_AUDIT.json"
    audit_path.write_text(
        json.dumps(audit_result, indent=2) + "\n",
        encoding="utf-8",
    )

    cover = output_dir / "GEB_INTEGRATED_COVER_LETTER_OUTCOME.md"
    cover.write_text(outcome_cover_letter(result_json), encoding="utf-8")

    files = []
    for path, source in (
        (geb_source, "generated:GEB outcome-rendered blinded manuscript"),
        (si, "generated:GEB outcome-rendered Supporting Information"),
        (audit_path, "generated:GEB outcome audit"),
        (cover, "generated:GEB outcome cover-letter template"),
    ):
        files.append(
            {
                "path": path.name,
                "source": source,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )

    for rel in STATIC_FILES:
        files.append(copy(rel, output_dir))

    for i in range(1, 7):
        path = rendered[f"figure_{i}"]
        files.append(
            {
                "path": path.relative_to(output_dir).as_posix(),
                "source": f"generated:GEB outcome figure {i}",
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    fig_manifest = rendered["manifest"]
    files.append(
        {
            "path": fig_manifest.relative_to(output_dir).as_posix(),
            "source": "generated:GEB outcome figure manifest",
            "bytes": fig_manifest.stat().st_size,
            "sha256": sha256(fig_manifest),
        }
    )

    payload = json.loads(result_json.read_text(encoding="utf-8"))
    result_class = classify_result(payload)
    manifest = {
        "status": "payoff_b_geb_integrated_outcome_working_package",
        "journal": "Global Ecology and Biogeography",
        "article_type": "Research Article",
        "scientific_state": "OUTCOME_RENDERED_SCIENCE_READY",
        "scientific_result": result_class,
        "final_science_blocker": None,
        "final_submission_eligible": False,
        "remaining_portal_blockers": [
            "anonymous stable reviewer archive link",
            "author-controlled title-page and declaration metadata",
        ],
        "structured_abstract_words": audit_result["metrics"]["abstract_words"],
        "main_body_words": audit_result["metrics"]["main_body_words"],
        "references": audit_result["metrics"]["reference_count"],
        "display_pieces": audit_result["metrics"]["display_pieces"],
        "keywords": audit_result["metrics"]["keyword_count"],
        "aikens_result_present": True,
        "aikens_outcome_opened": audit_result["aikens_lambda_outcome_opened"],
        "file_count": len(files),
        "figure_count": 6,
        "files": files,
    }

    mp = output_dir / "GEB_INTEGRATED_OUTCOME_PACKAGE_MANIFEST.json"
    mp.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    if zip_path is not None:
        deterministic_zip(output_dir, zip_path)
        manifest["zip_path"] = str(zip_path)
        manifest["zip_bytes"] = zip_path.stat().st_size
        manifest["zip_sha256"] = sha256(zip_path)

    return manifest


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--manuscript", type=Path, required=True)
    p.add_argument("--result-json", type=Path, required=True)
    p.add_argument("--claim-state-json", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--zip", type=Path, required=True)
    args = p.parse_args()

    manifest = build(
        args.manuscript,
        args.result_json,
        args.claim_state_json,
        args.output_dir,
        args.zip,
    )
    print(
        "GEB_OUTCOME_PACKAGE "
        f"result={manifest['scientific_result']} "
        f"words={manifest['main_body_words']} "
        f"abstract={manifest['structured_abstract_words']} "
        f"zip_sha256={manifest.get('zip_sha256')}"
    )


if __name__ == "__main__":
    main()
