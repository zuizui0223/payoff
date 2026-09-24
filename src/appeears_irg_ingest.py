"""Convert AppEEARS V061 point-result CSVs into PAYOFF-B IRG input.

This layer is explicitly a current-product sensitivity lane.

Expected AppEEARS inputs:
- one MOD09Q1.061 point-result CSV containing b01, b02, QC and State QA;
- one MOD10A2.061 point-result CSV containing Maximum_Snow_Extent.

AppEEARS result values for reflectance layers are treated as scale-applied
physical reflectance values, consistent with the AppEEARS product service /
point-result workflow. QA layers remain integer bit fields.

The output schema matches scripts/fit_peak_irg_from_ndvi.py:

    pixel_id
    year
    doy
    ndvi
    snow_free
    quality_good

Quality rule for this V061 sensitivity lane:
- MODLAND QA == ideal (00);
- band-1 quality == highest (0000);
- band-2 quality == highest (0000);
- atmospheric correction performed;
- State QA cloud state == clear (00);
- no cloud shadow;
- aerosol category is not high;
- internal cloud flag is clear;
- not adjacent to cloud.

Snow rule from MOD10A2.061 Maximum_Snow_Extent:
- 25  -> snow_free=True
- 200 -> snow_free=False
- all other values are unknown and the row is omitted.

These rules are transparent sensitivity rules, not a claim of bit-for-bit
reconstruction of the historical study-faithful V006 preprocessing.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import isfinite
import re
from typing import Iterable


@dataclass(frozen=True)
class AppEEARSReflectanceRow:
    pixel_id: str
    date: datetime
    red_reflectance: float
    nir_reflectance: float
    qc_250m: int
    state_250m: int


@dataclass(frozen=True)
class AppEEARSSnowRow:
    pixel_id: str
    date: datetime
    maximum_snow_extent: int


@dataclass(frozen=True)
class IRGInputRow:
    pixel_id: str
    year: int
    doy: int
    ndvi: float
    snow_free: bool
    quality_good: bool


@dataclass(frozen=True)
class AppEEARSIRGConversion:
    reflectance_rows: int
    snow_rows: int
    matched_rows: int
    output_rows: int
    unknown_snow_rows: int
    invalid_reflectance_rows: int
    duplicate_reflectance_keys: int
    duplicate_snow_keys: int
    rows: tuple[IRGInputRow, ...]


def normalize_column(value: str) -> str:
    return re.sub(
        r"[^a-z0-9]+",
        "_",
        value.strip().lower(),
    ).strip("_")


def resolve_column(
    headers: Iterable[str],
    *,
    exact_aliases: tuple[str, ...] = (),
    suffix_aliases: tuple[str, ...] = (),
) -> str:
    """Resolve AppEEARS columns across task-name/product-prefix variations."""

    header_list = tuple(headers)
    normalized = {
        normalize_column(header): header
        for header in header_list
    }

    for alias in exact_aliases:
        key = normalize_column(alias)
        if key in normalized:
            return normalized[key]

    candidates: list[str] = []
    normalized_suffixes = tuple(
        normalize_column(alias)
        for alias in suffix_aliases
    )
    for header in header_list:
        key = normalize_column(header)
        if any(
            key.endswith(suffix)
            for suffix in normalized_suffixes
        ):
            candidates.append(header)

    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        raise ValueError(
            "no AppEEARS column matches aliases "
            + ", ".join(exact_aliases + suffix_aliases)
        )
    raise ValueError(
        "ambiguous AppEEARS column match: "
        + ", ".join(candidates)
    )


def parse_appeears_date(value: str) -> datetime:
    """Parse common AppEEARS point-result date representations."""

    text = value.strip()
    if not text:
        raise ValueError("AppEEARS Date must be non-empty")

    for fmt in (
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%m-%d-%Y",
        "%Y/%m/%d",
    ):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass

    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(
            f"unsupported AppEEARS date format: {value!r}"
        ) from exc


def mod09q1_v061_quality_good(
    qc_250m: int,
    state_250m: int,
) -> bool:
    """Strict V061 sensitivity QA screen from official MOD09 bit fields."""

    if not 0 <= qc_250m <= 65535:
        return False
    if not 0 <= state_250m <= 65535:
        return False
    if qc_250m == 65535 or state_250m == 65535:
        return False

    modland = qc_250m & 0b11
    band1_quality = (qc_250m >> 4) & 0b1111
    band2_quality = (qc_250m >> 8) & 0b1111
    atmospheric_correction = (qc_250m >> 12) & 0b1

    cloud_state = state_250m & 0b11
    cloud_shadow = (state_250m >> 2) & 0b1
    aerosol = (state_250m >> 6) & 0b11
    internal_cloud = (state_250m >> 10) & 0b1
    adjacent_cloud = (state_250m >> 13) & 0b1

    return (
        modland == 0
        and band1_quality == 0
        and band2_quality == 0
        and atmospheric_correction == 1
        and cloud_state == 0
        and cloud_shadow == 0
        and aerosol != 3
        and internal_cloud == 0
        and adjacent_cloud == 0
    )


def snow_free_from_mod10a2_v061(
    maximum_snow_extent: int,
) -> bool | None:
    """Decode the official V061 maximum-snow-extent land codes."""

    if maximum_snow_extent == 25:
        return True
    if maximum_snow_extent == 200:
        return False
    return None


def ndvi_from_scaled_reflectance(
    red_reflectance: float,
    nir_reflectance: float,
) -> float | None:
    """Compute NDVI from scale-applied AppEEARS reflectances."""

    if not isfinite(red_reflectance) or not isfinite(nir_reflectance):
        return None

    # MOD09Q1.061 official scaled valid range is -0.01 .. 1.6.
    if not -0.01 <= red_reflectance <= 1.6:
        return None
    if not -0.01 <= nir_reflectance <= 1.6:
        return None

    denominator = nir_reflectance + red_reflectance
    if denominator <= 0.0:
        return None

    value = (
        nir_reflectance - red_reflectance
    ) / denominator
    if not -1.0 <= value <= 1.0:
        return None
    return value


def convert_appeears_v061_to_irg(
    reflectance_rows: Iterable[AppEEARSReflectanceRow],
    snow_rows: Iterable[AppEEARSSnowRow],
) -> AppEEARSIRGConversion:
    """Join exact point/date composites and build strict IRG-input rows."""

    refl = tuple(reflectance_rows)
    snow = tuple(snow_rows)

    reflectance_by_key: dict[
        tuple[str, datetime],
        AppEEARSReflectanceRow,
    ] = {}
    duplicate_reflectance = 0
    for row in refl:
        key = (row.pixel_id, row.date)
        if key in reflectance_by_key:
            duplicate_reflectance += 1
            continue
        reflectance_by_key[key] = row

    snow_by_key: dict[
        tuple[str, datetime],
        AppEEARSSnowRow,
    ] = {}
    duplicate_snow = 0
    for row in snow:
        key = (row.pixel_id, row.date)
        if key in snow_by_key:
            duplicate_snow += 1
            continue
        snow_by_key[key] = row

    output: list[IRGInputRow] = []
    matched = 0
    unknown_snow = 0
    invalid_reflectance = 0

    for key, reflectance in reflectance_by_key.items():
        snow_row = snow_by_key.get(key)
        if snow_row is None:
            continue
        matched += 1

        snow_free = snow_free_from_mod10a2_v061(
            snow_row.maximum_snow_extent
        )
        if snow_free is None:
            unknown_snow += 1
            continue

        ndvi = ndvi_from_scaled_reflectance(
            reflectance.red_reflectance,
            reflectance.nir_reflectance,
        )
        if ndvi is None:
            invalid_reflectance += 1
            continue

        quality_good = mod09q1_v061_quality_good(
            reflectance.qc_250m,
            reflectance.state_250m,
        )

        output.append(
            IRGInputRow(
                pixel_id=reflectance.pixel_id,
                year=reflectance.date.year,
                doy=int(
                    reflectance.date.strftime("%j")
                ),
                ndvi=ndvi,
                snow_free=snow_free,
                quality_good=quality_good,
            )
        )

    return AppEEARSIRGConversion(
        reflectance_rows=len(refl),
        snow_rows=len(snow),
        matched_rows=matched,
        output_rows=len(output),
        unknown_snow_rows=unknown_snow,
        invalid_reflectance_rows=invalid_reflectance,
        duplicate_reflectance_keys=duplicate_reflectance,
        duplicate_snow_keys=duplicate_snow,
        rows=tuple(
            sorted(
                output,
                key=lambda row: (
                    row.pixel_id,
                    row.year,
                    row.doy,
                ),
            )
        ),
    )
