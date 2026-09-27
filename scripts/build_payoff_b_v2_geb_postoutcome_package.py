#!/usr/bin/env python3
"""Build deterministic postoutcome GEB package for canonical PAYOFF-B V2.

The registered industrial-development phase-retention outcome is rendered only
into Supporting Information and a claim-state receipt. The blinded main text
and seven main figures are outcome-invariant by construction.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

from audit_payoff_b_v2_geb_source import audit
from build_payoff_b_v2_geb_source import build_source
from build_payoff_b_v2_geb_postoutcome_supporting_information import (
    render_supporting_information,
)
from render_information_deadlines_figures import render_all


ROOT = Path(__file__).resolve().parents[1]
ZIP_TIMESTAMP = (2026, 9, 27, 0, 0, 0)

STATIC_FILES = (
    "submission/GEB_V2_TITLE_PAGE_POSTOUTCOME_TEMPLATE.md",
    "submission/GEB_V2_COVER_LETTER_POSTOUTCOME.md",
    "submission/GEB_V2_DATA_CODE_POSTOUTCOME.md",
    "submission/GEB_V2_PORTAL_HANDOFF_POSTOUTCOME.md",
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def deterministic_zip(source_dir: Path, zip_path: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(
        zip_path,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for path in sorted(p for p in source_dir.rglob("*") if p.is_file()):
            info = zipfile.ZipInfo(
                path.relative_to(source_dir).as_posix(),
                date_time=ZIP_TIMESTAMP,
            )
            info.create_system = 3
            info.external_attr = (0o644 & 0xFFFF) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(
                info,
                path.read_bytes(),
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )


def _copy(rel: str, output_dir: Path) -> dict:
    source = ROOT / rel
    target = output_dir / source.name
    shutil.copy2(source, target)
    return {
        "path": target.name,
        "source": rel,
        "bytes": target.stat().st_size,
        "sha256": sha256(target),
    }


def build(
    output_dir: Path,
    *,
    result_json: Path,
    zip_path: Path | None = None,
) -> dict:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    payload = json.loads(result_json.read_text(encoding="utf-8"))
    supporting_text, claim_state = render_supporting_information(payload)

    main = output_dir / "GEB_V2_BLINDED_POSTOUTCOME.md"
    main.write_text(build_source(), encoding="utf-8")
    audit_result = audit(main.read_text(encoding="utf-8"))
    if not audit_result["all_preoutcome_hard_gates_pass"]:
        raise ValueError(
            "V2 GEB blinded main source failed invariant hard gates: "
            + json.dumps(audit_result["gates"], sort_keys=True)
        )

    audit_path = output_dir / "GEB_V2_POSTOUTCOME_MAIN_AUDIT.json"
    audit_path.write_text(
        json.dumps(audit_result, indent=2) + "\n",
        encoding="utf-8",
    )

    si = output_dir / "GEB_V2_SUPPORTING_INFORMATION_POSTOUTCOME.md"
    si.write_text(supporting_text, encoding="utf-8")

    result_copy = output_dir / "AIKENS_PHASE_RETENTION_RESULT.json"
    result_copy.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )

    claim_path = output_dir / "AIKENS_V2_CLAIM_STATE.json"
    claim_path.write_text(
        json.dumps(claim_state, indent=2) + "\n",
        encoding="utf-8",
    )

    figures_dir = output_dir / "figures"
    rendered = render_all(figures_dir)
    fig_manifest = rendered["manifest"]

    files = [
        {
            "path": main.name,
            "source": "generated:canonical V2 outcome-invariant blinded main",
            "bytes": main.stat().st_size,
            "sha256": sha256(main),
        },
        {
            "path": audit_path.name,
            "source": "generated:V2 invariant main audit",
            "bytes": audit_path.stat().st_size,
            "sha256": sha256(audit_path),
        },
        {
            "path": si.name,
            "source": "generated:outcome-specific V2 Supporting Information",
            "bytes": si.stat().st_size,
            "sha256": sha256(si),
        },
        {
            "path": result_copy.name,
            "source": "frozen:registered industrial-development result",
            "bytes": result_copy.stat().st_size,
            "sha256": sha256(result_copy),
        },
        {
            "path": claim_path.name,
            "source": "generated:V2 outcome claim state",
            "bytes": claim_path.stat().st_size,
            "sha256": sha256(claim_path),
        },
    ]

    for rel in STATIC_FILES:
        files.append(_copy(rel, output_dir))

    for index in range(1, 8):
        path = rendered[f"figure_{index}"]
        files.append(
            {
                "path": path.relative_to(output_dir).as_posix(),
                "source": f"generated:outcome-invariant V2 figure {index}",
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )

    files.append(
        {
            "path": fig_manifest.relative_to(output_dir).as_posix(),
            "source": "generated:outcome-invariant V2 figure manifest",
            "bytes": fig_manifest.stat().st_size,
            "sha256": sha256(fig_manifest),
        }
    )

    result_class = claim_state["scientific_result"]
    main_sha = sha256(main)
    fig_manifest_sha = sha256(fig_manifest)

    manifest = {
        "status": "payoff_b_v2_geb_postoutcome_working_package",
        "journal": "Global Ecology and Biogeography",
        "article_type": "Research Article",
        "canonical_source": (
            "manuscript/PAYOFF_B_INFORMATION_COORDINATION_V2_PREOUTCOME.md"
        ),
        "scientific_state": "POSTOUTCOME_INTERNAL_READY",
        "v1_status": "FROZEN_PROVENANCE_ONLY",
        "aikens_outcome_opened": True,
        "aikens_result_class": result_class,
        "aikens_result_surface": "Supporting Information only",
        "retuning_permitted": False,
        "outcome_invariance": {
            "title_changed": False,
            "structured_abstract_changed": False,
            "main_text_changed": False,
            "figures_changed": False,
            "main_sha256": main_sha,
            "figure_manifest_sha256": fig_manifest_sha,
        },
        "final_submission_eligible": False,
        "final_submission_blockers": [
            "anonymous stable reviewer archive link",
            "author-controlled title-page and declaration metadata",
        ],
        "structured_abstract_words": audit_result["metrics"]["abstract_words"],
        "main_body_words": audit_result["metrics"]["main_body_words"],
        "references": audit_result["metrics"]["reference_count"],
        "display_pieces": audit_result["metrics"]["figure_legend_count"],
        "keywords": audit_result["metrics"]["keyword_count"],
        "figure_count": 7,
        "file_count": len(files),
        "files": files,
    }

    manifest_path = output_dir / "GEB_V2_POSTOUTCOME_PACKAGE_MANIFEST.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    if zip_path is not None:
        deterministic_zip(output_dir, zip_path)
        manifest["zip_path"] = str(zip_path)
        manifest["zip_bytes"] = zip_path.stat().st_size
        manifest["zip_sha256"] = sha256(zip_path)

    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result-json", type=Path, required=True)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/payoff_b_v2_geb_postoutcome_package"),
    )
    parser.add_argument(
        "--zip",
        type=Path,
        default=Path("outputs/PAYOFF_B_V2_GEB_POSTOUTCOME_PACKAGE.zip"),
    )
    args = parser.parse_args()

    manifest = build(
        args.output_dir,
        result_json=args.result_json,
        zip_path=args.zip,
    )
    print(
        "PAYOFF_B_V2_GEB_POSTOUTCOME_PACKAGE "
        f"result={manifest['aikens_result_class']} "
        f"main_sha={manifest['outcome_invariance']['main_sha256']} "
        f"fig_manifest_sha={manifest['outcome_invariance']['figure_manifest_sha256']} "
        f"zip_sha256={manifest.get('zip_sha256')}"
    )


if __name__ == "__main__":
    main()
