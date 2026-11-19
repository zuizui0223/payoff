# Rüppel 2023 native-R individual timeline: source-join admission before any new effect

**2026-11-19, source metadata previously opened, event/flight response not yet reanalyzed.**

Original SHA256-pinned Figshare `rsos221420_si_002.zip` contains `data.Event` 1,783 daily at-risk records (33 columns) and `flights` 178 flight records (70 columns), each with **178 distinct `motusTagID` identifiers**. The original author RMarkdown references both. The original 2023 paper *already reports* 178 sustained flights and 24 observed landings among 275 originally marked birds; none of those outcomes is a new PAYOFF observation.

## Frozen source-only linkage audit

1. Native base R loads the **exact original ZIP** (size **100,303 bytes**, SHA256 `0ef08e19104aaceff5ef2700c324a094c49cbe2cd24ca198e3853b656d7744c6`). Verify original `data.Event` and `flights` data frames and published 1,783/178 row counts, 178 IDs each. No model is fitted.
2. Compute **only aggregates**: intersection/symmetric differences of `motusTagID` sets; number of repeated flight IDs; count/validity of event `status` 0/1 (at-risk daily departure); unique birds with a terminal event; count/validity of flight `landing` 0/1; original flight-category counts; source-time `flightStart/flightEnd` completeness; start-before-end order; start/end wind/cloud values completeness. Do not export original ID values or observed timestamp values.
3. Inspect the source event-date `time_abs` and individual `flightStart` chronology with **three fixed windows**: same UTC day, within UTC ±1 calendar day, and nonmatching/unknown. This is an observational source-join quality check, not independent weather observation accuracy.
4. The source key is **`motusTagID`** shared by both original tables. It is not joined on coordinates, routes, individual weather values, tag deployment time or post-departure outcomes. If source ID sets do not match, retain counts and report `ID_JOIN_NOT_SOURCE_FAITHFUL` rather than dropping unknown IDs.
5. A future observational sequential-decision analysis could be source-grain **eligible** if at least 30 distinct birds with linked risk→flight, at least 10 original observed landings, exactly one flight per linked bird and event/source weather timestamps are present. All numbers must be computed, not assumed from the paper. Even passing eligibility does **NOT** show forecast accuracy of destination spring, a causal information threshold, remaining recourse `r_t`, net waiting cost `D_eff`, fitness or interaction synchrony.
6. Scientific stop: **the original authors already modeled departure, routing, landing versus weather**. Refit those associations only for method reproduction, not new PAYOFF novelty. A future distinct test of unexpected wind change versus landing would require a frozen new estimand, route/detection-bias controls, independent weather timestamps and at least a credible out-of-year/taxon transfer; no such fit is authorized by this source audit.

The source original dataset may contain sensitive local coordinates; no animal-level rows or locations are ever committed, uploaded or printed. No eBird, no TinyFish, and frozen main/PAYOFF V2/V7 untouched.
