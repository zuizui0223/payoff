import json
from pathlib import Path


ROOT=Path(__file__).resolve().parents[1]
SCREEN=ROOT/"data"/"payoff_b_clock_portfolio_direct_test_screen_20261003.json"


def load():
    return json.loads(SCREEN.read_text(encoding="utf-8"))


def test_no_direct_natural_portfolio_test_is_admitted():
    p=load()
    assert p["decision"]["admitted_count"]==0
    assert p["decision"]["outcome"]=="NO_DIRECT_NATURAL_PORTFOLIO_FRAGILITY_TEST_ADMITTED"
    assert all(not row["admitted"] for row in p["screened_systems"])


def test_identification_triangle_requirements_are_all_explicit():
    p=load()
    req=p["admission_requirements"]
    assert len(req)==6
    text=" ".join(req).lower()
    assert "entry phase" in text
    assert "feedback reliance" in text
    assert "opportunity loss" in text
    assert "final phase" in text
    assert "selection" in text


def test_piping_plover_is_anchor_not_direct_test():
    p=load()
    row=next(x for x in p["screened_systems"] if x["system"].startswith("Sweeney"))
    assert row["classification"]=="OPPORTUNITY_LOSS_BEHAVIOR_ANCHOR"
    assert row["admitted"] is False
    assert any("downstream" in x for x in row["missing"])


def test_great_knot_is_selection_warning_not_fragility_confirmation():
    p=load()
    row=next(x for x in p["screened_systems"] if x["system"].startswith("Peng"))
    assert row["classification"]=="SELECTION_REWEIGHTING_ANCHOR"
    assert "selective disappearance" in row["warning"]
