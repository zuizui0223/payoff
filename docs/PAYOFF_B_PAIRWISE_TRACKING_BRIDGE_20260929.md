# PAYOFF-B interaction-level pairwise tracking bridge

Date: **2026-09-29**  
Status: **source-backed bridge ready; not a new PAYOFF-B discovery**

## Why this source matters

E6 established two natural gradients: predictive connectivity and migration
distance. Those are useful, but neither directly observes two interacting
partners changing at different rates.

Burgess et al. (2018; DOI 10.1038/s41559-018-0543-1) is closer to the
theoretical object because it analyses actual trophic pairs. Their bivariate
mixed models estimate how first-egg date in three insectivorous birds changes
among years with the timing of peak caterpillar biomass.

The relevant null is **perfect pairwise tracking**:

```text
major-axis slope = 1
```

A slope below one means that bird phenology changes less among years than the
caterpillar resource, so relative timing must change as spring phenology moves.

## Published temporal tracking results

| interaction | temporal correlation | major-axis slope | 95% credible interval | tracking deficit (1 - slope) |
|---|---:|---:|---:|---:|
| Caterpillar → Blue Tit | 0.800 | 0.510 | 0.236–0.770 | 0.490 |
| Caterpillar → Great Tit | 0.717 | 0.515 | 0.109–0.904 | 0.485 |
| Caterpillar → Pied Flycatcher | 0.911 | 0.348 | 0.210–0.490 | 0.652 |

All three temporal major-axis intervals are below one.

The source paper gives the same result in directly ecological units: for every
10-day advance of the caterpillar peak, Blue Tit, Great Tit and Pied
Flycatcher first-egg dates advance by about **5.1, 5.2 and 3.5 days**,
respectively. Thus a 10-day earlier resource year increases the relative timing
gap by about **4.9, 4.8 and 6.5 days**.

Mean predicted peak-demand minus peak-resource timing is approximately:

- Blue Tit: **+7.22 d** (95% CrI -2.35 to +11.82);
- Great Tit: **+6.30 d** (+0.09 to +12.32);
- Pied Flycatcher: **+16.41 d** (+10.49 to +22.12).

The source concludes that earlier, warmer springs increase bird-caterpillar
asynchrony, and that Pied Flycatcher has the shallowest temporal tracking slope.

## What this adds to PAYOFF-B

This source closes part of the reviewer-identified gap:

```text
E6:
different information positions / migration classes
        ↓
different response levels

Burgess bridge:
actual interacting pair
        ↓
different year-to-year response magnitude
        ↓
larger relative timing mismatch
```

So the natural evidence is no longer restricted to **levels**. There is
published interaction-level evidence that a **difference between partners'
phenological responses** produces mismatch.

## What it still does not test

It does **not** measure the theoretical waiting-cost difference `D2-D1`.

It does **not** observe the exact information-use thresholds `q1` and `q2`
or the predicted `q1 < q <= q2` asynchronous-information window.

It therefore supports the ecological bridge

> pairwise response asymmetry → mismatch

but not yet the mechanistic chain

> pairwise deadline difference → asynchronous cue uptake → mismatch.

This distinction should remain explicit in §4.6.

## Source and reproducibility boundary

The published analysis used bivariate MCMCglmm models with year-level
(co)variance to estimate temporal correlations and major-axis slopes. Example
R code and the open oak/frass data are archived at:

- Edinburgh DataShare: DOI **10.7488/ds/2215**
- GitHub: **allyphillimore/birds_frass_oak**

The BTO Nest Record Scheme bird records underlying the published bird models
are not redistributed by PAYOFF-B. The pairwise bird-caterpillar values above
are therefore treated as **published source results**, not as a new raw-data
reanalysis.
