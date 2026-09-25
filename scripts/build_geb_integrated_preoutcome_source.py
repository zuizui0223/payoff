#!/usr/bin/env python3
"""Build a GEB-facing blinded source from the frozen integrated manuscript."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "manuscript" / "PAYOFF_B_INTEGRATED_TRACKING_ECOLOGY_V1_PREOUTCOME.md"
DATA_TEMPLATE = ROOT / "submission" / "GEB_INTEGRATED_DATA_CODE_TEMPLATE.md"
CAPTIONS = ROOT / "submission" / "GEB_INTEGRATED_FIGURE_CAPTIONS_PREOUTCOME.md"

RUNNING_TITLE = "Temporal buffering and spatial tracking"
KEYWORDS = [
    "behavioral plasticity",
    "climate change",
    "environmental tracking",
    "habitat fragmentation",
    "migration",
    "movement ecology",
    "phase retention",
    "phenological mismatch",
]

ABSTRACT_START = "<!-- AIKENS_LAMBDA_ABSTRACT_START -->"
ABSTRACT_END = "<!-- AIKENS_LAMBDA_ABSTRACT_END -->"


def between(text: str, start: str, end: str) -> str:
    i = text.index(start) + len(start)
    j = text.index(end, i)
    return text[i:j].strip()


def strip_rule(text: str) -> str:
    return re.sub(r"\n?---\s*$", "", text.rstrip()).rstrip()


def structured_abstract(aikens_abstract_block: str) -> str:
    return f"""## Abstract

**Aim:** Test whether seasonal timing can replace spatial tracking under sustained
environmental change or instead acts as a finite buffer that postpones movement,
and ask whether natural migration collapses onto one portable
animal-speed/environmental-wave-speed optimum.

**Location:** Synthetic landscapes; eastern North America for the broad
55-species bird analysis; and published North American and northern
European–Arctic migration systems for direct phase-control reconstruction.

**Time period:** Broad bird analysis, 2002–2017; direct systems use the archived
periods of their source studies; synthetic analyses have no calendar period.

**Major taxa studied:** Fifty-five migratory bird species, mule deer
(*Odocoileus hemionus*), barnacle goose (*Branta leucopsis*) and Eurasian
wigeon (*Mareca penelope*).

**Methods:** We combined an exact local movement–timing feedback null, explicit
moving-landscape simulations, a registered macroecological reanalysis, and
scale-declared phase-retention reconstructions with independent environmental
reliability checks.

**Results:** Movement and timing can generate identical local mismatch dynamics,
but explicit landscapes show that finite timing acts as a temporary bypass:
phenological capacity expands persistence and reduces route costs before movement
re-enters under stronger directional forcing. Across 5,816 bird observations,
one universal natural speed optimum was not supported. Direct systems
transformed incoming phase error through different actuator architectures and
ecological intervals.
{ABSTRACT_START}
{aikens_abstract_block}
{ABSTRACT_END}

**Main conclusions:** Temporal adjustment buffers rather than permanently
replaces spatial tracking under sustained environmental change. Low mismatch can
therefore conceal latent spatial tracking demand until temporal capacity is
exhausted. Mismatch is consequently an outcome of the tracking system, not a
direct measure of its mechanism or remaining resilience.

**Keywords:** {", ".join(KEYWORDS)}
"""


def extract_caption_body() -> str:
    text = CAPTIONS.read_text(encoding="utf-8")
    lines = [
        line for line in text.splitlines()
        if not line.startswith("# ")
        and not line.startswith("These legends are journal-facing")
        and not line.startswith("the canonical six-figure")
        and not line.startswith("Numerical content")
    ]
    return "\n".join(lines).strip()


def geb_data_statement() -> str:
    text = DATA_TEMPLATE.read_text(encoding="utf-8")
    review = between(
        text,
        "## Blinded review statement",
        "## Publication archive",
    )
    boundary = text.split("## PREOUTCOME boundary", 1)[1].strip()
    return (
        "## Data and Code Availability Statement\n\n"
        + review.strip()
        + "\n\n"
        + "**PREOUTCOME boundary:** "
        + boundary.replace("\n", " ").strip()
    )


def build_source(source_path: Path = DEFAULT_SOURCE) -> str:
    source = source_path.read_text(encoding="utf-8")
    title = source.splitlines()[0].removeprefix("# ").strip()

    abstract_block = between(source, ABSTRACT_START, ABSTRACT_END)

    body_start = source.index("## 1. Introduction")
    prior_start = source.index("## Prior-art boundary")
    refs_start = source.index("## References")
    figure_start = source.index("## Figure architecture")

    body = strip_rule(source[body_start:prior_start])
    prior = strip_rule(
        source[prior_start + len("## Prior-art boundary"):refs_start]
    ).strip()
    references = strip_rule(source[refs_start:figure_start]).strip()

    limitation = "### 5.7 Limitations"
    if limitation not in body:
        raise ValueError("canonical integrated manuscript is missing 5.7 Limitations")
    body = body.replace(
        limitation,
        "### 5.7 Relationship to existing literature\n\n"
        + prior
        + "\n\n### 5.8 Limitations",
        1,
    )

    figures = extract_caption_body()

    return (
        f"# {title}\n\n"
        f"**Running title:** {RUNNING_TITLE}\n\n"
        + structured_abstract(abstract_block)
        + "\n---\n\n"
        + body.strip()
        + "\n\n---\n\n"
        + references
        + "\n\n---\n\n"
        + geb_data_statement()
        + "\n\n---\n\n"
        + "## Figure legends\n\n"
        + figures
        + "\n"
    )


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/GEB_INTEGRATED_BLINDED_PREOUTCOME.md"),
    )
    args = p.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    content = build_source(args.source)
    args.output.write_text(content, encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
