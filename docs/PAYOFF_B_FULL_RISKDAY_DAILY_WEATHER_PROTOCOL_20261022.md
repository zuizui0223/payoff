# PAYOFF-B full 5,509-source-riskday daily meteorology bridge

Date: 2026-10-22. Pre-batch design registered BEFORE full GPS-risk-day
NASA daily meteorology responses were opened. Existing selected 144-point
hourly pilot was already observed; therefore this is **exploratory
expanded-source validation**, not an untouched confirmatory test.

The complete original MD5-verified GPS panel has 5,509 at-risk stationary
source days (333 unthinned northward labels, 4,029 stayed, 727 other,
420 censored), and deduplicated 145/106/59 original events. Risk eligibility
uses only 3 stationary days, not the later move label.

NASA POWER **daily UTC** physical environmental fields:
T2M, WS10M, V10M, ALLSKY_SFC_SW_DWN, with grid rounded to 0.5 degrees
before any public query. Prior-day reference is event anchor day minus 1;
the preceding 7-day mean uses only days anchor minus 2 through minus 8.
No observational label is allowed to access event day/day4/day5 weather.
Daily NASA values are a different measurement aggregation from the
preceding hourly pilot, and direct numeric equivalence is not assumed.

The source-only API request planner found 343/334/132 original unique
grid-month-years (809 requests in total), all under the <=500-per-source
operational admission cap. Batch request spans month-first minus 8 UTC
days to month's end, but only historical days anchor minus 1...minus 8
are accessed by the predictor function. Retain every source failure and
every source day label (case/stay/other/censored); never reclassify missing
weather as a negative migration outcome. Require >=90% daily weather
completeness separately for source case and stay class.

Allowed DESCRIPTIVE summaries per source: unadjusted mean prior-weather
anomaly and raw last-day conditions contrasting northward-labelled vs
stay-labelled days. A stronger *source-standardized* descriptive quantity
is calculated within every original 0.5-degree grid × calendar year ×
calendar month containing both source classes, then averages stratum
contrasts weighted by number of source case days in each such stratum.
Requires >=25 case-days in overlap and >=10 nonempty overlap strata.
This controls coarse source place and season but not weather autocorrelation,
route stage, readiness, prior source state, animal identity or spatial
dependence across adjacent grid cells.

No source cells, animal IDs, exact timestamps, coordinates, or record-level
meteorology leave workflow. No causal departure hazard, biological
information processing, migration compensation, reproductive/survival
benefit or between-taxon meta effect may be claimed from this result.
One study per taxon and the historical PAYOFF goose overlap remain gaps.
