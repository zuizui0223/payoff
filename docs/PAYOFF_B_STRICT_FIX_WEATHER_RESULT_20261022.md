# PAYOFF-B: corrected original GPS-day stationarity changes source weather interpretation

**2026-10-22 — real public CC0 sources, exploratory measurement robustness; NOT a new causal information-use test.**

## Measurement failure identified independently of weather model

Original stationary eligibility for PAYOFF-B had used averages of GPS fixes during three consecutive days. Continuous GPS in a newly added Egyptian vulture source exposed that the previously reported 16h median "departure" sampling gap largely reflected an artificial UTC day-boundary interval; original continuous consecutive inside-to-outside 30km fix gaps had 2h median, with 9/18 candidates already outside the site on the last supposedly stationary day.

This prompted a complete audit of **7,368** previously frozen stationary 3-day source risk opportunities, across 4 bird taxa. In each taxon, a greater fraction of subsequently northward-labelled riskdays than stayed-labelled days contained original GPS fixes more than 30km outside their daily-centroid-defined stationary source circles DURING the supposedly stationary three-day anchor. A daily centroid can mask exploratory flights; whether those flights are true migratory departures or foraging excursions is not established.

To evaluate measurement sensitivity, the original later GPS outcome labels, same 30km centroid and all original meteorological fields/lag windows were HELD FIXED. Retain only the source windows whose ALL original fixes on EACH of the original three days stayed inside the original circle. This is deliberately restrictive and may discard actual stationary birds making longer foraging trips; it is a quality sensitivity sample and was created after seeing original source associations.

## Source selection BEFORE strict-subset weather

| Source | Original daily-centroid opportunities | Strict fix-level stable opportunities | Strict northward/stay labels | Northern case-days inside same grid-year-month stay strata |
|---|---:|---:|---|---:|
| Ciconia ciconia | 1,633 | 1,110 | 85/716 | 47 |
| Anser albifrons | 2,008 | 1,790 | 93/1,324 | 73 |
| Numenius arquata | 1,868 | 1,778 | 42/1,585 | 30 |
| Neophron percnopterus | 1,859 | 1,257 | 13/1,029 | **9; NOT ESTIMABLE** |

The fixed prior source gate demanded at least 10 case-days with a stay in the same 0.5-degree cell×year×month. The vulture failed, and the runner performed **zero** new public weather requests or climate fits for this source. For the other three, original NASA daily physical weather data (UTC source day−1 vs days−2 through−8, T2M, WS10M, V10M, shortwave) were re-read for strict-selected source subcohorts: 190+246+103 original month-grid queries. Descriptive weather-block bootstrap intervals resample complete shared weather fields 3,000 times.

## Same original physical-weather estimand, more careful source state

| Taxon, physical source anomaly | Earlier within-grid-year-month case–stay | After strict 3-day all-fix stationary filter | Entire year-month descriptive bootstrap 95% |
| --- | ---: | ---: | --- |
| Stork shortwave irradiance (W/m²) | −17.10 | **−19.64** | [−35.05, −3.50] |
| Goose temperature (°C) | +1.04 | +1.54 | [−0.40, +3.30] |
| Goose 10m wind speed (m/s) | −0.47 | **−0.65** | [−1.02, −0.20] |
| Curlew temperature (°C) | +0.34 | **−0.28** | [−1.56, +0.90] |

Across this specific within-source observational sensitivity, **stork lower solar shortwave** and **goose reduced 10m wind speed** remained in the same direction when coarse daily-centroid stationary misclassification was reduced. The curlew thermal contrast **reversed sign**, and the goose temperature descriptive interval still crossed zero when resampling entire shared year-month weather episodes. **These are not independent species-level confirmation results** and not confidence intervals for a causal effect.

The original stork sunlight observation still did NOT transfer to the held-out Egyptian vulture; the newly stringent vulture sample was **not estimable** under the prespecified matched-case count. Even the stork/goose/curlew source contrasts can reflect readiness, actual migration/foraging state, year/month selection and shared weather fields; a 30km GPS fixed circle does not identify the time of a biologically irreversible migratory decision.

## Ecological scope and next legitimate hypothesis

What is supported: (1) the source GPS permits materially better continuous-time measurement than the earlier UTC-day extraction; (2) published GPS daily-centroid stationarity may differentially misclassify source state; (3) some taxon-specific physical weather correlations persist under this sensitivity while others are fragile.

What is **NOT** supported: a universal warming or sunshine departure trigger; observed bird interpretation of pre-decision environmental forecasts; information deadline versus feasible subsequent correction; flight-altitude signed tailwind; arrival relative to destination phenology; reproductive/survival fitness rescue; ecological games or any independent cross-taxon causal generality.

A genuine test requires independent animals with high-frequency original GPS, a validated stopover/foraging-versus-migration state classifier, observable predeparture weather or vegetation cues, and downstream decisions/phenological targets. The previous registered V7R/V8 and stork 53-season NOT SUPPORTED verdicts remain unchanged.

Reproduction: https://github.com/zuizui0223/payoff/actions/runs/39784335141
Machine source receipt: data/payoff_b_strict_fix_stationary_weather_verdict_20261022.json
