from pathlib import Path
import importlib.util
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


source = load(
    "v2_geb_source",
    SCRIPTS / "build_payoff_b_v2_geb_source.py",
)
audit = load(
    "v2_geb_audit",
    SCRIPTS / "audit_payoff_b_v2_geb_source.py",
)
package = load(
    "v2_geb_package",
    SCRIPTS / "build_payoff_b_v2_geb_preoutcome_package.py",
)


def test_v2_geb_blinded_source_passes_hard_gates():
    text = source.build_source()
    result = audit.audit(text)

    assert text.startswith(
        "# Information deadlines can desynchronize seasonal interactions "
        "under environmental change"
    )
    assert "Dossman et al., 2023" in text
    assert "Raw waiting time therefore does not generally rank effective deadlines" in text
    assert 'python -m pip install -e ".[test,empirical]"' in text
    assert "statsmodels>=0.14" in text
    assert "fails if any of those tests are skipped" in text
    assert "We therefore do not treat cue–driver decoupling itself as a new idea." in text
    assert "the earlier temporal-buffering result" in text
    assert "the transparent model witness" in text
    assert "not a new discovery of this study" in text
    assert "We therefore do not claim a natural information-recovery hysteresis event." in text
    assert "We therefore distinguish:" in text
    assert "Our analysis therefore begins one step later." in text
    assert "remains unopened in this working package" not in text
    assert "handled only in Supporting Information under" in text
    assert "does not retune the" in text
    assert result["metrics"]["deinternalization_artifact_hits"] == []
    assert result["all_preoutcome_hard_gates_pass"]
    assert result["metrics"]["abstract_words"] <= 300
    assert result["metrics"]["main_body_words"] <= 5000
    assert result["metrics"]["reference_count"] <= 50
    assert result["metrics"]["figure_legend_count"] == 7
    assert result["metrics"]["internal_token_hits"] == []
    assert result["metrics"]["email_hits"] == []


def test_v2_geb_package_is_complete_but_not_finally_eligible(tmp_path):
    out = tmp_path / "package"
    zip_path = tmp_path / "package.zip"
    manifest = package.build(out, zip_path)

    assert manifest["canonical_source"].endswith(
        "PAYOFF_B_INFORMATION_COORDINATION_V2_PREOUTCOME.md"
    )
    assert manifest["v1_status"] == "FROZEN_PROVENANCE_ONLY"
    assert manifest["aikens_outcome_opened"] is False
    assert manifest["final_submission_eligible"] is False
    assert manifest["figure_count"] == 7
    assert (out / "GEB_V2_DECLARATIONS_TEMPLATE.md").exists()
    assert "anonymous reviewer archive delivery channel" in manifest["final_submission_blockers"]
    assert not (out / "PAYOFF_B_V1_V2_PUBLICATION_RELATION_20260927.md").exists()
    assert zip_path.exists()


def test_v2_geb_package_zip_is_deterministic(tmp_path):
    z1 = tmp_path / "one.zip"
    z2 = tmp_path / "two.zip"
    package.build(tmp_path / "one", z1)
    package.build(tmp_path / "two", z2)
    assert package.sha256(z1) == package.sha256(z2)
