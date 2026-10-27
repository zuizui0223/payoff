# PAYOFF-B: all-parent Movebank taxon / sensor source registry

2026-10-19. Purpose: turn the full published Movebank DOI census into
**publisher-grounded taxonomic and measurement coverage** for genuinely
database-wide ecological hypothesis testing.

Data source: https://datarepository.movebank.org/
- The frozen stage-1/2 DOI census identified 446 Movebank parent package
  candidates. The 10.5441 DOI prefix includes other publishers and must not
  be interpreted as 2,080 independent Movebank studies.
- DataCite titles/abstracts produced 76 T1 cue-and-decision *text hints*.
  Crucially, bat papers can be included by that broad text screen.
  Therefore no taxonomic or cross-species conclusion can use T1 as a verified
  bird sample.

## Complete public item metadata procedure

For every (not just top-ranking) parent DOI:
1. Use its original Movebank HTTPS package landing URL to resolve the
   repository's own DSpace item UUID.
2. Fetch only /server/api/core/items/{uuid}, never event data or private
   tracking accounts.
3. Validate available dc.identifier.doi against the DataCite parent DOI;
   label missing metadata separately.
4. Extract published dwc.ScientificName, sensor.name, mdr.animal.count,
   mdr.location.count and mdr.study.id without deducing missing values from
   titles or abstracts.
5. Keep unresolved parents in the full output and mark incomplete census
   status; do not silently drop them or reclassify them as absent taxa.
6. Identify repeated Movebank Study ID and previously published paper DOI
   families as *potential dependence*, not independent replication.
7. Report source metadata completeness, unique taxon strings and sensor
   distributions; no individual animal identity, GPS or fitness outcome
   may be downloaded at this stage.

The 446 package DOIs are NOT independent study replicates and the sum of
published animal/location counts is not a population sample size. Metadata
taxon strings do not automatically imply one-to-one taxonomic resolution,
absence/presence or comparability of seasonal activity windows.

The next biological admission requires event timestamps and actual route
quality for a sufficiently diverse set of taxon-confirmed accessible
packages; spring information must have been available *before* a tracked
migration decision. Fitness outcomes are a separate gate.

Executable:
- scripts/build_movebank_taxon_sensor_registry.py
- tests/test_movebank_taxon_sensor_registry.py
- .github/workflows/payoff-b-movebank-taxon-source-census.yml
