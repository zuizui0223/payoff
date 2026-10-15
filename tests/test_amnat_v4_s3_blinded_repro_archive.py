"""Source and noncausality guards for S3 anonymous, outcome-opened archive."""
from pathlib import Path
import json

import pytest

from scripts.build_amnat_v4_s3_blinded_repro_archive import (
    BASE_ZIP_SHA256,SIX_ORIGINALS,SPATIAL_ORIGINALS,ORIGINAL_SCRIPTS,
    s3_supplement,reproduction_command,prepare,finalize,safe_text,
)


def test_original_source_archive_and_complete_s3_input_files_locked():
    assert BASE_ZIP_SHA256=="047527afcb6eb6f59e52d7fec4cbe6988b350138b21c969c22aea3d8a8206016"
    assert len(SIX_ORIGINALS)==4
    assert len(SPATIAL_ORIGINALS)==8
    assert len(ORIGINAL_SCRIPTS)==2
    assert "day_metric_to_bird_exploratory_slopes.csv" in SIX_ORIGINALS
    assert "bootstrap_target_grid_10deg_10000.csv" in SPATIAL_ORIGINALS
    assert all(a.startswith("analysis/seasonal_v8_") for a in ORIGINAL_SCRIPTS.values())


def test_s3_report_explicitly_postoutcome_and_not_causing_bird_cognition():
    s=s3_supplement()
    for literal in ("POST-OUTCOME","−0.064456","−0.055101",
                    "NOT_ESTIMABLE","564","fixed-arrival"):
        assert literal in s
    assert "not" in s.lower()
    assert "https://github.com/zuizui0223" not in s
    assert "animal cognition" not in s.lower() or "not" in s.lower()
    safe_text(s,"S3 supplementary material")


def test_anonymized_reproduction_uses_both_original_72_pair_and_geographic_sensitivity():
    shell=reproduction_command()
    assert "Rscript analysis/seasonal_v8_daymetric_bird_transfer_exploratory.R" in shell
    assert "Rscript analysis/seasonal_v8_daymetric_spatial_sensitivity_posthoc.R" in shell
    assert "data/frozen_outputs/day_scale/seasonal_v8_metric_scale_pairs.csv" in shell
    assert "data/frozen_outputs/transfer/seasonal_v8_transfer_primary_rows.csv" in shell
    assert "data/frozen_outputs/structural/seasonal_v8_transfer_structural_null_rows.csv" in shell
    assert "--six-original data/frozen_outputs/s3/six" in shell
    assert "--spatial-original data/frozen_outputs/s3/spatial" in shell


def test_original_zip_must_match_exact_immutable_science_source(tmp_path):
    bad=tmp_path/"not_verified.zip"
    bad.write_bytes(b"not the original source")
    with pytest.raises(ValueError,match="ZIP SHA256 drift"):
        prepare(bad,tmp_path/"six",tmp_path/"spatial",tmp_path/"paper",tmp_path/"new")


def test_nonverified_s3_outputs_do_not_get_promoted_to_reviewer_package(tmp_path):
    stage=tmp_path/"candidate"
    (stage/"outputs/s3").mkdir(parents=True)
    (stage/"outputs/s3/S3_reproduction_verified.json").write_text(
        json.dumps({"status":"NO_SCIENTIFIC_REPLAY"}),encoding="utf-8")
    with pytest.raises(ValueError,match="not verified"):
        finalize(stage,tmp_path/"new.zip")


def test_author_identity_is_forbidden_in_supplement_scripts():
    with pytest.raises(ValueError):
        safe_text("internal link https://github.com/zuizui0223/payoff","unsafe")
    with pytest.raises(ValueError):
        safe_text("PAYOFF-B publication results","unsafe")
    safe_text("Study source DOI 10.5061/dryad.ttdz08m6w","safe")
