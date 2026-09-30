from pathlib import Path

import pytest

import scripts.materialize_snow_goose_2026_dryad as materialize


def ready_manifest():
    return {
        "classification": "PUBLIC_J_MECHANISM_SOURCE_READY",
        "probe_id": "probe",
        "files": [
            {
                "path": name,
                "download_href": f"https://example.test/{name}",
            }
            for name in sorted(materialize.REQUIRED)
        ],
    }


def test_selects_only_frozen_required_files():
    manifest = ready_manifest()
    manifest["files"].append({
        "path": "other.txt",
        "download_href": "https://example.test/other.txt",
    })
    selected = materialize.select_required_files(manifest)
    assert {row["path"] for row in selected} == materialize.REQUIRED


def test_unresolved_manifest_fails_closed():
    manifest = ready_manifest()
    manifest["classification"] = "PUBLIC_J_MECHANISM_SOURCE_UNRESOLVED"
    with pytest.raises(ValueError, match="not PUBLIC_J_MECHANISM_SOURCE_READY"):
        materialize.select_required_files(manifest)


def test_missing_required_file_fails_closed():
    manifest = ready_manifest()
    manifest["files"] = manifest["files"][:-1]
    with pytest.raises(ValueError, match="required Dryad files missing"):
        materialize.select_required_files(manifest)


def test_output_must_be_outside_repo(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    monkeypatch.setattr(materialize, "REPO_ROOT", repo)

    outside = tmp_path / "private"
    assert materialize.ensure_outside_repo(outside) == outside.resolve()

    with pytest.raises(ValueError, match="outside the PAYOFF-B repository"):
        materialize.ensure_outside_repo(repo / "data")
