import pytest

from src.route_recourse_capacity import TransitionDuration
from src.v7r_recourse_loo import audit_individual_exclusion


def _row(a, b, days, identifier):
    return TransitionDuration(
        "x", a, b, float(days), str(identifier)
    )


def test_leave_animal_out_keeps_route_when_supported():
    data = [
        _row("R1", "R2", 8 + i, f"a{i}")
        for i in range(5)
    ] + [
        _row("R2", "R3", 3 + i, f"b{i}")
        for i in range(5)
    ]
    out = audit_individual_exclusion(
        data,
        focal_edges={("x", "R2", "R3")},
        terminal_by_flyway={"x": "R3"},
    )
    assert len(out) == 1
    assert out[0].n_individuals == 5
    assert out[0].n_not_estimable == 0
    assert 0 < out[0].full_recourse < 1


def test_leave_animal_out_reports_graph_failure_without_relaxing_gate():
    data = [
        _row("R1", "R2", 8 + i, f"a{i}")
        for i in range(5)
    ] + [
        _row("R2", "R3", 3 + i, f"b{i}")
        for i in range(3)
    ]
    out = audit_individual_exclusion(
        data,
        focal_edges={("x", "R2", "R3")},
        terminal_by_flyway={"x": "R3"},
    )
    assert len(out) == 1
    assert out[0].n_individuals == 3
    assert out[0].n_estimable == 0
    assert out[0].n_not_estimable == 3


def test_unknown_focal_flyway_fails_closed():
    with pytest.raises(ValueError, match="lacks a declared terminal"):
        audit_individual_exclusion(
            [_row("R1", "R2", 1, "a")],
            focal_edges={("other", "R1", "R2")},
            terminal_by_flyway={"x": "R2"},
        )
