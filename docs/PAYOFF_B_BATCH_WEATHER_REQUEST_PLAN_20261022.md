# PAYOFF-B all-source 5,509-riskday weather batching strategy

Registered 2026-10-22 before executing full-scale weather downloads.
This is a *source-cost design* and not a new ecological effect.

The frozen risk set of 5,509 stationary anchor dates uses original CC0
GPS, strict historical MD5 and previous-day-only predictors. Instead of
issuing 5,509 individual NASA API calls for 8 days each, aggregate the
source anchor sites to original 0.5-degree NASA public lookup grids,
and group by original **calendar year + month + grid cell**.

A single API query per unique month-grid-year can cover the entire
calendar month plus eight preceding UTC days. This permits source dates
within the month to receive only physical reanalysis from day minus 1
and the preceding seven days without fetching future weather as a
statistical covariate. The returned series can include dates after a
particular event ONLY if the analysis script prevents use of those later
dates for that event. Exact date checks and missing hours must fail
closed. The data source is NASA POWER hourly T2M, WS10M, V10M,
ALLSKY_SFC_SW_DWN. Do not use retrospective weather as a genuine
forecast the bird received.

This planner reports ONLY number of unique year-month-grid batches,
potential reduction in source requests and counts of within-cell-month
northward/nonmovement overlap. Source geographic cells themselves and
individual/date keys are never in its output.
A predeclared operational gate limits a single unreviewed full query
operation to <=500 unique month-grid-year requests per taxon; above it,
do not silently send an arbitrarily large burst to the public NASA
service. Neither query batching nor raw row counts imply statistical
independence across animal-day, study, sensor or weather grid.
