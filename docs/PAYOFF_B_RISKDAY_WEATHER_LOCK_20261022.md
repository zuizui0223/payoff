# PAYOFF-B weather source sampling from ALL stationary-day risk opportunities

Date: 2026-10-22. Registered before fetching any new historical meteorology.
This is observational **source feasibility and descriptive weather**, not
animal cognition, migration hazard, active timing correction or fitness.

GPS origin remains the original 3 public Movebank CC0 datasets. The frozen
per-system full stationary-day counts (stork 1633; goose 2008; curlew 1868)
are checked prior to selecting any weather samples. Cases are future day4/day5
northward labels. Nonmove means observed day4/day5 still within 30km.
Right-censored and other movements are NEVER called controls.

From each full panel draw a fixed SHA256/identity/year/day-ranked sample,
round-robin across February-May calendar months, up to 16 case riskdays and
32 nonmove riskdays per source. No more than one day per identity-year per
outcome class. Selection uses the original source labels but NO weather.
It is outcome-stratified and must NOT be used to estimate population movement
probability from sampled fractions. Fail, rather than adjust quotas, if fewer
than 12 complete cases or 20 complete stays per taxon.

For each selected source day use the prior UTC day T2M, WS10M, and its
difference from the preceding seven UTC days. Require >=18 hourly
observations per variable per day, and 0.5-degree grid coarsening BEFORE
external NASA POWER requests. Deduplicate exact public source weather queries.
All failures remain documented; no tomorrow/outbound-day weather is allowed.

Outputs contain only per-taxon and outcome group means, descriptive bootstrap
intervals, source month comparisons and missing-data counts. Repeated animal
year and observational month/source heterogeneity preclude naive independent
tests; NO causal inference or pooled taxon effect is conducted in this gate.
Wind speed is not route-relative tailwind. Reanalysis is not a historic
forecast experienced by the bird. Cohort overlap with old goose analysis
remains unresolved. Scientific law or selective fitness effects are untested.
