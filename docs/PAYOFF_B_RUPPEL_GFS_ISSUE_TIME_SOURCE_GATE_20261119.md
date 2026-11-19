# PAYOFF-B Rüppel 2019–2021 historical issued-forecast availability and time gate

**Freeze 2026-11-19. NO weather forecast data or biological response has been opened.** This is a source-admission contract following the verified original bird×at-risk-night→flight→landing data linkage in [PR #410](https://github.com/zuizui0223/payoff/pull/410).

## Why original observed weather is not enough

Rüppel et al. (2023), [DOI 10.1098/rsos.221420](https://doi.org/10.1098/rsos.221420), recorded bird behavior and actual physical meteorology on autumn European coastal stopovers, 2019–2021. Their original Figshare RData source was SHA256 authenticated and genuinely links 1,783 bird×risk-night rows and 178 first flights/24 landings using the same 178 individual Motus IDs. Yet **actual reanalysis weather sampled at the departure hour is not a forecast issued to an animal before commitment**, and end-of-flight actual weather must not be used as if known beforehand. The original observational weather→departure/route/landing effects are published prior art.

An independent archived weather forecast, with **issuance (model initialisation) UTC time and forecast valid UTC time**, is therefore the next source requirement. This is the *objective external availability* of a forecast-like cue, not proof an individual bird perceived or trusted it.

## Original external forecast source and access gate

- [NCAR GDEX NCEP GFS 0.25° operational historical forecast archive d084001](https://gdex.ucar.edu/datasets/d084001/), **DOI 10.5065/D65D8PWK**; historical forecast years **2019, 2020, 2021** included in the official archive, 0.25° gridded GRIB2. Operational model initialisations **00/06/12/18 UTC** with forecasts at multiple lead times. Official source is NOAA/NCEP; this archive is a *historical issued-forecast archive*, unlike post-hoc reanalysis. The **GFS operational model configuration can change over 2019–2021**, so do not treat the original forecast error distribution as temporally stationary without model-version checks.
- [Official GDEX data access](https://gdex.ucar.edu/datasets/d084001/dataaccess/): **custom time/space/variable subsets and format conversion require registered login**; original full-gridded files are very large. The assistant **has not logged in, accepted terms on the user's behalf, requested any subset, or obtained GRIB2 bytes**.
- A 4-week rolling AWS forecast bucket does **not** by itself verify original 2019–2021 forecast data availability; never substitute a 2026-forecast, ERA5/hindcast, or a forecast issued after a bird's departure for archived 2019/20/21 operational information.

## Frozen forward-information estimand and no-leakage validation

First propose a **separate source feasibility test**, without any bird outcome or GPS location lookup:

1. A genuine original GRIB forecast record is identifiable by issuing-centre, archive file ID, model family/version, `forecast_issue_time_utc`, `forecast_valid_time_utc`, original selected surface 10-m U/V wind and total-cloud-cover product metadata, grid, and original source digest. A reconstructed `issue_time` from only the *valid* time is forbidden.
2. Issue time must **strictly precede the bird's recorded decision time**, with a fixed **≥1 h slack** to avoid same-time publication/processing ambiguity: `issue_utc <= observed_predeparture_decision_utc - 1h`. Actual forecast delivery latency, archive ingestion delay, and bird's real access **are not inferred** from model initialisation time.
3. Positive lead required: `valid_utc > issue_utc`, and a new target state **after** the bird's decision required: `valid_utc > decision_utc`. Do not use zero-hour analysis fields or weather observed at the decision as prospective forecast information.
4. Primary planned forecast horizon, **fixed before any bird/weather effect**: `forecast_valid_time_utc = nearest predeclared +6h valid forecast step after decision UTC` with at most **±1.5 h** alignment; sensitivity horizons **+3 h and +12 h**, not whichever lead produces a significant answer. The corresponding forecast lead `valid - issue` is *not* the same as 6 h relative to bird's decision.
5. Objective forecast error (when *independently observed later verification weather* is available) is an external diagnostic. Neither historical forecast accuracy nor ensemble spread is an observed bird-specific subjective `q`. Issue-time forecast skill must be calculated without using the focal bird outcome, within-year heldout tuning or selection of favorable years.
6. Do not merge exact bird-risk times, actual route, landing or source forecast GRIB in GitHub during **source admission**. No coordinates, bird IDs, restricted data or raw GRIB are uploaded. The original 2023 author model already reports weather effects.

A possible follow-up explanatory comparison of **issued, temporally observable forecast error/uncertainty × remaining leg length** would still need independent route geometry and detection opportunity (offshore flights are harder to detect), otherwise route/landing confounding remains. Only a new source/authenticated forecast issue-time dataset and its coding contract could license a new observational test. No `q_wait(D_eff)`, (r(t)), fitness or two-species coordination effect is identified now.

## Source-admission status

`HISTORICAL_ISSUED_GFS_DATASET_EXISTS` for 2019–2021 is verified from provider metadata; `HISTORICAL_GFS_SUBSET_AUTHENTICATED_AND_RETRIEVED` = **false**; `DECISION_CUE_CHRONOLOGY_FITTED` = **false**. Login required for targeted custom GDEX subset, so source access remains **SOURCE_ACCESS_NOT_ADMITTED** until the user authorizes access and original file bytes/coding are independently checked.

This is a distinct **independent environment-data source gate**, not an empirical information-use confirmation. Keep draft; main and frozen V2/V7 manuscripts untouched. Use no eBird or TinyFish.
