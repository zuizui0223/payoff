"""Synthetic source-only tests; no empirical inference about wild migrants."""

from dataclasses import replace
from datetime import datetime, timedelta, timezone
import random
import pytest

from src.decision_time_forecast_gate import (
    TimedEnvironmentalRecord,
    gaussian_historical_policy_transfer,
    heldout_incremental_forecast,
    validate_decision_time_records,
)


def make_row(pair, year, origin, checkpoint, target, *, late=False):
    date = datetime(year, 4, 10, tzinfo=timezone.utc)

    def at(days):
        return (date + timedelta(days=days)).isoformat()

    return TimedEnvironmentalRecord(
        pair_id=pair, seasonal_year=year, origin_cue=origin,
        checkpoint_cue=checkpoint, downstream_onset=target,
        origin_available_at=at(-15),
        checkpoint_available_at=at(1 if late else -1),
        action_decision_at=at(0), downstream_onset_available_at=at(20),
        origin_provenance="origin conditions observable before migration",
        checkpoint_provenance="checkpoint instrument before departure",
    )


def synthetic_records(seed=1207, checkpoint_coef=3.0):
    rng = random.Random(seed)
    out = []
    for year in range(2000, 2012):
        for i in range(6):
            x, z = rng.gauss(0, 1), rng.gauss(0, 1)
            y = 11 + 1.1 * x + checkpoint_coef * z + rng.gauss(0, 0.15)
            out.append(make_row(f"pair{i}", year, x, z, y))
    return out


def test_useful_checkpoint_adds_real_heldout_prediction():
    data = synthetic_records()
    result = heldout_incremental_forecast(
        data, train_years=range(2000, 2008), test_years=range(2008, 2012)
    )
    assert result.n_train == 48 and result.n_test == 24
    assert result.n_spatial_pairs == 6
    assert result.checkpoint_incremental_gain > 6.0
    assert result.refreshed_mse < 0.2


def test_uninformative_checkpoint_cannot_create_large_gain():
    result = heldout_incremental_forecast(
        synthetic_records(checkpoint_coef=0.0),
        train_years=range(2000, 2008), test_years=range(2008, 2012),
    )
    assert result.checkpoint_incremental_gain < 0.05


def test_species_replicated_shared_pair_year_fails():
    data = synthetic_records()
    with pytest.raises(ValueError, match="duplicate pair-year"):
        heldout_incremental_forecast(
            data + [data[0]], train_years=range(2000, 2008),
            test_years=range(2008, 2012),
        )


def test_retrospective_onset_does_not_become_an_available_checkpoint_cue():
    with pytest.raises(ValueError, match="leakage|chronology"):
        validate_decision_time_records([make_row("a", 2009, 2, 4, 5, late=True)])


def test_future_outcome_and_origin_timestamp_bounds():
    row = make_row("a", 2008, 0, 0, 1)
    with pytest.raises(ValueError):
        validate_decision_time_records([
            replace(row, downstream_onset_available_at=row.action_decision_at)
        ])
    with pytest.raises(ValueError):
        validate_decision_time_records([
            replace(row, origin_available_at=row.downstream_onset_available_at)
        ])


def test_unknown_time_zone_and_missing_cue_provenance_rejected():
    row = make_row("a", 2008, 0, 0, 1)
    with pytest.raises(ValueError, match="offset"):
        validate_decision_time_records([
            replace(row, action_decision_at="2008-04-10T00:00:00")
        ])
    with pytest.raises(ValueError, match="provenance"):
        validate_decision_time_records([
            replace(row, checkpoint_provenance="")
        ])


def test_training_years_must_precede_test_years():
    data = synthetic_records()
    for tr, te in [
        (range(2002, 2008), range(2007, 2010)),
        (range(2009, 2012), range(2000, 2008)),
    ]:
        with pytest.raises(ValueError, match="precede"):
            heldout_incremental_forecast(data, train_years=tr, test_years=te)


def test_registered_years_cannot_disappear_silently():
    with pytest.raises(ValueError, match="zero admitted"):
        heldout_incremental_forecast(
            synthetic_records(), train_years=[1999, 2000, 2001, 2002],
            test_years=[2008, 2009],
        )


