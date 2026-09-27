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
