# PAYOFF-B V8 preregistered environmental-predictability change — primary result 2026-11-17

**PRIMARY RESULT OPENED. Freeze this record before any sensitivity analysis.**

Frozen design: `docs/PAYOFF_B_V8_PREDICTIVE_CONNECTIVITY_DEGRADATION_CONTRACT_20261005.md`, preregistered on 2026-10-05, with its pre-outcome spatial pair dependency correction `docs/PAYOFF_B_V8_DEPENDENCY_CORRECTION_20261005.md`. Source fixed Amaral/BirdMigrationSpeed `data/final.rds` at commit `62c58d77c2028bd863dfe3697b0d9cf29ceaeab0` (linked public Dryad DOI 10.5061/dryad.ttdz08m6w). Original environmental `gr_mn` is MODIS-derived mid-green-up calendar day, **not** GDD jerk, individual cue use, or measured food/bird fitness. This is a multi-species **environmental-exposure** analysis.

## Exact source admission succeeded

Before computing any early/late pair correlations, the new executable R script reproduced the previous pre-outcome gate from source:

- original spatial source→breeding target mappings: **842**
- estimable source mappings in both fixed windows (≥6 paired years): **393 species×pair rows**
- **166 unique spatial source→target pairs**, never counting repeated species as independent environmental observations
- **28 species**, **26** with ≥3 eligible pair exposures
- windows: EARLY **2002–2009**, LATE **2010–2017**; each series detrended separately against calendar year; signed Pearson r retained; no response-based pair selection.

R 10,000 resamples of unique spatial pair IDs, seed `20261005`, carried each pair's complete species incidence into the equal-species exposure estimator. This is exactly the pre-registered unit correction, though nearby or shared-cell pairs may still be environmentally correlated.

## Result: opposite to frozen degradation hypothesis

| Quantity | Original source result |
|---|---:|
| Mean signed early pair correlation | **+0.2838149** |
| Mean signed late pair correlation | **+0.6528374** |
| Unique spatial-pair mean Δr = late − early | **+0.3690225** |
| 95% pair-resampled interval | **[+0.2992332, +0.4373114]** |
| Equal-species exposure mean Δr | **+0.3363547** |
| 95% pair-incidence bootstrap interval | **[+0.2612341, +0.4297203]** |
| Unique pairs with Δr < 0 | **27 of 166** |
| Species with negative mean exposure Δr | **2 of 28** |
| Pairs crossing from positive r to nonpositive r | **7 of 166** |

**V8 preregistered directional status: BROAD_DEGRADATION_NOT_SUPPORTED.** The observed change is in the *opposite* positive direction; do **not** recode the hypothesis after outcome inspection to claim a confirmatory strengthening result. Describe the positive pattern as a secondary observed direction; confidence intervals reflect frozen *pair* resampling, not all spatial-temporal environmental dependence.

### Required uncertainty disclosure

Some bootstrap replicates lack at least one of the 28 species because they sample whole source→target pairs with replacement. Mean represented species per replicate: **27.2094**; minimum **25**; all 28 species represented in **37.77%** of resamples. Species-unrepresented replicates exclude the absent species in the replicate mean (not impute Δr=0); this changes the species composition in some replicates. A complementary fixed-species bootstrap or leave-species-out sensitivity should be labelled a new analysis and must not replace the frozen pair-incidence confidence interval.

The 8-year per-window environmental correlations can have high sampling variability; nearby pairs can share original green-up cells and related large-scale climate anomalies. The source is satellite-derived forest mid-greenup with a 2002 onset and may have changing coverage. A positive interval is **not** definitive evidence that global climate change caused information to become more reliable.

## Ecological boundary

Do not conflate V8 with the other already known experimental results:
- Kölzsch et al. 2015 barnacle goose Movebank three flyways: 52,443 original GPS fixes source-verified, but historical 1982–2011 stopover GDD-jerk spring onset data in publisher supplementary DOCX remained HTTP 403; V7's q×route-stage urgency model **NOT_ESTIMABLE**.
- Scottish EIDC blue tits: seasonal mean caterpillar mass (g per standardized beating) predicted fledged/clutch more accurately than hatch-specific food mass; no robust early nestling mass effect.
- Little Owl source-derived prey biomass was exactly reconstructed from prey class counts (952/952), not independently measured biomass or a novel food effect.

V8 may provide an **environmental information baseline**, but the birds' exposure, perceived cue reliability, irreversible migration timing and fitness are not jointly tested. Its positive Δr does not establish an adaptive mechanism or refute species-level mismatches.

## Reproducibility

Source-locked primary code: `analysis/movement_phenology/payoff_b_v8_frozen_unique_pair_primary_20261117.R`.
Validated original-run workflow: https://github.com/zuizui0223/payoff/actions/runs/44010205100.
Original machine-readable outputs: `outputs/payoff_b_v8_primary_summary.csv`, `outputs/payoff_b_v8_unique_spatial_pairs.csv`, `outputs/payoff_b_v8_species_exposure.csv` attached as a workflow artifact. All files retained in the draft PR; no merge to main.

**Next:** run the sensitivity protocols already fixed in 2026-10-05 contract (Fisher-z, full 8-year windows, 7-year alternative, undetrended control, distances, leave-one-species-out) after this primary result is recorded, reporting all directions and not changing the primary.
