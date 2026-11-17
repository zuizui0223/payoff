# PAYOFF-B V7 three-flyway source and information gate — 2026-11-17

**Conclusion: Original GPS data are source-verified, but the frozen V7 predictability × urgency interaction is NOT_ESTIMABLE from the presently accessible original-source set. No environmental q, goose phenological timing error, game payoff or fitness coefficient was fitted.**

## 1. Original Movebank archive recovered

Kölzsch et al. (2015), Journal of Animal Ecology, DOI 10.1111/1365-2656.12281, already identified predictive spring connectivity and associations with migration timing. This is prior art. PAYOFF's *separate* V7 focal question is whether independently sourced predictability q changes its association with realized arrival error according to predecision geometry-only route urgency U, as frozen on 2026-10-05 in docs/PAYOFF_B_V7_PREDICTABILITY_URGENCY_CONTRACT_20261005.md.

The Movebank Data Repository DSpace v7 public REST confirmed the exact DOI and archival ORIGINAL, TEXT bundle for **each** of the three flyways. All nine original archive files (GPS, individual reference CSV, and README for each flyway) were retrieved without credentials, checked against their publisher-provided MD5 and independently SHA256-hashed.

| Flyway | DOI | GPS fixes | Source-identified birds | Original tracking CSV SHA256 | Repository license |
|---|---|---:|---:|---|---|
| Greenland | 10.5441/001/1.5d3f0664 | 6,853 | 7 | 6e01f16ddbc3638ae14dcce6c0883f26c61ce6abd81dc1629c37bea4db75b18d | CC BY-NC 4.0 |
| Svalbard | 10.5441/001/1.5k6b1364 | 24,488 | 22 | e879874956afbb73a5e291d4ff87c17dafcc825dc2f04805a65690b21bdcd2e0 | CC BY-NC 4.0 |
| Barents Sea | 10.5441/001/1.ps244r11 | 21,102 | 15 | 9ce5865e8edf4b0546adf4e52f26d665510514219ea75e924fbb93cbeb6fb786 | CC0 |
| **Total** | | **52,443** | **44** | | |

**The published 40 complete spring migrations are a filtered cohort, not automatically equivalent to the 44 tracking IDs or 52,443 fixes.** Do not count fixes as independent visits or infer complete migratory journeys from file-row counts. Data are from public tracking rather than eBird.

Validated source runner: https://github.com/zuizui0223/payoff/actions/runs/44006580544 (5 tests and all nine archival bitstreams succeeded).

## 2. GPS records' actual date and location quality

Second original-source audit: https://github.com/zuizui0223/payoff/actions/runs/44007516123 (7 tests and 3 original CSV quality panels succeeded).

| Flyway | Valid latitude+longitude and source-calendar fixes | Bird×year series | At least ten March–July GPS fixes |
|---|---:|---:|---:|
| Greenland | 6,853 | 7 | 7 |
| Svalbard | 24,488 | 26 | 26 |
| Barents Sea | 21,102 | 35 | 34 |
| **Total** | **52,443** | **68** | **67** |

No duplicate source bird+timestamp events were found. The Greenland and Barents files are UTF-8, whereas Svalbard requires source-preserving CP1252 decoding. All archived timestamps are text without an embedded timezone offset. The audit parsed their original calendar dates without converting them to a guessed UTC or local timezone; hourly interpretation still requires the Movebank timestamp source convention to be checked against the README.

The GPS source has true event IDs, bird IDs, timestamps and original geographic coordinates. It does **not itself** define the 16 original generalized stopover regions or historical environmental q, nor does it contain individual breeding fitness measurements. Individual geographic tracks were not republished in this source audit, respecting CC BY-NC source licensing.

## 3. Original 30-year GDD spring-onset data still inaccessible

