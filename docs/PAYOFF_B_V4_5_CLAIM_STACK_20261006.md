# PAYOFF-B V4.5 claim stack — 2026-10-06

Status: **CURRENT JOURNAL-FACING CLAIM BOUNDARY**

## Central ecological question

**What determines whether a forecastable seasonal environment becomes
phenological adjustment?**

## Four-layer architecture

1. **Environmental forecastability**  
   External environmental structure can reduce prediction loss for an ideal
   observer.

2. **Organismal information access**  
   Only information actually encountered or inferred by the organism can enter
   its decision process.

3. **Retained actionability**  
   Even accessible information matters only while useful timing responses
   remain feasible.

4. **Correction**  
   Residual phase error can then be altered, retained, or amplified.

These layers are not interchangeable.

## Claim 1 — environmental coupling strengthened

Evidence class:
**preregistered environmental primary result**

Licensed:
> Detrended source–destination spring correlation increased from 0.284 to 0.653
> between 2002–2009 and 2010–2017 in the sampled network.

Robustness:
- pair bootstrap;
- source/target/two-way clustering;
- 5° and 10° spatial blocks;
- calendar-year omission;
- remote-sensing support diagnostic.

Not licensed:
- climate-change causation;
- higher rho means lower absolute forecast error;
- birds used this signal.

## Claim 2 — destination spring became more variable

Evidence class:
**posthoc metric-scale diagnostic**

Licensed:
> Detrended target green-up SD increased from 2.41 to 4.66 d.

## Claim 3 — analyst forecastability increased

Evidence class:
**posthoc cross-validation**

Operational proxy:

    G_CV
      =
    MSE(target-history only)
      -
    MSE(source-informed analyst forecast).

G_CV is a finite-sample restricted-model forecast comparison and can be
negative. It is **not** the same object as the nonnegative theoretical
value-of-information quantity G_E.

Primary trend-baseline result:
- -16.1 -> +16.0 d^2;
- delta +32.1 d^2;
- median delta +15.84 d^2;
- 10% trimmed mean +20.87 d^2;
- 139/166 pairs positive.

Equal species:
- delta +20.87 d^2;
- 25/28 species positive.

Alternative climatological baseline:
- delta +22.37 d^2;
- 24/28 species positive.

Exact-complete:
- delta +28.30 d^2;
- all 16 year omissions retain positive intervals.

Source-rank sensitivity:
- rank 1 +37.23 d^2;
- rank 2 +33.46 d^2;
- rank 3 +29.13 d^2;
- nearest minus third-nearest equal-species contrast +10.68 d^2,
  CI +2.46 to +18.96.

Licensed:
> Regional nonlocal environmental structure gained marginal held-out predictive
> value.

Preferred wording:
**forecast-value proxy**, **ideal-observer forecastability**, or
**marginal predictive value**.

Not licensed:
- organismal fitness value of information;
- a true cue site;
- biological information access.

## Claim 4 — forecastability does not imply cue observability

Evidence class:
**posthoc source-event observability audit**

Restricted stagewise subset:
- 31 pairs;
- 14 species.

Annual source mid-green-up before source-front arrival:
- early 29.8%;
- late 45.8%.

Annual source mid-green-up between source- and target-front arrival:
- early 29.6%;
- late 18.3%.

Annual source mid-green-up after target-front arrival:
- early 41.6%;
- late 36.1%.

Mean event order:
- early: source mid-green-up 4.21 d after source-front arrival and 2.18 d before
  target-front arrival;
- late: 0.70 d after source-front arrival and 3.83 d before target-front
  arrival.

Licensed:
> The reconstructed predictor is retrospectively forecastable but its realized
> annual event is not consistently an online cue available at the mapped source
> stage.

Not licensed:
- birds observed source mid-green-up;
- G_CV estimates organismal information access.

## Claim 5 — bird arrival changed little while target green-up advanced

Evidence class:
**posthoc signed timing decomposition**

Transfer sample:
- 150 species-target rows;
- 72 pairs;
- 22 species.

Target green-up:
- shift -2.31 d;
- CI -2.58 to -2.08.

Bird arrival:
- shift -0.19 d;
- CI -0.95 to +0.52.

