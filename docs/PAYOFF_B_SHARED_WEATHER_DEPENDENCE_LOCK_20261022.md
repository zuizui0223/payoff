# PAYOFF-B shared-weather-cluster and within-bird sensitivity protocol

Locked 2026-10-22 **after observing** the earlier full source weather
patterns and animal-cluster bootstrap. This is therefore a POST-OUTCOME
ROBUSTNESS AUDIT, not another independent ecological confirmation.

## Scientific failure mode

One GPS bird contributes many overlapping stationary 3-day risk windows.
Different birds can additionally share the **same physically reconstructed
weather** at a 0.5° grid and calendar time. Whole-individual history
resampling is not sufficient to address the latter covariance; the
earlier animal-bootstrap "95% intervals excluding zero" are descriptively
interesting but can understate uncertainty when entire weather events are
shared by different animals.

## Source and unchanged estimand

Read all original MD5-validated GPS and NASA POWER *daily* physical fields
again, using exactly 343/334/132 original 0.5-degree year-month batches.
All source entry/label counts, no future weather for predictors, and all
previous original source effects are cross-checked numerically. Fail closed
if any source/weather batch is missing rather than subtly alter population.
The dependent variable remains a retrospective two-day northward *label*,
not a verified choice, outcome fitness or observed signal.

The original estimand is the case-weighted average of (northward source
day mean weather anomaly minus continuing-stay day mean anomaly) within
0.5° grid × calendar year × calendar month strata with BOTH outcomes.

## Fixed sensitivity contrasts

1. Treat the original full fine 0.5° grid-year-month stratum as ONE weather
   block, regardless of number of birds or risk days therein.
2. Treat all fine strata within a common contiguous *2-degree*
   latitude-longitude weather supercell in the SAME year and month
   as ONE spatial-temporal weather block.
3. Treat all fine strata across a source's geographic cells in the same
   calendar *year-month* as ONE broad shared-weather episode.

Resample each block scale with replacement 3,000 times (fixed seed
20261022), weighting each fine stratum by its original case-day count.
These are descriptive percentile intervals and are reported only with
at least 10 original weather blocks and at least 95% valid replicates.
Return source-block count, Kish-like effective case-weighted block
size, maximum single-block weight share, bootstrap intervals and
leave-one-weather-block-out ranges and sign consistency.

Separately estimate the same source contrast using only those
**individual × 0.5° grid × calendar year × calendar month** records
containing both an observed northward future-GPS label and a
continued-stay label of the SAME animal. Require >=10 such strata and
>=10 distinct animals, or mark NOT_ESTIMABLE; do not lower thresholds
to get a favorable sign. This reduces between-bird confounding but
still conditions on animals present at the site and time, and will
not eliminate gradual calendar readiness changes.

## Explicit identification ceiling

No source block has been established to be independent in real weather;
adjacent cells, successive months and distant correlated pressure systems
can violate every scheme. Unlike experimental randomization, the
retrospective original risk-set contrasts do not identify a causal
local cue, learned forecast, actual migration choice, active
compensation/recourse, reproductive effect or PAYOFF-B evolutionary
game-theoretic coordination. Prior V7R/V8 and the originally registered
stork-53 non-support must remain unchanged.

No original animal IDs, case event dates, cell/grid coordinates or
individual weather values are exported. Aggregate diagnostics and full
source operational failures alone are permissible.

Scripts: scripts/audit_payoff_b_weather_block_dependence.py,
tests/test_payoff_b_weather_block_dependence.py.
