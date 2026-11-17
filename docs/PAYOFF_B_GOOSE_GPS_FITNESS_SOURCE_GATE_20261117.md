# PAYOFF-B second GPS→fitness source admission: Boom et al. barnacle goose

Date 2026-11-17. **Source and field availability gate, no new effect fit.**

## Why switch from global annual-cycle event summaries

The Brlík et al. 2026 83-species annual-cycle Zenodo records (concept DOI 10.5281/zenodo.18175801, v3 19821864) provide bird IDs, species, seasonal event dates, distances and derived durations but no intermediate stopover coordinates, resource state, or individual fitness. They cannot establish an independent predeparture cue–destination link or remaining stopover actionability. Their partial migration compensation and winter reset are published prior art, not new effects.

Choose an independently sourced GPS + breeding-outcome system: Boom et al. (2023), *Journal of Animal Ecology*, DOI **10.1111/1365-2656.14020**, original Dryad DOI **10.5061/dryad.m63xsj47x**. Authors tracked 96 female barnacle geese, recovered 154 migration tracks and analysed 140 valid breeding-location tracks from 2008–2020. They **already reported** local onset of spring predicting breeding propensity/nest success better than arrival-vs-spring mismatch; those known local outcomes are prior art. The source reportedly includes nest location and raw GPS/accelerometer records.

## Source and methods

Use only official public Dryad API (GET) for metadata and the **documented** download-full-dataset route. No private data, eBird-derived occurrences, API key guessing, credentials or third-party relays. Record dataset DOI, version ID, official CSV manifest file names/sizes/source SHA256 if provided. Inspect exact bytes from the official dataset-package ZIP, verify original each CSV against official metadata digest, and write source headers and row-grain/missingness. If the whole-package download also returns HTTP 401 or an HTML login page, fail-close NO_GO without more endpoint guessing.

## Direct test gate

Any new test of cue information × route urgency × breeding payoff needs:
- identifiable female and **individual×year** key across GPS/migration and breeding;
- event/coordinate information before migration departure and at consecutive staging sites, not only calendar year of breeding;
- exact breeding date and nest outcome, with baseline reproduction attempts and source exclusion criteria;
- independently observed temperature or resource signal **prior to** departure, and later realized spring state. No use of the breeding outcome or destination condition to define a predeparture cue;
- externally defined route-stage urgency / remaining geometric opportunity independent of the observed speed or delay response;
- no unexamined duplicated individuals, calendar-day misalignment, mixing residents with Arctic migrants, or reuse of published Kölzsch 2015 tracks as independent animals.

Only source/missingness admission in this step. Do NOT fit any same-source treatment coefficient or write a new information theory support claim. If no per-stage timing or independent environment forecast exists, record **NO_GO_DIRECT_INFORMATION_CUE_X_RECOURSE_FIT** even when original GPS and reproductive outcomes download successfully.

## Prior-art boundary

Boom et al. already established spring-onset and latitude interaction with breeding propensity/success. Kölzsch et al. 2015 already quantified predictive spring connectivity along three barnacle goose migration routes. Brlík et al. 2026 already documented partial temporal compensation and annual-cycle reset. A new contribution cannot be claimed from reproducing any of these.
