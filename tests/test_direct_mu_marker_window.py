from src.direct_mu_marker_window import (
    DirectMuMarkerWindowReceipt,
    adjudicate_direct_mu_marker_window,
)


def base_receipt(**updates):
    data = dict(
        entry_marker_id="SCO7662_cmlR2_178kb_from_right_end",
        intermediate_marker_id="SCO7350_503kb_from_right_end",
        deep_marker_id="SCO7036_argG_841kb_from_right_end",
        core_reference_id="SCO3879_dnaA_oriC_core",
        start_hour=72,
        end_hour=120,
        whole_biomass_state_channel_declared=True,
        genotype_time_matched_intact_baseline_declared=True,
        terminal_core_dosage_calibration_declared=True,
        entry_marker_nearest_terminal_declared=True,
        severity_order_declared=True,
        candidate_outcomes_used_to_select_panel=False,
        candidate_outcomes_used_to_select_window=False,
        realization_channel_independent_declared=True,
        realization_channel_frozen_preoutcome=False,
    )
    data.update(updates)
    return DirectMuMarkerWindowReceipt(**data)


def test_registered_panel_and_72_to_120_window_freeze_state_channel_only():
    r = base_receipt()
    state_ready, full_ready, blockers = adjudicate_direct_mu_marker_window(r)
    assert r.marker_panel_frozen
    assert r.sampling_window_frozen
    assert state_ready
    assert not full_ready
    assert blockers == ("REALIZATION_CHANNEL_NOT_FROZEN",)


def test_freezing_independent_realization_channel_is_separately_required():
    r = base_receipt(realization_channel_frozen_preoutcome=True)
    state_ready, full_ready, blockers = adjudicate_direct_mu_marker_window(r)
    assert state_ready
    assert full_ready
    assert blockers == ()


def test_candidate_outcome_selected_panel_is_rejected():
    r = base_receipt(candidate_outcomes_used_to_select_panel=True)
    assert not r.marker_panel_frozen
    state_ready, full_ready, blockers = adjudicate_direct_mu_marker_window(r)
    assert not state_ready
    assert not full_ready
    assert "MARKER_PANEL_NOT_FROZEN" in blockers


def test_candidate_outcome_selected_window_is_rejected():
    r = base_receipt(candidate_outcomes_used_to_select_window=True)
    assert not r.sampling_window_frozen
    state_ready, full_ready, blockers = adjudicate_direct_mu_marker_window(r)
    assert not state_ready
    assert not full_ready
    assert "SAMPLING_WINDOW_NOT_FROZEN" in blockers


def test_invalid_window_is_not_frozen():
    r = base_receipt(start_hour=120, end_hour=72)
    assert not r.sampling_window_frozen


def test_core_reference_must_be_distinct_from_terminal_markers():
    r = base_receipt(core_reference_id="SCO7662_cmlR2_178kb_from_right_end")
    assert not r.marker_panel_frozen


def test_dosage_calibration_and_matched_intact_baseline_are_required():
    assert not base_receipt(terminal_core_dosage_calibration_declared=False).marker_panel_frozen
    assert not base_receipt(genotype_time_matched_intact_baseline_declared=False).marker_panel_frozen
