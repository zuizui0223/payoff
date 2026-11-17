# PAYOFF-B global tracking source admission — 2026-11-17

**Status: exploratory source/schema audit only. No new predictive-connectivity × remaining-opportunity coefficient inspected or fitted.**

## Source and current novelty boundary

Brlík et al. (2026), *Nature Ecology & Evolution*, "Temporal links in avian migration schedules across the annual cycle", DOI 10.1038/s41559-026-03208-w, first published 2026-10-27. Published work already documents 2,324 tracked individuals / 83 species, temporal links across seasonal stages, partial migration-duration compensation for late departures, and a temporal reset at the nonbreeding grounds. PAYOFF-B **cannot** claim those mechanisms as new.

Public published source is Zenodo DOI 10.5281/zenodo.18175801 (the paper's Data Availability Statement); Zenodo version v3 is displayed at https://zenodo.org/records/19821864. Source-version linkage **must be confirmed from the official record metadata**; do not assume a versioned record is interchangeable. Never infer ecological effect from a dataset file title, file preview, or publication abstract. Initial source preflight retrieves the official Zenodo API metadata for both identifiers and verifies exact file checksums before scanning headers.

This dataset is candidate **tracking** evidence, rather than eBird occurrence-data output. Whether the original files provide true individual location/stage identifiers, date/timing and independent pre-commitment environmental cues is unknown until the source schema check. Do not use datasets based on eBird occurrences. No use of user-opposed eBird input or TinyFish automation.

## Scientific question and hard admission

The remaining PAYOFF-B hypothesis is **not** whether late migrants compensate. It is whether **independently measured forecast reliability of later seasonal conditions × the ability to revise departure/stopover decisions** predicts *where compensation is incomplete*. Define the following separately before outcome analysis:

- Cue at departure: observed local temperature/phenology at departure, measured prior to the decision;
- Future environment: temperature/vegetation/food at destination later, measured independently of bird movement;
- Reliability q: historical or pre-focal-window correlation of cue and future state, calculated without current-year or bird timing outcome;
- Recourse/r: number/availability of downstream revisable stages or independently sourced opportunities, not inferred from realized stopover duration (a potential dependent variable);
- Observed correction and ecological response: individual event dates, travel duration and arrival phase. Breeding fitness outcomes are not presumed present.

**Admission only if** the original files have unambiguous individual ID, species, sampled year and stage events, date resolution, location or geographical unit linked to events, and ≥2 stages per individual. A separate environmental-source match and replicates across years are required before a q × recourse model. Temporal covariation without those elements is not adequate. Freeze source windows and source re-use rules before opening effect coefficients, not after.

## Stop rules and falsification

- For each official file, record Zenodo version, basename, byte length, MD5/SHA as advertised, downloaded SHA256, schema, first 3 rows of non-sensitive columns, row count, and candidate event/individual/location fields. Fail-close on size/digest mismatch or unauthorized URL.
- Never equate missing ecological response with zero or infer missing GPS coordinates from route-stage labels.
- Preserve 2026 global annual-cycle paper as prior art for partial compensation and reset; no redundant publication on these endpoints.
- If files contain only timing summaries without stage geography or pre-decision cues, record **NO_GO_DIRECT_INFORMATION_TEST**, even if the public source is valid. Then a different GPS + environment dataset is required.
- Avoid equating standardized timing repeatability with "inflexibility" or a fitted seasonal timing slope with measured information valuation.
