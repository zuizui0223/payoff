# PAYOFF-B empirical decision: prior-weather forecasting is not a validated information mechanism

**2026-11-14 | source-backed re-audit of opened 2026-10-22 CC0 GPS forecast receipts**  
**Status:** exploratory observational re-analysis; no newly opened animal outcomes; not an independent meta-analysis.

## Tested biological question

Does physically recorded weather *before* a GPS movement proxy improve out-of-calendar-year prediction of that proxy beyond season, location and prior stationary run-age?

The source analyses fixed L2-logistic baseline and eight NASA POWER prior-weather features and tested whole heldout calendar years, using strict original fix-level stationary eligibility. The present audit rereads the original aggregate JSON and verifies all split definitions, signs, denominators and sample accounting; it does not refit raw animal trajectories.

| Taxon | Year-heldout evaluated risk days | Log-loss improvement (baseline minus weather model) | Animal-heldout improvement |
| --- | ---: | ---: | ---: |
| Ciconia ciconia | 801 | -0.002651 | +0.004178 |
| Anser albifrons | 1406 | -0.017382 | -0.000653 |
| Numenius arquata | 1627 | -0.0000206 | +0.002751 |

All three source-specific year-heldout log-loss differences are nonpositive; two change sign under animal-heldout CV. Original 3845 strict case/stay days become 3834 tested year-fold days because a previously gated goose fold excludes 11. These are different generalization questions; neither proves birds ignore meteorology.

The equal-taxon descriptive average and day-weighted descriptive average are emitted by the executable audit. The latter is **not** a pooled independent biological effect, because observations share animals, weather episodes, sites and calendar years. No new confidence interval, P-value, effect discovery or causal information coefficient is claimed.

## Exact biological promotion gate

**Information / q:** historical meteorological reanalysis may be available to an analyst but does not establish that the bird perceived it or possessed the fitted statistical forecast. Distinguish observed physical weather from *information available at decision time*. For new independent cohorts, predeclare cue onset, source location, timestamp, training-year cutoff, and heldout forecast skill.

**Capacity / recourse:** GPS northward source labels are not the set of *alternative feasible* future movements. Estimate stage-specific available travel-speed, stopover and route options independently of the focal bird's realized future movement; retain signed advance and delay.

**Coordination / partner payoff:** a migrating bird and local resource/partner must have independently dated interaction or resource phenology, with matched temporal scale. Environmental green-up is not automatically fitness-optimal resource timing.

**Fitness:** reproductive/survival records must be linked to the same independently validated individual/season. Fledgling counts are reproductive output, not lifetime fitness. Shared tags and prior cohort overlap require source reconciliation.

**Independence:** earlier Kölzsch/Amaral, Rotics and already opened CC0 samples cannot be called untouched replication. The 2016/2018 stork reference audit found 35 shared tag IDs and two comparable overlapping deployment intervals; identity namespace unresolved. Avoid combining them as independent cohorts.

## Scientific conclusion and stop/go

The **observed negative year-heldout skill** means that this particular eight-variable prior-weather model did not reliably transport its incremental predictive performance to unseen years in the three recorded taxa. It is not evidence of zero true bird information, and it does not identify the mathematical information/capacity/coordination deficit shares from PR #340.

The next legitimate biological coefficient requires a truly independent source that passes cue chronology, independent recourse, destination/partner alignment and outcome availability *before* fitting. If these gates fail, report the data-availability limit; do not relax the requirements or use post-hoc weather directions to promote a mechanism.

## Reproducibility

Input: `data/payoff_b_strict_weather_heldout_predictive_result_20261022.json` on the parent empirical branch.  
Audit: `python scripts/audit_payoff_b_empirical_forecast_gate_20261114.py`  
Tests: `pytest -q tests/test_payoff_b_empirical_forecast_gate_20261114.py`

All source animal IDs, coordinates, raw GPS fixes and sensitive locations remain outside the repository.

This branch is based on the still-Draft independent tracking PR #336, not on main. Do not merge it independently into main or confuse its source-dependent diff with a new observational sample.
