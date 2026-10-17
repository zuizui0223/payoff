#!/usr/bin/env python3
"""Build an anonymized MARKDOWN+PNG editorial PREVIEW of AmNat Paper 2.

No scientific estimates are recalculated, no raw individual/pair observations
are embedded, and output is NOT a submission-ready reviewer archive. A
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
    figure_source_types=[]
    if figures_dir is not None:
        try:
            import cairosvg
        except ImportError as exc:
            raise RuntimeError("Install CairoSVG to include image previews") from exc

        # Captions must identify the actual level of source evidence. The
        # prior PDF mislabeled real 166/150 observation scatters as summary
        # panels. This is an evidence-labeling error, not just styling.
        captions={
            1: "Conceptual timer-controller architecture and the exact"
               " centered, deterministic two-actor mismatch identity."
               " No animal cognition, developmental gate or fitness"
               " effect is measured by this schematic.",
            4: "Mule-deer phase contraction reproduced from the published"
               " source: 152 animal-years, 72 deer. Start/end means and"
               " variance ratios are summaries, not individual paths"
               " or causal fitness effects.",
        }
        original_caps={
            2: "The 166 original, distinct geographic source-target"
               " green-up pairs, showing earlier versus later"
               " detrended correlation. The points are environmental"
               " pairs, not tracked individual migration routes.",
            3: "The 150 original bird species-target observations"
               " sharing 72 environmental pairs across 22 species."
               " The dashed fixed-arrival structural comparator can"
               " produce a positive association without bird"
               " timing adjustment. Points are not independent pairs.",
        }
        summary_caps={
            2: "Frozen summary estimates of the change in"
               " source-target environmental green-up correlations,"
               " with pair-bootstrap intervals. Individual pairs"
               " are not plotted in this summary version.",
            3: "Frozen correlation-to-bird-mismatch transfer, fixed-arrival"
               " structural null and observed-minus-null estimates"
               " with confidence intervals. Individual species-target"
               " observations are not plotted in this summary version.",
        }
        for i,name in enumerate(FIGURES,1):
            path=figures_dir/name
            if not path.is_file():
                raise FileNotFoundError(path)
            svg=path.read_text(encoding="utf-8")
            if i in (2,3):
                token=('class="observed-spatial-pair"' if i==2
                       else 'class="observed-species-target"')
                expected=(166 if i==2 else 150)
                count=svg.count(token)
                if count not in (0,expected):
                    raise ValueError(
                        f"Partial/inaccurate Figure {i} original-row plot count: {count}"
                    )
                source_type="observed_rows" if count==expected else "summary_only"
            else:
                source_type="schematic" if i==1 else "source_summary"
            target=out.parent/f"figure{i}_preview.png"
            target.parent.mkdir(parents=True,exist_ok=True)
            cairosvg.svg2png(url=str(path),write_to=str(target),scale=2)
            fig_entries.append(str(target))
            figure_source_types.append(source_type)

        s+="\n\\clearpage\n\n## Source-grounded main figures\n\n"
        for i,image_file in enumerate(fig_entries,1):
            if i>1:
                # Flush the preceding LaTeX figure float BEFORE authoring the
                # next block. This prevents detached headings / captions on
                # the previous page (confirmed in the original PDF).
                s+="\n\\clearpage\n\n"
            caption=(captions[i] if i in captions else
                     original_caps[i] if figure_source_types[i-1]=="observed_rows"
                     else summary_caps[i])
            filename=Path(image_file).name
            s+=f"![{caption}]({filename})\n\n"
        # No generic disclaimer that all figures are summary estimates:
        # Figures 2 and 3 can be actual archived observed rows.
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(s,encoding="utf-8")
    return {
        "status":"ANONYMOUS_MARKDOWN_EDITORIAL_PREVIEW_SUBMISSION_HOLD",
        "admin_provenance_stripped":True,
        "scientific_data_modified":False,
        "math_display_count":s.count(r"\["),
        "figure_count":len(fig_entries),
        "figure_images":fig_entries,
        "figure_source_types":figure_source_types,
        "figure2_real_pair_points":166 if figure_source_types and figure_source_types[1]=="observed_rows" else 0,
        "figure3_real_species_target_points":150 if figure_source_types and figure_source_types[2]=="observed_rows" else 0,
        "full_underlying_data_included":False,
        "approved_for_journal_submission":False,
        "important_limitations":[
            "All references need final journal style verification",
            "PDF output needs page-by-page visual inspection",
            "Source-backed data/code archive exists internally; anonymous external reviewer deposit unverified",
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
