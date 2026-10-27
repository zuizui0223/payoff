# PAYOFF-B stationary-day risk set (source-only)

2026-10-22. The prior 36-case matched NASA weather pilot selected a same-animal
stationary control exactly five days before each moving case; this design was
strongly confounded by calendar time and excluded all nonmigrating animals.

The new observational risk universe includes EVERY 3-day stationary GPS anchor
in Feb-May, requiring >=2 distinct hourly observation bins per day. Source
origin is the previously checksum-verified public CC0 GPS files of stork,
white-fronted goose and curlew, with frozen 145/106/59 cases reconstructed.

Eligibility uses only the three prior consecutive days within 30 km of their
source center. Outcomes from following day4/day5: northward candidate (day4
>=30km, day5 >=120km and >=0.8 degrees north), sustained stationary
(day4 and day5 <=30km), other movement (ambiguous) or right-censored
(followup missing). Missing observations and nonnorthward movements are never
called stays. Eventual departure is NOT an eligibility condition. The original
7-day de-duplication is maintained for reproducing frozen historical cases,
but full day-level risk labels are counted separately.

Risk entries are overlapping within animals; the raw event fraction is NOT a
causal or even complete natural migration hazard. No fitness or environmental
cue values are opened. Future hourly T2M / WS10M covariates must be dated
BEFORE the final stationary reference day, and inference must handle calendar
and site-dependent baseline trends, repeated animal-days, censoring and
original cohort overlap.

Files: scripts/qc_payoff_b_complete_stationary_riskset.py,
tests/test_payoff_b_complete_stationary_riskset.py.
