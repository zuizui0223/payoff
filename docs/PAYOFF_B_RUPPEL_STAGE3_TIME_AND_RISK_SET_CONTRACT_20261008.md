# PAYOFF-B: Rüppel flight-event chronology and mechanism-aliasing gate

Date: 2026-10-08.
**Stage 3: source inspection design after Stage-2 object schema, before new outcome analysis.**
Not a preregistered experimental test. Original authors already fitted weather-to-departure/routing/landing effects. No novel regression authorized by this document.

## Exact original source

Rüppel et al. 2023 Royal Society Open Science 10:221420, DOI 10.1098/rsos.221420, Figshare article 21967090, ZIP file 38968813.
MD5 e8fc27e9eb44aa1e89da09310183b39a; SHA256 0ef08e19104aaceff5ef2700c324a094c49cbe2cd24ca198e3853b656d7744c6.

First verified read-only R run 37791673297:
- data.Event: **1,783 rows, 33 columns**: motusTagID, time_abs Date, start, stop, status, flightStart POSIXct, stage weather u/uc/v/vc/pc/t/tc/c/r, etc.
- flights: **178 rows, 70 columns**: motusTagID, flightStart/flightEnd POSIXct, landing, flightCat, fuelLoad (45/178 NA), weather *_start and *_end, flight duration, route and stopover locality.
- Author Rcode.Rmd: 708 lines. Explicit time-to-departure survival regression on data.Event already present. Therefore **departure risk set / weather-informed departure is already established prior art**.
- Schema only; observed counts of landing, flight categories or weather associations were not fit.

## Precisely bounded second read-only check

1. Check unique individuals and repeated flight events, source-level years, nights-per-bird and weather covariates. Report counts, not individual's raw date or coordinates.
2. Check whether status events and flights are linkable by motusTagID and date, and whether **all** 178 flights can be assigned an origin decision timestamp and later measured weather (including detected censoring).
3. Check actual flightStart < flightEnd and whether weather_end variables are measured before or after completed/aborted flight. Column names do not settle event availability; interpret author Rmd and paper methods.
4. Extract short annotated author Rmd **source-code snippets** specifically for models of route and landing and when start/end weather is measured; never execute author code or re-estimate original coefficients.
5. Count source support for relevant missingness, individual repeat observations, weather_end minus weather_start measurement completeness and event status only. Keep all raw individuals/coordinates/timestamps out of output.
6. Require full source MD5/SHA256 and test failure if real data unavailable. Synthetic fixtures must not count as real source validation.

## Stop and promotion criteria

- A verified *nightly departure risk set* does not mean the *in-flight landing* table contains a decision risk set. Do not multiply flight count by event nights or treat the two tables' 1,783 and 178 rows as independent samples of the same decision.
- Temperature/wind at flight END is not a pre-flight cue; it may be contemporaneously measurable near landing but chronology and environmental spatial interpolation need independent support.
- A later wind variable may directly impose an adverse physical **weather hazard**, and thus predict landing even without any active belief update. Distinguish this null from a revision of a forecast made at departure.
- Route or landing decisions are existing Rüppel 2023 results. A simple landing ~ wind_end regression, even with heldout calibration, is not a new behavioral discovery.
- Stop short of causal actionability/fitness claims without independently observed feasible alternatives, energy expenditure, breeding/survival and stage-specific resource target.

The relevant new candidate is *conditional forecast innovation over an origin-issued forecast*, not just present weather. If source lacks that forecast and the flight-in-progress risk set, classification is **WEATHER-RESPONSIVE_POLICY_PRIOR_ART_ONLY** or **SOURCE_NEEDS_EXTERNAL_FORECAST_AND_RISK_SET**, not a new PAYOFF result.


## One additional source-structure discriminator registered after basic counts

The verified source shows exactly 24 flights coded landing=1 and exactly
24 flights labelled sea-crossing (154 in their complementary categories).
Before attributing these to separate decisions, calculate the explicit
2-by-2 route-category × landing cross-tab directly from the original source
and inspect the author Rmd's actual route and landing model sections.

Equal marginal counts DO NOT imply identical records. If these outcomes
are perfectly dependent or defined by overlapping tracking-detector criteria,
they cannot constitute two independent biological decisions. If not,
quantify source support and keep both decisions separate. Either way,
cross-tabulation is a source-ontology check, not a new weather association.

The original author Rmd is 708 lines long. The first automated source
snippet limit of 155 context lines stopped during the departure model;
the follow-up will read later script sections and their explicit use
of flight-start versus flight-end weather without running models.
