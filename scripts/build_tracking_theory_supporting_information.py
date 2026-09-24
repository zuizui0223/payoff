#!/usr/bin/env python3
"""Build Oikos-ready Supporting Information from frozen PAYOFF-B receipts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKING = ROOT / "data" / "payoff_b_tracking_synthetic_receipt_20260920.json"
MOVING = ROOT / "data" / "payoff_b_moving_landscape_receipt_20260920.json"
CONNECTIVITY = ROOT / "data" / "payoff_b_2d_connectivity_receipt_20260920.json"
CLOSED = ROOT / "data" / "payoff_b_closed_loop_tracking_receipt_20260920.json"
FEEDBACK = ROOT / "data" / "payoff_b_movement_feedback_landscape_receipt_20260920.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def f4(value: float) -> str:
    return f"{value:.4f}"


def f6(value: float) -> str:
    return f"{value:.6f}"


def pct(value: float) -> str:
    return f"{100 * value:.1f}%"


def build_supporting_information() -> str:
    tracking = load(TRACKING)
    moving = load(MOVING)
    conn = load(CONNECTIVITY)
    closed = load(CLOSED)
    feedback = load(FEEDBACK)

    lines = [
        "# Supporting Information",
        "",
        "## Hidden tracking: space-time buffering of environmental mismatch and its limits under moving environments",
        "",
        "Frozen synthetic evidence date: **2026-09-20**",
        "",
        "This Supporting Information reorganizes the five frozen synthetic PAYOFF-B tracking receipts. It introduces no new simulation, empirical calibration, or post-freeze phase-retention evidence. All velocities, costs, population sizes, barrier frequencies, and controller gains are model quantities under declared synthetic designs, not natural prevalence estimates or empirical thresholds.",
        "",
        "## S1. Deterministic tracking benchmark and estimand separation",
        "",
        "| quantity | value |",
        "|---|---:|",
        f"| ecological-grid cells | {tracking['ecological_grid']['cells']} |",
        f"| coordination-barrier cells | {tracking['ecological_grid']['coordination_barrier_cells']} |",
        "",
        "Finite-population weak-mutation occupancy, deterministic local accessibility, demographic persistence, and long-run payoff are treated as separate estimands.",
        "",
        "coordinated value != unilateral accessibility != demographic visibility != stochastic barrier crossing != long-run payoff improvement",
        "",
        "The ecological-grid barrier fraction is a property of the declared design and is not interpreted as natural prevalence.",
        "",
        "## S2. Moving-landscape, connectivity and anisotropy robustness",
        "",
        "### S2.1 One-dimensional persistence frontier",
        "",
        "| phenology limit | max persisted velocity | first failed velocity |",
        "|---:|---:|---:|",
    ]
    for row in moving["persistence_frontier"]["brackets"]:
        lines.append(
            f"| {row['phenology_limit']} | {row['max_persisted_velocity']:.3f} | {row['first_failed_velocity']:.3f} |"
        )

    lines += [
        "",
        f"The brackets were unchanged between the canonical and refined strategy grids: **{str(moving['persistence_frontier']['unchanged_across_strategy_grids']).lower()}**. Frontier strategies remained **{moving['persistence_frontier']['frontier_outcome'].replace('_', ' ')}**.",
        "",
        "### S2.2 Two-dimensional temporal bypass",
        "",
        "| velocity | migration | phenology | second-wall crossing |",
        "|---:|---:|---:|---:|",
    ]
    for row in conn["zigzag_temporal_buffering"]["canonical_zmax4_sequence"]:
        crossing = row["second_wall_crossing"]
        crossing_text = crossing if isinstance(crossing, str) else f"{crossing:.4f}"
        lines.append(
            f"| {row['velocity']:.2f} | {row['migration']:.4f} | {row['phenology']:.4f} | {crossing_text} |"
        )

    lines += [
        "",
        f"Raising the phenology limit from 0 to 4 reduced the magnitude of the canonical zigzag route-growth penalty by **{pct(conn['zigzag_temporal_buffering']['penalty_magnitude_reduction_0_to_4'])}**. The sampled persistence difference between open and zigzag landscapes in this comparison was {conn['zigzag_temporal_buffering']['sampled_persistence_difference_open_minus_zigzag']}.",
        "",
        "### S2.3 Movement anisotropy",
        "",
        "| transverse/axial movement weight | zmax=0 zigzag penalty | zmax=4 zigzag penalty | penalty reduction |",
        "|---:|---:|---:|---:|",
    ]
    anis = conn["anisotropic_movement"]
    for label, key0, key4, redkey in [
        ("1", "y1_z0", "y1_z4", "y1"),
        ("0.5", "y0.5_z0", "y0.5_z4", "y0.5"),
        ("0.25", "y0.25_z0", "y0.25_z4", "y0.25"),
        ("0.1", "y0.1_z0", "y0.1_z4", "y0.1"),
    ]:
        lines.append(
            f"| {label} | {f6(anis['mean_zigzag_growth_penalty'][key0])} | {f6(anis['mean_zigzag_growth_penalty'][key4])} | {pct(anis['penalty_magnitude_reduction_z0_to_z4'][redkey])} |"
        )

    lines += [
        "",
        f"Mean reduction across anisotropy levels was **{pct(anis['penalty_magnitude_reduction_z0_to_z4']['mean'])}**. {anis['persistence_losses'].capitalize()}.",
        "",
        "### S2.4 Boundary and stochastic-demography checks",
        "",
        "| boundary retention | barrier cells / 36 | persistence rescues / 36 | mean accessibility gap |",
        "|---:|---:|---:|---:|",
    ]
    for row in moving["boundary_robustness"]["by_retention"]:
        lines.append(
            f"| {row['retention']:.1f} | {row['barriers']}/36 | {row['persistence_rescues']}/36 | {f4(row['mean_gap'])} |"
        )
    lines += [
        "",
        f"Integer Poisson patch demography used **{moving['stochastic_patch_validation']['replicates_per_boundary']} replicates per boundary condition**. In every retained boundary condition, local-endpoint persistence was 0 and matched-optimum persistence was 1.",
        "",
        "## S3. Coordination-gate robustness and interaction geometry",
        "",
        "### S3.1 Coarse two-dimensional interaction design",
        "",
        "| interaction strength | barriers | total cells | persistence rescues |",
        "|---:|---:|---:|---:|",
    ]
    coarse = conn["coevolution"]["coarse_mutation_step_0_2"]
    for key, strength in [("interaction_0", "0"), ("interaction_0_5", "0.5"), ("interaction_1", "1")]:
        row = coarse[key]
        lines.append(f"| {strength} | {row['barriers']} | {row['total']} | {row['rescues']} |")

    fine = conn["coevolution"]["fine_mutation_step_0_1"]
    lines += [
        "",
        "### S3.2 Fine unilateral-mutation design",
        "",
        f"Across {fine['positive_interaction_cells']} positive-interaction cells, the fine design retained **{fine['barriers']} coordination barriers** and **{fine['persistence_rescues']} persistence rescues**.",
        "",
        "| interaction | geometry | barriers / 4 | rescues / 4 |",
        "|---:|---|---:|---:|",
    ]
    for ikey, strength in [("interaction_0_5", "0.5"), ("interaction_1", "1")]:
        for geometry in ["open", "straight", "zigzag"]:
            row = fine[ikey][geometry]
            lines.append(f"| {strength} | {geometry} | {row['barriers']}/{row['total']} | {row['rescues']}/{row['total']} |")

    gate = conn["coevolution"]["direct_gate"]
    lines += [
        "",
        "Direct one-step gate, resident (m,h)=(0.2,0), coordinated neighbor (0.2,0.2):",
        "",
        "| quantity | value |",
        "|---|---:|",
        f"| resident joint low-density growth | {f6(gate['resident_joint_growth'])} |",
        f"| coordinated joint low-density growth | {f6(gate['coordinated_joint_growth'])} |",
        f"| coordinated gain | {f6(gate['coordinated_gain'])} |",
        f"| unilateral gain A | {f6(gate['unilateral_gain_a'])} |",
        f"| unilateral gain B | {f6(gate['unilateral_gain_b'])} |",
        f"| unilateral interaction mismatch | {f6(gate['unilateral_interaction_mismatch'])} |",
        "",
        "### S3.3 Distribution-level overlap sensitivity",
        "",
        "| overlap-penalty scale | unilateral gain |",
        "|---:|---:|",
    ]
    overlap = conn["distribution_overlap_sensitivity"]
    for scale in ["0", "0.5", "1", "2"]:
        lines.append(f"| {scale} | {f6(overlap['unilateral_gain_by_scale'][scale])} |")
    lines += [
        "",
        f"The barrier, persistence rescue and fixed one-step gate were retained at every overlap scale. Unilateral mutant/resident overlap ranged from {overlap['unilateral_distribution_overlap_range'][0]:.5f} to {overlap['unilateral_distribution_overlap_range'][1]:.5f}.",
        "",
        "## S4. Partner asymmetry and forcing-dependent synchronization",
        "",
        "| forcing | interaction | persistence | mean strategy distance | mismatch / endpoint |",
        "|---:|---:|---|---:|---|",
    ]
    pa = conn["partner_asymmetry"]
    moderate = pa["moderate_velocity_0_04"]
    for key, strength in [("interaction_0", "0"), ("interaction_0_5", "0.5"), ("interaction_1", "1")]:
        row = moderate[key]
        endpoint = row.get("endpoint", f"mean mismatch {f6(row['mean_interaction_mismatch'])}")
        lines.append(f"| 0.04 | {strength} | {row['persisted']} | {row['mean_strategy_distance']:.4f} | {endpoint} |")
    strong = pa["strong_velocity_0_06"]
    for key, strength in [("interaction_0", "0"), ("interaction_0_5", "0.5"), ("interaction_1", "1")]:
        row = strong[key]
        distance = row.get("mean_strategy_distance")
        distance_text = "matched" if distance is None else f"{distance:.4f}"
        lines.append(f"| 0.06 | {strength} | {row['persisted']} | {distance_text} | {row['endpoint']} |")
    lines += [
        "",
        "The same matching interaction aligns different intrinsic responses under moderate forcing but synchronizes partners onto a non-persistent local attractor under stronger forcing.",
        "",
        "## S5. Demographic visibility and finite-population barrier crossing",
        "",
        "### S5.1 Demographic replication",
        "",
        "| analysis | replicates | cells with persistence gain >=0.10 | maximum persistence gain |",
        "|---|---:|---:|---:|",
    ]
    pilot = tracking["demographic_stress"]["pilot_32_replicates"]
    repl = tracking["demographic_stress"]["replication_128_replicates"]
    lines += [
        f"| pilot | 32 | {pilot['barrier_cells_gain_ge_0_10']} | {pilot['max_persistence_gain']:.5f} |",
        f"| independent replication | 128 | {repl['barrier_cells_gain_ge_0_10']} | {repl['max_persistence_gain']:.5f} |",
        "",
        f"The independent rerun is retained. Mean persistence gain across replicated barrier cells was {repl['mean_persistence_gain_all_barrier_cells']:.6f}. The earlier large cell-level effect did not reproduce at >=0.10 and is retained as a failed pilot rather than hidden.",
        "",
        "| baseline growth | K | local persistence | matched persistence | gain |",
        "|---:|---:|---:|---:|---:|",
    ]
    for row in repl["visibility_examples"]:
        lines.append(f"| {row['baseline_growth']:.2f} | {row['K']} | {row['local']:.6f} | {row['matched']:.6f} | {row['gain']:.6f} |")
    lines += [
        "",
        f"Mean gain in local-persistence bin 0.3-0.7 was {repl['local_persistence_bin_0_3_to_0_7']['mean_persistence_gain']:.6f}; in bin 0.9-1.0 it was {repl['local_persistence_bin_0_9_to_1_0']['mean_persistence_gain']:.6f}.",
        "",
        "### S5.2 Finite-N drift crossing at beta=5",
        "",
        "| N | escape fraction | occupancy summary | mean joint growth |",
        "|---:|---:|---|---:|",
    ]
    drift = tracking["drift_escape"]
    for key, n in [("N_10", 10), ("N_30", 30), ("N_100", 100), ("N_300", 300), ("N_1000", 1000)]:
        row = drift["beta_5"][key]
        occupancy = row.get("high_payoff_fraction", row.get("local_fraction"))
        label = "high-payoff" if "high_payoff_fraction" in row else "local"
        lines.append(f"| {n} | {row['escape_fraction']:.5f} | {label} {occupancy:.6f} | {row['mean_joint_growth']:.6f} |")
    lines += [
        "",
        f"Local joint growth was {drift['local_joint_growth']:.6f}; coordinated matched growth was {drift['matched_joint_growth']:.6f}; accessibility gap was {drift['accessibility_gap']:.4f}. Retained interpretation: **drift-assisted barrier crossing, not drift rescue**.",
        "",
        "## S6. Closed-loop controller and explicit feedback landscape",
        "",
        "### S6.1 Exact local controller witness",
        "",
        f"Exact recurrence: {closed['exact_results']['recurrence']}.",
        f"Total restoring gain: {closed['exact_results']['total_feedback_gain']}; stability: {closed['exact_results']['stability']}; equilibrium mismatch: {closed['exact_results']['equilibrium_mismatch']}.",
        "",
        "| r | K* | q_m | q_h | e* | stable | timing feasible |",
        "|---:|---:|---:|---:|---:|---|---|",
    ]
    for row in closed["equal_cost_witness"]["rows"]:
        lines.append(f"| {row['r']:.2f} | {row['K']:.6f} | {row['q_m']:.6f} | {row['q_h']:.6f} | {row['e_star']:.6f} | {str(row['stable']).lower()} | {str(row['phenology_feasible']).lower()} |")
    ca = closed["cost_asymmetry_witness"]
    lines += [
        "",
        "### S6.2 Cost asymmetry",
        "",
        "| regime | r | q_m | q_h |",
        "|---|---:|---:|---:|",
        f"| movement expensive | 0.2 | {ca['movement_expensive']['r_0_2']['q_m']:.6f} | {ca['movement_expensive']['r_0_2']['q_h']:.6f} |",
        f"| movement expensive | 1.0 | {ca['movement_expensive']['r_1']['q_m']:.6f} | {ca['movement_expensive']['r_1']['q_h']:.6f} |",
        f"| phenology expensive | 0.2 | {ca['phenology_expensive']['r_0_2']['q_m']:.6f} | {ca['phenology_expensive']['r_0_2']['q_h']:.6f} |",
        f"| phenology expensive | 1.0 | {ca['phenology_expensive']['r_1']['q_m']:.6f} | {ca['phenology_expensive']['r_1']['q_h']:.6f} |",
        "",
        "### S6.3 Explicit state-dependent movement feedback",
        "",
        "| velocity | h | persistence across controller gains |",
        "|---:|---:|---|",
    ]
    hp = feedback["high_forcing_persistence"]
    for vkey, velocity in [("v_0_05", "0.05"), ("v_0_06", "0.06")]:
        for hkey, h in [("h_0", "0"), ("h_0_25", "0.25"), ("h_0_5", "0.5")]:
            lines.append(f"| {velocity} | {h} | {hp[vkey][hkey]} |")
    lines += [
        "",
        "At fixed movement-feedback gain k_m=1.6:",
        "",
        "| velocity | h | mean effective migration | growth | ceiling fraction | persisted |",
        "|---:|---:|---:|---:|---:|---|",
    ]
    fg = feedback["fixed_gain_1_6"]
    for vkey, velocity in [("v_0_05", 0.05), ("v_0_06", 0.06)]:
        for hkey, h in [("h_0", 0), ("h_0_25", 0.25), ("h_0_5", 0.5)]:
            row = fg[vkey][hkey]
            lines.append(f"| {velocity:.2f} | {h:.2f} | {row['mean_migration']:.6f} | {row['growth']:.6f} | {row['ceiling_fraction']:.4f} | {str(row['persisted']).lower()} |")
    lines += [
        "",
        "The exact local substitution null becomes forcing-dependent complementarity after explicit spatial mechanics and finite capacities are restored.",
        "",
        "## S7. Frozen provenance",
        "",
        "| evidence item | workflow run | artifact | SHA256 |",
        "|---|---:|---:|---|",
        f"| demographic replication | {tracking['provenance']['population_stress_replication']['workflow_run']} | {tracking['provenance']['population_stress_replication']['artifact_id']} | {tracking['provenance']['population_stress_replication']['sha256']} |",
        f"| drift escape | {tracking['provenance']['drift_escape_pilot']['workflow_run']} | {tracking['provenance']['drift_escape_pilot']['artifact_id']} | {tracking['provenance']['drift_escape_pilot']['sha256']} |",
        f"| 1D frontier | {moving['persistence_frontier']['canonical_run']} | {moving['persistence_frontier']['artifact_id']} | {moving['persistence_frontier']['sha256']} |",
        f"| boundary robustness | {moving['boundary_robustness']['workflow_run']} | {moving['boundary_robustness']['artifact_id']} | {moving['boundary_robustness']['sha256']} |",
        f"| 2D zigzag resolution | {conn['provenance']['zigzag_resolution']['workflow_run']} | {conn['provenance']['zigzag_resolution']['artifact_id']} | {conn['provenance']['zigzag_resolution']['sha256']} |",
        f"| 2D fine coevolution | {conn['provenance']['coevolution_fine']['workflow_run']} | {conn['provenance']['coevolution_fine']['artifact_id']} | {conn['provenance']['coevolution_fine']['sha256']} |",
        f"| anisotropic movement | {conn['provenance']['anisotropic_movement']['workflow_run']} | {conn['provenance']['anisotropic_movement']['artifact_id']} | {conn['provenance']['anisotropic_movement']['sha256']} |",
        f"| closed-loop witness | {closed['provenance']['workflow_run']} | {closed['provenance']['equal_cost']['artifact_id']} | {closed['provenance']['equal_cost']['sha256']} |",
        f"| explicit feedback | {feedback['provenance']['workflow_run']} | {feedback['provenance']['artifact_id']} | {feedback['provenance']['sha256']} |",
        "",
        "## S8. Claim boundary",
        "",
        f"- Tracking receipt: {tracking['claim_boundary']}.",
        f"- Moving-landscape receipt: {moving['claim_boundary']}.",
        f"- Two-dimensional receipt: {conn['claim_boundary']}.",
        f"- Closed-loop receipt: {closed['claim_boundary']}.",
        f"- Explicit-feedback receipt: {feedback['claim_boundary']}.",
        "",
        "No number in this Supporting Information should be interpreted as a calibrated natural climate threshold, natural coordination-barrier prevalence, empirical controller gain, or named-species parameter estimate. The later empirical phase-retention programme is outside this Supporting Information.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("outputs/PAYOFF_B_TRACKING_SUPPORTING_INFORMATION_V1.md"))
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    text = build_supporting_information()
    args.output.write_text(text, encoding="utf-8")
    print(args.output)
    print(f"tracking_supporting_information bytes={len(text.encode('utf-8'))}")


if __name__ == "__main__":
    main()
