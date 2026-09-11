"""Pre-outcome marker/window contract for Streptomyces direct-mu measurement.

This module defines the registered DNA-state panel and primary interval. It does
not estimate mu and it does not certify the independent realization channel r=d/g.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DirectMuMarkerWindowReceipt:
    entry_marker_id: str
    intermediate_marker_id: str
    deep_marker_id: str
    core_reference_id: str
    start_hour: int
    end_hour: int
    whole_biomass_state_channel_declared: bool
    genotype_time_matched_intact_baseline_declared: bool
    terminal_core_dosage_calibration_declared: bool
    entry_marker_nearest_terminal_declared: bool
    severity_order_declared: bool
    candidate_outcomes_used_to_select_panel: bool
    candidate_outcomes_used_to_select_window: bool
    realization_channel_independent_declared: bool
    realization_channel_frozen_preoutcome: bool

    @property
    def marker_panel_frozen(self) -> bool:
        ids = (
            self.entry_marker_id,
            self.intermediate_marker_id,
            self.deep_marker_id,
            self.core_reference_id,
        )
        return bool(
            all(isinstance(x, str) and x.strip() for x in ids)
            and len(set(ids)) == 4
            and self.whole_biomass_state_channel_declared
            and self.genotype_time_matched_intact_baseline_declared
            and self.terminal_core_dosage_calibration_declared
            and self.entry_marker_nearest_terminal_declared
            and self.severity_order_declared
            and not self.candidate_outcomes_used_to_select_panel
        )

    @property
    def sampling_window_frozen(self) -> bool:
        return bool(
            isinstance(self.start_hour, int)
            and isinstance(self.end_hour, int)
            and self.start_hour >= 0
            and self.end_hour > self.start_hour
            and not self.candidate_outcomes_used_to_select_window
        )

    @property
    def state_channel_frozen(self) -> bool:
        return self.marker_panel_frozen and self.sampling_window_frozen

    @property
    def direct_mu_fully_ready(self) -> bool:
        # The registered state channel is not enough: r=d/g must be frozen and
        # independently measured over the same interval/context.
        return bool(
            self.state_channel_frozen
            and self.realization_channel_independent_declared
            and self.realization_channel_frozen_preoutcome
        )


def adjudicate_direct_mu_marker_window(
    receipt: DirectMuMarkerWindowReceipt,
) -> tuple[bool, bool, tuple[str, ...]]:
    blockers: list[str] = []
    if not receipt.marker_panel_frozen:
        blockers.append("MARKER_PANEL_NOT_FROZEN")
    if not receipt.sampling_window_frozen:
        blockers.append("SAMPLING_WINDOW_NOT_FROZEN")
    if not receipt.realization_channel_independent_declared:
        blockers.append("REALIZATION_CHANNEL_NOT_DECLARED_INDEPENDENT")
    if not receipt.realization_channel_frozen_preoutcome:
        blockers.append("REALIZATION_CHANNEL_NOT_FROZEN")
    return receipt.state_channel_frozen, receipt.direct_mu_fully_ready, tuple(blockers)
