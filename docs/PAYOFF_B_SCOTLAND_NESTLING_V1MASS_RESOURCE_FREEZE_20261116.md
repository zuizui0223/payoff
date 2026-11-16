# PAYOFF-B Scotland: nestling early mass as a potential consumer response to measured caterpillar mass

**Source/blind design freeze: 2026-11-16, after opening fledged/clutch outcomes and an exploratory joint count+mass result. This is NOT a new independent confirmatory experiment or preregistered biological discovery.** Existing head of the measured-mass branch is 1d8cbea9954fe084ab1cc44a301608516f0d4dd7; this offspring mass-stage branch must retain all its null results.

## Source

Use ONLY official UKCEH EIDC DOI 10.5285/b63d53ae-2fe7-4ce9-82a2-2325098489e3. Exact source original CSV SHA256 from initial RO-Crate validated audit:
- bird_phenology.csv eb3f8d9faaa30ee3363f515f97873f287a918bb8a3ad31d180e2ac3a81d89257
- nestlings.csv e292c06e9256700782ebd66c59741f5e8d50514c948fb4b83c4aa698113322e2
- branch_beating.csv 38f5c34cf656bab33c5d5b3516648306549049deebfbe693e4b4cad09ac4004c
- site_details.csv f2a65cd96b2241ae6ff9d1207888d1453fef2738545c52a6ace1222fb56e2165
- temperatures.csv 4686a544858e707b3844eee8bcd2ce26f1bf5d8daf3c3a0166843524734aa33b.

The official EIDC source description identifies v1mass as a nestling mass measurement in grams near day 6 after first hatching, v1date as date of that visit (ordinal day), and notes that 2020 northern sites may have irregular stages/visits. NO invented source age or observation. Original v2mass (around day 12 among surviving nestlings) is deliberately excluded from primary to avoid stronger survival selection.

## Source admission (must be audited before any outcome coefficient)

- Original blue tit `species=bluti` only, exact site/year/box join from bird_phenology to nestlings. Only source-verified nonmanipulated nests: 2017–19 require explicit `unmanipulated`; other years blank or explicitly unmanipulated. Never include unverified `coati` or blank species.
- Measured caterpillar mass only from 2017 forward (no structurally-zero-only 2014–16 cohorts). Original `caterpillar.mass` numeric g, exact `<0.02` or `<0.02g` interval-censored [0,0.02] grams per standardized 30-hit branch beating; positive-count missing mass and uncertain flags omitted. Source sampling dates with >=80% mass-covered branches admitted.
- For each nestling record, admit v1mass **greater than zero**, v1date finite ordinal within source year, `observed v1day - first-recorded hatch day` in **5–9 days inclusive** (not an exact developmental age because hatch is first observed). Require >=2 admitted distinct nestling records per nest. Record all denominator changes and row exclusions.
- No future-food leakage: for body-mass measured earliest at recorded hatch+5, fix potential prey exposure to **hatch day through hatch+4 (5 days)**, not the +14 days previously used for eventual fledging. Require 100% observed/interpolated support with <=8-day adjacent beating gap and no extrapolation. Equal-weight 5-day count per beating and mass g per beating, two mass-censor bounds. It is a *resource availability proxy*, not measured prey eaten.
- Number of nestlings per source nest and their visit ages are recorded; include mean first-visit offset in prediction covariates (siteyear mean for equal siteyear grain). Original `v1mass` is grams per individual chick, not plant/herbivore community biomass and not growth velocity.

## Pooled source estimation grain

Primary row is the *site-year mean of nest-level mean nestling first-visit mass*, not an individual chick repeated as independent sampling of the same resource. One datum per site-year; require >=2 source nestlings in each admitted nest. Exact year, site, box are the nest keys; no site/year alias.

Source gate to run any model: >=60 source siteyears, >=20 distinct sites, >=3 distinct years, >=150 admitted nests and >=400 admitted nestling v1mass rows. If these fail, NO_GO. Source temperature, latitude, elevation, site-year mean hatch day, mean clutch size and **mean first-observed-hatch-to-v1-visit age** are covariates; validate climate logger source units as upstream.

## Frozen models and validation

For same identical site-year rows, fixed ridge lambda=1 and training-only standardized covariates; continuous outcome of mean grams per chick (descriptive only).

- A: year + latitude + elevation + mean hatch DOY + mean clutch size + mean observed v1-day minus hatch day + spring temperature + source caterpillar count seasonal peak and signed peak minus hatch gap.
- B: A + log1p(5-day caterpillar **count** / standardized branch beating).
- C_lower/C_upper: A + log1p(5-day measured **mass g** / standardized beating), with censor bounds.
- D_lower/D_upper: B + mass (same mass bounds).

Hold out an **entire calendar year** (LOYO) and **entire site** (LOSO); equal-fold and equal-siteyear mean squared errors; all results both signs recorded. A joint positive claim is allowed only if D beats A and B in both validation dimensions at both censor bounds and in >=ceil(0.8 * tested years) heldout years, otherwise HOLD. Source-stage filters are not to be tuned after inspecting effects. 2020 excluded sensitivity is prelisted, reports both positive/negative, never replaces the all-source test.

## Key biological limitation and novelty

This may show that locally available prey mass has incremental predictive content for nestling early body mass; it cannot establish actual feeding/consumption, prey nutritional efficiency, causal information barriers, coordination game, or body-mass *growth rate*, because individuals are not continuously monitored. Earlier Scottish blue-tit and caterpillar-seasonality publications overlap data and concept. A positive result would be exploratory support for one observable **resource-to-consumer-condition** bridge, not a novel general ecological principle.
