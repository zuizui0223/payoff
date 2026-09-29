"""Frozen Movebank GPS input hygiene for PAYOFF-B greater snow goose."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


RAW_REQUIRED = (
    "timestamp",
    "location_long",
    "location_lat",
    "individual_id",
    "individual_local_identifier",
    "tag_id",
    "tag_local_identifier",
    "visible",
)


@dataclass(frozen=True)
class HygieneAudit:
    raw_rows: int
    exact_duplicates_collapsed: int
    visible_true_retained: int
    visible_false_excluded: int
    individuals_retained: int
    year_counts: dict[int, int]


def _normalize_visible(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and value in (0, 1):
        return bool(value)
    text = str(value).strip().lower()
    if text in {"true", "t", "1"}:
        return True
    if text in {"false", "f", "0"}:
        return False
    raise ValueError(f"unrecognized Movebank visible value: {value!r}")


def clean_movebank_gps_events(data):
    """Return deterministic movepp-ready rows plus an audit.

    Primary rules:
    - exact duplicate raw rows are collapsed;
    - only Movebank visible=true fixes are retained;
    - timestamp must parse as UTC;
    - visible=true coordinates must be finite and in WGS84 bounds;
    - conflicting same-individual same-timestamp rows fail closed;
    - no interpolation, resampling, smoothing, or speed filtering occurs here.
    """

    import numpy as np
    import pandas as pd

    missing = set(RAW_REQUIRED) - set(data.columns)
    if missing:
        raise ValueError(
            "missing required Movebank columns: "
            + ",".join(sorted(missing))
        )

    raw = data.loc[:, RAW_REQUIRED].copy()
    raw_rows = int(len(raw))
    if raw_rows == 0:
        raise ValueError("Movebank GPS table is empty")

    # Missing visibility is never guessed.
    if raw["visible"].isna().any():
        raise ValueError("Movebank visible contains missing values")
    raw["_visible_bool"] = raw["visible"].map(_normalize_visible)

    # Parse all timestamps consistently before duplicate adjudication.
    try:
        raw["_time_utc"] = pd.to_datetime(
            raw["timestamp"],
            utc=True,
            errors="raise",
        )
    except Exception as exc:
        raise ValueError("Movebank timestamp is not valid UTC datetime") from exc
    if raw["_time_utc"].isna().any():
        raise ValueError("Movebank timestamp contains missing values")

    if raw["individual_id"].isna().any():
        raise ValueError("Movebank individual_id contains missing values")

    before = len(raw)
    raw = raw.drop_duplicates(subset=list(RAW_REQUIRED), keep="first")
    exact_collapsed = int(before - len(raw))

    # Conflicting rows at one animal-time are never arbitrarily resolved.
    conflicts = (
        raw.groupby(["individual_id", "_time_utc"], dropna=False)
        .size()
    )
    conflict_keys = conflicts[conflicts > 1]
    if len(conflict_keys):
        first = conflict_keys.index[0]
        raise ValueError(
            "conflicting Movebank rows for individual_id/timestamp: "
            f"{first[0]} @ {first[1]}"
        )

    retained = raw[raw["_visible_bool"]].copy()
    excluded = int((~raw["_visible_bool"]).sum())

    for col in ("location_long", "location_lat"):
        retained[col] = pd.to_numeric(retained[col], errors="coerce")

    lon = retained["location_long"].to_numpy(dtype=float)
    lat = retained["location_lat"].to_numpy(dtype=float)
    valid = (
        np.isfinite(lon)
        & np.isfinite(lat)
        & (lon >= -180.0)
        & (lon <= 180.0)
        & (lat >= -90.0)
        & (lat <= 90.0)
    )
    if not bool(np.all(valid)):
        bad = retained.loc[~valid, ["individual_id", "timestamp"]].iloc[0]
        raise ValueError(
            "invalid coordinate in visible=true Movebank row: "
            f"{bad['individual_id']} @ {bad['timestamp']}"
        )

    if retained.empty:
        raise ValueError("no visible=true GPS rows remain")

    retained = retained.sort_values(
        ["individual_id", "_time_utc"],
        kind="mergesort",
    ).reset_index(drop=True)

    years = retained["_time_utc"].dt.year.astype(int)
    year_counts = {
        int(k): int(v)
        for k, v in years.value_counts().sort_index().items()
    }

    # Canonical movepp-facing names while preserving source IDs for audit.
    clean = pd.DataFrame(
        {
            "individual": retained["individual_id"].astype(str),
            "time": retained["_time_utc"],
            "lon": retained["location_long"].astype(float),
            "lat": retained["location_lat"].astype(float),
            "individual_id": retained["individual_id"],
            "individual_local_identifier": retained[
                "individual_local_identifier"
            ],
            "tag_id": retained["tag_id"],
            "tag_local_identifier": retained["tag_local_identifier"],
        }
    )

    audit = HygieneAudit(
        raw_rows=raw_rows,
        exact_duplicates_collapsed=exact_collapsed,
        visible_true_retained=int(len(clean)),
        visible_false_excluded=excluded,
        individuals_retained=int(clean["individual"].nunique()),
        year_counts=year_counts,
    )
    return clean, audit
