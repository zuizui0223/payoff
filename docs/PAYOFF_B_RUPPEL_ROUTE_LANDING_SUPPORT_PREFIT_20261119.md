# PAYOFF-B — source-only route × landing overlap, before a novel q/recourse interpretation

**2026-11-19. Pre-cross-tab source-only freeze. No new model or biological coefficient opened.**

## Original source fixed

Rüppel et al. 2023, *Royal Society Open Science* DOI `10.1098/rsos.221420`; original [Figshare collection 6403996](https://doi.org/10.6084/m9.figshare.c.6403996), `rsos221420_si_002.zip` exact provider SHA256 `0ef08e19104aaceff5ef2700c324a094c49cbe2cd24ca198e3853b656d7744c6` and size 100,303 bytes.

The original `data.Event` has 1,783 at-risk observations/178 birds; `flights` has 178 first flights, individual `motusTagID` sets intersect perfectly, route labels **`coasting` 154** and **`sea-crossing` 24**. Original landing events also total 24. The equal route/landing marginal totals **do not prove they concern the same 24 birds**.

## Research question

Does the *observed source design* support separate route versus post-departure landing variation, and across original species and years? This is a **source identifiability check**, not a claim about information use, route optimization, or adaptive recourse.

## Outcome-blind evaluation instructions frozen before inspecting new joint counts

1. Use native R and the exact SHA-verified original ZIP, with no bird ID or original flight row values exported. Read `flights` directly. Verify source route codes/coasting=154, sea-crossing=24, landing 0/1 with 24 positive.
2. Produce a **2×2 route-category × binary-landing contingency table** (all four counts) and counts of route/landing by original **year (2019–2021)** and **species** (the source's three published songbird taxa), including original source group sizes, but no individual records.
3. Fixed *minimum* for a potential cross-route landing modifier: both route groups must have ≥5 observed landings **and** ≥5 nonlandings and occur in ≥2 original years and ≥2 original species. This is an identifiability/support gate, not a sample-size/power result or post-hoc biological significance criterion. If it fails, mark `ROUTE_LANDING_MODIFIER_NOT_ESTIMABLE`; do not pool sparse cells or change thresholds after seeing outcomes.
4. Separately mark **source chronology / potential outcome leakage**: original `u_start/v_start/c_start` measured at first flight **start**, `u_end/v_end/c_end` measured at later flight **end**. Because they are distinct observation times, end-weather is **post-flight-start information** and cannot be used as a supposedly known cue for *earlier departure/routing* decisions. `landing` occurs during or after flight; cannot be an explanatory input to the departure hazard. Validate that actual `flightStart < flightEnd` in all 178 original flights and source fields are nonmissing; no forecast-issue-time predictor is documented.
5. Report only source **aggregate counts and join constraints**, never individual `motusTagID`, coordinates, time stamps, or per-bird weather/landing values. Do not fit route→landing or weather→landing association in this audit; those are published prior art in Rüppel et al.
6. The source cannot identify Bayesian destination forecast quality `q`, independently feasible recourse `r(t)`, waiting cost `D_eff`, season-end interactor synchrony or breeding fitness regardless of the cross-tab support. A sparse cell must not be replaced by a pseudo-count, and a favourable cross-tab cannot be promoted as causal evidence.

The original earlier experiment recovered 178 linked bird timelines using only original `motusTagID`; the new cross-tabs are *nested in the same published 178 birds*, so they do not add a second independent empirical sample.

## Stop rule

If the route×landing source design is sparse/collinear, stop developing a natural biological route-by-weather recourse interaction on this cohort. If supported, the next step remains an **independent issue-time forecast dataset and an objective detection-bias-aware downstream endpoint**, not a post-hoc significant refit of published weather effects. All original scripts, effects, frozen V2/V7 and main remain unchanged.
