#!/usr/bin/env python3
"""Render the frozen PAYOFF-B tracking-theory figures as dependency-free SVG.

The renderer consumes only build_tracking_theory_figure_data(), which itself is
restricted to the five 2026-09-20 synthetic receipts. No empirical phase-
retention result enters these figures.
"""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

from build_tracking_theory_figure_data import build_figure_data


WIDTH = 1200
HEIGHT = 720
PAD = 72


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def text(x, y, value, size=22, weight="normal", anchor="start"):
    return (
        f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
        f'{esc(value)}</text>'
    )


def line(x1, y1, x2, y2, width=2, dash=None):
    extra = "" if dash is None else f' stroke-dasharray="{dash}"'
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="currentColor" stroke-width="{width}"{extra}/>'
    )


def circle(cx, cy, r=6, fill="white"):
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="currentColor" '
        f'stroke-width="2" fill="{fill}"/>'
    )


def rect(x, y, w, h, fill="white", stroke="currentColor", sw=2):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{sw}"/>'
    )


def svg_page(title, subtitle, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" '
        f'height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" color="#111">'
        '<rect width="100%" height="100%" fill="white"/>'
        f'{text(PAD, 48, title, 28, "bold")}'
        f'{text(PAD, 78, subtitle, 16)}'
        f'{body}'
        '</svg>\n'
    )


def axes(x0, y0, x1, y1, xlabel, ylabel):
    return "".join([
        line(x0, y1, x1, y1, 2),
        line(x0, y0, x0, y1, 2),
        text((x0+x1)/2, y1+48, xlabel, 17, anchor="middle"),
        text(x0-14, y0-18, ylabel, 17, anchor="start"),
    ])


def scale(value, lo, hi, start, end):
    if hi == lo:
        return (start + end) / 2
    return start + (value - lo) * (end - start) / (hi - lo)


def figure1(data):
    stages = [
        ("Local null", "movement + timing\nshare one restoring budget"),
        ("Finite timing", "temporal bypass\nhas a capacity ceiling"),
        ("Spatial re-entry", "movement returns\nunder stronger forcing"),
        ("Partner matching", "interaction synchronizes\ntracking allocation"),
        ("Coordination gate", "jointly good change\ncan be unilaterally bad"),
        ("Population outcome", "visibility peaks near\npersistence boundaries"),
        ("Finite N", "barrier crossing\n!= automatic rescue"),
    ]
    out = [
        text(72, 125, "Adaptive capacity is not the same as adaptive accessibility", 21, "bold"),
    ]
    x = 70
    y = 245
    w = 140
    gap = 22
    for i, (title, subtitle) in enumerate(stages):
        out.append(rect(x, y, w, 150, fill="#fafafa"))
        out.append(text(x+w/2, y+32, title, 15, "bold", "middle"))
        for j, row in enumerate(subtitle.split("\n")):
            out.append(text(x+w/2, y+70+j*24, row, 13, anchor="middle"))
        if i < len(stages)-1:
            out.append(line(x+w, y+75, x+w+gap-4, y+75, 2))
            out.append(text(x+w+gap/2, y+80, ">", 18, "bold", "middle"))
        x += w + gap
    out += [
        text(72, 470, "Mechanistic sequence frozen for the standalone synthetic tracking-theory paper.", 17),
        text(72, 505, "The GEB phase-retention programme is intentionally excluded from this evidence chain.", 16),
        text(72, 560, "Core estimand hierarchy:", 17, "bold"),
        text(72, 590, "tracking capacity != chosen architecture != coordinated value != unilateral accessibility != persistence", 16),
        text(72, 620, "barrier crossing != long-run payoff improvement", 16),
    ]
    return svg_page(
        "Figure 1. Tracking architecture from capacity to accessibility",
        "Conceptual synthesis of the frozen model hierarchy",
        "".join(out),
    )


