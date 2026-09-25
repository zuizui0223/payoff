#!/usr/bin/env python3
"""Build deterministic PREOUTCOME submission and anonymous-review packages."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path

from build_integrated_tracking_supporting_information import build_supporting_information
from render_integrated_tracking_figures import render_all as render_figures

ROOT = Path(__file__).resolve().parents[1]
ZIP_TIMESTAMP = (2026, 9, 25, 0, 0, 0)

MANUSCRIPT = "manuscript/PAYOFF_B_INTEGRATED_TRACKING_ECOLOGY_V1_PREOUTCOME.md"

SUBMISSION_TEMPLATES = [
    "submission/PAYOFF_B_INTEGRATED_TITLE_PAGE_TEMPLATE.md",
    "submission/PAYOFF_B_INTEGRATED_COVER_LETTER_TEMPLATE.md",
    "submission/PAYOFF_B_INTEGRATED_DATA_AVAILABILITY_TEMPLATE.md",
    "submission/PAYOFF_B_INTEGRATED_AI_USE_TEMPLATE.md",
    "submission/PAYOFF_B_INTEGRATED_SUPPLEMENT_MAP_20260925.md",
    "submission/PAYOFF_B_INTEGRATED_FIGURE_SOURCE_CROSSWALK_20260925.md",
    "submission/PAYOFF_B_INTEGRATED_SIX_FIGURE_AUDIT_20260925.md",
]

INTERNAL_CONTRACTS = [
    "docs/PAYOFF_B_TWO_PAPER_PUBLICATION_ARCHITECTURE_20260925.md",
    "docs/PUBLICATION_STATUS.md",
    "data/payoff_b_broad_bird_stage1_result_20260925.json",
    "data/payoff_b_empirical_phase_panel_status_20260921.json",
    "data/payoff_b_phase_retention_interval_standardization_result_20260925.json",
    "data/payoff_b_integrated_empirical_figure_inputs_20260925.json",
    "data/payoff_b_industrial_mule_deer_actuator_receipt_20260921.json",
    "data/aikens2022_lambda_perturbation_registration_20260921.json",
    "data/aikens2022_lambda_outcome_interpretation_contract_20260922.json",
]

SYNTHETIC_RECEIPTS = [
    "data/payoff_b_tracking_synthetic_receipt_20260920.json",
    "data/payoff_b_moving_landscape_receipt_20260920.json",
    "data/payoff_b_2d_connectivity_receipt_20260920.json",
    "data/payoff_b_closed_loop_tracking_receipt_20260920.json",
    "data/payoff_b_movement_feedback_landscape_receipt_20260920.json",
]

REVIEW_CODE = [
    "scripts/build_integrated_tracking_supporting_information.py",
    "scripts/render_integrated_tracking_empirical_figures.py",
    "scripts/render_integrated_tracking_figures.py",
    "scripts/audit_integrated_tracking_manuscript.py",
    "scripts/audit_rendered_integrated_tracking_manuscript.py",
    "scripts/render_aikens_lambda_manuscript.py",
    "scripts/build_tracking_theory_supporting_information.py",
    "scripts/build_tracking_theory_figure_data.py",
    "scripts/render_tracking_theory_figures.py",
    "src/spatiotemporal_tracking.py",
    "src/moving_climate_landscape_2d.py",
]

IDENTITY_PATTERNS = {
    "author_name": re.compile(r"\bZHANG\b|\bRuiqi\b|張瑞琪", re.I),
    "repository_owner": re.compile(r"zuizui0223|github\.com/zuizui0223", re.I),
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def copy_file(source_rel: str, destination: Path, folder: str) -> dict:
    source = ROOT / source_rel
    if not source.exists():
        raise FileNotFoundError(source)
    target = destination / folder / source.name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return {
        "bundle_path": target.relative_to(destination).as_posix(),
        "source": source_rel,
        "bytes": target.stat().st_size,
        "sha256": sha256(target),
    }


def write_deterministic_zip(source_dir: Path, zip_path: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(
        zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as z:
        for path in sorted(p for p in source_dir.rglob("*") if p.is_file()):
            rel = path.relative_to(source_dir).as_posix()
            info = zipfile.ZipInfo(rel, date_time=ZIP_TIMESTAMP)
            info.create_system = 3
            info.external_attr = (0o644 & 0xFFFF) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(
                info,
                path.read_bytes(),
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )


def identity_hits(root: Path) -> dict[str, list[str]]:
    hits = {k: [] for k in IDENTITY_PATTERNS}
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        if path.suffix.lower() not in {".md", ".txt", ".json", ".py", ".csv", ".svg"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name, pattern in IDENTITY_PATTERNS.items():
            if pattern.search(text):
                hits[name].append(path.relative_to(root).as_posix())
    return hits


def build_anonymous_review_bundle(
    output_dir: Path,
    zip_path: Path | None = None,
) -> dict:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    files: list[dict] = []
    files.append(copy_file(MANUSCRIPT, output_dir, "manuscript"))

    si_path = output_dir / "supporting_information" / "PAYOFF_B_INTEGRATED_TRACKING_SUPPORTING_INFORMATION_V1.md"
    si_path.parent.mkdir(parents=True, exist_ok=True)
    si_path.write_text(build_supporting_information(), encoding="utf-8")
    files.append({
        "bundle_path": si_path.relative_to(output_dir).as_posix(),
        "source": "generated:integrated_supporting_information",
        "bytes": si_path.stat().st_size,
        "sha256": sha256(si_path),
    })

    fig_dir = output_dir / "figures"
    rendered = render_figures(fig_dir)
    for i in range(1, 7):
        path = rendered[f"figure_{i}"]
        files.append({
            "bundle_path": path.relative_to(output_dir).as_posix(),
            "source": f"generated:figure_{i}",
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    figure_manifest = rendered["manifest"]
    files.append({
        "bundle_path": figure_manifest.relative_to(output_dir).as_posix(),
        "source": "generated:six_figure_manifest",
        "bytes": figure_manifest.stat().st_size,
        "sha256": sha256(figure_manifest),
    })

    for rel in SYNTHETIC_RECEIPTS:
        files.append(copy_file(rel, output_dir, "data/synthetic"))
    for rel in INTERNAL_CONTRACTS[2:]:
        files.append(copy_file(rel, output_dir, "data/empirical"))
    for rel in REVIEW_CODE:
        files.append(copy_file(rel, output_dir, "code"))

    readme = output_dir / "README_REVIEW.md"
    readme.write_text(
        "# Anonymous reviewer bundle\n\n"
        "This bundle accompanies the PREOUTCOME integrated PAYOFF-B tracking ecology manuscript.\n\n"
        "The broad 55-species test is the primary cross-system generality result. "
        "Direct taxa provide mechanistic decomposition rather than a formal meta-analysis. "
        "Synthetic parameter-grid frequencies are not natural prevalence estimates, and "
        "raw lambda values are not pooled across incompatible ecological intervals.\n\n"
        "The preregistered Aikens fixed-24h lambda outcome is UNOPENED in this bundle. "
        "The manuscript and Figure 6 contain an outcome-blind slot that is populated only "
        "by the registered renderer after adjudication.\n\n"
        "Figures 1–6 are reproducibly rendered from the included machine receipts and code. "
        "Supporting Information S1–S12 is generated from the same frozen evidence layers.\n",
        encoding="utf-8",
    )
    files.append({
        "bundle_path": "README_REVIEW.md",
        "source": "generated:review_readme",
        "bytes": readme.stat().st_size,
        "sha256": sha256(readme),
    })

    hits = identity_hits(output_dir)
    nonempty_hits = {k: v for k, v in hits.items() if v}
    if nonempty_hits:
        raise ValueError(f"anonymous review bundle identity leak: {nonempty_hits}")

    manifest = {
        "status": "payoff_b_integrated_tracking_anonymous_review_bundle",
        "scientific_state": "PREOUTCOME_INTERNAL_READY",
        "aikens_lambda_outcome_opened": False,
        "file_count": len(files),
        "figure_count": 6,
        "identity_scan": hits,
        "files": files,
    }
    manifest_path = output_dir / "PAYOFF_B_INTEGRATED_REVIEW_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    if zip_path is not None:
        write_deterministic_zip(output_dir, zip_path)
        manifest["zip_path"] = str(zip_path)
        manifest["zip_bytes"] = zip_path.stat().st_size
        manifest["zip_sha256"] = sha256(zip_path)

    return manifest


def build_submission_package(
    output_dir: Path,
    zip_path: Path | None = None,
    review_zip_path: Path | None = None,
) -> dict:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    files: list[dict] = []
    files.append(copy_file(MANUSCRIPT, output_dir, "submission_ready"))

    for rel in SUBMISSION_TEMPLATES:
        files.append(copy_file(rel, output_dir, "submission_ready"))

    si_path = output_dir / "submission_ready" / "PAYOFF_B_INTEGRATED_TRACKING_SUPPORTING_INFORMATION_V1.md"
    si_path.write_text(build_supporting_information(), encoding="utf-8")
    files.append({
        "bundle_path": si_path.relative_to(output_dir).as_posix(),
        "source": "generated:integrated_supporting_information",
        "bytes": si_path.stat().st_size,
        "sha256": sha256(si_path),
    })

    fig_dir = output_dir / "figures"
    rendered = render_figures(fig_dir)
    for i in range(1, 7):
        path = rendered[f"figure_{i}"]
        files.append({
            "bundle_path": path.relative_to(output_dir).as_posix(),
            "source": f"generated:figure_{i}",
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    figure_manifest = rendered["manifest"]
    files.append({
        "bundle_path": figure_manifest.relative_to(output_dir).as_posix(),
        "source": "generated:six_figure_manifest",
        "bytes": figure_manifest.stat().st_size,
        "sha256": sha256(figure_manifest),
    })

    for rel in INTERNAL_CONTRACTS:
        files.append(copy_file(rel, output_dir, "internal_contracts"))
    for rel in SYNTHETIC_RECEIPTS:
        files.append(copy_file(rel, output_dir, "frozen_receipts"))

    review_dir = output_dir / "anonymous_review_bundle"
    internal_review_zip = output_dir / "anonymous_review_bundle.zip"
    review_manifest = build_anonymous_review_bundle(review_dir, internal_review_zip)
    files.append({
        "bundle_path": internal_review_zip.relative_to(output_dir).as_posix(),
        "source": "generated:anonymous_review_bundle",
        "bytes": internal_review_zip.stat().st_size,
        "sha256": sha256(internal_review_zip),
    })

    manifest = {
        "status": "payoff_b_integrated_tracking_submission_working_package",
        "scientific_state": "PREOUTCOME_INTERNAL_READY",
        "aikens_lambda_outcome_opened": False,
        "final_science_blocker": "registered Aikens fixed-24h lambda adjudication",
        "journal_overlay": "NOT_YET_SELECTED",
        "author_controlled_fields_required": True,
        "file_count": len(files),
        "figure_count": 6,
        "review_bundle": {
            "file_count": review_manifest["file_count"],
            "zip_sha256": review_manifest.get("zip_sha256"),
            "identity_scan": review_manifest["identity_scan"],
        },
        "files": files,
    }

    manifest_path = output_dir / "PAYOFF_B_INTEGRATED_SUBMISSION_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    if zip_path is not None:
        write_deterministic_zip(output_dir, zip_path)
        manifest["zip_path"] = str(zip_path)
        manifest["zip_bytes"] = zip_path.stat().st_size
        manifest["zip_sha256"] = sha256(zip_path)

    if review_zip_path is not None:
        review_zip_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(internal_review_zip, review_zip_path)
        manifest["external_review_zip_path"] = str(review_zip_path)
        manifest["external_review_zip_sha256"] = sha256(review_zip_path)

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
        default=Path("outputs/PAYOFF_B_INTEGRATED_TRACKING_SUBMISSION_PACKAGE.zip"),
    )
    p.add_argument(
        "--review-zip",
        type=Path,
        default=Path("outputs/PAYOFF_B_INTEGRATED_TRACKING_ANON_REVIEW.zip"),
    )
    args = p.parse_args()

    manifest = build_submission_package(
        args.output_dir,
        args.zip_path,
        args.review_zip,
    )
    print(args.output_dir / "PAYOFF_B_INTEGRATED_SUBMISSION_MANIFEST.json")
    print(
        "integrated_submission_package "
        f"files={manifest['file_count']} "
        f"figures={manifest['figure_count']} "
        f"zip_sha256={manifest.get('zip_sha256', 'none')} "
        f"review_zip_sha256={manifest.get('external_review_zip_sha256', 'none')}"
    )


if __name__ == "__main__":
    main()
