from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "theory" / "PHASE_VELOCITY_TEMPORAL_BUFFERING.md"


def mismatch(e0: float, v_e: float, v_a: float, t: float, z: float) -> float:
    return e0 - v_a * z + (v_e - v_a) * t


def test_static_timing_shift_changes_phase_not_drift() -> None:
    e0, ve, va = 3.0, 5.0, 4.0
    z1, z2 = 0.0, 2.0
    d1 = mismatch(e0, ve, va, 11, z1) - mismatch(e0, ve, va, 10, z1)
    d2 = mismatch(e0, ve, va, 11, z2) - mismatch(e0, ve, va, 10, z2)
    assert abs(d1 - (ve - va)) < 1e-12
    assert abs(d2 - (ve - va)) < 1e-12
    assert abs(
        (mismatch(e0, ve, va, 10, z2) - mismatch(e0, ve, va, 10, z1))
        + va * (z2 - z1)
    ) < 1e-12


def test_dynamic_timing_can_transiently_cancel_velocity_mismatch() -> None:
    e0, ve, va = 2.0, 5.0, 4.0
    zdot = (ve - va) / va
    for t in (0.0, 1.0, 5.0, 10.0):
        assert abs(mismatch(e0, ve, va, t, zdot * t) - e0) < 1e-12


def test_buffer_time_formula_follows_capacity_limit() -> None:
    ve, va, zmax = 5.0, 4.0, 3.0
    zdot = (ve - va) / va
    expected = zmax / abs(zdot)
    u = va / ve
    nondim = u * zmax / abs(1 - u)
    assert abs(expected - 12.0) < 1e-12
    assert abs(expected - nondim) < 1e-12
    assert abs(zdot * expected - zmax) < 1e-12


def test_gain_and_capacity_are_distinct_quantities() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "responsiveness is not capacity" in text
    assert "timing gain" in text
    assert "timing capacity" in text
    assert "remaining timing range" in text


def test_note_labels_identity_as_post_readout_interpretation() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "post-readout mechanistic interpretation" in text
    assert "elementary kinematics, not a claim of mathematical novelty" in text
    assert "not a preregistered prediction" in text
