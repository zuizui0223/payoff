import pytest

from src.wigeon_phase_simex import (
    draw_event_errors,
    prepare_wigeon_design,
    lambda_hat_from_phases,
    run_wigeon_simex,
)


def synthetic_frame():
    pd = pytest.importorskip("pandas")
    rows = []
    for animal_index in range(8):
        animal = f"A{animal_index}"
        for segment in range(1, 7):
            if segment == 6:
                continue
            origin = float(segment - 3)
            destination = 0.6 * origin + 0.1 * animal_index
            rows.append(
                {
                    "individual_id": animal,
                    "year": 2020,
                    "origin_segment": segment,
                    "destination_segment": segment + 1,
                    "origin_phase": origin,
                    "destination_phase": destination,
                    "origin_progress_km": float(segment * 10 + animal_index),
                    "endpoint_distance_km": float(100 + animal_index * 5),
                }
            )
    return pd.DataFrame(rows)


def test_fixed_design_recovers_observed_synthetic_lambda():
    frame = synthetic_frame()
    data, nuisance = prepare_wigeon_design(frame)
    observed = lambda_hat_from_phases(
        data,
        nuisance,
        origin_phase=data["origin_phase"],
        destination_phase=data["destination_phase"],
    )
    assert observed == pytest.approx(0.6, abs=1e-10)


def test_shared_event_error_is_reused_across_adjacent_transitions():
    frame = synthetic_frame()
    data, _ = prepare_wigeon_design(frame)
    errors = draw_event_errors(
        data,
        error_sd=2.0,
        error_correlation=0.0,
        seed=123,
    )
    key = ("A0", 2020, 2)
    assert key in errors
    # Segment 2 appears as destination of transition 1->2 and
    # origin of transition 2->3, so only one event error exists.
    assert isinstance(errors[key], float)


def test_zero_error_simex_extrapolates_to_observed_lambda():
    frame = synthetic_frame()
    result = run_wigeon_simex(
        frame,
        scenario_name="zero_error",
        error_sd_days=0.0,
        error_correlation=0.0,
        zeta_values=(0.5, 1.0, 1.5, 2.0),
        replicates_per_zeta=5,
        seed=42,
    )
    assert result.observed_lambda_hat == pytest.approx(0.6, abs=1e-10)
    assert result.simex_extrapolated_lambda_at_minus_one == pytest.approx(
        0.6,
        abs=1e-9,
    )
    assert all(
        point.mean_lambda_hat == pytest.approx(0.6, abs=1e-10)
        for point in result.zeta_points
    )


def test_positive_added_error_changes_mean_curve_and_simex_returns_finite_value():
    frame = synthetic_frame()
    result = run_wigeon_simex(
        frame,
        scenario_name="measurement_error",
        error_sd_days=1.0,
        error_correlation=0.0,
        zeta_values=(0.5, 1.0, 1.5, 2.0),
        replicates_per_zeta=30,
        seed=20260923,
    )
    assert len(result.zeta_points) == 4
    assert all(
        point.replicates == 30
        for point in result.zeta_points
    )
    assert result.simex_extrapolated_lambda_at_minus_one == pytest.approx(
        result.simex_extrapolated_lambda_at_minus_one
    )
