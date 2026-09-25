#!/usr/bin/env python3
"""Build deterministic GEB PREOUTCOME working package for integrated PAYOFF-B."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

from build_geb_integrated_preoutcome_source import build_source
from build_integrated_tracking_supporting_information import build_supporting_information
from render_geb_integrated_figures import render_all as render_geb_figures
from audit_geb_integrated_preoutcome import audit as audit_geb

ROOT = Path(__file__).resolve().parents[1]
ZIP_TIMESTAMP = (2026, 9, 25, 0, 0, 0)

FILES = [
    "submission/GEB_INTEGRATED_TITLE_PAGE_TEMPLATE.md",
    "submission/GEB_INTEGRATED_COVER_LETTER_PREOUTCOME.md",
    "submission/GEB_INTEGRATED_DATA_CODE_TEMPLATE.md",
    "submission/GEB_INTEGRATED_PORTAL_HANDOFF_PREOUTCOME.md",
    "submission/PAYOFF_B_INTEGRATED_JOURNAL_TARGETING_20260925.md",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def deterministic_zip(source_dir: Path, zip_path: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(
        zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as z:
        for path in sorted(p for p in source_dir.rglob("*") if p.is_file()):
            info = zipfile.ZipInfo(
                path.relative_to(source_dir).as_posix(),
                date_time=ZIP_TIMESTAMP,
            )
            info.create_system = 3
            info.external_attr = (0o644 & 0xFFFF) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(
                info,
                path.read_bytes(),
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )


def copy(rel: str, out: Path) -> dict:
    source = ROOT / rel
    target = out / source.name
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

    blinded = output_dir / "GEB_INTEGRATED_BLINDED_PREOUTCOME.md"
    blinded.write_text(build_source(), encoding="utf-8")

    audit_result = audit_geb(blinded)
    if not audit_result["all_preoutcome_hard_gates_pass"]:
        raise ValueError("GEB PREOUTCOME overlay does not pass hard gates")

    audit_path = output_dir / "GEB_INTEGRATED_PREOUTCOME_AUDIT.json"
    audit_path.write_text(json.dumps(audit_result, indent=2) + "\n", encoding="utf-8")

    si = output_dir / "GEB_INTEGRATED_SUPPORTING_INFORMATION.md"
    si.write_text(build_supporting_information(), encoding="utf-8")

    figures_dir = output_dir / "figures"
    rendered = render_geb_figures(figures_dir)

    files = [
        {
            "path": blinded.name,
            "source": "generated:GEB blinded manuscript",
            "bytes": blinded.stat().st_size,
            "sha256": sha256(blinded),
        },
        {
            "path": audit_path.name,
            "source": "generated:GEB PREOUTCOME audit",
            "bytes": audit_path.stat().st_size,
            "sha256": sha256(audit_path),
        },
        {
            "path": si.name,
            "source": "generated:integrated Supporting Information",
            "bytes": si.stat().st_size,
            "sha256": sha256(si),
        },
    ]
    for rel in FILES:
        files.append(copy(rel, output_dir))

    for i in range(1, 7):
        path = rendered[f"figure_{i}"]
        files.append({
            "path": path.relative_to(output_dir).as_posix(),
            "source": f"generated:GEB figure {i}",
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    manifest_path = rendered["manifest"]
    files.append({
        "path": manifest_path.relative_to(output_dir).as_posix(),
        "source": "generated:GEB figure manifest",
        "bytes": manifest_path.stat().st_size,
        "sha256": sha256(manifest_path),
    })

    manifest = {
        "status": "payoff_b_geb_integrated_preoutcome_working_package",
        "journal": "Global Ecology and Biogeography",
        "article_type": "Research Article",
        "scientific_state": "PREOUTCOME_INTERNAL_READY",
        "final_submission_eligible": False,
        "final_submission_blockers": [
            "registered Aikens fixed-24h lambda adjudication",
            "anonymous stable reviewer archive link",
            "author-controlled title-page and declaration metadata",
        ],
        "structured_abstract_words": audit_result["metrics"]["abstract_words"],
        "main_body_words": audit_result["metrics"]["main_body_words"],
        "references": audit_result["metrics"]["reference_count"],
        "display_pieces": audit_result["metrics"]["display_pieces"],
        "keywords": audit_result["metrics"]["keyword_count"],
        "file_count": len(files),
        "figure_count": 6,
        "files": files,
    }
    mp = output_dir / "GEB_INTEGRATED_PREOUTCOME_PACKAGE_MANIFEST.json"
    mp.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    if zip_path is not None:
        deterministic_zip(output_dir, zip_path)
        manifest["zip_path"] = str(zip_path)
        manifest["zip_bytes"] = zip_path.stat().st_size
        manifest["zip_sha256"] = sha256(zip_path)

    return manifest


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/geb_integrated_preoutcome_package"),
    )
    p.add_argument(
        "--zip",
        type=Path,
        default=Path("outputs/GEB_INTEGRATED_PREOUTCOME_PACKAGE.zip"),
    )
    args = p.parse_args()
    manifest = build(args.output_dir, args.zip)
    print(
        "GEB_PREOUTCOME_PACKAGE "
        f"words={manifest['main_body_words']} "
        f"abstract={manifest['structured_abstract_words']} "
        f"figures={manifest['figure_count']} "
        f"zip_sha256={manifest.get('zip_sha256')}"
    )


if __name__ == "__main__":
    main()
