from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from build_payoff_b_v2_portal_sources import (
    INTERNAL_EDITOR_TOKENS,
    audit_portal_sources,
    build_cover_letter_source,
    build_main_portal_source,
    build_supporting_information_source,
    build_title_page_source,
    normalize_display_math,
)


RESULT = ROOT / "data" / "aikens2022_access_blocked_submission_state_20260928.json"


def test_display_math_normalizer_converts_legacy_bracket_markers():
    source = "[\na+b\n]\ntext\n"
    normalized = normalize_display_math(source)
    assert normalized == "\\[\na+b\n\\]\ntext\n"


def test_portal_main_source_is_final_facing_and_embeds_seven_figures():
    main = build_main_portal_source()

    assert main.startswith(
        "# Information deadlines can desynchronize seasonal interactions "
        "under environmental change"
    )
    assert sum(1 for line in main.splitlines() if line.strip() == "[") == 0
    assert sum(1 for line in main.splitlines() if line.strip() == "]") == 0
    assert main.count("![Figure ") == 7
    for number in range(1, 8):
        assert f"![Figure {number}]" in main
        assert "{width=6.2in}" in main

    assert "Dossman et al., 2023" in main
    assert "Raw waiting time" in main
    assert 'python -m pip install -e ".[test,empirical]"' in main
    assert "statsmodels>=0.14" in main

    for token in INTERNAL_EDITOR_TOKENS:
        assert token not in main

    for artifact in (
        "We therefore does",
        "We therefore distinguishes",
        "We therefore begins",
        "earlier this framework temporal-buffering",
        "transparent this framework witness",
        "new this framework discovery",
    ):
        assert artifact not in main


def test_portal_title_cover_and_si_have_correct_boundaries():
    title = build_title_page_source()
    cover = build_cover_letter_source(RESULT)
    si = build_supporting_information_source(RESULT)

    assert title.startswith("# Global Ecology and Biogeography - Title page")
    assert "[AUTHOR LIST" in title
    assert "[AFFILIATIONS" in title
    assert "## Author contributions" in title
    assert "## Data and code availability" in title

    assert cover.startswith("# Cover letter")
    assert "Information deadlines can desynchronize seasonal interactions" in cover
    assert "effective waiting cost" in cover

    for text in (title, cover):
        for token in INTERNAL_EDITOR_TOKENS:
            assert token not in text

    assert "PREOUTCOME" not in si
    assert "remains unopened" not in si
    assert "Registered analysis status: not executed because authenticated source access was unavailable." in si\n    assert "Registered result class: ACCESS_BLOCKED" not in si


def test_portal_source_audit_passes_current_access_blocked_route():
    main = build_main_portal_source()
    title = build_title_page_source()
    cover = build_cover_letter_source(RESULT)
    si = build_supporting_information_source(RESULT)
    audit = audit_portal_sources(
        main=main,
        title_page=title,
        cover_letter=cover,
        supporting_information=si,
    )

    assert audit["bare_display_math_markers"] == 0
    assert audit["embedded_figure_links"] == 7
    assert all(not hits for hits in audit["internal_editor_token_hits"].values())
    assert audit["main_has_final_title"] is True
    assert audit["title_page_has_placeholders"] is True
    assert audit["cover_letter_has_final_title"] is True
    assert audit["supporting_information_is_outcome_rendered"] is True
