# PAYOFF-B 2026-11-15: resolve NEON 403, pivot to anonymous multi-population Dryad data

## Verified NEON access policy

As of 2026-06-30 NEON requires account login for Data Portal downloads and API token for original-data endpoints. Metadata `/products` remains public; `/data` endpoints explicitly require authentication. The prior 403 on original phenology and air-temperature data was therefore an expected policy outcome, not evidence of bad product IDs. Official documentation:
- https://www.neonscience.org/impact/observatory-blog/next-week-required-logins-and-data-licensing-updates
- https://data.neonscience.org/data-api/endpoints/data/
- https://data.neonscience.org/data-api/authentication/

Do not try alternative unauthenticated URLs as a circumvention. NEON stays an optional future replication dataset once the user independently authorizes an API token, kept in GitHub Actions secrets and never committed.

## Anonymous Dryad data sources (published and publicly catalogued)

1. **Visser et al. 2021, Hoge Veluwe:** https://doi.org/10.5061/dryad.f1vhhmgx6 . Resident great tit first clutches, number of recruits and caterpillar peak timing; existing PAYOFF-B source file SHA-256 already certified. Distinguish annual peak date from daily resource curve.
2. **Visser & Jantzen 2023, four study sites, two songbird species:** https://doi.org/10.5061/dryad.1zcrjdfz0 . `Tbl_Fitness_GT_HVVLOHLBWH_FirstClutches.xlsx`, `tbl_PeakDate_Biomass_AllAreas_AllSpecies.xlsx`, `Tbl_budburst_HV.xlsx`, `Tbl_BeechCropIndex.xlsx`, `deBilt_1955_2022.xlsx`, `temp_deKooy_1955_2022.xlsx`. README says `NumberRecruitsAllBroodsSummed` is recruits across broods and `MaxBiom` is peak caterpillar biomass g/(day m²). This is an **independent multi-population extension**, not independent of the Hoge Veluwe population already in #1; explicitly cluster by study site and guard overlapping years.
3. **Wytham Woods 2026, thermal homeostasis:** https://doi.org/10.5061/dryad.51c59zwjn . Includes daily temperature `clim_data.csv`, great-tit laying dates `gtdata_ld.csv`, `gtdata_hd.csv` and winter moth caterpillar phenology. Useful external population for climate–phenology–fitness mechanisms; the paper's mismatch definition and temperature windows must be preserved, not silently equated to Hoge Veluwe.

## Falsifiable next analysis

H2: within each population, compare held-out-year prediction of individual reproductive output by absolute laying–caterpillar-peak mismatch versus measured peak caterpillar biomass and their interaction. Include climate and individual/brood effects where supported. Multi-site cross-validation must hold out entire years and sites, not mix same population across training/test. Do not interpret peak biomass as integrated availability.

H3: no migrant route data in these Dryad sources, so the Bayesian information-asymmetry mechanism remains a separate prospective test.

This branch adds anonymous source metadata inventory and GitHub Actions receipt; no empirical coefficients yet.
