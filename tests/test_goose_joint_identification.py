import pytest

from src.goose_joint_identification import (
    climate_link_predictability,
    joint_predictability_recourse_coordinate,
    observed_recourse_envelope,
    remaining_duration_recourse,
)


def test_perfect_climate_link_has_unit_correlation_slope_and_loo_skill():
    x = [-3, -2, -1, 1, 2, 3]
    y = [-3, -2, -1, 1, 2, 3]
    out = climate_link_predictability(x, y)
    assert out.pearson_r == pytest.approx(1.0)
    assert out.regression_slope == pytest.approx(1.0)
    assert out.loo_skill == pytest.approx(1.0)
    assert out.nonnegative_loo_skill == pytest.approx(1.0)


def test_negative_or_useless_loo_skill_is_not_forced_positive():
    x = [-3, -2, -1, 1, 2, 3]
    y = [2, -1, 3, -3, 1, -2]
    out = climate_link_predictability(x, y)
    assert out.loo_skill <= 1.0
    assert 0.0 <= out.nonnegative_loo_skill <= 1.0


def test_recourse_envelope_sums_remaining_actuator_slack():
    env = observed_recourse_envelope(
        [
            [4, 5, 6, 7, 8],      # flight
            [1, 2, 3, 4, 5],      # stopover
            [8, 10, 12, 14, 16],  # flight
        ],
        component_names=["flight_1", "stopover_1", "flight_2"],
        lower_quantile=0.0,
        reference_quantile=0.5,
        upper_quantile=1.0,
    )
    assert env.components[0].advance_capacity == pytest.approx(2.0)
    assert env.components[1].advance_capacity == pytest.approx(2.0)
    assert env.components[2].advance_capacity == pytest.approx(4.0)
    assert env.stages[0].advance_capacity == pytest.approx(8.0)
    assert env.stages[1].advance_capacity == pytest.approx(6.0)
    assert env.stages[2].advance_capacity == pytest.approx(4.0)
    assert env.stages[3].advance_capacity == pytest.approx(0.0)
    assert [s.advance_fraction for s in env.stages] == pytest.approx(
        [1.0, 0.75, 0.5, 0.0]
    )


def test_stagewise_recourse_is_monotone_by_construction_but_component_slack_need_not_be():
    env = observed_recourse_envelope(
        [
            [1, 10, 11],
            [5, 6, 7],
            [1, 2, 20],
        ],
        lower_quantile=0.0,
        reference_quantile=0.5,
        upper_quantile=1.0,
    )
    values = [s.advance_capacity for s in env.stages]
    assert all(a >= b for a, b in zip(values, values[1:]))


def test_advance_and_delay_recourse_are_kept_separate():
    env = observed_recourse_envelope(
        [[2, 4, 5, 10, 20]],
        lower_quantile=0.0,
        reference_quantile=0.5,
        upper_quantile=1.0,
    )
    component = env.components[0]
    assert component.advance_capacity == pytest.approx(3.0)
    assert component.delay_capacity == pytest.approx(15.0)


def test_joint_coordinate_can_peak_at_intermediate_stage():
    rows = joint_predictability_recourse_coordinate(
        predictive_skills=[0.1, 0.5, 0.9, 1.0],
        recourse_fractions=[1.0, 0.8, 0.3, 0.0],
    )
    values = [row.actionable_predictability for row in rows]
    assert values == pytest.approx([0.1, 0.4, 0.27, 0.0])
    assert max(range(len(values)), key=values.__getitem__) == 1


def test_joint_coordinate_does_not_accept_negative_raw_skill():
    with pytest.raises(ValueError, match="predictive skills"):
        joint_predictability_recourse_coordinate(
            predictive_skills=[0.5, -0.1],
            recourse_fractions=[1.0, 0.5],
        )



def test_remaining_duration_recourse_uses_elapsed_time_not_absolute_arrival_date():
    rows = remaining_duration_recourse(
        [
            [8, 10, 12, 14, 16],
            [4, 5, 6, 7, 8],
            [1, 2, 2, 3, 4],
        ],
        lower_quantile=0.0,
        reference_quantile=0.5,
        upper_quantile=1.0,
    )
    assert rows[0].advance_capacity == pytest.approx(4.0)
    assert rows[1].advance_capacity == pytest.approx(2.0)
    assert rows[2].advance_capacity == pytest.approx(1.0)
    assert [x.advance_fraction for x in rows] == pytest.approx(
        [1.0, 0.5, 0.25]
    )


def test_remaining_duration_recourse_does_not_force_monotone_capacity():
    rows = remaining_duration_recourse(
        [
            [8, 10, 12],
            [5, 6, 20],
            [1, 2, 3],
        ],
        lower_quantile=0.0,
        reference_quantile=0.5,
        upper_quantile=1.0,
    )
    # Stage 1 can have more observed delay slack than stage 0; empirical
    # non-monotonicity is retained rather than repaired away.
    assert rows[1].delay_capacity > rows[0].delay_capacity
