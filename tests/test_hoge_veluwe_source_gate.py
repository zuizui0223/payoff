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
    assert "computed SHA-256 equals" in mirror["use_rule"]
    assert "Dryad-declared SHA-256" in mirror["use_rule"]
    amendment = contract["source_gate"]["transport_amendment"]
    effect = amendment["scientific_effect"]
    assert effect.startswith("none; Dryad DOI")
    assert "exact filenames" in effect
    assert "authoritative Dryad SHA-256" in effect
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

def test_compound_year_header_is_certified():
    module = load_module()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "data"
    ws.append(["YearOfBreeding", "LayDateApril"])
    for year in range(1973, 2021):
        ws.append([year, 20])
    buf = io.BytesIO()
    wb.save(buf)

    schema = module._inspect_xlsx_bytes(buf.getvalue())
    row = schema["sheets"][0]["year_columns"][0]
    assert row["column"] == "YearOfBreeding"
    assert row["min_year"] == 1973
    assert row["max_year"] == 2020


def test_mda_html_landing_form_resolves_binary_file(tmp_path: Path):
    module = load_module()
    html = b"""<!doctype html><html><body>
    <h3>File: 'TomotaniData.xlsx'</h3>
    <form method="post" action="download.php">
      <input type="hidden" name="fid" value="VLIZ_TEST">
      <button type="submit">Download</button>
    </form>
    </body></html>"""
    payload = workbook_bytes(1980, 2015)

    class Response:
        def __init__(self, status=200, content=b"", url="", headers=None):
            self.status_code = status
            self.content = content
            self.url = url
            self.headers = headers or {}
            self.encoding = "utf-8"

        @property
        def ok(self):
            return 200 <= self.status_code < 300

        def raise_for_status(self):
            if not self.ok:
                raise RuntimeError(f"HTTP {self.status_code}")

    class Session:
        def get(self, url, timeout=None, allow_redirects=True):
            return Response(
                200,
                html,
                "https://mda.example/directlink.php?fid=VLIZ_TEST",
                {"Content-Type": "text/html; charset=UTF-8"},
            )

        def post(self, url, data=None, timeout=None, allow_redirects=True):
            assert url == "https://mda.example/download.php"
            assert data == {"fid": "VLIZ_TEST"}
            return Response(
                200,
                payload,
                url,
                {
                    "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    "Content-Disposition": 'attachment; filename="TomotaniData.xlsx"',
                },
            )

    out = module._mda_download_file(
        Session(),
        "https://mda.example/directlink.php?fid=VLIZ_TEST",
        tmp_path,
        10,
    )
    assert out["filename"] == "TomotaniData.xlsx"
    assert out["landing_resolution"]["resolution"] == "html_form_post"

def test_cue_extension_receipt_is_required_for_final_gate_a_pass(tmp_path: Path):
    module = load_module()

    missing, missing_ok = module._load_cue_extension_receipt(None)
    assert missing["status"] == "NOT_PROVIDED"
    assert missing_ok is False

    receipt = tmp_path / "cue.json"
    receipt.write_text(
        json.dumps(
            {
                "status": "SOURCE_FAITHFUL_CUE_EXTENSION_COMPLETE",
                "years": [1980, 2015],
                "n_years": 36,
                "annual_csv_sha256": "abc123",
                "cue_window": "20 calendar days beginning 18 February",
                "grid_latitudes_deg_n": [10.0, 7.5, 5.0],
                "grid_longitudes_deg_e": [352.5, 355.0, 357.5],
                "transport_counts": {"erddap": 36},
                "outcome_firewall": {
                    "resource_data_read": False,
                    "resident_timing_read": False,
                    "migrant_timing_read": False,
                    "cue_resource_connectivity_computed": False,
                    "information_reversal_gate_opened": False,
                    "history_test_opened": False,
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    summary, ok = module._load_cue_extension_receipt(receipt)
    assert ok is True
    assert summary["certified"] is True
    assert summary["firewall_true_flags"] == []

