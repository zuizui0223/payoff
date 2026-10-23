# PAYOFF-B: across-taxon observational timing retention, exploratory contract

Created 2026-10-19 **before estimating any of these cross-system slopes**.
Unlike the separately precommitted 53-season winter-referenced stork pilot,
this across-taxon analysis was chosen **after source-geometry QC had been
opened** and is therefore explicitly exploratory.

## Biological question

When an animal reaches the first 20% of its observed northward movement
range earlier or later than conspecifics in the same year, does the timing
difference retain its scale by the 80% point? This assesses timing
propagation across systems, not the environment→information→decision process.

## Original source sets and unmodified inclusion thresholds

Use *exactly* the frozen Feb–May 20%/80% original source cohorts:
- Ciconia ciconia (Rotics 2018, GPS): 91 source pairs.
- Scolopax minor (published Argos, NOT independent of its GPS stream):
  37 source pairs.
- Anser albifrons (Kölzsch 2016, GPS): 23 source pairs, potential
  overlap with prior PAYOFF goose cohorts.
- Numenius arquata (Schwemmer 2021, GPS): 7, expected NOT_ESTIMABLE.
- Anas acuta / A. platyrhynchos mixed GPS package: zero, expected
  NOT_ESTIMABLE; no pooling of two species.

One source-animal identity in a calendar year = one timing pair; never
count separate fixes as independent observations. All missing/censored
years and source statuses remain in the output. Sensors remain separate.

## Fixed pilot model and scientific ceiling

Within each original taxon separately:
  T80_i,y = alpha_y + beta T20_i,y + error_i,y

Year fixed effects; normalize Feb–May DOY to a 365-day clock. Minimum
admission: >=20 pairs, >=10 distinct animals and >=3 study years,
otherwise NOT_ESTIMABLE; no adaptation of thresholds or data collection
once effect signs are seen. Report individual-level clustered 2,000
bootstrap 95% interval and invalid draws.

Re-run source file checksum verification before any effect fitting;
verify original included pairs equal frozen source counts. Do not fit
a species-pooled effect or a single cross-species p-value. Differences
in corridor, geolocation accuracy, seasonal observation window and
source sampling are major confounders.

beta<1 can arise from mechanically conditioning Y <= the study-window
end, even with independent departure and transit duration; see
docs/PAYOFF_B_STAGE_TIMING_WINDOW_NULL_20261019.md.
Thus beta<1 only describes sample-stage temporal compression. It
CANNOT establish active timing correction, forecast skill, ecology
of environmental information, local cue use, fitness benefit, or a
generalizable selective evolutionary law.

The original 53-season stork pilot retains its own pre-outcome lock
and verdict; do NOT choose whichever stork sample gives a more
favorable coefficient.
