from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTEGRATED = ROOT / "manuscript" / "PAYOFF_B_INTEGRATED_TRACKING_ECOLOGY_V1_PREOUTCOME.md"
ARCH = ROOT / "docs" / "PAYOFF_B_TWO_PAPER_PUBLICATION_ARCHITECTURE_20260925.md"
THEOREM = ROOT / "manuscript" / "PAYOFF_B_THEORETICAL_ECOLOGY_BRIEF_V1.md"
TRACKING_SOURCE = ROOT / "manuscript" / "PAYOFF_B_TRACKING_THEORY_V1.md"
GEB_SOURCE = ROOT / "manuscript" / "PAYOFF_B_MOVEMENT_PHENOLOGY_GEB_V3_PREOUTCOME.md"
BROAD = ROOT / "data" / "payoff_b_broad_bird_stage1_result_20260925.json"
HOLDOUT = ROOT / "data" / "payoff_b_temporal_buffering_bird_holdout_result_20260925.json"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_two_paper_architecture_keeps_exact_theorem_independent() -> None:
    m = text(INTEGRATED)
    a = text(ARCH)
    assert THEOREM.exists()
    assert "exact anti-phase optimum theorem remains a separate PAYOFF-B1 paper" in m
    assert "Paper 1 — exact benchmark" in a


def test_integrated_manuscript_retains_primary_broad_falsification() -> None:
    m = text(INTEGRATED)
    assert "5,816 observations from 55 migratory bird species" in m
    assert "portable movement-speed/environmental-wave-speed optimum" in m
    assert "is not supported" in m
    assert "The primary macroecological result is therefore a falsification" in m


def test_integrated_manuscript_keeps_aikens_outcome_unopened() -> None:
    m = text(INTEGRATED)
    assert "Aikens industrial-development lambda outcome remains unopened" in m
    assert "[AIKENS LAMBDA ABSTRACT PENDING" in m
    assert "[AIKENS LAMBDA RESULT PENDING" in m
    assert "[AIKENS LAMBDA DISCUSSION PENDING" in m
    assert "[AIKENS LAMBDA CONCLUSION PENDING" in m


def test_integration_promotes_temporal_buffering_not_universal_lambda() -> None:
    m = text(INTEGRATED)
    assert "temporal adjustment can buffer spatial tracking demand" in m
    assert "it cannot replace movement indefinitely under sustained environmental change" in m
    assert "latent spatial tracking demand" in m
    assert "mismatch is an outcome" in m.lower()
    assert "It does not support:" in m
    assert "a universal lambda or universal actuator" in m


def test_original_source_manuscripts_remain_available() -> None:
    assert TRACKING_SOURCE.exists()
    assert GEB_SOURCE.exists()


def test_integrated_manuscript_has_single_aikens_marker_pairs() -> None:
    m = text(INTEGRATED)
    for name in ("ABSTRACT", "RESULTS", "DISCUSSION", "CONCLUSION"):
        assert m.count(f"<!-- AIKENS_LAMBDA_{name}_START -->") == 1
        assert m.count(f"<!-- AIKENS_LAMBDA_{name}_END -->") == 1


def test_integrated_manuscript_keeps_compact_six_figure_architecture() -> None:
    import re

    m = text(INTEGRATED)
    figure_block = m.split("## Figure architecture", 1)[1].split("## Claim ceiling", 1)[0]
    figures = re.findall(r"^\*\*Figure\s+(\d+)\s+—", figure_block, flags=re.M)
    assert figures == ["1", "2", "3", "4", "5", "6"]


def test_integrated_manuscript_has_reference_spine() -> None:
    m = text(INTEGRATED)
    refs = m.split("## References", 1)[1].split("## Figure architecture", 1)[0]
    reference_lines = [line for line in refs.splitlines() if line.startswith("- ")]
    assert len(reference_lines) >= 15
    for required in (
        "Weir JC, Phillimore AB (2024)",
        "Amaral BR, Youngflesh C, Tingley M, Miller DAW (2025)",
        "Ortega AC, Aikens EO, Merkle JA, Monteith KL, Kauffman MJ (2023)",
        "van Toor ML et al. (2021)",
        "Aikens EO, Wyckoff TB, Sawyer H, Kauffman MJ (2022)",
    ):
        assert required in refs


def test_integrated_abstract_stays_short_preoutcome() -> None:
    import re

    m = text(INTEGRATED)
    abstract = m.split("## Abstract", 1)[1].split("**Keywords:**", 1)[0]
    abstract = re.sub(r"<!--.*?-->", " ", abstract, flags=re.S)
    abstract = re.sub(r"\[AIKENS LAMBDA ABSTRACT PENDING.*?\]", " ", abstract, flags=re.S)
    words = re.findall(r"\b[\w’'-]+\b", abstract, flags=re.UNICODE)
    assert len(words) <= 300


def test_integrated_broad_bird_claims_are_bound_to_machine_receipt() -> None:
    import json

    payload = json.loads(BROAD.read_text(encoding="utf-8"))
    assert payload["sample"]["n_rows"] == 5816
    assert payload["sample"]["n_species"] == 55
    minima = {(x["response"], round(float(x["alignment_ref"]), 6)): x for x in payload["gam_minima"]}
    assert abs(minima[("raw_abs_lag", 0.948293)]["u_star"] - 0.405133727255802) < 1e-12
    assert abs(minima[("centered_abs_lag", 0.948374)]["u_star"] - 1.04272442046421) < 1e-12
    assert abs(minima[("centered_abs_lag", 1.0)]["u_star"] - 1.39660423067479) < 1e-12
    assert payload["species_heterogeneity"]["n_vertices_inside_5_95"] == 11
    assert payload["source_analysis"]["workflow_run_id"] == 35328297725
    assert payload["source_analysis"]["workflow_artifact_id"] == 10540282539


def test_integrated_manuscript_retains_failed_temporal_substitution_test() -> None:
    import json

    m = text(INTEGRATED)
    x = json.loads(HOLDOUT.read_text(encoding="utf-8"))
    assert x["scientific_status"] == "FAIL_WRONG_DIRECTION"
    assert x["retuning_permitted"] is False
    assert "+0.0351 ± 0.0289" in m
    assert "opposite to the predicted negative direction" in m
    assert "not the registered primary test" in m
    assert "post-readout mechanistic interpretation" in m
    assert "phase intercept" in m
    assert "mismatch drifts" in m
