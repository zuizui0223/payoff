import importlib.util
import sys
import json
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_payoff_b_v45_main_figures.py"
DATA = ROOT / "data" / "payoff_b_v45_figure_data_20261006.json"


def load_module():
    spec = importlib.util.spec_from_file_location("v45figs", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_v45_figure_data_status_and_boundaries():
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    assert payload["status"] == "frozen_v45_main_figure_data"
    assert payload["figure_2"]["preregistered"]["delta_rho"] > 0
    assert payload["figure_2"]["posthoc_environment"]["delta_Gcv_d2"] > 0
    assert payload["figure_2"]["observability"]["early"]["before_source_arrival"] < 0.5
    assert payload["figure_2"]["observability"]["early"]["after_target_arrival"] > 0.3
    assert payload["figure_3"]["movement_slope_km_day_per_phase_day"] > 0
    assert payload["figure_3"]["stopover_slope_day_per_phase_day"] < 0


def test_render_all_is_deterministic_and_valid_svg(tmp_path):
    module = load_module()
    one = tmp_path / "one"
    two = tmp_path / "two"
    out1 = module.render_all(one)
    out2 = module.render_all(two)

    m1 = json.loads(Path(out1["manifest"]).read_text(encoding="utf-8"))
    m2 = json.loads(Path(out2["manifest"]).read_text(encoding="utf-8"))

    assert m1["figure_data_sha256"] == m2["figure_data_sha256"]
    assert set(m1["figures"]) == {"figure_1", "figure_2", "figure_3"}

    for key in ("figure_1", "figure_2", "figure_3"):
        assert m1["figures"][key]["sha256"] == m2["figures"][key]["sha256"]
        p = Path(out1[key])
        root = ET.parse(p).getroot()
        assert root.tag.endswith("svg")
        txt = p.read_text(encoding="utf-8")
        assert "PAYOFF-B" not in txt
        assert "V4.5" not in txt
        assert "Figure" in txt


def test_key_claims_appear_in_expected_figures(tmp_path):
    module = load_module()
    out = module.render_all(tmp_path)

    fig1 = Path(out["figure_1"]).read_text(encoding="utf-8")
    fig2 = Path(out["figure_2"]).read_text(encoding="utf-8")
    fig3 = Path(out["figure_3"]).read_text(encoding="utf-8")

    assert "Forecastability" in fig1
    assert "accessible" in fig1
    assert "Forecastable" in fig1

    assert "0.284" in fig2
    assert "0.653" in fig2
    assert "139/166" in fig2
    assert "29.8%" in fig2
    assert "41.6%" in fig2
    assert "signed lag" in fig2

    assert "26.41 d" in fig3
    assert "13.17 d" in fig3
    assert "0.0683" in fig3
    assert "-0.492" in fig3
