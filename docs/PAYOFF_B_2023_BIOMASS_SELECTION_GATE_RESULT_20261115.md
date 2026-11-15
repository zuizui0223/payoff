# PAYOFF-B: positive findings, failed biomass gate, and source-faithful theory-to-interaction bridge
Date: 2026-11-15. New original-data run: https://github.com/zuizui0223/payoff/actions/runs/43712856727

**Status:** exploratory empirical fit completed, frozen primary consistency gate **HOLD** (only 1/3 Great Tit populations). This result is **not** an empirical verification of the information-coordination game or a discovery that biomass is unimportant. The source 2023 publication already examined mismatch and selection, and an independently available July 2026 preprint already examines resource peak abundance and duration versus blue tit breeding success.

## 1. Evidence ledger, segregated by inferential status

1. **Analytically solved / synthetic theoretical positives, not measured ecology.** In the explicit moving 2D landscape, a fine-step pairwise design has 57/81 sampled positive-interaction cells with coordination barriers and 21/81 with coordinated persistence rescue. Sampled phenological-capacity change 0 -> 5 increases maximum tracked envelope velocity 0.030 -> 0.065. It is possible to be abiotically well-tracked yet fail through partner mismatch. These grid numbers have parameter/design units, not empirical population effect sizes. Evidence: repo README, sections 11, 11b and docs/PAYOFF_B_MOVING_LANDSCAPE_RESULTS_20260920.md.
2. **Real telemetry descriptive effect:** 224 sequential staging transitions from 28 wigeon, phase-retention estimates POWER lambda=0.749768 and ERA5 lambda=0.811312. Raw lambda varies by sampling interval, stopover directional result source-specific, travel-speed mechanism gate unsupported. No prey biomass or breeding fitness in this estimate. Evidence: README section 11b and docs/PAYOFF_B_PHASE_RETENTION_ACTUATOR_GATES_20260921.md.
3. **Real Japan phenology descriptive effect:** JMA fixed panels show bird–insect annual event-anomaly correlation +0.520648 (1961-80), +0.628986 (1981-2000), +0.796201 (2001-20). Shared-reference artifact: apparent 2001-20 bird–plant vs insect–plant lag correlation +0.877316 collapses to +0.031927 with independent disjoint plant references. JMA first appearances do not establish bird–insect interactions, shared resource use, or fitness.
4. **Real Dutch climate responses:** original Dryad 2023 certified files, March-April KNMI proxy: all six Great Tit/Blue Tit population strata have negative temperature slopes in first egg date (−2.86 to −4.52 days/C) and caterpillar peak (−3.54 to −8.17 days/C); all six bootstrapped *difference* intervals include zero. Hence both events advance, but heterogeneous differential advance is not demonstrated by this fixed-window test.
5. **Real Dutch annual reproductive predictions, PR #387:** peak-minus-mean-lay gap added to temperature-only only improves 2 of 12 endpoint x site/species comparisons; log peak magnitude added to temperature-only worsens all 12. For corrected fledglings, temperature-only was inferior to intercept-only in all six comparisons. These are explicit negative controls against a simplistic peak/mismatch predictor, **not** evidence of zero ecological effect.

## 2. New annual relative fledgling selection pilot: code + original data

Exact original first-clutch fitness 30,182 records and caterpillar peak resource file (97 rows) were retrieved from Dryad-identical Zenodo 8377972 and validated with source SHA256 by the existing load() function. The source's original units: LayDateApril and MidDate use the same April-day origin; MaxBiom is peak production rate g/(day*m^2), **not standing mass or demand-window integral**. Reproductive component is first-brood corrected fledglings = NumberFledged + 0.5*NumberFledgedDeviation; number of recruited offspring is from *all broods* and is excluded from this new pilot outcome.

In every eligible population/species/year: >=10 unmanipulated broods, lay-date SD >0, positive average fledglings. Annual descriptive relative fledging differential beta = mean(z_lay * (fledglings/annual_mean_fledglings − 1)). Negative beta = earlier broods fledged more offspring within that year, not a causal or lifetime-fitness selection coefficient. Primary Great Tit models use signed putative demand gap M = annual mean lay + 33 days − caterpillar peak date, peak rate B=log1p(MaxBiom) and M*B. The +33 is literature supported for Great Tit only. Fixed ridge=1, train-only standardization, full-year LOYO; no nest-level pseudo-replication.

| Great Tit population | Admitted years | Early laying + fledglings (years) | M-only MSE | M + B + M×B MSE | MSE(M)-MSE(M+B+M×B) | Pass both M and intercept? |
|---|---:|---:|---:|---:|---:|---|
| Hoge Veluwe | 47 | 31 | 0.021531354 | 0.020751899 | +0.000779455 | YES |
| Oosterhout | 24 | 17 | 0.011520846 | 0.014679317 | −0.003158471 | NO |
| Vlieland | 19 | 4 | 0.014739903 | 0.015743400 | −0.001003497 | NO |

Primary **gate requires at least 2/3 populations pass both baselines: HOLD (1/3)**. Blue Tit sensitivity: Hoge Veluwe NO (41 yrs), Oosterhout NO (22), Vlieland YES (19); Blue Tit 33-day developmental offset is unvalidated. These are not independent tests because both species share annual resource profiles.

### Posthoc year-deletion influence check (run 43712856727)

