import importlib.util
import json
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

spec = importlib.util.spec_from_file_location(
    "v2_review_archive",
    SCRIPTS / "build_payoff_b_v2_review_archive.py",
)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


FORBIDDEN = (
    "zuizui0223",
    "ZHANG RUIQI",
    "rachelzhang0223",
    "github.com/zuizui0223",
)


def synthetic_aikens_result():
    return {
        "status": "phase_retention_contrast_gate_fail",
        "gate": {
            "passed": False,
            "direction_passed": True,
            "support_passed": False,
            "lambda_difference_b_minus_a": 0.1,
            "observation": {
                "lambda_a": 0.3,
                "lambda_b": 0.4,
                "p_difference": 0.2,
            },
        },
    }


def assert_archive_anonymous(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".py", ".md", ".json", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()
        for token in FORBIDDEN:
            assert token.lower() not in lowered, (path, token)


def test_preoutcome_review_archive_is_anonymous_and_deterministic(tmp_path):
    out1 = tmp_path / "one"
    out2 = tmp_path / "two"
    z1 = tmp_path / "one.zip"
    z2 = tmp_path / "two.zip"

    m1 = module.build(out1, zip_path=z1)
    m2 = module.build(out2, zip_path=z2)

    assert m1["aikens_gate_resolved"] is False
    assert m1["aikens_result_included"] is False
    assert m1["file_count"] > 10
    assert m1["code_file_count"] > 5
    assert module.sha256(z1) == module.sha256(z2)
    assert_archive_anonymous(out1)

    with zipfile.ZipFile(z1) as archive:
        names = set(archive.namelist())
    assert "README_REVIEW.md" in names
    assert "REVIEW_ARCHIVE_MANIFEST.json" in names
    assert "data/aikens2022_lambda_perturbation_registration_20260921.json" in names


def test_postoutcome_review_archive_adds_only_frozen_result(tmp_path):
    result = tmp_path / "aikens.json"
    result.write_text(
        json.dumps(synthetic_aikens_result(), indent=2) + "\n",
        encoding="utf-8",
    )

    out = tmp_path / "post"
    manifest = module.build(
        out,
        zip_path=tmp_path / "post.zip",
        aikens_result_json=result,
    )

    assert manifest["aikens_gate_resolved"] is True
    assert manifest["aikens_result_included"] is True
    assert (
        out / "data" / "registered_aikens_phase_retention_result.json"
    ).exists()
    assert_archive_anonymous(out)


def test_archive_excludes_publication_and_identity_surfaces(tmp_path):
    out = tmp_path / "bundle"
    module.build(out)

    relative = {
        path.relative_to(out).as_posix()
        for path in out.rglob("*")
        if path.is_file()
    }
    assert not any(path.startswith("submission/") for path in relative)
    assert not any(path.startswith(".github/") for path in relative)
    assert "docs/PUBLICATION_STATUS.md" not in relative
    assert not any("credential" in path.lower() for path in relative)
