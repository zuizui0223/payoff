#!/usr/bin/env python3
"""Render GEB-formatted copies of the frozen integrated six-figure set."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from render_integrated_tracking_figures import render_all as render_canonical

PANEL_REPLACEMENTS = {
    ">A  ": ">(a) ",
    ">B  ": ">(b) ",
    ">C  ": ">(c) ",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def convert_panel_labels(svg: str) -> str:
    for old, new in PANEL_REPLACEMENTS.items():
        svg = svg.replace(old, new)
    return svg


def render_all(output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    source_dir = output_dir / "_canonical"
    canonical = render_canonical(source_dir)

    figures = {}
    figure_paths = {}
    for i in range(1, 7):
        source = Path(canonical[f"figure_{i}"])
        target = output_dir / source.name.replace(
            "PAYOFF_B_INTEGRATED_", "GEB_PAYOFF_B_INTEGRATED_"
        )
        converted = convert_panel_labels(source.read_text(encoding="utf-8"))
        target.write_text(converted, encoding="utf-8")
        figure_paths[f"figure_{i}"] = target
        figures[f"figure_{i}"] = {
            "path": target.name,
            "sha256": sha256(target),
            "canonical_source_sha256": sha256(source),
            "format_change_only": True,
        }

    for p in source_dir.iterdir():
        if p.is_file():
            p.unlink()
    source_dir.rmdir()

    manifest = {
        "status": "geb_integrated_six_figure_format_overlay",
        "scientific_result_changed": False,
        "panel_label_rule": "lower-case parenthetical labels",
        "figures": figures,
    }
    mp = output_dir / "GEB_INTEGRATED_FIGURE_MANIFEST.json"
    mp.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return {"manifest": mp, **figure_paths}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/geb_integrated_figures"),
    )
    args = p.parse_args()
    render_all(args.output_dir)
    print(args.output_dir / "GEB_INTEGRATED_FIGURE_MANIFEST.json")


if __name__ == "__main__":
    main()
