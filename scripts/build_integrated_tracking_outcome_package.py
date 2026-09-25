#!/usr/bin/env python3
"""Build deterministic science-ready package after registered Aikens adjudication."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

from build_integrated_tracking_outcome_supporting_information import (
    build_supporting_information,
)
from render_aikens_lambda_manuscript import classify_result

ROOT = Path(__file__).resolve().parents[1]
ZIP_TIMESTAMP = (2026, 9, 25, 0, 0, 0)

TEMPLATE_FILES = [
    "submission/PAYOFF_B_INTEGRATED_TITLE_PAGE_TEMPLATE.md",
    "submission/PAYOFF_B_INTEGRATED_COVER_LETTER_TEMPLATE.md",
    "submission/PAYOFF_B_INTEGRATED_DATA_CODE_TEMPLATE.md",
    "submission/PAYOFF_B_INTEGRATED_FIGURE_CAPTIONS.md",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def clean_anonymous_main(source: Path) -> str:
    kept = []
    for line in source.read_text(encoding="utf-8").splitlines():
        if line.startswith("**Status:**"):
            continue
        if line.startswith("**Publication architecture:**"):
            continue
        if line.startswith("**Evidence boundary:**"):
            continue
        kept.append(line)
    text = "\n".join(kept).strip() + "\n"
    if "PENDING" in text:
        raise ValueError("outcome-rendered anonymous main text still contains PENDING")
    return text


def clean_cover_letter() -> str:
    source = (
        ROOT / "submission" / "PAYOFF_B_INTEGRATED_COVER_LETTER_TEMPLATE.md"
    ).read_text(encoding="utf-8")
    start = source.find("**PREOUTCOME NOTE")
    if start >= 0:
        end = source.find("\n\nThis manuscript is", start)
        if end < 0:
            raise ValueError("cover-letter PREOUTCOME note terminator not found")
        source = source[:start] + source[end + 2 :]
    return source


def outcome_data_code_statement(result_class: str) -> str:
    source = (
        ROOT / "submission" / "PAYOFF_B_INTEGRATED_DATA_CODE_TEMPLATE.md"
    ).read_text(encoding="utf-8")
    marker = "## PREOUTCOME boundary"
    if marker in source:
        source = source.split(marker, 1)[0].rstrip()
    return (
        source
        + "\n\n## Registered Aikens adjudication\n\n"
        + f"The fixed-24 h industrial-mule-deer phase-retention test was "
        + f"adjudicated under its frozen contract as **{result_class}**. "
        + "The archived submission bundle includes the registered result JSON, "
        + "claim-state receipt, rendered figure manifest and post-outcome audit. "
        + "The Aikens test remains within taxon and is not added as another "
        + "cross-taxon replication.\n"
    )


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


def add_file(manifest: dict, root: Path, path: Path, source: str) -> None:
    manifest["files"].append(
        {
            "bundle_path": str(path.relative_to(root)),
            "source": source,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
    )


def build_package(
    *,
    manuscript: Path,
    result_json: Path,
    claim_state_json: Path,
    figure_dir: Path,
    postoutcome_audit_json: Path,
    output_dir: Path,
    zip_path: Path | None,
) -> dict:
    payload = json.loads(result_json.read_text(encoding="utf-8"))
    result_class = classify_result(payload)
    audit = json.loads(postoutcome_audit_json.read_text(encoding="utf-8"))
    claim = json.loads(claim_state_json.read_text(encoding="utf-8"))

    if audit.get("all_postoutcome_hard_gates_pass") is not True:
        raise ValueError("post-outcome manuscript audit did not pass")
    if audit.get("final_submission_science_ready") is not True:
        raise ValueError("post-outcome science state is not submission-ready")
    if claim.get("scientific_result") != result_class:
        raise ValueError("claim-state result class does not match registered result")
    if claim.get("retuning_permitted") is not False:
        raise ValueError("claim-state receipt does not forbid retuning")

    figure_manifest_path = (
        figure_dir / "PAYOFF_B_INTEGRATED_SIX_FIGURE_MANIFEST.json"
    )
    figure_manifest = json.loads(
        figure_manifest_path.read_text(encoding="utf-8")
    )
    if figure_manifest.get("aikens_result_present") is not True:
        raise ValueError("final figure set does not contain Aikens adjudication")

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "status": "payoff_b_integrated_tracking_outcome_package",
        "scientific_result": result_class,
        "final_submission_science_ready": True,
        "portal_metadata_complete": False,
        "author_metadata_complete": False,
        "retuning_permitted": False,
        "files": [],
    }

    ready = output_dir / "submission_ready"
    ready.mkdir(parents=True, exist_ok=True)

    anon = ready / "PAYOFF_B_INTEGRATED_ANON_MAIN_TEXT_OUTCOME_RENDERED.md"
    anon.write_text(clean_anonymous_main(manuscript), encoding="utf-8")
    add_file(manifest, output_dir, anon, "generated:outcome_rendered_anonymous_main")

    si = ready / "PAYOFF_B_INTEGRATED_SUPPORTING_INFORMATION_OUTCOME_RENDERED.md"
    si.write_text(build_supporting_information(result_json), encoding="utf-8")
    add_file(manifest, output_dir, si, "generated:outcome_rendered_supporting_information")

    for source_rel in TEMPLATE_FILES:
        source = ROOT / source_rel
        target = ready / source.name
        if source.name == "PAYOFF_B_INTEGRATED_COVER_LETTER_TEMPLATE.md":
            target = ready / "PAYOFF_B_INTEGRATED_COVER_LETTER_OUTCOME_WORKING.md"
            target.write_text(clean_cover_letter(), encoding="utf-8")
        elif source.name == "PAYOFF_B_INTEGRATED_DATA_CODE_TEMPLATE.md":
            target = ready / "PAYOFF_B_INTEGRATED_DATA_CODE_OUTCOME_WORKING.md"
            target.write_text(
                outcome_data_code_statement(result_class),
                encoding="utf-8",
            )
        else:
            shutil.copy2(source, target)
        add_file(manifest, output_dir, target, source_rel)

    figures_out = output_dir / "figures"
    figures_out.mkdir(parents=True, exist_ok=True)
    for i in range(1, 7):
        name = {
            1: "PAYOFF_B_INTEGRATED_FIG1_CONCEPT.svg",
            2: "PAYOFF_B_INTEGRATED_FIG2_TEMPORAL_BYPASS.svg",
            3: "PAYOFF_B_INTEGRATED_FIG3_COORDINATION_GATE.svg",
            4: "PAYOFF_B_INTEGRATED_FIG4_BROAD_BIRD.svg",
            5: "PAYOFF_B_INTEGRATED_FIG5_DIRECT_SYSTEMS.svg",
            6: "PAYOFF_B_INTEGRATED_FIG6_INFORMATION_ACTUATION.svg",
        }[i]
        source = figure_dir / name
        target = figures_out / name
        shutil.copy2(source, target)
        add_file(manifest, output_dir, target, f"rendered:{name}")

    normalized_figure_manifest = figures_out / figure_manifest_path.name
    for row in figure_manifest["figures"].values():
        row["path"] = Path(row["path"]).name
    normalized_figure_manifest.write_text(
        json.dumps(figure_manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    add_file(
        manifest,
        output_dir,
        normalized_figure_manifest,
        "rendered:six_figure_manifest",
    )

    evidence_dir = output_dir / "registered_outcome"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    for source, label in (
        (result_json, "registered_result_json"),
        (claim_state_json, "registered_claim_state"),
        (postoutcome_audit_json, "postoutcome_manuscript_audit"),
    ):
        target = evidence_dir / source.name
        shutil.copy2(source, target)
        add_file(manifest, output_dir, target, label)

    manifest["figure_count"] = 6
    manifest["file_count"] = len(manifest["files"])
    manifest["aikens_result_present"] = True
    manifest["aikens_outcome_opened"] = bool(
        figure_manifest.get("aikens_outcome_opened")
    )

    manifest_path = (
        output_dir / "PAYOFF_B_INTEGRATED_OUTCOME_PACKAGE_MANIFEST.json"
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
            "status": "payoff_b_integrated_tracking_outcome_archive_receipt",
            "scientific_result": result_class,
            "final_submission_science_ready": True,
            "portal_metadata_complete": False,
            "package_manifest_sha256": sha256(manifest_path),
            "zip_file": zip_path.name,
            "zip_bytes": zip_path.stat().st_size,
            "zip_sha256": sha256(zip_path),
            "zip_timestamp": "2026-09-25T00:00:00",
        }
        receipt_path = (
            zip_path.parent
            / "PAYOFF_B_INTEGRATED_OUTCOME_ARCHIVE_RECEIPT.json"
        )
        receipt_path.write_text(
            json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
        )
        manifest["zip_sha256"] = receipt["zip_sha256"]
        manifest["zip_path"] = str(zip_path)
        manifest["archive_receipt_path"] = str(receipt_path)

    return manifest


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--manuscript", type=Path, required=True)
    p.add_argument("--result-json", type=Path, required=True)
    p.add_argument("--claim-state-json", type=Path, required=True)
    p.add_argument("--figure-dir", type=Path, required=True)
    p.add_argument("--postoutcome-audit-json", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--zip", dest="zip_path", type=Path, required=True)
    args = p.parse_args()
    manifest = build_package(
        manuscript=args.manuscript,
        result_json=args.result_json,
        claim_state_json=args.claim_state_json,
        figure_dir=args.figure_dir,
        postoutcome_audit_json=args.postoutcome_audit_json,
        output_dir=args.output_dir,
        zip_path=args.zip_path,
    )
    print(
        "integrated_outcome_package "
        f"result={manifest['scientific_result']} "
        f"files={manifest['file_count']} "
        f"zip_sha256={manifest.get('zip_sha256', 'none')}"
    )


if __name__ == "__main__":
    main()
