# PAYOFF-B — original departure→routing→landing source-admission gate (2026-11-19)

**Source-only, before any new empirical fit; post-publication exploratory.**

Rüppel et al. (2023), *Royal Society Open Science* 10:221420, DOI [10.1098/rsos.221420](https://doi.org/10.1098/rsos.221420). Original supporting collection [Figshare DOI 10.6084/m9.figshare.c.6403996](https://doi.org/10.6084/m9.figshare.c.6403996), collection ID **6403996**. The authors already reported weather effects on **departure, routing and landing** in long-distance migratory songbirds. None of those effects are a novel PAYOFF result.

## Why this data source is being screened

PAYOFF-B requires a three-step longitudinal measurement: (a) an environmental cue actually available *before* departure, (b) a subsequent movement choice and downstream correction opportunity, and (c) final state mismatch or fitness. Rüppel et al. report hourly weather at sunset before departure and weather at flight start/end, observed routing, and flight interruption/landing, which is closer to the first two steps than prior 2024 Greenland geese. **There is no identified individual breeding payoff, future-destination information-quality estimate, or Bayesian cue acquisition in the published paper.**

## Admission checks locked before downloading source event tables

1. Read only Figshare's public REST API collections/6403996/articles and the original article metadata of returned IDs. Preserve provider DOI, published date, license, original file names/sizes/digest types.
2. Only original provider file URLs from the returned metadata are eligible. Download at most 12 *public* CSV/TSV/TXT/JSON/ZIP candidates, each capped at 8 MB before and after transfer; **no PDFs**, tracking coordinates, restricted files, credential bypass, user agreement acceptance or alternate mirrors. If the original API refuses access, record that explicitly.
3. In eligible small original tables or ZIP members, report schema and aggregated row counts, and only candidate identifier/timestamp/decision/weather field names. **Never export raw bird identifiers, records, locations or response values.** A field name containing ID is not proof of common identity across source files.
4. A future 3-decision analysis requires author-documented **same-individual** linkage of all three decisions (departure at-risk nights, actual route, subsequent landing or continuation), properly timestamped measured weather **before** each decision, **≥30 tracked birds with linked departure/route**, and **≥10 birds with observable subsequent landing/interruption**. These are practical data-admission thresholds, not power guarantees. Until verified, report SOURCE_JOIN_NOT_ESTIMABLE and do not fit a coefficient.
5. Even if admitted, this source alone does not measure actual cue belief about destination spring, independent controller/recourse capacity, net waiting cost D_eff, interacting partner timing, or breeding success. It could only offer source-faithful observational sequential-decision diagnostics, not a direct proof of PAYOFF-B information-deadline theory.
6. Do **not** relabel existing paper's weather/departure/routing/landing results as new, and do not count articles with overlapping tracked birds as independent replication.

Original alternative candidate: 2026 Sora Motus [Dryad DOI 10.5061/dryad.msbcc2g9k](https://doi.org/10.5061/dryad.msbcc2g9k) declares a dated daily departure-risk table with weather but later route join not yet verified; 2025 Golden-winged Warbler [Dryad DOI 10.5061/dryad.qbzkh18w5](https://doi.org/10.5061/dryad.qbzkh18w5) has departure and subsequent Motus detections but departure–speed association is already published. They are NOT counted as successfully accessed source data here.

## Required fail-closed statuses

- SOURCE_METADATA_ACCESS_BLOCKED: official Figshare collection or article API unavailable.
- PUBLISHED_SUPPLEMENT_WITHOUT_ORIGINAL_TABULAR_EVENTS: only PDF/figures or aggregated coefficients, no bird/time table.
- ORIGINAL_TABULAR_SCHEMA_FOUND_ID_JOIN_UNVERIFIED: at least one original tabular data file with event columns but no author-validated join of the three decisions.
- CANDIDATE_SEQUENTIAL_SOURCE_METADATA_ONLY: multiple event tables/ID-like fields, but actual record-level n and timing remain uncertified.
- SOURCE_SCHEMA_ELIGIBLE_ONLY_NOT_FITTED: an actual individually joined, properly timed source exists and independent support minima pass (requires original codebook verification beyond generic column-name heuristics).

The source downloader must not substitute invented data. Store a source metadata/count receipt and tests only in a separate Draft PR; no original bird records or eBird occurrences. Frozen V2/V7 and main unchanged.
