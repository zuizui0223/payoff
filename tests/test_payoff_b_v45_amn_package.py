import hashlib
import importlib.util
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_payoff_b_v45_amn_package.py"


def load_module():
    spec = importlib.util.spec_from_file_location("v45package", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_build_package_and_anonymous_boundaries(tmp_path):
    module = load_module()
    out = tmp_path / "pkg"
    zip_path = tmp_path / "pkg.zip"
    result = module.build(out, zip_path)

    manifest = json.loads(Path(result["manifest"]).read_text(encoding="utf-8"))
    assert manifest["target"] == "The American Naturalist"
    assert manifest["article_type"] == "Major Article"
    assert manifest["manuscript"]["abstract_words"] <= 200
    assert manifest["manuscript"]["main_text_words"] <= 7500

    anonymous = (out / "anonymous_manuscript.md").read_text(encoding="utf-8")
    for forbidden in module.FORBIDDEN:
        assert forbidden.lower() not in anonymous.lower()

    assert "Figure 1" in anonymous
    assert "Figure 2" in anonymous
    assert "Figure 3" in anonymous

    assert (out / "supporting_information.md").exists()
    assert (out / "figure_captions.md").exists()
    assert (out / "figures" / "PAYOFF_B_V45_FIG1_FRAMEWORK.svg").exists()
    assert (out / "figures" / "PAYOFF_B_V45_FIG2_BIRDS.svg").exists()
    assert (out / "figures" / "PAYOFF_B_V45_FIG3_MULE_DEER.svg").exists()
    assert zip_path.exists()


def test_package_zip_is_deterministic_at_fixed_output_path(tmp_path):
    module = load_module()
    out = tmp_path / "pkg"
    zip_path = tmp_path / "pkg.zip"

    module.build(out, zip_path)
    first = digest(zip_path)
    module.build(out, zip_path)
    second = digest(zip_path)

    assert first == second


def test_anonymous_file_list_excludes_title_page(tmp_path):
    module = load_module()
    out = tmp_path / "pkg"
    zip_path = tmp_path / "pkg.zip"
    module.build(out, zip_path)

    manifest = json.loads((out / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    anon = set(manifest["anonymous_reviewer_files"])
    assert "title_page_TEMPLATE_NOT_FOR_REVIEW.md" not in anon

    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
    assert "title_page_TEMPLATE_NOT_FOR_REVIEW.md" in names
