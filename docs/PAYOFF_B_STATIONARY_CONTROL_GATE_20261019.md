# PAYOFF-B source-only stay-vs-move controls and hourly departure brackets

Date 2026-10-19. Written before extracting new matched-pair or hourly
bracketing outcomes; earlier V7R/V8 and stork precommitted tests were not
supported, and are not overwritten.

Three original CC0 GPS sources with immutable MD5 checks: Ciconia ciconia,
Anser albifrons, Numenius arquata. Previously verified 145/106/59 stationary
3-day -> northward next-2-day cases MUST be reproduced exactly.

A nondeparture reference window has identical first three stationary
days (all daily means within 30 km anchor) AND both following days within
30 km. Eligible matched control is in the same original animal-year,
same location within 30 km and 5-21 calendar days before the case.
Choose latest valid control for each case; deterministic SHA256 chooses one
case-control pair per animal-year, without weather values.

For each chosen case report the last GPS fix on stationary day inside 30km,
first GPS fix on next day outside 30km, and 6h/12h/24h bracketing counts.
A bracket is NOT a precise departure time. Reject windows when data are
missing or original hour stamps are inadequate; report exclusions rather
than relaxing 30km or 24h thresholds.

This case/control selection is inherently retrospective and conditions on
a bird ultimately migrating. Seasonal weather trends and site/time
differences remain confounding. No weather association, fitness,
causal information effect or full migration route inference is performed.

For a future exploratory matched-weather comparison, require >=10 distinct
animal-year pairs per source with <=24h departure brackets; failures are
legitimate. NASA POWER reanalysis may physically precede departure without
being the bird's actual perceived cue. Source privacy: no individual IDs,
source dates or exact habitat coordinates in artifact outputs.