def figure2(data):
    d = data["figure_2_temporal_bypass"]
    frontier = d["one_dimensional_frontier"]
    seq = d["two_dimensional_zmax4_sequence"]

    out = [text(72, 125, "A  Finite phenological capacity extends the persistence frontier", 19, "bold")]
    x0, x1, y0, y1 = 95, 560, 160, 560
    out.append(axes(x0, y0, x1, y1, "phenology limit", "climate velocity"))
    vmax = 0.075
    for tick in [0, 1, 2, 3, 4, 5]:
        x = scale(tick, 0, 5, x0, x1)
        out += [line(x, y1, x, y1+7), text(x, y1+28, tick, 14, anchor="middle")]
    for tick in [0.0, 0.02, 0.04, 0.06]:
        y = scale(tick, 0, vmax, y1, y0)
        out += [line(x0-7, y, x0, y), text(x0-12, y+5, f"{tick:.2f}", 14, anchor="end")]

    max_pts, fail_pts = [], []
    for row in frontier:
        x = scale(row["phenology_limit"], 0, 5, x0, x1)
        ym = scale(row["max_persisted_velocity"], 0, vmax, y1, y0)
        yf = scale(row["first_failed_velocity"], 0, vmax, y1, y0)
        max_pts.append((x, ym)); fail_pts.append((x, yf))
    for pts, dash in [(max_pts, None), (fail_pts, "8 6")]:
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            out.append(line(xa, ya, xb, yb, 3, dash))
        for x, y in pts:
            out.append(circle(x, y, 6))
    out += [
        text(115, 190, "solid = max persisted", 14),
        text(115, 212, "dashed = first failed", 14),
    ]

    out.append(text(650, 125, "B  Temporal bypass, then spatial re-entry", 19, "bold"))
    bx0, bx1, by0, by1 = 680, 1125, 180, 555
    out.append(axes(bx0, by0, bx1, by1, "climate velocity", "tracking rate"))
    for tick in [0.04, 0.05, 0.06, 0.07]:
        x = scale(tick, 0.04, 0.07, bx0, bx1)
        out += [line(x, by1, x, by1+7), text(x, by1+28, f"{tick:.2f}", 14, anchor="middle")]
    for tick in [0, 0.1, 0.2, 0.3, 0.4]:
        y = scale(tick, 0, 0.4, by1, by0)
        out += [line(bx0-7, y, bx0, y), text(bx0-12, y+5, f"{tick:.1f}", 14, anchor="end")]
    mpts, hpts = [], []
    for row in seq:
        x = scale(row["velocity"], 0.04, 0.07, bx0, bx1)
        mpts.append((x, scale(row["migration"], 0, 0.4, by1, by0)))
        hpts.append((x, scale(row["phenology"], 0, 0.4, by1, by0)))
    for pts, dash in [(mpts, None), (hpts, "8 6")]:
        for a, b in zip(pts, pts[1:]):
            out.append(line(a[0], a[1], b[0], b[1], 3, dash))
        for x, y in pts:
            out.append(circle(x, y, 6))
    out += [
        text(700, 210, "solid = migration", 14),
        text(700, 232, "dashed = phenology", 14),
        text(680, 625, "Timing buffers movement demand at v=0.04–0.05; migration re-enters by v=0.06.", 16),
        text(680, 648, f"Zigzag growth-penalty magnitude reduction at zmax=4: {100*d['zigzag_penalty_reduction']:.1f}%.", 16),
    ]
    return svg_page(
        "Figure 2. Finite temporal bypass and spatial re-entry",
        "Frozen synthetic receipts only (2026-09-20)",
        "".join(out),
    )


def figure3(data):
    d = data["figure_3_coordination_gate"]
    g = d["direct_gate"]
    out = [
        text(72, 125, "A  One-step coordination gate", 19, "bold"),
        text(72, 162, f"Resident strategy: {g['resident_strategy']}", 17),
        text(72, 188, f"Coordinated adjacent strategy: {g['coordinated_strategy']}", 17),
    ]
    vals = [
        ("resident joint growth", g["resident_joint_growth"]),
        ("coordinated joint growth", g["coordinated_joint_growth"]),
        ("coordinated gain", g["coordinated_gain"]),
        ("unilateral gain A", g["unilateral_gain_a"]),
        ("unilateral gain B", g["unilateral_gain_b"]),
    ]
    x0, x1, base = 390, 1110, 330
    lo, hi = -6.5, 1.5
    zero = scale(0, lo, hi, x0, x1)
    out += [line(x0, base, x1, base), line(zero, 225, zero, 570, 2, "6 5")]
    for i, (name, val) in enumerate(vals):
        y = 255 + i*63
        xv = scale(val, lo, hi, x0, x1)
        left, width = min(zero, xv), abs(xv-zero)
        out += [
            text(72, y+7, name, 16),
            rect(left, y-16, max(width, 1), 28, fill="#eeeeee"),
            text(xv + (8 if val >= 0 else -8), y+6, f"{val:+.3f}", 15, "bold", "start" if val >= 0 else "end"),
        ]
    out += [
        text(72, 610, f"Fine 2D positive-interaction cells: {d['barriers']}/{d['positive_interaction_cells']} barriers; "
             f"{d['persistence_rescues']}/{d['positive_interaction_cells']} persistence rescues.", 16),
        text(72, 640, "The same adjacent timing shift is beneficial jointly but strongly deleterious unilaterally.", 16, "bold"),
    ]
    return svg_page(
        "Figure 3. Coordinated value is not unilateral accessibility",
        "Direct gate from the frozen 2D coevolution receipt",
        "".join(out),
    )


