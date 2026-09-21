"""Build AppEEARS point-task manifests from projected GPS observations.

This layer performs no authenticated network action. It converts projected
movement locations to the MODIS sinusoidal grid, deduplicates repeated GPS
locations to 250 m cells, and creates year-scoped AppEEARS V061 sensitivity
requests.

The current-product request is intentionally labeled a sensitivity lane:

    MOD09Q1.061 + MOD10A2.061

It does not replace the study-faithful MOD09Q1.006 lane.

Projection support is loaded lazily through the optional earthdata extra.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import floor, isfinite
from typing import Iterable


MODIS_SINUSOIDAL_PROJ4 = (
    "+proj=sinu +R=6371007.181 +nadgrids=@null "
    "+wktext +units=m +no_defs"
)

MODIS_GLOBAL_XMIN = -20015109.354
MODIS_GLOBAL_YMAX = 10007554.677
MODIS_250M_PIXEL_SIZE_M = 231.65635826395834

APPEEARS_V061_LAYERS = (
    ("MOD09Q1.061", "sur_refl_b01"),
    ("MOD09Q1.061", "sur_refl_b02"),
    ("MOD09Q1.061", "sur_refl_qc_250m"),
    ("MOD09Q1.061", "sur_refl_state_250m"),
    ("MOD10A2.061", "Maximum_Snow_Extent"),
    ("MOD10A2.061", "Eight_Day_Snow_Cover"),
)


@dataclass(frozen=True)
class ProjectedGPSObservation:
    observation_id: str
    animal_id: str
    animal_year: str
    group: str
    timestamp: datetime
    x: float
    y: float

    def __post_init__(self) -> None:
        for name in (
            "observation_id",
            "animal_id",
            "animal_year",
            "group",
        ):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} must be non-empty")
        if not isfinite(self.x) or not isfinite(self.y):
            raise ValueError("projected coordinates must be finite")


@dataclass(frozen=True)
class MODIS250Cell:
    cell_id: str
    row: int
    column: int
    sinusoidal_x: float
    sinusoidal_y: float
    latitude: float
    longitude: float


@dataclass(frozen=True)
class ObservationCellLink:
    observation_id: str
    animal_id: str
    animal_year: str
    group: str
    timestamp: datetime
    year: int
    cell_id: str


@dataclass(frozen=True)
class MODISCellDeduplication:
    source_crs: str
    gps_observations: int
    unique_cells: int
    unique_cell_years: int
    cells: tuple[MODIS250Cell, ...]
    links: tuple[ObservationCellLink, ...]

    @property
    def compression_ratio(self) -> float:
        return self.unique_cells / self.gps_observations


def _load_transformers(source_crs: str):
    try:
        from pyproj import CRS, Transformer
    except ImportError as exc:
        raise RuntimeError(
            "MODIS request generation requires the optional project "
            "dependency group earthdata"
        ) from exc

    source = CRS.from_user_input(source_crs)
    modis = CRS.from_proj4(MODIS_SINUSOIDAL_PROJ4)
    wgs84 = CRS.from_epsg(4326)

    to_modis = Transformer.from_crs(
        source,
        modis,
        always_xy=True,
    )
    to_wgs84 = Transformer.from_crs(
        modis,
        wgs84,
        always_xy=True,
    )
    return to_modis, to_wgs84


def modis_250m_cell_indices(
    sinusoidal_x: float,
    sinusoidal_y: float,
) -> tuple[int, int]:
    """Return global row/column indices on the standard 250 m MODIS grid."""

    if not isfinite(sinusoidal_x) or not isfinite(sinusoidal_y):
        raise ValueError("sinusoidal coordinates must be finite")

    column = floor(
        (sinusoidal_x - MODIS_GLOBAL_XMIN)
        / MODIS_250M_PIXEL_SIZE_M
    )
    row = floor(
        (MODIS_GLOBAL_YMAX - sinusoidal_y)
        / MODIS_250M_PIXEL_SIZE_M
    )
    if row < 0 or column < 0:
        raise ValueError(
            "projected point lies outside the standard global MODIS grid"
        )
    return row, column


def modis_250m_cell_center(
    row: int,
    column: int,
) -> tuple[float, float]:
    if row < 0 or column < 0:
        raise ValueError("MODIS row and column must be non-negative")

    x = (
        MODIS_GLOBAL_XMIN
        + (column + 0.5) * MODIS_250M_PIXEL_SIZE_M
    )
    y = (
        MODIS_GLOBAL_YMAX
        - (row + 0.5) * MODIS_250M_PIXEL_SIZE_M
    )
    return x, y


def _cell_id(row: int, column: int) -> str:
    return f"modis250_r{row:05d}_c{column:06d}"


def deduplicate_to_modis_250m_cells(
    observations: Iterable[ProjectedGPSObservation],
    *,
    source_crs: str = "EPSG:32613",
) -> MODISCellDeduplication:
    """Map projected GPS observations to unique standard MODIS 250 m cells."""

    rows = tuple(observations)
    if not rows:
        raise ValueError("at least one GPS observation is required")

    to_modis, to_wgs84 = _load_transformers(source_crs)

    cells_by_id: dict[str, MODIS250Cell] = {}
    links: list[ObservationCellLink] = []

    for observation in rows:
        sx, sy = to_modis.transform(
            observation.x,
            observation.y,
        )
        row, column = modis_250m_cell_indices(
            float(sx),
            float(sy),
        )
        cell_id = _cell_id(row, column)

        if cell_id not in cells_by_id:
            center_x, center_y = modis_250m_cell_center(
                row,
                column,
            )
            longitude, latitude = to_wgs84.transform(
                center_x,
                center_y,
            )
            if (
                not isfinite(longitude)
                or not isfinite(latitude)
                or not -180.0 <= longitude <= 180.0
                or not -90.0 <= latitude <= 90.0
            ):
                raise ValueError(
                    "MODIS cell center could not be transformed to WGS84"
                )
            cells_by_id[cell_id] = MODIS250Cell(
                cell_id=cell_id,
                row=row,
                column=column,
                sinusoidal_x=center_x,
                sinusoidal_y=center_y,
                latitude=float(latitude),
                longitude=float(longitude),
            )

        links.append(
            ObservationCellLink(
                observation_id=observation.observation_id,
                animal_id=observation.animal_id,
                animal_year=observation.animal_year,
                group=observation.group,
                timestamp=observation.timestamp,
                year=observation.timestamp.year,
                cell_id=cell_id,
            )
        )

    cell_years = {
        (link.cell_id, link.year)
        for link in links
    }

    return MODISCellDeduplication(
        source_crs=source_crs,
        gps_observations=len(rows),
        unique_cells=len(cells_by_id),
        unique_cell_years=len(cell_years),
        cells=tuple(
            sorted(
                cells_by_id.values(),
                key=lambda cell: cell.cell_id,
            )
        ),
        links=tuple(links),
    )


def summarize_appeears_coverage(
    deduplication: MODISCellDeduplication,
) -> dict:
    """Summarize source coverage before authenticated request submission."""

    observation_counts_by_year: dict[int, int] = {}
    observation_counts_by_group: dict[str, int] = {}
    cell_ids_by_year: dict[int, set[str]] = {}
    cell_ids_by_group: dict[str, set[str]] = {}

    for link in deduplication.links:
        observation_counts_by_year[link.year] = (
            observation_counts_by_year.get(link.year, 0) + 1
        )
        observation_counts_by_group[link.group] = (
            observation_counts_by_group.get(link.group, 0) + 1
        )
        cell_ids_by_year.setdefault(link.year, set()).add(
            link.cell_id
        )
        cell_ids_by_group.setdefault(link.group, set()).add(
            link.cell_id
        )

    return {
        "gps_observations_by_year": {
            str(year): observation_counts_by_year[year]
            for year in sorted(observation_counts_by_year)
        },
        "gps_observations_by_group": {
            group: observation_counts_by_group[group]
            for group in sorted(observation_counts_by_group)
        },
        "unique_cells_by_year": {
            str(year): len(cell_ids_by_year[year])
            for year in sorted(cell_ids_by_year)
        },
        "unique_cells_by_group": {
            group: len(cell_ids_by_group[group])
            for group in sorted(cell_ids_by_group)
        },
    }


def _chunks(values, size: int):
    for start in range(0, len(values), size):
        yield values[start : start + size]


def build_appeears_v061_tasks(
    deduplication: MODISCellDeduplication,
    *,
    task_prefix: str = "aikens_mod09q1_v061",
    max_points_per_task: int = 1000,
) -> dict:
    """Create year-scoped AppEEARS point requests for V061 sensitivity.

    max_points_per_task is an operational chunk size chosen by the analysis,
    not a claim about the AppEEARS service maximum.
    """

    if max_points_per_task <= 0:
        raise ValueError("max_points_per_task must be positive")
    if not task_prefix.strip():
        raise ValueError("task_prefix must be non-empty")

    cells = {
        cell.cell_id: cell
        for cell in deduplication.cells
    }
    cells_by_year: dict[int, set[str]] = {}
    for link in deduplication.links:
        cells_by_year.setdefault(
            link.year,
            set(),
        ).add(link.cell_id)

    layers = [
        {
            "product": product,
            "layer": layer,
        }
        for product, layer in APPEEARS_V061_LAYERS
    ]

    tasks = []
    for year in sorted(cells_by_year):
        cell_ids = sorted(cells_by_year[year])
        for part_index, chunk in enumerate(
            _chunks(cell_ids, max_points_per_task),
            start=1,
        ):
            coordinates = [
                {
                    "id": cell_id,
                    "category": "aikens_modis250_cell",
                    "latitude": cells[cell_id].latitude,
                    "longitude": cells[cell_id].longitude,
                }
                for cell_id in chunk
            ]
            tasks.append(
                {
                    "year": year,
                    "part": part_index,
                    "cell_count": len(chunk),
                    "task": {
                        "task_type": "point",
                        "task_name": (
                            f"{task_prefix}_{year}_p{part_index:03d}"
                        ),
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

    coverage = summarize_appeears_coverage(
        deduplication
    )

    return {
        "status": "appeears_v061_sensitivity_manifest",
        "reconstruction_lane": "v061_sensitivity_only",
        "source_crs": deduplication.source_crs,
        "gps_observations": deduplication.gps_observations,
        "unique_modis250_cells": deduplication.unique_cells,
        "unique_modis250_cell_years": (
            deduplication.unique_cell_years
        ),
        "operational_max_points_per_task": max_points_per_task,
        "task_count": len(tasks),
        "years": sorted(cells_by_year),
        "coverage": coverage,
        "layers": layers,
        "tasks": tasks,
        "claim_boundary": (
            "current-product V061 sensitivity extraction only; "
            "does not replace study-faithful MOD09Q1.006 reconstruction"
        ),
    }
