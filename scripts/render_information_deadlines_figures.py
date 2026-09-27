#!/usr/bin/env python3
"""Render the six PAYOFF-B information-deadlines figures from frozen sources.

Dependency-free SVG renderer. Quantitative panels consume frozen result JSONs or
exact model functions already committed in the repository. No Aikens outcome is
used.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from src.endogenous_information_timing import (  # noqa: E402
    InformationTimingScenario,
    evaluate_information_timing,
    expected_shared_cue_action_mismatch,
)
from src.information_rescue_coalition import (  # noqa: E402
    minimum_pinned_rescue_coalitions,
    minimum_self_financing_coalitions,
    pinned_rescue,
)
from src.shared_cue_deadline_network import (  # noqa: E402
    canonical_shared_cue_deadline_game,
)
from build_tracking_theory_figure_data import build_figure_data  # noqa: E402
from render_tracking_theory_figures import (  # noqa: E402
    axes,
    circle,
    figure2 as legacy_capacity_figure,
    line,
    rect,
    scale,
    svg_page,
    text,
    wrap_words,
)


DATA = ROOT / "data"
WIDTH = 1200
HEIGHT = 720


def load_json(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def arrow(x1, y1, x2, y2):
    body = line(x1, y1, x2, y2, 2)
    if abs(x2 - x1) >= abs(y2 - y1):
        direction = 1 if x2 >= x1 else -1
        head = (
            f'<polygon points="{x2},{y2} '
            f'{x2-12*direction},{y2-7} '
            f'{x2-12*direction},{y2+7}" fill="black"/>'
        )
    else:
        direction = 1 if y2 >= y1 else -1
        head = (
            f'<polygon points="{x2},{y2} '
            f'{x2-7},{y2-12*direction} '
            f'{x2+7},{y2-12*direction}" fill="black"/>'
        )
    return body + head


def polyline(points, width=3, dash=None):
    return "".join(
        line(a[0], a[1], b[0], b[1], width, dash)
        for a, b in zip(points, points[1:])
    )


def figure1():
    anchor = load_json(
        "payoff_b_flycatcher_social_information_anchor_20260926.json"
    )
    qs = [0.50 + 0.01 * i for i in range(51)]
    private, joint = [], []
    for q in qs:
        scenario = InformationTimingScenario(
            prior_early=0.40,
            cue_accuracy_after_wait=q,
            false_early_cost=2.0,
            missed_early_cost=1.0,
            partner_false_early_externality=1.0,
            partner_missed_early_externality=1.0,
        )
        d = evaluate_information_timing(scenario, delay_cost=0.40)
        private.append(d.private_information_value)
        joint.append(d.joint_information_value)

    out = [
        text(72, 125, "(a) Value of waiting for information", 19, "bold"),
    ]
    x0, x1, y0, y1 = 95, 610, 165, 550
    out.append(axes(x0, y0, x1, y1, "cue accuracy q", "value / delay cost"))
    for tick in [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        x = scale(tick, 0.5, 1.0, x0, x1)
        out += [
            line(x, y1, x, y1 + 7),
            text(x, y1 + 28, f"{tick:.1f}", 13, anchor="middle"),
        ]
    for tick in [0.0, 0.2, 0.4, 0.6, 0.8]:
        y = scale(tick, 0.0, 0.8, y1, y0)
        out += [
            line(x0 - 7, y, x0, y),
            text(x0 - 12, y + 5, f"{tick:.1f}", 13, anchor="end"),
        ]
    ppts, jpts = [], []
    for q, pv, jv in zip(qs, private, joint):
        x = scale(q, 0.5, 1.0, x0, x1)
        ppts.append((x, scale(pv, 0.0, 0.8, y1, y0)))
        jpts.append((x, scale(jv, 0.0, 0.8, y1, y0)))
    out += [
        polyline(ppts, 3),
        polyline(jpts, 3, "8 6"),
    ]
    delay_y = scale(0.40, 0.0, 0.8, y1, y0)
    out += [
        line(x0, delay_y, x1, delay_y, 2, "3 5"),
        text(118, 195, "solid = private information value", 13),
        text(118, 217, "dashed = joint information value", 13),
        text(118, 239, "dotted = example delay cost D = 0.40", 13),
        text(108, 515, "At q=0.90: private=0.24, joint=0.54", 14, "bold"),
    ]

    out += [
        text(680, 125, "(b) Information becomes available after an early decision", 19, "bold"),
        rect(680, 170, 440, 150, fill="#fafafa"),
        text(700, 202, "Earlier male settlement", 17, "bold"),
        text(700, 232, "tit-timing treatment: no detectable settlement effect", 14),
        text(
            700,
            258,
            f"Z={anchor['published_results']['male_settlement_treatment_effect']['z']:.3f}; "
            f"p={anchor['published_results']['male_settlement_treatment_effect']['p']:.3f}",
            14,
        ),
        text(700, 286, "most males settled before manipulated hatching was visible", 13),
        arrow(900, 320, 900, 370),
        rect(680, 370, 440, 190, fill="#fafafa"),
        text(700, 402, "Later female settlement / pairing", 17, "bold"),
        text(700, 432, "resident phenology becomes behaviorally relevant", 14),
        text(
            700,
            458,
            f"pairing GLMM: p={anchor['published_results']['male_pairing_glmm']['tit_timing_p']:.3f}",
            14,
        ),
        text(
            700,
            484,
            f"time-dependent Cox: p<{anchor['published_results']['female_settlement_cox']['p_less_than']:.3f}",
            14,
        ),
        text(700, 522, "Anchor: cue availability depends on decision timing.", 14, "bold"),
        text(72, 650, "Private incentives can favor acting before information that would benefit the interaction system becomes available.", 16, "bold"),
    ]
    return svg_page(
        "Figure 1. Useful information can arrive after the decision deadline",
        "Exact value-of-waiting model plus source-backed flycatcher experiment",
        "".join(out),
    )


def figure2():
    result = load_json(
        "payoff_b_endogenous_information_timing_result_20260926.json"
    )
    witness = result["endogenous_information_asymmetry_witness"]
    qs = [0.50 + 0.01 * i for i in range(51)]
    vals = []
    for q in qs:
        scenario = InformationTimingScenario(
            prior_early=0.40,
            cue_accuracy_after_wait=q,
            false_early_cost=2.0,
            missed_early_cost=1.0,
        )
        vals.append(
            expected_shared_cue_action_mismatch(
                scenario,
                actor_a_delay_cost=witness["early_actor_delay_cost"],
                actor_b_delay_cost=witness["late_actor_delay_cost"],
            )
        )

    out = [text(72, 125, "Expected mismatch under one monotonically improving shared cue", 19, "bold")]
    x0, x1, y0, y1 = 105, 1115, 170, 555
    out.append(axes(x0, y0, x1, y1, "cue accuracy q", "expected action mismatch"))
    for tick in [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        x = scale(tick, 0.5, 1.0, x0, x1)
        out += [line(x, y1, x, y1 + 7), text(x, y1 + 29, f"{tick:.1f}", 14, anchor="middle")]
    for tick in [0.0, 0.1, 0.2, 0.3, 0.4]:
        y = scale(tick, 0.0, 0.46, y1, y0)
        out += [line(x0 - 7, y, x0, y), text(x0 - 12, y + 5, f"{tick:.1f}", 14, anchor="end")]
    pts = [
        (
            scale(q, 0.5, 1.0, x0, x1),
            scale(v, 0.0, 0.46, y1, y0),
        )
        for q, v in zip(qs, vals)
    ]
    out.append(polyline(pts, 4))
    for q in [0.82, 0.94]:
        x = scale(q, 0.5, 1.0, x0, x1)
        out.append(line(x, y0, x, y1, 2, "5 5"))
        out.append(text(x, y0 - 12, f"q={q:.2f}", 14, "bold", "middle"))
    peak = result["information_induced_desynchronization"]
    px = scale(peak["peak_mismatch_accuracy"], 0.5, 1.0, x0, x1)
    py = scale(peak["peak_mismatch_probability"], 0.0, 0.46, y1, y0)
    out += [
        circle(px, py, 7, "#eeeeee"),
        text(px + 14, py - 12, f"peak={peak['peak_mismatch_probability']:.3f}", 14, "bold"),
        text(175, 615, "shared ignorance", 16, "bold", "middle"),
        text(600, 615, "asymmetric cue use", 16, "bold", "middle"),
        text(1010, 615, "shared informed response", 16, "bold", "middle"),
        text(72, 665, "Better information is not monotonically better coordination when partners cross waiting thresholds asynchronously.", 16, "bold"),
    ]
    return svg_page(
        "Figure 2. Improving information can transiently worsen coordination",
        "Same cue, unequal waiting costs: D_A=0.30 and D_B=0.10",
        "".join(out),
    )


def network_icon(cx, cy, topology):
    pts = {
        "flower": (cx - 80, cy),
        "pollinator": (cx, cy - 65),
        "migrant": (cx + 80, cy),
    }
    if topology == "complete":
        edges = [("flower", "pollinator"), ("pollinator", "migrant"), ("flower", "migrant")]
    elif topology == "chain":
        edges = [("flower", "pollinator"), ("pollinator", "migrant")]
    else:
        edges = [("flower", "migrant"), ("pollinator", "migrant")]
    out = []
    for a, b in edges:
        out.append(line(*pts[a], *pts[b], 2))
    for name, (x, y) in pts.items():
        out.append(circle(x, y, 17, "#fafafa"))
        out.append(text(x, y + 5, name[0].upper(), 12, "bold", "middle"))
    return "".join(out)


def figure3():
    d = load_json("payoff_b_bayesian_strict_phase_diagram_20260926.json")
    order = ["complete", "chain", "migrant_star"]
    labels = {"complete": "complete", "chain": "chain", "migrant_star": "migrant-star"}
    out = [text(72, 125, "(a) Shock transmission versus strict ecological memory", 19, "bold")]
    x0, x1, y0, y1 = 100, 650, 190, 550
    out.append(axes(x0, y0, x1, y1, "network topology", "fraction of eligible cells"))
    xpos = [190, 370, 550]
    for x, key in zip(xpos, order):
        row = d["results"][key]
        cascade = row["resident_cascade"] / row["eligible"]
        strict = row["strict_inefficient_hysteresis"] / row["eligible"]
        yc = scale(cascade, 0.0, 1.0, y1, y0)
        ys = scale(strict, 0.0, 1.0, y1, y0)
        out += [
            rect(x - 42, yc, 34, y1 - yc, fill="#e8e8e8"),
            rect(x + 8, ys, 34, y1 - ys, fill="#bdbdbd"),
            text(x, y1 + 28, labels[key], 13, anchor="middle"),
            text(x - 25, yc - 8, f"{cascade:.2f}", 12, anchor="middle"),
            text(x + 25, ys - 8, f"{strict:.2f}", 12, "bold", "middle"),
        ]
    out += [
        text(115, 175, "left bar = resident cascade", 13),
        text(350, 175, "right bar = strict lower-payoff hysteresis", 13),
    ]

    out += [text(710, 125, "(b) Same edge count, different memory", 19, "bold")]
    out.append(network_icon(830, 270, "chain"))
    out.append(text(830, 380, "chain", 16, "bold", "middle"))
    out.append(text(830, 410, "52 / 364 strict-memory cells", 14, anchor="middle"))
    out.append(network_icon(1030, 270, "migrant_star"))
    out.append(text(1030, 380, "migrant-star", 16, "bold", "middle"))
    out.append(text(1030, 410, "0 / 404 strict-memory cells", 14, anchor="middle"))
    out += [
        text(730, 480, "Both sparse networks can transmit the migrant information shock.", 14),
        text(730, 510, "Only the chain stores a broad strict historical state.", 14, "bold"),
        text(72, 650, "Edge placement determines whether an information shock disappears or becomes ecological timing memory.", 16, "bold"),
    ]
    return svg_page(
        "Figure 3. Interaction topology determines whether information shocks are stored",
        "Strict phase-diagram audit excludes tie-supported recovery states",
        "".join(out),
    )


def ci_row(out, x0, x1, y, label, estimate, low, high, *, lo=-0.18, hi=0.08, bold=False):
    zero = scale(0, lo, hi, x0, x1)
    xl = scale(low, lo, hi, x0, x1)
    xh = scale(high, lo, hi, x0, x1)
    xe = scale(estimate, lo, hi, x0, x1)
    out += [
        text(72, y + 5, label, 13, "bold" if bold else "normal"),
        line(xl, y, xh, y, 3),
        line(zero, y - 15, zero, y + 15, 1, "4 4"),
        circle(xe, y, 6, "#eeeeee"),
        text(x1 + 15, y + 5, f"{estimate:+.3f} [{low:+.3f}, {high:+.3f}]", 12),
    ]


def figure4():
    d = load_json("payoff_b_broad_predictive_connectivity_result_20260926.json")
    out = [text(72, 125, "Registered coefficient and robustness boundaries", 19, "bold")]
    x0, x1 = 420, 900
    lo, hi = -0.18, 0.08
    zero = scale(0, lo, hi, x0, x1)
    out += [line(x0, 570, x1, 570), line(zero, 160, zero, 570, 2, "5 5")]
    for tick in [-0.15, -0.10, -0.05, 0.0, 0.05]:
        x = scale(tick, lo, hi, x0, x1)
        out += [line(x, 570, x, 578), text(x, 600, f"{tick:+.2f}", 12, anchor="middle")]

    p = d["preregistered_primary"]
    rows = [
        ("8-y detrended primary", p["coefficient"], p["ci_low_95"], p["ci_high_95"], True),
    ]
    for row in d["window_and_definition_sensitivity"]:
        if row.get("gaussian_q_bridge"):
            label = "Gaussian-q bridge"
        elif not row.get("detrended"):
            label = "8-y raw correlation"
        else:
            label = f"{row['window_years']}-y detrended"
        if label == "8-y detrended":
            continue
        rows.append((label, row["coefficient"], row["ci_low_95"], row["ci_high_95"], False))
    y = 190
    for row in rows:
        ci_row(out, x0, x1, y, row[0], row[1], row[2], row[3], lo=lo, hi=hi, bold=row[4])
        y += 52

    dep = d["dependency_audit"]
    cluster_map = {
        "cluster: species": dep["one_way_cluster_ci"]["species"],
        "cluster: source-target": dep["one_way_cluster_ci"]["source_target_pair"],
        "species summary": [
            dep["within_species"]["inverse_variance_fixed_summary"]["ci_low_95"],
            dep["within_species"]["inverse_variance_fixed_summary"]["ci_high_95"],
        ],
    }
    est_map = {
        "cluster: species": dep["fixed_effect_estimate"],
        "cluster: source-target": dep["fixed_effect_estimate"],
        "species summary": dep["within_species"]["inverse_variance_fixed_summary"]["estimate"],
    }
    for label, interval in cluster_map.items():
        ci_row(out, x0, x1, y, label, est_map[label], interval[0], interval[1], lo=lo, hi=hi)
        y += 52

    out += [
        text(72, 635, f"{d['sample']['analysis_rows']:,} rows; {d['sample']['species']} species; "
             f"{d['dependency_audit']['leave_one_species_out']['negative_fraction']*100:.0f}% leave-one-species-out coefficients negative.", 14),
        text(72, 663, "Pooled direction is stable, but dependence-aware intervals cross zero.", 15, "bold"),
    ]
    return svg_page(
        "Figure 4. Pre-outcome predictive connectivity is associated with lower mismatch",
        "Broad migratory-bird analysis: pooled support with dependence-sensitive uncertainty",
        "".join(out),
    )


def figure5():
    w = load_json("payoff_b_wigeon_predictive_connectivity_result_20260926.json")
    c = load_json("payoff_b_cv24c_cue_driver_result_20260927.json")
    fly = load_json("payoff_b_flycatcher_social_information_anchor_20260926.json")
    out = [
        text(72, 125, "(a) Post-error correction: wigeon registered prediction not supported", 18, "bold"),
    ]
    x0, x1, y = 180, 600, 255
    lo, hi = -0.18, 0.18
    zero = scale(0, lo, hi, x0, x1)
    p = w["primary_interaction"]
    xl = scale(p["ci_low_95"], lo, hi, x0, x1)
    xh = scale(p["ci_high_95"], lo, hi, x0, x1)
    xe = scale(p["estimate"], lo, hi, x0, x1)
    out += [
        line(x0, y, x1, y),
        line(zero, y - 75, zero, y + 75, 2, "5 5"),
        line(xl, y, xh, y, 4),
        circle(xe, y, 8, "#eeeeee"),
        text(190, 195, "registered direction: negative", 13),
        text(190, 320, f"estimate={p['estimate']:+.3f}; 95% CI [{p['ci_low_95']:+.3f}, {p['ci_high_95']:+.3f}]", 13),
        text(190, 345, f"p={p['p_value_two_sided']:.3f}", 13),
    ]

    out += [
        text(665, 125, "(b) Long-term cue-driver path: gate fails before hysteresis test", 18, "bold"),
        rect(680, 170, 430, 205, fill="#fafafa"),
        text(705, 205, f"best segmented change: {c['frozen_reversal_gate']['best_segmented']['break_year']}", 15, "bold"),
        text(705, 237, f"pre slope = {c['frozen_reversal_gate']['best_segmented']['left_slope']:+.4f}", 14),
        text(705, 265, f"post slope = {c['frozen_reversal_gate']['best_segmented']['right_slope']:+.4f}", 14),
        text(705, 293, f"ΔAICc = {c['frozen_reversal_gate']['best_segmented']['delta_aicc_vs_linear']:.2f}", 14),
        text(705, 328, "required pre-break decline: FAIL", 15, "bold"),
        text(705, 353, "history model: NOT RUN", 15, "bold"),
        text(72, 435, "(c) Decision-time anchor", 18, "bold"),
        rect(80, 470, 1030, 105, fill="#fafafa"),
        text(105, 503, "Flycatcher manipulation:", 15, "bold"),
        text(270, 503, "early male settlement before cue visibility → no treatment response", 14),
        text(270, 532, "later female settlement after cue visibility → treatment response", 14),
        text(105, 555, "These are distinct informational positions, not one generic tracking coefficient.", 14, "bold"),
        text(72, 645, "Predictive information before commitment, cue availability at settlement and correction after error appears are empirically separable.", 15, "bold"),
    ]
    return svg_page(
        "Figure 5. Prediction, decision-time information and correction are different axes",
        "Registered negative evidence is retained rather than retuned",
        "".join(out),
    )


def figure6():
    data = build_figure_data()
    svg = legacy_capacity_figure(data)
    svg = svg.replace(
        "Figure 2. Finite temporal bypass and spatial re-entry",
        "Figure 6. Capacity is a separate barrier: temporal bypass and spatial re-entry",
        1,
    )
    svg = svg.replace(
        "A  Finite phenological capacity extends the persistence frontier",
        "(a) Finite phenological capacity extends the persistence frontier",
        1,
    )
    svg = svg.replace(
        "B  Temporal bypass, then spatial re-entry",
        "(b) Temporal bypass, then spatial re-entry",
        1,
    )
    return svg



def figure7():
    topologies = ("complete", "chain", "migrant_star")
    labels = {
        "complete": "complete",
        "chain": "chain",
        "migrant_star": "migrant-star",
    }
    out = [
        text(72, 120, "Recovery leverage after perfect-information lock-in", 20, "bold"),
        text(
            72,
            150,
            "Temporary cue use can nucleate a self-sustaining return to the informed equilibrium.",
            14,
        ),
    ]

    x_centers = [235, 600, 965]
    for x, topology in zip(x_centers, topologies):
        game = canonical_shared_cue_deadline_game(
            1.0,
            interaction_topology=topology,
        )
        voluntary = minimum_self_financing_coalitions(game)
        pinned = minimum_pinned_rescue_coalitions(game)
        voluntary_size = len(voluntary[0].members) if voluntary else None
        seed_names = [
            row.pinned_names[0]
            for row in pinned
            if len(row.pinned_members) == 1
        ]

        out.append(network_icon(x, 285, topology))
        out.append(text(x, 395, labels[topology], 17, "bold", "middle"))
        out.append(
            text(
                x,
                430,
                f"minimum voluntary coalition: {voluntary_size if voluntary_size is not None else 'none'}",
                13,
                anchor="middle",
            )
        )

        if seed_names:
            if topology == "chain":
                seed_text = "singleton rescue: local pollinator only"
            else:
                seed_text = "singleton rescue: any actor"
        else:
            seed_text = "singleton rescue: none"
        out.append(text(x, 462, seed_text, 13, "bold", "middle"))

        y = 505
        for i, player in enumerate(game.players):
            result = pinned_rescue(game, (i,))
            status = "rescues" if result.persists_after_release else "fails"
            out.append(
                text(
                    x,
                    y,
                    f"{player.name}: {status}",
                    12,
                    anchor="middle",
                )
            )
            y += 25

    out += [
        text(
            72,
            635,
            "Trap stability and rescue leverage are different network properties.",
            16,
            "bold",
        ),
        text(
            72,
            663,
            "In the chain, only the central local pollinator is a one-species rescue seed; either peripheral actor fails.",
            14,
        ),
    ]
    return svg_page(
        "Figure 7. Network position determines minimum rescue intervention",
        "Exact temporary-seed recovery result at perfect cue accuracy",
        "".join(out),
    )


def sha256(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_all(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    payloads = {
        "figure_1": ("PAYOFF_B_INFO_V2_FIG1_DECISION_DEADLINE.svg", figure1()),
        "figure_2": ("PAYOFF_B_INFO_V2_FIG2_DESYNCHRONIZATION.svg", figure2()),
        "figure_3": ("PAYOFF_B_INFO_V2_FIG3_NETWORK_MEMORY.svg", figure3()),
        "figure_4": ("PAYOFF_B_INFO_V2_FIG4_BROAD_CONNECTIVITY.svg", figure4()),
        "figure_5": ("PAYOFF_B_INFO_V2_FIG5_INFORMATION_AXES.svg", figure5()),
        "figure_6": ("PAYOFF_B_INFO_V2_FIG6_CAPACITY.svg", figure6()),
        "figure_7": ("PAYOFF_B_INFO_V2_FIG7_RESCUE.svg", figure7()),
    }
    manifest = {
        "status": "payoff_b_information_coordination_v2_seven_figure_set",
        "aikens_outcome_used": False,
        "source_policy": {
            "figure_1": "exact endogenous-information model + frozen published flycatcher anchor",
            "figure_2": "exact endogenous-information model + frozen result receipt",
            "figure_3": "frozen strict Bayesian topology receipt",
            "figure_4": "frozen broad predictive-connectivity receipt",
            "figure_5": "frozen wigeon null + frozen long-term cue-driver negative gate + flycatcher anchor",
            "figure_6": "frozen 2026-09-20 capacity / temporal-bypass synthetic receipts",
            "figure_7": "exact perfect-information rescue-coalition theorem",
        },
        "figures": {},
    }
    for key, (name, svg) in payloads.items():
        path = output_dir / name
        path.write_text(svg, encoding="utf-8")
        manifest["figures"][key] = {
            "path": path.name,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
    mp = output_dir / "PAYOFF_B_INFORMATION_DEADLINES_V2_FIGURE_MANIFEST.json"
    mp.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return {"manifest": mp, **{k: output_dir / v[0] for k, v in payloads.items()}}


def main():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/payoff_b_information_deadlines_v2_figures"),
    )
    a = p.parse_args()
    paths = render_all(a.output_dir)
    for key, path in paths.items():
        print(f"{key}={path}")


if __name__ == "__main__":
    main()
