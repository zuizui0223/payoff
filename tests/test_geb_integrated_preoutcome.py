from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

BUILD_PATH = SCRIPTS / "build_geb_integrated_preoutcome_source.py"
AUDIT_PATH = SCRIPTS / "audit_geb_integrated_preoutcome.py"
FIG_PATH = SCRIPTS / "render_geb_integrated_figures.py"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


builder = load("geb_builder", BUILD_PATH)
auditor = load("geb_auditor", AUDIT_PATH)
figures = load("geb_figures", FIG_PATH)


def test_geb_overlay_passes_preoutcome_gates(tmp_path: Path) -> None:
    path = tmp_path / "geb.md"
    path.write_text(builder.build_source(), encoding="utf-8")
    result = auditor.audit(path)
    assert result["all_preoutcome_hard_gates_pass"] is True
    assert result["metrics"]["abstract_words"] <= 300
    assert result["metrics"]["main_body_words"] <= 5000
    assert result["metrics"]["display_pieces"] == 6
    assert result["metrics"]["keyword_count"] == 8
    assert result["final_submission_eligible"] is False


def test_geb_overlay_strips_internal_sections_and_preserves_aikens_markers() -> None:
    text = builder.build_source()
    assert "**Status:**" not in text
    assert "**Publication architecture:**" not in text
    assert "## Claim ceiling" not in text
    assert "## Figure architecture" not in text
    assert "## Prior-art boundary" not in text
    assert "### 5.8 Relationship to existing literature" in text
    for name in ("ABSTRACT", "RESULTS", "DISCUSSION", "CONCLUSION"):
        assert text.count(f"<!-- AIKENS_LAMBDA_{name}_START -->") == 1
        assert text.count(f"<!-- AIKENS_LAMBDA_{name}_END -->") == 1


def test_geb_figure_overlay_changes_panel_labels_only(tmp_path: Path) -> None:
    rendered = figures.render_all(tmp_path)
    manifest = __import__("json").loads(
        rendered["manifest"].read_text(encoding="utf-8")
    )
    assert manifest["scientific_result_changed"] is False
    assert len(manifest["figures"]) == 6
    for row in manifest["figures"].values():
        assert row["format_change_only"] is True
    combined = "\n".join(
        rendered[f"figure_{i}"].read_text(encoding="utf-8")
        for i in range(1, 7)
    )
    assert ">A  " not in combined
    assert ">B  " not in combined
    assert ">C  " not in combined
