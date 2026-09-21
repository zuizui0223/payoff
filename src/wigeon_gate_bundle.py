"""Assemble the source-backed wigeon two-gate result without an omnibus score.

Required inputs:
- primary prospective phase-retention evaluation;
- stronger |lambda|<0.75 evaluation;
- W2 stopover prospective actuator evaluation.

Optional W3 travel-speed / W4 route-moderation diagnostics are carried as
separate descriptive diagnostics and never promoted to formal actuator gates.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class WigeonGateBundle:
    system_name: str
    primary_lambda_passed: bool
    lambda_retention: float
    lambda_se: float | None
    p_vs_no_correction: float | None
    strong_contraction_passed: bool
    stopover_actuator_passed: bool
    two_gate_class: str
    travel_speed_diagnostic: dict[str, Any] | None
    distance_moderation_diagnostic: dict[str, Any] | None

    @property
    def omnibus_score(self):
        raise AttributeError(
            "PAYOFF-B intentionally defines no omnibus wigeon score; "
            "inspect lambda, strong-forecast, actuator, and diagnostics separately"
        )


def assemble_wigeon_gate_bundle(
    primary_phase_receipt: dict[str, Any],
    strong_phase_receipt: dict[str, Any],
    stopover_actuator_receipt: dict[str, Any],
    *,
    travel_speed_diagnostic: dict[str, Any] | None = None,
    distance_moderation_diagnostic: dict[str, Any] | None = None,
) -> WigeonGateBundle:
    """Combine already evaluated source-backed receipts without re-scoring them."""

    primary_gate = primary_phase_receipt.get("gate")
    strong_gate = strong_phase_receipt.get("gate")
    stopover_gate = stopover_actuator_receipt.get("gate")
    if primary_gate is None or strong_gate is None or stopover_gate is None:
        raise ValueError("all three source receipts must contain gate payloads")

    systems = {
        str(primary_phase_receipt.get("system_name", "")),
        str(strong_phase_receipt.get("system_name", "")),
        str(stopover_actuator_receipt.get("system_name", "")),
    }
    if systems != {"Eurasian wigeon"}:
        raise ValueError(
            "wigeon gate bundle requires three Eurasian-wigeon source receipts"
        )

    phase_test_ids = {
        str(primary_phase_receipt.get("independent_test_id", "")),
        str(strong_phase_receipt.get("independent_test_id", "")),
    }
    if phase_test_ids != {"wigeon_vantoor2021_W1"}:
        raise ValueError(
            "primary and strong phase receipts must use the frozen W1 test ID"
        )

    if str(
        stopover_actuator_receipt.get("independent_test_id", "")
    ) != "wigeon_vantoor2021_W2_stopover":
        raise ValueError(
            "stopover receipt must use the frozen W2 stopover test ID"
        )

    if not bool(
        primary_phase_receipt.get(
            "prospective_contract_satisfied",
            False,
        )
    ):
        raise ValueError("primary W1 phase receipt is not prospective")
    if not bool(
        strong_phase_receipt.get(
            "prospective_contract_satisfied",
            False,
        )
    ):
        raise ValueError("strong W1 phase receipt is not prospective")
    if not bool(
        stopover_actuator_receipt.get(
            "prospective_contract_satisfied",
            False,
        )
    ):
        raise ValueError("W2 stopover receipt is not prospective")

    estimate = primary_gate.get("estimate", {})
    lambda_retention = float(estimate["lambda_retention"])
    lambda_se = (
        None
        if estimate.get("lambda_se") is None
        else float(estimate["lambda_se"])
    )
    p_vs_no_correction = (
        None
        if estimate.get("p_vs_no_correction") is None
        else float(estimate["p_vs_no_correction"])
    )

    primary_pass = bool(primary_gate["passed"])
    strong_pass = bool(strong_gate["passed"])
    stopover_pass = bool(
        stopover_gate["all_prospective_passed"]
    )

    if primary_pass and not stopover_pass:
        two_gate_class = "LAMBDA_PASS_ACTUATOR_FAIL"
    elif primary_pass and stopover_pass:
        two_gate_class = "LAMBDA_PASS_ACTUATOR_PASS"
    elif (not primary_pass) and stopover_pass:
        two_gate_class = "LAMBDA_FAIL_ACTUATOR_PASS"
    else:
        two_gate_class = "LAMBDA_FAIL_ACTUATOR_FAIL"

    return WigeonGateBundle(
        system_name="Eurasian wigeon",
        primary_lambda_passed=primary_pass,
        lambda_retention=lambda_retention,
        lambda_se=lambda_se,
        p_vs_no_correction=p_vs_no_correction,
        strong_contraction_passed=strong_pass,
        stopover_actuator_passed=stopover_pass,
        two_gate_class=two_gate_class,
        travel_speed_diagnostic=travel_speed_diagnostic,
        distance_moderation_diagnostic=(
            distance_moderation_diagnostic
        ),
    )
