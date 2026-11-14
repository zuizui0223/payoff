# JMA national multi-taxon census: first independently reconciled panel

**2026-11-14 | actual original JMA public archive read by GitHub Actions; still NOT a climate/NDVI biological fit**

Source: `https://www.data.jma.go.jp/sakura/data/ruinenchi/ruinenchi_all.zip`. Exact archive SHA256 `0ca3e39524918d61d85f4c6424c4b0925613af8100daf9880a74cfdcce2b1c70`. Original official HTML event labels resolved for all 65 files.

## Reproduced results

- 65/65 files recognized as wide JMA station-by-year tables, including the nine initially misread due to trailing summary-year columns.
- 160,367 valid-calendar event-date cells independently reproduced by a **second event-level panel parser**. This is **not** a quality-screened sample or 160,367 independent biological replicates.
- Provisional original event-file categories: 3 amphibian files / 4,490 cells; 6 bird / 18,598; 15 insect / 44,694; 41 plant or unclassified / 92,585. Categories are source-label heuristic, not taxonomic name resolution.
- Original `rm` codes on these 160,367 calendar-valid cells: 8=116,879; 9=35,758; 6=4,626; 7=1,957; 3=1,103; 4=44. **Code semantics have not yet been source-certified.** Do not treat these as quality ranks or discard 8/9 without official documentation.
- Duplicate event keys are rejected per source-file × station-ID × year. Leap dates are validated with actual calendar years. Trailing source summary columns are not treated as annual observations.
- CI: https://github.com/zuizui0223/payoff/actions/runs/43595663483 (16 offline tests passed; original source read and aggregate receipt succeeded). The exact source receipt is uploaded as a GitHub Actions artifact, not copied into main or claimed to be independent biological data.

## Current ecological identification limit

The panel presently has `source_file, event_label, station_id, station_name, year, event_date, day_of_year, rm_original_code`. **It has no independently source-certified station coordinates, effort, local air temperature, MODIS/VIIRS NDVI or validated rm interpretation.** Thus a temperature coefficient, NDVI incremental predictive score, climate-trend attribution or comparison of animal cue-use thresholds is not estimable yet from this admitted panel.

## Next executable source gate

1. Verify official JMA station identifier → WGS84 station coordinate table, retaining station relocation/ID changes, and exact original `rm` code meanings. Join on station IDs, not station names. If official quality meaning cannot be verified, keep code as a stratification factor and report sensitivity by code.
2. Fetch original daily temperature or ERA5-Land for matched station-year with a fixed pre-event time window; separately source-verify gridded NDVI and its QA/snow mask.
3. Predeclare heldout-year and heldout-site temperature-only versus temperature+NDVI comparisons for each source event type; do not use future environmental values for a pre-event forecast.
4. Treat JMA's animal-phenology observation termination/protocol changes as observation-process censoring; do not interpret zero after cessation as delayed/no phenology.

This is a reproducible real-data ingestion and audit result, not yet evidence that NDVI predicts amphibian or bird phenology.
