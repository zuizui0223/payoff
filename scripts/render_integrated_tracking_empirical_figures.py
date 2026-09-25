#!/usr/bin/env python3
"""Render integrated PAYOFF-B empirical Figures 4–6 from frozen machine receipts.

Dependency-free SVG renderer. It never reads manuscript prose for numbers.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BROAD = ROOT / "data" / "payoff_b_broad_bird_stage1_result_20260925.json"
INPUTS = ROOT / "data" / "payoff_b_integrated_empirical_figure_inputs_20260925.json"
PANEL = ROOT / "data" / "payoff_b_empirical_phase_panel_status_20260921.json"
STANDARD = ROOT / "data" / "payoff_b_phase_retention_interval_standardization_result_20260925.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def esc(x: object) -> str:
    return html.escape(str(x))


def svg_start(w: int, h: int, title: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="30" y="36" font-family="sans-serif" font-size="22" font-weight="700">{esc(title)}</text>',
    ]


def text(x, y, s, size=13, weight="400", anchor="start"):
    return f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{esc(s)}</text>'


def line(x1, y1, x2, y2, width=1.5, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="black" stroke-width="{width}"{d}/>'


def rect(x, y, w, h, fill="none", stroke="black", width=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'


def circle(x, y, r=5, fill="black"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="black" stroke-width="1"/>'


def log_map(v, lo, hi, x0, x1):
    return x0 + (math.log(v) - math.log(lo)) / (math.log(hi) - math.log(lo)) * (x1 - x0)


def linear_map(v, lo, hi, x0, x1):
    return x0 + (v - lo) / (hi - lo) * (x1 - x0)


def render_figure4(out: Path, broad: dict) -> None:
    w, h = 1100, 560
    s = svg_start(w, h, "Figure 4. Broad natural test rejects one universal speed rule")
    s.append(text(45, 78, "A  Fitted speed-ratio minima", 15, "700"))
    x0, x1 = 120, 610
    y0 = 455
    lo, hi = 0.25, 16.0
    for tick in [0.25, 0.5, 1, 1.6061152988, 2, 4, 8, 16]:
        x = log_map(tick, lo, hi, x0, x1)
        s.append(line(x, 115, x, y0, 0.7, "3,4"))
        s.append(text(x, y0 + 24, f"{tick:g}", 11, anchor="middle"))
    band0 = log_map(1.0, lo, hi, x0, x1)
    band1 = log_map(1.6061152988, lo, hi, x0, x1)
    s.append(f'<rect x="{band0}" y="105" width="{band1-band0}" height="{y0-105}" fill="#eeeeee" stroke="none"/>')
    s.append(text((band0+band1)/2, 130, "PAYOFF-B1 benchmark", 10, anchor="middle"))

    minima = broad["gam_minima"]
    rows = [
        ("Raw mismatch, median alignment", "raw_abs_lag", 0.948293188488715, 190),
        ("Phase-centered, median alignment", "centered_abs_lag", 0.948374287018569, 275),
        ("Phase-centered, perfect alignment", "centered_abs_lag", 1.0, 360),
    ]
    unc = {round(float(x["alignment_ref"]),6): x for x in broad["centered_optimum_uncertainty"]}
    for label, response, align, y in rows:
        m = min((x for x in minima if x["response"] == response), key=lambda x: abs(float(x["alignment_ref"]) - align))
        x = log_map(float(m["u_star"]), lo, hi, x0, x1)
        if response == "centered_abs_lag":
            u = unc[round(align,6)]
            xl = log_map(float(u["u_lo_95"]), lo, hi, x0, x1)
            xh = log_map(float(u["u_hi_95"]), lo, hi, x0, x1)
            s.append(line(xl, y, xh, y, 3))
            s.append(line(xl, y-7, xl, y+7, 1.5))
            s.append(line(xh, y-7, xh, y+7, 1.5))
        s.append(circle(x, y, 6))
        s.append(text(55, y+5, label, 12))
        s.append(text(x+10, y-10, f'u*={float(m["u_star"]):.3f}', 11))
    s.append(line(x0, y0, x1, y0, 1.5))
    s.append(text((x0+x1)/2, y0+48, "animal speed / environmental-wave speed (log scale)", 12, anchor="middle"))

    s.append(text(675, 78, "B  Species-level heterogeneity", 15, "700"))
    sh = broad["species_heterogeneity"]
    cats = [
        ("Species fit", sh["n_species_fit"]),
        ("Positive curvature", sh["n_positive_curvature"]),
        ("Internal vertex", sh["n_vertices_inside_5_95"]),
        ("Curvature p<0.1", sh["n_curvature_p_lt_0_1"]),
    ]
    bx0, bx1 = 760, 1030
    for i,(label,val) in enumerate(cats):
        y = 165 + i*72
        s.append(text(675, y+6, label, 12))
        barw = (bx1-bx0) * float(val) / max(1, float(sh["n_species_fit"]))
        s.append(rect(bx0, y-15, barw, 26, fill="#dddddd"))
        s.append(text(bx0+barw+8, y+5, f"{val}/{sh['n_species_fit']}", 12))
    s.append(text(675, 475, "Point minima shift with phase centering,", 12))
    s.append(text(675, 493, "but uncertainty and heterogeneity remain large.", 12))
    s.append("</svg>")
    out.write_text("\n".join(s)+"\n", encoding="utf-8")


def render_figure5(out: Path, inputs: dict, panel: dict, standard: dict) -> None:
    w, h = 1100, 600
    s = svg_start(w, h, "Figure 5. Real systems transform phase error through different architectures")
    s.append(text(45, 78, "A  Raw segment-scale retention", 15, "700"))
    x0, x1 = 265, 620
    for tick in [0,0.25,0.5,0.75,1.0]:
        x=linear_map(tick,0,1,x0,x1)
        s.append(line(x,110,x,475,0.7,"3,4"))
        s.append(text(x,498,f"{tick:g}",11,anchor="middle"))
    rows=list(inputs["direct_controller_rows"])
    wigeon=next(x for x in panel["direct_taxa"] if x["common_name"]=="Eurasian wigeon")
    rows.append({"label":"Eurasian wigeon ERA5","lambda":wigeon["independent_era5_replication"]["lambda_hat"],"lambda_abs":abs(wigeon["independent_era5_replication"]["lambda_hat"]),"controller_architecture":"independent reconstruction"})
    for i,row in enumerate(rows):
        y=145+i*52
        x=linear_map(float(row["lambda_abs"]),0,1,x0,x1)
        s.append(text(50,y+5,row["label"],11))
        s.append(circle(x,y,5,fill="white" if float(row["lambda"])<0 else "black"))
        if float(row["lambda"])<0:
            s.append(text(x+9,y-8,"overshoot sign",9))
    s.append(line(x0,475,x1,475,1.5))
    s.append(text((x0+x1)/2,525,"|lambda| on declared ecological interval",12,anchor="middle"))

    s.append(text(675,78,"B  Secondary path-memory comparison",15,"700"))
    ist=panel["measurement_error_status"]["interval_standardization"]
    vals=[
        ("Mule deer whole migration",ist["mule_deer_whole_migration_retention"]),
        ("Wigeon POWER ×7",ist["wigeon_power_typical_path_retention"]),
        ("Wigeon ERA5 ×7",ist["wigeon_era5_typical_path_retention"]),
        ("Wigeon conservative SIMEX ×7",ist["wigeon_conservative_simex_typical_path_retention"]),
    ]
    bx0,bx1=760,1030
    for i,(label,val) in enumerate(vals):
        y=160+i*78
        s.append(text(675,y+5,label,11))
        bw=(bx1-bx0)*float(val)
        s.append(rect(bx0,y-14,bw,26,fill="#dddddd"))
        s.append(text(bx0+bw+8,y+5,f"{float(val):.3f}",11))
    s.append(text(675,505,"Secondary standardization clarifies scale;",11))
    s.append(text(675,523,"it does not define a universal biological lambda.",11))
    s.append("</svg>")
    out.write_text("\n".join(s)+"\n",encoding="utf-8")


def render_figure6(out: Path, inputs: dict, aikens_result: dict | None) -> None:
    w,h=1200,610
    s=svg_start(w,h,"Figure 6. Information, retention and actuation are distinct")
    s.append(text(40,78,"A  Environmental innovation vs retention",14,"700"))
    x0,x1,y0,y1=70,390,440,125
    inv=[x for x in inputs["innovation_rows"] if x["stable_phase_map"]]
    xmin,xmax=3.2,6.5
    for tick in [3.5,4,4.5,5,5.5,6,6.5]:
        x=linear_map(tick,xmin,xmax,x0,x1); s.append(line(x,y1,x,y0,0.6,"3,4")); s.append(text(x,y0+20,f"{tick:g}",10,anchor="middle"))
    for tick in [0,0.25,0.5,0.75,1]:
        y=y0-(y0-y1)*tick; s.append(line(x0,y,x1,y,0.6,"3,4")); s.append(text(x0-8,y+4,f"{tick:g}",10,anchor="end"))
    for row in inv:
        x=linear_map(row["environmental_innovation_sd_days"],xmin,xmax,x0,x1)
        y=y0-(y0-y1)*row["abs_lambda"]
        s.append(circle(x,y,5))
        s.append(text(x+7,y-7,f"{row['flyway']} {row['transition']}",9))
    s.append(line(x0,y0,x1,y0)); s.append(line(x0,y0,x0,y1))
    s.append(text((x0+x1)/2,485,"environmental innovation SD (days)",11,anchor="middle"))
    s.append(text(12,285,"|lambda|",11))

    s.append(text(430,78,"B  Industrial actuation contrast",14,"700"))
    xx0,xx1=500,760
    rows=inputs["industrial_rows"]
    gmax=max(max(r["median_G_small"],r["median_G_large"]) for r in rows)
    for i,row in enumerate(rows):
        y=135+i*42
        a=linear_map(row["median_G_small"],0,gmax,xx0,xx1)
        b=linear_map(row["median_G_large"],0,gmax,xx0,xx1)
        s.append(line(a,y,b,y,1.2))
        s.append(circle(a,y,4,"white")); s.append(circle(b,y,4,"black"))
        s.append(text(440,y+4,f"{row['edge_km']}/{row['far_km']} km",9))
    s.append(text(500,500,"○ small development   ● large development",10))
    s.append(text(500,520,"8/8 definitions: G_large < G_small",10))
    primary=next(r for r in rows if r["edge_km"]==2 and r["far_km"]==10)
    s.append(text(500,540,f"Primary log-G shift={primary['large_intercept_shift']:.3f}, p={primary['large_intercept_shift_p']:.3f}",10))
    s.append(text(500,558,"Stronger year×development trend: not supported",10))

    s.append(text(825,78,"C  Preregistered within-taxon lambda test",14,"700"))
    s.append(rect(840,120,315,335,fill="#f5f5f5"))
    if aikens_result is None:
        s.append(text(997,225,"Aikens fixed-24 h lambda outcome",13,"700",anchor="middle"))
        s.append(text(997,255,"UNOPENED",22,"700",anchor="middle"))
        s.append(text(997,292,"No retuning permitted.",11,anchor="middle"))
        s.append(text(997,312,"Panel remains pending until the",11,anchor="middle"))
        s.append(text(997,330,"registered environmental extraction runs.",11,anchor="middle"))
    else:
        status=str(aikens_result.get("status","UNKNOWN"))
        s.append(text(997,205,"Registered Aikens result",13,"700",anchor="middle"))
        s.append(text(997,235,status,13,"700",anchor="middle"))
        gate=aikens_result.get("gate") or {}
        obs=gate.get("observation") or {}
        if "lambda_a" in obs and "lambda_b" in obs:
            s.append(text(997,285,f"lambda small={obs['lambda_a']:.3f}",12,anchor="middle"))
            s.append(text(997,307,f"lambda large={obs['lambda_b']:.3f}",12,anchor="middle"))
            s.append(text(997,329,f"Delta={gate.get('lambda_difference_b_minus_a',float('nan')):.3f}",12,anchor="middle"))
    s.append(text(997,430,"Within taxon; never added as a fourth",10,anchor="middle"))
    s.append(text(997,447,"cross-taxon replication.",10,anchor="middle"))
    s.append("</svg>")
    out.write_text("\n".join(s)+"\n",encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_all(output_dir: Path, aikens_result_path: Path | None = None) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    broad=load(BROAD); inputs=load(INPUTS); panel=load(PANEL); standard=load(STANDARD)
    aikens=load(aikens_result_path) if aikens_result_path else None
    paths={
        "figure_4":output_dir/"PAYOFF_B_INTEGRATED_FIG4_BROAD_BIRD.svg",
        "figure_5":output_dir/"PAYOFF_B_INTEGRATED_FIG5_DIRECT_SYSTEMS.svg",
        "figure_6":output_dir/"PAYOFF_B_INTEGRATED_FIG6_INFORMATION_ACTUATION.svg",
    }
    render_figure4(paths["figure_4"],broad)
    render_figure5(paths["figure_5"],inputs,panel,standard)
    render_figure6(paths["figure_6"],inputs,aikens)
    manifest={
        "status":"integrated_tracking_empirical_figures",
        "aikens_outcome_opened":aikens is not None,
        "sources":[str(BROAD.relative_to(ROOT)),str(INPUTS.relative_to(ROOT)),str(PANEL.relative_to(ROOT)),str(STANDARD.relative_to(ROOT))],
        "files":{k:{"path":str(v),"sha256":sha256(v)} for k,v in paths.items()},
    }
    mp=output_dir/"PAYOFF_B_INTEGRATED_EMPIRICAL_FIGURE_MANIFEST.json"
    mp.write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    return {"manifest":mp,**paths}


def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument("--output-dir",type=Path,default=Path("outputs/integrated_tracking_figures"))
    p.add_argument("--aikens-result",type=Path)
    a=p.parse_args()
    paths=render_all(a.output_dir,a.aikens_result)
    for k,v in paths.items():
        print(f"{k}={v}")


if __name__=="__main__":
    main()
