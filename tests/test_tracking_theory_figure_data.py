import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from build_tracking_theory_figure_data import build_figure_data


CLAIM_FREEZE = ROOT / "data" / "payoff_b_tracking_theory_claim_freeze_20260924.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_tracking_theory_figure_data_uses_only_frozen_synthetic_receipts():
    payload = build_figure_data()
    assert payload["frozen_date"] == "2026-09-20"
    assert len(payload["source_receipts"]) == 5
    assert all("20260920" in path for path in payload["source_receipts"])
    assert all("wigeon" not in path for path in payload["source_receipts"])
    assert all("aikens" not in path.lower() for path in payload["source_receipts"])


def test_tracking_theory_figure_data_matches_claim_freeze():
    payload = build_figure_data()
    freeze = load(CLAIM_FREEZE)["licensed_quantitative_results"]

    frontier = payload["figure_2_temporal_bypass"]["one_dimensional_frontier"]
    assert frontier[0]["max_persisted_velocity"] == freeze[
        "one_dimensional_persistence_frontier"
    ]["phenology_limit_0"]["max_persisted_velocity"]
    assert frontier[-1]["max_persisted_velocity"] == freeze[
        "one_dimensional_persistence_frontier"
    ]["phenology_limit_5"]["max_persisted_velocity"]

    gate = payload["figure_3_coordination_gate"]
    frozen_gate = freeze["two_dimensional_coordination"]
    assert gate["positive_interaction_cells"] == frozen_gate[
        "fine_positive_interaction_cells"
    ]
    assert gate["barriers"] == frozen_gate["barriers"]
    assert gate["persistence_rescues"] == frozen_gate["persistence_rescues"]
    assert gate["direct_gate"]["coordinated_gain"] == frozen_gate[
        "direct_gate"
    ]["coordinated_gain"]
    assert gate["direct_gate"]["unilateral_gain_a"] == frozen_gate[
        "direct_gate"
    ]["unilateral_gain_a"]


def test_tracking_theory_figure_data_preserves_negative_replication_result():
    payload = build_figure_data()
    demography = payload["figure_5_demography_and_drift"]
    assert demography["pilot_ge_0_10"] == 9
    assert demography["replication_ge_0_10"] == 0
    assert demography["replication_128"]["max_persistence_gain"] == 0.09375


def test_tracking_theory_figure_data_preserves_drift_crossing_not_rescue():
    payload = build_figure_data()
    rows = {
        row["N"]: row for row in payload["figure_5_demography_and_drift"][
            "drift_beta_5"
        ]
    }
    assert rows[10]["escape_fraction"] == 0.9375
    assert rows[30]["escape_fraction"] == 0.96875
    assert rows[100]["escape_fraction"] == 0
    assert (
        payload["figure_5_demography_and_drift"][
            "drift_retained_interpretation"
        ]
        == "drift_assisted_barrier_crossing_not_drift_rescue"
    )


def test_tracking_theory_figure_data_preserves_high_forcing_complementarity():
    payload = build_figure_data()
    high = payload["figure_6_local_null_vs_landscape"][
        "high_forcing_persistence"
    ]
    assert high["v_0_05"]["h_0"] == "0/7 controller gains persist"
    assert high["v_0_05"]["h_0_25"] == "7/7 persist"
    assert high["v_0_06"]["h_0"] == "0/7 controller gains persist"
    assert high["v_0_06"]["h_0_5"] == "7/7 persist"
