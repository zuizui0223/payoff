"""Pre-outcome adjudication for prodiginine congener separation-of-function probes.

This module freezes the *logic* of C1 (task preservation) x C2
(genotoxic/direct-mu branch) before either registered congener probe has outcome
data. Numeric materiality thresholds remain assay-specific and must themselves
be frozen before outcome opening; this module never invents them.

All quantitative comparisons are oriented so that larger performance is better
for the focal task, while positive reduction values mean less genotoxicity or
less direct deletion-generation in the probe than in its registered control.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


def _q(value: object) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, str):
        return Fraction(value)
    raise ValueError("use an exact rational-compatible value")


def _band(value: tuple[object, object], name: str) -> tuple[Fraction, Fraction]:
    if not isinstance(value, tuple) or len(value) != 2:
        raise ValueError(f"{name} must be a two-element tuple")
    lo, hi = _q(value[0]), _q(value[1])
    if lo > hi:
        raise ValueError(f"{name} lower bound exceeds upper bound")
    return lo, hi


@dataclass(frozen=True)
class TaskPreservationReceipt:
    performance_difference_band: tuple[Fraction, Fraction]
    material_loss_tolerance: Fraction
    task_result: str
    boundary_contact: bool
    scope: str = "predeclared_task_noninferiority_gate"


def classify_task_preservation(
    performance_difference_band: tuple[object, object],
    *,
    material_loss_tolerance: object,
) -> TaskPreservationReceipt:
    """Classify task preservation from a closed difference band.

    The difference is `probe - control` on a predeclared higher-is-better task
    scale.  A loss larger than `delta >= 0` is material, so the non-inferiority
    boundary is `-delta`.

    Closed-boundary contact is deliberately unresolved:
    - preserved only if the *entire* band is strictly above `-delta`;
    - material_task_loss only if the *entire* band is strictly below `-delta`;
    - equality/contact/straddling is unresolved.
    """
    lo, hi = _band(performance_difference_band, "performance_difference_band")
    delta = _q(material_loss_tolerance)
    if delta < 0:
        raise ValueError("material_loss_tolerance must be nonnegative")
    boundary = -delta
    if lo > boundary:
        result = "preserved"
    elif hi < boundary:
        result = "material_task_loss"
    else:
        result = "unresolved"
    return TaskPreservationReceipt(
        performance_difference_band=(lo, hi),
        material_loss_tolerance=delta,
        task_result=result,
        boundary_contact=bool(lo <= boundary <= hi),
    )


@dataclass(frozen=True)
class ReductionEvidenceReceipt:
    reduction_band: tuple[Fraction, Fraction]
    material_reduction: Fraction
    result: str
    boundary_contact: bool
    scope: str = "predeclared_material_reduction_gate"


def classify_material_reduction(
    reduction_band: tuple[object, object],
    *,
    material_reduction: object,
) -> ReductionEvidenceReceipt:
    """Classify a positive-oriented reduction band against a strict threshold.

    `reduction = control - probe`, so positive values mean the probe is lower.
    `reduced` requires every compatible value to be strictly above the
    materiality threshold. `material_reduction_excluded` requires every value
    to be strictly below it. Contact or overlap remains unresolved.
    """
    lo, hi = _band(reduction_band, "reduction_band")
    delta = _q(material_reduction)
    if delta < 0:
        raise ValueError("material_reduction must be nonnegative")
    if lo > delta:
        result = "reduced"
    elif hi < delta:
        result = "material_reduction_excluded"
    else:
        result = "unresolved"
    return ReductionEvidenceReceipt(
        reduction_band=(lo, hi),
        material_reduction=delta,
        result=result,
        boundary_contact=bool(lo <= delta <= hi),
    )


@dataclass(frozen=True)
class GenotoxicGenerationBranchReceipt:
    genotoxicity_result: str
    direct_mu_result: str
    branch_result: str
    scope: str = "joint_genotoxicity_direct_mu_branch_gate"


def adjudicate_genotoxic_generation_branch(
    genotoxicity_result: str,
    direct_mu_result: str,
) -> GenotoxicGenerationBranchReceipt:
    allowed = {"reduced", "material_reduction_excluded", "unresolved"}
    if genotoxicity_result not in allowed or direct_mu_result not in allowed:
        raise ValueError("branch results must be reduced, material_reduction_excluded, or unresolved")

    pair = (genotoxicity_result, direct_mu_result)
    if pair == ("reduced", "reduced"):
        branch = "genotoxic_generation_reduced"
    elif pair == ("material_reduction_excluded", "material_reduction_excluded"):
        branch = "registered_route_not_supported"
    elif "unresolved" in pair:
        branch = "unresolved"
    else:
        branch = "genotoxic_mu_discordant"
    return GenotoxicGenerationBranchReceipt(
        genotoxicity_result=genotoxicity_result,
        direct_mu_result=direct_mu_result,
        branch_result=branch,
    )


@dataclass(frozen=True)
class CongenerSOFOutcomeReceipt:
    task_result: str
    genotoxic_generation_branch_result: str
    outcome_class: str
    separation_of_function_supported: bool
    mechanism_signal_supported: bool
    task_match_supported: bool
    matched_s_promoted: bool = False
    architecture_mapping_promoted: bool = False
    generic_game_promoted: bool = False
    eta_promoted: bool = False
    e1_promoted: bool = False
    scope: str = "prodiginine_congener_C1_x_C2_preoutcome_adjudication"


def adjudicate_congener_sof_outcome(
    task_result: str,
    genotoxic_generation_branch_result: str,
) -> CongenerSOFOutcomeReceipt:
    task_allowed = {"preserved", "material_task_loss", "unresolved"}
    branch_allowed = {
        "genotoxic_generation_reduced",
        "registered_route_not_supported",
        "genotoxic_mu_discordant",
        "unresolved",
    }
    if task_result not in task_allowed:
        raise ValueError("unknown task_result")
    if genotoxic_generation_branch_result not in branch_allowed:
        raise ValueError("unknown genotoxic_generation_branch_result")

    if "unresolved" in (task_result, genotoxic_generation_branch_result):
        outcome = "INCOMPLETE_OR_UNRESOLVED_SOF"
    elif genotoxic_generation_branch_result == "genotoxic_mu_discordant":
        outcome = "GENOTOXIC_MU_DISCORDANCE_SOF_UNRESOLVED"
    elif task_result == "preserved" and genotoxic_generation_branch_result == "genotoxic_generation_reduced":
        outcome = "SEPARATION_OF_FUNCTION_SUPPORTED"
    elif task_result == "preserved" and genotoxic_generation_branch_result == "registered_route_not_supported":
        outcome = "TASK_PRESERVED_REGISTERED_GENOTOXIC_GENERATION_ROUTE_NOT_SUPPORTED"
    elif task_result == "material_task_loss" and genotoxic_generation_branch_result == "genotoxic_generation_reduced":
        outcome = "MECHANISM_SIGNAL_PRESENT_BUT_TASK_CONFOUNDED"
    else:
        outcome = "CANDIDATE_FAILS_TASK_AND_REGISTERED_ROUTE_CRITERIA"

    sof = outcome == "SEPARATION_OF_FUNCTION_SUPPORTED"
    mechanism = genotoxic_generation_branch_result == "genotoxic_generation_reduced"
    task = task_result == "preserved"
    return CongenerSOFOutcomeReceipt(
        task_result=task_result,
        genotoxic_generation_branch_result=genotoxic_generation_branch_result,
        outcome_class=outcome,
        separation_of_function_supported=sof,
        mechanism_signal_supported=mechanism,
        task_match_supported=task,
    )
