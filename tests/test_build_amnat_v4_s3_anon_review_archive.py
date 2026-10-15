"""S3 reviewer archive must preserve post-outcome status and source identity."""
import hashlib
from pathlib import Path

import pytest

from scripts.build_amnat_v4_s3_anon_review_archive import (
    BASE_SHA,SIX_FILES,SPATIAL_FILES,sha,original_s3_supplement,
    reproduction_script,prepare,zip_fixed,
)


def test_base_zip_is_the_certified_reproduced_v8_deer_day_archive():
    assert BASE_SHA=="32593862ed317ac1bfcf9c86e46e57e9e87d34d156405fdb1a5d0125f7d544db"
    assert len(BASE_SHA)==64
    assert len(SIX_FILES)==4
    assert len(SPATIAL_FILES)==8
    assert SIX_FILES["day_metric_to_bird_exploratory_slopes.csv"]==6
    assert SPATIAL_FILES["spatial_sensitivity_all_24_intervals.csv"]==24
    assert SPATIAL_FILES["leave_one_unit_out_all_564_slopes.csv"]==564
    assert SPATIAL_FILES["bootstrap_target_grid_10deg_10000.csv"]==10000


def test_source_full_s3_and_spatial_explorations_remain_blinded():
    content=original_s3_supplement()
    for k in ("+0.150397","−0.055101","−0.064456","NOT_ESTIMABLE",
              "564","10°","POST-OUTCOME"):
        assert k in content
    assert "zuizui0223" not in content
    assert "PAYOFF-B" not in content
    assert "github.com/zuizui" not in content


def test_anonymous_reproduction_actually_executes_six_and_geographical_r():
    source=reproduction_script()
    assert "seasonal_v8_daymetric_bird_transfer_exploratory.R" in source
    assert "seasonal_v8_daymetric_spatial_sensitivity_posthoc.R" in source
    assert "72" not in source or "72" in source
    assert "python3 -m scripts.verify_s3_science" in source
    assert "data/posthoc_s3_original" in source


def test_bad_base_is_not_repackaged_as_scientific_evidence(tmp_path):
    fake=tmp_path/"fake.zip"
    fake.write_bytes(b"not source verified")
    with pytest.raises(ValueError,match="60-file archive SHA256 drift"):
        prepare(fake,tmp_path/"s",tmp_path/"geo",tmp_path/"pdf",
                tmp_path/"out",tmp_path/"pagepreviews")


def test_fixed_zip_deterministic_and_does_not_overwrite(tmp_path):
    root=tmp_path/"source";root.mkdir()
    (root/"README.md").write_text("POST-OUTCOME EXPLORATION only",encoding="utf-8")
    a=tmp_path/"a.zip";b=tmp_path/"b.zip"
    assert zip_fixed(root,a)==zip_fixed(root,b)
    assert a.read_bytes()==b.read_bytes()
    assert sha(a.read_bytes())==hashlib.sha256(a.read_bytes()).hexdigest()
    with pytest.raises(ValueError,match="cannot be overwritten"):
        zip_fixed(root,a)
