# PAYOFF-B Rüppel original source: Stage 2 completed, Stage 3 pending

Date: 2026-10-08
Status: **SOURCE SCHEMA VERIFIED / causal actionability and forecast-innovation still HOLD**.

## Provenance

Rüppel et al. (2023) Royal Society Open Science, doi:10.1098/rsos.221420. Authors' public Figshare item DOI 10.6084/m9.figshare.21967090.v1, ZIP file ID 38968813, 100303 bytes, MD5 e8fc27e9eb44aa1e89da09310183b39a, SHA256 0ef08e19104aaceff5ef2700c324a094c49cbe2cd24ca198e3853b656d7744c6.

A dedicated base-R structural inspection **succeeded** in GitHub Actions run **37791673297** (native Figshare exact checksum, R setup, synthetic gate, real serialized data column audit). Source-only schema receipt artifact **11556901081**, ZIP SHA256 c39f77f67925b3344e71c8695b6f63e5f1b3ca155e9fda65cfb4f3000f533e30. No author model executed, no animal outcomes fitted.

## RData objects read from original deposited file

| Original object | Real rows | Columns | Units inferable from schema |
|---|---:|---:|---|
| data.Event | **1,783** | **33** | individual/nightly **potential departure** risk-history candidate, with motusTagID, time_abs Date, start, stop, status and weather; original Rmd fits departure-time survival model |
| flights | **178** | **70** | individual flight summary/event, motusTagID, flightStart, flightEnd, landing, flightCat, stage-start/endpoint weather, distance, fuelLoad |

The published paper already tested direct weather effects on departure, routing and interrupted in-flight movement, so these existing associations are not novel PAYOFF findings.

Date variables: nightly time_abs is Date, flightStart and flightEnd are POSIXct; these are semantically different clocks and must be linked by source individual and date. data.Event status is a modeled event indicator, not 1,783 independent flight outcomes.

Original flight schema has u_start/v_start and u_end/v_end; latter may correspond to weather at observed flight termination, but source authors' processing and measurement chronology require inspection before treating endpoint weather as a cue observed *prior to* landing. Column fuelLoad is missing for **45/178** flight records (133 nonmissing), a potential individual condition proxy but NOT direct energy expenditure or future reproductive fitness. Sex is missing 114/178; landing and start/end timestamps have no missing cells in the source frame. 24/178 flights have coordinates of an identified stopover, but a location field is not an independently observed feasible choice set.

The author Rcode.Rmd is 708 lines and its departure model uses data.Event as a nightly time/event table. No cross-system interaction or demographic fitness outcome is present in the verified object names.

## Stage 3 remaining admission questions

A separately prewritten Stage 3 audit (docs/PAYOFF_B_RUPPEL_STAGE3_TIME_AND_RISK_SET_CONTRACT_20261008.md) checks:
- actual number of distinct birds and dates, shareable individual-flight-to-night link, repeated individual support;
- flight duration chronology, landing and routing category support, and relationship of observed endpoint weather to flight decisions;
- original authors' landing and routing model code and whether an external, prospectively valid departure-time forecast exists.

Do not replace those source checks with guesswork from a column label, and do not infer a new feedback controller merely from an endpoint wind coefficient.

## Scientific decision so far

The data genuinely expose *nightly departure risk* and *flight-event decisions*, which are closer to the PAYOFF-B route-wise information framework than earlier Amaral/V8 grids, Greenland white-fronted goose seasonal stages or Burnside Asian houbara origin/arrival records.

However, **same-flight prospectively known weather, newly arriving information, independent alternative actions and reproductive fitness have not yet been identified**. The only justified new result today is a verified, much stronger original-data source admission. If Stage 3 shows no prior forecast or risk-time-aligned weather, HOLD on a unique mechanism even though Rüppel provides useful stage-specific observational data.

## Links

- Original paper: https://doi.org/10.1098/rsos.221420
- Public data: https://doi.org/10.6084/m9.figshare.c.6403996
- Source code: scripts/payoff_b_ruppel_rdata_schema.R
- Stage-3 code: scripts/payoff_b_ruppel_stage3_time_support.R
