#!/usr/bin/env python3
"""Build the complete six-figure PAYOFF-B integrated tracking set."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from render_tracking_theory_figures import render_all as render_synthetic
from render_integrated_tracking_empirical_figures import (
    render_all as render_empirical,
    esc,
    line,
    rect,
    text,
)

ROOT = Path(__file__).resolve().parents[1]


def arrow(x1, y1, x2, y2):
    body = line(x1, y1, x2, y2, 2)
    if abs(x2-x1) >= abs(y2-y1):
        head = f'<polygon points="{x2},{y2} {x2-12},{y2-7} {x2-12},{y2+7}" fill="black"/>'
    else:
        head = f'<polygon points="{x2},{y2} {x2-7},{y2-12} {x2+7},{y2-12}" fill="black"/>'
    return body + head


def box(x, y, w, h, title, lines):
    out=[rect(x,y,w,h,fill="#fafafa",width=1.5),text(x+14,y+28,title,15,"700")]
    for i,s in enumerate(lines):
        out.append(text(x+14,y+54+i*21,s,12))
    return "".join(out)


def render_integrated_concept(path: Path) -> None:
    w,h=1200,720
    out=[
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="white"/>',
        text(36,40,"Figure 1. Temporal buffering and latent spatial tracking demand",22,"700"),
        text(36,68,"Timing can absorb tracking demand temporarily, but finite capacity causes spatial response to re-enter under sustained forcing.",13),
    ]
    out.append(box(55,110,280,125,"1  PAYOFF-B1 benchmark",[
        "Exact anti-phase two-patch model:",
        "one positive migration optimum",
        "on the environmental switching timescale."
    ]))
    out.append(arrow(335,172,425,172))
    out.append(box(425,110,310,125,"2  Local identifiability null",[
        "movement feedback + timing feedback",
        "enter through one restoring gain K;",
        "same mismatch can hide different allocations."
    ]))
    out.append(arrow(735,172,825,172))
    out.append(box(825,95,315,155,"3  Finite temporal buffer",[
        "timing postpones movement",
        "capacity is finite",
        "geometry and coordination constrain reallocation",
        "=> spatial demand re-enters."
    ]))

    out.append(arrow(585,235,585,320))
    out.append(box(390,320,390,115,"4  Broad empirical test",[
        "5,816 observations / 55 migratory bird species:",
        "one universal natural speed rule is rejected.",
        "Phase centering shifts the point minimum but not heterogeneity."
    ]))
    out.append(arrow(585,435,585,495))
    out.append(box(295,495,580,125,"5  What replaces the failed universal rule",[
        "mule deer, barnacle geese and wigeon transform incoming phase error;",
        "raw lambda is interval-scale, actuator architecture is system-specific;",
        "environmental information, retention and actuation stay separate."
    ]))
    out.append(arrow(875,557,1035,557))
    out.append(box(955,480,205,155,"6  Perturbation gate",[
        "industrial mule deer:",
        "actuation attenuation known;",
        "fixed-24 h lambda test",
        "remains outcome-blind."
    ]))
    out.append(text(55,680,"Headline: temporal buffering delays but does not replace spatial tracking.",16,"700"))
    out.append("</svg>")
    path.write_text("\n".join(out)+"\n",encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_all(output_dir: Path, aikens_result: Path | None = None) -> dict:
    output_dir.mkdir(parents=True,exist_ok=True)
    synth_dir=output_dir/"_synthetic_source"
    empirical_dir=output_dir/"_empirical_source"
    render_synthetic(synth_dir)
    empirical=render_empirical(empirical_dir,aikens_result)

    paths={
        "figure_1":output_dir/"PAYOFF_B_INTEGRATED_FIG1_CONCEPT.svg",
        "figure_2":output_dir/"PAYOFF_B_INTEGRATED_FIG2_TEMPORAL_BYPASS.svg",
        "figure_3":output_dir/"PAYOFF_B_INTEGRATED_FIG3_COORDINATION_GATE.svg",
        "figure_4":output_dir/"PAYOFF_B_INTEGRATED_FIG4_BROAD_BIRD.svg",
        "figure_5":output_dir/"PAYOFF_B_INTEGRATED_FIG5_DIRECT_SYSTEMS.svg",
        "figure_6":output_dir/"PAYOFF_B_INTEGRATED_FIG6_INFORMATION_ACTUATION.svg",
    }
    render_integrated_concept(paths["figure_1"])
    shutil.copyfile(synth_dir/"PAYOFF_B_TRACKING_FIG2_TEMPORAL_BYPASS.svg",paths["figure_2"])
    shutil.copyfile(synth_dir/"PAYOFF_B_TRACKING_FIG3_COORDINATION_GATE.svg",paths["figure_3"])
    shutil.copyfile(empirical["figure_4"],paths["figure_4"])
    shutil.copyfile(empirical["figure_5"],paths["figure_5"])
    shutil.copyfile(empirical["figure_6"],paths["figure_6"])

    aikens_payload = None
    if aikens_result is not None:
        aikens_payload = json.loads(aikens_result.read_text(encoding="utf-8"))
    aikens_result_present = aikens_payload is not None
    aikens_outcome_opened = False
    if aikens_payload is not None:
        aikens_outcome_opened = bool(
            aikens_payload.get(
                "lambda_outcome_opened",
                aikens_payload.get("status") != "phase_retention_contrast_not_estimable",
            )
        )
    manifest={
        "status":"payoff_b_integrated_six_figure_set",
        "aikens_result_present":aikens_result_present,
        "aikens_outcome_opened":aikens_outcome_opened,
        "source_policy":{
            "figure_1":"integrated conceptual synthesis; no new quantitative result",
            "figures_2_3":"frozen synthetic 2026-09-20 receipt chain",
            "figures_4_6":"frozen machine empirical receipts / outcome-blind Aikens slot",
        },
        "figures":{
            k:{"path":str(v),"sha256":sha256(v),"bytes":v.stat().st_size}
            for k,v in paths.items()
        },
    }
    mp=output_dir/"PAYOFF_B_INTEGRATED_SIX_FIGURE_MANIFEST.json"
    mp.write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    shutil.rmtree(synth_dir)
    shutil.rmtree(empirical_dir)
    return {"manifest":mp,**paths}


def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument("--output-dir",type=Path,default=Path("outputs/integrated_tracking_six_figures"))
    p.add_argument("--aikens-result",type=Path)
    a=p.parse_args()
    paths=render_all(a.output_dir,a.aikens_result)
    for k,v in paths.items():
        print(f"{k}={v}")


if __name__=="__main__":
    main()