def figure4(data):
    d = data["figure_4_synchronization"]
    moderate = d["moderate_velocity_0_04"]
    strong = d["strong_velocity_0_06"]
    out = [text(72, 125, "A  Moderate forcing (v=0.04)", 19, "bold")]
    groups = [("I=0", moderate["interaction_0"]), ("I=0.5", moderate["interaction_0_5"]), ("I=1", moderate["interaction_1"])]
    x = 90
    for label, row in groups:
        out += [
            rect(x, 180, 300, 160, fill="#fafafa"),
            text(x+18, 210, label, 18, "bold"),
            text(x+18, 244, f"persisted: {row['persisted']}", 17),
            text(x+18, 278, f"mean strategy distance: {row['mean_strategy_distance']:.3f}", 16),
        ]
        if "mean_interaction_mismatch" in row:
            out.append(text(x+18, 310, f"mean mismatch: {row['mean_interaction_mismatch']:.4f}", 15))
        x += 355
    out += [
        text(72, 380, "Interaction collapses partner strategy distance to zero while persistence remains possible.", 17, "bold"),
        text(72, 430, "B  Strong forcing (v=0.06)", 19, "bold"),
    ]
    groups2 = [("I=0", strong["interaction_0"]), ("I=0.5", strong["interaction_0_5"]), ("I=1", strong["interaction_1"])]
    x = 90
    for label, row in groups2:
        out += [
            rect(x, 465, 300, 145, fill="#fafafa"),
            text(x+18, 495, label, 18, "bold"),
            text(x+18, 530, f"persisted: {row['persisted']}", 17),
            text(x+18, 565, row["endpoint"], 14),
        ]
        x += 355
    out.append(text(72, 655, "The same matching interaction becomes a maladaptive synchronization lock under stronger forcing.", 17, "bold"))
    return svg_page(
        "Figure 4. Interaction-mediated synchronization changes ecological sign",
        "Partner-asymmetry experiment, frozen 2026-09-20",
        "".join(out),
    )


def figure5(data):
    d = data["figure_5_demography_and_drift"]
    examples = d["replication_128"]["visibility_examples"]
    drift = d["drift_beta_5"]
    out = [text(72, 125, "A  Demographic visibility window", 19, "bold")]
    x0, x1, y0, y1 = 95, 555, 165, 520
    out.append(axes(x0, y0, x1, y1, "local persistence", "matched - local persistence"))
    for row in examples:
        x = scale(row["local"], 0, 1, x0, x1)
        y = scale(row["gain"], 0, 0.025, y1, y0)
        out.append(circle(x, y, 7, "#eeeeee"))
    out += [
        text(100, 552, f"mean gain near transition (0.3–0.7): {d['replication_128']['local_persistence_bin_0_3_to_0_7']['mean_persistence_gain']:.4f}", 14),
        text(100, 574, f"mean gain in safe regime (0.9–1): {d['replication_128']['local_persistence_bin_0_9_to_1_0']['mean_persistence_gain']:.4f}", 14),
        text(100, 596, f"pilot cells >=0.10: {d['pilot_ge_0_10']}; replication cells >=0.10: {d['replication_ge_0_10']}", 14),
    ]

    out.append(text(650, 125, "B  Drift-assisted crossing is not drift rescue", 19, "bold"))
    bx0, bx1, by0, by1 = 690, 1120, 165, 520
    out.append(axes(bx0, by0, bx1, by1, "population size N (log-spaced positions)", "escape fraction"))
    ns = [row["N"] for row in drift]
    positions = {n: bx0 + i*(bx1-bx0)/(len(ns)-1) for i, n in enumerate(ns)}
    pts = []
    for row in drift:
        x = positions[row["N"]]
        y = scale(row["escape_fraction"], 0, 1, by1, by0)
        pts.append((x, y))
        out += [circle(x, y, 7), text(x, by1+28, row["N"], 13, anchor="middle")]
    for a,b in zip(pts,pts[1:]):
        out.append(line(a[0],a[1],b[0],b[1],3))
    local_growth = 0.340292788918
    out += [
        text(690, 558, f"deterministic local joint growth: {local_growth:.3f}", 14),
        text(690, 580, "N=10 and 30 cross frequently, but their mean long-run joint growth is lower.", 14),
        text(690, 615, "Crossing probability and evolutionary rescue are distinct estimands.", 16, "bold"),
    ]
    return svg_page(
        "Figure 5. Barrier visibility and finite-population crossing",
        "Frozen higher-replication demographic result retained; pilot large effects rejected",
        "".join(out),
    )


