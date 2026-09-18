# Movement–phenology macro programme for PAYOFF-B

Status: **active empirical extension**. This programme does **not** alter the frozen PAYOFF-B theorem paper or its submission claim ceiling.

## Question

PAYOFF-B proves that the symmetric anti-phase two-patch model has one finite optimum in the dimensionless movement–environment variable u = m * tau, with u*(v) approaching 1.6061152988... under weak contrast and 1 under strong contrast.

The empirical macro question is therefore not "is natural migration exactly 1.606 times environmental change?" The testable question is:

> **Do migratory organisms show lowest phenological mismatch when their effective movement timescale is of the same order as the environmental phenology timescale?**

## Empirical bridge

For a spatial segment with common comparison length L,

~~~text
animal front speed       c_a = L / t_a
environmental-wave speed c_e = L / t_e
effective migration rate m   ~ 1 / t_a = c_a / L
environmental timescale  tau ~ t_e     = L / c_e
~~~

so

~~~text
u = m * tau ~ c_a / c_e.
~~~

Define the macro analogue

~~~text
u_macro = c_animal / c_environment
q       = log(u_macro)
~~~

This mapping is an **empirical analogue**, not an identity. It is most defensible when animal and environmental velocities are estimated over the same spatial support and their directions are aligned.

For two-dimensional fronts also define

~~~text
alignment = cos(theta_animal - theta_environment)

vector_mismatch
= |v_animal - v_environment| / |v_environment|
= sqrt(1 + u_macro^2 - 2*u_macro*alignment)
~~~

## Stage 1 — immediate macro reanalysis

Use the fully published dataset from Amaral et al. (2025), *Diversity and Distributions*, "Shifting Gears in a Shifting Climate: Birds Adjust Migration Speed in Response to Spring Vegetation Green-Up" (Dryad DOI 10.5061/dryad.ttdz08m6w).

The dataset contains eastern North American spring migration for 55 bird species across 2002–2017 and already supplies, at species × year × cell grain:

~~~text
vArrMag   bird migration-front speed (km/day)
vArrAng   bird velocity direction
vGrMag    vegetation green-up speed (km/day)
vGrAng    green-up direction
arr_GAM_mean
gr_mn
lag
cell_lat2
species
year
cell
mig_cell / breed_cell
HWI
Body_mass_g
winlat
~~~

The original paper tested whether green-up timing and velocity affect bird migration velocity and relative arrival. PAYOFF-B adds a different estimand: **the location and shape of the mismatch minimum along the movement/environment speed ratio**.

### H1 — finite timescale-matching optimum

Primary response:

~~~text
phenology_mismatch_days = abs(arr_GAM_mean - gr_mn)
~~~

Primary predictor:

~~~text
q = log(vArrMag / vGrMag)
~~~

Prediction: phenology mismatch is minimized at a finite, order-one speed ratio.

Primary inferential object:

~~~text
u_macro_star = exp(q_star)
~~~

estimated from the fitted response surface with uncertainty.

The PAYOFF-B interval 1 ... 1.606115... is a **theory reference**, not a preregistered empirical acceptance interval.

### H2 — direction matters

Timescale matching should perform best when the animal front and green-up front move in similar directions. Higher alignment should reduce mismatch and sharpen the speed-ratio optimum.

### H3 — climate-driven departure from matching

Within a species × cell, anomalously early or rapidly advancing green-up can move the environmental wave away from the species' historically realized movement response. Larger departure of q from the fitted optimum should predict larger absolute arrival/green-up mismatch.

### H4 — trait modulation is secondary

Use HWI, body mass, overwinter latitude, migration timing, and migration distance only as moderators of the ability to remain close to the fitted optimum. These are secondary comparative hypotheses, not required for the core PAYOFF-B test.

## Stage-1 primary models

Primary flexible model:

~~~text
abs_mismatch
~ s(q)
+ s(latitude)
+ greenup-date anomaly
+ range type
+ alignment
+ ti(q, alignment)
+ species random effect
+ species:cell random effect
+ year random effect
~~~

Quadratic companion:

~~~text
abs_mismatch
~ q + q^2
+ alignment
+ latitude
+ greenup-date anomaly
+ range type
+ (1|species)
+ (1|species:cell)
+ (1|year)
~~~

The quadratic vertex is

~~~text
q_star = -beta_q / (2 * beta_q2)
u_macro_star = exp(q_star)
~~~

Report the GAM minimum and quadratic vertex side by side. Do not call either an evolutionary optimum because the response is phenological mismatch, not measured fitness.

## Existing-source audit

The Amaral repository's generating code sets

~~~r
all$lag <- all$gr_mn - all$arr_GAM_mean
~~~

whereas its data dictionary describes lag with the opposite verbal sign. The absolute-mismatch analysis is unaffected, but all signed analyses must recompute the quantity directly from arr_GAM_mean and gr_mn rather than trusting the stored lag label.

The published velocity construction also applies:

~~~text
VALID_GAM == TRUE
green-up pixels gr_ncell > 10000
at least 5 neighbouring cells to estimate a velocity
velocity magnitudes > 3000 km/day set to missing
~~~

These source rules should be inherited before adding PAYOFF-B-specific filters.

## Stage 2 — global bird macroecology

Scale the same estimand globally using eBird Status and Trends weekly abundance surfaces and satellite land-surface phenology.

Candidate stack:

~~~text
animal front:
  eBird Status and Trends weekly relative abundance / proportion-population
  52 weeks, 3/9/27 km products
  thousands of globally modelled bird species

environment front:
  MODIS MCD12Q2 v6.1
  500 m annual green-up / midpoint / peak / senescence
  2001–2024

traits:
  AVONET
  BIRDBASE movement strategy
  migration-distance / wintering-latitude sources where licensing permits
~~~

Compute weekly animal front velocities and local phenology-front velocities on a common equal-area grid, then repeat H1–H3 across flyways, migratory strategies, and trophic guilds.

## Stage 3 — individual-level cross-taxon validation

Use public archived tracking datasets in the Movebank Data Repository as a mechanistic validation lane. Candidate taxa include ungulates, birds, and other seasonal migrants.

For each individual trajectory, annotate vegetation phenology and estimate movement velocity, local green-wave velocity, speed ratio, directional alignment, and days from the local phenology peak.

## Claim boundary

This programme tests whether phenological mismatch is minimized at a finite movement/environment timescale ratio, whether directional alignment strengthens that relationship, whether climate anomalies push species away from their fitted matching point, and whether traits explain among-species variation in tracking ability.

It does **not** establish that natural selection globally optimizes migration at the exact PAYOFF-B constant, that observed front-speed ratio is literally equal to m*tau in every system, that lower arrival/green-up mismatch is identical to higher lifetime fitness, or that the symmetric anti-phase theorem applies unchanged to continuous landscapes.

## Promotion criterion

Promote this empirical programme to a standalone macroecology paper when either the 55-species reanalysis recovers a clear finite order-one mismatch minimum not explained away by latitude, range position, or direction, or the global eBird × phenology analysis reproduces the same qualitative minimum across multiple flyways or migratory guilds.

A failure to find an order-one minimum is still informative: it identifies where the two-patch PAYOFF-B timescale mechanism does not transport cleanly into continuous migration.
