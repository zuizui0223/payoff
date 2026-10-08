# PAYOFF-B: Rüppel radio-telemetry source disposition — prior weather-change model already present

Date: 2026-10-08
Source status: **ORIGINAL BINARY VERIFIED; REAL RDATA OBJECTS, TEMPORAL LINKAGE AND AUTHOR CODE INSPECTED**.
Ecological claim status: **NO NEW PAYOFF-B INFORMATION-REVISION OR FITNESS MECHANISM IDENTIFIED**.

## Provenance and runs

Rüppel et al. (2023), Royal Society Open Science 10:221420, DOI 10.1098/rsos.221420.
Original author Figshare: DOI 10.6084/m9.figshare.c.6403996,
ZIP rsos221420_si_002.zip, Figshare file ID 38968813;
100303 bytes, MD5 e8fc27e9eb44aa1e89da09310183b39a,
SHA256 0ef08e19104aaceff5ef2700c324a094c49cbe2cd24ca198e3853b656d7744c6.

- GitHub Actions **37788214629** verified source ZIP structure and SHA; RData and original Rcode.Rmd found.
- **37791673297** verified and inspected RData objects: data.Event 1783 rows/33 columns, flights 178 rows/70 columns, plus 708-line author Rmd.
- **37792277616** and **37792839996** inspected individual ID × event time linkage, flight duration chronology, cross-tabulated route versus landing, and exact original Rmd landing/routing model source.
- All those dedicated source workflows PASSED; synthetic tests are supplemental and were never mistaken for substantive real-data outcomes.
- No author model was executed, no novel coefficient estimated, no ecological demographic fitness estimated.
- Source-only program: scripts/payoff_b_ruppel_fetch_verified_zip.py, scripts/payoff_b_ruppel_rdata_schema.R, scripts/payoff_b_ruppel_stage3_time_support.R.

## Exactly what this public source supports

| Component | Original records / variables | Status |
|---|---|---|
| Nights at risk for a departure event | data.Event: **1,783 rows**, 178 individuals, unique individual-day key; status=0 for **1,605**, status=1 for **178** | **OBSERVED AND ALREADY PUBLISHED BY AUTHORS** |
| Observed individual flights | flights: **178 flights, 178 individuals, exactly one observed flight per bird**, complete start and end time; all durations positive | VERIFIED one flight per bird; not a repeated within-individual flight policy panel |
| Risk/flight linkage | 178 shared bird IDs, **175/178** same individual and calendar date at departure; 3 non-matches require midnight/timezone/event-date checks | DATA GRAIN PARTIALLY LINKED, do not silently force |
| Routing | flightCat: **154 coasting, 24 sea-crossing** | Original authors' logistic route choice |
| Interrupted flight / observed landing | landing=1 in **24**, landing=0 in **154** | Original authors' event endpoint; value 0 includes non-observation phrasing in Rmd, so detectability/censoring is a rival |
| Route × landing overlap | coast/no landing **133**, coast/landing **21**, sea/no landing **21**, sea/landing **3** | Not perfectly aliased; 3 observations in sea/landing joint cell limit interaction support |
| Wind and weather relative to flight | u_start/v_start/u_end/v_end fully populated, flightStart/flightEnd valid in 178 records | Start and endpoint observations are different **times**; end weather is not an origin-issued forecast |
| Condition/energy proxy | fuelLoad available 133/178 (45 missing), mass and wing field mostly populated | Not a direct physiological movement cost, and no linked reproduction/survival endpoint |
| Full physical action set | No individual alternative route/speed/landing-feasibility measurements documented in released tables | NOT IDENTIFIED |
| Behavioral learned forecast changes | No departure-issued probability forecast for later wind field or subjective expectation; one flight per bird | NOT IDENTIFIED |

The observed flight duration ranged from **0.389 to 10.920 hours** with median **2.454 hours**; this is a source range, not a fitness effect.

## Direct original-code prior-art collision

Original author Rcode.Rmd:
- Lines 68–72 fit departure with original Bayesian survival regression:
  Surv(start, stop, status) on wind and weather, with seasonal/year terms.
  Therefore a departure-night hazard/weather model is entirely prior art.
- Lines 500–512 transform flightCat and fit **flightCat on u_start**:
  route choice conditioned on wind available at flight start already published.
- Lines 589–610 explicitly model the landing outcome. The author creates
  **v_diff = v_end - v_start**, standardizes it and fits a Bernoulli
  model using **v_diff and cloudiness**, accounting for year/species and
  date. Therefore even the tempting analysis of **weather change while
  flying, followed by observed landing** was already carried out in the
  original paper. PAYOFF-B must NOT call it a new finding or unique
  confirmation of the timer/controller theory.

The author Rmd labels the landing analysis as 'landing vs. not seen'.
This is a warning that flight non-detection must not automatically be
interpreted as deliberate continuation with equal receiver coverage.
The published paper discusses detection and censoring; any further
reanalysis must preserve the original study's assumptions and labels.

## Why the tempting new information-value test fails here

PAYOFF-B would need:
- before departure: time-stamped forecast of later encountered wind
  and resource/landing opportunities, not just flight-start measured wind;
- during flight: a later, previously unavailable weather innovation,
  measured BEFORE a well-defined in-flight route/landing decision;
- at each decision: independently defined, genuinely feasible continue
  versus land alternatives and weather-censored receiver coverage;
- then: future energetic and demographic payoff for claims of optimality.

The provided flight table has weather at the two observed endpoints, not a
departure-issued forecast and not repeated candidate landing/continue
intervals along every flight. Because flightEnd itself depends on the
recorded flight termination, weather_end must not be assumed to have
been known *prior to the landing choice*. A naive end-minus-start
covariate can measure realized weather change without distinguishing
information updating, a physical hazard, or event-time sampling.

No individual appears in multiple observed flights, so a model of
within-individual revisions to a learned route policy cannot be
validated using repeated flights in this archive. data.Event offers a
legitimate risk set for ORIGIN DEPARTURE, not by itself a risk set for
landing after departure.

Thus: **NEW_INFLIGHT_FORECAST_INNOVATION_GATE = HOLD**;
**INDIVIDUAL_FITNESS_OPTIMALITY_GATE = HOLD**;
**INTERSPECIFIC_COORDINATION_GATE = HOLD**.

The appropriate role in Paper 2 is a concrete, citation-backed
original-source example of multiple different migration decisions with
different event structures, and a strict prior-art/temporal
identifiability boundary. Do not fit another wind-to-landing
coefficient and label it PAYOFF-B discovery.

## Scientific next action (not another fitted model)

Look only for an original source that adds a genuinely historical
departure-issued weather forecast plus timestamped in-flight
information and decision risk intervals to these kinds of records.
A prospective forecast reconstruction with independent weather
verification and observation-at-choice timing is a separate study
requiring an explicit source, permissions and before-outcome analysis
plan. Until that is admitted, retain Paper 2 as theoretical and
its natural sources as prior-art and structural-negative controls.

Original article: https://doi.org/10.1098/rsos.221420
Public archive: https://doi.org/10.6084/m9.figshare.c.6403996
