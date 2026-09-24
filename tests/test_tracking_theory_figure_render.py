import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from render_tracking_theory_figures import render_all


def test_tracking_theory_renderer_writes_five_svg_figures(tmp_path):
    manifest = render_all(tmp_path)
    assert manifest["frozen_date"] == "2026-09-20"
    assert len(manifest["figures"]) == 5

    for key, row in manifest["figures"].items():
        path = Path(row["path"])
        assert path.exists(), key
        assert path.suffix == ".svg"
        text = path.read_text(encoding="utf-8")
        assert text.startswith("<svg")
        assert "Frozen" in text or "frozen" in text
        assert row["bytes"] == path.stat().st_size
        assert row["bytes"] > 1000

    saved = json.loads(
        (tmp_path / "PAYOFF_B_TRACKING_FIGURE_MANIFEST.json").read_text(
            encoding="utf-8"
        )
    )
    assert saved["source_policy"] == manifest["source_policy"]


def test_tracking_theory_svg_contains_core_claim_labels(tmp_path):
    render_all(tmp_path)
    figure3 = (
        tmp_path / "PAYOFF_B_TRACKING_FIG3_COORDINATION_GATE.svg"
    ).read_text(encoding="utf-8")
    figure5 = (
        tmp_path / "PAYOFF_B_TRACKING_FIG5_DEMOGRAPHY_DRIFT.svg"
    ).read_text(encoding="utf-8")
    figure6 = (
        tmp_path / "PAYOFF_B_TRACKING_FIG6_COMPLEMENTARITY.svg"
    ).read_text(encoding="utf-8")

    assert "coordinated gain" in figure3
    assert "unilateral gain A" in figure3
    assert "pilot cells &gt;=0.10: 9; replication cells &gt;=0.10: 0" in figure5
    assert "0/7 controller gains persist" in figure6
    assert "7/7 persist" in figure6
