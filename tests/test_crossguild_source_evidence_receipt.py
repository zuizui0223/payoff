"""Consistency checks for frozen Movebank source geometry receipt."""
import json
from pathlib import Path

def test_source_geometry_receipt_not_counted_as_ecological_test():
    p=Path("data/payoff_b_crossguild_spring_source_geometry_result_20261019.json")
    r=json.loads(p.read_text(encoding="utf-8"))
    assert len(r["sources"])==5
    assert len({s["doi"] for s in r["sources"]})==5
    assert sum(s["two_northward_checkpoints"] for s in r["sources"])==158
    assert sum(s["identity_years_with_spring_fixes"] for s in r["sources"])==284
    assert sum(s["two_northward_checkpoints"]>=20 for s in r["sources"])==3
    assert all(s["two_northward_checkpoints"]<=s["identity_years_with_spring_fixes"] for s in r["sources"])
    assert not r["data_gate"]["no_new_seasonal_information_actionability_slope"] == False
    assert r["data_gate"]["independent_migration_cohorts"]=="NOT_CONFIRMED"
