from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "PAYOFF_B_INFORMATION_COORDINATION_V2_PREOUTCOME.md"
SI_SCRIPT = ROOT / "scripts" / "build_payoff_b_v2_geb_supporting_information.py"


def load_si_module():
    spec = importlib.util.spec_from_file_location("v2_si", SI_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_negative_reversal_gates_are_compact_in_main_text():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    start = text.index("### 3.4 Two preregistered natural reversal gates")
    end = text.index("### 3.5 Capacity remains a distinct failure mode", start)
    section = text[start:end]

    assert "NO\\_CUE\\_DRIVER\\_REVERSAL" in section
    assert "NO\\_CUE\\_RESOURCE\\_REVERSAL" in section
    assert "resident–migrant history test remained unopened" in section
    assert "Full breakpoint, slope and source-provenance diagnostics are retained in Supporting Information" in section

    # Failure geometry belongs in SI/receipts, not as a competing main result.
    assert "10.81" not in section
    assert "\\hat\\beta_{pre}" not in section
    assert "+0.228" not in section
    assert "+0.027" not in section


def test_hoge_veluwe_gate_b_diagnostics_are_retained_in_si():
    si = load_si_module().build_supporting_information()

    assert "Appendix S7. Same-system cue–resource reversal gate" in si
    assert "NO_CUE_RESOURCE_REVERSAL" in si
    assert "10.81" in si
    assert "break year 1999" in si
    assert "pre-break = 0.228" in si
    assert "post-break = 0.027" in si
    assert "remained NOT_RUN" in si
    assert "14cf9d5d249e582cf07079f3724b227a835acae95c297e3e8a1bac1bede5cc31" in si
    assert "9f113eb3f95d239ac31652c4083a159d82dacb61355b03fa2f355a2733a0b984" in si
