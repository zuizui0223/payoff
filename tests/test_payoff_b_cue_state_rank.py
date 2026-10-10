from itertools import product

import pytest

from src.payoff_b_cue_state_rank import (
    audit, exact_rank, factorial_design_row,
)


def test_full_crossing_identifies_saturated_terms():
    rows = [factorial_design_row(*c) for c in product((0, 1), repeat=3)]
    assert len(rows) == 8
    assert exact_rank(rows) == 8


def test_partner_cue_alias_when_only_observed_with_true_state():
    rows = [
        factorial_design_row(h, h, t)
        for h, t in product((0, 1), repeat=2)
    ]
    assert exact_rank(rows) == 4
    assert all(row[1] == row[2] for row in rows)


def test_signal_timing_cannot_be_estimated_without_early_reveal():
    rows = [
        factorial_design_row(h, s, 0)
        for h, s in product((0, 1), repeat=2)
    ]
    assert exact_rank(rows) == 4
    assert all(row[3] == row[5] == row[6] == row[7] == 0 for row in rows)


def test_source_only_audit_and_no_biological_claim():
    result = audit()
    assert result["fully_crossed_2x2x2"]["rank"] == 8
    assert result["cue_equals_state"]["rank"] == 4
    assert result["never_predecision_signal"]["rank"] == 4
    assert "causal cue use" in result["not_inferred"]


def test_reject_nonbinary_and_ragged_design():
    with pytest.raises(ValueError):
        factorial_design_row(0, 2, 1)
    with pytest.raises(ValueError):
        factorial_design_row(0, 0.0, 1)
    with pytest.raises(ValueError):
        exact_rank([[1, 2], [1]])
