"""Build the frozen PAYOFF-B V7B AppEEARS point manifest.

The V7B source is intentionally small and behavior-independent: fixed
generalized-region coordinates are sampled for the same declared calendar years
regardless of goose behavior or focal outcomes.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable, Sequence

from src.appeears_modis_request import APPEEARS_V061_LAYERS


@dataclass(frozen=True)
class FeedbackRegion:
    flyway: str
    region_id: str
    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        if not self.flyway.strip() or not self.region_id.strip():
            raise ValueError("flyway and region_id must be non-empty")
        if not isfinite(self.latitude) or not -90.0 <= self.latitude <= 90.0:
            raise ValueError("latitude must be finite and in [-90,90]")
        if not isfinite(self.longitude) or not -180.0 <= self.longitude <= 180.0:
            raise ValueError("longitude must be finite and in [-180,180]")

    @property
    def point_id(self) -> str:
        return f"{self.flyway}_{self.region_id}"


def build_feedback_appeears_manifest(
    regions: Iterable[FeedbackRegion],
    *,
    years: Sequence[int],
    task_prefix: str = "payoff_v7b_feedback",
) -> dict:
    rows = tuple(regions)
    if not rows:
        raise ValueError("at least one region is required")
    if len({row.point_id for row in rows}) != len(rows):
        raise ValueError("region point ids must be unique")
    declared_years = tuple(sorted({int(year) for year in years}))
    if not declared_years:
        raise ValueError("at least one year is required")
    if any(year < 2000 or year > 2100 for year in declared_years):
        raise ValueError("declared years are outside supported contract range")
    if not task_prefix.strip():
        raise ValueError("task_prefix must be non-empty")

    layers = [
        {"product": product, "layer": layer}
        for product, layer in APPEEARS_V061_LAYERS
    ]
    coordinates = [
        {
            "id": row.point_id,
            "category": "payoff_v7b_fixed_region",
            "latitude": row.latitude,
            "longitude": row.longitude,
        }
        for row in sorted(rows, key=lambda item: item.point_id)
    ]

    tasks = []
    for year in declared_years:
        tasks.append(
            {
                "year": year,
                "region_count": len(coordinates),
                "task": {
                    "task_type": "point",
                    "task_name": f"{task_prefix}_{year}",
                    "params": {
                        "dates": [
                            {
                                "startDate": f"01-01-{year}",
                                "endDate": f"12-31-{year}",
                            }
                        ],
                        "layers": layers,
                        "coordinates": coordinates,
                    },
                },
            }
        )

    return {
        "schema": "payoff_b_v7b_appeears_manifest_v1",
        "status": "PRE_ENVIRONMENT_VALUE",
        "reconstruction_lane": "MOD09Q1.061_MOD10A2.061_current_product",
        "region_count": len(rows),
        "years": list(declared_years),
        "expected_region_years": len(rows) * len(declared_years),
        "task_count": len(tasks),
        "layers": layers,
        "tasks": tasks,
        "claim_boundary": (
            "fixed-region environmental extraction only; no behavior-selected "
            "GPS pixels and no V7B behavioral outcome access"
        ),
    }
