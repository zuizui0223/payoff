# PAYOFF-B: sequential departure-route-landing data admission, Rüppel 2023

Date: 2026-10-08
**Status: PRE-READ SOURCE CONTRACT. Not an ecological result or preregistration of novel effects.**

## Why this system, and prior-art exclusion

Rüppel G, Hüppop O, Lagerveld S, Schmaljohann H & Brust V. 2023.
*Departure, routing and landing decisions of long-distance migratory
songbirds in relation to weather*. Royal Society Open Science 10:221420.
DOI 10.1098/rsos.221420.

The original authors used regional radio-telemetry in spring migrant
songbirds, finding weather associated with **departure, coastal versus
offshore routing, and in-flight landing/stopover decisions**. Wind
support predicted routing; overcast/headwinds predicted interrupted
flights. They already established these three linked weather-response
phenomena. PAYOFF-B cannot claim priority for them.

The paper states that data are provided in supplementary material
Figshare DOI 10.6084/m9.figshare.c.6403996 (collection ID 6403996).

## SOURCE-ONLY gate (before exposure to potential biological rows)

1. Fetch Figshare public collection metadata with immutable-looking
   collection ID 6403996 via its v2 public API.
2. Enumerate all collection items and their article file listings.
   Record title, article ID, posted/updated dates, DOI, filename, size,
   checksum and license where published. Do not assume a reference to
   supplementary tables means public unaggregated tracking trajectories.
3. Download only **small** public files (cap per file 20 MB) if openly
   available; verify published checksum when available.
   Inspect archive/container directory names and CSV/TSV *header and row
   count only*; no weather effects, binary outcomes or time-series fits.
   For PDF and other inaccessible formats, report metadata alone.
4. Determine whether the source contains at the SAME anonymized individual
   and flight level: (i) dated departure decisions including nights when
   the bird could have stayed, (ii) observed route choice, (iii) temporal
   weather *before* landing, (iv) actual in-flight landing timestamp, and
   (v) independent measured change capacity and demographic fitness.
5. Prevent post-outcome leakage: weather computed AFTER a landing is not
   a pre-landing decision cue; route-level averages cannot substitute for
   the weather at the instant of route or landing choice.
6. If supplementary files contain only analysis summaries, models or
   aggregate tables, label **REPRODUCIBILITY_SUMMARY_ONLY**. Do not invent
   unobserved individual event records.
7. Fail CI closed if the public API fails, source verification cannot be
   completed, or required collection metadata cannot be obtained. Preserve
   diagnostic receipt as an artifact even when CI fails.
8. No regression is run in the source gate. Never claim published
   behavioral effects as independently discovered by PAYOFF-B.

## Decision states

- OPEN_INDIVIDUAL_MULTI_DECISION_EVENT_DATA: original records actually
  resolve sequential within-migration cue and decisions. They support a
  *new heldout-prediction question only*, contingent on its difference
  from the existing authors' analysis.
- MISSING_DEADLINE_OR_ALTERNATIVE_ACTION_SET: even event data do not
  identify the feasible set of earlier/later departure or landing, so
  optimal behavioral control and fitness-cost claims remain HOLD.
- NO_INDIVIDUAL_FITNESS: without individual reproduction/survival data
  no causal correction-to-fitness comparison is possible.
- SUMMARY_ONLY_OR_ACCESS_HOLD: do not reconstruct individual decisions
  from paper summary figures.

## Direct ecological novelty challenge

The strongest preexisting source already observes multiple weather-linked
decisions within migration. PAYOFF-B therefore needs a **different
testable construct**—for example a *newly available, temporally ordered
forecast innovation* followed by a change from a prior individual policy,
tested against annual calendars, persistent individual offsets, weather-
driven hazards, and social groups. A contemporaneous weather predictor
of landing, which Rüppel et al. already reported, is NOT that novelty.

Full route recourse must be estimated independently of the animal's
observed stopover or flight; otherwise claiming that an animal used all
available flexibility from its actual movement is circular.

## Sources

- Paper: https://doi.org/10.1098/rsos.221420
- Open access paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC9905979/
- Authors' data: https://doi.org/10.6084/m9.figshare.c.6403996
