# Japan-wide climate/NDVI join: source and admissibility status

**2026-11-14 | source discovery and code implemented; no climate raster values joined yet**

## Original sources newly verified

- JMA official *ground meteorological observation station metadata history* and *statistical discontinuity* files are available from https://www.data.jma.go.jp/stats/mdrr/man/kansoku_gaiyou.html . The page explicitly says latitude, longitude and station relocation/history are available, with format tables updated on 2026-08-20. **The phenology three-digit station ID has NOT been shown to be the same identifier as the ground-meteorology metadata ID**. A source-certified crosswalk is mandatory; joining on name alone is disallowed.
- JMA original biological season observation guide and archived events: https://www.data.jma.go.jp/sakura/data/index.html . Some historical event definitions use *observation years* that can cross calendar years; a calendar-year date constructed from the CSV header is provisional until event-specific year conventions are verified.
- JMA first-call and first-sighting definitions: https://www.jma-net.go.jp/daitou/shosai/kansoku/kansoku_seibutu.html . First call is first *heard* vocalization; first sighting is first *seen* individual. Neither is a detection-effort-controlled physiological or population-onset measurement. The same page explicitly documents animal observation terminations at 2020-12-31 for several focal taxa.
- JMA official guide for historical cumulative-table symbols is linked as '生物季節観測累年表の見方' on the official phenology index. The source-specific `rm` code semantics have not been transcribed/verified. Generic meteorological quality-flag documentation **cannot** be substituted as evidence for these biological-event `rm` codes.
- JMA annual CSV original archive SHA256 `0ca3e39524918d61d85f4c6424c4b0925613af8100daf9880a74cfdcce2b1c70`; 65 event files; 160,367 calendar-valid source cells; independent row parser confirms count; valid-date `rm` counts 8=116,879, 9=35,758, 6=4,626, 7=1,957, 3=1,103, 4=44. Source-audit workflow https://github.com/zuizui0223/payoff/actions/runs/43595663483 .

## Executable environment admission

`src/japan_phenology_environment_gate.py` validates each event × station × year row has:
- a source-certified historical WGS84 station coordinate valid in that observation year, with independent metadata identifier;
- temperature mean and number of valid days from a window ending **before** the observed event date, with at least 90% coverage;
- NDVI value, named product version, positive pixel area, at least 80% QA-valid fraction, from a window ending **before** the event date;
- actual source identifiers for station, temperature and NDVI, valid event-date/DOY/year consistency, and unique biological event key;
- at least five observed years per event/station series before any predictive comparison.

This is an **admission test only**. Tests use explicitly labelled synthetic inputs; passing does not mean JMA temperature or MODIS NDVI has been acquired. It cannot establish causal information use or fitness.

## Next empirical work

1. Download and parse official JMA station metadata history, resolve the phenology station ID crosswalk, audit relocations and observation-year conventions; record matched/unmatched station-years.
2. Download source-faithful temperature and NDVI with product/QA provenance for **the same** matched station-year, avoiding future information for forecast analyses.
3. Fit heldout-year and heldout-site temperature-only versus temperature+NDVI, stratifying by event and provisional `rm` code until meanings are certified. Cross-taxon heterogeneity is exploratory until the observation processes are harmonized.

**No temperature/NDVI effect size is claimed here.**
