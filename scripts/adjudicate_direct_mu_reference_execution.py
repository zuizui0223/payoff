from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.direct_mu_single_reference_execution import (
    ClosedBand,
    DirectMuReferenceExecutionReceipt,
    adjudicate_reference_execution,
)


RECEIPT_ID = "STREPTOMYCES_M5_FIRST_REFERENCE_EXECUTION_V1"


def _num(value: object, name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be numeric")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be numeric") from exc


def _band(data: dict, name: str) -> ClosedBand:
    if not isinstance(data, dict):
        raise ValueError(f"{name} must be an object")
    return ClosedBand(
        _num(data.get("lower"), f"{name}.lower"),
        _num(data.get("upper"), f"{name}.upper"),
    )


def load_receipt(data: dict) -> DirectMuReferenceExecutionReceipt:
    if data.get("receipt_id") != RECEIPT_ID:
        raise ValueError(f"receipt_id must be {RECEIPT_ID}")
    if data.get("reference_id") != "M5_T0":
        raise ValueError("this v1 execution packet is frozen to M5_T0")
    if data.get("deletion_class") == "NOT_YET_VERIFIED":
        raise ValueError("M5 deletion_class must be verified before adjudication")

    return DirectMuReferenceExecutionReceipt(
        reference_id=data["reference_id"],
        deletion_class=data["deletion_class"],
        origin_cluster_id=data["origin_cluster_id"],
        support_reference=data["support_reference"],
        physical_stock_access_confirmed=bool(data["physical_stock_access_confirmed"]),
        marker_pattern_verified=bool(data["marker_pattern_verified"]),
        core_reference_present=bool(data["core_reference_present"]),
        pre_existing_at_72h=bool(data["pre_existing_at_72h"]),
        same_medium_and_context=bool(data["same_medium_and_context"]),
        independently_derived_from_direct_mu_candidate_outcome=bool(
            data["independently_derived_from_direct_mu_candidate_outcome"]
        ),
        candidate_outcomes_used_for_selection=bool(data["candidate_outcomes_used_for_selection"]),
        viable_at_72h=bool(data["viable_at_72h"]),
        measurable_at_120h=bool(data["measurable_at_120h"]),
        gross_secondary_rearrangement_unresolved=bool(
            data["gross_secondary_rearrangement_unresolved"]
        ),
        measurement_unit=data["measurement_unit"],
        interval_start_h=_num(data["interval_start_h"], "interval_start_h"),
        interval_end_h=_num(data["interval_end_h"], "interval_end_h"),
        context_id=data["context_id"],
        intact_comparator_id=data["intact_comparator_id"],
        d_mass_72h=_band(data["d_mass_72h"], "d_mass_72h"),
        d_mass_120h=_band(data["d_mass_120h"], "d_mass_120h"),
    )


def to_json(result) -> dict:
    band = result.d_realization_band
    return {
        "receipt_id": RECEIPT_ID,
        "reference_id": result.reference_id,
        "deletion_class": result.deletion_class,
        "origin_cluster_id": result.origin_cluster_id,
        "derived_d_realization_band": None
        if band is None
        else {"lower": band.lower, "upper": band.upper},
        "quantitative_receipt_valid": result.quantitative_receipt_valid,
        "semantic_qualification_passed": result.semantic_qualification.qualified,
        "qualified_reference": result.qualified_reference,
        "blockers": list(result.blockers),
        "claim_ceiling": result.claim_ceiling,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Adjudicate the frozen M5_T0 direct-mu realization reference packet"
    )
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    data = json.loads(args.receipt.read_text(encoding="utf-8"))
    result = adjudicate_reference_execution(load_receipt(data))
    payload = json.dumps(to_json(result), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
