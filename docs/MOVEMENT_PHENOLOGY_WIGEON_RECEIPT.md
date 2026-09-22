# Eurasian-wigeon migration-distance evidence receipt

Status: independent literature-derived evidence; raw Movebank reanalysis pending.

Source: van Toor et al. (2021), *Movement Ecology* 9:61, DOI 10.1186/s40462-021-00296-0.

Tracking data: Movebank Data Repository DOI 10.5441/001/1.dv5mm289.

## Design

After preparation, the study retained:

~~~text
35 spring migration trajectories
31 individuals
28 individuals with spring-arrival/TGS analysis
208 staging-site arrival events
migration endpoints spanning roughly 300–4000 km
median migration speed 48.2 km/day
Q1 = 30.0 km/day
Q3 = 60.9 km/day
maximum observed daily displacement ~963 km
~~~

Local environmental phase was measured relative to onset of the thermal growing season (TGS).

## Main evidence

At staging sites, tracked wigeons arrived a median of 22.5 days after TGS onset:

~~~text
median = 22.5 d
Q1 = 13 d
Q3 = 35.3 d
~~~

Arrival phase depended on total migration distance and progress along migration.

The published mixed-effects analysis found:

- birds reaching higher maximum longitude, a proxy for longer total migration, arrived earlier relative to TGS onset;
- this effect became stronger the farther individuals had already travelled;
- TGS deviation also affected arrival phase;
- fixed effects explained about 42% of variation in arrival phase.

For a standardized hypothetical individual after 1000 km of migration and average annual TGS timing, predicted arrival phase relative to TGS onset was:

~~~text
Lithuania-like endpoint: 39 d
Moscow-like endpoint:    33 d
Perm-like endpoint:      26 d
Ob River Delta:          22 d
~~~

The last-arrival-only sensitivity analysis recovered the same qualitative effect, with marginal R^2 about 0.44.

## Interpretation in the controller framework

This system supplies a clear **strategy-gradient** result:

> As total migration distance increases, wigeons progressively reduce their lag relative to spring phenology.

This is not yet a direct estimate of the local feedback gain \(\kappa\), because the published main analysis models staging-site phase rather than relative animal/environment wave speed.

Nevertheless, it supports the macro hypothesis that time pressure and migration strategy alter the target phase \(E_*\).

Long-distance migrants appear to aim for an earlier phase relative to local spring than short-distance conspecifics.

## Important measurement perturbation

Tagged birds migrated more slowly than ring-marked birds from the broader population.

Published differences:

~~~text
Arnhem ringing comparison:
  +11.57 d delay
  95% CI 5.75 .. 17.38 d

London:
  +11.30 d delay
  95% CI 5.48 .. 17.12 d

Moscow:
  +4.64 d delay
  95% CI -0.93 .. 10.21 d
~~~

Thus absolute controller calibration from these tracks must account for tag-induced migration delay.

The published authors explicitly note that the relative result — closer tracking of spring farther into migration — should be more robust than the absolute phase.

## Macro role

This system supports:

~~~text
M4:
migration strategy / total route length can shift the target phase

not:
one universal E* across individuals or routes
~~~

It also gives a useful within-species design because total migratory distance varies by more than an order of magnitude while taxonomy and broad trophic niche remain fixed.

## Claim boundary

Licensed:

- longer-distance wigeons follow spring phenology more closely;
- this effect strengthens with distance already travelled;
- absolute tagged-bird timing is delayed relative to ring recoveries;
- migration distance is therefore a candidate moderator of phase target or correction strategy.

Not licensed:

- a direct estimate of \(\kappa\), \(E_*\), or correction distance;
- causal proof that route length itself changes the controller;
- use of raw tagged timing as an unbiased population phase.

## Promotion rule

Upgrade to Tier A when the Movebank trajectories are reconstructed into migration legs and staging events, TGS timing is recreated, and segment-level animal speed plus signed phase error can be evaluated jointly.
