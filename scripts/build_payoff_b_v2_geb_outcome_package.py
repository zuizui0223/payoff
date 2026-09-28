#!/usr/bin/env python3
"""Build deterministic outcome-rendered GEB package for canonical PAYOFF-B V2.

The registered industrial-development phase-retention result is rendered into
Supporting Information only. The blinded main text and seven main figures are
identical across all licensed result classes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from audit_payoff_b_v2_geb_source import audit as audit_main
from build_payoff_b_v2_geb_source import build_source
from build_payoff_b_v2_geb_outcome_supporting_information import (
    build_supporting_information,
)
from build_payoff_b_v2_geb_preoutcome_package import deterministic_zip
from render_aikens_lambda_manuscript import classify_result
from render_information_deadlines_figures import render_all

ROOT = Path(__file__).resolve().parents[1]

STATIC_FILES = (
    "submission/GEB_V2_TITLE_PAGE_OUTCOME_TEMPLATE.md",
    "submission/GEB_V2_DATA_CODE_OUTCOME.md",
    "submission/GEB_V2_PORTAL_HANDOFF_OUTCOME.md",
    "submission/GEB_V2_DECLARATIONS_TEMPLATE.md",
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _copy(rel: str, output_dir: Path) -> dict:
    source = ROOT / rel
    target = output_dir / source.name
    shutil.copy2(source, target)
    return {
        "path": target.name,
        "source": rel,
        "bytes": target.stat().st_size,
        "sha256": sha256(target),
    }


def outcome_cover_letter(result_json: Path) -> str:
    payload = json.loads(result_json.read_text(encoding="utf-8"))
    result_class = classify_result(payload)
    summaries = {
        "PASS": (
            "The registered within-taxon industrial-development test supported "
            "greater retention of incoming phase error under the large-development "
            "forcing regime."
        ),
        "FAIL_WRONG_DIRECTION": (
            "The registered within-taxon industrial-development prediction failed "
            "in direction, separating the independently observed actuator contrast "
            "from the phase-retention response."
        ),
        "FAIL_INSUFFICIENT_SUPPORT": (
            "The registered within-taxon industrial-development contrast pointed "
            "in the predicted direction but did not pass its frozen inferential "
            "support criterion."
        ),
        "NOT_ESTIMABLE": (
            "The registered within-taxon industrial-development contrast was not "
            "estimable under the frozen reconstruction and support criteria, and "
            "no retuning was performed."
        ),
        "ACCESS_BLOCKED": (
            "The registered within-taxon industrial-development contrast was not "
            "executed because the frozen environmental reconstruction required "
            "authenticated source access that was unavailable; no substitute "
            "analysis was used."
        ),
    }

    return f"""# Global Ecology and Biogeography — V2 cover-letter template

Dear Editors,

Please consider our Research Article, **“Better information can fail to restore
seasonal coordination under environmental change,”** for *Global Ecology and
Biogeography*.

Species tracking seasonal environments are usually evaluated by how accurately
they match changing conditions. We ask a different question: when does useful
environmental information actually become behaviourally usable by interacting
organisms?

We derive an exact information-deadline result showing that cue quality and cue
use are distinct ecological state variables. Interactors facing the same
improving cue but different costs of delaying action begin using that cue at
different thresholds, creating a finite range in which better information
increases rather than decreases phenological mismatch. We then show that under
perfect environmental information, an obsolete uninformed timing convention and
a better informed convention can both be strict equilibria. Temporary
information degradation can therefore leave a system in a lower-payoff timing
state even after cue quality fully recovers.

Natural analyses deliberately test separate links rather than claiming a
complete observed hysteresis event. The broad migratory-bird analysis provides
pooled, dependence-sensitive support for predictive connectivity; the
pied-flycatcher manipulation anchors timing-dependent cue availability; the
registered wigeon analysis does not support a universal effect of predictive
connectivity on post-error correction; and a preregistered Hoge Veluwe
cue–resource recovery gate failed before resident–migrant history was opened.

