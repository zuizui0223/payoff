import pytest

from src.route_recourse_capacity import (
    TransitionDuration,
    build_edge_envelopes,
    remaining_recourse,
)


def test_linear_route_recourse_declines_to_zero():
    rows = []
    for value in (8, 10, 12, 14, 16):
        rows.append(TransitionDuration("x", "R1", "R2", value, f"a{value}"))
    for value in (3, 4, 5, 6, 7):
        rows.append(TransitionDuration("x", "R2", "R3", value, f"b{value}"))

    env = build_edge_envelopes(rows, min_edge_rows=3)
    out = remaining_recourse(env, terminal_by_flyway={"x": "R3"})
    by_region = {row.region: row for row in out}

    assert by_region["R1"].retained_recourse == pytest.approx(1.0)
    assert 0.0 < by_region["R2"].retained_recourse < 1.0
    assert by_region["R3"].retained_recourse == pytest.approx(0.0)


def test_route_branching_expands_latest_minus_earliest_window():
    rows = []
    for i, value in enumerate((4, 5, 6, 7, 8)):
        rows.append(TransitionDuration("x", "R1", "R2", value, f"a{i}"))
        rows.append(TransitionDuration("x", "R2", "R4", value, f"b{i}"))
    for i, value in enumerate((10, 12, 14, 16, 18)):
        rows.append(TransitionDuration("x", "R1", "R4", value, f"c{i}"))

    env = build_edge_envelopes(rows)
    out = remaining_recourse(env, terminal_by_flyway={"x": "R4"})
    by_region = {row.region: row for row in out}

    assert by_region["R1"].latest_remaining_days > by_region["R2"].latest_remaining_days
    assert by_region["R1"].window_days > by_region["R2"].window_days


def test_edges_below_support_threshold_are_excluded():
    rows = [
        TransitionDuration("x", "R1", "R2", 5, "a"),
        TransitionDuration("x", "R1", "R2", 6, "b"),
        TransitionDuration("x", "R2", "R3", 4, "a"),
        TransitionDuration("x", "R2", "R3", 5, "b"),
        TransitionDuration("x", "R2", "R3", 6, "c"),
    ]
    env = build_edge_envelopes(rows, min_edge_rows=3)
    assert {(e.origin_region, e.destination_region) for e in env} == {("R2", "R3")}


def test_backward_or_equal_region_edges_are_not_admitted():
    rows = [
        TransitionDuration("x", "R2", "R1", 5, "a"),
        TransitionDuration("x", "R2", "R2", 5, "b"),
        TransitionDuration("x", "R1", "R2", 5, "c"),
        TransitionDuration("x", "R1", "R2", 6, "d"),
        TransitionDuration("x", "R1", "R2", 7, "e"),
    ]
    env = build_edge_envelopes(rows, min_edge_rows=3)
    assert len(env) == 1
    assert env[0].origin_region == "R1"
    assert env[0].destination_region == "R2"
