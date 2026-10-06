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
    assert (out / "figures" / "figure1.svg").exists()
    assert (out / "figures" / "figure2.svg").exists()
    assert (out / "figures" / "figure3.svg").exists()
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


def test_anonymous_bundle_contains_no_title_page(tmp_path):
    module = load_module()
    out = tmp_path / "pkg"
    zip_path = tmp_path / "pkg.zip"
    module.build(out, zip_path)

    manifest = json.loads((out / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    anon = set(manifest["anonymous_reviewer_files"])
    assert all("title_page" not in name.lower() for name in anon)

    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
    assert all("title_page" not in name.lower() for name in names)


def test_amnat_metadata_limits():
    front = (ROOT / "submission" / "AMNAT_V4_5_FRONTMATTER_20261006.md").read_text(encoding="utf-8")
    manuscript = (ROOT / "manuscript" / "PAYOFF_B_FORECAST_ACCESS_CORRECTION_V4_5_AMNAT.md").read_text(encoding="utf-8")
    captions = (ROOT / "submission" / "AMNAT_V4_5_FIGURE_CAPTIONS_20261006.md").read_text(encoding="utf-8")

    short = front.split("## Short title", 1)[1].split("## Abstract", 1)[0]
    short = short.replace("**", "").strip()
    assert len(short) <= 40

    keyword_text = manuscript.split("Keywords:", 1)[1].split("---", 1)[0]
    keywords = [x.strip() for x in keyword_text.replace("\n", " ").split(";") if x.strip()]
    assert 1 <= len(keywords) <= 6

    chunks = captions.split("## Figure ")[1:]
    assert len(chunks) == 3
    for chunk in chunks:
        body = chunk.split("\n\n", 1)[1]
        words = [w for w in body.replace("\n", " ").split() if w]
        assert len(words) <= 100

    for n in (1, 2, 3):
        assert f"Figure {n}" in manuscript
