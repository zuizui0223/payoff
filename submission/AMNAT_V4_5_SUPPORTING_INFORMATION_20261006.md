# Supporting Information

## Seasonal tracking depends on information access and opportunities for correction

### Evidence-status key

**Preregistered / prospectively specified before outcome opening**
- source–destination detrended correlation contrast;
- frozen source-target mapping and admission rules;
- primary support rule.

**Posthoc diagnostics**
- day-scale variance decomposition;
- cross-validated forecast-value proxy G_CV;
- alternative baseline and source-rank sensitivities;
- temporal-order and observability audits;
- signed arrival–green-up timing decomposition;
- forecast-value-to-mismatch transfer and structural nulls;
- same-system stagewise population-front analyses;
- stagewise measurement-uncertainty and subset-selection audits.

**Published prior phenomenon with source-data reanalysis**
- mule-deer bidirectional compensation and resynchronization.

No posthoc analysis is relabelled as preregistered.

---

## S1. Frozen migratory-bird environmental analysis

### S1.1 Source and windows

Source:
Amaral et al. (2025) public `final.rds`, repository commit

`62c58d77c2028bd863dfe3697b0d9cf29ceaeab0`.

Windows:
- EARLY: 2002–2009;
- LATE: 2010–2017.

For each breeding-range target cell, the frozen mapping selected the nearest
lower-latitude migratory-range cell for the same species. Operational range
semantics followed the source analysis code. At least six finite paired annual
green-up observations were required in each window.

### S1.2 Primary sample

- 393 species-by-pair incidence rows;
- 166 unique spatial source-target pairs;
- 28 species;
- 26 species with at least three unique pairs.

### S1.3 Primary estimand

Source and target green-up dates were detrended separately within each period.
The primary environmental coordinate was the Pearson correlation of the paired
residual anomalies.

Primary result:

| quantity | early | late | late − early |
|---|---:|---:|---:|
| mean rho | 0.284 | 0.653 | +0.369 |

Pair-bootstrap 95% CI for delta-rho:
**+0.298 to +0.436**.

Species means:
- 26/28 positive;
- 2/28 negative.

### S1.4 Dependence audit

The positive period contrast remained under:
- source-cell cluster bootstrap;
- target-cell cluster bootstrap;
- two-way source × target robust uncertainty;
- 5° spatial blocks;
- 10° spatial blocks;
- global leave-one-calendar-year-out analysis.

Calendar-year omission:
- 16/16 omitted-year contrasts remained positive.

The primary result licenses a period contrast in standardized environmental
coupling, not climate-change attribution.

---

## S2. Metric-scale forecast diagnostics

All analyses in this section are posthoc.

### S2.1 Target variability

Detrended target anomaly SD:

| period | mean SD |
|---|---:|
| 2002–2009 | 2.412 d |
| 2010–2017 | 4.662 d |

Change:
**+2.250 d**, pair-bootstrap 95% CI **+1.946 to +2.549 d**.

### S2.2 Same-window descriptive regression

Mean source-to-target slope:
- early 0.399;
- late 0.640.

Mean R²:
- early 0.290;
- late 0.572.

Mean fitted residual RMSE:
- early 1.821 d;
- late 2.494 d.

Because model fitting and evaluation used the same short period, this RMSE is
descriptive and not out-of-sample forecast error.

### S2.3 Leave-one-year-out prediction

For each held-out year:
1. estimate source and target linear trends using all other years;
2. detrend training source and target observations;
3. fit target anomaly ~ source anomaly;
4. predict the held-out target with and without source information.

RMSE:

| model | early | late | change |
|---|---:|---:|---:|
| source-informed | 4.113 d | 4.168 d | +0.055 d |
| target-history only | 3.182 d | 5.865 d | +2.683 d |

The source-informed change has an interval spanning zero; the target-only
increase remains positive under all dependence-aware summaries.

### S2.4 Cross-validated forecast-value proxy

Define

`G_CV = MSE(target-history only) − MSE(source-informed)`.

This is a finite-sample restricted-model comparison and can be negative. It is
not the same object as a nonnegative population value of information.

Trend-baseline result:

| quantity | value |
|---|---:|
| early pair mean | −16.094 d² |
| late pair mean | +15.987 d² |
| delta | +32.082 d² |
| pair-bootstrap 95% CI | +21.040 to +46.796 d² |
| median delta | +15.843 d² |
| 10% trimmed mean | +20.871 d² |
| positive pairs | 139/166 |

