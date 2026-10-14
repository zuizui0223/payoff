"""Source licensing/anonymity and exact-number guards for 2023 deer addendum."""
import hashlib
import json
from pathlib import Path

import pytest

from scripts.build_amnat_v4_deer_source_addendum import (
    DEER_SHA,V8_ARCHIVE_SHA,ORIGINAL_CODE,ORIGINAL_FROZEN,
    neutralize,safe_text,prepare,finish,reproduction_script,
)
from scripts.verify_amnat_v4_muledeer_replay import close_value,CHECKS,EXPECTED_SHA


def test_exact_published_source_and_four_reproducible_analysis_modules():
    assert DEER_SHA==EXPECTED_SHA
    assert len(DEER_SHA)==64 and len(V8_ARCHIVE_SHA)==64
    assert len(ORIGINAL_CODE)==4
    assert len(ORIGINAL_FROZEN)==3
    assert len(CHECKS["phase"])>=10
    assert len(CHECKS["readiness"])>=5
    assert len(CHECKS["channels"])>=5


def test_labels_neutralized_without_touching_numeric_parameter_seeds():
    source="from payoff_b_ortega_source_data_probe import DEFAULT_URL\n"
    source+="EXPECTED_SHA256='2645420b74c8e2228eb555d14c755bba207c49ea72ecb2eff4c950892f743364'\n"
    source+="BOOT_SEED=20261003\n# PAYOFF-B analysis\n"
    clean=neutralize(source)
    safe_text(clean,"script")
    assert "from source_workbook_reader import DEFAULT_URL" in clean
    assert "20261003" in clean
    assert "2645420b74c8e2228eb555d14c755bba207c49ea72ecb2eff4c950892f743364" in clean
    assert "payoff_b" not in clean.lower()
    assert "animal_phase_variance.py" in reproduction_script()


def test_unauthorized_personal_information_fails():
    for t in ("PAYOFF-B","zuizui0223","contact@mail.org"):
        with pytest.raises(ValueError):
            safe_text("sample "+t,"supplemental.txt")


def test_validator_frozen_number_tolerance_does_not_rescue_contradiction():
    close_value([0.2488754818871811],[0.2488754818871811+1e-11],"phase.ratio")
    with pytest.raises(ValueError,match="differs"):
        close_value(.248875,.91,"phase.variance_ratio")


def test_wrong_source_sha_aborts_before_archive_created(tmp_path):
    base=tmp_path/"base.zip";base.write_bytes(b"not valid artifact")
    workbook=tmp_path/"data.xlsx";workbook.write_bytes(b"fake")
    qc=tmp_path/"qc.json";qc.write_text("{}")
    with pytest.raises(ValueError,match="archive digest"):
        prepare(base,workbook,qc,tmp_path/"out")


def test_cannot_promote_without_true_deer_reproduction(tmp_path):
    root=tmp_path/"root"
    (root/"outputs/deer").mkdir(parents=True)
    (root/"outputs/deer/verified_deer.json").write_text('{"status":"DEER_NOT_ESTIMABLE"}')
    with pytest.raises(ValueError,match="not supported"):
        finish(root,tmp_path/"new.zip")
