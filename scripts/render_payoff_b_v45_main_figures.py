#!/usr/bin/env python3
"""Render the PAYOFF-B V4.5 American Naturalist main figures as SVG.

The renderer reads only the frozen V4.5 figure-data manifest:
data/payoff_b_v45_figure_data_20261006.json

It does not rerun analyses and does not infer missing values.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "payoff_b_v45_figure_data_20261006.json"

WIDTH = 1400
HEIGHT = 900
MARGIN = 60

INK = "#202124"
MUTED = "#5f6368"
GRID = "#dadce0"
BLUE = "#3367d6"
ORANGE = "#d97706"
GREEN = "#188038"
RED = "#c5221f"
PURPLE = "#7e57c2"
LIGHT_BLUE = "#e8f0fe"
LIGHT_ORANGE = "#fef3e2"
LIGHT_GREEN = "#e6f4ea"
LIGHT_GRAY = "#f5f5f5"


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def text(x, y, value, size=18, weight="normal", anchor="start", fill=INK):
    return (
        f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" '
        f'fill="{fill}">{esc(value)}</text>'
    )


def line(x1, y1, x2, y2, width=2, color=INK, dash=None):
    extra = "" if dash is None else f' stroke-dasharray="{dash}"'
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{color}" stroke-width="{width}"{extra}/>'
    )


def rect(x, y, w, h, fill="white", stroke=INK, width=1.5, rx=0):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'
    )


def circle(cx, cy, r=5, fill="white", stroke=INK, width=1.8):
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{width}"/>'
    )


def polyline(points, color=INK, width=2.5, dash=None, fill="none"):
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    extra = "" if dash is None else f' stroke-dasharray="{dash}"'
    return (
        f'<polyline points="{pts}" fill="{fill}" stroke="{color}" '
        f'stroke-width="{width}"{extra}/>'
    )


def polygon(points, fill=INK, stroke="none"):
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}"/>'


def arrow(x1, y1, x2, y2, color=INK, width=2.2):
    out = [line(x1, y1, x2, y2, width, color)]
    angle = math.atan2(y2-y1, x2-x1)
    size = 10
    a1 = angle + math.pi*0.84
    a2 = angle - math.pi*0.84
    out.append(
        polygon([
            (x2, y2),
            (x2 + size*math.cos(a1), y2 + size*math.sin(a1)),
            (x2 + size*math.cos(a2), y2 + size*math.sin(a2)),
        ], fill=color)
    )
    return "".join(out)


def wrap(value: str, max_chars: int) -> list[str]:
    words = str(value).split()
    lines, cur, n = [], [], 0
    for word in words:
        add = len(word) + (1 if cur else 0)
        if cur and n + add > max_chars:
            lines.append(" ".join(cur))
            cur, n = [word], len(word)
        else:
            cur.append(word)
            n += add
    if cur:
        lines.append(" ".join(cur))
    return lines


def paragraph(x, y, value, width_chars=52, size=14, dy=19, fill=INK, weight="normal"):
    out = []
    for i, row in enumerate(wrap(value, width_chars)):
        out.append(text(x, y+i*dy, row, size, weight, fill=fill))
    return "".join(out)


def panel_label(x, y, label, title):
    return text(x, y, label, 22, "700") + text(x+34, y, title, 18, "700")


def scale(v, lo, hi, a, b):
    if hi == lo:
        return (a+b)/2
    return a + (v-lo)*(b-a)/(hi-lo)


def interval_glyph(x0, x1, y, lo, est, hi, color=BLUE, value_fmt="{:+.2f}"):
    xs = scale(lo, lo, hi, x0, x1)
    xe = scale(est, lo, hi, x0, x1)
    xh = scale(hi, lo, hi, x0, x1)
    return "".join([
        line(xs, y, xh, y, 4, color),
        line(xs, y-8, xs, y+8, 2, color),
        line(xh, y-8, xh, y+8, 2, color),
        circle(xe, y, 6, fill=color, stroke=color),
        text(x1+12, y+5, value_fmt.format(est), 13, "700", fill=color),
    ])


def svg_page(title, subtitle, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}">'
        '<rect width="100%" height="100%" fill="white"/>'
        f'{text(MARGIN, 42, title, 27, "700")}'
        f'{text(MARGIN, 70, subtitle, 14, fill=MUTED)}'
        f'{body}</svg>\n'
    )


def figure1(data: dict) -> str:
    d = data["figure_1"]
    out = []

    # Panel A: forecastability decomposition.
    out.append(panel_label(60, 120, "A", "External forecastability"))
    out.append(rect(70, 150, 570, 270, fill=LIGHT_GRAY, stroke=GRID, rx=8))
    out.append(text(95, 185, "Ideal-observer prediction problem", 16, "700"))
    out.append(text(100, 225, "baseline risk", 14, fill=MUTED))
    out.append(rect(100, 245, 480, 52, fill="#ffffff", stroke=GRID, rx=5))
    out.append(rect(100, 245, 280, 52, fill=LIGHT_BLUE, stroke=BLUE, rx=5))
    out.append(text(240, 277, "G_E  forecast value", 14, "700", "middle", BLUE))
    out.append(text(480, 277, "residual risk", 14, "700", "middle", MUTED))
    out.append(text(100, 330, f"R0 = {d['gaussian']['baseline_risk']}", 15))
    out.append(text(100, 355, f"G_E = {d['gaussian']['ideal_observer_value']}", 15, fill=BLUE))
    out.append(text(100, 380, f"R1 = {d['gaussian']['residual_risk']}", 15, fill=MUTED))

    # Panel B: access bottleneck.
    out.append(panel_label(720, 120, "B", "Forecastable ≠ accessible"))
    out.append(rect(730, 150, 600, 270, fill=LIGHT_GRAY, stroke=GRID, rx=8))
    out.append(rect(770, 195, 500, 62, fill=LIGHT_BLUE, stroke=BLUE, rx=6))
    out.append(text(1020, 232, "external environmental information set  I_E", 15, "700", "middle", BLUE))
    out.append(rect(870, 285, 300, 58, fill=LIGHT_ORANGE, stroke=ORANGE, rx=6))
    out.append(text(1020, 319, "organism-accessible set  I_O", 15, "700", "middle", ORANGE))
    out.append(arrow(1020, 257, 1020, 282, MUTED))
    out.append(text(1020, 382, d["inequality"], 18, "700", "middle", PURPLE))
    out.append(text(1020, 406, "extra analyst information can be unavailable to the organism", 13, anchor="middle", fill=MUTED))

    # Panel C: actionability window.
    out.append(panel_label(60, 500, "C", "Accessible information × actionability"))
    x0, x1, y0, y1 = 90, 640, 540, 805
    out.append(line(x0, y1, x1, y1, 1.8))
    out.append(line(x0, y0, x0, y1, 1.8))
    out.append(text((x0+x1)/2, 842, "seasonal sequence", 14, anchor="middle"))
    out.append(text(85, 528, "relative value", 13, fill=MUTED))
    pts_g, pts_r, pts_n = [], [], []
    for i in range(101):
        t = i/100
        g = 1-math.exp(-3.2*t)
        r = math.exp(-1.6*t)
        n = g*r
        x = scale(t,0,1,x0,x1)
        pts_g.append((x, scale(g,0,1,y1,y0)))
        pts_r.append((x, scale(r,0,1,y1,y0)))
        pts_n.append((x, scale(n,0,0.5,y1,y0)))
    out.append(polyline(pts_g, BLUE, 3))
    out.append(polyline(pts_r, ORANGE, 3))
    out.append(polyline(pts_n, GREEN, 4))
    out.append(text(475, 575, "G_O(t)", 13, "700", fill=BLUE))
    out.append(text(475, 690, "r(t)", 13, "700", fill=ORANGE))
    peak = max(range(len(pts_n)), key=lambda i: -pts_n[i][1])
    px, py = pts_n[peak]
    out.append(line(px, py, px, y1, 1.5, GREEN, "5 5"))
    out.append(circle(px, py, 6, fill=GREEN, stroke=GREEN))
    out.append(text(px+10, py-12, "usable-value peak", 13, "700", fill=GREEN))
    out.append(text(90, 865, d["reduced_form"], 15, "700"))

    # Panel D: correction transition.
    out.append(panel_label(720, 500, "D", "Residual phase can still be corrected"))
    out.append(rect(730, 540, 600, 265, fill=LIGHT_GRAY, stroke=GRID, rx=8))
    boxes = [
        (760, 610, 130, 65, "entry phase", "e_t"),
        (950, 610, 150, 65, "accessible phase", "estimate"),
        (1160, 610, 130, 65, "actuator", "u_t"),
    ]
    for x,y,w,h,t1,t2 in boxes:
        out.append(rect(x,y,w,h,fill="white",stroke=GRID,rx=7))
        out.append(text(x+w/2,y+25,t1,13,"700","middle"))
        out.append(text(x+w/2,y+49,t2,14,"700","middle",PURPLE))
    out.append(arrow(890,642,945,642,MUTED))
    out.append(arrow(1100,642,1155,642,MUTED))
    out.append(arrow(1225,680,1060,745,MUTED))
    out.append(rect(930,725,260,58,fill=LIGHT_GREEN,stroke=GREEN,rx=7))
    out.append(text(1060,758,"updated phase  e_(t+1)",14,"700","middle",GREEN))
    out.append(text(1030, 835, d["phase_update"], 15, "700", "middle"))
    out.append(text(1030, 862, "Forecastability is only the first gate.", 14, "700", "middle", RED))

    return svg_page(
        "Figure 1. Forecastability, access, actionability and correction are distinct",
        "The framework separates what an analyst can predict from what an organism can know and still change.",
        "".join(out),
    )


def figure2(data: dict) -> str:
    d = data["figure_2"]
    p = d["preregistered"]
    e = d["posthoc_environment"]
    o = d["observability"]
    t = d["population_timing"]
    out = []

    # A
    out.append(panel_label(60, 120, "A", "Preregistered environmental coordinate"))
    out.append(rect(70, 150, 300, 270, fill=LIGHT_GRAY, stroke=GRID, rx=8))
    maxrho = 0.8
    for i,(lab,val,col) in enumerate([
        ("2002–09",p["rho_early"],MUTED),
        ("2010–17",p["rho_late"],BLUE),
    ]):
        x=120+i*125
        h=190*val/maxrho
        out.append(rect(x,380-h,70,h,fill=col,stroke=col,rx=3))
        out.append(text(x+35,398,lab,13,"700","middle"))
        out.append(text(x+35,370-h,f"{val:.3f}",14,"700","middle",col))
    out.append(text(220, 188, f"Δρ = {p['delta_rho']:+.3f}", 16, "700", "middle"))
    out.append(text(220, 214, f"26/28 species positive", 13, anchor="middle", fill=MUTED))
    out.append(text(220, 242, "preregistered", 12, "700", "middle", GREEN))

    # B
    out.append(panel_label(420, 120, "B", "Forecastability rose as target variability increased"))
    out.append(rect(430,150,520,270,fill=LIGHT_GRAY,stroke=GRID,rx=8))
    out.append(text(460,185,"Target green-up anomaly SD",14,"700"))
    out.append(text(460,214,f"{e['target_sd_early_days']:.2f} → {e['target_sd_late_days']:.2f} d",17,"700",fill=ORANGE))
    out.append(text(460,257,"Cross-validated forecast-value proxy  G_CV",14,"700"))
    out.append(text(460,286,f"{e['Gcv_early_d2']:+.1f} → {e['Gcv_late_d2']:+.1f} d²",17,"700",fill=BLUE))
    out.append(text(460,318,f"Δ = {e['delta_Gcv_d2']:+.1f} d²",16,"700",fill=BLUE))
    out.append(text(460,346,f"139/166 pairs positive; 25/28 species positive",13,fill=MUTED))
    out.append(text(460,374,"posthoc, model-relative forecast proxy",12,"700",fill=RED))
    out.append(text(460,400,"nearest / 2nd / 3rd source gains: +37.2 / +33.5 / +29.1 d²",12,fill=MUTED))

    # C stacked observability
    out.append(panel_label(1000, 120, "C", "The predictor was not consistently an online cue"))
    out.append(rect(1010,150,330,270,fill=LIGHT_GRAY,stroke=GRID,rx=8))
    categories=[
        ("before source front","before_source_arrival",GREEN),
        ("between stages","between_source_target",ORANGE),
        ("after target front","after_target_arrival",RED),
    ]
    for row_i,(period,label) in enumerate([("early","2002–09"),("late","2010–17")]):
        y=225+row_i*95
        x=1040
        total_w=260
        for cat,key,col in categories:
            frac=o[period][key]
            w=total_w*frac
            out.append(rect(x,y,w,38,fill=col,stroke="white",width=1))
            if w>44:
                out.append(text(x+w/2,y+25,f"{100*frac:.0f}%",12,"700","middle","white"))
            x+=w
        out.append(text(1040,y-10,label,13,"700"))
    y=390
    for i,(cat,key,col) in enumerate(categories):
        x=1035+(i%2)*155
        yy=y+(i//2)*24
        out.append(rect(x,yy-11,12,12,fill=col,stroke=col))
        out.append(text(x+18,yy,cat,10,fill=MUTED))

    # D timing shifts
    out.append(panel_label(60, 500, "D", "Population arrival changed little while target green-up advanced"))
    out.append(rect(70,535,1270,290,fill=LIGHT_GRAY,stroke=GRID,rx=8))
    # timeline
    x0,x1=130,1280
    day_lo,day_hi=120,134
    y_green=625
    y_arr=735
    out.append(line(x0,y_green,x1,y_green,1.5,GRID))
    out.append(line(x0,y_arr,x1,y_arr,1.5,GRID))
    for day in [120,124,128,132,134]:
        x=scale(day,day_lo,day_hi,x0,x1)
        out.append(line(x,595,x,770,1,GRID,"4 5"))
        out.append(text(x,795,str(day),11,anchor="middle",fill=MUTED))
    out.append(text(95,y_green+5,"target green-up",13,"700",anchor="end"))
    out.append(text(95,y_arr+5,"bird arrival",13,"700",anchor="end"))
    # early/late points and arrows
    for y,early,late,col in [
        (y_green,t["target_greenup_early_day"],t["target_greenup_late_day"],ORANGE),
        (y_arr,t["arrival_early_day"],t["arrival_late_day"],BLUE),
    ]:
        xe=scale(early,day_lo,day_hi,x0,x1)
        xl=scale(late,day_lo,day_hi,x0,x1)
        out.append(circle(xe,y,7,fill="white",stroke=col,width=3))
        out.append(circle(xl,y,7,fill=col,stroke=col,width=3))
        out.append(arrow(xe-8,y-24,xl+8,y-24,col,2.5))
        out.append(text(xe,y+29,f"{early:.2f}",11,"700","middle",col))
        out.append(text(xl,y+29,f"{late:.2f}",11,"700","middle",col))
    out.append(text(1070,565,"open = 2002–09   filled = 2010–17",12,fill=MUTED))
    out.append(text(940,690,f"signed lag: {t['signed_lag_early_day']:.2f} → {t['signed_lag_late_day']:.2f} d",15,"700"))
    out.append(text(940,716,f"shift = {t['signed_lag_shift_day']:+.2f} d",15,"700",fill=PURPLE))
    out.append(text(940,744,"zero lag is not assumed optimal",11,fill=MUTED))

    return svg_page(
        "Figure 2. Environmental forecastability increased without proportional arrival adjustment",
        "Bird evidence separates preregistered coupling, posthoc forecastability, observability, and realized population timing.",
        "".join(out),
    )


def figure3(data: dict) -> str:
    d = data["figure_3"]
    out=[]

    # A phase SD
    out.append(panel_label(60,120,"A","Phase variance contracts across migration"))
    out.append(rect(70,150,370,285,fill=LIGHT_GRAY,stroke=GRID,rx=8))
    maxv=30
    for i,(lab,val,col) in enumerate([
        ("start",d["phase_sd_start_day"],ORANGE),
        ("end",d["phase_sd_end_day"],GREEN),
    ]):
        x=135+i*160
        h=200*val/maxv
        out.append(rect(x,390-h,85,h,fill=col,stroke=col,rx=3))
        out.append(text(x+42,412,lab,14,"700","middle"))
        out.append(text(x+42,380-h,f"{val:.2f} d",14,"700","middle",col))
    out.append(text(255,195,f"variance ratio = {d['variance_ratio']:.3f}",15,"700","middle"))
    out.append(text(255,220,f"95% CI {d['variance_ratio_ci'][0]:.3f}–{d['variance_ratio_ci'][1]:.3f}",12,anchor="middle",fill=MUTED))

    # B abs phase
    out.append(panel_label(510,120,"B","Most animal-years move closer to the green wave"))
    out.append(rect(520,150,370,285,fill=LIGHT_GRAY,stroke=GRID,rx=8))
    out.append(text(705,205,f"{100*d['closer_fraction']:.1f}% ended closer to peak",18,"700","middle",GREEN))
    out.append(text(705,260,"mean |phase error|",14,"700","middle"))
    out.append(text(705,305,f"{d['mean_abs_start_day']:.2f} d  →  {d['mean_abs_end_day']:.2f} d",22,"700","middle",PURPLE))
    out.append(text(705,350,f"whole-route λ = {d['lambda']:.3f}",15,"700","middle"))
    out.append(text(705,376,f"95% CI {d['lambda_ci'][0]:.3f}–{d['lambda_ci'][1]:.3f}",12,anchor="middle",fill=MUTED))
    out.append(text(705,410,f"{d['animal_years']} animal-years / {d['individuals']} females",12,anchor="middle",fill=MUTED))

    # C signed actuators
    out.append(panel_label(960,120,"C","Signed phase predicts opposite actuator changes"))
    out.append(rect(970,150,370,285,fill=LIGHT_GRAY,stroke=GRID,rx=8))
    out.append(text(1005,205,"movement rate",14,"700"))
    out.append(line(1005,245,1290,245,1.5,GRID))
    # movement interval scale -0.1..0.1
    lo,hi=-0.10,0.10
    xlo,xhi=1030,1305
    mv=d["movement_slope_km_day_per_phase_day"]
    mlo,mhi=d["movement_slope_ci"]
    out.append(line(scale(mlo,lo,hi,xlo,xhi),245,scale(mhi,lo,hi,xlo,xhi),245,5,BLUE))
    out.append(circle(scale(mv,lo,hi,xlo,xhi),245,6,fill=BLUE,stroke=BLUE))
    out.append(text(1005,285,f"+{mv:.4f} km d⁻¹ per phase day",13,"700",fill=BLUE))
    out.append(text(1005,330,"stopover duration",14,"700"))
    lo2,hi2=-0.7,0.2
    y=370
    out.append(line(1005,y,1290,y,1.5,GRID))
    slo,shi=d["stopover_slope_ci"]; sv=d["stopover_slope_day_per_phase_day"]
    out.append(line(scale(slo,lo2,hi2,xlo,xhi),y,scale(shi,lo2,hi2,xlo,xhi),y,5,ORANGE))
    out.append(circle(scale(sv,lo2,hi2,xlo,xhi),y,6,fill=ORANGE,stroke=ORANGE))
    out.append(text(1005,410,f"{sv:.3f} d per phase day",13,"700",fill=ORANGE))

    # D serial schematic
    out.append(panel_label(60,520,"D","Individual correction provides the natural mechanism anchor"))
    out.append(rect(70,550,1270,260,fill=LIGHT_GRAY,stroke=GRID,rx=8))
    stages=[
        (110,625,220,80,"enter migration","signed phase e₀",ORANGE),
        (405,625,240,80,"access local phase","early / late",BLUE),
        (725,625,240,80,"change progression","speed + stopover",PURPLE),
        (1045,625,230,80,"end migration","reduced phase error",GREEN),
    ]
    for x,y,w,h,a,b,col in stages:
        out.append(rect(x,y,w,h,fill="white",stroke=col,width=2,rx=8))
        out.append(text(x+w/2,y+30,a,14,"700","middle",col))
        out.append(text(x+w/2,y+57,b,13,"middle",fill=MUTED))
    for (x1,x2) in [(330,400),(645,720),(965,1040)]:
        out.append(arrow(x1,665,x2,665,MUTED,2.5))
    out.append(text(705,760,"Published compensation phenomenon; reanalysis places it on the continuous phase scale.",13,"700","middle"))
    out.append(text(705,788,"This does not identify the bird mechanism.",12,"middle",fill=RED))

    return svg_page(
        "Figure 3. Individual trajectories can correct signed phase after commitment",
        "Red Desert mule deer provide an independent individual-level anchor for downstream correction.",
        "".join(out),
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_all(output_dir: Path) -> dict:
    data=json.loads(DATA.read_text(encoding="utf-8"))
    if data.get("status")!="frozen_v45_main_figure_data":
        raise ValueError("unexpected V4.5 figure-data status")
    output_dir.mkdir(parents=True,exist_ok=True)

    figs={
        "figure_1":("PAYOFF_B_V45_FIG1_FRAMEWORK.svg",figure1(data)),
        "figure_2":("PAYOFF_B_V45_FIG2_BIRDS.svg",figure2(data)),
        "figure_3":("PAYOFF_B_V45_FIG3_MULE_DEER.svg",figure3(data)),
    }
    manifest={
        "status":"payoff_b_v45_main_figures",
        "date":data["date"],
        "figure_data":str(DATA.relative_to(ROOT)),
        "figure_data_sha256":sha256(DATA),
        "figures":{},
    }
    for key,(name,svg) in figs.items():
        p=output_dir/name
        p.write_text(svg,encoding="utf-8")
        manifest["figures"][key]={
            "path":str(p),
            "sha256":sha256(p),
            "bytes":p.stat().st_size,
            "format":"svg",
        }
    mp=output_dir/"PAYOFF_B_V45_MAIN_FIGURE_MANIFEST.json"
    mp.write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    return {"manifest":mp,**{k:output_dir/v[0] for k,v in figs.items()}}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/payoff_b_v45_main_figures"),
    )
    args=ap.parse_args()
    out=render_all(args.output_dir)
    for k,v in out.items():
        print(f"{k}={v}")


if __name__=="__main__":
    main()
