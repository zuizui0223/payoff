from pathlib import Path
import math

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "theory" / "PHASE_VELOCITY_TEMPORAL_BUFFERING.md"


def mismatch(e0: float, v_e: float, v_a: float, t: float, z: float) -> float:
    return e0 - v_a * z + (v_e - v_a) * t


def test_timing_changes_intercept_not_mismatch_drift() -> None:
    e0, ve, va = 3.0, 5.0, 4.0
    z1, z2 = 0.0, 2.0
    # Same drift across time for different timing shifts.
    d1 = mismatch(e0, ve, va, 11, z1) - mismatch(e0, ve, va, 10, z1)
    d2 = mismatch(e0, ve, va, 11, z2) - mismatch(e0, ve, va, 10, z2)
    assert abs(d1 - (ve - va)) < 1e-12
    assert abs(d2 - (ve - va)) < 1e-12
    # Timing shifts only the intercept by -v_a * delta_z.
    assert abs(
        (mismatch(e0, ve, va, 10, z2) - mismatch(e0, ve, va, 10, z1))
        + va * (z2 - z1)
    ) < 1e-12


def test_buffer_time_formula() -> None:
    ve, va, zmax = 5.0, 4.0, 3.0
    expected = va * zmax / abs(ve - va)
    u = va / ve
    nondim = u * zmax / abs(1 - u)
    assert abs(expected - 12.0) < 1e-12
    assert abs(expected - nondim) < 1e-12


def test_persistent_zero_mismatch_requires_speed_matching() -> None:
    e0, ve, va = 0.0, 5.0, 4.0
    # choose z to zero mismatch at t=10
    z = (e0 + (ve - va) * 10) / va
    assert abs(mismatch(e0, ve, va, 10, z)) < 1e-12
    assert abs(mismatch(e0, ve, va, 11, z)) > 1e-9


def test_note_labels_identity_as_post_readout_interpretation() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "post-readout mechanistic interpretation" in text
    assert "elementary kinematics, not a claim of mathematical novelty" in text
    assert "better timing" in text
    assert "weaker speed dependence" in text
    assert "not a preregistered prediction" in text
