"""Candidate gate for prodiginine congener separation-of-function probes.

This module belongs to the Streptomyces architecture-mechanism sublane.
It deliberately distinguishes a *biochemical congener probe* from a certified
separation-of-function architecture counterfactual.

Changing the prodiginine congener profile while retaining some prodiginine
output is useful because it avoids the strongest task-loss confound of a full
RED knockout.  It is not enough, however, to establish that antibacterial task
is preserved, that DNA-damaging activity has changed, or that terminal genomic
specialist generation (`mu`) has changed.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProdiginineCongenerProbeReceipt:
    probe_id: str
    support_reference: str
    same_background_declared: bool
    congener_profile_changed_declared: bool
    prodiginine_output_not_fully_abolished_declared: bool
    candidate_selected_before_mu_outcome_declared: bool
    gross_development_matched_declared: bool
    focal_antibacterial_task_preserved_declared: bool
    dna_damage_or_genotoxicity_difference_measured_declared: bool
    direct_mu_difference_measured_declared: bool
    focal_task_assay_same_context_declared: bool
    mu_assay_same_context_declared: bool

    @property
    def biochemical_congener_probe_ready(self) -> bool:
        return all(
            (
                self.same_background_declared,
                self.congener_profile_changed_declared,
                self.prodiginine_output_not_fully_abolished_declared,
                self.candidate_selected_before_mu_outcome_declared,
            )
        )

    @property
    def task_preservation_supported(self) -> bool:
        return all(
            (
                self.gross_development_matched_declared,
                self.focal_antibacterial_task_preserved_declared,
                self.focal_task_assay_same_context_declared,
            )
        )

    @property
    def genotoxic_branch_supported(self) -> bool:
        return all(
            (
                self.dna_damage_or_genotoxicity_difference_measured_declared,
                self.direct_mu_difference_measured_declared,
                self.mu_assay_same_context_declared,
            )
        )

    @property
    def separation_of_function_certified(self) -> bool:
        return all(
            (
                self.biochemical_congener_probe_ready,
                self.task_preservation_supported,
                self.genotoxic_branch_supported,
            )
        )


@dataclass(frozen=True)
class ProdiginineCongenerProbeAdjudication:
    biochemical_congener_probe_ready: bool
    task_preservation_supported: bool
    genotoxic_branch_supported: bool
    separation_of_function_certified: bool
    blockers: tuple[str, ...]
    matched_s_promoted: bool = False
    architecture_mapping_promoted: bool = False
    generic_game_promoted: bool = False
    eta_promoted: bool = False
    e1_promoted: bool = False
    scope: str = "prodiginine_congener_separation_of_function_candidate_gate_v1"


def _nonempty(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def adjudicate_prodiginine_congener_probe(
    receipt: ProdiginineCongenerProbeReceipt,
) -> ProdiginineCongenerProbeAdjudication:
    _nonempty(receipt.probe_id, "probe_id")
    _nonempty(receipt.support_reference, "support_reference")
    if not receipt.candidate_selected_before_mu_outcome_declared:
        raise ValueError("congener probe must be selected before direct-mu outcome")

    checks = (
        (receipt.same_background_declared, "BACKGROUND_NOT_MATCHED"),
        (receipt.congener_profile_changed_declared, "CONGENER_PROFILE_NOT_CHANGED"),
        (
            receipt.prodiginine_output_not_fully_abolished_declared,
            "PRODIGININE_OUTPUT_FULLY_ABOLISHED_OR_NOT_SHOWN_RETAINED",
        ),
        (
            receipt.gross_development_matched_declared,
            "GROSS_DEVELOPMENT_MATCH_NOT_RECOVERED",
        ),
        (
            receipt.focal_antibacterial_task_preserved_declared,
            "FOCAL_ANTIBACTERIAL_TASK_PRESERVATION_NOT_MEASURED",
        ),
        (
            receipt.focal_task_assay_same_context_declared,
            "TASK_ASSAY_CONTEXT_NOT_MATCHED",
        ),
        (
            receipt.dna_damage_or_genotoxicity_difference_measured_declared,
            "GENOTOXICITY_DIFFERENCE_NOT_MEASURED",
        ),
        (
            receipt.direct_mu_difference_measured_declared,
            "DIRECT_MU_DIFFERENCE_NOT_MEASURED",
        ),
        (
            receipt.mu_assay_same_context_declared,
            "MU_ASSAY_CONTEXT_NOT_MATCHED",
        ),
    )
    blockers = tuple(label for passed, label in checks if not passed)
    return ProdiginineCongenerProbeAdjudication(
        biochemical_congener_probe_ready=receipt.biochemical_congener_probe_ready,
        task_preservation_supported=receipt.task_preservation_supported,
        genotoxic_branch_supported=receipt.genotoxic_branch_supported,
        separation_of_function_certified=receipt.separation_of_function_certified,
        blockers=blockers,
    )
