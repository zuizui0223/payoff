import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "submission" / "PAYOFF_B_TRACKING_PARAMETER_TABLE.md"
MOVING = ROOT / "data" / "payoff_b_moving_landscape_receipt_20260920.json"
CONNECTIVITY = ROOT / "data" / "payoff_b_2d_connectivity_receipt_20260920.json"
FEEDBACK = ROOT / "data" / "payoff_b_movement_feedback_landscape_receipt_20260920.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_tracking_parameter_table_preserves_frontier_receipt():
    text = TABLE.read_text(encoding="utf-8")
    moving = load(MOVING)
    for row in moving["persistence_frontier"]["brackets"]:
        expected = (
            f"| {row['phenology_limit']} | "
            f"{row['max_persisted_velocity']:.3f} | "
            f"{row['first_failed_velocity']:.3f} |"
        )
        assert expected in text


def test_tracking_parameter_table_preserves_2d_gate_design():
    text = TABLE.read_text(encoding="utf-8")
    connectivity = load(CONNECTIVITY)
    fine = connectivity["coevolution"]["fine_mutation_step_0_1"]
    assert f"{fine['barriers']}/{fine['positive_interaction_cells']}" in text
    assert (
        f"{fine['persistence_rescues']}/{fine['positive_interaction_cells']}"
        in text
    )
    assert "0, 0.5, 1.0" in text
    assert "open, straight two-wall, zigzag two-wall" in text


def test_tracking_parameter_table_preserves_feedback_design():
    text = TABLE.read_text(encoding="utf-8")
    feedback = load(FEEDBACK)["design"]
    assert "0.02, 0.03, 0.04, 0.05, 0.06" in text
    assert "0, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6" in text
    assert "0, 0.25, 0.5" in text
    assert f"| baseline migration rate | {feedback['baseline_migration_rate']} |" in text
    assert f"| maximum migration rate | {feedback['max_migration_rate']} |" in text
    assert f"| total design cells | {feedback['cells']} |" in text


def test_tracking_parameter_table_keeps_empirical_boundary():
    text = TABLE.read_text(encoding="utf-8").lower()
    assert "none of the numeric design values below are empirical estimates" in text
    assert "not an empirical aikens estimate" in text
    assert "no later empirical phase-retention result" in text