def test_ridge_and_support_fail_closed():
    data = synthetic_records()
    with pytest.raises(ValueError, match="ridge"):
        heldout_incremental_forecast(
            data, train_years=range(2000, 2008),
            test_years=range(2008, 2012), ridge=0,
        )
    with pytest.raises(ValueError, match="too few"):
        heldout_incremental_forecast(
            [r for r in data if r.pair_id == "pair0"],
            train_years=[2000, 2001, 2002, 2003, 2004],
            test_years=[2008, 2009], ridge=0.1,
        )


def test_stronger_cross_site_correlation_can_coexist_with_bad_calibration():
    early, transported, oracle = gaussian_historical_policy_transfer(
        earlier_correlation=0.3, later_correlation=0.8,
        later_mean_shift=1.0,
    )
    assert early == pytest.approx(0.91)
    assert transported == pytest.approx(1.61)
    assert oracle == pytest.approx(0.36)


def test_no_shift_and_stronger_same_sign_correlation_not_artificially_harmful():
    early, transported, oracle = gaussian_historical_policy_transfer(
        earlier_correlation=0.3, later_correlation=0.8,
        later_mean_shift=0,
    )
    assert transported < early and oracle < transported


def test_environmental_gate_cannot_claim_behavior_or_fitness():
    result = heldout_incremental_forecast(
        synthetic_records(),
        train_years=range(2000, 2008),
        test_years=range(2008, 2012),
    )
    assert not hasattr(result, "behavioral_gain")
    assert not hasattr(result, "fitness_effect")


def test_exact_mean_shift_boundary_reverses_stronger_connectivity_benefit():
    from src.decision_time_forecast_gate import positive_connectivity_reversal_threshold

    boundary = positive_connectivity_reversal_threshold(
        earlier_correlation=0.3, later_correlation=0.8)
    assert boundary == pytest.approx((0.3)**0.5)
    for delta, direction in [(boundary - .01, -1), (boundary, 0), (boundary + .01, 1)]:
        earlier, transferred, _ = gaussian_historical_policy_transfer(
            earlier_correlation=.3, later_correlation=.8,
            later_mean_shift=delta)
        assert (transferred - earlier) * direction >= -1e-12
        if direction == 0:
            assert transferred == pytest.approx(earlier)


def test_reversal_threshold_rejects_negative_or_weaker_connectivity():
    from src.decision_time_forecast_gate import positive_connectivity_reversal_threshold
    with pytest.raises(ValueError):
        positive_connectivity_reversal_threshold(
            earlier_correlation=-.2, later_correlation=.8)
    with pytest.raises(ValueError):
        positive_connectivity_reversal_threshold(
            earlier_correlation=.9, later_correlation=.8)


def test_costly_optimally_calibrated_actor_can_undertrack_shifted_spring():
    from src.decision_time_forecast_gate import (
        fully_calibrated_costly_actor_mismatch,
        calibrated_cost_reversal_threshold,
    )
    threshold = calibrated_cost_reversal_threshold(
        earlier_correlation=.3, later_correlation=.8, effort_penalty=1)
    assert threshold == pytest.approx((1.65)**.5)
    before = fully_calibrated_costly_actor_mismatch(
        cue_target_correlation=.3, seasonal_mean_shift=0, effort_penalty=1)
    after = fully_calibrated_costly_actor_mismatch(
        cue_target_correlation=.8, seasonal_mean_shift=1.5, effort_penalty=1)
    assert before == pytest.approx(.9325)
    assert after == pytest.approx(1.0825)
    assert after > before


def test_zero_adjustment_cost_never_creates_a_false_reversal():
    from src.decision_time_forecast_gate import (
        fully_calibrated_costly_actor_mismatch,
        calibrated_cost_reversal_threshold,
    )
    assert fully_calibrated_costly_actor_mismatch(
        cue_target_correlation=.8, seasonal_mean_shift=2,
        effort_penalty=0) == pytest.approx(.36)
    with pytest.raises(ValueError):
        calibrated_cost_reversal_threshold(
            earlier_correlation=.3, later_correlation=.8,
            effort_penalty=0)
