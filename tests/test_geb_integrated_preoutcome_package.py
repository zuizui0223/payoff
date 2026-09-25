from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SCRIPT = ROOT / "scripts" / "build_geb_integrated_preoutcome_package.py"

spec = importlib.util.spec_from_file_location("geb_package", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_geb_preoutcome_package_is_complete_but_blocked(tmp_path: Path) -> None:
    out = tmp_path / "geb"
    zip_path = tmp_path / "geb.zip"
    m = module.build(out, zip_path)
    assert m["journal"] == "Global Ecology and Biogeography"
    assert m["article_type"] == "Research Article"
    assert m["scientific_state"] == "PREOUTCOME_INTERNAL_READY"
    assert m["final_submission_eligible"] is False
    assert m["figure_count"] == 6
    assert m["structured_abstract_words"] <= 300
    assert m["main_body_words"] <= 5000
    assert zip_path.exists()


def test_geb_preoutcome_zip_is_deterministic(tmp_path: Path) -> None:
    z1 = tmp_path / "one.zip"
    z2 = tmp_path / "two.zip"
    module.build(tmp_path / "one", z1)
    module.build(tmp_path / "two", z2)
    assert module.sha256(z1) == module.sha256(z2)
