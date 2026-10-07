import pytest

from scripts.evaluate_racing_information_absorption import audit_primary_invariants


def _rows():
    return [
        {"split":"train","race_id":"tr1","horse_id":"A","time_slice":"T-60","decimal_odds":"2","form_probability":"0.7","winner":"1"},
        {"split":"train","race_id":"tr1","horse_id":"B","time_slice":"T-60","decimal_odds":"2","form_probability":"0.3","winner":"0"},
        {"split":"train","race_id":"tr1","horse_id":"A","time_slice":"LAST","decimal_odds":"1.5","form_probability":"0.7","winner":"1"},
        {"split":"train","race_id":"tr1","horse_id":"B","time_slice":"LAST","decimal_odds":"3","form_probability":"0.3","winner":"0"},
        {"split":"test","race_id":"te1","horse_id":"A","time_slice":"T-60","decimal_odds":"2","form_probability":"0.6","winner":"1"},
        {"split":"test","race_id":"te1","horse_id":"B","time_slice":"T-60","decimal_odds":"2","form_probability":"0.4","winner":"0"},
        {"split":"test","race_id":"te1","horse_id":"A","time_slice":"LAST","decimal_odds":"1.7","form_probability":"0.6","winner":"1"},
        {"split":"test","race_id":"te1","horse_id":"B","time_slice":"LAST","decimal_odds":"2.5","form_probability":"0.4","winner":"0"},
    ]


def test_primary_invariant_audit_accepts_clean_complete_panel():
    out = audit_primary_invariants(_rows())
    assert out == {"train_races": 1, "test_races": 1, "time_slices": 2}


def test_primary_invariant_audit_rejects_form_drift():
    rows = _rows()
    rows[2] = dict(rows[2], form_probability="0.65")
    with pytest.raises(ValueError, match="form_probability changed"):
        audit_primary_invariants(rows)


def test_primary_invariant_audit_rejects_runner_set_change():
    rows = [r for r in _rows() if not (
        r["split"] == "train"
        and r["race_id"] == "tr1"
        and r["time_slice"] == "LAST"
        and r["horse_id"] == "B"
    )]
    with pytest.raises(ValueError, match="runner set changed"):
        audit_primary_invariants(rows)


def test_primary_invariant_audit_rejects_train_test_race_overlap():
    rows = _rows()
    rows[4] = dict(rows[4], race_id="tr1")
    rows[5] = dict(rows[5], race_id="tr1")
    rows[6] = dict(rows[6], race_id="tr1")
    rows[7] = dict(rows[7], race_id="tr1")
    with pytest.raises(ValueError, match="train/test race_id overlap"):
        audit_primary_invariants(rows)


def test_primary_invariant_audit_rejects_incomplete_time_panel():
    rows = [r for r in _rows() if not (
        r["split"] == "test" and r["time_slice"] == "LAST"
    )]
    with pytest.raises(ValueError, match="same time-slice set|incomplete time-slice"):
        audit_primary_invariants(rows)
