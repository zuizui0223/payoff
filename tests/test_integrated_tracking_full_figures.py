from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
SCRIPT = SCRIPTS / "render_integrated_tracking_figures.py"

spec = importlib.util.spec_from_file_location("integrated_full_figures", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_integrated_full_six_figure_set(tmp_path: Path) -> None:
    paths = module.render_all(tmp_path)
    assert paths["manifest"].exists()
    for i in range(1, 7):
        key=f"figure_{i}"
        assert paths[key].exists()
        assert paths[key].stat().st_size > 500

    f1=paths["figure_1"].read_text(encoding="utf-8")
    assert "PAYOFF-B1 benchmark" in f1
    assert "Local identifiability null" in f1
    assert "Broad empirical test" in f1
    assert "temporal buffering delays but does not replace spatial tracking" in f1

    import json
    manifest=json.loads(paths["manifest"].read_text(encoding="utf-8"))
    assert manifest["status"]=="payoff_b_integrated_six_figure_set"
    assert manifest["aikens_outcome_opened"] is False
    assert list(manifest["figures"]) == [f"figure_{i}" for i in range(1,7)]
