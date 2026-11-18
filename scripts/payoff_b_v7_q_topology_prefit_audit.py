"""Original-source-only q topology screen for frozen PAYOFF-B V7.

Never opens goose timing, computes geometry-only urgency U, fits q*U, or
uses synthetic stand-ins for missing source-year spring onsets or polygons.
The ordinal route stage used below is *not* V7's geographical U.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import mean

from scripts.payoff_b_v7_suppinfo_aggregate_gate import (
    QP,
    REGIONS,
    ROUTES,
    SOURCE_SHA,
    audit_pairs,
    readrows,
)

# Incoming ecological barriers explicitly classified in the source manuscript
# (Kölzsch et al. 2015, DOI 10.1111/1365-2656.12281, Stopover regions).
# This is published prior art, not a newly inferred environmental effect.
BARRIER_DESTINATIONS = frozenset({"SIC", "SGR", "SNO", "SVA", "WS"})


def pearson(x: list[float], y: list[float]) -> float | None:
    if len(x) < 3 or len(x) != len(y):
        return None
    mx, my = mean(x), mean(y)
    top = sum((a - mx) * (b - my) for a, b in zip(x, y))
    xx = sum((a - mx) ** 2 for a in x)
    yy = sum((b - my) ** 2 for b in y)
    return top / math.sqrt(xx * yy) if xx > 0 and yy > 0 else None


def rounded(v: float | None) -> float | None:
    return round(v, 9) if v is not None else None


def summarize(rows: list[dict]) -> dict:
    if not rows:
        raise ValueError("No consecutive transitions in source topology")
    q = [r["q"] for r in rows]
    stages = [r["ordinal_target_position"] for r in rows]
    by_flyway = {}
    for flyway in ROUTES:
        group = [r for r in rows if r["flyway"] == flyway]
        if not group:
            raise ValueError("Expected at least one source transition per flyway")
        qq = [r["q"] for r in group]
        by_flyway[flyway] = {
            "n_transitions": len(group),
            "mean_q": rounded(mean(qq)),
            "q_min": min(qq),
            "q_max": max(qq),
            "n_negative_q": sum(v < 0 for v in qq),
        }
    # Only an ordinal placement screen, not a substitute for geometry-only U.
    q_demeaned = [r["q"] - by_flyway[r["flyway"]]["mean_q"] for r in rows]
    stage_means = {
        f: mean(r["ordinal_target_position"] for r in rows if r["flyway"] == f)
        for f in ROUTES
    }
    rank_demeaned = [r["ordinal_target_position"] - stage_means[r["flyway"]]
                        for r in rows]
    at_barrier = [r["q"] for r in rows if r["is_published_ecological_barrier"]]
    no_barrier = [r["q"] for r in rows if not r["is_published_ecological_barrier"]]
    if not at_barrier or not no_barrier:
        raise ValueError("Barrier and non-barrier segments both required")
    return {
        "n_independent_candidate_transitions": len(rows),
        "n_flyways": len(by_flyway),
        "n_negative_signed_q": sum(v < 0 for v in q),
        "mean_signed_q": rounded(mean(q)),
        "pooled_pearson_q_vs_ordinal_stage": rounded(pearson(q, stages)),
        "flyway_centered_pearson_q_vs_ordinal_stage": rounded(
            pearson(q_demeaned, rank_demeaned)
        ),
        "published_barrier_n": len(at_barrier),
        "published_barrier_mean_q": rounded(mean(at_barrier)),
        "published_nonbarrier_n": len(no_barrier),
        "published_nonbarrier_mean_q": rounded(mean(no_barrier)),
        "barrier_minus_nonbarrier_mean_q": rounded(mean(at_barrier) - mean(no_barrier)),
        "by_flyway": by_flyway,
        "unit": "historical published regional transition, never GPS fix",
        "ordinal_stage_is_registered_geometry_urgency_U": False,
        "significance_test_or_biological_effect_fitted": False,
    }


def audit(q_rows: list[dict] | None = None,
          region_rows: list[dict] | None = None) -> dict:
    q_rows = readrows(QP) if q_rows is None else q_rows
    region_rows = readrows(REGIONS) if region_rows is None else region_rows
    source = audit_pairs(q_rows, region_rows)
    consecutive = [r for r in q_rows if r["consecutive"] == "1"]
    if len(consecutive) != 13 or source["consecutive_unambiguous_S1_candidate_names"] != 11:
        raise ValueError("Original consecutive route topology changed")
    derived = []
    for r in consecutive:
        flyway, source_code, target_code = (r["flyway"], r["source_code"],
                                             r["target_code"])
        route = ROUTES[flyway]
        pos = route.index(target_code)
        if pos == 0 or pos != route.index(source_code) + 1 or len(route) < 3:
            raise ValueError("Not an original forward consecutive transition")
        derived.append({
            "flyway": flyway,
            "source_code": source_code,
            "target_code": target_code,
            "q": float(r["q_30year_correlation"]),
            "ordinal_target_position": (pos - 1) / (len(route) - 2),
            "is_published_ecological_barrier": target_code in BARRIER_DESTINATIONS,
            "source_S1_alias_without_unresolved_code": (
                r["source_alias_status"] == "exact" and
                r["target_alias_status"] == "exact"
            ),
        })
    exact = [r for r in derived if r["source_S1_alias_without_unresolved_code"]]
    if len(exact) != 11:
        raise ValueError("Expected 11 source-label-unambiguous adjacent q candidates")
    out = {
        "status": "SOURCE_ONLY_ORDINAL_TOPOLOGY_SCREEN_COMPLETE_V7_HOLD",
        "as_of": "2026-11-18",
        "source_original_DOCX_sha256": SOURCE_SHA,
        "original_source_30year_q_n": source["original_30year_pairwise_q"],
        "all_adjacent_published_q": summarize(derived),
        "without_two_unresolved_source_label_aliases": summarize(exact),
        "published_barrier_destination_codes": sorted(BARRIER_DESTINATIONS),
        "prior_art": "Kölzsch et al. 2015, J Anim Ecol, DOI 10.1111/1365-2656.12281",
        "frozen_contract": "docs/PAYOFF_B_V7_PREDICTABILITY_URGENCY_CONTRACT_20261005.md",
        "q_stage_screen_only_not_geographic_urgency": True,
        "no_statistical_inference_on_13_or_11_dependent_route_transitions": True,
        "not_independent_animal_level_replication": True,
        "original_GPS_region_geometry_available": False,
        "source_region_year_specific_S_jy_available": False,
        "q_by_U_and_bird_response_fitted": False,
        "V7_REGISTERED_PRIMARY_GATE": "HOLD_NOT_ESTIMABLE",
        "further_admission": [
            "Original 1982-2011 region-year spring onset S_jy with source region mapping",
            "Authoritative 16-region GPS membership or pre-outcome agreed original reconstruction",
            "Geometry-only U independent of observed stopover timing or duration",
            "Original 40 complete spring migrations and at least 30 actual stops, >=2 flyways",
            "At least 3 independent route positions; absolute corr(q,U) < 0.90",
        ],
    }
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