The 2015 paper explicitly lists **jane12281-sup-0001-SuppInfo.docx**, approximately 712.5KB, with Table S1 mean/SD of regional spring onset, **Tables S2–S7 paired stopover-region 1982–2011 spring-onset anomalies**, and Figures S1–S4. This is the relevant independent historical source for connectivity q; it must not be inferred from movement response data.

The exact publisher article pages used for source-linked supporting-file discovery both returned **HTTP 403** (no HTML anchor returned), so the original DOCX's **file bytes, source SHA256, 30-year numeric tables and route mapping were not accessed or verified**. Publisher API was not bypassed and no private URL was guessed.

Verified source-only gate: https://github.com/zuizui0223/payoff/actions/runs/44007837722, 3 tests passed; source result HOLD_PUBLISHER_SUPPLEMENT_HREF_UNAVAILABLE.

Published 2015 estimates of r and s can be discussed as prior-art descriptions but cannot be silently converted to a complete new individual-route q×U table. The complete source and original 16-region centroid/polygon crosswalk remain a strict prerequisite before any q×U outcome fit.

## 4. Separate tracking/fitness searches (no conflation)

- Brlík et al. 2026 Nature Ecology & Evolution (DOI 10.1038/s41559-026-03208-w): Zenodo paper concept 18175801/v3 record 19821864, four original tracking data CSVs checksum-verified. They record annual-cycle departure and arrival dates per bird, but **no intermediate GPS coordinates or independent cue and fitness measurements**. Their partial compensation and nonbreeding reset are published prior art. Source: docs/PAYOFF_B_GLOBAL_TRACKING_SOURCE_RESULT_20261117.md.
- Boom et al. 2023 (DOI 10.1111/1365-2656.14020), Dryad DOI 10.5061/dryad.m63xsj47x: official version 3 original GPS, nesting and mapping filenames/source SHA256 identified, but official documented whole-package GET returned **HTTP 401**. No original outcome rows downloaded or fitted. Source: docs/PAYOFF_B_GOOSE_GPS_FITNESS_SOURCE_GATE_20261117.md.
- PR #394 Little Owl derived BM and BM2 reconstruction matched 952/952 rows from fixed prey-class weights: prey-composition oracle prediction is an arithmetic identity, not independent ecological confirmation.

## 5. Frozen V7 primary admissibility and remaining work

The contract requires (a) ≥10 independently sourced transition q values; (b) ≥3 route positions; (c) ≥30 **actual** individual stopover visits; (d) ≥2 flyways; and (e) |corr(q,U)| below 0.90 across independent route transitions. U must use geometry-only remaining breeding distance, never realized transit duration or observed arrival mismatch. The exact q×U response and original 40 complete migration cohort must be joined from independent published source identifiers, not guessed.

Although the original article reported 16 generalized stopover regions, the independently verifiable source materials currently accessible here cannot certify the **route region pairs, numeric historical q, or sample inclusion needed for the V7 interaction**.

The current source gate state is:

- GPS_ORIGINAL=VERIFIED_3_FLYWAYS
- GPS_FIXES=52443
- TRACKED_IDS_BY_FLYWAY=44
- SOURCE_BIRD_YEAR_SERIES=68
- HISTORICAL_GDD_SUPPLEMENT=NOT_DOWNLOADED_HTTP403
- STOP_REGION_Q_CROSSWALK=NOT_VERIFIED
- V7_Q_X_ROUTE_URGENCY=NOT_ESTIMABLE_WITH_CURRENT_SOURCES
- BIRD_FITNESS_CAUSAL_EFFECT=NOT_IDENTIFIED

**Only remaining main-line source task:** obtain the actual published supporting-information DOCX or a separately sourced and independently verified original 1982–2011 GDD jerk onset table with the original region IDs, then validate the stopover-region GPS crosswalk with those source IDs before inspecting any V7 outcomes. Preserve this branch and source evidence as a DRAFT, unmerged. No positive result hunting by changing stage bins, environmental time windows or q source after seeing the response.
