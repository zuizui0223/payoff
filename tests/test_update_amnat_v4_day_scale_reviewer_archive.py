"""Anonymity, source-SHA and posthoc-classification guards for revised Paper2."""
from pathlib import Path
import hashlib
import zipfile

import pytest

from scripts.update_amnat_v4_day_scale_reviewer_archive import (
    BASE_ZIP_SHA, DAY_SCRIPT_SHA, DAY_FILES, sha, gitsha,
    zip_deterministic, reproduction_command, assemble,
)


def test_original_verified_anonymous_science_source_and_day_files_locked():
    assert BASE_ZIP_SHA=="dfb568290d4a5c6a9bac21251e5c0370ca791c95faff5c599d8b2afd0ad89934"
    assert DAY_SCRIPT_SHA=="a42b4d9f1a1792d647d6091e980754c428009ce1"
    assert len(DAY_FILES)==7
    assert all(f.startswith("payoff_b_v8_metric_scale_") for f in DAY_FILES)
    assert "metric_scale_pairs.csv" in DAY_FILES[0]


def test_day_source_is_always_rerun_on_offline_input_without_promoting_transfer():
    sh=reproduction_command()
    assert "Rscript analysis/seasonal_v8_metric_scale_diagnostic.R" in sh
    assert "--historical data/frozen_outputs/day_scale" in sh
    assert "--supplement supplementary/Table_S2_day_scale.md" in sh
    assert "python3 -m scripts.audit_day_scale" in sh


def test_bad_archive_does_not_get_promoted(tmp_path):
    wrong=tmp_path/"wrong.zip";wrong.write_bytes(b"not an original verified archive")
    with pytest.raises(ValueError,match="science archive SHA"):
        assemble(wrong,tmp_path/"pdf",tmp_path/"day",tmp_path/"out")


def test_git_blob_content_hash_includes_git_header():
    b=b"Original exact R scientific source\n"
    assert gitsha(b)==hashlib.sha1(
        b"blob "+str(len(b)).encode()+b"\0"+b
    ).hexdigest()


def test_zip_is_reproducible_and_protects_against_overwrite(tmp_path):
    root=tmp_path/"source";root.mkdir()
    (root/"README.md").write_text("POST HOC\n",encoding="utf-8")
    a=tmp_path/"a.zip";b=tmp_path/"b.zip"
    hash1=zip_deterministic(root,a)
    hash2=zip_deterministic(root,b)
    assert hash1==hash2==sha(a.read_bytes())
    assert a.read_bytes()==b.read_bytes()
    with zipfile.ZipFile(a) as z:
        assert z.namelist()==["README.md"]
    with pytest.raises(ValueError,match="Refuse overwrite"):
        zip_deterministic(root,a)
