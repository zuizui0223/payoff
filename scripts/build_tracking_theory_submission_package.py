#!/usr/bin/env python3
"""Build a reproducible PAYOFF-B tracking-theory submission working package."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

from render_tracking_theory_figures import render_all
from build_tracking_theory_supporting_information import build_supporting_information
from build_oikos_review_manuscript import build_review_rtf
from build_oikos_supporting_information import build_supporting_rtf


ROOT = Path(__file__).resolve().parents[1]
ZIP_TIMESTAMP = (2026, 9, 24, 0, 0, 0)

SUBMISSION_FILES = [
    "manuscript/PAYOFF_B_TRACKING_THEORY_V1.md",
    "submission/PAYOFF_B_TRACKING_REFERENCES.bib",
    "submission/PAYOFF_B_TRACKING_FIGURE_CAPTIONS.md",
    "submission/PAYOFF_B_TRACKING_SUPPLEMENT_MAP.md",
    "submission/PAYOFF_B_TRACKING_TITLE_PAGE_TEMPLATE.md",
    "submission/PAYOFF_B_TRACKING_COVER_LETTER_TEMPLATE.md",
    "submission/OIKOS_TRACKING_HANDOFF_V1.md",
    "submission/OIKOS_SIGNIFICANCE_STATEMENT.md",
    "submission/OIKOS_DATA_AVAILABILITY_TEMPLATE.md",
    "submission/OIKOS_AI_USE_STATEMENT.md",
]

INTERNAL_FILES = [
    "data/payoff_b_tracking_theory_claim_freeze_20260924.json",
    "data/payoff_b_tracking_theory_framing_amendment_20260925.json",
    "docs/PAYOFF_B_TRACKING_THEORY_PRIOR_ART_20260924.md",
    "submission/PAYOFF_B_TRACKING_PARAMETER_TABLE.md",
    "submission/PAYOFF_B_TRACKING_RESULTS_FIGURE_CROSSWALK.md",
    "submission/PAYOFF_B_TRACKING_FIGURE_VISUAL_AUDIT.md",
    "submission/PAYOFF_B_TRACKING_SUBMISSION_READINESS.md",
    "submission/PAYOFF_B_TRACKING_PACKAGE_INDEX.md",
    "submission/PAYOFF_B_TRACKING_JOURNAL_TARGETING_20260924.md",
]

RECEIPT_FILES = [
    "data/payoff_b_tracking_synthetic_receipt_20260920.json",
    "data/payoff_b_moving_landscape_receipt_20260920.json",
    "data/payoff_b_2d_connectivity_receipt_20260920.json",
    "data/payoff_b_closed_loop_tracking_receipt_20260920.json",
    "data/payoff_b_movement_feedback_landscape_receipt_20260920.json",
    "docs/PAYOFF_B_TRACKING_SYNTHETIC_RESULTS_20260920.md",
    "docs/PAYOFF_B_MOVING_LANDSCAPE_RESULTS_20260920.md",
    "docs/PAYOFF_B_2D_CONNECTIVITY_RESULTS_20260920.md",
    "docs/PAYOFF_B_CLOSED_LOOP_TRACKING_RESULTS_20260920.md",
    "docs/PAYOFF_B_MOVEMENT_FEEDBACK_LANDSCAPE_RESULTS_20260920.md",
]

THEORY_FILES = [
    "theory/MIGRATION_PHENOLOGY_TRACKING.md",
    "theory/CLOSED_LOOP_MOVEMENT_PHENOLOGY_TRACKING.md",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_one(source_rel: str, destination: Path, prefix: str) -> dict:
    source = ROOT / source_rel
    if not source.exists():
        raise FileNotFoundError(source)
    target = destination / prefix / source.name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return {
        "bundle_path": str(target.relative_to(destination)),
        "source": source_rel,
        "bytes": target.stat().st_size,
        "sha256": sha256(target),
    }


def write_deterministic_zip(source_dir: Path, zip_path: Path) -> None:
    """Write byte-stable ZIP metadata for a fixed package content set."""
    with zipfile.ZipFile(
        zip_path,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for path in sorted(source_dir.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(source_dir).as_posix()
            info = zipfile.ZipInfo(relative, date_time=ZIP_TIMESTAMP)
            info.create_system = 3
            info.external_attr = (0o644 & 0xFFFF) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(
                info,
                path.read_bytes(),
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )


def build_package(output_dir: Path, zip_path: Path | None = None) -> dict:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "status": "payoff_b_tracking_theory_submission_working_package",
        "scientific_freeze_date": "2026-09-24",
        "synthetic_receipt_freeze_date": "2026-09-20",
        "journal_preparation": {
            "first_shot": "Oikos",
            "fallback": "Theoretical Ecology",
            "stretch": "Global Change Biology",
        },
        "files": [],
    }

    for source_rel in SUBMISSION_FILES:
        manifest["files"].append(
            copy_one(source_rel, output_dir, "submission_ready")
        )

    supporting_path = (
        output_dir
        / "submission_ready"
        / "PAYOFF_B_TRACKING_SUPPORTING_INFORMATION_V1.md"
    )
    supporting_path.write_text(
        build_supporting_information(),
        encoding="utf-8",
    )
    manifest["files"].append({
        "bundle_path": str(supporting_path.relative_to(output_dir)),
        "source": "generated:supporting_information",
        "bytes": supporting_path.stat().st_size,
        "sha256": sha256(supporting_path),
    })

    supporting_rtf_path = (
        output_dir
        / "submission_ready"
        / "OIKOS_TRACKING_SUPPORTING_INFORMATION.rtf"
    )
    supporting_rtf_path.write_text(
        build_supporting_rtf(),
        encoding="ascii",
    )
    manifest["files"].append({
        "bundle_path": str(supporting_rtf_path.relative_to(output_dir)),
        "source": "generated:oikos_supporting_information_rtf",
        "bytes": supporting_rtf_path.stat().st_size,
        "sha256": sha256(supporting_rtf_path),
    })

    review_rtf_path = (
        output_dir
        / "submission_ready"
        / "OIKOS_TRACKING_ANON_MAIN_TEXT.rtf"
    )
    review_rtf_path.write_text(
        build_review_rtf(),
        encoding="ascii",
    )
    manifest["files"].append({
        "bundle_path": str(review_rtf_path.relative_to(output_dir)),
        "source": "generated:oikos_anonymous_main_text",
        "bytes": review_rtf_path.stat().st_size,
        "sha256": sha256(review_rtf_path),
    })

    for source_rel in INTERNAL_FILES:
        manifest["files"].append(
            copy_one(source_rel, output_dir, "internal_contracts")
        )

    for source_rel in RECEIPT_FILES:
        manifest["files"].append(
            copy_one(source_rel, output_dir, "frozen_receipts")
        )

    for source_rel in THEORY_FILES:
        manifest["files"].append(
            copy_one(source_rel, output_dir, "theory")
        )

    figure_dir = output_dir / "figures"
    figure_manifest = render_all(figure_dir)
    for key, row in sorted(figure_manifest["figures"].items()):
        path = Path(row["path"])
        manifest["files"].append({
            "bundle_path": str(path.relative_to(output_dir)),
            "source": f"generated:{key}",
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })

    generated_figure_manifest = figure_dir / "PAYOFF_B_TRACKING_FIGURE_MANIFEST.json"
    bundled_figure_manifest = json.loads(
        generated_figure_manifest.read_text(encoding="utf-8")
    )
    for row in bundled_figure_manifest["figures"].values():
        row["path"] = Path(row["path"]).name
    generated_figure_manifest.write_text(
        json.dumps(bundled_figure_manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    manifest["files"].append({
        "bundle_path": str(generated_figure_manifest.relative_to(output_dir)),
        "source": "generated:figure_manifest",
        "bytes": generated_figure_manifest.stat().st_size,
        "sha256": sha256(generated_figure_manifest),
    })

    manifest["file_count"] = len(manifest["files"])
    manifest["figure_count"] = len(figure_manifest["figures"])

    manifest_path = output_dir / "PAYOFF_B_TRACKING_SUBMISSION_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    if zip_path is not None:
        zip_path.parent.mkdir(parents=True, exist_ok=True)
        if zip_path.exists():
            zip_path.unlink()
        write_deterministic_zip(output_dir, zip_path)
        archive_receipt = {
            "status": "payoff_b_tracking_theory_submission_archive_receipt",
            "scientific_freeze_date": manifest["scientific_freeze_date"],
            "package_manifest": str(manifest_path.name),
            "package_manifest_sha256": sha256(manifest_path),
            "zip_file": zip_path.name,
            "zip_bytes": zip_path.stat().st_size,
            "zip_sha256": sha256(zip_path),
            "zip_timestamp": "2026-09-24T00:00:00",
        }
        receipt_path = (
            zip_path.parent
            / "PAYOFF_B_TRACKING_SUBMISSION_ARCHIVE_RECEIPT.json"
        )
        receipt_path.write_text(
            json.dumps(archive_receipt, indent=2) + "\n",
            encoding="utf-8",
        )
        manifest["archive_receipt_path"] = str(receipt_path)
        manifest["zip_path"] = str(zip_path)
        manifest["zip_bytes"] = archive_receipt["zip_bytes"]
        manifest["zip_sha256"] = archive_receipt["zip_sha256"]

    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/tracking_theory_submission_package"),
    )
    parser.add_argument(
        "--zip",
        dest="zip_path",
        type=Path,
        default=Path("outputs/PAYOFF_B_TRACKING_SUBMISSION_PACKAGE.zip"),
    )
    args = parser.parse_args()
    manifest = build_package(args.output_dir, args.zip_path)
    print(args.output_dir / "PAYOFF_B_TRACKING_SUBMISSION_MANIFEST.json")
    print(
        "tracking_submission_package "
        f"files={manifest['file_count']} "
        f"figures={manifest['figure_count']} "
        f"zip_sha256={manifest.get('zip_sha256', 'none')}"
    )


if __name__ == "__main__":
    main()
