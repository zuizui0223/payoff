"""Tests of anonymization and non-submission-ready anonymous editorial preview."""
from __future__ import annotations

from pathlib import Path

import pytest

from scripts.build_amnat_v4_anonymous_preview import (
    TITLE, anonymize, build_preview,
)

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"manuscript/PAYOFF_B_INFORMATION_CONTROL_V4_V8_INTEGRATED.md"


def source():
    return SOURCE.read_text(encoding="utf-8")


def test_anonymization_preserves_frozen_claims_math_and_20_reference_core():
    old=source()
    new=anonymize(old)
    assert new.startswith("# "+TITLE)
    assert "PAYOFF-B" not in new
    assert "V8" not in new
    assert "V3" not in new
    assert "V4" not in new
    assert "Post-freeze transparency statement" not in new
    assert "## Literature Cited" in new
    assert new.count("https://doi.org/") >= 20
    assert "0.369" in new and "0.062" in new
    assert "152 animal-years" in new
    assert "same individuals' migration speed" in new
    assert old.count(r"\[") == new.count(r"\[")
    assert len(new) < len(old)


def test_preview_receipt_is_explicitly_non_submission_ready(tmp_path):
    path=tmp_path/"anonymous_preview.md"
    result=build_preview(source(),path)
    assert path.exists()
    assert result["status"]=="ANONYMOUS_MARKDOWN_EDITORIAL_PREVIEW_SUBMISSION_HOLD"
    assert result["admin_provenance_stripped"]
    assert result["figure_count"]==0
    assert result["approved_for_journal_submission"] is False
    assert result["full_underlying_data_included"] is False
    assert "Original" not in result.get("figure_images",[])
    assert "PAYOFF-B" not in path.read_text(encoding="utf-8")


def test_missing_cited_bibliography_fails_closed():
    text=source()
    with pytest.raises(ValueError,match="Literature Cited"):
        anonymize(text.replace("## Literature Cited","## Bibliography Missing"))


def test_internal_project_title_drift_fails_closed():
    text=source()
    with pytest.raises(ValueError,match="title"):
        anonymize(text.replace(TITLE,"A dramatically different title",1))


def test_missing_data_claim_fails_closed():
    text=source().replace("+0.369","0.999")
    with pytest.raises(ValueError,match="Major numeric"):
        anonymize(text)
