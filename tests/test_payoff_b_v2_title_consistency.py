from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TITLE = (
    "Effective information deadlines can desynchronize seasonal interactions "
    "under environmental change"
)

FILES = (
    ROOT / "manuscript" / "PAYOFF_B_INFORMATION_COORDINATION_V2_PREOUTCOME.md",
    ROOT / "submission" / "GEB_V2_TITLE_PAGE_TEMPLATE.md",
    ROOT / "submission" / "GEB_V2_DECLARATIONS_TEMPLATE.md",
    ROOT / "submission" / "GEB_V2_COVER_LETTER_PREOUTCOME.md",
    ROOT / "submission" / "GEB_V2_TITLE_PAGE_OUTCOME_TEMPLATE.md",
    ROOT / "submission" / "GEB_V2_TITLE_PAGE_ACCESS_BLOCKED_TEMPLATE.md",
    ROOT / "scripts" / "build_payoff_b_v2_geb_outcome_package.py",
)


def normalized(text: str) -> str:
    return " ".join(text.split())


def test_v2_title_is_consistent_across_submission_surfaces():
    for path in FILES:
        text = normalized(path.read_text(encoding="utf-8"))
        assert TITLE in text, path


def test_old_recovery_only_title_is_absent():
    old = (
        "Better information can fail to restore seasonal coordination "
        "under environmental change"
    )
    for path in FILES:
        text = normalized(path.read_text(encoding="utf-8"))
        assert old not in text, path
