from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from build_payoff_b_v2_geb_outcome_package import outcome_cover_letter
from build_payoff_b_v2_geb_outcome_supporting_information import (
    build_supporting_information,
)
from build_payoff_b_v2_geb_source import FIGURE_LEGENDS, build_source


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULT = (
    ROOT / "data" / "aikens2022_access_blocked_submission_state_20260928.json"
)
TITLE_PAGE = ROOT / "submission" / "GEB_V2_TITLE_PAGE_ACCESS_BLOCKED_TEMPLATE.md"
DECLARATIONS = ROOT / "submission" / "GEB_V2_DECLARATIONS_TEMPLATE.md"

FIGURE_FILES = {
    1: "PAYOFF_B_INFO_V2_FIG1_DECISION_DEADLINE.png",
    2: "PAYOFF_B_INFO_V2_FIG2_DESYNCHRONIZATION.png",
    3: "PAYOFF_B_INFO_V2_FIG3_NETWORK_MEMORY.png",
    4: "PAYOFF_B_INFO_V2_FIG4_BROAD_CONNECTIVITY.png",
    5: "PAYOFF_B_INFO_V2_FIG5_INFORMATION_AXES.png",
    6: "PAYOFF_B_INFO_V2_FIG6_CAPACITY.png",
    7: "PAYOFF_B_INFO_V2_FIG7_RESCUE.png",
}

INTERNAL_EDITOR_TOKENS = (
    "PAYOFF-B",
    "PREOUTCOME",
    "V2 cover-letter template",
    "V2 title-page template",
    "ACCESS_BLOCKED package state",
    "WORKING TEMPLATE",
)


def normalize_display_math(text: str) -> str:
    """Convert legacy bracket-only display math markers to Pandoc TeX math."""

    out = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "[":
            prefix = line[: len(line) - len(line.lstrip())]
            out.append(prefix + r"\[")
        elif stripped == "]":
            prefix = line[: len(line) - len(line.lstrip())]
            out.append(prefix + r"\]")
        else:
            out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def _figure_entries() -> list[tuple[int, str]]:
    body = FIGURE_LEGENDS.split("## Figure legends", 1)[-1].strip()
    chunks = re.split(r"(?=\*\*Figure\s+\d+\.)", body)
    entries: list[tuple[int, str]] = []
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        match = re.match(r"\*\*Figure\s+(\d+)\.", chunk)
        if match is None:
            raise ValueError(f"could not parse figure legend block: {chunk[:80]}")
        number = int(match.group(1))
        entries.append((number, chunk))
    if [n for n, _ in entries] != list(range(1, 8)):
        raise ValueError("expected exactly Figure 1 through Figure 7 legends")
    return entries


def build_main_portal_source() -> str:
    text = build_source()
    if "## Figure legends" not in text:
        raise ValueError("GEB source is missing Figure legends")
    body = text.split("## Figure legends", 1)[0].rstrip()
    figure_blocks = ["## Figure legends"]
    for number, legend in _figure_entries():
        filename = FIGURE_FILES[number]
        figure_blocks.extend(
            [
                "",
                legend,
                "",
                f"![Figure {number}](figures_png/{filename}){{width=6.2in}}",
            ]
        )
    text = body + "\n\n" + "\n".join(figure_blocks).rstrip() + "\n"
    return normalize_display_math(text)


def _title_identity_block() -> str:
    text = TITLE_PAGE.read_text(encoding="utf-8")
    if "## Acknowledgements" not in text:
        raise ValueError("title page no longer contains Acknowledgements boundary")
    block = text.split("## Acknowledgements", 1)[0].strip()
    lines = block.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    return "\n".join(lines).strip()


def _declaration_block() -> str:
    text = DECLARATIONS.read_text(encoding="utf-8")
    lines = text.splitlines()
    while lines and (not lines[0].strip() or lines[0].startswith("# ")):
        lines.pop(0)
    if lines and lines[0].startswith("**Article:**"):
        lines.pop(0)
    return "\n".join(lines).strip()


