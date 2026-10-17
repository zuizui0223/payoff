#!/usr/bin/env python3
"""Render four *summary-level* AmNat review-preview SVGs from frozen PAYOFF-B receipts.

No individual/pair points are synthesized, no unpublished coefficients are
estimated, and no full reviewer data/code archive is claimed. Only frozen
numerical summaries and an explicitly schematic controller are drawn.
Standard library only; no PDF or external dependency.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "v8_environment": "docs/PAYOFF_B_V8_PRIMARY_AND_SENSITIVITY_RESULT_20261005.md",
    "v8_transfer": "docs/PAYOFF_B_V8_DOWNSTREAM_TRANSFER_PRIMARY_RESULT_20261005.md",
    "v8_structural_null": "docs/PAYOFF_B_V8_TRANSFER_STRUCTURAL_NULL_RESULT_20261005.md",
    "ortega": "data/payoff_b_ortega_variance_funnel_result_20261003.json",
    "deer_channels": "data/payoff_b_mule_deer_two_clock_channel_result_20261003.json",
}
W, H = 1180, 690
INK, BLUE, LT, GREY = "#18232d", "#234b65", "#e8eff2", "#697885"


def read_sources(root: Path = ROOT) -> tuple[dict, dict]:
    contents = {}
    hashes = {}
    for name, relative in SOURCES.items():
        raw = (root / relative).read_bytes()
        contents[name] = raw.decode("utf-8")
        hashes[name] = {"path": relative, "sha256": hashlib.sha256(raw).hexdigest()}
    return contents, hashes


def grab(text: str, pattern: str, source: str) -> tuple[float, ...]:
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        raise ValueError("Registered value missing in " + source + ": " + pattern)
    vals = tuple(float(v) for v in match.groups())
    if any(not math.isfinite(v) for v in vals):
        raise ValueError("Nonfinite frozen estimate")
    return vals


def extract_inputs(contents: dict) -> dict:
    a = contents["v8_environment"]
    b = contents["v8_transfer"]
    c = contents["v8_structural_null"]
    deer = json.loads(contents["ortega"])
    two = json.loads(contents["deer_channels"])

    environmental = {
        "unique_pair": {
            "estimate": grab(a, r"unique-pair mean delta-rho = \*\*([+-]?\d+\.\d+)\*\*", "environment")[0],
            "ci95": grab(a, r"95% pair-bootstrap interval = \*\*([+-]?\d+\.\d+) to ([+-]?\d+\.\d+)\*\*", "environment"),
            "n": 166,
        },
        "equal_species": {
            "estimate": grab(a, r"equal-species exposure mean delta-rho = \*\*([+-]?\d+\.\d+)\*\*", "environment")[0],
            "ci95": grab(a, r"95% dependency-aware bootstrap interval = \*\*([+-]?\d+\.\d+) to ([+-]?\d+\.\d+)\*\*", "environment"),
            "n_species": 28,
        },
    }
    if "- 166 unique spatial pairs;" not in a or "- 28 species;" not in a:
        raise ValueError("V8 environmental source unit changed")
    if "V8_BROAD_DEGRADATION = NOT_SUPPORTED" not in a:
        raise ValueError("Outcome support decision changed")

    transfer = {
        "primary": {
            "estimate": grab(b, r"beta_transfer = ([+-]?\d+\.\d+)", "transfer")[0],
            "ci95": grab(b, r"95% interval = \*\*([+-]?\d+\.\d+) to ([+-]?\d+\.\d+)\*\*", "transfer"),
        },
        "fixed_arrival_null": {
            "estimate": grab(c, r"fixed-arrival-null beta = \*\*([+-]?\d+\.\d+)\*\*", "structural null")[0],
            "ci95": grab(c, r"fixed-arrival-null beta = [^\n]+\n- 95% CI = \*\*([+-]?\d+\.\d+) to ([+-]?\d+\.\d+)\*\*", "structural null"),
        },
        "bird_increment": {
            "estimate": grab(c, r"bird increment = \*\*([+-]?\d+\.\d+)\*\*", "structural null")[0],
            "ci95": grab(c, r"bird increment = [^\n]+\n- 95% CI = \*\*([+-]?\d+\.\d+) to ([+-]?\d+\.\d+)\*\*", "structural null"),
        },
        "permutation_null": {
            "median": grab(c, r"null median beta = \*\*([+-]?\d+\.\d+)\*\*", "permutation null")[0],
            "range_95": grab(c, r"null 2\.5.97\.5% interval = \*\*([+-]?\d+\.\d+) to ([+-]?\d+\.\d+)\*\*", "permutation null"),
            "n_permutations": 2000,
        },
    }
    if "INFORMATION_TO_TIMING_TRANSFER = NOT_SUPPORTED" not in b:
        raise ValueError("V8 transfer status changed")
    if "BIRD_INCREMENT_DETECTED = NO" not in c:
        raise ValueError("Structural null guard changed")

    p = deer["phase"]
    boot = deer["bootstrap"]
    actuator = deer["actuators"]
    if not (p["n"] == 152 and boot["unique_animals"] == 72
            and two["safe_joined_rows"] == 62 and two["safe_animals"] == 40):
        raise ValueError("Ortega source sample identity drift")
    mule = {
        "animal_years": p["n"],
        "animals": boot["unique_animals"],
        "start_abs_mean_days": p["mean_abs_start"],
        "end_abs_mean_days": p["mean_abs_end"],
        "variance_ratio": {
            "estimate": p["variance_ratio_end_over_start"],
            "ci95": boot["variance_ratio_ci95"],
        },
        "within_year_ratio": {
            "estimate": p["within_year_variance_ratio"],
            "ci95": boot["within_year_variance_ratio_ci95"],
        },
        "movement_rate": {
            "estimate": actuator["movement_rate_slope_per_DFP_day"],
            "ci95": boot["movement_rate_slope_ci95"],
            "n": actuator["movement_rate_n"],
            "within_year_estimate": actuator["movement_rate_within_year_slope"],
            "within_year_ci95": boot["movement_rate_within_year_slope_ci95"],
        },
        "stopover": {
            "estimate": actuator["stopover_slope_days_per_DFP_day"],
            "ci95": boot["stopover_slope_ci95"],
            "n": actuator["stopover_n"],
            "within_year_estimate": actuator["stopover_within_year_slope"],
            "within_year_ci95": boot["stopover_within_year_slope_ci95"],
        },
        "safe_subset": {
            "animal_years": two["safe_joined_rows"],
            "animals": two["safe_animals"],
            "condition_gate_supported": False,
        },
    }
    assert deer["source"]["source_data_sha256"] == two["source_sha256"]
    return {
        "environment": environmental,
        "transfer": transfer,
        "mule_deer": mule,
        "status": "FROZEN_SUMMARY_LEVEL_ONLY",
    }


def t(x: float, y: float, content: object, size: int = 17, weight="normal", color=INK, anchor="start") -> str:
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{color}" '
            f'font-family="Arial, Helvetica, sans-serif" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}">'
            f'{html.escape(str(content))}</text>')


def line(x1, y1, x2, y2, color=INK, width=2, dash="") -> str:
    dashed = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" '
            f'x2="{x2:.2f}" y2="{y2:.2f}" stroke="{color}" '
            f'stroke-width="{width}"{dashed}/>')


def rect(x, y, w, h, fill=LT, stroke=BLUE) -> str:
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
            f'rx="10" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')


def dot(x, y, color=BLUE, r=7) -> str:
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{color}"/>'


def svg(title: str, content: list[str], footer: str) -> str:
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" role="img">'
            f'<title>{html.escape(title)}</title>'
            '<rect width="100%" height="100%" fill="#fff"/>')
    return "\n".join([
        head, t(42, 52, title, 25, "bold"),
        line(42, 68, W-42, 68, GREY, 1),
        *content, line(42, H-62, W-42, H-62, GREY, 1),
        t(44, H-37, footer, 13, color=GREY), "</svg>",
    ]) + "\n"


def arrow(x0, y0, x1, y1, label="") -> list[str]:
    # Arrows are schematic; not measured causal effects.
    parts = [line(x0, y0, x1, y1, BLUE, 2)]
    tip = f'{x1:.1f},{y1:.1f} {x1-12:.1f},{y1-6:.1f} {x1-12:.1f},{y1+6:.1f}'
    parts.append(f'<polygon points="{tip}" fill="{BLUE}"/>')
    if label:
        parts.append(t((x0+x1)/2, y0-14, label, 13, color=GREY, anchor="middle"))
    return parts


def figure1() -> str:
    x_positions = [45, 325, 605, 885]
    labels = [("Entry/readiness", "tau sets initial phase e0"),
              ("Local/remote cue", "information at stage k"),
              ("Phase estimation", "signed expected error"),
              ("Timing control", "feasible action u_k")]
    ss = [t(50, 112, "A  Serial architecture (prospective mathematical model)", 19, "bold")]
    for x, (label, sub) in zip(x_positions, labels):
        ss += [rect(x, 145, 245, 100),
               t(x+12, 179, label, 19, "bold"),
               t(x+12, 209, sub, 13)]
    for a, b in zip(x_positions, x_positions[1:]):
        ss.extend(arrow(a+246, 196, b-8, 196))
    ss += [t(52, 319, "B  Interaction mismatch with two controllers", 19, "bold"),
           rect(48, 346, 1080, 100, "#f7f9fa", GREY),
           t(67, 390, "Propagated initial mismatch   +   unequal response to shared phase", 19, "bold"),
           t(67, 423, "Exact identity in main text and S4; centered, deterministic model only", 14, color=GREY),
           t(52, 506, "C  Three distinct reasons for a remaining seasonal gap", 19, "bold")]
    for i, label in enumerate(("Insufficient forecast", "Lost feasible options", "Costly optimal restraint")):
        xx = 50 + i * 370
        ss += [rect(xx, 537, 345, 54, "#f8f9fa", GREY),
               t(xx+14, 572, label, 16)]
    return svg("Figure 1. Information, commitment and seasonal control", ss,
               "Conceptual theory, not measured animal beliefs, physiological gates or fitness")


def make_axis(x0, x1, y0, scale_min, scale_max, ticks, label) -> list[str]:
    def coord(v): return x0 + (v - scale_min) / (scale_max - scale_min) * (x1-x0)
    parts = [line(x0, y0, x1, y0, GREY, 1.5)]
    for tick in ticks:
        x = coord(tick)
        parts += [line(x, y0-7, x, y0+7, GREY, 1),
                  t(x, y0+29, f"{tick:+.2f}", 13, anchor="middle")]
    parts.append(t((x0+x1)/2, y0+61, label, 15, anchor="middle"))
    if scale_min < 0 < scale_max:
        parts.append(line(coord(0), 128, coord(0), y0, GREY, 1, "5,6"))
    return parts


def forest_row(y, label, estimate, ci, x0, x1, lower, upper, extra="") -> list[str]:
    if not (lower <= ci[0] <= estimate <= ci[1] <= upper):
        raise ValueError(f"Invalid or out-of-domain CI for {label}")
    def coord(v): return x0 + (v-lower)/(upper-lower)*(x1-x0)
    xx, lo, hi = coord(estimate), coord(ci[0]), coord(ci[1])
    return [
        t(63, y+5, label, 16),
        line(lo, y, hi, y, BLUE, 4),
        line(lo, y-8, lo, y+8, BLUE, 2),
        line(hi, y-8, hi, y+8, BLUE, 2),
        dot(xx, y),
        t(936, y+5, f"{estimate:+.3f} [{ci[0]:+.3f}, {ci[1]:+.3f}]", 13),
        *([t(936, y+25, extra, 11, color=GREY)] if extra else []),
    ]


def figure2(environment: dict) -> str:
    ss = [t(50, 110, "Late (2010-2017) minus early (2002-2009)", 18),
          t(50, 150, "Environmental correlations, not bird-perceived forecasts", 15, color=GREY)]
    x0, x1 = 510, 920
    for y, label, key in [(280, "Unique spatial pairs (n=166)", "unique_pair"),
                          (410, "Equal-species exposure (n=28)", "equal_species")]:
        row = environment[key]
        ss.extend(forest_row(y, label, row["estimate"], row["ci95"],
                             x0, x1, -0.1, 0.6))
    ss += make_axis(x0, x1, 492, -0.1, 0.6, [-0.1,0,0.2,0.4,0.6],
                    "Change in signed detrended green-up correlation")
    ss += [t(55, 577, "Registered broad decline hypothesis: NOT SUPPORTED", 17, "bold")]
    return svg("Figure 2. Environmental predictive connectivity increased", ss,
               "95% pair-bootstrap CIs from frozen V8 summary receipts; no individual-route data")


def figure3(transfer: dict) -> str:
    ss=[t(48, 112, "Registered direction: negative (larger connectivity gain -> less mismatch)", 16),
        t(48, 143, "The opposite-sign point estimate is reproducible under structural nulls", 14, color=GREY)]
    lo,hi=-0.10,0.16
    x0,x1=486,888
    for y,label,key in [(246,"Observed registered transfer","primary"),
                        (344,"Fixed-arrival structural null","fixed_arrival_null"),
                        (442,"Observed minus fixed-arrival","bird_increment")]:
        v=transfer[key]
        ss.extend(forest_row(y,label,v["estimate"],v["ci95"],x0,x1,lo,hi))
    ss+=make_axis(x0,x1,510,lo,hi,[-0.10,-0.05,0,0.05,0.10,0.15],
                  "Weighted change-on-change slope (95% pair bootstrap CI)")
    v=transfer["permutation_null"]
    ss += [
        t(51,587,f'Permutation null: median {v["median"]:+.3f}; central 95% [{v["range_95"][0]:+.3f}, {v["range_95"][1]:+.3f}]',15),
        t(51,610,"Permutation limits summarize a null distribution, not a confidence interval.",13,color=GREY)
    ]
    return svg("Figure 3. A prespecified matching transfer was not supported",ss,
               "150 species-target rows; 72 unique pairs; 22 species; no causal bird response inferred")


def figure4(mule: dict) -> str:
    ss=[
       t(52,108,"A  Observed phase summaries",18,"bold"),
       t(65,157,"Mean absolute Days-From-Peak",15,color=GREY)
    ]
    longest=27.0
    for y,label,key in [(199,"Migration start","start_abs_mean_days"),
                        (257,"Migration end","end_abs_mean_days")]:
        v=mule[key]
        ss += [t(65,y+6,label,15), rect(250,y-17,310*v/longest,28,BLUE,BLUE),
               t(575,y+5,f"{v:.2f} d",15)]
    ss += [t(52,340,"B  Phase-variance ratio (end/start)",18,"bold")]
    x0,x1=320,800
    ss+=forest_row(397,"All animal-years",mule["variance_ratio"]["estimate"],
                   mule["variance_ratio"]["ci95"],x0,x1,0,1.1)
    ss+=forest_row(465,"Within-year centred",mule["within_year_ratio"]["estimate"],
                   mule["within_year_ratio"]["ci95"],x0,x1,0,1.1)
    ss+=make_axis(x0,x1,505,0,1.1,[0,0.25,0.5,0.75,1.0],
                  "Ratio; 1 means no variance change")
    ss += [t(55,590,f'n={mule["animal_years"]} animal-years from {mule["animals"]} deer; '
             f'{mule["safe_subset"]["animal_years"]} animal-years in the conservative readiness subset',13)]
    ss += [t(55,614,"Signed actuator slopes and unsupported readiness interaction are reported in the companion table.",12,color=GREY)]
    return svg("Figure 4. Seasonal phase narrows along the mule-deer migration",ss,
               "Descriptive reproduction of Ortega et al.; no individual trajectories or fitness effect")


LEGENDS = {
  "figure1": "Schematic serial architecture separating readiness, information, estimation and feasible timing correction. The two-actor mismatch identity is exact only in the specified linear no-innovation model. Neither the component gains nor the ecological incentives are estimated here.",
  "figure2": "Change in signed detrended source–destination mid-green-up correlation between 2002–2009 and 2010–2017. Points represent published frozen mean changes with pair-bootstrap 95% intervals. Environmental links are range-derived spatial proxies, not observed routes or perceived cues.",
  "figure3": "Preregistered species-equal transfer estimate, fixed-arrival structural null and observed-minus-null increment, all with pair-bootstrap 95% intervals. The permutation null is separately reported as its median and central 95% range. No biological worsening effect is inferred from the positive observed slope.",
  "figure4": "Descriptive reconstruction of Ortega et al. mule-deer phase convergence. Panel A shows means of absolute start/end phase, without invented uncertainty. Panel B shows end-to-start phase-variance ratios with animal-cluster bootstrap intervals. Neither panel identifies latent information/control gains or reproductive fitness effects.",
}


def write(path: Path, content: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = content.encode("utf-8")
    path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()


def build(output_dir: Path, root: Path = ROOT, archive: Path | None = None) -> dict:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError("Refusing to overwrite nonempty figure directory")
    contents, source_hashes = read_sources(root)
    inputs = extract_inputs(contents)
    svgs = [figure1(), figure2(inputs["environment"]),
            figure3(inputs["transfer"]), figure4(inputs["mule_deer"])]
    files = {}
    for i, output in enumerate(svgs, 1):
        name=f"figure{i}_summary.svg"
        files[name] = {"sha256":write(output_dir / name, output),
                       "kind":"SCHEMATIC" if i == 1 else "FROZEN_SUMMARY_ONLY"}

    legend_text = "# Figure legends — editorial preview only\n\n" + "\n\n".join(
        f"## Figure {i}\n\n{LEGENDS[f'figure{i}']}" for i in range(1,5)
    )+"\n"
    files["LEGENDS.md"]={"sha256":write(output_dir/"LEGENDS.md",legend_text),
                         "kind":"EDITORIAL_LEGENDS"}
    # Signed actuator slopes are available in a **separate** numerical
    # companion table; never draw raw deer trajectories without raw data.
    mule = inputs["mule_deer"]
    def fmt(est, ci):
        return f'{est:+.4f} [{ci[0]:+.4f}, {ci[1]:+.4f}]'
    table = (
        "# Table S1 — source-frozen mule-deer signed actuator summary\n\n"
        "Published-source descriptive associations only; not causal adjustment gains.\n\n"
        "| Response (units per starting DFP day) | n animal-years | Raw slope [95% animal-cluster CI] | Within-year-centred slope [95% CI] |\n"
        "|---|---:|---:|---:|\n"
        f"| Movement rate (km/day) | {mule['movement_rate']['n']} | "
        f"{fmt(mule['movement_rate']['estimate'],mule['movement_rate']['ci95'])} | "
        f"{fmt(mule['movement_rate']['within_year_estimate'],mule['movement_rate']['within_year_ci95'])} |\n"
        f"| Stopover duration (days) | {mule['stopover']['n']} | "
        f"{fmt(mule['stopover']['estimate'],mule['stopover']['ci95'])} | "
        f"{fmt(mule['stopover']['within_year_estimate'],mule['stopover']['within_year_ci95'])} |\n\n"
        "Source: data/payoff_b_ortega_variance_funnel_result_20261003.json; "
        "the published Ortega et al. findings are prior art. "
        "The separate 62-animal-year IFBFat readiness analysis is NOT included "
        "in these raw phase–actuator slopes; it did not support readiness-gated feedback.\n"
    )
    files["TABLE_S1_ACTUATORS.md"]={
        "sha256":write(output_dir/"TABLE_S1_ACTUATORS.md",table),
        "kind":"SOURCE_FROZEN_DESCRIPTIVE_COMPANION_TABLE"}

    manifest = {
        "status": "VERIFIED_SUMMARY_FIGURE_PREVIEW_SUBMISSION_HOLD",
        "individual_or_pair_level_points_generated": False,
        "underlying_observation_data_included": False,
        "new_fitted_biological_effects": False,
        "anonymous_review_archive_complete": False,
        "submission_ready": False,
        "figures": files,
        "read_only_source_receipts": source_hashes,
        "values": inputs,
        "scope": "four standalone deterministic SVG previews; not full data/code reproduction",
    }
    write(output_dir/"figure_manifest.json",
          json.dumps(manifest,indent=2,ensure_ascii=False,sort_keys=True)+"\n")
    if archive is not None:
        archive.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(archive,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for entry in sorted(output_dir.iterdir()):
                zi=zipfile.ZipInfo("summary_preview/"+entry.name,date_time=(2026,10,13,0,0,0))
                zi.create_system=3
                zi.external_attr=(0o644 & 0xffff)<<16
                zi.compress_type=zipfile.ZIP_DEFLATED
                z.writestr(zi,entry.read_bytes())
    return manifest


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,required=True)
    parser.add_argument("--zip",type=Path,default=None)
    args=parser.parse_args()
    m=build(args.out,archive=args.zip)
    print(json.dumps({"status":m["status"],"figures":len(
        [f for f in m["figures"] if f.endswith(".svg")]),
        "anonymous_review_archive_complete":False,"submission_ready":False}))


if __name__=="__main__":
    main()
