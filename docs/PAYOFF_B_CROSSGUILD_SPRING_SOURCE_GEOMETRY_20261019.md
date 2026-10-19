# PAYOFF-B normalized northward source-geometry gate

Date 2026-10-19. This rule is frozen before any new natural trajectory
statistics are calculated. Four nonidentical archives:
Rotics 2018 Ciconia ciconia published GPS,
Schwemmer 2021 Numenius arquata published GPS,
USGS Scolopax minor published Argos (NOT equivalent accuracy to GPS),
and mixed Anas acuta/Anas platyrhynchos published GPS.

Original CC0 files are re-downloaded with the source-specific frozen MD5 and
byte counts. No animal identity or raw coordinate leaves the isolated job.

For each source animal-name identity x calendar-year with February-May GPS
or Argos fixes, daily mean latitude is computed, requiring:
- 12 or more distinct calendar dates observed in February-May;
- difference of daily-latitude 90th minus 10th percentile >=10 degrees;
- median last-five minus first-five daily latitudes >=7 degrees northward;
- first observed day below the 20% latitude-progress threshold;
- observable ordered 20% and 80% checkpoint crossings.

Report all failure categories, including left censoring and insufficient
sampling. Do not choose a subset after checking correlations with breeding
or environmental outcomes; none is opened in this source-only check.
All taxon names are kept as declared by original event metadata.
If one published package contains two taxa, it must not be treated as one
taxon in later models.

These latitude-threshold intervals are neither independently validated
migration legs nor arrival at breeding territory. Argos measurement accuracy,
sampling effort, annual site fidelity and actual route boundaries require
separate checks. No movement controller gain, cue availability, fitness
or species-common ecological effect may be inferred from this gate.

Earlier source-specific stork January-April 53-season audit uses a DIFFERENT
winter-referenced definition and must NOT be pooled with these normalized
within-February-May proxies as if interchangeable.