def build_title_page_source() -> str:
    return (
        "# Global Ecology and Biogeography - Title page\n\n"
        + _title_identity_block()
        + "\n\n"
        + _declaration_block()
        + "\n"
    )


def build_supporting_information_source(result_json: Path) -> str:
    text, _ = build_supporting_information(result_json)
    return normalize_display_math(text)


def build_cover_letter_source(result_json: Path) -> str:
    return outcome_cover_letter(result_json)


def audit_portal_sources(
    *,
    main: str,
    title_page: str,
    cover_letter: str,
    supporting_information: str,
) -> dict:
    bare_math_open = sum(1 for line in main.splitlines() if line.strip() == "[")
    bare_math_close = sum(1 for line in main.splitlines() if line.strip() == "]")
    embedded_figures = len(
        re.findall(r"!\[Figure\s+\d+\]\(figures_png/[^)]+\.png\)", main)
    )
    internal_hits = {
        name: [token for token in INTERNAL_EDITOR_TOKENS if token in text]
        for name, text in {
            "main": main,
            "title_page": title_page,
            "cover_letter": cover_letter,
        }.items()
    }
    return {
        "bare_display_math_markers": bare_math_open + bare_math_close,
        "embedded_figure_links": embedded_figures,
        "internal_editor_token_hits": internal_hits,
        "main_has_final_title": main.startswith(
            "# Information deadlines can desynchronize seasonal interactions "
            "under environmental change"
        ),
        "title_page_has_placeholders": (
            "[AUTHOR LIST" in title_page
            and "[AFFILIATIONS" in title_page
            and "[AUTHOR CONTROLLED]" in title_page
        ),
        "cover_letter_has_final_title": (
            "Information deadlines can desynchronize seasonal interactions"
            in cover_letter
        ),
        "supporting_information_is_outcome_rendered": (
            "PREOUTCOME" not in supporting_information
            and "remains unopened" not in supporting_information
        ),
    }


def build(output_dir: Path, result_json: Path = DEFAULT_RESULT) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    main = build_main_portal_source()
    title = build_title_page_source()
    cover = build_cover_letter_source(result_json)
    si = build_supporting_information_source(result_json)

    paths = {
        "main": output_dir / "GEB_MAIN_REVIEW_SOURCE.md",
        "title_page": output_dir / "GEB_TITLE_PAGE_SOURCE.md",
        "cover_letter": output_dir / "GEB_COVER_LETTER_SOURCE.md",
        "supporting_information": output_dir / "GEB_SUPPORTING_INFORMATION_SOURCE.md",
    }
    for key, text in {
        "main": main,
        "title_page": title,
        "cover_letter": cover,
        "supporting_information": si,
    }.items():
        paths[key].write_text(text, encoding="utf-8")

    audit = audit_portal_sources(
        main=main,
        title_page=title,
        cover_letter=cover,
        supporting_information=si,
    )
    audit_path = output_dir / "GEB_PORTAL_SOURCE_AUDIT.json"
    audit_path.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")

    if audit["bare_display_math_markers"] != 0:
        raise ValueError("bare display-math bracket markers remain")
    if audit["embedded_figure_links"] != 7:
        raise ValueError("expected seven embedded figure links")
    if any(audit["internal_editor_token_hits"].values()):
        raise ValueError(
            "internal editor-facing tokens remain: "
            + json.dumps(audit["internal_editor_token_hits"], sort_keys=True)
        )
    if not audit["main_has_final_title"]:
        raise ValueError("portal main source title drifted")
    if not audit["cover_letter_has_final_title"]:
        raise ValueError("cover-letter title drifted")
    if not audit["supporting_information_is_outcome_rendered"]:
        raise ValueError("supporting information is not outcome-rendered")

    return {
        "paths": {key: str(value) for key, value in paths.items()},
        "audit": audit,
        "audit_path": str(audit_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("submission/geb_v2/generated"),
    )
    parser.add_argument("--result-json", type=Path, default=DEFAULT_RESULT)
    args = parser.parse_args()
    result = build(args.output_dir, args.result_json)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
