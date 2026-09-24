"""Attach environmental phase to preselected fixed GPS targets and pair them."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from src.fixed_interval_gps_targets import FixedIntervalGPSTarget
from src.phase_environment_join import PeakIRGRecord


@dataclass(frozen=True)
class AnnotatedFixedTarget:
    animal_id: str
    animal_year: str
    group: str
    target_index: int
    target_timestamp: datetime
    observation_id: str
    observed_timestamp: datetime
    deviation_seconds: float
    pixel_id: str
    phase_valid: bool
    local_peak_irg_timestamp: datetime | None
    phase_error_days: float | None
    modis_product: str | None
    reconstruction_lane: str | None


@dataclass(frozen=True)
class FixedTargetPhaseAudit:
    total_targets: int
    valid_targets: int
    invalid_targets: int
    valid_by_group: tuple[tuple[str, int], ...]
    invalid_by_group: tuple[tuple[str, int], ...]
    products: tuple[str, ...]
    reconstruction_lanes: tuple[str, ...]
    targets: tuple[AnnotatedFixedTarget, ...]


@dataclass(frozen=True)
class FixedTargetPhasePair:
    animal_id: str
    animal_year: str
    group: str
    start_target_index: int
    start_timestamp: datetime
    end_timestamp: datetime
    phase_before: float
    phase_after: float


def attach_phase_to_fixed_targets(
    targets: Iterable[FixedIntervalGPSTarget],
    peak_irg: Iterable[PeakIRGRecord],
    *,
    required_modis_product: str | None = None,
) -> FixedTargetPhaseAudit:
    """Attach peak IRG without changing which GPS observation was selected."""

    rows = tuple(targets)
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

    annotated: list[AnnotatedFixedTarget] = []
    valid_by_group: dict[str, int] = {}
    invalid_by_group: dict[str, int] = {}

    for row in rows:
        record = index.get(
            (row.pixel_id, row.observed_timestamp.year)
        )
        valid = (
            record is not None
            and (
                required_modis_product is None
                or record.modis_product == required_modis_product
            )
        )

        if not valid:
            invalid_by_group[row.group] = (
                invalid_by_group.get(row.group, 0) + 1
            )
            annotated.append(
                AnnotatedFixedTarget(
                    animal_id=row.animal_id,
                    animal_year=row.animal_year,
                    group=row.group,
                    target_index=row.target_index,
                    target_timestamp=row.target_timestamp,
                    observation_id=row.observation_id,
                    observed_timestamp=row.observed_timestamp,
                    deviation_seconds=row.deviation_seconds,
                    pixel_id=row.pixel_id,
                    phase_valid=False,
                    local_peak_irg_timestamp=None,
                    phase_error_days=None,
                    modis_product=None,
                    reconstruction_lane=None,
                )
            )
            continue

        assert record is not None
        peak = datetime.fromisoformat(record.peak_irg_date)
        if row.observed_timestamp.tzinfo is not None:
            peak = peak.replace(tzinfo=row.observed_timestamp.tzinfo)
        phase = (
            row.observed_timestamp - peak
        ).total_seconds() / 86400.0

        valid_by_group[row.group] = valid_by_group.get(row.group, 0) + 1
        annotated.append(
            AnnotatedFixedTarget(
                animal_id=row.animal_id,
                animal_year=row.animal_year,
                group=row.group,
                target_index=row.target_index,
                target_timestamp=row.target_timestamp,
                observation_id=row.observation_id,
                observed_timestamp=row.observed_timestamp,
                deviation_seconds=row.deviation_seconds,
                pixel_id=row.pixel_id,
                phase_valid=True,
                local_peak_irg_timestamp=peak,
                phase_error_days=phase,
                modis_product=record.modis_product,
                reconstruction_lane=record.reconstruction_lane,
            )
        )

    valid_rows = [row for row in annotated if row.phase_valid]
    products = tuple(
        sorted(
            {
                str(row.modis_product)
                for row in valid_rows
                if row.modis_product is not None
            }
        )
    )
    lanes = tuple(
        sorted(
            {
                str(row.reconstruction_lane)
                for row in valid_rows
                if row.reconstruction_lane is not None
            }
        )
    )
    if len(products) > 1 or len(lanes) > 1:
        raise ValueError(
            "one fixed-target phase audit cannot mix product versions or lanes"
        )

    return FixedTargetPhaseAudit(
        total_targets=len(rows),
        valid_targets=len(valid_rows),
        invalid_targets=len(rows) - len(valid_rows),
        valid_by_group=tuple(sorted(valid_by_group.items())),
        invalid_by_group=tuple(sorted(invalid_by_group.items())),
        products=products,
        reconstruction_lanes=lanes,
        targets=tuple(annotated),
    )


def build_adjacent_phase_pairs(
    targets: Iterable[AnnotatedFixedTarget],
) -> tuple[FixedTargetPhasePair, ...]:
    """Pair only adjacent preselected target indices with valid phase."""

    rows = tuple(targets)
    by_year: dict[str, list[AnnotatedFixedTarget]] = {}
    for row in rows:
        by_year.setdefault(row.animal_year, []).append(row)

    pairs: list[FixedTargetPhasePair] = []
    for animal_year, year_rows in by_year.items():
        animals = {row.animal_id for row in year_rows}
        groups = {row.group for row in year_rows}
        if len(animals) != 1 or len(groups) != 1:
            raise ValueError(
                f"animal_year {animal_year!r} has inconsistent identity/group"
            )
        animal_id = next(iter(animals))
        group = next(iter(groups))
        valid = {
            row.target_index: row
            for row in year_rows
            if row.phase_valid and row.phase_error_days is not None
        }
        for start_index in sorted(valid):
            end_index = start_index + 1
            if end_index not in valid:
                continue
            start = valid[start_index]
            end = valid[end_index]
            pairs.append(
                FixedTargetPhasePair(
                    animal_id=animal_id,
                    animal_year=animal_year,
                    group=group,
                    start_target_index=start_index,
                    start_timestamp=start.target_timestamp,
                    end_timestamp=end.target_timestamp,
                    phase_before=float(start.phase_error_days),
                    phase_after=float(end.phase_error_days),
                )
            )

    return tuple(pairs)
