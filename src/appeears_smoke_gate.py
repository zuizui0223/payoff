"""Operational go/no-go gate for a live AppEEARS V061 smoke task.

This gate is intentionally structural. It does not tune a quality threshold
after seeing the data and does not claim that one task is sufficient for IRG
reconstruction.

GO requires only that the downloaded AppEEARS product pair can be converted
into at least one usable, quality-good, snow-free pixel-year record. Seasonal
composite sufficiency remains the responsibility of the downstream IRG fitter.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AppEEARSSmokeGate:
    passed: bool
    matched_rows: int
    output_rows: int
    pixel_years: int
    quality_good_rows: int
    snow_free_rows: int
    unknown_snow_rows: int
    invalid_reflectance_rows: int
    reasons: tuple[str, ...]


def evaluate_appeears_smoke_gate(
    receipt: dict,
) -> AppEEARSSmokeGate:
    """Evaluate structural usability of a V061 task conversion receipt."""

    if receipt.get("status") != "appeears_v061_irg_input_ready":
        return AppEEARSSmokeGate(
            passed=False,
            matched_rows=0,
            output_rows=0,
            pixel_years=0,
            quality_good_rows=0,
            snow_free_rows=0,
            unknown_snow_rows=0,
            invalid_reflectance_rows=0,
            reasons=("IRG_INPUT_RECEIPT_NOT_READY",),
        )

    conversion = receipt.get("conversion") or {}
    matched_rows = int(conversion.get("matched_rows", 0))
    output_rows = int(conversion.get("output_rows", 0))
    unknown_snow_rows = int(
        conversion.get("unknown_snow_rows", 0)
    )
    invalid_reflectance_rows = int(
        conversion.get("invalid_reflectance_rows", 0)
    )
    pixel_years = int(receipt.get("pixel_years", 0))
    quality_good_rows = int(
        receipt.get("quality_good_rows", 0)
    )
    snow_free_rows = int(
        receipt.get("snow_free_rows", 0)
    )

    reasons: list[str] = []
    if matched_rows <= 0:
        reasons.append("NO_EXACT_MOD09_MOD10_MATCHES")
    if output_rows <= 0:
        reasons.append("NO_USABLE_IRG_INPUT_ROWS")
    if pixel_years <= 0:
        reasons.append("NO_PIXEL_YEARS")
    if quality_good_rows <= 0:
        reasons.append("NO_QUALITY_GOOD_ROWS")
    if snow_free_rows <= 0:
        reasons.append("NO_SNOW_FREE_ROWS")

    return AppEEARSSmokeGate(
        passed=not reasons,
        matched_rows=matched_rows,
        output_rows=output_rows,
        pixel_years=pixel_years,
        quality_good_rows=quality_good_rows,
        snow_free_rows=snow_free_rows,
        unknown_snow_rows=unknown_snow_rows,
        invalid_reflectance_rows=invalid_reflectance_rows,
        reasons=tuple(reasons),
    )
