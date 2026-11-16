"""Synthetic-source parsing tests (not published ecological findings)."""
from scripts.payoff_b_little_owl_broodday_source_admission import (
    parse_number, source_counts
)


def test_zero_not_missing_and_non_numeric_null():
    assert parse_number("0")==0
    assert parse_number("NA") is None
    assert parse_number("not available") is None


def make(yr="2020",brood="N12020",day="44001",nest="N1"):
    return {
        "country":"Germany","country2":"Germany","broodID":brood,
        "nestID":nest,"Year":yr,"day":day,"age":"8",
        "prov_rate":"2","number_juv.x":"3",
        "temp":"12","humid":"60","rain":"0","wind":"2",
        "mammal":"1","bird":"0","insect":"1","earthworms":"0",
        "other":"0","BM":"4","prop.day.monitored":"0.5",
        "prov_rate2":"4","BM2":"8"
    }


def test_source_broodday_unique_and_halfday_consistency():
    data={
        "Littleowl.dat.JAB.csv":[make(day="44001"),make(day="44002")],
        "all_hab_vars.csv":[{"nestID":"N1","Field area":"1","Grassland area":"2",
           "Orchard area":"3","Hedges area":"4","Garden area":"5","country3":"Germany"}]
    }
    x=source_counts(data)
    assert x["admitted_brood_day_rows"]==2
    assert x["n_admitted_broods"]==1
    assert x["source_rate_normalization_qc"]=={}


def test_duplicate_source_day_not_pseudoreplicated():
    data={
        "Littleowl.dat.JAB.csv":[make(),make()],
        "all_hab_vars.csv":[{"nestID":"N1","Field area":"1","Grassland area":"2",
           "Orchard area":"3","Hedges area":"4","Garden area":"5","country3":"Germany"}]
    }
    x=source_counts(data)
    assert x["excluded_or_duplicated"]["duplicate_brood_day"]==1
    assert x["ready_for_separate_brood_holdout_measurement_diagnostic"] is False
