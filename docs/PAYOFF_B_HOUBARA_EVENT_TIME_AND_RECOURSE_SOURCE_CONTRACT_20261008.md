# PAYOFF-B Asian houbara: workbook identity, event-time and actionability gate

Date: 2026-10-08.
Status: SOURCE-ONLY DESIGN FIXED BEFORE READING THE ACTUAL SPRING RECORDS.
This is a post-publication source audit, NOT a prospective biological finding.

## Original source

Burnside et al. (2021), PNAS doi:10.1073/pnas.2026378118. Zenodo record 4917565. Source file MigrationData.xlsx MD5 183edf4bc6b3ba9946e4145589ff1c2d, PNAS_code.R MD5 73050bfb758fd8d7a290913d80315ce7. Both were byte-verified in GitHub Actions 37773797850; no animal data used then.

Five original workbook sheets and headers were recovered. The primary spring sheet has columns:
migration.period, burst, id, sex, departure.latitude, departure.date, arrival.date, Year, departure.julian, arrival.julian, wind.velocity.NS, daylength, departure.temperature.C, arrival.temperature.C, annual.ref.temperature.breeding. There is NO route-stage checkpoint field, cue time series, realized action cost, breeding reproductive success, or repeated joint partner-phenology outcome among these fields. The supplemental 1000 shuffled-data worksheet is an author-defined comparison, not individual GPS full route tracks.

## Audit targets and strict interpretation

1. Parse **all actual rows** (not the worksheet dimension alone) in spring_migration_data, autumn_migration_data, repeatable_comparisons and Explanations. For the giant 132000-row null_spring_dataset, use declared size and header only, never fit outcomes.
2. Confirm source row-level presence, uniqueness and completeness for (id,Year,departure.date,arrival.date). Report actual record count, distinct individual identifiers, years covered, duplicate keys, invalid/missing departure or arrival, and nonpositive event date order. Never invent a missing record.
3. Critically, the 2021 paper's Figure 2 caption says 133 spring departures of 45 houbara; the XLSX metadata shows spring_migration_data!A1:O133, which would have **132** data rows if row 1 is a header and bounds reflect actual records. Do not assume the discrepancy is real until counting populated row nodes. If 132, preserve discrepancy and do not silently relabel source as a 133-event sample.
4. Read the Explanations tab for author-provided field semantics (headers and prose). Report *only* variable definitions and schema; do not use original biological results as independent confirmation.
5. Inspect PNAS_code.R for whether it operates on an event-time-only table, uses daily predeparture risk sets or within-route telemetry, and what the author nulls actually condition on. Emit a bounded, verbatim relevant function/keyword list; no biological coefficient new estimate.
6. Distinguish an 8-day temperature summary **anchored to an observed departure date** from a daily risk-set/hazard design with all potential no-departure decision days observed. The former alone cannot identify causal decision triggers from temporal associations. The original paper's shuffled timing null is relevant prior art and must not be ignored.
7. Distinguish arrival.temperature.C (environment at realized destination arrival) from an externally established reproductive optimal spring date or partner co-occurrence target. Arrival thermal consistency does not equal individual fitness gain.
8. Data are **not fit** to a new regression or recombined with the 2018–2022 Schindler Greenland goose individual-year fitness cohort or the 2002–2017 Amaral gridded bird species-cell data.

## Data admission decisions

- SOURCE_VALIDATED_EVENT_DATA: byte digest and rows intact, origin cue and departure/arrival fields identifiable.
- SOURCE_INSUFFICIENT_FOR_CHECKPOINT_RECOURSE: no dated intermediate decisions nor independent available action range.
- SOURCE_INSUFFICIENT_FOR_FITNESS_AND_MULTI_PARTNER: no individual survival/reproductive success and no jointly observed partner phenology.
- MIXED/UNRESOLVED: missingness, duplicate keys, inconsistency of the purported 133-event figure or underdefined temperature time periods must be shown explicitly without retrospective sample selection.

No new paper or causal claim follows source admission. Original Burnside et al. results on temperature-cue repeatability and spring arrival thermal compensation are prior art.

**Outcome-blind source gate:** no new cue regression, model selection, Bayesian posterior decision rule, climate response slope or survival endpoint can be fitted as part of this audit.
