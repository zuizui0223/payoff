#!/usr/bin/env python3
"""PAYOFF-B prospective 2x2 cue x recourse factorial design calibration.

SYNTHETIC ONLY. No bee, bird, flower or other organism was observed.
The original actionability theorem remains unchanged. Trials nested within a
colony do NOT become independent treatment-assignment units.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import statistics
from pathlib import Path

CONTRACT = (
    Path(__file__).resolve().parents[1]
    / "data/payoff_b_joint_cue_recourse_experiment_contract_20261120.json"
)
ARMS = ("lowq_lowr", "highq_lowr", "lowq_highr", "highq_highr")
POSITIVE_Z = 1.959963984540054


def load_contract(path: Path = CONTRACT) -> dict:
    cfg = json.loads(path.read_text(encoding="utf-8"))
    if cfg.get("contract_id") != (
        "payoff_b_prospective_2x2_cue_recourse_colony_assay_v1_20261120"
    ):
        raise ValueError("Unrecognized prospective joint-q-and-r contract")
    p = cfg["design"]
    q = p["randomized_factors"]["cue_reliability_q"]
    r = p["randomized_factors"]["corrective_switch_opportunity_r"]
    if (
        q != [0.65, 0.95]
        or r != [0.20, 0.85]
        or p["equal_hidden_state_prior_pi_early"] != 0.4
        or p["asymmetric_false_early_loss_CF"] != 2
        or p["asymmetric_missed_early_loss_CM"] != 1
        or p["assigned_waiting_cost_D"] != 0.08
    ):
        raise ValueError("PAYOFF-B original synthetic numerical witness changed")
    power = cfg["synthetic_power_plan"]
    if (
        power["seed"] != 20261120
        or power["candidate_independent_colonies_per_arm"] != [8, 12, 16, 24, 32]
        or power["trials_per_colony"] != 48
        or power["synthetic_behavioral_compliance_scenarios"] != [0, 0.5, 0.75]
        or power["synthetic_monte_carlo_repetitions"] != 300
    ):
        raise ValueError("Synthetic design power contract changed without version")
    return cfg


def model_geometry(cfg: dict) -> dict:
    p = cfg["design"]
    pi = p["equal_hidden_state_prior_pi_early"]
    cf = p["asymmetric_false_early_loss_CF"]
    cm = p["asymmetric_missed_early_loss_CM"]
    d = p["assigned_waiting_cost_D"]
    a = (1 - pi) * cf
    l = pi * cm
    s = a + l
    b = max(a, l)
    q0 = b / s
    # The planned q grid is above random-cue accuracy 0.5, and this
    # symmetric-cue binary branch has V_A(q)=max(0,S*q-B).
    reliability = p["randomized_factors"]["cue_reliability_q"]
    opportunity = p["randomized_factors"]["corrective_switch_opportunity_r"]
    arms = {}
    for iq, q in enumerate(reliability):
        v = max(0.0, s * q - b)
        for ir, r in enumerate(opportunity):
            label = ("highq" if iq else "lowq") + "_" + (
                "highr" if ir else "lowr"
            )
            gross = r * v
            net = gross - d
            arms[label] = {
                "assigned_cue_accuracy": q,
                "assigned_successful_switch_opportunity": r,
                "gross_information_value": gross,
                "net_information_value_minus_waiting_cost": net,
                "optimal_wait_for_cue_in_reduced_model": net > 0,
                "no_biological_behavior_implied": True,
            }
    if (
        abs(q0 - 0.75) > 1e-12
        or set(arms) != set(ARMS)
        or sum(x["optimal_wait_for_cue_in_reduced_model"] for x in arms.values()) != 1
        or not arms["highq_highr"]["optimal_wait_for_cue_in_reduced_model"]
    ):
        raise ValueError("Exact prospective threshold witness failed")
    return {
        "baseline_normal_action_expected_loss": l,
        "false_early_expected_loss": a,
        "total_asymmetric_loss_scale": s,
        "cue_actionability_threshold_q0": q0,
        "delay_cost": d,
        "intervention_arms": arms,
        "perfect_policy_expected_causal_interaction": (
            arms["highq_highr"]["net_information_value_minus_waiting_cost"]
        ),
    }


def _clamp(x: float, low: float, high: float) -> float:
    return min(high, max(low, x))


def simulated_colony_mean_loss(
    rng: random.Random,
    *,
    q: float,
    r: float,
    compliance: float,
    trials: int,
    pi: float,
    cf: float,
    cm: float,
    delay: float,
    baseline_cluster_noise: float,
) -> float:
    if not (0 <= compliance <= 1 and 0 <= pi <= 1 and 0 <= q <= 1
            and 0 <= r <= 1 and trials > 0 and delay >= 0):
        raise ValueError("Invalid frozen synthetic colony trial inputs")
    information_value = max(0.0, ((1 - pi) * cf + pi * cm) * q - max(
        (1 - pi) * cf, pi * cm
    ))
    # Under the declared model, rational waiting is profitable only if
    # expected remaining action opportunity × VOI exceeds time cost.
    permitted_optimal_wait = r * information_value > delay
    total = 0.0
    for _ in range(trials):
        early_state = rng.random() < pi
        cue_early = early_state if rng.random() < q else not early_state
        waits = (permitted_optimal_wait and compliance > 0.0
                 and (rng.random() < compliance))
        # An independent physical-gate lottery decides whether a
        # state-informed corrective switch remains possible.
        switches_to_early = waits and cue_early and (rng.random() < r)
        loss = 0.0
        if switches_to_early and not early_state:
            loss = cf
        elif not switches_to_early and early_state:
            loss = cm
        if waits:
            loss += delay
        total += loss
    return total / trials + baseline_cluster_noise


def estimate_interaction(colony_means: dict[str, list[float]]) -> dict:
    if set(colony_means) != set(ARMS):
        raise ValueError("Four original q×r colony-randomized arms required")
    if any(len(colony_means[a]) < 2 for a in ARMS):
        raise ValueError("At least two independent colonies per arm")
    means = {a: statistics.mean(colony_means[a]) for a in ARMS}
    # Positive is the greater reduction in net loss from higher q
    # in the group with higher remaining opportunity.
    tau = (
        means["lowq_highr"] - means["highq_highr"]
        - means["lowq_lowr"] + means["highq_lowr"]
    )
    variance = sum(
        statistics.variance(colony_means[a]) / len(colony_means[a])
        for a in ARMS
    )
    if variance <= 0:
        raise ValueError("Synthetic cluster-level contrast has zero variance")
    se = math.sqrt(variance)
    return {
        "four_colony_arm_mean_losses": means,
        "ITT_loss_difference_in_differences": tau,
        "cluster_mean_based_standard_error": se,
        "approximate_normal_lower_95": tau - POSITIVE_Z * se,
        "approximate_normal_upper_95": tau + POSITIVE_Z * se,
        "positive_interaction_lower_bound_above_zero": (
            tau - POSITIVE_Z * se > 0
        ),
        "two_sided_approximate_null_rejected": abs(tau / se) > POSITIVE_Z,
        "inference_is_a_synthetic_large_sample_approximation": True,
    }


def simulate(cfg: dict, *,
             colony_numbers: list[int] | None = None,
             repetitions: int | None = None) -> dict:
    power = cfg["synthetic_power_plan"]
    experimental = cfg["design"]
    geometry = model_geometry(cfg)
    sizes = colony_numbers if colony_numbers is not None else (
        power["candidate_independent_colonies_per_arm"]
    )
    nrep = repetitions if repetitions is not None else (
        power["synthetic_monte_carlo_repetitions"]
    )
    if (
        not sizes or any((not isinstance(n, int) or n < 2) for n in sizes)
        or not isinstance(nrep, int) or nrep < 1
    ):
        raise ValueError("Invalid synthetic-only design simulation dimensions")
    rng = random.Random(power["seed"])
    res = []
    for compliance in power["synthetic_behavioral_compliance_scenarios"]:
        for n in sizes:
            estimates = []
            false_or_power = 0
            directional = 0
            for _ in range(nrep):
                arms = {}
                for label in ARMS:
                    treatment = geometry["intervention_arms"][label]
                    arm = []
                    for _colony in range(n):
                        # Null scenario is a genuine NO-CUE-USE world.
                        # A truncated Gaussian centered at zero would give
                        # half the colonies positive compliance and corrupt
                        # the null calibration in an outcome-independent way.
                        c = (0.0 if compliance == 0.0 else _clamp(
                            rng.gauss(
                                compliance,
                                power["assumed_between_colony_compliance_SD"]
                            ), 0.0, 1.0
                        ))
                        shift = rng.gauss(
                            0.0, power["assumed_between_colony_measurement_SD_loss"]
                        )
                        arm.append(simulated_colony_mean_loss(
                            rng,
                            q=treatment["assigned_cue_accuracy"],
                            r=treatment["assigned_successful_switch_opportunity"],
                            compliance=c,
                            trials=power["trials_per_colony"],
                            pi=experimental["equal_hidden_state_prior_pi_early"],
                            cf=experimental["asymmetric_false_early_loss_CF"],
                            cm=experimental["asymmetric_missed_early_loss_CM"],
                            delay=experimental["assigned_waiting_cost_D"],
                            baseline_cluster_noise=shift
                        ))
                    arms[label] = arm
                fit = estimate_interaction(arms)
                estimates.append(fit["ITT_loss_difference_in_differences"])
                if fit["two_sided_approximate_null_rejected"]:
                    false_or_power += 1
                if fit["positive_interaction_lower_bound_above_zero"]:
                    directional += 1
            # Under the assumed model, only high-q/high-r waits. With
            # treatment compliance gamma, its mean benefit is gamma×0.192.
            res.append({
                "synthetic_compliance": compliance,
                "independent_colonies_per_randomized_arm": n,
                "synthetic_total_colonies": 4 * n,
                "synthetic_trials_per_colony": power["trials_per_colony"],
                "simulations": nrep,
                "theoretical_interaction_given_compliance": (
                    compliance
                    * geometry["perfect_policy_expected_causal_interaction"]
                ),
                "synthetic_mean_estimated_interaction": statistics.mean(estimates),
                "synthetic_sd_of_interaction": (
                    statistics.stdev(estimates) if nrep > 1 else None
                ),
                "synthetic_two_sided_rejection_frequency": false_or_power / nrep,
                "synthetic_directional_positive_CI_frequency": directional / nrep,
                "calibration_does_not_observe_organism_choices": True,
            })
    return {
        "simulation_status": "SYNTHETIC_DESIGN_CALIBRATION_ONLY_NO_NATURAL_DATA",
        "precommitted_contract": cfg["contract_id"],
        "project_date": cfg["date"],
        "seed": power["seed"],
        "exact_Payoff_B_binary_model_witness": geometry,
        "synthetic_simulation": res,
        "warnings": [
            "No biological effect, natural q, r, D_eff, fitness or migration phenotype measured",
            "Simulated compliance/cluster noise are assumptions, NOT field observations",
            "Normal-approximation 95% CI is power-planning only; real colony-level inference requires preregistered cluster-aware analysis",
            "Bee foraging patch task is a short-timescale analogy, NOT migration phenology or partner fitness",
            "Observed q/r probes, colony randomization and welfare admission are required before real outcome acquisition",
        ],
        "frozen_main_Payoff_B_papers_unchanged": True,
        "does_not_create_an_independent_positive_ecological_record": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=CONTRACT)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = simulate(load_contract(args.contract))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8"
    )
    for row in result["synthetic_simulation"]:
        print(json.dumps({
            "SIMULATED_ONLY": True,
            "compliance": row["synthetic_compliance"],
            "colonies_per_arm": row["independent_colonies_per_randomized_arm"],
            "hypothetical_interaction": round(
                row["synthetic_mean_estimated_interaction"], 4
            ),
            "synthetic_approx_directional_detection": (
                row["synthetic_directional_positive_CI_frequency"]
            ),
        }))
    print("SYNTHETIC_DESIGN_CALIBRATION_ONLY — no biological outcome opened")


if __name__ == "__main__":
    main()
