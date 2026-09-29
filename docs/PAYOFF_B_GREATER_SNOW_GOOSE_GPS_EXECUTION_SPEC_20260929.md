# PAYOFF-B greater snow goose GPS cue-uptake execution specification

Date: **2026-09-29**  
Status: **pre-outcome executable specification**

This document operationalises the frozen registration
`payoff_b_greater_snow_goose_gps_cue_uptake_v1_20260929`. It does not change
the ecological question, response, predictor, estimability gate or claim
ceiling.

## Input boundary

The model consumes two tables prepared without inspecting the focal
temperature-by-predictive-connectivity outcome.

### Day-risk table

One row per individual × staging context × day at risk, with:

- `individual_id`
- `year`
- `context`
- `depart_next_24h`
- `local_temp_anom3`
- `day_of_year_within_context`
- `wind_support`
- `precipitation`

Staging geometry must come from the frozen automatic `movepp` chain at
commit `220e953a2f1c8f29540cb74d0ec69599f24e1d14`:
centered step speed → BALM → data-derived DBSCAN → MPI phase classification.
No climate-informed or hand-drawn primary stopover boundaries are allowed.

The automatic per-individual staging habitats are mapped to exactly three
shared route contexts before any climate or departure-model outcome is read.
Habitat centroids from 1 April–15 June are clustered on **latitude only** by
k-means (`k=3`, `nstart=100`, `set.seed(1)`). Cluster centres are ordered
south to north and labelled `southern_staging`, `mid_arctic_staging`,
`northern_arctic_staging`. These correspond only as ecological anchors to
the published St. Lawrence, Nunavik and Baffin route regions; no manual
boundary adjustment is permitted.

`day_of_year_within_context` is calendar day-of-year centred on the pooled
mean day-of-year within each of those three shared contexts. It is **not**
days since arrival or visit duration.

### Historical connectivity table

One row per context × focal year:

- `context`
- `year`
- `connectivity_rho`
- `training_end_year`
- `training_years`

Every row must satisfy

[
training\_end\_year \le focal\_year-1
]

and at least 15 historical training years.

## Primary model

[
logit(P(depart_{t+1}=1))
=
\alpha
+\beta_1 T_{local,3d}
+\beta_2 z_\rho
+\beta_3 T_{local,3d}z_\rho
+controls.
]

The registered directional prediction is

[
\beta_3>0.
]

Uncertainty is clustered by individual. The result is promoted only when the
estimability gate passes before coefficient interpretation.

## Estimability gate

All conditions are mandatory:

- at least 30 individuals;
- at least 4 years;
- at least 3 staging contexts;
- at least 100 departure events;
- transition-row SD of predictive connectivity at least 0.03.

Failure of any condition returns `NOT_ESTIMABLE`.

## Secondary threshold-like analysis

The secondary Gaussian bridge is

[
q=0.5+\arcsin(\rho)/\pi.
]

Only these candidate thresholds may be evaluated:

[
0.500,0.525,0.550,0.575,0.600,0.625,0.650,0.675,0.700.
]

For candidate (\tau),

[
cue\_active=I(q\ge\tau),
]

and local-temperature sensitivity is allowed to differ between inactive and
active rows.

Selection uses leave-one-individual-out predictive log loss. The
no-threshold model is always retained as a comparator. An interior threshold
may be described only as a **behavioral threshold-like candidate**; it is never
the theorem's (q_{wait}(D)).

The registered 1-SE adjacency gate is implemented on paired held-out-individual
losses. A threshold is supported only when the minimum-loss candidate is an
interior grid point, has lower mean LOIO log loss than the no-threshold model,
and each adjacent grid point has a larger paired mean loss by **more than one
standard error of the paired individual-fold loss difference**. Otherwise
report `THRESHOLD_NOT_IDENTIFIED`.

## Interpretation ceiling

Even a positive primary interaction means only:

> departure timing is more contingent on local temperature where that local
> temperature historically contains more information about later Bylot
> conditions.

It does not demonstrate conscious cue use, identify PAYOFF-B (D), recover
(q_{wait}(D)), or test the pairwise asynchronous window.
