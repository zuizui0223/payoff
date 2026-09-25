#!/usr/bin/env python3
"""Build integrated PAYOFF-B Supporting Information from frozen receipts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_tracking_theory_supporting_information import (
    build_supporting_information as build_synthetic_supporting_information,
)

ROOT = Path(__file__).resolve().parents[1]
BROAD = ROOT / "data" / "payoff_b_broad_bird_stage1_result_20260925.json"
PANEL = ROOT / "data" / "payoff_b_empirical_phase_panel_status_20260921.json"
INDUSTRIAL = ROOT / "data" / "payoff_b_industrial_mule_deer_actuator_receipt_20260921.json"
WIGEON = ROOT / "data" / "wigeon_era5_sourcefaithful_calibration_result_20260924.json"
BARNACLE = ROOT / "data" / "barnacle_era5_reliability_result_20260924.json"
SVALBARD = ROOT / "data" / "svalbard_barnacle_era5_reliability_result_20260924.json"
AIKENS = ROOT / "data" / "aikens2022_lambda_perturbation_registration_20260921.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_supporting_information() -> str:
    synthetic = build_synthetic_supporting_information()
    start = synthetic.find("## S1.")
    if start < 0:
        raise ValueError("synthetic Supporting Information is missing S1")
    synthetic_body = synthetic[start:]
    synthetic_body = synthetic_body.replace(
        "No number in this Supporting Information should be interpreted as a "
        "calibrated natural climate threshold, natural coordination-barrier "
        "prevalence, empirical controller gain, or named-species parameter "
        "estimate. The later empirical phase-retention programme is outside this "
        "Supporting Information.",
        "No number in S1-S8 should be interpreted as a calibrated natural climate "
        "threshold or natural coordination-barrier prevalence. S9-S12 below "
        "document the separate empirical evidence layer used by the integrated "
        "manuscript.",
    )

    broad = load(BROAD)
    panel = load(PANEL)
    industrial = load(INDUSTRIAL)
    wigeon = load(WIGEON)
    barnacle = load(BARNACLE)
    svalbard = load(SVALBARD)
    aikens = load(AIKENS)

    minima = {
        (row["response"], round(float(row["alignment_ref"]), 6)): row
        for row in broad["gam_minima"]
    }
    raw = minima[("raw_abs_lag", 0.948293)]
    centered = minima[("centered_abs_lag", 0.948374)]
    perfect = minima[("centered_abs_lag", 1.0)]
    centered_unc = next(
        row
        for row in broad["centered_optimum_uncertainty"]
        if round(float(row["alignment_ref"]), 6) == 0.948374
    )

    direct = panel["direct_taxa"]
    mule = next(row for row in direct if row["common_name"] == "mule deer")
    goose = next(row for row in direct if row["common_name"] == "barnacle goose")
    wigeon_panel = next(
        row for row in direct if row["common_name"] == "Eurasian wigeon"
    )
    interval = panel["measurement_error_status"]["interval_standardization"]

    lines = [
        "# Supporting Information",
        "",
        "## Hidden tracking: why environmental mismatch does not reveal how organisms keep pace with changing environments",
        "",
        "**PREOUTCOME working Supporting Information - 2026-09-25**",
        "",
        "S1-S8 preserve the frozen synthetic mechanism evidence dated 2026-09-20. "
        "S9-S12 document the empirical macroecological, direct-controller, "
        "reliability and perturbation layers. The registered Aikens fixed-24 h "
        "lambda outcome remains unopened; no result is inferred in advance.",
        "",
        synthetic_body,
        "",
        "## S9. Broad 55-species migration-speed falsification",
        "",
        "The Stage-1 analysis is materialized from the original frozen workflow "
        f"run {broad['source_analysis']['workflow_run_id']} and artifact "
        f"{broad['source_analysis']['workflow_artifact_id']}. The materialized "
        "receipt binds the original output-file hashes; this section does not "
        "refit the models.",
        "",
        "| quantity | value |",
        "|---|---:|",
        f"| observations | {broad['sample']['n_rows']} |",
        f"| centered-response observations | {broad['sample']['n_centered_rows']} |",
        f"| species | {broad['sample']['n_species']} |",
        f"| years | {broad['sample']['n_years']} |",
        f"| median animal/environment speed ratio | {broad['sample']['median_speed_ratio']:.3f} |",
        f"| median directional alignment | {broad['sample']['median_directional_alignment']:.3f} |",
        "",
        "| response / reference | fitted point minimum u* |",
        "|---|---:|",
        f"| raw absolute mismatch, median alignment | {raw['u_star']:.4f} |",
        f"| species-by-cell phase-centered mismatch, median alignment | {centered['u_star']:.4f} |",
        f"| phase-centered mismatch, perfect alignment | {perfect['u_star']:.4f} |",
        "",
        "Conditional coefficient draws for the centered median-alignment surface "
        f"gave median u*={centered_unc['u_median']:.3f} with a 95% interval "
        f"{centered_unc['u_lo_95']:.3f}-{centered_unc['u_hi_95']:.3f}. "
        "The wide interval is retained as evidence against treating the point "
        "minimum as a portable constant.",
        "",
        "| species-level diagnostic | value |",
        "|---|---:|",
        f"| species with fitted diagnostic | {broad['species_heterogeneity']['n_species_fit']} |",
        f"| positive curvature | {broad['species_heterogeneity']['n_positive_curvature']} |",
        f"| finite vertex inside species 5-95% support | {broad['species_heterogeneity']['n_vertices_inside_5_95']} |",
        f"| positive curvature with p<0.1 | {broad['species_heterogeneity']['n_curvature_p_lt_0_1']} |",
        "",
        "Retained inference: the registered broad test does not support one universal "
        "natural movement-speed/environmental-wave-speed optimum.",
        "",
        "## S10. Direct phase-control systems and interval scale",
        "",
        "| system | raw lambda / range | evidence role | actuator architecture |",
        "|---|---|---|---|",
        f"| mule deer | {mule['lambda_approx']:.3f} | existing direct system | {mule['actuator']} |",
        f"| barnacle goose | {min(goose['lambdas']):.3f} to {max(goose['lambdas']):.3f} | within-taxon route replication | {goose['actuator']} |",
        f"| Eurasian wigeon POWER | {wigeon_panel['lambda']:.3f} | prospective third taxon | stopover source-specific; travel speed unsupported |",
        f"| Eurasian wigeon ERA5 | {wigeon_panel['independent_era5_replication']['lambda_hat']:.3f} | independent environmental reconstruction | stopover replication unsupported |",
        "",
        "Raw lambda is a segment-scale estimator. It is not used to rank taxa by a "
        "single biological controller rate.",
        "",
        "| secondary scale-explicit comparison | retained initial phase memory |",
        "|---|---:|",
        f"| mule deer whole migration | {interval['mule_deer_whole_migration_retention']:.3f} |",
        f"| wigeon typical 7-transition path, POWER | {interval['wigeon_power_typical_path_retention']:.3f} |",
        f"| wigeon typical 7-transition path, ERA5 | {interval['wigeon_era5_typical_path_retention']:.3f} |",
        f"| wigeon typical path, conservative SIMEX sensitivity | {interval['wigeon_conservative_simex_typical_path_retention']:.3f} |",
        "",
        "These path-memory quantities are secondary comparison coordinates, not "
        "predicted final phase error and not corrected universal biological constants.",
        "",
        "## S11. Environmental-reconstruction reliability",
        "",
        "### S11.1 Eurasian wigeon",
        "",
        f"The source-faithful ERA5 follow-up covered "
        f"{wigeon['coverage']['paired_events']}/{wigeon['coverage']['frozen_events']} "
        f"staging events and {wigeon['coverage']['complete_transition_pairs']} "
        "complete controller transitions.",
        "",
        "| reconstruction | lambda | stopover slope | stopover p |",
        "|---|---:|---:|---:|",
        f"| POWER | {wigeon['controller_comparison']['power']['lambda_hat']:.3f} | {wigeon['controller_comparison']['power']['stopover_slope']:.3f} | {wigeon['controller_comparison']['power']['stopover_cluster_p']:.3f} |",
        f"| ERA5 | {wigeon['controller_comparison']['era5']['lambda_hat']:.3f} | {wigeon['controller_comparison']['era5']['stopover_slope']:.3f} | {wigeon['controller_comparison']['era5']['stopover_cluster_p']:.3f} |",
        "",
        "Phase-retention contraction reproduces across the two environmental "
        "surfaces, whereas the POWER stopover association does not reproduce under "
        "the independent ERA5 reconstruction.",
        "",
        "### S11.2 Barnacle-goose highlighted transitions",
        "",
        "| flyway / transition | POWER lambda | ERA5 lambda | negative stopover response reproduced |",
        "|---|---:|---:|---|",
    ]
    for row in barnacle["flyways"]:
        lines.append(
            f"| {row['flyway']} {row['transition']} | "
            f"{row['power']['lambda_hat']:.3f} | "
            f"{row['era5']['lambda_hat']:.3f} | yes |"
        )
    lines += [
        f"| Svalbard {svalbard['transition']} | "
        f"{svalbard['power']['lambda_hat']:.3f} | "
        f"{svalbard['era5']['lambda_hat']:.3f} | yes |",
        "",
        "The Svalbard negative lambda sign reproduces under ERA5. POWER-versus-ERA5 "
        "disagreement is treated as assumption-conditional replicate sensitivity, "
        "not a source-specific gold-standard error distribution.",
        "",
        "## S12. Industrial actuation perturbation and preregistered Aikens gate",
        "",
        "### S12.1 Frozen actuation contrast",
        "",
        "| quantity | value |",
        "|---|---:|",
        f"| source GPS positions | {industrial['source_reconstruction']['gps_points']} |",
        f"| source animals | {industrial['source_reconstruction']['gps_animals']} |",
        f"| primary animal-years | {industrial['primary_analysis']['animal_years']} |",
        f"| primary animals | {industrial['primary_analysis']['animals']} |",
        f"| median G, small development | {industrial['primary_analysis']['median_G_small']:.3f} |",
        f"| median G, large development | {industrial['primary_analysis']['median_G_large']:.3f} |",
        f"| large-development log-G shift | {industrial['primary_analysis']['large_development_logG_shift']:.3f} |",
        f"| clustered p | {industrial['primary_analysis']['p']:.3f} |",
        "",
        "The stronger longitudinal-deterioration prediction was not supported "
        f"(beta={industrial['stronger_longitudinal_forecast']['beta']:.3f}, "
        f"p={industrial['stronger_longitudinal_forecast']['p']:.3f}).",
        "",
        "### S12.2 Preregistered fixed-24 h lambda perturbation",
        "",
        "| registration field | frozen value |",
        "|---|---|",
        f"| independent test ID | {aikens['independent_test_id']} |",
        f"| phase coordinate | {aikens['phase_coordinate_id']} |",
        f"| segment scale | {aikens['segment_scale_id']} |",
        f"| comparison | {aikens['group_a']} vs {aikens['group_b']} |",
        f"| expected direction | {aikens['expected_direction']} |",
        f"| maximum p-value | {aikens['max_p_value']} |",
        "",
        "**PREOUTCOME STATE: the Aikens lambda outcome is unopened.** The final "
        "Supporting Information must be rebuilt after registered adjudication. "
        "Supported, wrong-direction, insufficient-support and non-estimable "
        "outcomes are all licensed by the frozen renderer without narrative retuning.",
        "",
        "## S13. Integrated claim boundary",
        "",
        "- The 55-species result is the primary cross-system generality test.",
        "- Direct taxa share a phase-retention estimator form, not a universal raw lambda.",
        "- Interval-standardized retained memory is a secondary scale-explicit coordinate.",
        "- Actuator architecture remains system- and reconstruction-dependent.",
        "- Synthetic velocities, barrier counts and route penalties are not natural thresholds or prevalence estimates.",
        "- The Aikens perturbation is within taxon and is never counted as a fourth cross-taxon replication.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/PAYOFF_B_INTEGRATED_SUPPORTING_INFORMATION_PREOUTCOME.md"),
    )
    args = p.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    text = build_supporting_information()
    args.output.write_text(text, encoding="utf-8")
    print(args.output)
    print(f"integrated_supporting_information bytes={len(text.encode('utf-8'))}")


if __name__ == "__main__":
    main()
