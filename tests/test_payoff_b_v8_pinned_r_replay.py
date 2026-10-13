"""Network-free original-versus-replay row comparison identity guards."""
from pathlib import Path

import pytest

from scripts.audit_payoff_b_v8_pinned_r_replay import KEYS, snapshot


def test_all_scientifically_distinct_pairs_species_and_targets_keyed():
    assert KEYS["environment_pairs"]==("pair_key",)
    assert KEYS["environment_species"]==("species",)
    assert KEYS["transfer_rows"]==("species","target_cell","pair_key")
    assert KEYS["structural_rows"]==("species","target_cell","pair_key")
    records=[
       {"species":"A","target_cell":"2","pair_key":"p1","delta_mismatch":".1"},
       {"species":"B","target_cell":"2","pair_key":"p1","delta_mismatch":".2"}
    ]
    row=snapshot(records,KEYS["transfer_rows"],"example")
    assert len(row)==2


def test_duplicate_frozen_source_rows_fail_closed():
    rec={"species":"A","target_cell":"1","pair_key":"p"}
    with pytest.raises(ValueError,match="Duplicate key"):
        snapshot([rec,dict(rec)],KEYS["transfer_rows"],"tampered")


def test_filename_comparison_requires_raw_rows_not_a_summary():
    assert "species" in KEYS["structural_rows"]
    assert "pair_key" in KEYS["environment_pairs"]
