#!/usr/bin/env python3
"""Build Supporting Information for the integrated PAYOFF-B tracking ecology paper."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_tracking_theory_supporting_information import (
    build_supporting_information as build_synthetic_si,
)

ROOT = Path(__file__).resolve().parents[1]
BROAD = ROOT / "data" / "payoff_b_broad_bird_stage1_result_20260925.json"
PANEL = ROOT / "data" / "payoff_b_empirical_phase_panel_status_20260921.json"
STANDARD = ROOT / "data" / "payoff_b_phase_retention_interval_standardization_result_20260925.json"
INPUTS = ROOT / "data" / "payoff_b_integrated_empirical_figure_inputs_20260925.json"
INDUSTRIAL = ROOT / "data" / "payoff_b_industrial_mule_deer_actuator_receipt_20260921.json"
AIKENS_REG = ROOT / "data" / "aikens2022_lambda_perturbation_registration_20260921.json"
AIKENS_CONTRACT = ROOT / "data" / "aikens2022_lambda_outcome_interpretation_contract_20260922.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def empirical_sections() -> str:
    broad = load(BROAD)
    panel = load(PANEL)
    standard = load(STANDARD)
    inputs = load(INPUTS)
    industrial = load(INDUSTRIAL)
    aikens_reg = load(AIKENS_REG)
    aikens_contract = load(AIKENS_CONTRACT)

    lines = [
        "",
        "## S9. Broad 55-species macroecological test",
        "",
        "### S9.1 Frozen sample and source identity",
        "",
        "| quantity | value |",
        "|---|---:|",
        f"| observations | {broad['sample']['n_rows']} |",
        f"| phase-centered observations | {broad['sample']['n_centered_rows']} |",
        f"| species | {broad['sample']['n_species']} |",
        f"| years | {broad['sample']['n_years']} |",
        f"| median animal/environment speed ratio | {broad['sample']['median_speed_ratio']:.4f} |",
        f"| median directional alignment | {broad['sample']['median_directional_alignment']:.4f} |",
        "",
        "Original workflow run: "
        + str(broad["source_analysis"]["workflow_run_id"])
        + "; artifact ID: "
        + str(broad["source_analysis"]["workflow_artifact_id"])
        + "; artifact SHA256: "
        + broad["source_analysis"]["workflow_artifact_sha256"]
        + ".",
        "",
        "### S9.2 Fitted minima",
        "",
        "| response | alignment reference | fitted speed-ratio minimum | fitted minimum |",
        "|---|---:|---:|---:|",
    ]
    for row in broad["gam_minima"]:
        lines.append(
            f"| {row['response']} | {float(row['alignment_ref']):.6f} | "
            f"{float(row['u_star']):.6f} | {float(row['fitted_minimum']):.4f} |"
        )

    lines += [
        "",
        "### S9.3 Conditional optimum uncertainty",
        "",
        "| alignment | median u* | 95% interval | boundary-hit fraction | fraction in PAYOFF-B1 1–1.606 interval |",
        "|---:|---:|---:|---:|---:|",
    ]
    for row in broad["centered_optimum_uncertainty"]:
        lines.append(
            f"| {float(row['alignment_ref']):.6f} | {float(row['u_median']):.3f} | "
            f"{float(row['u_lo_95']):.3f}–{float(row['u_hi_95']):.3f} | "
            f"{float(row['boundary_hit_fraction']):.3f} | "
            f"{float(row['in_payoff_b_reference_fraction']):.3f} |"
        )

    sh = broad["species_heterogeneity"]
    lines += [
        "",
        "### S9.4 Species-level heterogeneity",
        "",
        "| diagnostic | value |",
        "|---|---:|",
        f"| species with fitted diagnostics | {sh['n_species_fit']} |",
        f"| positive curvature | {sh['n_positive_curvature']} |",
        f"| finite vertex inside species 5–95% support | {sh['n_vertices_inside_5_95']} |",
        f"| positive curvature with p<0.1 | {sh['n_curvature_p_lt_0_1']} |",
        f"| median internal vertex u* | {float(sh['median_u_star_inside']):.3f} |",
        f"| fraction internal vertices inside 1–1.606 | {float(sh['fraction_inside_payoff_b_reference']):.3f} |",
        "",
        "Retained interpretation: the broad analysis rejects one portable natural speed optimum. "
        "Phase centering moves the point estimate toward order-one values, but the fitted "
        "minimum is shallow and species-level optima remain heterogeneous.",
        "",
        "## S10. Direct phase-control systems, interval scale and reliability",
        "",
        "### S10.1 Direct system registry",
        "",
        "| taxon/system | raw lambda | ecological interval / role | actuator / reliability note |",
        "|---|---:|---|---|",
    ]
    for row in panel["direct_taxa"]:
        if row["common_name"] == "mule deer":
            lines.append(
                f"| mule deer | {float(row['lambda_approx']):.5f} | whole spring migration | "
                f"{row['actuator']} |"
            )
        elif row["common_name"] == "barnacle goose":
            vals = ", ".join(f"{float(x):.3f}" for x in row["lambdas"])
            lines.append(
                f"| barnacle goose highlighted transitions | {vals} | repeated route stages "
                f"within one taxon | {row['actuator']} |"
            )
        elif row["common_name"] == "Eurasian wigeon":
            era5 = row["independent_era5_replication"]
            lines.append(
                f"| Eurasian wigeon POWER | {float(row['lambda']):.6f} | "
                f"224 consecutive staging transitions | stopover source gate: "
                f"{row['stopover_actuator']} |"
            )
            lines.append(
                f"| Eurasian wigeon ERA5 | {float(era5['lambda_hat']):.6f} | "
                f"same 224 transitions, independent environmental reconstruction | "
                f"stopover replication: {era5['stopover_replication']} |"
            )

    ist = panel["measurement_error_status"]["interval_standardization"]
    lines += [
        "",
        "### S10.2 Secondary interval-standardized comparison",
        "",
        "| secondary quantity | value |",
        "|---|---:|",
        f"| mule-deer whole-migration retained memory | {float(ist['mule_deer_whole_migration_retention']):.4f} |",
        f"| wigeon typical transition count | {ist['wigeon_typical_transition_count']} |",
        f"| wigeon POWER typical-path retained memory | {float(ist['wigeon_power_typical_path_retention']):.4f} |",
        f"| wigeon ERA5 typical-path retained memory | {float(ist['wigeon_era5_typical_path_retention']):.4f} |",
        f"| wigeon conservative SIMEX typical-path retained memory | {float(ist['wigeon_conservative_simex_typical_path_retention']):.4f} |",
        "",
        "These are scale-explicit comparison coordinates, not pooled biological controller estimates.",
        "",
        "### S10.3 Highlighted system interval details",
        "",
        "| system | median interval (d) | variant | lambda | k_eq (d^-1) | path memory licensed |",
        "|---|---:|---|---:|---:|---|",
    ]
    keep = {
        "mule_deer_whole_migration",
        "barnacle_svalbard_R2_R4",
        "barnacle_greenland_R2_R3",
        "barnacle_barents_R1_R2",
        "eurasian_wigeon_staging_transition",
    }
    for sys in standard["systems"]:
        if sys["system_id"] not in keep:
            continue
        for v in sys["variants"]:
            licensed = bool(v.get("path_memory", {}).get("licensed", False))
            lines.append(
                f"| {sys['system_id']} | {float(sys['duration_days']['median']):.3f} | "
                f"{v['variant_id']} | {float(v['lambda']):.6f} | "
                f"{float(v['equivalent_decay_constant_per_day']):.4f} | "
                f"{str(licensed).lower()} |"
            )

    mstatus = panel["measurement_error_status"]
    lines += [
        "",
        "### S10.4 Measurement-error / reconstruction boundary",
        "",
        f"- Wigeon complete source-faithful ERA5 calibration: **{mstatus['wigeon_source_faithful_era5_calibration']['status']}**.",
        f"- Wigeon frozen SIMEX status: **{mstatus['wigeon_simex_v2']['status']}**; role: {mstatus['wigeon_simex_v2']['role']}.",
        f"- Registered ERA5-Land lane: **{mstatus['registered_era5land_lane']['status']}**.",
        f"- Mule-deer reliability calibration: **{mstatus['mule_deer_reliability_calibration']}**.",
        f"- Barnacle-goose reliability calibration: **{mstatus['barnacle_goose_reliability_calibration']['status']}**.",
        "",
        "No source-specific gold-standard phase-error distribution is identified, so "
        "cross-system latent-magnitude ranking remains unlicensed.",
        "",
        "## S11. Environmental innovation, industrial actuation and Aikens preregistration",
        "",
        "### S11.1 Environmental innovation and phase retention",
        "",
        "| flyway | transition | environmental innovation SD (d) | lambda | |lambda| |",
        "|---|---|---:|---:|---:|",
    ]
    for row in inputs["innovation_rows"]:
        if row["stable_phase_map"]:
            lines.append(
                f"| {row['flyway']} | {row['transition']} | "
                f"{float(row['environmental_innovation_sd_days']):.3f} | "
                f"{float(row['lambda']):.4f} | {float(row['abs_lambda']):.4f} |"
            )

    lines += [
        "",
        "The retained screen does not support a simple rule that higher phenological "
        "predictability mechanically produces stronger realized correction.",
        "",
        "### S11.2 Industrial-development actuation sensitivity",
        "",
        "| near/far definition (km) | animal-years | animals | median G small | median G large | year×large beta | p |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in inputs["industrial_rows"]:
        lines.append(
            f"| {row['edge_km']}/{row['far_km']} | {row['n_individual_years']} | "
            f"{row['n_animals']} | {float(row['median_G_small']):.3f} | "
            f"{float(row['median_G_large']):.3f} | "
            f"{float(row['year_x_large_beta']):.4f} | {float(row['year_x_large_p']):.3f} |"
        )

    primary = industrial["primary_analysis"]
    lines += [
        "",
        f"Primary 2/10-km contrast: median G small={float(primary['median_G_small']):.3f}, "
        f"median G large={float(primary['median_G_large']):.3f}; "
        f"large-development log-G shift={float(primary['large_development_logG_shift']):.3f}, "
        f"p={float(primary['p']):.3f}.",
        "",
        "The stronger year-by-development deterioration prediction was not supported and "
        "remains a retained negative result.",
        "",
        "### S11.3 Registered Aikens fixed-24h lambda gate",
        "",
        "Registration ID: "
        + str(aikens_reg.get("registration_id", aikens_reg.get("test_id", "aikens2022_lambda_perturbation_v1")))
        + ".",
        "",
        "PREOUTCOME status: **UNOPENED**.",
        "",
        "The fixed analysis preserves the declared phase coordinate, 24-h segment scale, "
        "±3-h target tolerance, environmental-product amendment, minimum animals/pairs "
        "per group, direction and support thresholds. No retuning is licensed after the "
        "result is opened.",
        "",
        "Interpretation contract: "
        + str(aikens_contract.get("contract_id", "aikens2022_lambda_outcome_interpretation_contract_20260922"))
        + ".",
        "",
        "The result may enter only through the frozen outcome-blind renderer. It is never "
        "counted as a fourth independent cross-taxon lambda replication.",
        "",
        "## S12. Integrated provenance and claim boundary",
        "",
        "- the 55-species broad test is the primary cross-system generality result;",
        "- direct taxa provide mechanistic decomposition rather than a formal n=3 meta-analysis;",
        "- raw lambda values remain segment-scale estimands;",
        "- interval-standardized quantities remain secondary comparison coordinates;",
        "- synthetic design frequencies are not natural prevalence estimates;",
        "- synthetic velocities are not calibrated natural thresholds;",
        "- Aikens cannot retune the headline, broad-bird result, or direct-system synthesis;",
        "- the former standalone Oikos and GEB manuscripts are rollback/provenance sources, not simultaneous submissions.",
        "",
        "This Supporting Information introduces no new scientific result beyond the frozen receipts named above.",
        "",
    ]
    return "\n".join(lines)


def build_supporting_information() -> str:
    synthetic = build_synthetic_si()
    synthetic = synthetic.replace(
        "## Hidden tracking: space-time buffering of environmental mismatch and its limits under moving environments",
        "## Hidden tracking: why environmental mismatch does not reveal how organisms keep pace with changing environments",
        1,
    )
    synthetic = synthetic.replace(
        "No number in this Supporting Information should be interpreted as a calibrated natural climate threshold, natural coordination-barrier prevalence, empirical controller gain, or named-species parameter estimate. The later empirical phase-retention programme is outside this Supporting Information.",
        "No synthetic number in S1–S8 should be interpreted as a calibrated natural climate threshold, natural coordination-barrier prevalence or named-species parameter estimate. Registered empirical evidence is added separately in S9–S12.",
    )
    return synthetic.rstrip() + "\n" + empirical_sections()


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/PAYOFF_B_INTEGRATED_TRACKING_SUPPORTING_INFORMATION_V1.md"),
    )
    args = p.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    content = build_supporting_information()
    args.output.write_text(content, encoding="utf-8")
    print(args.output)
    print(f"integrated_supporting_information bytes={len(content.encode('utf-8'))}")


if __name__ == "__main__":
    main()
