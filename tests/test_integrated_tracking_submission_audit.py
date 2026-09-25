from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_integrated_tracking_manuscript.py"

spec = importlib.util.spec_from_file_location("integrated_audit", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_integrated_manuscript_passes_all_preoutcome_submission_gates() -> None:
    result = module.audit()
    assert result["all_preoutcome_hard_gates_pass"] is True
    assert all(result["hard_preoutcome_gates"].values())


def test_integrated_manuscript_final_submission_block_is_only_aikens() -> None:
    result = module.audit()
    assert result["final_submission_ready"] is False
    assert result["final_submission_blockers"] == [
        "registered Aikens fixed-24h lambda outcome remains unopened"
    ]
    assert result["claim_state"]["aikens_lambda_outcome_opened"] is False


def test_integrated_manuscript_reference_and_figure_contract() -> None:
    result = module.audit()
    assert result["metrics"]["reference_count"] >= 15
    assert result["uncited_references"] == []
    assert result["metrics"]["main_figure_count"] == 6
