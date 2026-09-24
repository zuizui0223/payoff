"""Attach reconstructed peak-IRG dates to GPS observations.

The join is explicit and fail-auditable. Missing pixel-year environmental
records are counted rather than silently removed. The output can be passed
directly to build_fixed_interval_phase_pairs.py.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable


@dataclass(frozen=True)
class GPSPhaseKey:
    observation_id: str
    animal_id: str
    animal_year: str
    group: str
    timestamp: datetime
    pixel_id: str

    def __post_init__(self) -> None:
        for name in (
            "observation_id",
            "animal_id",
            "animal_year",
            "group",
            "pixel_id",
        ):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} must be non-empty")


@dataclass(frozen=True)
class PeakIRGRecord:
    pixel_id: str
    year: int
    modis_product: str
    reconstruction_lane: str
    peak_irg_date: str

    def __post_init__(self) -> None:
        if not self.pixel_id.strip():
            raise ValueError("pixel_id must be non-empty")
        if self.modis_product not in {
            "MOD09Q1.006",
            "MOD09Q1.061",
        }:
            raise ValueError("unsupported MODIS product")
        if self.reconstruction_lane not in {
            "study_faithful_v006",
            "v061_sensitivity_only",
            "v061_primary_successor_after_v006_decommission",
        }:
            raise ValueError(
                "unsupported IRG reconstruction lane"
            )
        allowed_lanes = (
            {"study_faithful_v006"}
            if self.modis_product == "MOD09Q1.006"
            else {
                "v061_sensitivity_only",
                "v061_primary_successor_after_v006_decommission",
            }
        )
        if self.reconstruction_lane not in allowed_lanes:
            raise ValueError(
                "MODIS product and reconstruction lane disagree"
            )
        try:
            parsed = datetime.fromisoformat(
                self.peak_irg_date
            )
        except ValueError as exc:
            raise ValueError(
                "peak_irg_date must be ISO compatible"
            ) from exc
        if parsed.year != self.year:
            raise ValueError(
                "peak_irg_date year does not match record year"
            )


@dataclass(frozen=True)
class PhaseAnnotatedGPS:
    observation_id: str
    animal_id: str
    animal_year: str
    group: str
    timestamp: datetime
    pixel_id: str
    local_peak_irg_timestamp: datetime
    modis_product: str
    reconstruction_lane: str


@dataclass(frozen=True)
class EnvironmentalJoinAudit:
    gps_observations: int
    matched_observations: int
    missing_observations: int
    matched_fraction: float
    matched_by_group: tuple[tuple[str, int], ...]
    missing_by_group: tuple[tuple[str, int], ...]
    products: tuple[str, ...]
    reconstruction_lanes: tuple[str, ...]
    annotated: tuple[PhaseAnnotatedGPS, ...]


def attach_peak_irg_to_gps(
    gps: Iterable[GPSPhaseKey],
    peak_irg: Iterable[PeakIRGRecord],
    *,
    required_modis_product: str | None = None,
    minimum_matched_fraction: float = 0.0,
    enforce_minimum: bool = True,
) -> EnvironmentalJoinAudit:
    """Join GPS points to one unique peak-IRG record per pixel-year."""

    if not 0.0 <= minimum_matched_fraction <= 1.0:
        raise ValueError(
            "minimum_matched_fraction must lie in [0,1]"
        )

    gps_rows = tuple(gps)
    if not gps_rows:
        raise ValueError("at least one GPS observation is required")

    records = tuple(peak_irg)
    index: dict[tuple[str, int], PeakIRGRecord] = {}
    for record in records:
        key = (record.pixel_id, record.year)
        if key in index:
            raise ValueError(
                "duplicate peak-IRG record for pixel-year "
                f"{record.pixel_id}/{record.year}"
            )
        index[key] = record

    annotated: list[PhaseAnnotatedGPS] = []
    matched_by_group: dict[str, int] = {}
    missing_by_group: dict[str, int] = {}

    for row in gps_rows:
        record = index.get(
            (row.pixel_id, row.timestamp.year)
        )
        if (
            record is None
            or (
                required_modis_product is not None
                and record.modis_product
                != required_modis_product
            )
        ):
            missing_by_group[row.group] = (
                missing_by_group.get(row.group, 0) + 1
            )
            continue

        peak_date = datetime.fromisoformat(
            record.peak_irg_date
        )
        if row.timestamp.tzinfo is not None:
            peak_date = peak_date.replace(
                tzinfo=row.timestamp.tzinfo
            )

        annotated.append(
            PhaseAnnotatedGPS(
                observation_id=row.observation_id,
                animal_id=row.animal_id,
                animal_year=row.animal_year,
                group=row.group,
                timestamp=row.timestamp,
                pixel_id=row.pixel_id,
                local_peak_irg_timestamp=peak_date,
                modis_product=record.modis_product,
                reconstruction_lane=(
                    record.reconstruction_lane
                ),
            )
        )
        matched_by_group[row.group] = (
            matched_by_group.get(row.group, 0) + 1
        )

    matched = len(annotated)
    fraction = matched / len(gps_rows)
    if enforce_minimum and fraction < minimum_matched_fraction:
        raise ValueError(
            "environmental join matched fraction "
            f"{fraction:.6f} below predeclared minimum "
            f"{minimum_matched_fraction:.6f}"
        )

    products = tuple(
        sorted({row.modis_product for row in annotated})
    )
    lanes = tuple(
        sorted(
            {
                row.reconstruction_lane
                for row in annotated
            }
        )
    )
    if len(products) > 1 or len(lanes) > 1:
        raise ValueError(
            "one environmental join cannot mix MODIS product versions or "
            "reconstruction lanes"
        )

    return EnvironmentalJoinAudit(
        gps_observations=len(gps_rows),
        matched_observations=matched,
        missing_observations=(
            len(gps_rows) - matched
        ),
        matched_fraction=fraction,
        matched_by_group=tuple(
            sorted(matched_by_group.items())
        ),
        missing_by_group=tuple(
            sorted(missing_by_group.items())
        ),
        products=products,
        reconstruction_lanes=lanes,
        annotated=tuple(annotated),
    )
