from fractions import Fraction

import pytest

from src.direct_mu_realization_design import (
    DirectMuRealizationDesignReceipt,
    envelope_d_bands,
)


def base_receipt(**updates):
    data = dict(
        start_hour=72,
        end_hour=120,
        realization_unit="CORE_CHROMOSOME_EQUIVALENT_FOLD_CHANGE",
        pre_existing_D_verified_by_marker_panel=True,
        same_medium_and_context_as_state_channel=True,
        final_mixed_state_fraction_reused_to_estimate_d=False,
        candidate_outcomes_used_to_select_reference_panel=False,
        entry_class_predeclared=True,
        intermediate_class_predeclared=True,
        deep_class_predeclared=True,
        minimum_independent_references_per_class=2,
        core_equivalent_fold_change_declared=True,
        reference_panel_materialized=False,
        reference_panel_qualified=False,
    )
    data.update(updates)
    return DirectMuRealizationDesignReceipt(**data)


def test_design_can_be_frozen_before_reference_panel_is_materialized():
    r = base_receipt()
    assert r.design_frozen_preoutcome
    assert not r.realization_channel_ready


def test_materialized_and_qualified_panel_is_required_for_ready_channel():
    r = base_receipt(reference_panel_materialized=True, reference_panel_qualified=True)
    assert r.design_frozen_preoutcome
    assert r.realization_channel_ready


def test_using_final_mixed_state_fraction_breaks_independence():
    r = base_receipt(final_mixed_state_fraction_reused_to_estimate_d=True)
    assert not r.design_frozen_preoutcome
    assert not r.realization_channel_ready


def test_reference_selection_cannot_use_congener_outcomes():
    r = base_receipt(candidate_outcomes_used_to_select_reference_panel=True)
    assert not r.design_frozen_preoutcome


def test_all_three_predeclared_severity_classes_are_required():
    assert not base_receipt(entry_class_predeclared=False).design_frozen_preoutcome
    assert not base_receipt(intermediate_class_predeclared=False).design_frozen_preoutcome
    assert not base_receipt(deep_class_predeclared=False).design_frozen_preoutcome


def test_at_least_two_independent_references_per_class_are_required():
    assert not base_receipt(minimum_independent_references_per_class=1).design_frozen_preoutcome


def test_d_envelope_is_conservative_across_reference_bands():
    lo, hi = envelope_d_bands(
        [
            (Fraction(1, 5), Fraction(2, 5)),
            (Fraction(1, 10), Fraction(1, 2)),
            (Fraction(3, 10), Fraction(4, 5)),
        ]
    )
    assert lo == Fraction(1, 10)
    assert hi == Fraction(4, 5)


def test_invalid_or_empty_d_envelope_rejected():
    with pytest.raises(ValueError):
        envelope_d_bands([])
    with pytest.raises(ValueError):
        envelope_d_bands([(2, 1)])
    with pytest.raises(ValueError):
        envelope_d_bands([(-1, 1)])
