#!/usr/bin/env python3
"""Build deterministic GEB PREOUTCOME package for canonical PAYOFF-B V2."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

from audit_payoff_b_v2_geb_source import audit
from build_payoff_b_v2_geb_source import build_source
from build_payoff_b_v2_geb_supporting_information import (
    build_supporting_information,
)
from render_information_deadlines_figures import render_all

ROOT = Path(__file__).resolve().parents[1]
ZIP_TIMESTAMP = (2026, 9, 27, 0, 0, 0)

STATIC_FILES = (
    "submission/GEB_V2_TITLE_PAGE_TEMPLATE.md",
    "submission/GEB_V2_COVER_LETTER_PREOUTCOME.md",
    "submission/GEB_V2_DATA_CODE_TEMPLATE.md",
    "submission/GEB_V2_PORTAL_HANDOFF_PREOUTCOME.md",
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


def build(output_dir: Path, zip_path: Path | None = None) -> dict:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    main = output_dir / "GEB_V2_BLINDED_PREOUTCOME.md"
    main.write_text(build_source(), encoding="utf-8")

    audit_result = audit(main.read_text(encoding="utf-8"))
    if not audit_result["all_preoutcome_hard_gates_pass"]:
        raise ValueError(
            "V2 GEB blinded source failed hard gates: "
            + json.dumps(audit_result["gates"], sort_keys=True)
        )
    audit_path = output_dir / "GEB_V2_PREOUTCOME_AUDIT.json"
    audit_path.write_text(
        json.dumps(audit_result, indent=2) + "\n",
        encoding="utf-8",
    )

    si = output_dir / "GEB_V2_SUPPORTING_INFORMATION_PREOUTCOME.md"
    si.write_text(build_supporting_information(), encoding="utf-8")

    pending = output_dir / "REGISTERED_INDUSTRIAL_PHASE_RETENTION_PENDING.md"
    pending.write_text(
        "# Registered industrial-development phase-retention supplement\n\n"
        "Status: UNOPENED.\n\n"
        "This registered result is reserved for Supporting Information. "
        "It is not used to tune the title, structured abstract, primary "
        "information-deadline result, perfect-information recovery-failure "
        "result, natural evidence boundaries or current figures.\n",
        encoding="utf-8",
    )

    figures_dir = output_dir / "figures"
    rendered = render_all(figures_dir)

    files = [
        {
            "path": main.name,
            "source": "generated:canonical V2 GEB blinded overlay",
            "bytes": main.stat().st_size,
            "sha256": sha256(main),
        },
        {
            "path": audit_path.name,
            "source": "generated:V2 GEB audit",
            "bytes": audit_path.stat().st_size,
            "sha256": sha256(audit_path),
        },
        {
            "path": si.name,
            "source": "generated:V2 Supporting Information",
            "bytes": si.stat().st_size,
            "sha256": sha256(si),
        },
        {
            "path": pending.name,
            "source": "generated:registered unopened supplement marker",
            "bytes": pending.stat().st_size,
            "sha256": sha256(pending),
        },
    ]

    for rel in STATIC_FILES:
        files.append(_copy(rel, output_dir))

    for index in range(1, 8):
        path = rendered[f"figure_{index}"]
        files.append(
            {
                "path": path.relative_to(output_dir).as_posix(),
                "source": f"generated:V2 figure {index}",
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )

    fig_manifest = rendered["manifest"]
    files.append(
        {
            "path": fig_manifest.relative_to(output_dir).as_posix(),
            "source": "generated:V2 figure manifest",
            "bytes": fig_manifest.stat().st_size,
            "sha256": sha256(fig_manifest),
        }
    )

    manifest = {
        "status": "payoff_b_v2_geb_preoutcome_working_package",
        "journal": "Global Ecology and Biogeography",
        "article_type": "Research Article",
        "canonical_source": (
            "manuscript/PAYOFF_B_INFORMATION_COORDINATION_V2_PREOUTCOME.md"
        ),
        "scientific_state": "PREOUTCOME_INTERNAL_READY",
        "v1_status": "FROZEN_PROVENANCE_ONLY",
        "aikens_outcome_opened": False,
        "final_submission_eligible": False,
        "final_submission_blockers": [
            "registered industrial-development phase-retention result",
            "anonymous stable reviewer archive link",
            "author-controlled title-page and declaration metadata",
            "final post-result package regeneration",
        ],
        "structured_abstract_words": audit_result["metrics"]["abstract_words"],
        "main_body_words": audit_result["metrics"]["main_body_words"],
        "references": audit_result["metrics"]["reference_count"],
        "display_pieces": audit_result["metrics"]["figure_legend_count"],
        "keywords": audit_result["metrics"]["keyword_count"],
        "file_count": len(files),
        "figure_count": 7,
        "files": files,
    }

    manifest_path = output_dir / "GEB_V2_PREOUTCOME_PACKAGE_MANIFEST.json"
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
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/payoff_b_v2_geb_preoutcome_package"),
    )
    parser.add_argument(
        "--zip",
        type=Path,
        default=Path("outputs/PAYOFF_B_V2_GEB_PREOUTCOME_PACKAGE.zip"),
    )
    args = parser.parse_args()
    manifest = build(args.output_dir, args.zip)
    print(
        "PAYOFF_B_V2_GEB_PACKAGE "
        f"main_words={manifest['main_body_words']} "
        f"abstract={manifest['structured_abstract_words']} "
        f"references={manifest['references']} "
        f"figures={manifest['figure_count']} "
        f"zip_sha256={manifest.get('zip_sha256')}"
    )


if __name__ == "__main__":
    main()
