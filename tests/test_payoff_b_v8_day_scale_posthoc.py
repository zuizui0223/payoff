"""Source/metric guards for already executed exploratory V8 day-scale analysis."""
from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scripts.audit_payoff_b_v8_day_scale_posthoc import (
    SCRIPT_BLOB_SHA, EXPECTED, SOURCES, approx, unique, fl,
    compare_historical, record_key, read_csv
)


def test_primary_day_metrics_are_locked_and_have_correct_scale():
    assert SCRIPT_BLOB_SHA=="a42b4d9f1a1792d647d6091e980754c428009ce1"
    assert EXPECTED["target_sd"] == (2.412,4.662,2.250,1.946,2.549)
    assert EXPECTED["rmse_in"] == (1.821,2.494,.673,.460,.891)
    assert EXPECTED["loo_rmse"] == (4.113,4.168,.055,-.591,.632)
    assert EXPECTED["loo_null_rmse"] == (3.182,5.865,2.683,2.342,3.013)
    assert len(SOURCES)==7


def test_day_scale_result_not_reinterpreted_as_confirmatory_or_mismatch_causation():
    doc=Path(__file__).resolve().parents[1]/"submission/AMNAT_V4_SUPPLEMENTARY_TABLE_S2_DAY_SCALE_20261014.md"
    s=doc.read_text(encoding="utf-8")
    assert "POST HOC" in s and "LOYO" in s
    assert "−0.591" in s and "+2.628" in s
    assert "A negative direct RMSE-to-mismatch transfer has not been established" in s
    assert "Doubling the destination's variability did not *cause* Pearson correlation" in s


def test_numeric_checks_and_frozen_sample_units_fail_closed():
    approx(2.4121,2.412,"SD",.001)
    with pytest.raises(ValueError,match="drift"):
        approx(4.5,2.412,"SD",.001)
    with pytest.raises(ValueError,match="Nonfinite"):
        fl({"a":"NaN"},"a")
    with pytest.raises(ValueError,match="expected 2 distinct"):
        unique([{"pair_key":"x"},{"pair_key":"x"}],"pair_key",2,"environment")


def test_historical_rerun_comparison_accepts_float_rounding_not_changed_data(tmp_path):
    old=tmp_path/"old";replay=tmp_path/"new"
    old.mkdir();replay.mkdir()
    for name in SOURCES:
        fields=["metric","n_pairs","value"]
        rows=[{"metric":"x","n_pairs":"166","value":"0.5"}]
        if name.endswith("_pairs.csv"):
            fields=["pair_key","value"];rows=[{"pair_key":"p","value":"0.500000000"}]
        if name.endswith("_bird_rows.csv"):
            fields=["species","target_cell","pair_key","value"]
            rows=[{"species":"A","target_cell":"2","pair_key":"p","value":"0.500000000"}]
        for folder,change in ((old,0),(replay,1e-10)):
            with (folder/name).open("w",encoding="utf-8",newline="") as fp:
                w=csv.DictWriter(fp,fieldnames=fields);w.writeheader()
                w.writerow({**rows[0],"value":str(.5+change)})
    out=compare_historical(old,replay)
    assert len(out)==7
    with (replay/SOURCES[0]).open("w",encoding="utf-8",newline="") as fp:
        fp.write("pair_key,value\np,0.8\n")
    with pytest.raises(ValueError,match="field drift"):
        compare_historical(old,replay)
