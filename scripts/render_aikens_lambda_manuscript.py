#!/usr/bin/env python3
"""Render the frozen Aikens lambda outcome into the GEB manuscript.

The result class and wording are determined from the registered result receipt.
This script does not fit the model and does not change any threshold.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


RESULTS_START = "<!-- AIKENS_LAMBDA_RESULTS_START -->"
RESULTS_END = "<!-- AIKENS_LAMBDA_RESULTS_END -->"
DISCUSSION_START = "<!-- AIKENS_LAMBDA_DISCUSSION_START -->"
DISCUSSION_END = "<!-- AIKENS_LAMBDA_DISCUSSION_END -->"
ABSTRACT_START = "<!-- AIKENS_LAMBDA_ABSTRACT_START -->"
ABSTRACT_END = "<!-- AIKENS_LAMBDA_ABSTRACT_END -->"
CONCLUSION_START = "<!-- AIKENS_LAMBDA_CONCLUSION_START -->"
CONCLUSION_END = "<!-- AIKENS_LAMBDA_CONCLUSION_END -->"


def _fmt(value: float | None) -> str:
    if value is None:
        return "NA"
    value = float(value)
    if value == 0:
        return "0"
    if abs(value) < 0.001:
        return f"{value:.2e}"
    return f"{value:.4f}"


def classify_result(payload: dict) -> str:
    status = str(payload.get("status", ""))
    if status == "phase_retention_contrast_not_estimable":
        return "NOT_ESTIMABLE"
    if status not in {
        "phase_retention_contrast_gate_pass",
        "phase_retention_contrast_gate_fail",
    }:
        raise ValueError(f"unrecognized Aikens lambda result status: {status!r}")

    gate = payload.get("gate")
    if not isinstance(gate, dict):
        raise ValueError("contrast result is missing gate object")
    if bool(gate.get("passed")):
        return "PASS"
    if not bool(gate.get("direction_passed")):
        return "FAIL_WRONG_DIRECTION"
    return "FAIL_INSUFFICIENT_SUPPORT"


def render_blocks(payload: dict) -> tuple[str, str, str, str, dict]:
    result_class = classify_result(payload)

    if result_class == "NOT_ESTIMABLE":
        reasons = payload.get("reasons") or []
        reason_text = "; ".join(str(x) for x in reasons) or "registered support or reconstruction gate not met"
        results = (
            "The preregistered within-mule-deer phase-retention contrast was "
            "**not estimable** under the frozen reconstruction and sample-support "
            f"contract ({reason_text}). We did not change the 24 h interval, ±3 h "
            "matching tolerance, environmental product, or support thresholds."
        )
        discussion = (
            "Because the registered phase-retention contrast was not estimable, "
            "the industrial-development analysis contributes no inference about "
            "whether the independently observed actuation attenuation propagates "
            "into lambda. The previously frozen movement-control permeability "
            "contrast remains valid, while the forcing-to-retention link remains "
            "open rather than being rescued by retuning the analysis."
        )
        abstract = (
            "The preregistered within-taxon lambda perturbation was not "
            "estimable under the frozen reconstruction and support criteria."
        )
        conclusion = (
            "The within-taxon forcing-to-lambda test remained unresolved under "
            "its frozen criteria, so no phase-retention response to development "
            "is inferred."
        )
        claim_state = {
            "scientific_result": result_class,
            "lambda_shift_supported": False,
            "wrong_direction": False,
            "estimable": False,
            "cross_taxon_lambda_synthesis_changed": False,
            "actuator_result_changed": False,
        }
        return results, discussion, abstract, conclusion, claim_state

    gate = payload["gate"]
    obs = gate["observation"]
    lam_a = obs["lambda_a"]
    lam_b = obs["lambda_b"]
    delta = gate["lambda_difference_b_minus_a"]
    p = obs.get("p_difference")

    numeric = (
        f"lambda_small={_fmt(lam_a)}, lambda_large={_fmt(lam_b)}, "
        f"Delta lambda={_fmt(delta)}, p={_fmt(p)}"
    )

    if result_class == "PASS":
        results = (
            f"Under the frozen V061 primary-successor reconstruction, the "
            f"small-development and large-development populations had {numeric}. "
            "The preregistered prediction that phase retention would be greater "
            "under large-development forcing therefore **passed**. The result is "
            "a within-taxon forcing contrast and is not counted as an additional "
            "cross-taxon lambda replication."
        )
        discussion = (
            "The Aikens perturbation links two independently evaluated layers of "
            "the controller framework. Large-development forcing had already been "
            "associated with attenuated movement-control permeability, and the "
            "prospective phase analysis now shows greater retention of incoming "
            "phase error on the frozen 24 h coordinate. This concordance is "
            "consistent with an actuation constraint propagating into realized "
            "phase correction, but it does not identify a causal equality between "
            "the permeability proxy G and lambda, nor does it imply a universal "
            "forcing response across taxa."
        )
        abstract = (
            f"The preregistered within-taxon forcing test also supported greater "
            f"phase retention under large development "
            f"(Delta lambda={_fmt(delta)}, p={_fmt(p)})."
        )
        conclusion = (
            "Within mule deer, the preregistered forcing perturbation linked "
            "independently observed actuation attenuation with greater retained "
            "phase error, while remaining separate from the cross-taxon synthesis."
        )
        claim_state = {
            "scientific_result": result_class,
            "lambda_shift_supported": True,
            "wrong_direction": False,
            "estimable": True,
            "cross_taxon_lambda_synthesis_changed": False,
            "actuator_result_changed": False,
        }
    elif result_class == "FAIL_WRONG_DIRECTION":
        results = (
            f"Under the frozen V061 primary-successor reconstruction, the "
            f"small-development and large-development populations had {numeric}. "
            "The preregistered prediction that large-development forcing would "
            "increase phase retention therefore **failed in direction**. The "
            "previously supported movement-control permeability contrast is "
            "retained, but it did not propagate into greater lambda as predicted."
        )
        discussion = (
            "This outcome separates actuator attenuation from the phase-retention "
            "coordinate even within one taxon. Industrial development can alter a "
            "measured movement response without producing the preregistered increase "
            "in retained phase error. The result therefore strengthens the need to "
            "treat actuators and lambda as distinct empirical gates; it does not "
            "invalidate the shared within-system phase-retention estimator form observed "
            "across the three direct taxa; raw cross-system magnitudes remain "
            "interval-scale dependent."
        )
        abstract = (
            "The preregistered within-taxon forcing-to-lambda prediction failed "
            "in direction despite independently supported actuator attenuation."
        )
        conclusion = (
            "Within mule deer, actuator attenuation did not propagate into the "
            "preregistered increase in phase retention, reinforcing that actuator "
            "and lambda are distinct empirical levels."
        )
        claim_state = {
            "scientific_result": result_class,
            "lambda_shift_supported": False,
            "wrong_direction": True,
            "estimable": True,
            "cross_taxon_lambda_synthesis_changed": False,
            "actuator_result_changed": False,
        }
    else:
        results = (
            f"Under the frozen V061 primary-successor reconstruction, the "
            f"small-development and large-development populations had {numeric}. "
            "Although the point contrast was in the preregistered direction, the "
            "registered inferential support criterion was not met. The prospective "
            "lambda perturbation therefore **failed the support gate**, and we do "
            "not claim a development-associated shift in phase retention."
        )
        discussion = (
            "The Aikens system therefore retains a supported actuator contrast "
            "without a supported shift in lambda. This is informative because it "
            "shows that a change in one movement-control proxy need not be detectable "
            "as a change in phase retention at the frozen 24 h scale. Actuator "
            "architecture and phase retention remain separate levels of inference."
        )
        abstract = (
            "The preregistered within-taxon forcing-to-lambda contrast pointed "
            "in the predicted direction but did not pass the inferential support gate."
        )
        conclusion = (
            "Within mule deer, the independently supported actuator attenuation "
            "was not accompanied by a supported shift in phase retention at the "
            "frozen 24 h scale."
        )
        claim_state = {
            "scientific_result": result_class,
            "lambda_shift_supported": False,
            "wrong_direction": False,
            "estimable": True,
            "cross_taxon_lambda_synthesis_changed": False,
            "actuator_result_changed": False,
        }

    claim_state.update(
        {
            "lambda_small": lam_a,
            "lambda_large": lam_b,
            "delta_lambda_large": delta,
            "p_difference": p,
        }
    )
    return results, discussion, abstract, conclusion, claim_state


def replace_between(text: str, start: str, end: str, body: str) -> str:
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError(f"expected exactly one marker pair: {start} / {end}")
    left, rest = text.split(start, 1)
    _, right = rest.split(end, 1)
    return left + start + "\n" + body.strip() + "\n" + end + right


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--baseline", type=Path, required=True)
    p.add_argument("--result-json", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--claim-state-output", type=Path, required=True)
    args = p.parse_args()

    baseline = args.baseline.read_text(encoding="utf-8")
    payload = json.loads(args.result_json.read_text(encoding="utf-8"))
    results, discussion, abstract, conclusion, claim_state = render_blocks(payload)

    rendered = replace_between(
        baseline, RESULTS_START, RESULTS_END, results
    )
    rendered = replace_between(
        rendered, DISCUSSION_START, DISCUSSION_END, discussion
    )
    rendered = replace_between(
        rendered, ABSTRACT_START, ABSTRACT_END, abstract
    )
    rendered = replace_between(
        rendered, CONCLUSION_START, CONCLUSION_END, conclusion
    )

    integrated_preoutcome_status = (
        "**Status:** integrated ecology manuscript v1, PREOUTCOME"
    )
    if integrated_preoutcome_status in rendered:
        rendered = rendered.replace(
            integrated_preoutcome_status,
            "**Status:** integrated ecology manuscript v1, OUTCOME-RENDERED",
            1,
        )

    if "AIKENS LAMBDA RESULT PENDING" in rendered:
        raise SystemExit("unresolved Aikens result placeholder remains")
    if "AIKENS LAMBDA DISCUSSION PENDING" in rendered:
        raise SystemExit("unresolved Aikens discussion placeholder remains")
    if "AIKENS LAMBDA ABSTRACT PENDING" in rendered:
        raise SystemExit("unresolved Aikens abstract placeholder remains")
    if "AIKENS LAMBDA CONCLUSION PENDING" in rendered:
        raise SystemExit("unresolved Aikens conclusion placeholder remains")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")

    claim_state.update(
        {
            "result_source": str(args.result_json),
            "baseline_manuscript": str(args.baseline),
            "retuning_permitted": False,
            "aikens_added_to_cross_taxon_lambda_synthesis": False,
        }
    )
    args.claim_state_output.parent.mkdir(parents=True, exist_ok=True)
    args.claim_state_output.write_text(
        json.dumps(claim_state, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    print(args.claim_state_output)
    print("AIKENS_MANUSCRIPT_RESULT=" + claim_state["scientific_result"])


if __name__ == "__main__":
    main()
