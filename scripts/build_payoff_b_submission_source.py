from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCIENCE = ROOT / "manuscript" / "PAYOFF_B_THEORETICAL_ECOLOGY_BRIEF_V1.md"
TITLE_PAGE = ROOT / "submission" / "PAYOFF_B_TITLE_PAGE_TEMPLATE.md"
DECLARATIONS = ROOT / "submission" / "PAYOFF_B_DECLARATIONS_TEMPLATE.md"
DEFAULT_OUT = ROOT / "submission" / "theoretical_ecology" / "generated" / "MANUSCRIPT_SUBMISSION_SOURCE.md"

INTERNAL_TARGET_LINE = "**Target:** *Theoretical Ecology* — Brief Communication"
ABSTRACT_OLD = (
    "The result sharpens existing dispersal-induced-growth theory from existence of "
    "beneficial intermediate migration to a unique, dimensionless connectivity prediction."
)
ABSTRACT_NEW = (
    "The result sharpens existing dispersal-induced-growth theory from existence of "
    "beneficial intermediate migration to a unique, dimensionless connectivity prediction "
    "tied directly to the environmental switching timescale."
)


def _title_page_fields() -> str:
    text = TITLE_PAGE.read_text(encoding="utf-8")
    marker = "**Authors:**"
    if marker not in text:
        raise ValueError("title-page template is missing the Authors field")
    fields = marker + text.split(marker, 1)[1]
    # The explanatory footer is useful in the template but should not appear in the manuscript.
    fields = fields.split("The title-page metadata must match", 1)[0].rstrip()
    return fields


def build_submission_source() -> str:
    text = SCIENCE.read_text(encoding="utf-8")

    if INTERNAL_TARGET_LINE not in text:
        raise ValueError("internal target line drifted; update submission overlay deliberately")
    text = text.replace(f"\n{INTERNAL_TARGET_LINE}\n", "\n", 1)

    if ABSTRACT_OLD not in text:
        raise ValueError("abstract endpoint sentence drifted; update submission overlay deliberately")
    text = text.replace(ABSTRACT_OLD, ABSTRACT_NEW, 1)

    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        raise ValueError("science source no longer starts with the manuscript title")
    title = lines[0]
    body = "\n".join(lines[1:]).lstrip("\n")
    text = f"{title}\n\n{_title_page_fields()}\n\n{body}".rstrip()

    declarations = DECLARATIONS.read_text(encoding="utf-8").strip()
    if "## Statements and Declarations" not in declarations:
        raise ValueError("declarations template is missing the required heading")
    text += "\n\n" + declarations + "\n"
    return text


def main(out_path: str | None = None) -> None:
    out = Path(out_path) if out_path else DEFAULT_OUT
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_submission_source(), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    import sys

    main(sys.argv[1] if len(sys.argv) > 1 else None)
