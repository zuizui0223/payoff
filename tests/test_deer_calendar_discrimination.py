"""Pre-outcome scientific/design safeguards for calendar vs seasonal-phase contrast."""
from __future__ import annotations

import json
import pytest

pytest.importorskip("numpy", reason="Calendar/phase fixed-effects empirical test requires NumPy")

from scripts import payoff_b_deer_calendar_discrimination as cal


def synthetic_panel():
    rows = []
    for i in range(4):
        for j in range(4):
            # Nonadditive calendar and phenology vary independently after FE.
            phase = float((i + 1) * (j + 1))
            doy = float(105 + (i + 1) * (j + 1) ** 2)
            stop = float(20 + 6 * i + 3 * j - 0.4 * phase + 0.15 * doy)
            rows.append({
                "animal": f"deer-{i}", "year": 2010 + j,
                "start": phase, "calendar": doy, "stopover": stop,
            })
    return rows


def gates():
    return dict(
        min_rows=12, min_repeated_individuals=3, min_years=3,
        min_residual_df=3, min_raw_calendar_after_FE_rms_days=0.01,
        min_DFP_after_FE_and_calendar_rms_days=0.01,
        max_DFP_calendar_partial_VIF=100.0,
    )


def test_conditional_fe_correctly_separates_calendar_and_phase():
    sample = synthetic_panel()
    design = cal.prefit_design(sample, gates())
    assert design["status"] == "PASS"
    fit = cal.fit_conditional(sample)
    assert fit["beta_DFP_after_calendar"] == pytest.approx(-0.4, abs=1e-10)
    assert fit["calendar_plus_phase_residual_ss"] == pytest.approx(0, abs=1e-15)


def test_calendar_does_not_identify_cue_use():
    sample = synthetic_panel()
    contract = {
        "status": "EXPLORATORY", "support_gates_before_primary_coefficient": gates(),
        "uncertainty": {"replicates": 30, "seed": 2, "minimum_valid_fraction": 0},
        "provenance": {"source_doi": "fictional study"},
    }
    result = cal.analyze(sample, contract)
    assert result["no_causal_information_use_claim"] is True
    assert result["status"] in {
        "NEGATIVE_CALENDAR_CONDITIONAL_ASSOCIATION",
        "NO_SUPPORTED_NEGATIVE_CALENDAR_CONDITIONAL_ASSOCIATION",
        "BOOTSTRAP_SUPPORT_FAIL",
    }


def test_phase_identical_to_calendar_fails_before_outcome():
    sample = synthetic_panel()
    for row in sample:
        row["start"] = row["calendar"] + 5 * (row["year"] - 2010)
    design = cal.prefit_design(sample, gates())
    assert design["status"] == "NOT_ESTIMABLE"
    assert not design["checks"]["independent_phase"]
    assert not design["checks"]["collinearity"]


def test_no_outcome_information_needed_for_design_gate():
    sample = synthetic_panel()
    for row in sample:
        del row["stopover"]
    assert cal.prefit_design(sample, gates())["status"] == "PASS"


def test_original_checksum_rejects_wrong_file(tmp_path):
    wrong = tmp_path / "wrong.xlsx"
    wrong.write_bytes(b"wrong workbook bytes")
    with pytest.raises(ValueError, match="SHA256"):
        cal.get_original(wrong, "no network")


def test_contract_does_not_claim_animal_decision_cues():
    from pathlib import Path
    contract = json.loads((
        Path(__file__).resolve().parents[1]
        / "data/payoff_b_deer_calendar_discrimination_contract_20261122.json"
    ).read_text())
    assert contract["sampling"].startswith("Exactly same")
    assert contract["support_gates_before_primary_coefficient"]["max_DFP_calendar_partial_VIF"] == 10
    assert "No causal information/reward/fitness inference" in contract["constraints"]