def figure6(data):
    d = data["figure_6_local_null_vs_landscape"]
    exact = d["closed_loop_exact"]
    high = d["high_forcing_persistence"]
    fixed = d["fixed_gain_1_6"]["v_0_06"]
    out = [
        text(72, 125, "A  Exact local null", 19, "bold"),
        rect(80, 165, 470, 250, fill="#fafafa"),
        text(105, 205, exact["recurrence"], 18, "bold"),
        text(105, 245, f"total restoring gain: {exact['total_feedback_gain']}", 17),
        text(105, 285, f"stability: {exact['stability']}", 17),
        text(105, 325, "At fixed K, movement and timing are exactly substitutable.", 17),
        text(105, 365, "Costs only determine how K is allocated between channels.", 16),
        text(640, 125, "B  Explicit landscape at strong forcing", 19, "bold"),
        rect(630, 165, 500, 250, fill="#fafafa"),
        text(655, 205, "v = 0.06", 18, "bold"),
        text(655, 242, f"h=0: {high['v_0_06']['h_0']}", 17),
        text(655, 278, f"h=0.25: {high['v_0_06']['h_0_25']}", 17),
        text(655, 314, f"h=0.5: {high['v_0_06']['h_0_5']}", 17),
        text(655, 360, "Finite route mechanics break the local equivalence.", 17, "bold"),
        text(72, 475, "C  Timing unloads movement-controller demand at fixed movement-feedback gain = 1.6", 19, "bold"),
    ]
    rows=[("h=0",fixed["h_0"]),("h=0.25",fixed["h_0_25"]),("h=0.5",fixed["h_0_5"])]
    x=95
    for label,row in rows:
        out += [
            rect(x, 510, 315, 125, fill="#fafafa"),
            text(x+16, 540, label, 17, "bold"),
            text(x+16, 570, f"mean effective m = {row['mean_migration']:.3f}", 15),
            text(x+16, 595, f"growth = {row['growth']:+.3f}", 15),
            text(x+16, 620, f"persisted = {row['persisted']}", 15),
        ]
        x+=350
    out.append(text(72, 680, "Local substitutability becomes forcing-dependent complementarity once finite capacities and spatial mechanics are restored.", 16, "bold"))
    return svg_page(
        "Figure 6. From local substitutability to explicit-landscape complementarity",
        "Closed-loop theorem versus frozen movement-feedback landscape",
        "".join(out),
    )


def render_all(output_dir: Path) -> dict:
    data = build_figure_data()
    output_dir.mkdir(parents=True, exist_ok=True)
    figures = {
        "figure_1": ("PAYOFF_B_TRACKING_FIG1_CONCEPT.svg", figure1(data)),
        "figure_2": ("PAYOFF_B_TRACKING_FIG2_TEMPORAL_BYPASS.svg", figure2(data)),
        "figure_3": ("PAYOFF_B_TRACKING_FIG3_COORDINATION_GATE.svg", figure3(data)),
        "figure_4": ("PAYOFF_B_TRACKING_FIG4_SYNCHRONIZATION.svg", figure4(data)),
        "figure_5": ("PAYOFF_B_TRACKING_FIG5_DEMOGRAPHY_DRIFT.svg", figure5(data)),
        "figure_6": ("PAYOFF_B_TRACKING_FIG6_COMPLEMENTARITY.svg", figure6(data)),
    }
    manifest = {
        "status": "payoff_b_tracking_theory_rendered_figures",
        "frozen_date": data["frozen_date"],
        "source_policy": data["source_policy"],
        "figures": {},
    }
    for key, (name, svg) in figures.items():
        path = output_dir / name
        path.write_text(svg, encoding="utf-8")
        manifest["figures"][key] = {
            "path": str(path),
            "format": "svg",
            "bytes": path.stat().st_size,
        }
    manifest_path = output_dir / "PAYOFF_B_TRACKING_FIGURE_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("submission/tracking_theory_figures"),
    )
    args = parser.parse_args()
    manifest = render_all(args.output_dir)
    print(args.output_dir / "PAYOFF_B_TRACKING_FIGURE_MANIFEST.json")
    print(
        "tracking_theory_figures "
        f"count={len(manifest['figures'])} "
        f"frozen_date={manifest['frozen_date']}"
    )


if __name__ == "__main__":
    main()
