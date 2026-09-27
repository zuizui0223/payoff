from __future__ import annotations

import math

import pytest

from src.hoge_veluwe_network_history import (
    evaluate_information_reversal,
    fit_history_hac,
)


def stable_reversal():
    years = list(range(1992, 2016))
    values = []
    for index, year in enumerate(years):
        noise = ((index % 3) - 1) * 0.006
        if year < 2004:
            value = 1.0 - 0.055 * (year - 1992) + noise
        else:
            # Recovery begins near the fitted low and then rises strongly.
            value = 0.35 + 0.070 * (year - 2004) + noise
        values.append(value)
    return years, values


def test_registered_reversal_gate_detects_stable_decline_recovery():
    years, values = stable_reversal()
    result = evaluate_information_reversal(years, values)

    assert result["status"] == "INFORMATION_REVERSAL"
    assert result["full_geometry_pass"] is True
    assert result["segmented"]["left"]["slope"] < 0.0
    assert result["segmented"]["right"]["slope"] > 0.0
    assert result["segmented"]["delta_aicc_vs_linear"] >= 4.0
    assert result["segmented"]["recovery_fraction"] >= 0.50
    assert result["segmented"]["k"] == 5
    assert result["linear"]["k"] == 2
    assert result["stability"]["slope_signs_preserved_fraction"] >= 0.80
    assert result["stability"]["breakpoint_within_tolerance_fraction"] >= 0.80


def test_monotonic_connectivity_cannot_open_history_gate():
    years = list(range(1992, 2016))
    values = [1.0 - 0.03 * index for index in range(len(years))]
    result = evaluate_information_reversal(years, values)

    assert result["status"] == "NO_CUE_RESOURCE_REVERSAL"
    assert result["full_geometry_pass"] is False
    assert result["stability"]["status"] == "NOT_EVALUATED_FULL_GEOMETRY_FAILED"


def test_gate_b_rejects_duplicate_years():
    with pytest.raises(ValueError, match="unique"):
        evaluate_information_reversal(
            [1992, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002],
            [float(i) for i in range(12)],
        )


def test_gate_c_refuses_to_open_without_registered_gate_b_pass():
    result = fit_history_hac(
        [],
        break_year=2004,
        reversal_status="NO_CUE_RESOURCE_REVERSAL",
    )
    assert result == {
        "status": "NOT_RUN",
        "reason": "Gate B did not license the history test",
    }


def test_gate_c_uses_overlap_support_and_hac7_when_licensed():
    pytest.importorskip("pandas")
    pytest.importorskip("statsmodels")

    records = []
    # Both branches span the same connectivity support; recovery is shifted
    # upward by ~2 days at the mean support. Small deterministic noise avoids
    # a zero-residual covariance fixture.
    decline_years = list(range(1992, 2004))
    recovery_years = list(range(2004, 2016))
    for branch_index, years in enumerate((decline_years, recovery_years)):
        for i, year in enumerate(years):
            connectivity = 0.2 + 0.05 * (i % 10)
            noise = ((i % 3) - 1) * 0.05
            mismatch = (
                4.0
                - 1.5 * connectivity
                + 2.0 * branch_index
                + noise
            )
            records.append(
                {
                    "year": year,
                    "connectivity": connectivity,
                    "mismatch": mismatch,
                }
            )

    result = fit_history_hac(
        records,
        break_year=2004,
        reversal_status="INFORMATION_REVERSAL",
    )

    assert result["status"] == "COMPLETE"
    assert result["n"] >= 12
    assert result["branch_counts"]["decline"] >= 6
    assert result["branch_counts"]["recovery"] >= 6
    assert result["covariance"]["primary"] == "HAC(7) finite-sample corrected"
    primary = result["branch_at_mean_overlap"]["primary_hac7"]
    assert math.isfinite(primary["estimate"])
    assert primary["estimate"] == pytest.approx(2.0, abs=0.20)

def test_full_sample_reversal_can_fail_the_frozen_stability_gate():
    years = list(range(1992, 2016))
    values = [
        1.071796, 0.844474, 0.906202, 1.050682, 1.043100, 0.744754,
        0.716719, 0.820574, 0.872824, 0.791050, 0.780355, 0.626116,
        0.778679, 0.861685, 0.736433, 0.666651, 0.764118, 0.946166,
        0.726630, 0.920812, 0.860899, 0.976887, 0.995548, 1.051586,
    ]

    result = evaluate_information_reversal(years, values)

    assert result["full_geometry_pass"] is True
    assert result["status"] == "UNSTABLE_CUE_RESOURCE_REVERSAL"
    assert result["stability"]["slope_signs_preserved_fraction"] >= 0.80
    assert result["stability"]["breakpoint_within_tolerance_fraction"] < 0.80

