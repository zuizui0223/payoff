import json
import subprocess
import sys
from pathlib import Path


def test_information_deadlines_renderer_builds_seven_outcome_independent_svgs(tmp_path):
    root = Path(__file__).resolve().parents[1]
    out = tmp_path / "figures"
    subprocess.run(
        [
            sys.executable,
            str(root / "scripts" / "render_information_deadlines_figures.py"),
            "--output-dir",
            str(out),
        ],
        cwd=root,
        check=True,
    )

    manifest_path = out / "PAYOFF_B_INFORMATION_DEADLINES_V2_FIGURE_MANIFEST.json"
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["aikens_outcome_used"] is False
    assert len(manifest["figures"]) == 7

    for row in manifest["figures"].values():
        path = Path(row["path"])
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert text.startswith("<svg")
        assert "AIKENS_LAMBDA" not in text
        assert row["bytes"] > 1000
        assert len(row["sha256"]) == 64


def test_information_figures_include_core_headlines(tmp_path):
    root = Path(__file__).resolve().parents[1]
    out = tmp_path / "figures"
    subprocess.run(
        [
            sys.executable,
            str(root / "scripts" / "render_information_deadlines_figures.py"),
            "--output-dir",
            str(out),
        ],
        cwd=root,
        check=True,
    )

    fig2 = (out / "PAYOFF_B_INFO_V2_FIG2_DESYNCHRONIZATION.svg").read_text(
        encoding="utf-8"
    )
    fig3 = (out / "PAYOFF_B_INFO_V2_FIG3_NETWORK_MEMORY.svg").read_text(
        encoding="utf-8"
    )
    fig5 = (out / "PAYOFF_B_INFO_V2_FIG5_INFORMATION_AXES.svg").read_text(
        encoding="utf-8"
    )

    assert "transiently worsen coordination" in fig2
    assert "52 / 364 strict-memory cells" in fig3
    assert "0 / 404 strict-memory cells" in fig3
    assert "history model: NOT RUN" in fig5



def test_information_figures_include_rescue_topology(tmp_path):
    root = Path(__file__).resolve().parents[1]
    out = tmp_path / "figures"
    subprocess.run(
        [
            sys.executable,
            str(root / "scripts" / "render_information_deadlines_figures.py"),
            "--output-dir",
            str(out),
        ],
        cwd=root,
        check=True,
    )

    fig7 = (out / "PAYOFF_B_INFO_V2_FIG7_RESCUE.svg").read_text(
        encoding="utf-8"
    )
    assert "local pollinator only" in fig7
    assert "any actor" in fig7
    assert "Trap stability and rescue leverage are different network properties." in fig7
