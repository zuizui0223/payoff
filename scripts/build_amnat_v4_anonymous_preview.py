#!/usr/bin/env python3
"""Build an anonymized MARKDOWN+PNG editorial PREVIEW of AmNat Paper 2.

No scientific estimates are recalculated. The passed-in, independently
source-verified figures may include authentic observed spatial pairs and
species-target rows; no points are synthesized here. The output is NOT an
approved or deposited reviewer archive. A
separate workflow may typeset this preview with Pandoc + XeLaTeX.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SOURCE=Path("manuscript/PAYOFF_B_INFORMATION_CONTROL_V4_V8_INTEGRATED.md")
FIGURES=("figure1_summary.svg","figure2_summary.svg",
         "figure3_summary.svg","figure4_summary.svg")
TITLE="Environmental predictability alone does not determine seasonal tracking"

# One page per figure. Captions describe the scientific evidence units and
# MUST NOT recast genuine archived V8 observations as summary-only figures.
FIGURE_CAPTIONS=(
    "Serial timing and control architecture. Schematic theory and a "
    "conditional linear, innovation-free two-actor identity; neither "
    "animal belief nor fitness is observed.",
    "Early versus late signed green-up correlations for 166 distinct "
    "original source-target environmental spatial pairs used by 28 bird "
    "species. These are environmental relationships, not tracked animals.",
    "Original 150 bird species-target mismatch observations associated "
    "with 72 distinct environmental spatial pairs (22 species), with "
    "the fixed-arrival structural-null comparison. The 150 rows are "
    "not 150 independent environmental relationships.",
    "Original published-source descriptive mule-deer summaries from "
    "152 animal-years (72 individuals). No fabricated individual "
    "trajectories, direct cue estimates, or demographic fitness effects.",
)


def figure_appendix(images:list[str])->str:
    if len(images)!=4 or len(FIGURE_CAPTIONS)!=4:
        raise ValueError("Exactly four source-bounded figure inputs required")
    text="\\clearpage\n\n## Figures (source-verified editorial previews)\n\n"
    for i,(image,caption) in enumerate(zip(images,FIGURE_CAPTIONS),1):
        if i>1:
            text+="\\clearpage\n\n"
        name=Path(image).name
        # Non-floating LaTeX image makes it impossible to leave an orphaned
        # heading on the preceding page or pack two unreadably small
        # science figures on one page.
        text+=f"\\begin{{center}}\n\\includegraphics[width=0.94\\textwidth]{{{name}}}\n\\end{{center}}\n\n"
        text+=f"**Figure {i}.** {caption}\n\n"
    text+=("Figures 2 and 3 plot the original, source-verified environmental "
           "pair and bird species-target observations; Figures 1 and 4 "
           "are respectively conceptual and descriptive summaries. "
           "The panels do not establish individual information use, "
           "behavioural causality, or fitness effects.\n")
    return text



def anonymize(source:str)->str:
    if not source.startswith("# "+TITLE+"\n"):
        raise ValueError("Unexpected agreed manuscript title")
    if "## Literature Cited" not in source:
        raise ValueError("Literature Cited must be source-checked before preview")
    if "## Post-freeze transparency statement" not in source:
        raise ValueError("Original post-freeze provenance block missing")
    before_admin=source.split("## Post-freeze transparency statement",1)[0]
    # Administrative provenance has no place in a double-anonymous manuscript.
    start=before_admin.find("## Abstract")
    if start<0:
        raise ValueError("Abstract missing")
    s="# "+TITLE+"\n\n"+before_admin[start:]
    replacements=[
        ("The existing PAYOFF-B closed-loop model","An earlier reduced closed-loop model"),
        ("PAYOFF-B does not","We do not"),
        ("PAYOFF-B therefore","We therefore"),
        ("PAYOFF-B consequently","We consequently"),
        ("PAYOFF-B","this study"),
        ("The V8 environmental analysis","The prospectively specified environmental analysis"),
        ("the V8 environmental analysis","the prospectively specified environmental analysis"),
        ("The current V8 evidence","The current bird-data evidence"),
        ("the V8 correlations","the range-based correlation measurements"),
        ("V8 correlations","range-based correlation measurements"),
        ("the V8 stress test","the broad-bird stress test"),
        ("the V8 integration","the environmental analysis"),
        ("V8 rejects","The registered analysis rejects"),
        ("V8","the bird-data test"),
        ("V3 does not infer","The reduced model does not infer"),
        ("V3","earlier theoretical analysis"),
        ("V4","the integrated model"),
        ("H2 readiness-gated","the readiness-gated"),
        ("H2","the readiness-gating hypothesis"),
        ("post-freeze","subsequent, exploratory"),
    ]
    for old,new in replacements:
        s=s.replace(old,new)
    s=s.strip()+"\n"
    forbidden=[
        "PAYOFF-B","V8","V7R","V3","V4","rollback",
        "zuizui0223","github.com/zuizui",
        "## Post-freeze transparency statement",
    ]
    if any(x in s for x in forbidden):
        raise ValueError("Unresolved internal or identifying token in manuscript")
    if not ("## Literature Cited" in s and "+0.369" in s and
            "+0.062" in s and "152 animal-years" in s):
        raise ValueError("Major numeric claims or bibliography were lost")
    if s.count(r"\[")!=before_admin[start:].count(r"\["):
        raise ValueError("Display math delimiters changed")
    # Bracket math has to remain unaltered; Pandoc must render it as TeX.
    return s


def build_preview(source:str, out:Path, figures_dir:Path|None=None)->dict:
    s=anonymize(source)
    fig_entries=[]
    if figures_dir is not None:
        try:
            import cairosvg
        except ImportError as exc:
            raise RuntimeError("Install CairoSVG to include image previews") from exc
        for i,name in enumerate(FIGURES,1):
            path=figures_dir/name
            if not path.is_file():
                raise FileNotFoundError(path)
            target=out.parent/f"figure{i}_preview.png"
            target.parent.mkdir(parents=True,exist_ok=True)
            cairosvg.svg2png(url=str(path),write_to=str(target),scale=2)
            fig_entries.append(str(target))
        s+='\n'+figure_appendix(fig_entries)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(s,encoding="utf-8")
    return {
        "status":"ANONYMOUS_MARKDOWN_EDITORIAL_PREVIEW_SUBMISSION_HOLD",
        "admin_provenance_stripped":True,
        "scientific_data_modified":False,
        "math_display_count":s.count(r"\["),
        "figure_count":len(fig_entries),
        "figure_images":fig_entries,
        "full_underlying_data_included":False,
        "approved_for_journal_submission":False,
        "important_limitations":[
            "All references need final journal style verification",
            "PDF output needs page-by-page visual inspection",
            "A PDF by itself is not an anonymous data/code reviewer archive",
            "Bibliographic and manuscript science still require human author approval",
        ],
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,default=SOURCE)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--figures-dir",type=Path,default=None)
    p.add_argument("--receipt",type=Path,required=True)
    a=p.parse_args()
    receipt=build_preview(a.source.read_text(encoding="utf-8"),
                          a.out,a.figures_dir)
    a.receipt.parent.mkdir(parents=True,exist_ok=True)
    a.receipt.write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":receipt["status"],"figures":receipt["figure_count"],
                      "submission_ready":False}))


if __name__=="__main__":
    main()
