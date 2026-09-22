# Svalbard barnacle-goose raw-source receipt

Status: **raw GPS acquisition passed; environmental phase reconstruction remains the blocker**.

Dataset DOI: 10.5441/001/1.5k6b1364.

The public Movebank Data Repository bitstreams are downloaded directly in CI using the current DSpace bitstream API documented by the movepub workflow.

## GPS source

~~~text
GPS rows = 24,488
GPS columns = 17
individuals represented = 22
years represented = 6
time span = 2006-04-05 through 2011-06-18
rows with complete coordinates = 24,488
~~~

Detected core columns:

~~~text
timestamp
location-long
location-lat
individual-local-identifier
tag-local-identifier
utm-easting
utm-northing
utm-zone
study-local-timestamp
~~~

The data are hourly-to-multi-hourly GPS fixes rather than only stopover summaries, so segment-level movement and stopover reconstruction is feasible.

## Reference source

~~~text
reference rows = 22
reference columns = 20
~~~

Available metadata include:

~~~text
animal-id
tag-id
deploy-on-date
animal-life-stage
animal-mass
animal-ring-id
animal-sex
attachment-type
deployment-id
study-site
tag-mass
tag-readout-method
~~~

The deployment comments explicitly state that the analyzed data cover spring migration, approximately February through July.

## Important sample-size note

The 2015 paper reports N=21 tracked geese for the Svalbard population, whereas the current public Movebank source contains 22 individual identifiers.

Therefore the direct reanalysis must reproduce the original paper's track inclusion rules rather than assuming that every public deployment belongs to the published analytical sample.

## What can now be reconstructed directly

From the GPS source alone:

~~~text
individual spring tracks
daily / segment displacement
movement speed
stopover timing and duration
route progress
arrival dates in Norway / Svalbard regions
route-stage transitions
~~~

These are sufficient for the animal side of the controller model.

## Remaining blocker — environmental timing

The original paper derives annual onset of spring from GDD-jerk peaks for each stopover region.

The supporting file

~~~text
jane12281-sup-0001-SuppInfo.docx
~~~

contains:

~~~text
Table S1:
  average and SD of onset of spring by region

Tables S2–S7:
  annual onset-of-spring anomalies for pairs of regions

Figures S1–S4:
  annual / regional GDD-jerk timing
~~~

The publisher page exposes the supporting-file metadata but automated direct download currently returns HTTP 403.

Thus GPS acquisition is no longer the limiting step. The quantitative Tier-A upgrade requires either:

1. obtaining the supplementary regional onset table through an accessible archival copy;
2. reconstructing the original GDD-jerk onset from public meteorological data;
3. replacing the original GDD measure with a preregistered modern remote-sensing phenology product and treating it as an independent reanalysis.

## Preferred next implementation

Use the public GPS with a fresh, reproducible environmental phase surface rather than manually transcribing figure points.

For each year 2006–2011:

~~~text
identify migration / stopover segments
derive local environmental timing
calculate signed phase error E
calculate movement/environment speed ratio u
fit:
  log(u) ~ E + individual random effects
compare controller gain among route stages
~~~

The original Kölzsch predictability metrics remain a separate environmental-information axis.

## Claim boundary

Licensed now:

- raw Svalbard GPS and deployment metadata are programmatically accessible without a user account;
- sample density and temporal coverage are sufficient for direct movement reconstruction;
- 22 public individual identifiers span six spring seasons;
- the environmental timing surface, not animal movement data, is the remaining technical blocker.

Not licensed:

- a direct goose \(\kappa\), \(E_*\), or correction distance;
- reproduction of the original 21-goose analytical sample;
- substitution of a new environmental phenology metric without preregistration.
