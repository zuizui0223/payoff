# PAYOFF-B: Asian houbara decision-time climate-cue source eligibility

Date: 2026-10-08
Status: **ORIGINAL ZENODO FILES MD5-VERIFIED; FIVE-SHEET OOXML SCHEMA PASSED; FULL SOURCE-ROW / CHRONOLOGY AND ACTIONABILITY AUDIT PENDING**.
This is a candidate for a missing construct, NOT a new empirical claim and NOT another paper.

## Why it is a materially different source

The original PAYOFF-B V8 environmental connectivity paired range-derived source and destination greenup statistics; cue perception/behavior were not jointly observed. The Schindler Greenland-goose cohort has real repeated calendar-stage timing and subsequent energetics/reproductive outcome, but no independently measured predeparture distant forecast cue.

**Burnside et al. 2021 (PNAS; DOI 10.1073/pnas.2026378118)** followed 48 satellite-tagged Asian houbara bustards across spring and autumn, with the reported *spring departure cue* figure specifically covering **133 departures from 45 individuals**. Temperature over the eight days preceding spring departure was an individually repeatable cue, linked to population departure/arrival advances with variable spring temperature at breeding areas. The published observation is already strong: temperature cue and departure choice are connected within the original analysis, including a simulated wintering-site fidelity null. **Do not claim PAYOFF-B first identified local temperature as a departure cue**.

Primary data archive DOI: https://doi.org/10.5281/zenodo.4917565, Zenodo record ID 4917565, published in 2021.
Fixed publisher-listed data:
- MigrationData.xlsx, advertised 13.4 MB, MD5 183edf4bc6b3ba9946e4145589ff1c2d.
- PNAS_code.R, 23.9 kB, MD5 73050bfb758fd8d7a290913d80315ce7.
- XLSX workbook has sheets for spring and autumn departure/arrival, 1000 shuffled spring null datasets, comparison table, and field descriptions.

The archived data DOI/research article licenses study methods, but **a web search abstract is not evidence that the workbook has passed source audit**. Raw row counts, actual model fields, and dates must be verified from the bytes.

## Outcome-blind source-only gates

- Try only officially public Zenodo fixed-record endpoints, without authentication bypass, and record clear ACCESS HOLD if download fails.
- Compare raw bytes to publisher-listed MD5; an alternate authoritative URL may be tried without weakening digest validation.
- Inspect exact workbook sheet names, dimensions and first three header rows using ZIP/XML metadata; output only schema and source-manifest metadata. No individual migration outcomes, inferred cue effects or bivariate comparisons in source-gate run.
- Inspect original R-script header and references if file content retrieved; no published code relabelled as our independent method.
- Identify whether a **predecision** cue measurement is present (not a retrospective value at destination), whether departure and arrival dates are individual/year matched, and whether a route-stage checkpoint after departure is present.
- Biological positivity / data completeness gates remain NOT ASSESSED until actual source rows are materialized and temporal fields verified.
- Do not relax source MD5 or invent field meanings because a plausible biological inference would be attractive.

## Target construct and competitive explanations

If source passes, use the predeparture 8-day mean temperature, individual/year GPS departure and arrival to distinguish **static calendar + bird offset** from a temperature-cue rule in heldout individuals or years. However, *that direct comparison is substantially prior art in Burnside et al. (2021)*, and would initially be a replication/negative control.

A genuinely PAYOFF-B-specific ecological question would be whether **later cue updating, independently observed route-stage behavioral recourse, or actual fitness cost** alters the optimum between origin departure and breeding. The public Zenodo description promises departure/arrival and a shuffled null set but does NOT promise within-route checkpoint opportunities, direct adjustment costs, reproduction, consumer–resource pairing or fitness-optimal phenological targets. If these constructs are absent, **HOLD** on new causal ecological claims; do not dress an already-published temperature repeatability as new.

The source cannot be combined at the individual level with the 2018–2022 Greenland white-fronted goose spring/fitness archive, nor with the 2002–2017 Amaral bird phenology grids: populations, species, period and life histories differ.

## Decision rule

- Verified XLSX with individual-year cue and departure/arrival but no independent recourse or fitness: **CUE_BIOLOGY_REPLICATION_ONLY**, potentially a comparator panel for Paper 2, not an identifiable new mechanism.
- Verified within-route decisions plus cue chronology but no fitness: **CHECKPOINT_POLICY_TEST_POSSIBLE**, with explicit alternative fixed-calendar and individual-temperature-threshold models.
- Verified cue/decision/independent cost/fitness in same individuals: **ECOLOGY_FITNESS_TEST_CANDIDATE**, subject to prospective prespecification before opening those outcome fields.
- Unavailable raw data or incomplete schema: **ACCESS_OR_SCHEMA_HOLD**. Do not substitute paper aggregate numbers as source rows.

No preliminary ecological state, null tests or old theory theorem are reclassified by this screening.


## Actual first source gate outcome, no biological data fitted

Dedicated GitHub Actions **37773797850** completed successfully:
- MigrationData.xlsx 13,365,399 bytes, exact advertised MD5
  183edf4bc6b3ba9946e4145589ff1c2d, SHA256
  5aebe52763d2a72ba5b05f6ffa434fc216c885305322eecc194d0e06ee961729.
- PNAS_code.R 23,948 bytes, MD5
  73050bfb758fd8d7a290913d80315ce7.
- OOXML workbook exactly five sheets:
  Explanations (A1:K34),
  spring_migration_data (A1:O133),
  autumn_migration_data (A1:N153),
  repeatable_comparisons (A1:D43),
  null_spring_dataset (A1:N132001).
- Spring header specifically lists departure/arrival dates, latitude, wind,
  day length, departure/arrival temperature and annual breeding-ground
  reference temperature. It does NOT list waypoint decision times, actual
  physiological route recourse, survival or individual reproduction.
- Null spring sheet has 132,000 declared data rows under one header,
  consistent with 1,000 shuffles of 132 observations, but that is a
  **schema implication only**, not proof of original numeric support.
- In the paper, Figure 2 explicitly reports 133 spring departure events
  from 45 birds; the Excel spring dimension includes just 133 rows
  *including a text header*. The full row count and reason for any mismatch
  require independent checking. Do not silently reconcile the counts.

No new temperature or arrival regression was fitted; the direct departure
temperature cue findings are Burnside et al.'s original discovery.

The more discriminating second source-only plan was registered separately
in docs/PAYOFF_B_HOUBARA_EVENT_TIME_AND_RECOURSE_SOURCE_CONTRACT_20261008.md,
with the parser and CI on this PR. Its dedicated run must be completed
before interpreting event support.
