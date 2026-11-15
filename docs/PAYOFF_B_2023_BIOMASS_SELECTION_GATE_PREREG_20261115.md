# PAYOFF-B 2023: preregistered peak-resource magnitude x mismatch selection audit (2026-11-15)

Status at creation: **outcome-blind for this new annual-selection-gradient endpoint**. Existing original-data year-mean fledgling/recruit LOYO results in PR #387 are already open. This is a downstream exploratory follow-up, **not** confirmatory independent preregistration.

## Motivation and existing prior art

PR #387: adding original peak-mass magnitude to climate-only annual mean fledgling/recruit prediction worsened MSE in all 12 tested population x endpoint comparisons. This is **not** proof that food is unimportant. Year-average reproduction may not recover within-year selection on relative breeding date; peak magnitude is not demand-period food exposure.

The source 2023 study (DOI 10.1098/rspb.2023.1474; Dryad 10.5061/dryad.1zcrjdfz0) already shows that mismatch relates to annual selection on breeding date. Its original analysis used 33 days from first egg to inferred chick peak demand and included survival + recruits in combined fitness. **We do not claim to discover either the 33-day convention or mismatch-selection association.** This audit asks whether peak magnitude adds held-out-year predictive information to a first-brood fledgling component conditional on mismatch.

## Frozen source and units

- SHA256-certified original files from Zenodo record 8377972, identical to Dryad:
  - fitness Tbl_Fitness_GT_HVVLOHLBWH_FirstClutches.xlsx: 53c5c4e0861759c2b33e5a95e1b734f83368875a67cff481353e22072fafb977
  - food tbl_PeakDate_Biomass_AllAreas_AllSpecies.xlsx: f6562a60c91b98b2c295afb1f07b1f9f8af5760a6e72c1375369a0daaedd0b28
- Original README SHA 7aa6f4c1d0bb440a73b2c31c70ff5f50bc3f807fc211876a05f788fd77ee18e9
- Both LayDateApril and MidDate are April days with the same date origin. MaxBiom is peak resource rate in **g/(day*m^2)**, **not** integrated resource quantity or standing biomass.
- Source Include=1 only. First-clutch corrected fledglings = NumberFledged + 0.5*NumberFledgedDeviation, not all-brood recruitment.
- Resource joined only at exact population x year. No unverified source aliases. No climate-station crosswalk needed for this follow-up.
- Year is inferential independent unit, not the individual brood count. Shared resource-year values are not independent samples.

## Frozen estimand and mechanism proxy

Within each population x species x year with >=10 valid unmanipulated broods, at least three unique first-egg dates and positive mean corrected fledgling count:

1. Standardize individual laying dates z = (lay - mean(lay))/SD(lay), within the year.
2. Relative first-brood fledging score w = corrected_fledglings / mean(corrected_fledglings), within the year.
3. Annual phenotypic differential beta = mean[z * (w - 1)]. A negative beta indicates an early-laying advantage in that **reproductive component**, not total fitness or causation.
4. Annual signed inferred demand-offset M = mean(lay) + 33 - caterpillar_peak. Positive values mean putative nestling demand after the resource peak.
5. Annual log peak magnitude B = log(1 + MaxBiom). This transform is for the regression only; source units unchanged.

The +33 offset is source/literature supported for **great tits**. Primary panel: great tit strata (Hoge Veluwe, Oosterhout, Vlieland) each >=12 eligible years. Blue tit panels are **sensitivity only** because the +33 assumption is not validated for blue-tit development. No data-selected offsets or width/peak-time optimization.

## Models and out-of-year test

Within each stratum, fixed ridge=1, training-only standardized columns, intercept unpenalized. Leave one entire year out and predict the annual beta for that year:

- I: intercept only.
- M: signed annual mismatch M only (prior-art baseline).
- MB: M and log peak magnitude B (incremental magnitude).
- MBI: M, B and M*B (incremental interaction).

Primary comparison: held-out-year MSE(M) - MSE(MBI) for each of three great-tit populations; require **positive improvement in >=2/3 populations and MBI beating intercept in those same populations** before describing consistent predictive evidence. Report every stratum including negative, zero and missing results, and a separate blue-tit sensitivity table. No pooled individual-level p-values; do not treat species sharing a resource year as independent. This is exploratory model comparison after previous null results, **not a confirmatory test**. A favorable result requires validation in an independent forest/country.

## What remains unidentifiable

- Daily prey availability / food-quality curve and demand-time integral: unavailable from the 4-column peak-source file.
- Actual nestling hatching and demand peak: not observed in the original first-clutch sheet. The 33-day offset is an approximation, not measured chick demand.
- Spatial distribution, foraging accessibility, alternative prey and density-dependent competition: not observed.
- Remote cue predictability, value of information, departure/migration recourse: not measured, therefore neither PAYOFF-B information-game nor actuator predictions are empirically tested by this analysis.
- Mechanistic interaction, selection on lifetime fitness, causal effect or generalizability cannot be inferred from this observational pilot.

## Mathematical bridge (illustration only, not fitted from these data)

For two Gaussian curves of equal temporal width sigma (resource and demand), normalized temporal overlap relative to perfect alignment is proportional to B * exp[-delta^2/(4*sigma^2)]. Twice the instantaneous peak B with a 10-day shift and sigma=5 days leaves 2*exp(-1)=0.736 of the original contact integral. This is **synthetic mathematics**, not a claim about measured Dutch caterpillar availability. More resource can coexist with lower realized contact when timing worsens. Only independently observed daily resource and demand curves could test it as food exposure.