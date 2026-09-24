#!/usr/bin/env python3
"""Render frozen PAYOFF-B Supporting Information as Oikos-ready RTF."""

from __future__ import annotations

import argparse
from pathlib import Path

from build_oikos_review_manuscript import BS, NL, render_markdown
from build_tracking_theory_supporting_information import build_supporting_information


def build_supporting_rtf() -> str:
    header = (
        "{"
        + BS + "rtf1" + BS + "ansi" + BS + "ansicpg1252" + BS + "deff0" + NL
        + "{"
        + BS + "fonttbl"
        + "{"
        + BS + "f0 Arial;}"
        + "{"
        + BS + "f1 Courier New;}"
        + "}"
        + NL
        + BS + "paperw12240" + BS + "paperh15840"
        + BS + "margl1440" + BS + "margr1440"
        + BS + "margt1440" + BS + "margb1440"
        + BS + "widowctrl"
        + NL
        + "{"
        + BS + "footer"
        + BS + "pard" + BS + "qr" + BS + "f0" + BS + "fs18 Page "
        + "{"
        + BS + "field"
        + "{"
        + BS + "*"
        + BS + "fldinst PAGE}"
        + "{"
        + BS + "fldrslt 1}}"
        + BS + "par}"
        + NL
    )
    body = render_markdown(build_supporting_information().splitlines())
    return header + body + "}" + NL


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/OIKOS_TRACKING_SUPPORTING_INFORMATION.rtf"),
    )
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    content = build_supporting_rtf()
    args.output.write_text(content, encoding="ascii")
    print(args.output)
    print(f"oikos_supporting_rtf bytes={len(content.encode('ascii'))}")


if __name__ == "__main__":
    main()
