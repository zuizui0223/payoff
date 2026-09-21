"""Merge AppEEARS point-result CSVs from multiple exact-manifest tasks.

The full Aikens V061 request is year/task sharded. This layer merges task-level
CSV outputs by product before the existing V061 -> IRG-input converter runs.

It refuses:
- no product CSVs;
- header drift across tasks;
- duplicate data rows across task files.

Duplicate rejection is conservative because the exact manifest partitions
unique cell/year points across tasks.
"""

from __future__ import annotations

from dataclasses import dataclass
import csv
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class MergedPointProduct:
    product: str
    source_files: tuple[str, ...]
    rows: int
    output_path: str
    header: tuple[str, ...]


def discover_product_csvs(
    root: Path,
    product: str,
) -> tuple[Path, ...]:
    key = product.upper()
    files = tuple(
        sorted(
            path
            for path in root.rglob("*.csv")
            if key in path.name.upper()
        )
    )
    if not files:
        raise ValueError(
            f"no AppEEARS CSV files found for product {product}"
        )
    return files


def merge_point_result_csvs(
    files: Iterable[Path],
    *,
    product: str,
    output_path: Path,
) -> MergedPointProduct:
    paths = tuple(files)
    if not paths:
        raise ValueError("at least one source CSV is required")

    canonical_header: tuple[str, ...] | None = None
    rows: list[tuple[str, ...]] = []
    seen_rows: set[tuple[str, ...]] = set()

    for path in paths:
        with path.open(
            newline="",
            encoding="utf-8-sig",
        ) as handle:
            reader = csv.reader(handle)
            try:
                header = tuple(next(reader))
            except StopIteration as exc:
                raise ValueError(
                    f"AppEEARS CSV is empty: {path}"
                ) from exc
            if not header:
                raise ValueError(
                    f"AppEEARS CSV has empty header: {path}"
                )
            if canonical_header is None:
                canonical_header = header
            elif header != canonical_header:
                raise ValueError(
                    "AppEEARS product header drift detected for "
                    f"{product}: {path}"
                )

            for row_number, row in enumerate(reader, start=2):
                values = tuple(row)
                if len(values) != len(header):
                    raise ValueError(
                        f"row width mismatch in {path} line {row_number}"
                    )
                if values in seen_rows:
                    raise ValueError(
                        "duplicate AppEEARS data row across task files "
                        f"for {product}: {path} line {row_number}"
                    )
                seen_rows.add(values)
                rows.append(values)

    assert canonical_header is not None
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.writer(handle)
        writer.writerow(canonical_header)
        writer.writerows(rows)

    return MergedPointProduct(
        product=product,
        source_files=tuple(str(path) for path in paths),
        rows=len(rows),
        output_path=str(output_path),
        header=canonical_header,
    )