Equal-species:
- delta +20.87 d²;
- 95% CI +16.37 to +32.48 d²;
- 25/28 species positive.

Exact 8/8-year subset:
- 58 pairs;
- delta +28.30 d²;
- all dependence-aware intervals positive.

Global year leverage:
- 16/16 year omissions positive;
- minimum mean delta +23.02 d²;
- minimum lower CI bound +15.05 d².

---

## S3. Forecast-value robustness

### S3.1 Alternative no-source baseline

Replacing the target linear-trend baseline with a target climatological mean:

- early G_CV = −5.01 d²;
- late G_CV = +17.36 d²;
- delta = +22.37 d²;
- 95% CI +18.13 to +26.78 d²;
- 136/166 pairs positive.

Equal species:
- delta +21.30 d²;
- 24/28 species positive.

The exact pair ranking is baseline-dependent, as expected for a value relative
to an alternative forecast, but the population-level direction is stable.

### S3.2 Source-rank sensitivity

On the common sample with the first three lower-latitude source ranks
estimable:

- 223 species-target rows;
- 22 species.

Mean delta G_CV:

| source rank | mean distance | delta G_CV |
|---|---:|---:|
| nearest | 469 km | +37.23 d² |
| second | 614 km | +33.46 d² |
| third | 732 km | +29.13 d² |

Equal-species nearest minus third-nearest:
**+10.68 d²**, 95% CI **+2.46 to +18.96 d²**.

Nearest minus second-nearest remained unresolved.

Interpretation:
the temporal increase is a regional nonlocal forecast structure, not a uniquely
identified biological cue site.

---

## S4. Temporal order and observability boundary

### S4.1 Source versus target environment

Across all 166 environmental pairs, source mid-green-up preceded target
mid-green-up by about 13.4 d on average.

- 158/166 pairs had positive mean source lead in both windows;
- 127/166 had source earlier in every paired observed year.

This establishes environmental temporal ordering only.

### S4.2 Same-species population-front subset

Requiring at least six annual arrival estimates at both source and target cells
in both periods admitted:
- 56 species-source-target units;
- 31 unique pairs;
- 14 species.

The estimated population front generally reached the source cell first:
- source-to-target front interval 7.20 d early;
- 5.69 d late.

### S4.3 Realized source-event observability

Annual ordering of source mid-green-up relative to the same species' population
front:

| order | early | late |
|---|---:|---:|
| source event before source-front arrival | 29.8% | 45.8% |
| source event between source and target arrivals | 29.6% | 18.3% |
| source event after target arrival | 41.6% | 36.1% |

Mean source event timing:
- early: 4.21 d after source-front arrival and 2.18 d before target arrival;
- late: 0.70 d after source-front arrival and 3.83 d before target arrival.

Therefore the reconstructed annual source mid-green-up is not demonstrated to
be an online cue available at the mapped source stage.

---

## S5. Signed bird timing

The transfer sample contained:
- 150 species-target rows;
- 72 unique environmental pairs;
- 22 species.

Signed lag was defined as:

`arrival − target mid-green-up`.

Period means:

| quantity | early | late | change |
|---|---:|---:|---:|
| target green-up | 130.98 | 128.67 | −2.31 d |
| bird arrival | 123.17 | 122.98 | −0.19 d |
| signed lag | −7.81 | −5.69 | +2.12 d |
| absolute lag | 8.42 | 8.07 | −0.35 d |

Signed-lag change:
95% pair-bootstrap CI **+1.41 to +2.77 d**.

Equal species:
- signed change +2.14 d;
- 20/22 species positive.

Because arrival was earlier than mid-green-up in both periods, decline in
absolute distance does not by itself demonstrate active tracking.

---

## S6. Forecastability-to-timing transfer

Posthoc model:
change in bird mismatch ~ standardized change in G_CV,
with equal total weight per species.

Day-scale raw coefficient:
**+2.43 d per SD delta G_CV**, 95% CI **+0.35 to +3.65 d**.

Fixed-arrival environmental null:
**+2.98 d**.

Observed minus fixed-arrival bird increment:
**−0.56 d**, 95% CI **−2.39 to +0.55 d**.

Within-window arrival permutations reproduced the raw positive coefficient.

Licensed conclusion:
larger route-level gains in analyst forecastability did not produce a detectable
bird-specific improvement beyond shared environmental geometry.

---

## S7. Same-system stagewise population geometry

Restricted sample:
- 31 pairs;
- 14 species.

