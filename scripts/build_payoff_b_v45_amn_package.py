#!/usr/bin/env python3
"""Build a deterministic anonymous American Naturalist V4.5 reviewer package.

The package contains:
- anonymous journal-facing manuscript source (Markdown);
- Supporting Information source;
- figure captions;
- three deterministic SVG main figures;
- a package manifest with SHA256 hashes.

Author metadata are intentionally excluded from the anonymous reviewer bundle.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import zipfile
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from render_payoff_b_v45_main_figures import render_all

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "PAYOFF_B_FORECAST_ACCESS_CORRECTION_V4_5_AMNAT.md"
SI = ROOT / "submission" / "AMNAT_V4_5_SUPPORTING_INFORMATION_20261006.md"
CAPTIONS = ROOT / "submission" / "AMNAT_V4_5_FIGURE_CAPTIONS_20261006.md"
FIGDATA = ROOT / "data" / "payoff_b_v45_figure_data_20261006.json"

FORBIDDEN = (
    "PAYOFF-B",
    "V2",
    "V3",
    "V4",
    "V5",
    "V8",
    "post-freeze",
    "rollback",
    "workflow ID",
    "artifact ID",
)

FIXED_ZIP_TIME = (2026, 10, 6, 0, 0, 0)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def word_count(text: str) -> int:
    cleaned = re.sub(r"[\[\]{}()*#]", " ", text)
    return len([x for x in re.split(r"\s+", cleaned.strip()) if x])


def extract_between(text: str, start: str, end: str) -> str:
    a = text.index(start) + len(start)
    b = text.index(end, a)
    return text[a:b].strip()


def validate_manuscript(text: str) -> dict:
    low = text.lower()
    forbidden = [x for x in FORBIDDEN if x.lower() in low]
    if forbidden:
        raise ValueError(f"internal labels in anonymous manuscript: {forbidden}")

    for required in (
        "## Abstract",
        "## 1. Introduction",
        "## 2. Theory",
        "## 3. Methods",
        "## 4. Natural evidence",
        "## 5. Discussion",
        "## 6. Conclusion",
        "## Literature Cited",
        "Figure 1",
        "Figure 2",
        "Figure 3",
    ):
        if required not in text:
            raise ValueError(f"missing required manuscript element: {required}")

    abstract = extract_between(text, "## Abstract", "Keywords:")
    main = text[: text.index("## Literature Cited")]
    aw = word_count(abstract)
    mw = word_count(main)
    if aw > 200:
        raise ValueError(f"abstract exceeds 200 words: {aw}")
    if mw > 7500:
        raise ValueError(f"main text exceeds 7500 words: {mw}")

    return {
        "abstract_words": aw,
        "main_text_words": mw,
        "title": text.splitlines()[0].lstrip("# ").strip(),
    }


def deterministic_zip(source_dir: Path, zip_path: Path) -> None:
    entries = sorted(p for p in source_dir.rglob("*") if p.is_file())
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in entries:
            rel = path.relative_to(source_dir).as_posix()
            info = zipfile.ZipInfo(rel, FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, path.read_bytes())


def build(output_dir: Path, zip_path: Path | None = None) -> dict:
    manuscript_text = MANUSCRIPT.read_text(encoding="utf-8")
    manuscript_stats = validate_manuscript(manuscript_text)

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    anon = output_dir / "anonymous_manuscript.md"
    supp = output_dir / "supporting_information.md"
    caps = output_dir / "figure_captions.md"

    anon.write_text(manuscript_text, encoding="utf-8")
    shutil.copyfile(SI, supp)
    shutil.copyfile(CAPTIONS, caps)

    rendered_dir = output_dir / "_rendered"
    rendered = render_all(rendered_dir)
    figure_dir = output_dir / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)

    generic_figures = {}
    for index, key in enumerate(("figure_1", "figure_2", "figure_3"), start=1):
        src = Path(rendered[key])
        txt = src.read_text(encoding="utf-8")
        bad = [x for x in FORBIDDEN if x.lower() in txt.lower()]
        if bad:
            raise ValueError(f"internal labels in {key}: {bad}")
        dst = figure_dir / f"figure{index}.svg"
        shutil.copyfile(src, dst)
        generic_figures[key] = dst

    shutil.rmtree(rendered_dir)

    for journal_file in (anon, supp, caps):
        txt = journal_file.read_text(encoding="utf-8")
        bad = [x for x in FORBIDDEN if x.lower() in txt.lower()]
        if bad:
            raise ValueError(f"internal labels in {journal_file.name}: {bad}")

    package_files = [
        anon,
        supp,
        caps,
        generic_figures["figure_1"],
        generic_figures["figure_2"],
        generic_figures["figure_3"],
    ]

    manifest = {
        "status": "anonymous_reviewer_package",
        "date": "2026-10-06",
        "target": "The American Naturalist",
        "article_type": "Major Article",
        "manuscript": manuscript_stats,
        "anonymous_reviewer_files": [
            "anonymous_manuscript.md",
            "supporting_information.md",
            "figure_captions.md",
            "figures/figure1.svg",
            "figures/figure2.svg",
            "figures/figure3.svg",
        ],
        "file_hashes": {
            path.relative_to(output_dir).as_posix(): sha256(path)
            for path in package_files
        },
    }
    mp = output_dir / "PACKAGE_MANIFEST.json"
    mp.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    if zip_path is None:
        zip_path = output_dir.parent / "payoff_b_v45_amn_reviewer_package.zip"
    deterministic_zip(output_dir, zip_path)

    return {
        "output_dir": output_dir,
        "zip": zip_path,
        "manifest": mp,
        "manuscript_stats": manuscript_stats,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/payoff_b_v45_amn_package"),
    )
    ap.add_argument(
        "--zip",
        type=Path,
        default=Path("outputs/payoff_b_v45_amn_reviewer_package.zip"),
    )
    args = ap.parse_args()
    result = build(args.output_dir, args.zip)
    print(result["manifest"])
    print(result["zip"])
    print(json.dumps(result["manuscript_stats"], sort_keys=True))


if __name__ == "__main__":
    main()
