"""Gate outcome opening for predeclared congener separation-of-function assays."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CongenerOutcomeOpeningReceipt:
    task_scale_frozen_preoutcome: bool
    genotoxicity_scale_frozen_preoutcome: bool
    direct_mu_scale_frozen_preoutcome: bool
    task_materiality_threshold_frozen_preoutcome: bool
    genotoxicity_materiality_threshold_frozen_preoutcome: bool
    direct_mu_materiality_threshold_frozen_preoutcome: bool
    uncertainty_construction_frozen_preoutcome: bool
    analysis_window_frozen_preoutcome: bool
    candidate_set_frozen_preoutcome: bool
    outcome_data_already_opened: bool

    @property
    def all_measurement_semantics_frozen(self) -> bool:
        return all(
            (
                self.task_scale_frozen_preoutcome,
                self.genotoxicity_scale_frozen_preoutcome,
                self.direct_mu_scale_frozen_preoutcome,
                self.uncertainty_construction_frozen_preoutcome,
                self.analysis_window_frozen_preoutcome,
                self.candidate_set_frozen_preoutcome,
            )
        )

    @property
    def all_materiality_thresholds_frozen(self) -> bool:
        return all(
            (
                self.task_materiality_threshold_frozen_preoutcome,
                self.genotoxicity_materiality_threshold_frozen_preoutcome,
                self.direct_mu_materiality_threshold_frozen_preoutcome,
            )
        )

    @property
    def outcome_opening_allowed(self) -> bool:
        return bool(
            self.all_measurement_semantics_frozen
            and self.all_materiality_thresholds_frozen
            and not self.outcome_data_already_opened
        )


def adjudicate_congener_outcome_opening(
    receipt: CongenerOutcomeOpeningReceipt,
) -> tuple[bool, tuple[str, ...]]:
    checks = (
        (receipt.task_scale_frozen_preoutcome, "TASK_SCALE_NOT_FROZEN"),
        (receipt.genotoxicity_scale_frozen_preoutcome, "GENOTOXICITY_SCALE_NOT_FROZEN"),
        (receipt.direct_mu_scale_frozen_preoutcome, "DIRECT_MU_SCALE_NOT_FROZEN"),
        (
            receipt.task_materiality_threshold_frozen_preoutcome,
            "TASK_MATERIALITY_THRESHOLD_NOT_FROZEN",
        ),
        (
            receipt.genotoxicity_materiality_threshold_frozen_preoutcome,
            "GENOTOXICITY_MATERIALITY_THRESHOLD_NOT_FROZEN",
        ),
        (
            receipt.direct_mu_materiality_threshold_frozen_preoutcome,
            "DIRECT_MU_MATERIALITY_THRESHOLD_NOT_FROZEN",
        ),
        (
            receipt.uncertainty_construction_frozen_preoutcome,
            "UNCERTAINTY_CONSTRUCTION_NOT_FROZEN",
        ),
        (receipt.analysis_window_frozen_preoutcome, "ANALYSIS_WINDOW_NOT_FROZEN"),
        (receipt.candidate_set_frozen_preoutcome, "CANDIDATE_SET_NOT_FROZEN"),
    )
    blockers = [label for passed, label in checks if not passed]
    if receipt.outcome_data_already_opened:
        blockers.append("OUTCOME_ALREADY_OPENED_BEFORE_FULL_FREEZE")
    allowed = receipt.outcome_opening_allowed and not blockers
    return allowed, tuple(blockers)
