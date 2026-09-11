"""Prospective design for independently estimating pre-existing D realization d.

The design is intentionally separate from the congener outcome state channel.
It freezes how D reference material will be selected and how class-wise
realization uncertainty will be enveloped before any congener outcome is opened.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class DirectMuRealizationDesignReceipt:
    start_hour: int
    end_hour: int
    realization_unit: str
    pre_existing_D_verified_by_marker_panel: bool
    same_medium_and_context_as_state_channel: bool
    final_mixed_state_fraction_reused_to_estimate_d: bool
    candidate_outcomes_used_to_select_reference_panel: bool
    entry_class_predeclared: bool
    intermediate_class_predeclared: bool
    deep_class_predeclared: bool
    minimum_independent_references_per_class: int
    core_equivalent_fold_change_declared: bool
    reference_panel_materialized: bool
    reference_panel_qualified: bool

    @property
    def design_frozen_preoutcome(self) -> bool:
        return bool(
            self.start_hour == 72
            and self.end_hour == 120
            and self.realization_unit == "CORE_CHROMOSOME_EQUIVALENT_FOLD_CHANGE"
            and self.pre_existing_D_verified_by_marker_panel
            and self.same_medium_and_context_as_state_channel
            and not self.final_mixed_state_fraction_reused_to_estimate_d
            and not self.candidate_outcomes_used_to_select_reference_panel
            and self.entry_class_predeclared
            and self.intermediate_class_predeclared
            and self.deep_class_predeclared
            and self.minimum_independent_references_per_class >= 2
            and self.core_equivalent_fold_change_declared
        )

    @property
    def realization_channel_ready(self) -> bool:
        return bool(
            self.design_frozen_preoutcome
            and self.reference_panel_materialized
            and self.reference_panel_qualified
        )


def envelope_d_bands(reference_bands) -> tuple[Fraction, Fraction]:
    """Return the conservative d envelope across predeclared qualified references."""
    bands = []
    for band in reference_bands:
        if len(band) != 2:
            raise ValueError("each d band must contain lower and upper endpoints")
        lo = band[0] if isinstance(band[0], Fraction) else Fraction(band[0])
        hi = band[1] if isinstance(band[1], Fraction) else Fraction(band[1])
        if lo < 0 or hi < 0 or lo > hi:
            raise ValueError("d bands must be ordered and nonnegative")
        bands.append((lo, hi))
    if not bands:
        raise ValueError("at least one qualified D reference band is required")
    return min(lo for lo, _ in bands), max(hi for _, hi in bands)
