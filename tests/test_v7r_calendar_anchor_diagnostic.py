import pytest

from src.v7r_calendar_anchor_diagnostic import slope, summarize_edge


def _fixed_departure_fixture():
    rows=[]
    for i in range(10):
        arrival = 85.0 + 3.0*i
        departure = 145.0
        transit = 3.0 + (i % 2)
        destination_arrival = departure + transit
        rows.append({
            "e0": arrival,              # fixed onset coordinate = 0
            "e1": destination_arrival,  # fixed destination onset = 0
            "a0": arrival,
            "a1": destination_arrival,
            "stop_days": departure-arrival,
            "year": 2009 + (i % 2),
            "individual_id": "ID"+str(i),
        })
    return rows


def test_accounting_decomposition_is_exact():
    out = summarize_edge(_fixed_departure_fixture(), draws=200, seed=17)
    assert out["n"] == 10
    assert out["identity_residual"] == pytest.approx(0.0, abs=1e-10)
    assert out["beta_stopover"] == pytest.approx(-1.0)
    assert out["departure_on_arrival_calendar_slope"] == pytest.approx(0.0)
    assert out["departure_to_arrival_within_year_sd_ratio"] == pytest.approx(0.0)


def test_bootstrap_is_deterministic_and_individual_clustered():
    first=summarize_edge(_fixed_departure_fixture(),draws=100,seed=7)
    second=summarize_edge(_fixed_departure_fixture(),draws=100,seed=7)
    assert first==second
    assert first["bootstrap_individual_cluster"]["beta_stopover_fraction_below_zero"]==1.0
    assert first["bootstrap_individual_cluster"]["draws"]==100


def test_constant_predictor_is_rejected():
    with pytest.raises(ValueError, match="zero-variance predictor"):
        slope([1.0,1.0,1.0],[1.0,2.0,3.0])
