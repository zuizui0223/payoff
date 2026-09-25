from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_integrated_tracking_empirical_figures.py"

spec = importlib.util.spec_from_file_location("integrated_figures", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_integrated_empirical_figures_render_from_machine_inputs(tmp_path: Path) -> None:
    paths = module.render_all(tmp_path)
    for key in ("figure_4", "figure_5", "figure_6", "manifest"):
        assert paths[key].exists()

    f4 = paths["figure_4"].read_text(encoding="utf-8")
    assert "Natural data reject a universal speed rule and simple temporal substitution" in f4
    assert "u*=0.405" in f4
    assert "u*=1.043" in f4
    assert "u*=1.397" in f4
    assert "11/41" in f4
    assert "Registered timing-substitution holdout" in f4
    assert "FAIL_WRONG_DIRECTION" in f4
    assert "+0.035 ± 0.029" in f4
    assert "Timing responsiveness lowers mean mismatch" in f4

    f5 = paths["figure_5"].read_text(encoding="utf-8")
    assert "Mule deer" in f5
    assert "Eurasian wigeon ERA5" in f5
    assert "Secondary path-memory comparison" in f5

    f6 = paths["figure_6"].read_text(encoding="utf-8")
    assert "Environmental innovation vs retention" in f6
    assert "8/8 definitions: G_large &lt; G_small" in f6
    assert "UNOPENED" in f6
    assert "No retuning permitted." in f6