Define local phase:
`e = arrival − local mid-green-up`.

Source phase:
- early −4.56 d;
- late −1.06 d;
- shift +3.50 d.

Target phase:
- early −8.14 d;
- late −6.00 d;
- shift +2.13 d.

Stage transformation:
`e_target − e_source`.

- early −3.57 d;
- late −4.95 d;
- change −1.37 d;
- pair-bootstrap 95% CI −2.36 to −0.36 d;
- 23/31 pairs more negative;
- 12/14 species more negative.

Descriptive attenuation fraction of the between-period source-stage phase
shift:
- 0.392;
- 95% CI 0.101 to 0.656.

This is a population-level stage-transformation statistic, not an individual
correction fraction.

### S7.1 Subset representativeness

Compared with excluded environmental pairs, the stagewise subset was:
- shorter distance: 495 vs 911 km mean;
- more strongly coupled late: rho 0.847 vs 0.608;
- less strongly increased in target variability.

Delta G_CV was similar:
- stagewise subset +26.61 d²;
- excluded +33.34 d²;
- standardized mean difference −0.078.

The stagewise subset should not be generalized mechanically to all 166 pairs.

### S7.2 Measurement uncertainty

Arrival posterior SD was larger early than late.

Posterior-normal propagation using the reported arrival means and SDs:
- 5,000 simulations;
- pair-mean stage-transformation change median −1.37 d;
- 95% Monte Carlo interval −2.04 to −0.71 d;
- fraction below zero = 1.000.

Inverse-variance weighting:
- pair estimate −0.92 d;
- 95% interval −1.91 to +0.12 d.

Thus direction survives direct posterior-normal propagation but strength is not
invariant to precision weighting.

### S7.3 Retention-slope non-identifiability

Raw source-to-target phase-retention slopes were not interpreted
mechanistically. In the early period, expected predictor measurement-error
variance exceeded the residual source-phase variance required for a classical
errors-in-variables correction. In the late period the corrected slope was
approximately the fixed-arrival environmental null.

No bird controller gain is claimed.

---

## S8. Mule-deer source-data reanalysis

Source:
Ortega et al. (2023) public Source Data.

Sample:
- 152 animal-years;
- 72 adult females.

Phase contraction:

| quantity | value |
|---|---:|
| start phase SD | 26.41 d |
| end phase SD | 13.17 d |
| end/start variance ratio | 0.249 |
| 95% animal-cluster CI | 0.167 to 0.362 |
| within-year variance ratio | 0.294 |
| whole-route phase slope lambda | 0.107 |
| lambda 95% CI | 0.013 to 0.209 |
| ended closer to peak | 70.4% |
| mean absolute start phase | 21.91 d |
| mean absolute end phase | 11.12 d |

Signed actuators:

| response | slope per start-phase day | 95% CI |
|---|---:|---:|
| movement rate | +0.0683 km d^-1 | +0.0554 to +0.0800 |
| stopover duration | −0.492 d | −0.569 to −0.412 |

The published phenomenon of compensation/resynchronization is prior art. The
reanalysis provides the continuous signed-phase representation used by the
current framework.

---

## S9. Reduced-model theory boundary

Let:
- G_E(t): ideal-observer environmental value under a declared decision problem;
- G_O(t): organismally accessible information value;
- r(t): retained actionability;
- C(t): direct waiting cost.

For nested information sets under the same loss/action problem:

`0 <= G_O(t) <= G_E(t)`.

This is established value-of-information monotonicity.

Reduced seasonal specialization:

`N(t) = r(t) G_O(t) - C(t)`.

Interior condition:

`r G_O' = -r' G_O + C'`.

For the declared exponential accessible-information/actionability special case:

`t* = log(1 + alpha/beta) / alpha`.

These equations are not claimed as a new general theory of information or
optimal stopping.

---

## S10. Claim boundary summary

The current paper directly supports:
- stronger standardized environmental coupling between periods;
- greater target environmental variability;
- larger analyst forecast value of reconstructed nonlocal environmental
  structure;
- incomplete online observability of the reconstructed source event;
- limited population arrival shift relative to target-green-up advance;
- population-level timing transformation across stages in a restricted subset;
- individual signed phase correction in mule deer as a published independent
  mechanism anchor.

The current paper does not directly identify:
- which cues birds perceive;
- organismal information value G_O in birds;
- actionability r(t) in birds;
- individual bird feedback gain;
- climate-change causation of period contrasts;
- a natural estimate of the theoretical t*.
