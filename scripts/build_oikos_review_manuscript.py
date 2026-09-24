#!/usr/bin/env python3
"""Build an anonymous, line-numbered Oikos review manuscript as RTF."""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "PAYOFF_B_TRACKING_THEORY_V1.md"
CAPTIONS = ROOT / "submission" / "PAYOFF_B_TRACKING_FIGURE_CAPTIONS.md"
AI_STATEMENT = ROOT / "submission" / "OIKOS_AI_USE_STATEMENT.md"
BS = chr(92)
NL = chr(10)


def rtf_escape(text: str) -> str:
    out = []
    for char in text:
        if char == BS:
            out.append(BS + BS)
        elif char == "{":
            out.append(BS + "{")
        elif char == "}":
            out.append(BS + "}")
        else:
            code = ord(char)
            if 32 <= code <= 126:
                out.append(char)
            elif char == chr(9):
                out.append(BS + "tab ")
            else:
                signed = code if code <= 32767 else code - 65536
                out.append(f"{BS}u{signed}?")
    return "".join(out)


def strip_inline_markdown(text: str) -> str:
    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace(chr(96), "")
    text = text.replace("*", "")
    return text.strip()


def paragraph(
    text: str,
    *,
    bold: bool = False,
    size: int = 24,
    font: int = 0,
    align: str = "ql",
    before: int = 0,
    after: int = 120,
) -> str:
    controls = (
        BS + "pard"
        + BS + align
        + BS + "sl480"
        + BS + "slmult1"
        + BS + f"sb{before}"
        + BS + f"sa{after}"
        + BS + f"f{font}"
        + BS + f"fs{size}"
    )
    if bold:
        controls += BS + "b"
    body = rtf_escape(strip_inline_markdown(text))
    if bold:
        body += BS + "b0"
    return controls + " " + body + BS + "par" + NL


def render_markdown(lines: list[str]) -> str:
    output = []
    buffer = []
    in_code = False

    def flush() -> None:
        nonlocal buffer
        if buffer:
            output.append(paragraph(" ".join(x.strip() for x in buffer)))
            buffer = []

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()

        if stripped.startswith(chr(96) * 3):
            flush()
            in_code = not in_code
            continue

        if in_code:
            if stripped:
                output.append(paragraph(stripped, size=20, font=1, after=40))
            continue

        if not stripped:
            flush()
            continue

        if stripped == "---":
            flush()
            continue

        if stripped.startswith("### "):
            flush()
            output.append(
                paragraph(stripped[4:], bold=True, size=24, before=200, after=80)
            )
            continue

        if stripped.startswith("## "):
            flush()
            output.append(
                paragraph(stripped[3:], bold=True, size=28, before=260, after=100)
            )
            continue

        if stripped.startswith("# "):
            flush()
            output.append(
                paragraph(stripped[2:], bold=True, size=30, before=260, after=100)
            )
            continue

        if stripped.startswith("|"):
            flush()
            output.append(paragraph(stripped, size=19, font=1, after=20))
            continue

        if stripped.startswith("- "):
            flush()
            output.append(paragraph(chr(8226) + " " + stripped[2:], after=50))
            continue

        if len(stripped) > 2 and stripped[0].isdigit() and stripped[1] == ".":
            flush()
            output.append(paragraph(stripped, after=50))
            continue

        if raw.startswith("    "):
            flush()
            output.append(paragraph(stripped, size=20, font=1, after=40))
            continue

        buffer.append(stripped)

    flush()
    return "".join(output)


def extract_parts() -> tuple[str, str, str, list[str]]:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = next(line[2:] for line in lines if line.startswith("# "))

    abstract_start = lines.index("## Abstract") + 1
    keyword_index = next(
        i for i, line in enumerate(lines)
        if line.startswith("**Keywords:**")
    )
    abstract = " ".join(
        line.strip()
        for line in lines[abstract_start:keyword_index]
        if line.strip()
    )
    keywords = strip_inline_markdown(lines[keyword_index])

    body_start = lines.index("## 1. Introduction")
    body_end = lines.index("## Prior-art boundary and core references")
    body_lines = lines[body_start:body_end]

    reference_marker = lines.index("The compact manuscript list is:") + 1
    reference_end = next(
        i for i in range(reference_marker, len(lines))
        if lines[i].strip() == "---"
    )
    reference_lines = ["## References", ""] + lines[
        reference_marker:reference_end
    ]

    ai_lines = AI_STATEMENT.read_text(encoding="utf-8").splitlines()
    if ai_lines and ai_lines[0].startswith("# "):
        ai_lines[0] = "## " + ai_lines[0][2:]

    caption_lines = CAPTIONS.read_text(encoding="utf-8").splitlines()
    caption_start = next(
        i for i, line in enumerate(caption_lines)
        if line.startswith("## Figure 1.")
    )
    figure_lines = ["## Figure legends", ""] + caption_lines[caption_start:]

    review_lines = (
        body_lines
        + [""]
        + reference_lines
        + [""]
        + ai_lines
        + [""]
        + figure_lines
    )
    return title, abstract, keywords, review_lines


def build_review_rtf() -> str:
    title, abstract, keywords, review_lines = extract_parts()

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
        + BS + "widowctrl" + BS + "linemod1"
        + BS + "linex360" + BS + "linecont" + NL
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

    return "".join([
        header,
        paragraph(title, bold=True, size=30, align="qc", after=240),
        paragraph("Abstract", bold=True, size=26, after=100),
        paragraph(abstract, size=24, after=180),
        paragraph(keywords, size=22, after=120),
        BS + "page" + NL,
        render_markdown(review_lines),
        "}" + NL,
    ])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/OIKOS_TRACKING_ANON_MAIN_TEXT.rtf"),
    )
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    content = build_review_rtf()
    args.output.write_text(content, encoding="ascii")
    print(args.output)
    print(f"oikos_review_rtf bytes={len(content.encode('ascii'))}")


if __name__ == "__main__":
    main()
