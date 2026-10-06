import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_payoff_b_v45_reproducibility_bundle.py"


def load_module():
    spec = importlib.util.spec_from_file_location("reprobundle", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_reproducibility_bundle_builds_and_is_anonymous(tmp_path):
    module = load_module()
    out = tmp_path / "bundle"
    zip_path = tmp_path / "bundle.zip"
    result = module.build(out, zip_path)

    manifest = json.loads(Path(result["manifest"]).read_text(encoding="utf-8"))
    assert manifest["status"] == "anonymous_review_reproducibility_bundle"
    assert result["file_count"] >= 20
    assert (out / "README_REVIEW.txt").exists()
    assert zip_path.exists()

    for path in out.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for forbidden in module.FORBIDDEN_IDENTIFIERS:
            assert forbidden.lower() not in text.lower()


def test_reproducibility_zip_is_deterministic(tmp_path):
    module = load_module()
    out = tmp_path / "bundle"
    zip_path = tmp_path / "bundle.zip"
    module.build(out, zip_path)
    first = digest(zip_path)
    module.build(out, zip_path)
    second = digest(zip_path)
    assert first == second