Re-fit leave-one-year-out prediction models for each single excluded annual observation (a jackknife-of-the-LOYO-comparison diagnostic, not inferential/bootstrap CI):

| Great Tit site | Positive resource-interaction increment in dropped-year models | Both-baseline pass fraction | Largest issue |
|---|---|---|---|
| Hoge Veluwe | 46/47 = 97.9% | 46/47 | dropping 1958 makes improvement negative; 1958, 1962, 1963 have inferred offsets below −40 days |
| Oosterhout | 1/24 = 4.2% | 1/24 | 1996 exclusion reverses sign |
| Vlieland | 2/19 = 10.5% | 0/19 | intercept-only remains stronger |

All extreme annual offsets were **retained in primary tests** and flagged for source audit. Their status as true ecological timing mismatch is unresolved (no direct hatching/demand dates). Diagnostics are exploratory and cannot overturn the failed 2/3 generalization gate.

### Validation and limitations

Dedicated GitHub Actions run https://github.com/zuizui0223/payoff/actions/runs/43712856727 completed successfully with 9 synthetic tests plus source-verified original-data fit and posthoc influence report. Earlier narrow run https://github.com/zuizui0223/payoff/actions/runs/43712474061 completed successfully with 7 tests. Repo-minimal pytest initially failed to collect these two new tests because the generic job does not install optional numpy/openpyxl; these are now marked with pytest.importorskip for the generic environment, while the dedicated job explicitly installs the packages and executes all nine tests. The new source-units and outcome constraints are visible in test and code.

## 3. Mathematical link: production != realized biotic interaction

An analytic illustrative null, **not calibrated on the Dutch data**: Gaussian resource rate R(t)=B exp[-(t-mu_R)^2/(2*sigma^2)] and consumer demand D(t)=exp[-(t-mu_D)^2/(2*sigma^2)]. Their weighted temporal contact E=integral R(t)D(t)dt = B*sqrt(pi)*sigma*exp[-delta^2/(4*sigma^2)]. Accordingly, a twofold resource peak, a 10-day newly acquired gap and sigma=5 days yields E_new/E_old=2*exp(-1)=0.736, so inferred contact *falls by 26.4%* even as peak rate doubles. Real food intake additionally requires measured resource accessibility, diet/quality, search/foraging capacity, competition, and saturation. Food amount is not automatically a demographic resource.

For pairwise coordination, the payoff effect depends on *co-use* rather than absolute peak and cannot be obtained from phenology dates alone. For uncertain migrants, remote predictive cue correlation rho and recourse-adjusted loss D_eff are separate axes; neither is present in a local Dutch tit-caterpillar peak panel. The user-proposed Bayesian game and information×irreversibility×recourse theorem remain model propositions, not yet cross-taxon empirical claims.

## 4. Prior-art collision and novelty boundary

- Jantzen & Visser (2023), Proc. R. Soc. B, doi:10.1098/rspb.2023.1474: source of this dataset; directly studied selection on reproductive dates, mismatch, spatial heterogeneity, 33-day convention. We cannot present seasonal selection or Dutch bird–caterpillar mismatch as a new finding.
- Macphie et al. (2026-07-07), prereviewed preprint doi:10.32942/X27Q35: 44 sites, 11 years, direct caterpillar phenological shape (mean, maximum and duration) vs blue tit optimum hatch dates, breeding success and stabilizing selection. Resource peak magnitude vs reproductive output is not unoccupied novelty.
- Versluijs et al. (2024), Proc. R. Soc. B, doi:10.1098/rspb.2023.1785: arthropod peak phenology measured in individual abundance vs biomass yields opposite trends. A mismatched measurement currency can change the answer itself.

**Remaining PAYOFF-B research prospect, not yet demonstrated:** how forecast information, irreversible commitment and within-season recourse change the payoff of biotic interactions *after* observed resource magnitude and demand timing are controlled. The empirical data must separately measure (i) remote vs local cues, (ii) adjustable actions, (iii) temporally resolved compatible food or reward and need, (iv) interaction encounters/intake or pollen transfer, and (v) fitness, with spatial and temporal replication.

## 5. Next strict data gate

1. Retrieve original within-season caterpillar (daily or repeated) biomass/abundance and true hatch/peak nestling-demand dates for same site/year. If only peak date/rate are available, label demand-weighted resource integral **not identifiable**, do not reconstruct a daily Gaussian as data.
2. If a legitimate daily dataset exists, pre-register held-out-year and held-out-site comparison: temperature-only or source-appropriate phenology baseline; peak magnitude; simple timing mismatch; empirical demand-weighted exposure (temporal integration); and availability/encounter/fitness sequential mediation. Control population density, tree habitat, alternate prey, sampling intensity. Use hierarchical models with year/site as clustered units.
3. Separately, for migratory birds, obtain departure/stopover/arrival stages, independent winter-to-destination forecastability, route compensation and fitness. Do not infer recourse from resident tit laying records.
4. Independently validate the interaction-to-fitness pathway with flower/pollinator: dated flower reward amount (not just plant biomass/NDVI), actual visitation/pollen transfer and seed set; retain unsynchronized years and observer effort as explicit null controls.

**No new general positive claim is authorized by this gate.** Code, complete negative and positive data, and the posthoc uncertainty receipts should remain inspectable.