Registered Supplementary test: **{result_class}**. {summaries[result_class]}
This registered result does not alter the manuscript's title, abstract,
information-deadline theorem, perfect-information recovery-failure result or
main figures.

The theory predicts that **environmental information can recover before
ecological coordination does**.

[AUTHOR-CONFIRMED statement that the work is original, approved by all authors,
and not under consideration elsewhere.]

Potential reviewers / handling editors: [AUTHOR-CONTROLLED, CONFLICT-CHECKED].

Sincerely,

[CORRESPONDING AUTHOR — AUTHOR CONTROLLED]
"""


def audit_outcome(
    *,
    main_text: str,
    si_text: str,
    claim_state: dict,
    result_class: str,
    figure_manifest: dict,
) -> dict:
    main_audit = audit_main(main_text)

    si_forbidden = (
        "remains unopened",
        "Registered industrial-development supplement — pending",
        "PREOUTCOME",
    )
    si_hits = [token for token in si_forbidden if token in si_text]

    main_invariants = {
        "main_hard_gates_pass": main_audit["all_preoutcome_hard_gates_pass"],
        "main_has_no_result_class": result_class not in main_text,
        "main_has_no_pending_aikens": (
            "AIKENS_LAMBDA" not in main_text
            and "Aikens lambda result pending" not in main_text
        ),
        "si_has_result_class": result_class in si_text,
        "si_has_no_preoutcome_language": not si_hits,
        "claim_state_matches_result": (
            claim_state.get("scientific_result") == result_class
        ),
        "retuning_forbidden": claim_state.get("retuning_permitted") is False,
        "main_text_changed_false": (
            claim_state.get("canonical_main_text_changed") is False
        ),
        "main_figures_changed_false": (
            claim_state.get("main_figures_changed") is False
        ),
        "seven_main_figures": len(figure_manifest.get("figures", {})) == 7,
        "figures_do_not_use_aikens": (
            figure_manifest.get("aikens_outcome_used") is False
        ),
    }

    return {
        "status": "PASS" if all(main_invariants.values()) else "FAIL",
        "scientific_result": result_class,
        "main_metrics": main_audit["metrics"],
        "gates": main_invariants,
        "si_preoutcome_hits": si_hits,
        "all_outcome_hard_gates_pass": all(main_invariants.values()),
    }


def build(
    result_json: Path,
    output_dir: Path,
    zip_path: Path | None = None,
) -> dict:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    payload = json.loads(result_json.read_text(encoding="utf-8"))
    result_class = classify_result(payload)

    main = output_dir / "GEB_V2_BLINDED_OUTCOME.md"
    main.write_text(build_source(), encoding="utf-8")

    si_text, claim_state = build_supporting_information(result_json)
    si = output_dir / "GEB_V2_SUPPORTING_INFORMATION_OUTCOME.md"
    si.write_text(si_text, encoding="utf-8")

    claim_path = output_dir / "GEB_V2_AIKENS_CLAIM_STATE.json"
    claim_path.write_text(
        json.dumps(claim_state, indent=2) + "\n",
        encoding="utf-8",
    )

    cover = output_dir / "GEB_V2_COVER_LETTER_OUTCOME.md"
    cover.write_text(outcome_cover_letter(result_json), encoding="utf-8")

    figures_dir = output_dir / "figures"
    rendered = render_all(figures_dir)
    fig_manifest = json.loads(
        rendered["manifest"].read_text(encoding="utf-8")
    )

    audit_result = audit_outcome(
        main_text=main.read_text(encoding="utf-8"),
        si_text=si_text,
        claim_state=claim_state,
        result_class=result_class,
        figure_manifest=fig_manifest,
    )
    if not audit_result["all_outcome_hard_gates_pass"]:
        raise ValueError(
            "V2 GEB outcome package failed hard gates: "
            + json.dumps(audit_result["gates"], sort_keys=True)
        )

    audit_path = output_dir / "GEB_V2_OUTCOME_AUDIT.json"
    audit_path.write_text(
        json.dumps(audit_result, indent=2) + "\n",
        encoding="utf-8",
    )

    files = []
    for path, source in (
        (main, "generated:canonical V2 blinded main text"),
        (si, "generated:V2 outcome-rendered Supporting Information"),
        (claim_path, "generated:registered result claim state"),
        (cover, "generated:V2 outcome cover letter"),
        (audit_path, "generated:V2 outcome audit"),
    ):
        files.append(
            {
                "path": path.name,
                "source": source,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )

    for rel in STATIC_FILES:
        files.append(_copy(rel, output_dir))

    for index in range(1, 8):
        path = rendered[f"figure_{index}"]
        files.append(
            {
                "path": path.relative_to(output_dir).as_posix(),
                "source": f"generated:V2 figure {index}",
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    files.append(
        {
            "path": rendered["manifest"].relative_to(output_dir).as_posix(),
            "source": "generated:V2 figure manifest",
            "bytes": rendered["manifest"].stat().st_size,
            "sha256": sha256(rendered["manifest"]),
        }
    )

    manifest = {
        "status": "payoff_b_v2_geb_outcome_package",
        "journal": "Global Ecology and Biogeography",
        "article_type": "Research Article",
        "canonical_source": (
            "manuscript/PAYOFF_B_INFORMATION_COORDINATION_V2_PREOUTCOME.md"
        ),
        "scientific_state": (
            "OUTCOME_RENDERED_ACCESS_BLOCKED"
            if result_class == "ACCESS_BLOCKED"
            else "OUTCOME_RENDERED_SCIENCE_READY"
        ),
        "scientific_result": result_class,
        "v1_status": "FROZEN_PROVENANCE_ONLY",
        "registered_result_frozen": True,
        "phase_retention_estimate_available": bool(
            claim_state.get("estimable", False)
        ),
        "aikens_outcome_opened": bool(
            claim_state.get("estimable", False)
        ),
        "aikens_result_location": "Supporting Information only",
        "main_text_retuned": False,
        "main_figures_retuned": False,
        "final_science_blocker": (
            "author decision required: submit with registered Aikens ACCESS_BLOCKED "
            "state or wait for authenticated execution"
            if result_class == "ACCESS_BLOCKED"
            else None
        ),
        "final_submission_eligible": False,
        "remaining_portal_blockers": (
            [
                "author decision on registered Aikens ACCESS_BLOCKED state",
                "anonymous reviewer archive delivery channel",
                "author-controlled title-page and declaration metadata",
                "final human review of generated package and portal metadata",
            ]
            if result_class == "ACCESS_BLOCKED"
            else [
                "anonymous reviewer archive delivery channel",
                "author-controlled title-page and declaration metadata",
                "final human review of generated package and portal metadata",
            ]
        ),
        "structured_abstract_words": audit_result["main_metrics"]["abstract_words"],
        "main_body_words": audit_result["main_metrics"]["main_body_words"],
        "references": audit_result["main_metrics"]["reference_count"],
        "display_pieces": audit_result["main_metrics"]["figure_legend_count"],
        "keywords": audit_result["main_metrics"]["keyword_count"],
        "figure_count": 7,
        "file_count": len(files),
        "files": files,
    }

    manifest_path = output_dir / "GEB_V2_OUTCOME_PACKAGE_MANIFEST.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    if zip_path is not None:
        deterministic_zip(output_dir, zip_path)
        manifest["zip_path"] = str(zip_path)
        manifest["zip_bytes"] = zip_path.stat().st_size
        manifest["zip_sha256"] = sha256(zip_path)

    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result-json", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--zip", type=Path, required=True)
    args = parser.parse_args()

    manifest = build(args.result_json, args.output_dir, args.zip)
    print(
        "PAYOFF_B_V2_GEB_OUTCOME_PACKAGE "
        f"result={manifest['scientific_result']} "
        f"main_words={manifest['main_body_words']} "
        f"abstract={manifest['structured_abstract_words']} "
        f"references={manifest['references']} "
        f"figures={manifest['figure_count']} "
        f"zip_sha256={manifest.get('zip_sha256')}"
    )


if __name__ == "__main__":
    main()
