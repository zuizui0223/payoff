# PAYOFF-B Scotland: original 2022 EIDC hatch-window prey-count versus fledging — result (2026-11-16)

**Verdict: HOLD. New original-data predictive test completed; no general incremental hatch-window prey-count signal.** This is exploratory after prior Dutch 2023 data, not confirmatory or a novel seasonal prey–fitness finding.

## Provenance and data quality

Official published data DOI 10.5285/b63d53ae-2fe7-4ce9-82a2-2325098489e3, EIDC OGL 44 Scotland forest site dataset 2014–2021. Public official dataset ZIP URL https://data-package.ceh.ac.uk/data/b63d53ae-2fe7-4ce9-82a2-2325098489e3.zip . The ZIP wrapper bytes vary between fetches (earlier SHA256 e5e7fa4f2fe60420c11675a1d21fdc69b7b8d8fa5565f67b268e1ae070cd0d7d; new SHA256 979d71ead06cd3d04a5f283510b008e6ae9ba02e7e181bd110ca6bbf7b8c6813), but each of the four original data member files was **SHA256-identical** to the first downloaded and RO-Crate-size-verified source:
- bird_phenology.csv: eb3f8d9faaa30ee3363f515f97873f287a918bb8a3ad31d180e2ac3a81d89257
- branch_beating.csv: 38f5c34cf656bab33c5d5b3516648306549049deebfbe693e4b4cad09ac4004c
- site_details.csv: f2a65cd96b2241ae6ff9d1207888d1453fef2738545c52a6ace1222fb56e2165
- temperatures.csv: 4686a544858e707b3844eee8bcd2ce26f1bf5d8daf3c3a0166843524734aa33b

This fixes a source-gate error that rejected a changed ZIP packaging digest despite unchanged original CSV bytes. No biological outcome was fitted until source files passed exact per-member checksums.

EIDC source bird records n=2307; branch beating n=37674. Strict blue tit code bluti only; blank or coal tit excluded, unmanipulated nests only and no uncertain treatment in 2017–2019; first observed hatch, 0<=fledged<=clutch and clutch>0. Bird source 500 eligible nests before prey temporal support, 448 with full 14-day prey window; after source climate/site complete cases still 448 nests, aggregated **143 independent site-years**, 44 sites, 5 years (2014: 5 site-years, 2018:41, 2019:41, 2020:22, 2021:34). Equal site-year weight; mean 3.13 nests per siteyear, 1–8 nests/siteyear. Original 614 logger rows yield valid fixed-window March1-Apr15 hourly-temperature means in 321 source site-years, zero failed sensor-coverage checks. The whole source actually had 2014–2021 but hatch completeness constrained the test years.

Seasonal resource **count** per standardized 30-hit branch beating, not measured total biomass, nutrition or actual food consumption. Hatching through hatching+13 days, equal proxy weights, full source coverage and interpolation gaps no more than 8 days. Source mass g is a **different metric**, with 6269 blank, 1109 below-limit and 30296 numeric entries; it was intentionally excluded from this fit. Source-provided hatch/feeding overlap, prey encounter rate, foraging efficiency, migratory forecasts and behavior were not observed.

## Frozen LOYO+LOSO out-of-sample comparisons

The before-outcome model contract is docs/PAYOFF_B_SCOTLAND_HATCH_WINDOW_FIT_FREEZE_20261116.md. Same 143 site-year rows all models, unpenalized intercept+fixed ridge 1, predictors standardized on train only, no posthoc optimized windows. Outcome mean within-siteyear observed fledglings / clutch proportion. M0=intercept; M1=source temperature fixed March1-Apr15, year, latitude, elevation, mean hatch DOY, mean clutch size; M2=M1+log peak branch-beating caterpillars+peak date-minus-hatch date; M3=M2+log(mean observed caterpillars within hatch+13 days).

| Model | LOYO equal-year-fold MSE (5 yrs) | LOSO equal-site-fold MSE (44 sites) |
|---|---:|---:|
| M0 intercept | 0.042893239 | 0.047156851 |
| M1 climate + hatch | **0.040872898** | **0.046388444** |
| M2 peak + date gap | 0.042723653 | 0.047103102 |
| M3 + 14-day prey contact index | 0.045000691 | 0.048354379 |

Main incremental MSE(M2)−MSE(M3): LOYO **−0.002277039**, LOSO **−0.001251277** (negative means the added food-window count *worsened* prediction). Guard MSE(M1)−MSE(M3): LOYO −0.004127793, LOSO −0.001965935. 1/5 held-out years positive M3−M2: 2014 −0.00136349, 2018 −0.000242737, 2019 −0.009926547, 2020 −0.000001818, 2021 **+0.000149400**. **Preset GO threshold failed** in both geographic and year holdouts.

Alternative pooled equal-siteyear MSE (not primary, same held-out predictions):
- LOYO M0 0.047526231, M1 0.047655209, M2 0.050251539, M3 0.053179640;
- LOSO M0 0.047378468, M1 0.045341332, M2 0.046024514, M3 0.047530008.
The added food metric worsens every primary and these secondary prediction summaries; not proof of a true zero ecological effect or that count-availability negatively causes breeding outcomes.

## Why this constrains the theory–empirical bridge

- The analytically derived overlap E=integral R(t)D(t)dt is still a valid formal food-contact concept, but original supply proxy counts in sampled branches are NOT the realized consumer feeding rate, caloric prey supply, territory-level resource density or individual energetic demand. A 14-day uniform demand proxy may be too crude.
- The model's information availability and recourse variables are absent (wintering cues, migration adjustment, individual decision information). No claim of Bayesian information-game or coordination-barrier confirmation from Scottish blue tits.
- Negative out-of-sample evidence is informative: **simple season peak + gap + a measured-window prey COUNT proxy does not improve broad spatial or annual out-of-group prediction in this sample**. Do not turn absence of predictive gain into evidence that prey or timing is biologically irrelevant.
- This same Scottish monitoring system informed earlier papers on resource abundance/season length and blue tit reproduction (Macphie et al. 2026 preprint DOI 10.32942/X27Q35), so do not present this as independent replication or new natural-history mechanism. Prior-art collision remains.

## Decision and next gate

1. **Keep this negative result.** Do not tune hatch window, feature definitions or validation folds after seeing these LOYO/LOSO results.
2. Mass rather than count is the next source-integrity issue: original branch beating has mass in grams since 2017, 1109 left-censored <0.02 g and some uncertain records. The mass vs count relation must be audited with numeric lower/upper bounds *before* any fit; need >5 breeding years for the same confirmatory LOYO criterion, so 2018–2021 alone is insufficient for the same primary test.
3. Other outcomes like nestling body mass at measured days 6 and 12 may be more proximal indicators of food access, but require separate prereg, source individual-to-nest checks, developmental age control, and independent holdouts. No claiming body-mass result here.
4. Keep theoretical information×irreversibility×recourse tests separate from this local seasonal resource observation until actual cue/commitment/adjustment data become available.

## Execution

Original source + schema + admission + 19 synthetic tests success:
https://github.com/zuizui0223/payoff/actions/runs/43881619335
Source gate fixed from initial ZIP wrapper mismatch while retaining strict **original CSV byte** verification. No code or empirical evidence was merged into main.
