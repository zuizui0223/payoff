"""Offline safety guards for anonymous reproducibility package builder."""
from pathlib import Path
import hashlib
import zipfile

import pytest

from scripts.build_amnat_v4_blind_repro_archive import (
    FORBIDDEN, SOURCE_BLOB, SOURCE_SIZE, SOURCE_R, SOURCE_CONTRACTS,
    ORIGINAL_DATA, gitblob, neutral, safe, fixed_zip, readme, replay_script, build
)


def test_path_and_label_anonymization_preserves_scientific_identifiers():
    old="analysis/movement_phenology/payoff_b_v8_primary.R"
    assert neutral(old)=="analysis/seasonal_v8_primary.R"
    assert neutral("docs/PAYOFF_B_V8_TRANSFER_STRUCTURAL_NULL_CONTRACT_20261005.md") == (
        "docs/SEASONAL_V8_TRANSFER_STRUCTURAL_NULL_CONTRACT_20261005.md"
    )
    assert neutral("PAYOFF-B frozen science")=="Seasonal tracking frozen science"
    assert neutral("SOURCE_COMMIT <- '62c58d77c2028bd863dfe3697b0d9cf29ceaeab0'").endswith(
        "'62c58d77c2028bd863dfe3697b0d9cf29ceaeab0'"
    )
    assert all("payoff_b" not in neutral(s) for s in SOURCE_R)
    assert all("PAYOFF_B" not in neutral(s) for s in SOURCE_CONTRACTS)


def test_forbid_identity_and_email_in_reviewed_source():
    safe("Source DOI 10.5061/dryad.ttdz08m6w","citation")
    for token in ("zuizui0223", "PAYOFF-B", "payoff_b", "rachelzhang0223"):
        with pytest.raises(ValueError,match="Identifying"):
            safe("comment "+token,"science.txt")
    with pytest.raises(ValueError,match="Email"):
        safe("sender private@identifying.test","memo.md")


def test_git_blob_hash_uses_real_git_object_envelope():
    data=b"hello\n"
    expected=hashlib.sha1(b"blob 6\0"+data).hexdigest()
    assert gitblob(data)==expected
    assert SOURCE_SIZE==7250107 and len(SOURCE_BLOB)==40


def test_source_data_archive_has_all_three_original_frozen_modules():
    assert len(SOURCE_R)==3
    assert len(SOURCE_CONTRACTS)==2
    assert sum(len(x) for x in ORIGINAL_DATA.values())==13
    assert all(Path(k).suffix==".R" for k in SOURCE_R)
    assert "Rscript analysis/seasonal_v8_transfer_structural_null_audit.R" in replay_script()


def test_avoid_premature_submission_claim():
    text=readme()
    assert "NOT YET A DEPOSITED REVIEWER LINK" not in text or "not a submitted" in text
    assert "NOT a submitted" in text or "not a submitted" in text
    assert "10.5061/dryad.ttdz08m6w" in text
    assert "150 species-target" in text
    assert "72 unique environmental pairs" in text


def test_deterministic_zip_entries_and_no_overwrite(tmp_path):
    src=tmp_path/"src"
    (src/"data").mkdir(parents=True)
    (src/"data"/"a.txt").write_text("x")
    (src/"data"/"b.txt").write_text("y")
    one=tmp_path/"one.zip"
    two=tmp_path/"two.zip"
    fixed_zip(src,one)
    fixed_zip(src,two)
    assert one.read_bytes()==two.read_bytes()
    with zipfile.ZipFile(one) as z:
        assert sorted(z.namelist())==["data/a.txt","data/b.txt"]
        assert all(f.date_time==(2026,10,13,0,0,0) for f in z.infolist())
    with pytest.raises(ValueError,match="Refuse overwrite"):
        fixed_zip(src,one)


def test_missing_real_raw_source_fails_before_creating_any_archive(tmp_path):
    orig=tmp_path/"original";orig.mkdir()
    rds=tmp_path/"bad.rds";rds.write_bytes(b"not original data")
    paper=tmp_path/"paper";paper.mkdir()
    with pytest.raises(ValueError,match="size/Git blob"):
        build(orig,rds,paper,tmp_path/"new",tmp_path/"new.zip")
