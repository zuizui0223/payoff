from __future__ import annotations

import importlib.util
import io
import json
import sys
from pathlib import Path

import pytest

openpyxl = pytest.importorskip("openpyxl")

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "payoff_b_hoge_veluwe_source_gate.py"
CONTRACT = ROOT / "data" / "payoff_b_hoge_veluwe_network_hysteresis_contract_20260927.json"


def load_module():
    spec = importlib.util.spec_from_file_location("hv_source_gate", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def workbook_bytes(start: int, end: int) -> bytes:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "data"
    ws.append(["year", "value"])
    for year in range(start, end + 1):
        ws.append([year, year * 0.1])
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


def test_xlsx_schema_audit_reports_headers_and_year_coverage_only():
    module = load_module()
    schema = module._inspect_xlsx_bytes(workbook_bytes(1980, 2015))

    assert schema["format"] == "xlsx"
    assert schema["sheets"][0]["columns"] == ["year", "value"]
    assert schema["sheets"][0]["year_columns"] == [
        {
            "column": "year",
            "unique_year_count": 36,
            "min_year": 1980,
            "max_year": 2015,
        }
    ]
    assert "value" not in schema["sheets"][0]["year_columns"]


def test_registered_source_gate_passes_when_individual_year_coverages_are_present():
    module = load_module()
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    migrant = module._inspect_xlsx_bytes(workbook_bytes(1980, 2015))
    resident = module._inspect_xlsx_bytes(workbook_bytes(1973, 2020))
    resource = module._inspect_xlsx_bytes(workbook_bytes(1985, 2020))

    status, reasons = module._source_gate_status(
        contract,
        migrant,
        resident,
        resource,
    )
    assert status == "BIOLOGICAL_SOURCE_GATE_PASS_CUE_EXTENSION_PENDING"
    assert reasons == []


def test_registered_source_gate_fails_closed_on_short_year_coverage():
    module = load_module()
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    migrant = module._inspect_xlsx_bytes(workbook_bytes(1980, 2014))
    resident = module._inspect_xlsx_bytes(workbook_bytes(1973, 2020))
    resource = module._inspect_xlsx_bytes(workbook_bytes(1985, 2020))

    status, reasons = module._source_gate_status(
        contract,
        migrant,
        resident,
        resource,
    )
    assert status == "SCHEMA_REVIEW_REQUIRED"
    assert "MIGRANT_YEAR_COVERAGE_NOT_CERTIFIED" in reasons


def test_contract_keeps_gate_a_separate_from_outcome_opening():
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert contract["status"] == "PREOUTCOME_ASSEMBLY_REGISTERED_SOURCE_FILES_UNOPENED"
    assert contract["information_reversal_gate"]["data_used"] == "cue-resource predictive-connectivity series only"
    assert "focal and partner timing are not opened" in contract["information_reversal_gate"]["rule"]

def test_dryad_transport_fallback_is_digest_guarded_and_outcome_blind():
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    resident = contract["sources"]["resident_partner_timing"]["source_transport"]
    mirror = resident["digest_verified_public_mirror"]

    assert mirror["provider"] == "Zenodo"
    assert mirror["record_id"] == 5730499
    assert "computed SHA-256 equals" in mirror["use_rule"]\n    assert "Dryad-declared SHA-256" in mirror["use_rule"]
    amendment = contract["source_gate"]["transport_amendment"]
    assert amendment["scientific_effect"] == "none; Dryad DOI, exact filenames and Dryad-declared SHA-256 remain authoritative"
    assert amendment["outcome_data_inspected"] is False

def test_dryad_download_accepts_only_digest_matching_zenodo_fallback(
    tmp_path: Path,
    monkeypatch,
):
    module = load_module()
    payload = b"registered source bytes"
    declared = module.sha256_bytes(payload)

    monkeypatch.setattr(
        module,
        "_dryad_latest_files",
        lambda session, doi, timeout: (
            {"versionNumber": 1, "publicationDate": "2021-11-26"},
            [
                {
                    "path": "target.xlsx",
                    "size": len(payload),
                    "mimeType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    "digest": declared,
                    "digestType": "sha-256",
                    "_links": {
                        "self": {"href": "/api/v2/files/123"},
                        "stash:download": {"href": "/api/v2/files/123/download"},
                    },
                }
            ],
        ),
    )
    monkeypatch.setattr(
        module,
        "DRYAD_PUBLIC_MIRRORS",
        {
            "10.5061/dryad.test": {
                "provider": "zenodo",
                "record_id": 99,
            }
        },
    )

    class Response:
        def __init__(self, status, content=b"", url="", json_payload=None):
            self.status_code = status
            self.content = content
            self.url = url
            self._json = json_payload

        @property
        def ok(self):
            return 200 <= self.status_code < 300

        def raise_for_status(self):
            if not self.ok:
                raise RuntimeError(f"HTTP {self.status_code}")

        def json(self):
            return self._json

    class Session:
        def get(self, url, timeout=None, allow_redirects=True):
            if "zenodo.org/api/records/99" in url:
                return Response(
                    200,
                    url=url,
                    json_payload={
                        "files": [
                            {
                                "key": "target.xlsx",
                                "checksum": "md5:irrelevant",
                                "links": {"content": "https://mirror.test/target"},
                            }
                        ]
                    },
                )
            if "mirror.test/target" in url:
                return Response(200, content=payload, url=url)
            return Response(403, url=url)

    result = module._dryad_download_file(
        Session(),
        "10.5061/dryad.test",
        "target.xlsx",
        tmp_path,
        10,
    )
    assert result["declared_digest_match"] is True
    assert result["download_transport"] == "zenodo_mirror_digest_verified"
    assert result["sha256"] == declared

def test_mirror_fails_closed_without_authoritative_dryad_sha256(
    tmp_path: Path,
    monkeypatch,
):
    module = load_module()
    payload = b"mirror bytes without authoritative dryad sha"

    monkeypatch.setattr(
        module,
        "_dryad_latest_files",
        lambda session, doi, timeout: (
            {"versionNumber": 1, "publicationDate": "2021-11-26"},
            [
                {
                    "path": "target.xlsx",
                    "size": len(payload),
                    "mimeType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    "digest": None,
                    "digestType": None,
                    "_links": {
                        "self": {"href": "/api/v2/files/123"},
                        "stash:download": {"href": "/api/v2/files/123/download"},
                    },
                }
            ],
        ),
    )
    monkeypatch.setattr(
        module,
        "DRYAD_PUBLIC_MIRRORS",
        {
            "10.5061/dryad.test": {
                "provider": "zenodo",
                "record_id": 99,
            }
        },
    )

    class Response:
        def __init__(self, status, content=b"", url="", json_payload=None):
            self.status_code = status
            self.content = content
            self.url = url
            self._json = json_payload

        @property
        def ok(self):
            return 200 <= self.status_code < 300

        def raise_for_status(self):
            if not self.ok:
                raise RuntimeError(f"HTTP {self.status_code}")

        def json(self):
            return self._json

    class Session:
        def get(self, url, timeout=None, allow_redirects=True):
            if "zenodo.org/api/records/99" in url:
                return Response(
                    200,
                    url=url,
                    json_payload={
                        "files": [
                            {
                                "key": "target.xlsx",
                                "checksum": "md5:irrelevant",
                                "links": {"content": "https://mirror.test/target"},
                            }
                        ]
                    },
                )
            if "mirror.test/target" in url:
                return Response(200, content=payload, url=url)
            return Response(403, url=url)

    with pytest.raises(RuntimeError, match="lacks authoritative SHA-256"):
        module._dryad_download_file(
            Session(),
            "10.5061/dryad.test",
            "target.xlsx",
            tmp_path,
            10,
        )

def test_dryad_dataset_archive_extracts_exact_registered_file(tmp_path: Path):
    module = load_module()

    archive_buf = io.BytesIO()
    import zipfile
    with zipfile.ZipFile(archive_buf, "w") as archive:
        archive.writestr("nested/target.xlsx", b"registered bytes")
        archive.writestr("nested/other.txt", b"other")

    class Response:
        status_code = 200
        ok = True
        content = archive_buf.getvalue()
        url = "https://datadryad.org/api/v2/datasets/example/download"

        def raise_for_status(self):
            return None

    class Session:
        def get(self, url, timeout=None, allow_redirects=True):
            return Response()

    result = module._dryad_dataset_archive_download(
        Session(),
        doi="10.5061/dryad.example",
        exact_name="target.xlsx",
        output_dir=tmp_path,
        timeout=10,
    )

    assert result["provider"] == "dryad_dataset_archive"
    assert result["filename"] == "target.xlsx"
    assert (tmp_path / "target.xlsx").read_bytes() == b"registered bytes"
    assert result["sha256"] == module.sha256_bytes(b"registered bytes")

