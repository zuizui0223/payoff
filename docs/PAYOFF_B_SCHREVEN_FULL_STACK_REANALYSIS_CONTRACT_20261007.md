# PAYOFF-B Schreven same-system reanalysis contract

Date: **2026-10-07**
Status: **SOURCE-PROSPECTIVE; PUBLISHED AGGREGATE RESULTS KNOWN**

## Aim

Test whether the Schreven pink-footed-goose system can place multiple PAYOFF
interfaces on the same individual route-stage coordinate.

This is not an outcome-blind discovery study. Aggregate published results are
already known. The prospective objects are row-level linkage and interface
estimands defined here before raw Dataverse rows are opened in this repository.

## Intended source

DataverseNL DOI 10.34894/KLPQG9.

Required source families if available:

- individual GPS/tracking records;
- route or breeding-population assignment;
- stopover-region definitions or sufficient coordinates to reproduce them;
- site-year environmental spring dates;
- migration timing / stopover tables allowing individuals to be linked across
  ordered stages.

Published tables may validate reconstruction but must not be used to fabricate
missing row-level values.

## Primary route-stage table

Construct one row per:

    individual x migration year x ordered route stage

Required columns:

    individual_id
    year
    route
    stage
    source_site
    target_site
    source_arrival
    source_departure
    target_arrival
    source_spring_date
    target_spring_date

Optional if source-backed:

    target_departure
    movement_duration
    source_target_distance
    mean_movement_speed
    source_stopover_duration
    remaining_stopovers
    breeding_destination

## Frozen coordinates

### External mapping

Within a declared period/site definition:

    target_spring_anomaly
        = alpha_s + betaE_s * source_spring_anomaly + error.

Report signed betaE, signed correlation and uncertainty. If sample size permits,
also report held-out source-added prediction value.

### Individual exposure

    O_isy =
      1{source_arrival <= source_spring_date <= source_departure}.

Continuous lead before departure:

    Lsource_isy = source_departure - source_spring_date.

These are exposure-opportunity coordinates only.

### Behavioral response

Primary candidate response is source departure timing conditional on source
arrival and source spring anomaly, with route/stage and individual structure.

The exact mixed-model random-effects structure will be frozen only after a
source-level replication audit and before focal coefficients are opened.

### Signed phase

    e_isy = arrival_isy - spring_sy.

Consecutive-stage transformation:

    Delta e_isy = e_i,s+1,y - e_isy.

### Temporal-flexibility proxy

Primary descriptive proxy:

    T_isy = source_departure - source_arrival.

Observed duration is never labelled structural actionability r.

Additional proxies may be admitted only if source fields support them before
focal outcome fitting:

- stage-specific duration range;
- lower-tail duration within route stage;
- realized movement-time compression;
- remaining stopover count;
- route-stage speed range.

## Interface tests

### A. Exposure opportunity

By route stage report the fraction O=1 and continuous source-event timing
relative to arrival and departure.

### B. Response-map sign

Estimate whether departure/progression responds to the local seasonal
coordinate and whether signed response differs among route steps with different
signed external mappings.

A negative external mapping does not automatically imply a required negative
behavioral slope; the ecological loss mapping must justify any directional
prediction.

### C. Response-to-phase transfer

Conditional on starting phase and source-stage response, summarize signed phase
change by the next stage.

This remains descriptive unless a causal response model is identified.

### D. Flexibility moderation

Test whether an independently declared temporal-flexibility proxy predicts
source-to-target phase transformation after controlling for starting phase and
route stage.

Because realized duration can be endogenous behavior, this does not identify r.

## Minimal feasibility gate

A route step enters the same-system bridge only if:

- at least 3 migration years have source and target environmental values;
- at least 5 tracked individual-years have source arrival and departure;
- at least 5 have next-stage arrival;
- stage assignment is unambiguous;
- exposure can be calculated without creating residence by interpolation over
  long tracking gaps.

If fewer than two route steps pass, do not claim a route-comparative full-stack
test.

## Route reconstruction rules

- Never infer an unvisited stopover just because it occurs in the nominal route.
- A skipped stopover is a biological observation, not missing data to impute.
- Do not linearly interpolate across multi-day gaps to manufacture residence.
- Use one arrival/departure algorithm across routes.
- If published stopover polygons or centres are unavailable, freeze a spatial
  reconstruction rule before opening focal response results.

## Benchmark rule

Published aggregates are source-validation checks only.

Useful checks include:
- Jutland stopover-duration contrast;
- recent Trondelag-to-Svalbard signed predictability;
- route-specific timing contrasts.

If source reconstruction cannot recover published direction under a
source-faithful method, stop and audit the reconstruction. Do not tune thresholds
until the published result appears.

## Claim ceiling

A successful Level-3 bridge licenses at most:

> Route-stage environmental predictability, individual exposure opportunity,
> enacted timing response, observed temporal flexibility and downstream phase
> can be placed on the same ordered migration trajectory.

It does not automatically license:
- cue perception;
- learning;
- optimality;
- structural r(t);
- fitness value of the cue;
- broad generalization.

## Stop rule

Do not add another PAYOFF theory layer or Bellman controller before source
materialization.

The only valuable next question is empirical:

> Can the missing biological interfaces be separately observed in the same
> natural trajectory?
