"""Mathematical guardrails for PAYOFF-B's prospective cue-and-competition model."""
from dataclasses import replace

import pytest

from src.payoff_b_information_choice_corridor import (
    CueCompetition, density_sweep, evaluate,
)


def test_published_synthetic_parameters_and_density_switch():
    r = evaluate(CueCompetition())
    assert r["status"] == "TOY_DECISION_MODEL_NOT_NATURAL_EVIDENCE"
    assert r["density_without_cue_boundary"] == pytest.approx(1.0)
    assert r["density_enter_boundary_good_signal"] == pytest.approx(2.8)
    assert r["density_enter_boundary_bad_signal"] == pytest.approx(-0.8)
    assert r["no_cue_optimal_expected_payoff"] == pytest.approx(0.0)
    assert r["cue_optimal_expected_payoff"] == pytest.approx(0.9)
    assert r["incremental_information_value"] == pytest.approx(0.9)
    assert r["enter_after_good_signal"] is True
    assert r["enter_after_bad_signal"] is False
    assert r["optimal_entry_probability"] == pytest.approx(0.5)


def test_middle_density_voi_peak_and_no_negative_values():
    result = density_sweep()
    assert [round(v["incremental_information_value"], 3) for v in result] == [
        0.4, 0.65, 0.9, 0.65, 0.4, 0.15, 0.0,
    ]
    assert result[-1]["enter_after_good_signal"] is False
    assert all(v["incremental_information_value"] >= 0 for v in result)
    assert result[2]["incremental_information_value"] > result[0]["incremental_information_value"]


def test_uninformative_cue_and_postdecision_cue_have_zero_value():
    for d in (0.0, 0.5, 1.0, 2.0, 3.0):
        assert evaluate(CueCompetition(accuracy=0.5, competitor_density=d))[
            "incremental_information_value"
        ] == pytest.approx(0)
        assert evaluate(CueCompetition(cue_before_choice=False, competitor_density=d))[
            "incremental_information_value"
        ] == pytest.approx(0)


def test_perfect_information_upper_bound_and_optional_decisions():
    for d in (0.0, 0.2, 1.0, 2.8, 4.0):
        perfect = evaluate(CueCompetition(accuracy=1.0, competitor_density=d))
        moderate = evaluate(CueCompetition(accuracy=0.8, competitor_density=d))
        useless = evaluate(CueCompetition(accuracy=0.5, competitor_density=d))
        assert perfect["cue_optimal_expected_payoff"] + 1e-12 >= moderate[
            "cue_optimal_expected_payoff"
        ] >= useless["cue_optimal_expected_payoff"] - 1e-12


def test_exhaustive_free_disposal_nonnegativity():
    for p in (0, .1, .25, .5, .75, .9, 1):
        for q in (.5, .55, .8, .95, 1):
            for d in (0, .2, 1, 2, 3, 4, 8):
                got = evaluate(CueCompetition(
                    prior_good=p, accuracy=q, competitor_density=d
                ))
                assert got["incremental_information_value"] >= 0
                assert got["cue_optimal_expected_payoff"] + 1e-12 >= got[
                    "no_cue_optimal_expected_payoff"
                ]


def test_bad_input_rejected_and_no_demographic_inference():
    for altered in (
        {"accuracy": 0.4},
        {"prior_good": -0.01},
        {"competitor_density": -1},
        {"cost_per_competitor": 0},
        {"value_if_bad": 5},
        {"cue_before_choice": 0},
    ):
        with pytest.raises(ValueError):
            evaluate(replace(CueCompetition(), **altered))
    assert evaluate(CueCompetition())["general_equilibrium_or_social_welfare"] == "NOT_IDENTIFIED"
