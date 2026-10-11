"""Network-free tests of 2017 Dryad source gate and outcome firewall."""
import json
from pathlib import Path

import pytest

from scripts import payoff_b_social_cue_source_audit as audit


MANIFEST = (
    Path(__file__).resolve().parents[1]
    / "data/payoff_b_social_cue_source_manifest_20261011.json"
)


def test_metadata_exactly_seven_files_and_no_outcomes():
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    files = audit.validate_manifest(m)
    assert len(files) == 7
    assert {f["file_id"] for f in files} == {
        34678, 34672, 34677, 34676, 34675, 34673, 34674
    }
    assert m["outcome_status"] == "UNOPENED"
    assert "predictor_outcome_join" in m["forbidden_extractions"]


def test_headers_only_receipt_ignores_row_values():
    blob = b"year;plot;measure\r2014;A;1,3\r2015;B;2,4\r"
    info = {"name": "arrival.csv", "file_id": 34672,
            "size": len(blob), "role": "arrival"}
    r = audit.source_receipt(info, blob, "https://datadryad.org/example")
    assert r["metadata_only"] is True
    assert r["schema"] == {
        "n_rows": 2, "n_columns": 3, "columns": ["year", "plot", "measure"],\n        "delimiter": ";", "decimal_mark": ",",\n        "published_reader": 'read.table(sep=";", dec=",")'
    }
    assert "2014" not in json.dumps(r) and "2015" not in json.dumps(r)


def test_reject_wrong_size_and_bad_headers():
    b = b"year;plot\n2014;A\n"
    info = {"name": "arrival.csv", "file_id": 34672,
            "size": 1, "role": "arrival"}
    with pytest.raises(ValueError, match="File-size mismatch"):
        audit.source_receipt(info, b, "dummy")
    info["size"] = len(b"x;x\n1;2\n")
    with pytest.raises(ValueError, match="Duplicate column headers"):
        audit.source_receipt(info, b"x,x\n1,2\n", "dummy")


def test_reject_wrong_delimiter_when_source_requires_semicolon():
    bad = b"year,plot\\n2014,A\\n"
    info = {"name": "arrival.csv", "file_id": 34672,
            "size": len(bad), "role": "arrival"}
    with pytest.raises(ValueError, match="Unusable column header"):
        audit.source_receipt(info, bad, "dummy")


def test_fake_source_pass_does_not_open_outcomes(monkeypatch):
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    fake = {}
    for row in m["files"]:
        value = b"x;y\n1;2\n3;4\n" if row["name"].endswith(".csv") \
            else b"# source only\n"
        row["size"] = len(value)
        fake[row["name"]] = value

    def fake_download(meta, timeout=30):
        return fake[meta["name"]], "https://datadryad.org/test"

    monkeypatch.setattr(audit, "download", fake_download)
    result = audit.run(m)
    assert result["status"] == "SOURCE_SCHEMA_PASS_MECHANISM_NOT_IDENTIFIED"
    assert result["file_success_n"] == 7
    assert result["outcome_opened"] is False
    assert result["analysis_outcome_computed"] is False


def test_partial_download_is_fail_closed(monkeypatch):
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for f in m["files"]:
        f["size"] = 8

    def fake_download(meta, timeout=30):
        raise RuntimeError("SOURCE_ACCESS_BLOCKED")

    monkeypatch.setattr(audit, "download", fake_download)
    r = audit.run(m)
    assert r["status"] == "SOURCE_ACCESS_OR_SCHEMA_BLOCKED"
    assert r["file_success_n"] == 0
    assert r["outcome_opened"] is False


def test_refuse_outcome_open_and_schema_drift():
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    m["outcome_status"] = "OPENED"
    with pytest.raises(ValueError, match="reopen outcome"):
        audit.validate_manifest(m)
    m["outcome_status"] = "UNOPENED"
    m["files"][0]["name"] = "posthoc_new_outcome.csv"
    with pytest.raises(ValueError, match="Unexpected file names"):
        audit.validate_manifest(m)
