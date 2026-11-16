# PAYOFF-B Scotland hatch-window supply → fledging prediction: exploratory freeze
2026-11-16. This is frozen before opening any new Scottish fitness prediction coefficients. Source-availability audit has been opened, and Dutch previous fitness results are already known. A future positive Scotland result would be **exploratory**, not confirmatory.

## Original data / admission

Official UKCEH EIDC dataset DOI:10.5285/b63d53ae-2fe7-4ce9-82a2-2325098489e3, downloaded at the *officially advertised* OGL data-package URL (SHA256 e5e7fa4f2fe60420c11675a1d21fdc69b7b8d8fa5565f67b268e1ae070cd0d7d). All seven raw CSV lengths match source RO-Crate. Bird = original bluti code only; exclude blank species and coati. Treatment = explicitly unmanipulated only in clutch-swap years 2017–2019; blank treatment in these experiment years excluded; in other years blank or unmanipulated admitted. Exclude missing/negative hatch, fledglings, clutch, sentinel -999, or fledged>clutch.

Resource = original branch-beating caterpillar **counts per standardized 30-hit branch**; no conversion to mass, grams or diet. For each source site×year, average counts per beat on each sampled date; nest's hatch-day through hatch+13 day proxy count from linear interpolation over adjacent observations no more than 8 days apart, with **100% of the 14 days** covered (no extrapolation). Uniform daily demand is a *proxy* and not measured nestling energetic demand. Peak count/beat and peak date are obtained from the original site-year observed season (earliest peak date on tie).

Source prefit gate: 448 source-identified blue-tit candidate nests with full count window, 143 site-years, 44 sites, 2014 and 2018–2021. Climate complete-case restrictions yet to be applied. The 2020 COVID data are site/time selected, so report sensitivity with 2020 excluded **without replacing primary**.

## Analytic unit and outcome

Primary independent row: source site×year, equal siteyear weights. Outcome Y = arithmetic mean among eligible nests of original fledged / original clutch size; no pseudo-replication from multiple nests using one resource curve. Within siteyear, mean admitted hatch ordinal day, mean clutch size, average nest-indexed full 14-day count/beat supply. Source site MeanLat, MeanElev and original temperature CSV are covariates.

Source temperature: pre-fixed **March 1 to April 15**, inclusive, from original hourly logger values in columns X46–X163, require >=80% valid hourly readings per retained logger, then average logger means at site-year. Record true logger count; do not treat loggers as independent site-years. Temperature source unit and plausible range must be verified before calling it degrees C. If climate gate leaves fewer than 75 source siteyears or fewer than 5 years/20 sites, stop climate-adjusted prediction and record NO_GO.

## Frozen predictors and models

For all models use the **exact same siteyear rows** (no differing missingness) and train-only feature standardization. Fixed ridge lambda=1, unpenalized intercept. Continuous proportion target (descriptive prediction, not binomial causal inference).

- M0: intercept-only.
- M1: year (linear), site latitude, site elevation, mean hatch DOY, mean clutch size, source March1–April15 mean temperature.
- M2: M1 + log1p(observed seasonal caterpillar peak count per beating) + signed seasonal peak day minus mean hatch DOY.
- M3: M2 + log1p(admitted hatch-window mean caterpillar count per beating).

Evaluate held-out entire calendar year (LOYO, at most five year folds) and held-out entire site (LOSO, at most 44 site folds). Predict one site-year per row; report equal-fold MSE and pooled equal-siteyear MSE with per-year and per-site fold errors. Primary incremental contrast MSE(M2)−MSE(M3), guard MSE(M1)−MSE(M3).

An exploratory overall improvement **requires** both contrasts positive in both LOYO and LOSO, plus improvement of M3 over M2 in at least **4/5 heldout calendar years**. All other outcomes HOLD, with full negative results. No optimized hatch window, prey guild weights, model hyperparameters, environmental windows or selective year removals.

## Novelty and biological interpretation firewall

Macphie et al. 2025 Oikos studied tree taxon–specific caterpillar seasonal abundance/biomass; Bialy et al. 2026 Ecology and Evolution studied alternative prey phenology; Macphie et al. 2026 preprint (doi 10.32942/X27Q35) already investigates resource peak abundance/duration vs blue tit fitness across 44 Scottish sites. PAYOFF-B therefore **cannot** claim to discover resource phenology and reproduction association. This is a source-verified empirical check of potential resource supply during a hatch-based demand proxy. It does not measure actual caterpillars eaten, non-caterpillar replacement diets, the information available to a bird before commitment, migratory recourse or game-theoretic coordination. Even a robust predictive effect could be confounded by weather, habitat, density and source selection.
