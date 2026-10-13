"""Source and counterfeiting guards for AmNat mixed-provenance figure packet."""
import hashlib
import json
from pathlib import Path

import pytest

from scripts.assemble_amnat_v4_original_observed_figures import assemble


def fake_set(base:Path):
    summary=base/"summary";observed=base/"observed"
    summary.mkdir();observed.mkdir()
    sman={"status":"VERIFIED_SUMMARY_FIGURE_PREVIEW_SUBMISSION_HOLD","figures":{}}
    oman={"status":"ORIGINAL_V8_OBSERVED_ROW_SVG_PREVIEW_SUBMISSION_HOLD",
          "verified_actual_spatial_pair_points":166,
          "verified_actual_species_target_points":150,
          "distinct_environmental_pairs_in_transfer":72,
          "no_synthetic_points":True,
          "source_row_sha256":{"original":"fixture-only"},
          "svg_sha256":{}}
    raw_svg='<svg xmlns="http://www.w3.org/2000/svg"><title>Data source fixture</title>{}</svg>'
    for num in (1,4):
        name=f"figure{num}_summary.svg"
        raw=raw_svg.format("").encode()
        (summary/name).write_bytes(raw)
        sman["figures"][name]={"sha256":hashlib.sha256(raw).hexdigest()}
    for num,name,cls,count in [
        (2,"figure2_observed_166_pairs.svg","observed-spatial-pair",166),
        (3,"figure3_observed_150_species_targets.svg","observed-species-target",150)
    ]:
        body="".join(f'<circle class="{cls}" cx="{i}" cy="25" r="2"/>' for i in range(count))
        raw=raw_svg.format(body).encode()
        (observed/name).write_bytes(raw)
        oman["svg_sha256"][name]=hashlib.sha256(raw).hexdigest()
    (summary/"figure_manifest.json").write_text(json.dumps(sman))
    (observed/"observed_figures_receipt.json").write_text(json.dumps(oman))
    return summary,observed


def test_combined_figures_preserve_exact_verified_original_counts(tmp_path):
    summary,observed=fake_set(tmp_path)
    output=tmp_path/"combined"
    result=assemble(summary,observed,output)
    assert result["status"]=="REAL_POINT_F2_F3_AND_FROZEN_F1_F4_EDITORIAL_PREVIEW_PASS"
    assert result["f2_observed_unique_spatial_pairs"]==166
    assert result["f3_observed_species_target_rows"]==150
    assert result["f3_independent_environment_pairs"]==72
    assert result["synthetic_observations_generated"] is False
    assert result["submission_ready"] is False
    assert len(list(output.glob("*.svg")))==4


def test_source_figure_tamper_fails_before_copy(tmp_path):
    summary,observed=fake_set(tmp_path)
    f=observed/"figure2_observed_166_pairs.svg"
    f.write_text(f.read_text()+"<!-- counterfeit -->")
    with pytest.raises(ValueError,match="SHA256 changed"):
        assemble(summary,observed,tmp_path/"combined")


def test_false_original_count_or_synthetic_source_fails(tmp_path):
    summary,observed=fake_set(tmp_path)
    f=observed/"observed_figures_receipt.json"
    m=json.loads(f.read_text())
    m["verified_actual_spatial_pair_points"]=150
    f.write_text(json.dumps(m))
    with pytest.raises(ValueError,match="Wrong true-row"):
        assemble(summary,observed,tmp_path/"combined")


def test_reviewer_packet_cannot_carry_owner_identity(tmp_path):
    summary,observed=fake_set(tmp_path)
    f=summary/"figure1_summary.svg"
    raw=f.read_bytes().replace(b"Data source fixture",b"zuizui0223 private project")
    f.write_bytes(raw)
    m=json.loads((summary/"figure_manifest.json").read_text())
    m["figures"]["figure1_summary.svg"]["sha256"]=hashlib.sha256(raw).hexdigest()
    (summary/"figure_manifest.json").write_text(json.dumps(m))
    with pytest.raises(ValueError,match="Identifying project"):
        assemble(summary,observed,tmp_path/"combined")
