# PAYOFF-B: Rüppel 2023 radio-telemetry object schema and decision-time gate

Date: 2026-10-08
Classification: SOURCE-ONLY; source collection opened, individual data structure NOT YET EXAMINED; no behavioral outcome or regression may be fitted in this check.

Prior source receipt: GitHub run 37788214629 verifies Figshare collection DOI 10.6084/m9.figshare.c.6403996, source article 21967090, file 38968813, ZIP name rsos221420_si_002.zip, 100303 bytes, MD5 e8fc27e9eb44aa1e89da09310183b39a, SHA256 0ef08e19104aaceff5ef2700c324a094c49cbe2cd24ca198e3853b656d7744c6. It contains data.Event.RData, flights.RData, Rcode.Rmd. The authors published weather responses for departure, offshore/coastal route, and interrupted flight; those effects are prior art.

## Stage-2 read-only audit before source outcomes

- Fetch ONLY the exact public author-deposited Figshare ZIP, verify MD5 AND SHA256 before inspecting.
- R base load each RData into an isolated namespace. Inspect object names, data-frame dimensions, column names, column storage type, missingness percentage, and date/time class. No row values, coefficients, dependent-variable outcome distributions, model fits or individuals' tracks in output.
- Parse Rcode.Rmd only for bounded, short source-code snippets matching joins, time conversion, departure/landing decision definitions, environmental lookups or modeling structure. Code is inspected as TEXT, not executed.
- Determine if both data objects have a linkable individual ID and event/flight ID; whether weather is recorded prior to each decision, or aggregated over the whole flight; and whether non-landing risk-time windows exist. A mere flight summary or weather mean during an outcome cannot establish an innovation relative to origin-time forecasts.
- Never impute a missing source forecast, actual feasible alternative action set or demographic fitness. If columns lack these, stop novelty promotion.
- Do not use raw individual radio-telemetry data to make a new empirical claim without a later, separately documented estimand and independent comparison to the authors' already-published models.
- Fail CI closed when ZIP, R installation, serialized objects or required provenance are unavailable; always upload the diagnostic schema receipt.

## Source categories

1. VERIFIED_OBJECT_SCHEMAS_ONLY: object names and columns reported but no semantic identification yet.
2. REAL_INDIVIDUAL_DECISION_RISK_SET_CANDIDATE: linkable ID, timestamped flight-risk intervals and weather measured before a route/landing action; inspect the original authors' already tested target first.
3. FLIGHT_LEVEL_SUMMARY_ONLY: stop at weather association, route/landing or group event model; cannot infer sequential forecast surprise.
4. ACTIONABILITY_AND_FITNESS_HOLD: unless independently dated feasible choices and individual survival/breeding are in the same underlying data, no ecological optimal-payoff result is identified.

All ranks must explicitly mention direct prior art from Rüppel et al. (2023, doi:10.1098/rsos.221420). This project does not claim discovery of multi-stage weather-responsive migration.
