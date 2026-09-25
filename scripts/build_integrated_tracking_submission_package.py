#!/usr/bin/env python3
"""Build deterministic PREOUTCOME working package for integrated PAYOFF-B paper."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

from build_integrated_tracking_supporting_information import build_supporting_information
from render_integrated_tracking_figures import render_all

ROOT = Path(__file__).resolve().parents[1]
ZIP_TIMESTAMP = (2026, 9, 25, 0, 0, 0)

MANUSCRIPT = "manuscript/PAYOFF_B_INTEGRATED_TRACKING_ECOLOGY_V1_PREOUTCOME.md"

SUBMISSION_FILES = [
    "submission/PAYOFF_B_INTEGRATED_TITLE_PAGE_TEMPLATE.md",
    "submission/PAYOFF_B_INTEGRATED_COVER_LETTER_TEMPLATE.md",
    "submission/PAYOFF_B_INTEGRATED_DATA_CODE_TEMPLATE.md",
    "submission/PAYOFF_B_INTEGRATED_FIGURE_CAPTIONS.md",
    "submission/PAYOFF_B_INTEGRATED_PACKAGE_INDEX.md",
]

INTERNAL_FILES = [
    "docs/PAYOFF_B_TWO_PAPER_PUBLICATION_ARCHITECTURE_20260925.md",
    "docs/PUBLICATION_STATUS.md",
    "submission/PAYOFF_B_INTEGRATED_PREOUTCOME_READINESS_20260925.md",
    "submission/PAYOFF_B_INTEGRATED_FIGURE_SOURCE_CROSSWALK_20260925.md",
    "submission/PAYOFF_B_INTEGRATED_SIX_FIGURE_AUDIT_20260925.md",
]

EMPIRICAL_RECEIPTS = [
    "data/payoff_b_broad_bird_stage1_result_20260925.json",
    "data/payoff_b_empirical_phase_panel_status_20260921.json",
    "data/payoff_b_phase_retention_interval_standardization_result_20260925.json",
    "data/payoff_b_industrial_mule_deer_actuator_receipt_20260921.json",
    "data/wigeon_era5_sourcefaithful_calibration_result_20260924.json",
    "data/barnacle_era5_reliability_result_20260924.json",
    "data/svalbard_barnacle_era5_reliability_result_20260924.json",
    "data/aikens2022_lambda_perturbation_registration_20260921.json",
    "data/payoff_b_integrated_empirical_figure_inputs_20260925.json",
]

SYNTHETIC_RECEIPTS = [
    "data/payoff_b_tracking_synthetic_receipt_20260920.json",
    "data/payoff_b_moving_landscape_receipt_20260920.json",
    "data/payoff_b_2d_connectivity_receipt_20260920.json",
    "data/payoff_b_closed_loop_tracking_receipt_20260920.json",
    "data/payoff_b_movement_feedback_landscape_receipt_20260920.json",
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


def anonymous_preoutcome_main() -> str:
    source = (ROOT / MANUSCRIPT).read_text(encoding="utf-8")
    kept = []
    for line in source.splitlines():
        if line.startswith("**Status:**"):
            continue
        if line.startswith("**Publication architecture:**"):
            continue
        if line.startswith("**Evidence boundary:**"):
            continue
        kept.append(line)
    return "\n".join(kept).strip() + "\n"


def write_deterministic_zip(source_dir: Path, zip_path: Path) -> None:
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
        "status": "payoff_b_integrated_tracking_preoutcome_working_package",
        "package_date": "2026-09-25",
        "scientific_state": "PREOUTCOME_INTERNAL_READY",
        "final_submission_eligible": False,
        "final_submission_blocker": "registered Aikens fixed-24h lambda adjudication",
        "canonical_manuscript": MANUSCRIPT,
        "files": [],
    }

    anon = (
        output_dir
        / "submission_ready"
        / "PAYOFF_B_INTEGRATED_ANON_MAIN_TEXT_PREOUTCOME.md"
    )
    anon.parent.mkdir(parents=True, exist_ok=True)
    anon.write_text(anonymous_preoutcome_main(), encoding="utf-8")
    manifest["files"].append(
        {
            "bundle_path": str(anon.relative_to(output_dir)),
            "source": f"generated:anonymous_preoutcome_from:{MANUSCRIPT}",
            "bytes": anon.stat().st_size,
            "sha256": sha256(anon),
        }
    )

    for source_rel in SUBMISSION_FILES:
        manifest["files"].append(
            copy_one(source_rel, output_dir, "submission_ready")
        )

    si = (
        output_dir
        / "submission_ready"
        / "PAYOFF_B_INTEGRATED_SUPPORTING_INFORMATION_PREOUTCOME.md"
    )
    si.write_text(build_supporting_information(), encoding="utf-8")
    manifest["files"].append(
        {
            "bundle_path": str(si.relative_to(output_dir)),
            "source": "generated:integrated_supporting_information",
            "bytes": si.stat().st_size,
            "sha256": sha256(si),
        }
    )

    for source_rel in INTERNAL_FILES:
        manifest["files"].append(
            copy_one(source_rel, output_dir, "internal_contracts")
        )
    for source_rel in EMPIRICAL_RECEIPTS:
        manifest["files"].append(
            copy_one(source_rel, output_dir, "frozen_receipts/empirical")
        )
    for source_rel in SYNTHETIC_RECEIPTS:
        manifest["files"].append(
            copy_one(source_rel, output_dir, "frozen_receipts/synthetic")
        )

    figure_dir = output_dir / "figures"
    rendered = render_all(figure_dir)
    for i in range(1, 7):
        key = f"figure_{i}"
        path = Path(rendered[key])
        manifest["files"].append(
            {
                "bundle_path": str(path.relative_to(output_dir)),
                "source": f"generated:{key}",
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )

    fig_manifest = Path(rendered["manifest"])
    payload = json.loads(fig_manifest.read_text(encoding="utf-8"))
    for row in payload["figures"].values():
        row["path"] = Path(row["path"]).name
    fig_manifest.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    manifest["files"].append(
        {
            "bundle_path": str(fig_manifest.relative_to(output_dir)),
            "source": "generated:six_figure_manifest",
            "bytes": fig_manifest.stat().st_size,
            "sha256": sha256(fig_manifest),
        }
    )

    manifest["file_count"] = len(manifest["files"])
    manifest["figure_count"] = 6
    manifest["aikens_result_present"] = False
    manifest["aikens_outcome_opened"] = False

    manifest_path = (
        output_dir / "PAYOFF_B_INTEGRATED_PREOUTCOME_PACKAGE_MANIFEST.json"
    )
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    if zip_path is not None:
        zip_path.parent.mkdir(parents=True, exist_ok=True)
        if zip_path.exists():
            zip_path.unlink()
        write_deterministic_zip(output_dir, zip_path)
        receipt = {
            "status": "payoff_b_integrated_tracking_preoutcome_archive_receipt",
            "final_submission_eligible": False,
            "package_manifest": manifest_path.name,
            "package_manifest_sha256": sha256(manifest_path),
            "zip_file": zip_path.name,
            "zip_bytes": zip_path.stat().st_size,
            "zip_sha256": sha256(zip_path),
            "zip_timestamp": "2026-09-25T00:00:00",
            "aikens_outcome_opened": False,
        }
        receipt_path = (
            zip_path.parent
            / "PAYOFF_B_INTEGRATED_PREOUTCOME_ARCHIVE_RECEIPT.json"
        )
        receipt_path.write_text(
            json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
        )
        manifest["zip_path"] = str(zip_path)
        manifest["zip_sha256"] = receipt["zip_sha256"]
        manifest["archive_receipt_path"] = str(receipt_path)

    return manifest


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/integrated_tracking_submission_package"),
    )
    p.add_argument(
        "--zip",
        dest="zip_path",
        type=Path,
        default=Path(
            "outputs/PAYOFF_B_INTEGRATED_TRACKING_PREOUTCOME_PACKAGE.zip"
        ),
    )
    args = p.parse_args()
    manifest = build_package(args.output_dir, args.zip_path)
    print(
        args.output_dir
        / "PAYOFF_B_INTEGRATED_PREOUTCOME_PACKAGE_MANIFEST.json"
    )
    print(
        "integrated_preoutcome_package "
        f"files={manifest['file_count']} "
        f"figures={manifest['figure_count']} "
        f"zip_sha256={manifest.get('zip_sha256', 'none')}"
    )


if __name__ == "__main__":
    main()
