from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "theory" / "PHASE_VELOCITY_TEMPORAL_BUFFERING.md"


def test_phase_velocity_note_has_intact_latex_and_no_control_character_corruption() -> None:
    text = NOTE.read_text(encoding="utf-8")
    for required in (
        r"\frac{\partial e}{\partial z}=-v_A",
        r"\frac{\partial e}{\partial t}=v_E-v_A",
        r"v_E\neq v_A",
        r"|z|\le z_{\max}",
        r"T_{\rm buffer}",
        r"\frac{u z_{\max}}{|1-u|}",
        r"\beta_{q^2\times h}=+0.0351\pm0.0289",
        r"\text{better timing}",
        r"\not\Rightarrow",
    ):
        assert required in text
    bad = [ch for ch in text if ord(ch) < 32 and ch not in "\n\t"]
    assert bad == []


def test_phase_velocity_note_preserves_post_readout_boundary() -> None:
    text = NOTE.read_text(encoding="utf-8")
    assert "post-readout mechanistic interpretation" in text
    assert "not a preregistered prediction" in text
    assert "not a new PAYOFF confirmatory result" in text
    assert "unsupported positive interaction" in text
