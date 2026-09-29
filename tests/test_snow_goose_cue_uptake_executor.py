import math

import pytest

pd = pytest.importorskip("pandas")

from scripts.payoff_b_greater_snow_goose_cue_uptake import (
    _estimability,
    _prepare,
    _primary_fit,
)


RHO = {
    (2019, "St_Lawrence"): -0.25,
    (2019, "Nunavik"): 0.05,
    (2019, "Baffin"): 0.30,
    (2020, "St_Lawrence"): 0.10,
    (2020, "Nunavik"): 0.35,
    (2020, "Baffin"): -0.10,
    (2021, "St_Lawrence"): 0.40,
    (2021, "Nunavik"): -0.20,
    (2021, "Baffin"): 0.15,
    (2022, "St_Lawrence"): 0.00,
    (2022, "Nunavik"): 0.25,
    (2022, "Baffin"): 0.50,
}


def synthetic_rows(n_individuals=32):
    rows = []
    contexts = ["St_Lawrence", "Nunavik", "Baffin"]
    for i in range(n_individuals):
        for year in range(2019, 2023):
            for context_index, context in enumerate(contexts):
                rho = RHO[(year, context)]
                for day in range(5):
                    temp = (day - 2) * 0.45 + (year - 2020.5) * 0.08
                    wind = ((i + day + context_index) % 7 - 3) / 3
                    precip = ((i + year + day) % 4) * 0.2
                    outcome = int(
                        (i + year + context_index + day) % 5 < 2
                    )
                    rows.append(
                        {
                            "individual": f"g{i:02d}",
                            "year": year,
                            "context": context,
                            "decision_date": f"{year}-05-{day + 1:02d}-{context}",
                            "depart_next_24h": outcome,
                            "local_temp_anom3": temp,
                            "same_day_temp_anom": temp * 0.55
                            + context_index * 0.07,
                            "day_of_year_within_context": day,
                            "wind_support": wind,
                            "precipitation": precip,
                            "predictive_connectivity_rho": rho,
                            "connectivity_training_n": 20,
                            "connectivity_window_end_year": year - 1,
                        }
                    )
    return pd.DataFrame(rows)


def test_synthetic_table_passes_registered_estimability_gate():
    data, rho_sd = _prepare(synthetic_rows())
    gate = _estimability(data, rho_sd)

    assert gate["individuals"] == 32
    assert gate["years"] == 4
    assert gate["contexts"] == 3
    assert gate["departure_events"] >= 100
    assert gate["predictive_connectivity_sd"] >= 0.03
    assert gate["within_context_predictive_connectivity_sd"] > 0
    assert gate["passes"]


def test_primary_registered_formula_fits_synthetic_data():
    data, _ = _prepare(synthetic_rows())
    result = _primary_fit(data)

    assert result["term"] == (
        "local_temp_anom3:z_predictive_connectivity"
    )
    assert math.isfinite(result["estimate"])
    assert math.isfinite(result["cluster_se"])
    assert result["support_status"] in {"SUPPORTED", "NOT_SUPPORTED"}


def test_connectivity_leakage_is_rejected_before_model_fit():
    data = synthetic_rows()
    data.loc[data.index[0], "connectivity_window_end_year"] = 2019
    data.loc[data.index[0], "year"] = 2019

    with pytest.raises(
        ValueError,
        match="predictive connectivity leaks focal or future year",
    ):
        _prepare(data)


def test_individual_specific_habitat_id_is_not_a_route_context():
    data = synthetic_rows()
    data.loc[data.index[0], "context"] = "cluster_17"

    with pytest.raises(
        ValueError,
        match="context must use only frozen shared route regions",
    ):
        _prepare(data)
