# PAYOFF-B V7 Kölzsch 2015 original Movebank stopover tracking — source admission

Date: 2026-11-17. This follows the **frozen prospective V7 predictability × route-stage urgency contract** already on repository main since 2026-10-05: docs/PAYOFF_B_V7_PREDICTABILITY_URGENCY_CONTRACT_20261005.md. That contract specifies main response absolute timing error relative to regional spring, source-destination predictability q from an independent 30-year spring series, geometry-only urgency U, and main interaction q×U. It has never authorized estimating q or U from observed goose timing.

**This step is metadata/data source admission only. The focal q×U effect remains UNOPENED.**

## Official public archival source

Kölzsch et al. (2015), *Journal of Animal Ecology*, DOI 10.1111/1365-2656.12281. Already reported predictive spring connectivity differences, better timing in more predictable stages, three flyways and 40 spring migrations. These are **prior art**, not novel PAYOFF results.

Archived Movebank Data Repository DOIs from the paper:
- Greenland: 10.5441/001/1.5d3f0664
- Svalbard: 10.5441/001/1.5k6b1364
- Barents Sea: 10.5441/001/1.ps244r11

Movebank Data Repository is the certified formal archive (distinct from Movebank live study permissions). The current repository uses public DSpace 7 REST at https://datarepository.movebank.org/server/api; discovery GET /discover/search/objects is documented by DSpace's official REST contract. Query exact DOI, verify the found item embeds the same DOI, inspect license metadata and its publicly linked file bundles/bitstreams. No credential, API token, or private/live Movebank API access.

## Source admission and eligibility

- Record every DOI's resolved archival item title, handle and license, repository file names, byte sizes, checksum and download links (follow only official returned links); no "name-only" or label-only species matches.
- From public GPS files only, identify individual IDs, exact times, coordinates, sampling units and the three flyways. No ecological output fit before independent source spring phenology q and route geometry U are recovered and source permissions/conditions recorded.
- The old paper supporting tables of historical GDD spring onset/correlation must be source verified. **Do not** derive q from stopover arrivals; do not infer urgency from realized speed or dwell duration.
- Admit V7 only with ≥10 independently estimated stopover transitions, ≥3 route positions, ≥30 individual stops, ≥2 flyways and |cor(q,U)|<0.90 as frozen. Otherwise output V7_PRIMARY_TEST=NOT_ESTIMABLE.
- Stop when the API cannot find or license/serve original data; neither paper abstract nor synthetic route stages is a substitute. No use of eBird-derived occurrence data.
