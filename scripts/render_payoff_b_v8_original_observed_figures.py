#!/usr/bin/env python3
"""Two genuinely observation-level V8 ecological SVG figures.

Reads actual original 2026-10-05 archived V8 pair/target rows only AFTER the
immutable-artifact restoration receipt has passed. Never draws manufactured
pair or species observations from numerical means. No new ecological model
or inference is fit: any weighted line is reconstructed from the frozen
original equal-species-weighted regression estimand.
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import html
import json
import math
from pathlib import Path
from xml.etree import ElementTree as ET

from scripts.audit_payoff_b_v8_restored_rows import (
    weighted_slope, load_rows
)

WIDTH, HEIGHT = 1280, 740
INK, BLUE, GREY, LIGHT, NULL = "#263743", "#315878", "#697988", "#e3e9ed", "#a56038"


def esc(value):
    return html.escape(str(value),quote=False)


def fnum(x):
    if not math.isfinite(float(x)):
        raise ValueError("Nonfinite original point")
    return float(x)


def svg_header(title, subtitle):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}" role="img">',
        f'<title>{esc(title)}</title>',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="55" y="54" font-size="24" font-family="Arial, sans-serif" fill="{INK}" font-weight="bold">{esc(title)}</text>',
        f'<text x="56" y="82" font-size="15" font-family="Arial, sans-serif" fill="{GREY}">{esc(subtitle)}</text>',
    ]


def txt(x,y,caption,fs=14,fill=INK,anchor="start"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial, sans-serif" '
            f'fill="{fill}" font-size="{fs}" text-anchor="{anchor}">{esc(caption)}</text>')


def lin(x,y,x2,y2,stroke=GREY,width=1,dash=None):
    dashpart=f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
            f'stroke="{stroke}" stroke-width="{width}"{dashpart}/>')


def mapx(x,lo,hi):
    return 160+(x-lo)/(hi-lo)*780


def mapy(y,lo,hi):
    return 590-(y-lo)/(hi-lo)*440


def plot_axis(xlo,xhi,ylo,yhi,xlabel,ylabel):
    elements=[]
    for i in range(6):
        x=xlo+(xhi-xlo)*i/5
        y=ylo+(yhi-ylo)*i/5
        px=mapx(x,xlo,xhi)
        py=mapy(y,ylo,yhi)
        elements += [
            lin(px,150,px,590,LIGHT,.9),
            lin(160,py,940,py,LIGHT,.9),
            txt(px,616,f"{x:+.2f}",13,GREY,"middle"),
            txt(149,py+5,f"{y:+.2f}",13,GREY,"end"),
        ]
    elements += [
        lin(160,590,940,590,INK,1.4),
        lin(160,150,160,590,INK,1.4),
        txt(550,672,xlabel,18,INK,"middle"),
        txt(65,136,ylabel,16),
    ]
    return elements


def figure2(pairs, env_summary):
    header=svg_header("Figure 2. Stronger spring coupling across environmental pairs",
        "Each point is an original, distinct geographic source–target pair; not a tracked bird route")
    lines=plot_axis(-1,1,-1,1,"Detrended rho in 2002–2009","Detrended rho in 2010–2017")
    lines.append(lin(mapx(-1,-1,1),mapy(-1,-1,1),
                     mapx(1,-1,1),mapy(1,-1,1),GREY,2,"7,5"))
    for row in pairs:
        old=fnum(row["rho_early"]);new=fnum(row["rho_late"])
        lines.append(
            f'<circle class="observed-spatial-pair" cx="{mapx(old,-1,1):.2f}" '
            f'cy="{mapy(new,-1,1):.2f}" r="4.2" fill="{BLUE}" fill-opacity="0.48"/>'
        )
    mean=env_summary["mean_delta_rho"]
    ci=env_summary["ci95_pair_bootstrap"]
    lines += [
        txt(969,184,"Source-backed data",18,INK),
        txt(969,220,"166 unique pairs",16),
        txt(969,247,"28 species use these pairs",14,GREY),
        txt(969,303,"Mean late - early:",15),
        txt(969,335,f"{mean:+.3f}",21,BLUE),
        txt(969,368,f"95% pair CI [{ci[0]:+.3f}, {ci[1]:+.3f}]",13),
        txt(969,430,"Dashed line: y = x",13,GREY),
        txt(969,459,"Above line: stronger coupling",13,GREY),
        txt(968,524,"Original broad degradation",13),
        txt(968,548,"hypothesis: NOT SUPPORTED",13,BLUE),
        txt(55,703,"Only environmental correlations are measured; cue perception and demographic fitness are not estimated.",12,GREY),
        "</svg>",
    ]
    return "\n".join(header+lines)+"\n"


def weighted_fit(rows,ykey):
    counts=collections.Counter(r["species"] for r in rows)
    weights=[1/counts[r["species"]] for r in rows]
    total=sum(weights)
    xbar=sum(fnum(r["z_delta_rho"])*w for r,w in zip(rows,weights))/total
    ybar=sum(fnum(r[ykey])*w for r,w in zip(rows,weights))/total
    slope=weighted_slope(rows,ykey)
    return (slope,ybar-slope*xbar)


def rounded_bounds(vals):
    lo,hi=min(vals),max(vals)
    span=hi-lo
    if span<1e-8:
        span=1
    pad=.08*span
    return lo-pad,hi+pad


def figure3(transfer,structural,summary):
    allx=[fnum(r["z_delta_rho"]) for r in transfer]
    ally=[fnum(r["delta_mismatch"]) for r in transfer]
    # Include original fixed-arrival null panel domain, not manufactured data.
    y_null=[fnum(r["delta_pseudo_mismatch"]) for r in structural]
    xl,xh=rounded_bounds(allx)
    yl,yh=rounded_bounds(ally+y_null)
    slope_obs,int_obs=weighted_fit(transfer,"delta_mismatch")
    slope_null,int_null=weighted_fit(structural,"delta_pseudo_mismatch")
    if abs(slope_obs-summary["beta"])>1e-8:
        raise ValueError("Observed original source rows do not match frozen beta")
    if abs(slope_null-summary["null_beta"])>1e-4:
        raise ValueError("Original structural null source rows do not match frozen beta")

    elems=svg_header("Figure 3. Environmental change did not predict better bird matching",
       "150 original species–target observations; shared environmental exposures across 72 distinct pairs")
    elems+=plot_axis(xl,xh,yl,yh,
         "Standardized environmental correlation change",
         "Late-minus-early log arrival/green-up mismatch")
    if xl<0<xh:
        elems.append(lin(mapx(0,xl,xh),150,mapx(0,xl,xh),590,GREY,1.5,"4,5"))
    if yl<0<yh:
        elems.append(lin(160,mapy(0,yl,yh),940,mapy(0,yl,yh),GREY,1.5,"4,5"))
    for row in transfer:
        cx=mapx(fnum(row["z_delta_rho"]),xl,xh)
        cy=mapy(fnum(row["delta_mismatch"]),yl,yh)
        elems.append(
            f'<circle class="observed-species-target" cx="{cx:.2f}" cy="{cy:.2f}" '
            f'r="4.2" fill="{BLUE}" fill-opacity="0.36"/>'
        )
    for slope,intercept,colour,dash in [
        (slope_obs,int_obs,BLUE,None),
        (slope_null,int_null,NULL,"7,6"),
    ]:
        elems.append(lin(mapx(xl,xl,xh),mapy(intercept+slope*xl,yl,yh),
                         mapx(xh,xl,xh),mapy(intercept+slope*xh,yl,yh),
                         colour,3,dash))
    ci=summary["ci95"]
    elems += [
        txt(962,180,"Registered transfer:",15),
        txt(962,213,f"beta = {slope_obs:+.4f}",17,BLUE),
        txt(962,239,f"CI [{ci[0]:+.3f}, {ci[1]:+.3f}]",13),
        txt(962,299,"Fixed-arrival null:",15),
        txt(962,333,f"beta = {slope_null:+.4f}",17,NULL),
        txt(962,369,"Dashed line: fixed arrival",13,NULL),
        txt(962,396,"Solid line: observed",13,BLUE),
        txt(962,468,"Bird-specific increment",14),
        txt(962,495,"not detected",15,BLUE),
        txt(962,552,"150 rows / 72 pairs / 22 species",12,GREY),
        txt(55,703,"Scatter shows original rows; species-target points are not independent spatial-pair observations.",12,GREY),
        "</svg>",
    ]
    return "\n".join(elems)+"\n"


def render(artifact_root,receipt,out):
    receipt=json.loads(receipt.read_text(encoding="utf-8"))
    if receipt.get("status")!="FROZEN_V8_ROW_LEVEL_ARTIFACTS_RESTORED_AND_ARITHMETIC_VERIFIED":
        raise ValueError("Refusing point-level plot without validated original row receipt")
    base=artifact_root
    p=base/"environment/payoff_b_v8_primary_unique_pairs.csv"
    b=base/"transfer/payoff_b_v8_transfer_primary_rows.csv"
    n=base/"structural/payoff_b_v8_transfer_structural_null_rows.csv"
    pair_rows=load_rows(p)
    trans=load_rows(b)
    null_rows=load_rows(n)
    if (len(pair_rows)!=166 or len({r["pair_key"] for r in pair_rows})!=166 or
        len(trans)!=150 or len({r["pair_key"] for r in trans})!=72 or
        len({r["species"] for r in trans})!=22 or len(null_rows)!=150):
        raise ValueError("Restored observation count or clustering changed")
    t=receipt["transfer"]
    st=receipt["structural_null"]
    summary={
        "beta":t["beta"],
        "null_beta":st["fixed_arrival_beta"],
        "ci95":t["bootstrap_ci95"],
    }
    files={
        "figure2_observed_166_pairs.svg":figure2(pair_rows,receipt["environment"]),
        "figure3_observed_150_species_targets.svg":figure3(trans,null_rows,summary),
    }
    out.mkdir(parents=True,exist_ok=True)
    if any(out.iterdir()):
        raise ValueError("Refuse to overwrite existing publication preview")
    checksum={}
    for name,contents in files.items():
        # Assert the image syntax parses; this checks markup, not publication layout.
        ET.fromstring(contents)
        raw=contents.encode("utf-8")
        (out/name).write_bytes(raw)
        checksum[name]=hashlib.sha256(raw).hexdigest()
    provenance={
        "status":"ORIGINAL_V8_OBSERVED_ROW_SVG_PREVIEW_SUBMISSION_HOLD",
        "verified_actual_spatial_pair_points":166,
        "verified_actual_species_target_points":150,
        "distinct_environmental_pairs_in_transfer":72,
        "no_synthetic_points":True,
        "no_new_biological_hypothesis_fitted":True,
        "source_row_sha256":{
            "environment_pairs":hashlib.sha256(p.read_bytes()).hexdigest(),
            "transfer_rows":hashlib.sha256(b.read_bytes()).hexdigest(),
            "structural_rows":hashlib.sha256(n.read_bytes()).hexdigest(),
        },
        "svg_sha256":checksum,
        "independent_pair_count_as_n_for_transfer":False,
        "visual_quality_approved":False,
        "anonymous_archive_complete":False,
        "submission_ready":False,
    }
    (out/"observed_figures_receipt.json").write_text(
        json.dumps(provenance,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return provenance


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--original",type=Path,required=True)
    p.add_argument("--verification",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    r=render(args.original,args.verification,args.out)
    print(json.dumps({k:r[k] for k in (
        "status","verified_actual_spatial_pair_points",
        "verified_actual_species_target_points","submission_ready")}))


if __name__=="__main__":
    main()
