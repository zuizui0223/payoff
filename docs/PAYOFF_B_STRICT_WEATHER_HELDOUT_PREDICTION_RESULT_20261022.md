# PAYOFF-B: does physically available prior weather predict departure beyond site and season?

**2026-10-22 | Published public CC0 GPS sources | Exploratory held-out prediction, NOT a causal bird-information test**

Original source state, corrected BEFORE this result: all three prior anchor days must contain *only* GPS fixes within 30km of the source reference circle. The original day4/day5 northward proxy and two-day continued-stay proxy are kept fixed, with all other outcomes/censoring excluded rather than made stays. Eligible comparison populations: **801 stork, 1,417 white-fronted goose, 1,627 curlew observation days (3,845 in total)**.

This follow-up was designed after earlier exploratory mean-weather patterns. It is not a previously preregistered clean confirmatory test. The predictor run-age was specifically corrected to compute the sequence of strict GPS source eligibility days **before** filtering to the future-assigned movement/stay class; this prevents accidental leakage of future GPS categories into a predecision feature.

## Fixed weather-value prediction

Baseline inputs: season as day-of-year sine/cosine, coarse original source position as latitude/circular longitude (private), and the log length of the past strict stationary-source eligibility run. Additional physical weather inputs: NASA POWER daily T2M, WS10M, V10M and incoming solar radiation, each as previous-day level and anomaly vs previous seven days. No departure-day/future weather or tracking is a predictor.

Two identical ordinary L2 logistic models (C=1, train-only feature standardization) were compared on **entire held-out original calendar years** within each bird source; another grouped split held out entire animal IDs. Improvement = baseline predictive loss minus weather-augmented loss; positive indicates predictive improvement.

| Taxon | Strict source cases/stays | Entire-year-heldout tested risk days | Heldout-year log loss baseline | Baseline+physical-weather | Incremental log-loss skill |
| --- | --- | ---: | ---: | ---: | ---: |
| *Ciconia ciconia* | 85/716 | 801 | 0.288070 | 0.290721 | **−0.002651** |
| *Anser albifrons* | 93/1324 | 1406 | 0.273173 | 0.290555 | **−0.017382** |
| *Numenius arquata* | 42/1585 | 1627 | 0.103491 | 0.103512 | **−0.000021** |

Year CV folds admitted: stork 5/5, goose 4/5, curlew 7/7; the single excluded goose fold failed the original minimum positive/day gate, without changing thresholds. In no source did the eight physical weather variables improve held-out-year **log loss** versus the site/season/history baseline. Curlew's Brier score improved slightly (+0.000521) despite its negligible negative log-loss difference, so the finding is metric-dependent at small magnitudes.

### Dependence on the generalization target

Holding out original **animal identities** instead of whole source years changed the signs of some gains: stork +0.004178 log loss, goose −0.000653, curlew +0.002751. These are small observational predictive scores on distinct splits, NOT statistical evidence of weather causation. Neither split creates an independent study or fully controls shared regional weather/years.

**Supported ecology:** Across the three recorded cohorts, in this specifically fixed model and after excluding falsely stationary GPS states, past local physical weather did **not** provide a consistently transportable incremental prediction of the two-day northward-source indicator into held-out years. This highlights why available climatic measurements, statistical association, and **usable predictive information** must be separated in full-annual-cycle migration ecology.

**Unsupported interpretation:** This does NOT mean birds ignore weather, all climate forecasts lack value, information cannot assist migratory adaptation, or the PAYOFF-B game-theoretic information/recourse/deadline mechanism is falsified. The current physical reanalysis is not what the birds demonstrably perceived, GPS northward transitions are not validated commitment, and no destination phase/remaining speed or stopover correction/fitness endpoints are linked.

Main next scientific goal is a genuinely separate high-frequency cohort with validated departure decisions and predecision cue availability, then a prospective held-out test of signal value and independent feasible correction, without selecting weather features after viewing source effect directions.

Source workflow: https://github.com/zuizui0223/payoff/actions/runs/39787458090

Machine-readable complete original source QC and predictive scoring:
`data/payoff_b_strict_weather_heldout_predictive_result_20261022.json`.
