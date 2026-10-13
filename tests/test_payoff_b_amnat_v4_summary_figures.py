"""Frozen-source, summary-only, deterministic AmNat Paper 2 figure checks."""
from __future__ import annotations

import hashlib
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from scripts.build_payoff_b_amnat_v4_summary_figures import (
    ROOT, LEGENDS, build, extract_inputs, read_sources, figure3,
)


def test_all_figure_values_are_exactly_frozen_source_summaries():
    raw, sha = read_sources()
    values = extract_inputs(raw)
    assert set(sha) == {
        "v8_environment", "v8_transfer", "v8_structural_null",
        "ortega", "deer_channels",
    }
    a = values["environment"]
    assert a["unique_pair"]["estimate"] == pytest.approx(0.3690)
    assert a["unique_pair"]["ci95"] == pytest.approx((0.2984, 0.4365))
    assert a["equal_species"]["estimate"] == pytest.approx(0.3364)
    assert a["equal_species"]["ci95"] == pytest.approx((0.2628, 0.4312))
    b = values["transfer"]
    assert b["primary"]["estimate"] == pytest.approx(0.06243969)
    assert b["primary"]["ci95"] == pytest.approx((-0.01411178, 0.1363489))
    assert b["fixed_arrival_null"]["estimate"] == pytest.approx(0.04742)
    assert b["fixed_arrival_null"]["ci95"] == pytest.approx((-0.04076, 0.12269))
    assert b["bird_increment"]["estimate"] == pytest.approx(0.01502)
    assert b["bird_increment"]["ci95"] == pytest.approx((-0.05212, 0.10273))
    assert b["permutation_null"]["median"] == pytest.approx(0.04677)
    assert b["permutation_null"]["range_95"] == pytest.approx((0.01312, 0.08188))
    d = values["mule_deer"]
    assert d["animal_years"] == 152
    assert d["animals"] == 72
    assert d["safe_subset"]["animal_years"] == 62
    assert d["variance_ratio"]["estimate"] == pytest.approx(0.2488754818871811)


def test_no_outcome_support_rule_can_be_removed_silently():
    original, _ = read_sources()
    altered = dict(original)
    altered["v8_environment"] = altered["v8_environment"].replace(
        "V8_BROAD_DEGRADATION = NOT_SUPPORTED",
        "V8_BROAD_DEGRADATION = SUPPORTED",
    )
    with pytest.raises(ValueError, match="support decision"):
        extract_inputs(altered)
    altered = dict(original)
    altered["v8_transfer"] = altered["v8_transfer"].replace(
        "INFORMATION_TO_TIMING_TRANSFER = NOT_SUPPORTED",
        "INFORMATION_TO_TIMING_TRANSFER = SUPPORTED",
    )
    with pytest.raises(ValueError, match="status"):
        extract_inputs(altered)


def test_four_svg_preview_manifest_and_zip_determinism(tmp_path):
    o1, o2 = tmp_path/"first", tmp_path/"second"
    zip1, zip2 = tmp_path/"one.zip", tmp_path/"two.zip"
    a = build(o1, archive=zip1)
    b = build(o2, archive=zip2)
    assert a == b
    assert zip1.read_bytes() == zip2.read_bytes()
    assert a["status"] == "VERIFIED_SUMMARY_FIGURE_PREVIEW_SUBMISSION_HOLD"
    assert a["submission_ready"] is False
    assert a["anonymous_review_archive_complete"] is False
    assert a["individual_or_pair_level_points_generated"] is False
    assert a["underlying_observation_data_included"] is False
    figs = sorted(o1.glob("*.svg"))
    assert len(figs) == 4
    assert len(a["figures"]) == 5
    for fig in figs:
        xml = ET.fromstring(fig.read_text(encoding="utf-8"))
        assert xml.tag.endswith("svg")
        assert len(xml.findall(".//{http://www.w3.org/2000/svg}title")) == 1
        assert "individual trajectories" in fig.read_text(encoding="utf-8") or "no" in fig.read_text(encoding="utf-8").lower()
        assert a["figures"][fig.name]["sha256"] == hashlib.sha256(fig.read_bytes()).hexdigest()


def test_summary_level_not_fake_pair_or_individual_plots(tmp_path):
    out=tmp_path/"figures"
    build(out)
    fig2=(out/"figure2_summary.svg").read_text(encoding="utf-8")
    fig3=(out/"figure3_summary.svg").read_text(encoding="utf-8")
    fig4=(out/"figure4_summary.svg").read_text(encoding="utf-8")
    assert "Unique spatial pairs (n=166)" in fig2
    assert "150 species-target rows; 72 unique pairs; 22 species" in fig3
    assert "n=152 animal-years from 72 deer" in fig4
    assert "individual trajectories" in fig4.lower()
    assert "95% pair-bootstrap CIs" in fig2
    assert "permutation" in fig3.lower()


def test_writes_fail_closed_in_nonempty_directory(tmp_path):
    out=tmp_path/"out"
    out.mkdir()
    (out/"some_other_data.txt").write_text("do not overwrite",encoding="utf-8")
    with pytest.raises(ValueError, match="Refusing"):
        build(out)


def test_legend_caps_and_no_misleading_claims():
    for label, text in LEGENDS.items():
        assert len(text.split()) <= 100, label
    assert "reproductive fitness" in LEGENDS["figure4"]
    assert "not a confidence interval" not in LEGENDS["figure3"] or "permutation" in LEGENDS["figure3"]
