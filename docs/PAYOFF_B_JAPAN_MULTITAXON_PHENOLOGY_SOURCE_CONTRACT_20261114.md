# PAYOFF-B Japan multispecies climate–vegetation–phenology census

**2026-11-14 | new exploratory national study; source discovery + executable JMA archive census, not an effect estimate**

## Source identity and observation-type firewall

1. **JMA historical biological-season observations**: official per-event annual CSV and one ZIP, https://www.data.jma.go.jp/sakura/data/download_ruinenchi.html . Includes first song of Japanese tree frog, first appearance of pond frog, first songs of bush warbler/cuckoo/skylark, first arrival of swallow, insect first song/appearance, plant first bloom/leafing. The JMA animal programme was greatly reduced/ended in 2021; the 2021 boundary is **a measurement-protocol discontinuity**, not an inferred biological disappearance. JMA first song is the first detected vocalization by the observer, not a standardized chorus onset or population abundance.
2. **MOE Monitoring Sites 1000 satoyama**: https://www.biodic.go.jp/moni1000/village.html . Frog outcome is **red-frog first egg-mass timing / egg-mass counts**, roughly every two weeks in winter, NOT frog first song. Birds are standardized breeding/wintering route counts (six surveys per season), NOT automatically first arrival or song. Butterflies and fireflies have count surveys with different effort schedules. These are a separate observation process and must never be pooled as if the same event variable.
3. **MOE Monitoring Sites 1000 alpine**: https://www.biodic.go.jp/moni1000/findings/data/ . Plant flowering camera/visual records, air/soil temperature, butterflies and bumblebees; inspect individual release schemas before attempting within-site guild mismatch.
4. **MOE Monitoring Sites 1000 forest**: tree stems, litter/seed fall and birds; quantity and phenology are separate axes. Abundance is not biomass without calibration.
5. **NIES citizen phenology**: https://adaptation-platform.nies.go.jp/ccca/monitoring/phenology/ , a possible newer first-song/first-sighting stream with volunteer-observer changes; do not append to JMA historical station series as identical protocol.

## First pass preregistered outcome families

- Bird first song vs first appearance/arrival; migrate vs resident as independently sourced life-history strata.
- Amphibian first call/first appearance vs red-frog first egg-mass, **different biological events**.
- Insect first song/first appearance vs butterfly abundance and firefly count peaks.
- Plant first bloom/leafout vs alpine flowering intervals.
- Forest leaf/seed production and bird abundance: *resource quantity* but not automatically same phenological response.

For each original record retain `dataset_id, source_file_sha256, species, event_type, station_or_site_id, observation_date, year, latitude, longitude, effort/protocol, missingness_code, quality_flag`. JMA ZIP schema is **not assumed**: source audit CI records exact first rows, encoding and file checksums before building a parser. For MOE site coordinates, respect disclosure restrictions; do not publicly export precise sensitive locations.

## Climate/NDVI exposure windows: prospective hypotheses

- Temperature: daily 2-m air temperature, prior 7/30/60-day mean and growing degree days with a fixed biological baseline, precipitation and snow where relevant. Source options JMA station climate and ERA5-Land; distinguish gridded from station measurements.
- NDVI: MODIS Terra/Aqua or VIIRS time series with QA/cloud/snow masks, green-up onset, peak date, peak amplitude and integrated vegetation greenness. NDVI is a vegetation proxy, **not direct prey or total biomass**.
- Do not use vegetation or temperature observed **after** the first-song/first-appearance event as a predictor in a forecasting claim. For ecological response models, retrospective full-season phenology can be used as a separate concurrent association, clearly labelled nonforecast.
- A first song/appearance day is detection-limited: observer effort, weather-dependent singing activity, protocol changes, urbanization and species range shifts can shift observed first events independently of physiological timing.
- Two-week frog egg-mass visits imply interval-censored first spawning: event occurred between previous negative and first positive survey, not necessarily on the survey date.

## Statistical execution order

1. **Source census**: download original JMA ZIP; checksum; classify original file types; report exact encoding/header, year/station/event coverage and missingness. No effect estimate.
2. **Observation harmonization**: verify source IDs and dates; leap-year and year-wrap checks; event-type-specific censoring and JMA 2021 protocol break; no imputation of discontinued taxa as zero events.
3. **Temperature benchmark**: per species/event/site fit temperature-only baseline using prior-season windows and site/year effects; heldout whole years and sites. Include nonlinear/threshold response and varying slopes.
4. **NDVI incremental test**: compare temperature-only with temperature + independently reconstructed NDVI metrics on exactly matched event/site/years, with QA/season/latency guards. Report heldout log predictive score or absolute-day error and improvement uncertainty at **site and year** blocks.
5. **Cross-taxon synthesis**: report effects within amphibian/bird/insect/plant groups, separating first-call vs first-appearance vs breeding vs flowering. Hierarchical meta-regression on comparable standardized slopes only after observation-process harmonization; site, species and climate-year dependence retained.

**Falsifiable contrast:** Does NDVI improve prediction of biological timing **beyond local temperature**, and is the incremental information stronger for taxa with resource-dependent life cycles than for taxa whose first-song detection responds mainly to short-term weather? This is a hypothesis, not a result.

## Already published source benchmark

MOE satoyama summary reports Japanese brown-frog first egg-laying advances around **5–10 days per decade**; this is an external published benchmark, not a PAYOFF replication. Source: https://www.nacsj.or.jp/wp/wp-content/uploads/2024/10/01_moni1000_4th_report_summary.pdf

## Executable first audit

`python scripts/payoff_b_japan_phenology_source_census.py --output outputs/japan_phenology/jma_archive_inventory.json`

Workflow: `.github/workflows/payoff-b-japan-phenology-source-census.yml`; it reads the JMA ZIP using GitHub-hosted network, records source archive/file SHA256 and first rows only, and uploads a **schema-only** receipt. Original raw observations are not redistributed. If download fails, report source-access failure rather than fabricating sample counts or NDVI effects.

**No empirical temperature coefficient, NDVI coefficient, taxon comparison, or cross-guild mismatch estimate has been fitted in this commit.**
