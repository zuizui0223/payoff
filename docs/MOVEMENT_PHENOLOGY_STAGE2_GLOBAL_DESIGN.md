# Stage 2 — global movement–phenology front design

Status: design frozen for pilot implementation; data access remains external.

## Why Stage 2 changes after Stage 1

Stage 1 did not support a universal raw arrival/green-up optimum. The order-one signal appeared only after removing the locally realized species × cell phase offset, and even then the minimum was shallow and heterogeneous.

Therefore Stage 2 is not a hunt for a single global constant. It asks:

> **Where does a finite order-one movement–phenology matching minimum emerge, and what ecological features make it sharp?**

The primary estimands are heterogeneity and moderation, not a grand mean.

## Common geometry

Represent both animal timing and environmental timing as spatial surfaces:

~~~text
T_animal(x,y)
T_environment(x,y)
~~~

For any timing surface T in days on coordinates measured in km,

~~~text
gradient(T) = (dT/dx, dT/dy)  [days / km]
~~~

and the local isochrone/front velocity is

~~~text
v = gradient(T) / ||gradient(T)||^2
speed = 1 / ||gradient(T)||  [km / day].
~~~

This identity gives a common bridge from Stage 1 to global products. It is implemented and unit-tested in analysis/movement_phenology/fronts.py.

Derived quantities are

~~~text
u_macro = |v_animal| / |v_environment|
q = log(u_macro)
alignment = cos(angle_animal - angle_environment)
vector_mismatch = |v_animal - v_environment| / |v_environment|.
~~~

## Bird timing surface from eBird Status and Trends

Use weekly relative-abundance rasters from the current eBird Status release.

For each species and grid cell, derive a spring timing statistic only inside the pre-breeding migration / breeding-transition portion of the annual cycle. Candidate timing definitions are:

1. week of maximum positive abundance change;
2. 50% cumulative arrival week after the local winter minimum;
3. midpoint between 20% and 80% seasonal accumulation.

The pilot must compare these definitions before one is frozen.

The current eBird products require an access key tied to an eBird account for geospatial downloads. The pilot code therefore must fail clearly when the key is absent; no scraping of map images is permitted.

## Environmental timing surface

Primary vegetation target:

~~~text
MODIS MCD12Q2 v6.1 MidGreenup
~~~

with Greenup, Maturity, Peak and EVI2 amplitude retained for sensitivity analyses.

For non-herbivorous or weakly vegetation-coupled taxa, vegetation green-up is a proxy for the resource wave rather than the resource itself. Diet is therefore a preregistered moderator, not a nuisance to be ignored.

## Spatial support

Start at a coarse common equal-area grid (target approximately 25–30 km), matching the scale at which broad eBird movement surfaces are stable.

For each focal cell:

1. fit a local plane to animal timing over neighboring cells;
2. fit the same local plane to environmental timing;
3. convert both gradients to front velocities;
4. retain only cells with adequate neighbors and finite gradients;
5. compute speed ratio, alignment and vector mismatch.

The same neighborhood geometry must be used for animal and environment timing.

## Response

Raw phase mismatch:

~~~text
raw_phase = T_animal - T_environment.
~~~

Because Stage 1 showed that species-specific local phase is essential, the primary Stage-2 response is a baseline-relative phase displacement:

~~~text
phase_residual
= raw_phase
- expected phase for that species × macroregion / route segment.
~~~

The baseline is estimated without using the focal cell when possible.

Primary response:

~~~text
abs_phase_residual = abs(phase_residual).
~~~

## Pilot hypotheses

### G1 — conditional finite optimum

A finite order-one minimum in abs_phase_residual is more likely when animal and environmental fronts are directionally aligned.

### G2 — cue relevance

The minimum is sharper in taxa whose food/resource phenology is plausibly coupled to vegetation timing, and weaker for trophic guilds where vegetation green-up is a poor cue.

### G3 — movement capacity

HWI and migration strategy alter the ability to remain near the local matching point, but are not assumed to shift the theoretical optimum in a fixed direction.

### G4 — route geometry

Simple directional routes should show clearer matching than broad-front, loop, or strongly longitudinal migration.

## Pilot sampling

Do not begin with all ~3000 modeled species. Use a stratified pilot with approximately 60–100 species spanning:

- Nearctic and Neotropical migrants;
- Palearctic–Afrotropical / Eurasian migrants where current products are available;
- New Zealand or Chilean seasonal movers as Southern Hemisphere contrasts;
- herbivores / granivores / insectivores / omnivores;
- low and high HWI;
- short-, medium- and long-distance migrants.

Species inclusion must require a clearly resolved pre-breeding movement front and adequate modeled-area coverage.

## Models

Core hierarchical form:

~~~text
abs_phase_residual
~ s(q)
+ s(alignment)
+ ti(q, alignment)
+ trophic guild
+ HWI
+ migration strategy
+ route geometry
+ interactions of q with the registered moderators
+ species random effect
+ macroregion random effect.
~~~

The key outputs are:

- whether a finite minimum exists;
- its location and uncertainty;
- curvature / sharpness;
- how those quantities vary among ecological groups.

## Data-access gate

eBird Status and Trends geospatial products require an access key. Current official documentation states that access is granted after agreeing to the product terms and that weekly geospatial abundance rasters require the key.

Until a key is supplied, Stage 2 can advance through:

- front-geometry code and synthetic tests;
- species registry construction;
- MCD12Q2 preprocessing;
- taxonomic / trait joins;
- model and quality-control contracts.

Do not substitute screenshots or PNG map extraction for the actual geospatial products.
