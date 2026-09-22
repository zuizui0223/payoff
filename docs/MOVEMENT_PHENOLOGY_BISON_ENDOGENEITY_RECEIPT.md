# Yellowstone-bison endogenous-wave boundary receipt

Status: independent boundary-case evidence. This system is **not** eligible for the exogenous-wave controller meta-analysis without a coupled animal–vegetation model.

Sources:

- Geremia et al. (2019), *PNAS*, DOI 10.1073/pnas.1913783116.
- Dryad DOI 10.5061/dryad.prr4xgxgz.

## Data availability

The public Dryad release contains:

~~~text
bisonsurfdata.csv
  animal id
  year
  animal-location Julian day
  local peak-IRG Julian day

fullspringbisonsurfdata.csv
  same variables for the expanded spring analysis

functionalNDVIdata.csv
  site/year NDVI time series
  bison-use index
  climate and terrain covariates

grazingexperimentdata.csv
  paired grazed / exclosure plot observations

grazingintensitydata.csv
  field grazing intensity and modeled bison-use index

Run_analyses.R
  native replication code
~~~

Current Dryad file-stream downloads return an authenticated-session requirement in automated retrieval, so this branch records the data contract and published result rather than silently scraping around that gate.

## Published movement result

Bison do not behave as simple passive surfers of an externally imposed green wave.

The study reports that:

1. most bison tracked the spring wave early in the season;
2. later, bison slowed and allowed the remotely sensed green wave to pass;
3. forage quality nevertheless remained high in heavily grazed areas.

A purely exogenous-wave controller would interpret point 2 as tracking failure.

The grazing experiments show why that interpretation is wrong.

## Published environment-feedback result

Small-scale grazing experiments showed that grazing can sustain high-quality forage.

At landscape scale, a roughly sixfold decadal increase in bison density was associated with intense grazing that caused grasslands to green up:

~~~text
faster
more intensely
for longer
~~~

Thus animal movement and density alter the environmental timing surface itself.

## Coupled-dynamics interpretation

The exogenous controller model is

\[
\frac{dE}{ds}
=
\frac{1/u(E)-1}{c_e},
\]

with \(c_e\) treated as an environmental input.

For ecosystem engineers such as bison, this must become a coupled system:

\[
\frac{dE}{ds}
=
\frac{1/u(E,R)-1}{c_e(R,B)},
\]

where

~~~text
R = local resource state
B = grazing intensity / bison use
~~~

and resource dynamics satisfy schematically

\[
\dot R
=
F(R,\text{climate})
+
H(R,B).
\]

Now the animal changes the wave that it appears to be "tracking."

## Consequence

A large mismatch from satellite peak-IRG does not necessarily indicate poor resource matching.

The animal can remain in high-quality forage by **engineering** a local resource state whose timing is no longer captured by the untreated/exogenous green-wave trajectory.

This creates a distinct migration strategy class:

~~~text
ENGINEER
modify the resource wave so that the animal–resource phase relationship
cannot be interpreted with an externally imposed c_e alone
~~~

The current strategy set becomes:

~~~text
SURF      continuous tracking of an exogenous wave
STEP      stopover-to-stopover phase control
JUMP      rapid relocation, then phase reacquisition
OVERTAKE  deliberately change target phase along route
ENGINEER  alter the environmental wave itself
~~~

## Why this matters for macroecology

Cross-taxon movement–phenology studies often use remotely sensed vegetation phenology as if it were an external covariate.

Bison show a clear failure mode of that assumption.

Therefore every candidate system should be assigned an **environment-endogeneity flag** before entering a controller meta-analysis.

Systems with strong endogeneity should not be pooled directly with exogenous-wave systems.

## Empirical test generated

A direct bison reanalysis can test whether apparent phase mismatch increases with grazing intensity while local forage-quality metrics remain high.

If so:

~~~text
satellite phase mismatch ↑
while realized forage quality remains stable/high
~~~

would be diagnostic of environmental engineering rather than controller failure.

## Claim boundary

Licensed:

- published bison movements cease close surfing later in spring;
- grazing feedback sustains forage quality;
- higher bison density modifies the shape and duration of vegetation green-up;
- the system violates the exogenous-environment assumption used by the simplest phase-locking model.

Not licensed:

- a new estimate of bison \(\kappa\), \(E_*\), or correction distance;
- inference that bison movement is maladaptive because satellite-phase mismatch increases;
- quantitative comparison with the mule-deer controller before resource feedback is modeled.

## Promotion rule

Treat Yellowstone bison as a formal boundary/falsification system. It enters quantitative comparison only through a coupled animal–resource model, not through the exogenous-wave controller registry used for ordinary surfers.
