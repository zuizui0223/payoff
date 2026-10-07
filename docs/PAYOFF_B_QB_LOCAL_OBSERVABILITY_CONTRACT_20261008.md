# PAYOFF-B QB prospective contract — local phase observability × recourse

Date: **2026-10-08**  
Status: **FROZEN BEFORE LOCAL VEGETATION q_B EXTRACTION**

## 1. Post-outcome origin of the question

V7R produced a robust null for

\[
q_F\times R
\]

using cross-site historical spring predictability as \(q_F\), including a null
direct-stopover-actuator test.

That result is already known and is not evidence for this new hypothesis.

The new question is:

> **Does independently measured local seasonal-state observability amplify
> corrective stopover response when remaining temporal recourse is high?**

## 2. Primary response

Use the already frozen 95 row-level barnacle-goose transition observations from
the ten V7R transitions.

Response:

\[
D_{ie}
=
\text{origin stopover duration in days}.
\]

Incoming signed phase error:

\[
E_{ie}.
\]

Late phase has \(E>0\). Corrective shortening therefore corresponds to a
negative \(E\)-by-information effect.

No transition is added after q_B is opened.

## 3. Primary recourse

Use the frozen V7R Q10--Q90 remaining-route temporal-window recourse coordinate

\[
R_e.
\]

It is not recomputed from local vegetation.

## 4. Primary local feedback-information coordinate

### 4.1 Fixed regions

q_B is defined at the **origin region** of each focal transition.

Unique origin regions:

- Greenland: R1, R2
- Svalbard: R1, R2
- Barents Sea: R1, R2, R3, R4, R5

No destination-only region is added.

### 4.2 Environmental data

Primary vegetation source:

- MOD09Q1.061 8-day surface reflectance;
- red = sur_refl_b01;
- near-infrared = sur_refl_b02;
- NDVI = (NIR-red)/(NIR+red);
- AppEEARS point extraction using existing PAYOFF Earthdata workflow
  credentials if configured.

Primary historical window:

\[
2001\text{--}2011.
\]

This window is fixed before q_B extraction and covers a common MODIS-era period
spanning the tracking years while providing multiple independent years per
region.

### 4.3 Spatial sampling

For every frozen Stage-3 region centroid, use a deterministic 3×3 point lattice:

- center;
- 4 km north/south/east/west;
- 4 km on the four diagonals.

Offsets are constructed geodesically from the centroid before request
submission.

No point is moved after seeing NDVI.

At each composite date, compute the median NDVI across valid lattice points.

Primary validity requires at least 5 of 9 lattice points at that date.

Quality filtering is frozen to the existing PAYOFF MOD09Q1.061 rule:

- MODLAND QA = ideal;
- band-1 and band-2 quality = highest;
- atmospheric correction performed;
- State QA cloud state = clear;
- no cloud shadow;
- aerosol category not high;
- internal cloud flag clear;
- not adjacent to cloud.

Snow is **not** separately filtered in the primary q_B coordinate; snow-driven
vegetation contrast is part of the local seasonal signal being quantified.

### 4.4 Independent phase anchor

Local spring onset \(S_{jy}\) is reconstructed from ERA5 using the already
frozen PAYOFF-B latitude-dependent GDD + logistic-third-derivative transform.

q_B does not use goose arrival, phase error, stopover duration, lambda, or
actuator response.

### 4.5 Local observability fit

For every region, retain vegetation observations satisfying

\[
-24\le\tau_{jyt}\le24,
\]

where

\[
\tau_{jyt}
=
\text{DOY}_t-S_{jy}^{ERA5}.
\]

Fit

\[
NDVI_{jyt}
=
a_{jy}+b_j\tau_{jyt}+\epsilon_{jyt},
\]

with year-specific intercepts and one region-specific local slope \(b_j\).

Let residual SD be

\[
\sigma_j
=
\sqrt{
\frac{\sum \hat\epsilon_{jyt}^2}
{n_j-Y_j-1}
},
\]

where \(Y_j\) is the number of admitted year intercepts.

Define

\[
J_{B,j}
=
\frac{b_j^2}{\sigma_j^2}.
\]

Primary coordinate:

\[
Q_{B,j}
=
z\{\log J_{B,j}\}
\]

across the nine frozen origin regions, using the ordinary sample standard
deviation (denominator 8).

### 4.6 q_B admission gates

A region is estimable only if:

- at least 8 of the 11 years have valid observations inside the ±24 d window;
- at least 4 valid composite dates occur in that window per admitted year;
- pooled valid observations >= 40;
- \(b_j\neq0\);
- residual SD > 0.

All nine origin regions must pass for the primary test.

If any origin region fails:

\[
QB\_PRIMARY=\text{NOT ESTIMABLE}.
\]

No window, year threshold or lattice geometry is relaxed.

## 5. Primary behavioral model

Use transition fixed effects:

\[
D_{ie}
=
\alpha_e
+\beta_EE_{ie}
+\beta_{ER}E_{ie}R_e
+\beta_{EB}E_{ie}Q_{B,e}
+\beta_{EBR}E_{ie}Q_{B,e}R_e
+\epsilon_{ie}.
\]

The focal coefficient is

\[
\boxed{\beta_{EBR}}.
\]

Directional prediction:

\[
\boxed{\beta_{EBR}<0}.
\]

Interpretation:

> when local phase is more observable and more route-level temporal recourse
> remains, a late incoming phase error should produce stronger stopover
> shortening.

## 6. Primary inference

q_B is an origin-region property, not a transition-row property.

Primary exact permutation therefore:

- hold all behavioral rows, E, R and transition labels fixed;
- permute the nine q_B region labels **within flyway at the unique-origin-region
  level**;
- assign the permuted q_B to every transition sharing that origin.

Permutation space:

\[
2!\times2!\times5!=480.
\]

One-sided P value counts permutation coefficients

\[
\beta_{EBR}^{perm}\le\beta_{EBR}^{obs}.
\]

## 7. Mandatory sensitivities

Only if primary is estimable:

1. local window ±16 d;
2. local window ±32 d;
3. center pixel only;
4. mean instead of median across 3×3 lattice;
5. \(Q_B=\log J_B\) without z scaling;
6. use inverse phase-resolution SD \(|b|/\sigma\);
7. ERA5 spring anchor replaced by the frozen POWER spring anchor where source
   coverage permits;
8. transition-level direct actuator gain as secondary response;
9. exclude the low-individual-support Barents R5→R7 transition;
10. leave-one-origin-region-out.

No sensitivity replaces the primary result.

## 8. Stop rule

Do not:

- tune NDVI windows after seeing behavioral coefficients;
- choose a subset of regions;
- add another vegetation product to rescue a null;
- redefine q_B from the goose response;
- reinterpret V7R as prior support.

If primary is null:

\[
QB\_ROUTE=\text{NOT SUPPORTED}.
\]

If primary is supported, safe claim is limited to this system and this
environmental observability proxy.

## 9. Claim ceiling

Safe if supported:

> Corrective stopover response was stronger where an independently constructed
> local vegetation-phase observability coordinate and independently
> constructed remaining-route recourse were jointly high.

Not licensed:

- geese directly sense NDVI;
- q_B is their internal posterior precision;
- causal effect of vegetation visibility;
- universal migration feedback law.
