from math import isclose

from scripts.predict_modular_topology import (
    _signed_receipt,
    write_edge_pressures,
    write_edge_transfer,
)
from src.edgewise_modularity import edge_pressures
from src.three_function_example import EDGES, OPTIMA, REFERENCE_COUPLINGS, WEIGHTS


LABELS = (("0", "1"), ("0", "2"), ("1", "2"))
IDS = ("0", "1", "2")


def test_edge_pressure_direction_receipts_are_trait_scale_invariant(tmp_path):
    base_pressures = edge_pressures(OPTIMA, WEIGHTS, EDGES, REFERENCE_COUPLINGS)
    base_costs = (
        0.5 * base_pressures[0],
        base_pressures[1],
        2.0 * base_pressures[2],
    )
    expected = (
        "favor_more_decoupling",
        "marginal_balance",
        "favor_more_coupling",
    )

    for scale in (1e-8, 1.0, 1e8):
        optima = tuple(scale * value for value in OPTIMA)
        costs = tuple(scale * scale * value for value in base_costs)
        rows = write_edge_pressures(
            tmp_path / f"pressures_{scale:g}.csv",
            IDS,
            optima,
            WEIGHTS,
            EDGES,
            LABELS,
            REFERENCE_COUPLINGS,
            costs,
        )
        assert tuple(row["direction"] for row in rows) == expected
        for row, base_pressure in zip(rows, base_pressures):
            assert isclose(
                float(row["pressure"]),
                scale * scale * base_pressure,
                rel_tol=1e-12,
                abs_tol=0.0,
            )


def test_edge_transfer_effect_receipts_are_trait_scale_invariant(tmp_path):
    _, base_rows = write_edge_transfer(
        tmp_path / "transfer_base.csv",
        OPTIMA,
        WEIGHTS,
        EDGES,
        LABELS,
        REFERENCE_COUPLINGS,
    )
    expected = tuple(row["effect"] for row in base_rows)
    assert "increase" in expected
    assert "decrease" in expected

    for scale in (1e-8, 1.0, 1e8):
        optima = tuple(scale * value for value in OPTIMA)
        _, rows = write_edge_transfer(
            tmp_path / f"transfer_{scale:g}.csv",
            optima,
            WEIGHTS,
            EDGES,
            LABELS,
            REFERENCE_COUPLINGS,
        )
        assert tuple(row["effect"] for row in rows) == expected


def test_signed_receipt_uses_no_absolute_floor():
    labels = dict(positive="positive", negative="negative", zero="zero")
    assert _signed_receipt(1e-200, (1e-200, 0.0), **labels) == "positive"
    assert _signed_receipt(-1e-200, (-1e-200, 0.0), **labels) == "negative"
    assert _signed_receipt(0.0, (1e-200, -1e-200), **labels) == "zero"