Signed lag:
- -7.81 -> -5.69 d;
- shift +2.12 d;
- CI +1.41 to +2.77.

Equal species:
- signed shift +2.14 d;
- 20/22 species positive.

Licensed:
> The estimated population arrival front changed little while the environmental
> target advanced, shifting relative arrival timing.

Do not label zero phase as optimal.

## Claim 6 — absolute mismatch stability is not active tracking evidence

Absolute mismatch:
- 8.42 -> 8.07 d unweighted;
- equal-species change -0.63 d.

Because the population front was early relative to mid-green-up in both periods,
an advancing target moved toward a largely unchanged arrival schedule.

Licensed:
> Stable absolute distance does not demonstrate active adjustment.

## Claim 7 — route-level forecastability did not transfer detectably to bird timing

Evidence class:
**posthoc transfer + structural nulls**

Observed day-scale beta:
- +2.43 d per SD delta G_CV.

Fixed-arrival null:
- +2.98 d.

Bird-specific increment:
- -0.56 d;
- CI -2.39 to +0.55.

Permutation:
- observed positive slope ordinary under null.

Licensed:
> Larger gains in analyst forecastability did not produce detectable
> bird-specific mismatch improvement beyond shared environmental geometry.

## Claim 8 — same-system population timing transforms across stages

Evidence class:
**posthoc restricted stagewise analysis**

Restricted subset:
- 31 pairs;
- 14 species;
- selected toward shorter routes and stronger late coupling.

Front interval:
- 7.20 -> 5.69 d.

Green-up interval:
- 10.78 -> 10.64 d.

Stage transformation:
- -3.57 -> -4.95 d;
- change -1.37 d;
- CI -2.36 to -0.36.

Descriptive attenuation of between-period source-stage phase shift:
- A = 0.392;
- CI 0.101 to 0.656.

Measurement boundary:
- posterior-normal propagation retains negative change in all 5,000 draws;
- inverse-variance weighting retains negative point estimate but interval crosses
  zero;
- source-to-target retention slopes are not mechanistically identifiable under
  the reported arrival uncertainty.

Licensed:
> Population-level relative timing changed across mapped stages rather than
> being identical at source and target.

Not licensed:
- individual feedback correction in birds;
- controller gain;
- extrapolation to all 166 pairs.

## Claim 9 — individual signed correction exists in mule deer

Evidence class:
**published prior art + independent source-data reanalysis**

Licensed:
- phase variance contracts;
- early and late individuals adjust speed in opposite directions;
- stopover use changes in the opposite signed direction;
- mean absolute phase error declines.

Not licensed:
- discovery of the phenomenon;
- identification of bird mechanism;
- natural G_O(t) or r(t).

## Claim 10 — accessible information and actionability jointly determine usable value

Evidence class:
**reduced theoretical specialization**

Let G_E(t) be ideal-observer environmental forecastability and G_O(t)
organismally accessible information value.

For nested information sets under the same loss/action problem:

    0 <= G_O(t) <= G_E(t).

This is established value-of-information monotonicity. It does not imply that
the empirical finite-sample G_CV proxy must be nonnegative.

Reduced seasonal model:

    N(t) = r(t) G_O(t) - C(t).

Interior balance:

    r G_O' = -r' G_O + C'.

Exponential special case retains:

    t* = log(1 + alpha/beta) / alpha.

Licensed:
> In the declared reduced model, accessible information can increase while
> actionability declines, creating an intermediate stage of maximal usable
> information.

Not licensed:
- a new general VOI theorem;
- natural t* estimate.

## Submission headline

Preferred title:

> **Seasonal tracking depends on information access and opportunities for
> correction**

One-sentence contribution:

> **Environmental forecastability, organismal information access and correction
> opportunity are distinct layers of seasonal tracking; the current bird data
> identify the first and population-level timing geometry, while mule deer
> anchor individual downstream correction.**

## What the paper is not

Do not sell as:
- discovery of spatial synchrony;
- discovery that variability changes information value;
- discovery of feedforward versus feedback;
- proof that birds used the reconstructed source predictor;
- proof that actionability loss caused the bird pattern;
- direct measurement of organismal information value in birds.

The contribution is the empirical and theoretical separation of
**forecastability, accessibility, actionability and correction**.
