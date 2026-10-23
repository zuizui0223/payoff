from scripts.simulate_stage_timing_window_null import simulate

def test_independent_duration_has_beta_one_without_censoring():
    r=simulate(draws=50000)
    assert abs(r["uncensored_stage_retention_slope"]-1)<.04
    assert r["original_tracking_fitted"] is False

def test_calendar_right_window_alone_induces_apparent_compression():
    r=simulate(draws=50000)
    assert .55<r["window_conditioned_stage_retention_slope"]<.80
    assert r["retained_draws"]<r["draws"]
    assert r["unmeasured_behavioral_feedback_in_simulation"]

def test_seed_is_deterministic():
    assert simulate(draws=1000)==simulate(draws=1000)
