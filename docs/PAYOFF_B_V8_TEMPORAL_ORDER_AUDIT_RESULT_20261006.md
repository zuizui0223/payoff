# PAYOFF-B V8 source-target temporal-order audit — 2026-10-06

Status: **POSTHOC TEMPORAL-ORDER AUDIT; FROZEN V8 PRIMARY UNCHANGED**

## Question

The frozen V8 mapping selects the nearest lower-latitude migratory-range source cell for each breeding-range target cell. Lower latitude does not guarantee that source green-up actually occurs earlier in time.

This audit therefore asks whether source green-up temporally precedes target green-up in the same observed years.

Define lead_days = target green-up date - source green-up date. Positive values mean the source environmental state is observed earlier than the target state.

## Early window, 2002–2009

Across 166 unique spatial pairs:

- mean pair lead = **13.36 d**;
- median pair lead = **11.71 d**;
- mean fraction of years with source earlier = **0.944**;
- **95.8%** of pairs have positive mean lead;
- **95.2%** of pairs have source earlier in a majority of observed years;
- pair-bootstrap 95% CI for mean lead = **11.89 to 14.85 d**;
- source-cell cluster CI = **10.30 to 15.93 d**;
- target-cell cluster CI = **11.04 to 15.43 d**;
- 5-degree block CI = **11.21 to 15.05 d**;
- 10-degree block CI = **10.13 to 15.40 d**.

## Late window, 2010–2017

Across the same 166 pairs:

- mean pair lead = **13.43 d**;
- median pair lead = **11.08 d**;
- mean fraction of years with source earlier = **0.949**;
- **97.0%** of pairs have positive mean lead;
- **98.2%** of pairs have source earlier in a majority of observed years;
- pair-bootstrap 95% CI = **12.01 to 14.98 d**;
- source-cell cluster CI = **10.17 to 16.04 d**;
- target-cell cluster CI = **11.34 to 15.19 d**;
- 5-degree block CI = **11.27 to 15.02 d**;
- 10-degree block CI = **10.36 to 15.39 d**.

## Joint temporal-order summary

- **158/166 = 95.2%** of pairs have positive mean source lead in both windows;
- **157/166 = 94.6%** have source earlier in a majority of years in both windows;
- **127/166 = 76.5%** have source earlier in every observed paired year across both windows;
- grand pair-mean lead = **13.40 d**.

Descriptively, restricting the information-value diagnostic to the 158 pairs with positive mean source lead in both windows leaves the result essentially unchanged:

- early mean G_CV = **-16.80 d^2**;
- late mean G_CV = **+15.79 d^2**;
- delta G_CV = **+32.59 d^2**;
- **84.2%** of retained pairs have positive delta G_CV.

This restricted G_CV summary is descriptive and was not a separately frozen inferential sensitivity.

## Interpretation

The frozen lower-latitude source signal is temporally leading in the great majority of retained environmental pairs. It is therefore reasonable to describe it as a **temporally leading nonlocal environmental signal** or **potentially available prior environmental information**.

Do not describe it as a cue actually perceived by the birds. The dataset does not track individuals through the source cells or establish that birds observed, learned, or acted on the fitted source green-up signal.

## Provenance

- workflow run: 37391792058
- artifact: 11380859798
- artifact SHA256: 3e44f2349e2dd728d8387f5fde27a4f47df82d148c7b019dd3c8eddb7fc0779

Script: analysis/movement_phenology/payoff_b_v8_temporal_order_audit.R