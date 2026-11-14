# PAYOFF-B Japan JMA temporal coordinate crosswalk — real source result

**2026-11-14 | PR #347 | real JMA phenology archive × original 146-byte smaster.index**

Official fixed-width metadata format: https://www.data.jma.go.jp/stats/data/mdrr/man/smasterindex_format.pdf . Original station-history archive: https://www.data.jma.go.jp/stats/data/mdrr/chiten/meta/smaster.index.zip .

## Executed audit

GitHub Actions run https://github.com/zuizui0223/payoff/actions/runs/43599848876 — 61 tests passed and original data join succeeded.

- JMA phenology original CSV: 65 event files, **160,367** calendar-valid event-date cells, not yet screened by biological `rm` meaning.
- JMA station-history source: **3,046** records across **168** numeric station IDs.
- Numeric station-ID overlap: **102/102** phenology station IDs found in station-history source.
- Source-history records valid on the actual biological event date: **141,562** (88.3%), each with exactly one metadata record.
- No source-history record valid on the biological event date: **18,805** (11.7%). Do not silently backfill with nearest or modern station location.
- Ambiguous multiple valid metadata records: **0** in this run.
- **64/168** metadata station IDs have multiple distinct coordinate pairs across history. This is a station-history statistic, not necessarily 64 relocations among the 102 phenology stations; some changes may be metadata corrections.

## Source-specific interpretation and limits

- Official byte positions: ID 1–3; latitude 37–42; longitude 43–49; observation valid-from 65–72; valid-through 73–80. End sentinel `99999999` means ongoing.
- Example official `452490` = 45°24.9′ = 45.415° latitude; longitude `1414070` = 141°40.7′ = 141.678333...°.
- The original source includes a non-Japan meteorological station; parsing the whole source must not assume all station coordinates lie within Japan. Coordinate datum is not independently certified WGS84 by the station-history format alone.
- The **18,805** unmatched event rows have not been decomposed into pre-1961 observations, gaps, or other temporal mismatches. The historical metadata file explicitly starts in 1961; older phenology events are therefore expected to be partially unmatched, but this explanation has not been quantified.
- The join establishes source-temporal station location eligibility, **not** successful daily temperature/rainfall/humidity/wind/NDVI/biomass retrieval or validated `rm` biological quality codes.
- No ecological effect estimates or heldout predictions have been fitted.

## Next gate

Decompose unmatched event rows by year and taxon; certify datum or carry location uncertainty; then obtain original JMA weather daily data on the **same** station-event-years, with independent per-variable quality and availability masks. NDVI and measured prey/plant biomass remain separate data sources and measurement types.
