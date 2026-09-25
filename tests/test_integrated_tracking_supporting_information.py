from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SCRIPT = ROOT / "scripts" / "build_integrated_tracking_supporting_information.py"

spec = importlib.util.spec_from_file_location("integrated_si", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_integrated_supporting_information_contains_both_evidence_layers() -> None:
    text = module.build_supporting_information()
    assert "## S2. Moving-landscape, connectivity and anisotropy robustness" in text
    assert "## S9. Broad 55-species macroecological test" in text
    assert "## S10. Direct phase-control systems, interval scale and reliability" in text
    assert "## S11. Environmental innovation, industrial actuation and Aikens preregistration" in text
    assert "## S12. Integrated provenance and claim boundary" in text


def test_integrated_supporting_information_preserves_preoutcome_aikens_boundary() -> None:
    text = module.build_supporting_information()
    assert "PREOUTCOME status: **UNOPENED**" in text
    assert "No retuning is licensed after the result is opened." in text
    assert "never counted as a fourth independent cross-taxon lambda replication" in text


def test_integrated_supporting_information_contains_registered_empirical_values() -> None:
    text = module.build_supporting_information()
    assert "| observations | 5816 |" in text
    assert "1.042724" in text
    assert "0.749768" in text
    assert "0.811312" in text
    assert "Primary 2/10-km contrast" in text
