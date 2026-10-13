"""True V8 spatial-pair and species-target point figure source guards."""
from __future__ import annotations

import csv
import json
import math
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from scripts.render_payoff_b_v8_original_observed_figures import (
    figure2, figure3, render, weighted_fit
)


def test_source_observation_points_are_not_synthetic_summary_points():
    pairs=[
       {"rho_early":str(-.8+i*.01),"rho_late":str(-.7+i*.01)}
       for i in range(166)
    ]
    graphic=figure2(pairs,{"mean_delta_rho":.1,
                           "ci95_pair_bootstrap":[.01,.2]})
    assert graphic.count('class="observed-spatial-pair"')==166
    assert "not a tracked bird route" in graphic
    ET.fromstring(graphic)


def test_actual_source_style_transfer_plot_not_independent_150_pairs():
    rows=[]
    null=[]
    for i in range(150):
        x=-1.5+3*i/149
        sp=f"Species{i%22}"
        key=f"Pair{i%72}"
        row={"species":sp,"z_delta_rho":str(x),
             "delta_mismatch":str(.15+.06*x+.005*math.sin(i)),
             "pair_key":key,"target_cell":str(i)}
        rows.append(row)
        null.append({
            **row,
            "delta_pseudo_mismatch":str(.10+.047*x)
        })
    obs_slope=weighted_fit(rows,"delta_mismatch")[0]
    null_slope=weighted_fit(null,"delta_pseudo_mismatch")[0]
    graphic=figure3(rows,null,{
        "beta":obs_slope,"null_beta":null_slope,
        "ci95":[obs_slope-.1,obs_slope+.1]
    })
    assert graphic.count('class="observed-species-target"')==150
    assert "72 distinct pairs" in graphic
    assert "not independent spatial-pair observations" in graphic
    ET.fromstring(graphic)


def test_source_numeric_mismatch_stops_figure():
    records=[
        {"species":"A","z_delta_rho":"0","delta_mismatch":"0",
         "delta_pseudo_mismatch":"0"},
        {"species":"B","z_delta_rho":"1","delta_mismatch":"1",
         "delta_pseudo_mismatch":".1"}
    ]
    with pytest.raises(ValueError,match="frozen beta"):
        figure3(records,records,{"beta":-10,"null_beta":.1,"ci95":[0,1]})


def test_file_source_gate_never_accepts_empty_or_failed_original_rows(tmp_path):
    root=tmp_path/"source"
    root.mkdir()
    receipt=tmp_path/"receipt.json"
    receipt.write_text(json.dumps({"status":"OUTCOME_NOT_VERIFIED"}))
    with pytest.raises(ValueError,match="validated original row"):
        render(root,receipt,tmp_path/"figures")


def test_output_refuses_missing_original_csv_even_with_good_receipt(tmp_path):
    root=tmp_path/"source"
    root.mkdir()
    receipt=tmp_path/"receipt.json"
    receipt.write_text(json.dumps({
        "status":"FROZEN_V8_ROW_LEVEL_ARTIFACTS_RESTORED_AND_ARITHMETIC_VERIFIED"
    }))
    with pytest.raises(FileNotFoundError):
        render(root,receipt,tmp_path/"figures")
