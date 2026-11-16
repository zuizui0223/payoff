# PAYOFF-B Scotland: phase specificity of prey mass as a negative-control test

Frozen 2026-11-16 **after** the count+mass fledging and nestling-mass outcome receipts were opened. This is a downstream **exploratory falsification**, not independent preregistration, causal inference or confirmation of a theory.

## Why this comparison is required

PR #390's corrected 2018–21 cohort (138 site-years, 427 nests, 44 sites) showed that **count + measured source prey mass in the hatch+0..13 window** modestly improved held-out fledged/clutch prediction beyond the count-only model, but mass alone did not consistently beat the climate+peak baseline. PR #391 tested early body mass and failed. The remaining positive result may reflect **between-site/year food productivity** rather than *when* food is available.

Independent work already studies caterpillar biomass and consumer fitness (e.g., Macphie 2026 preprint DOI 10.32942/X27Q35). Therefore testing generic "more food yields more fledglings" is not a novel contribution. The PAYOFF-B bridge uniquely requires distinguishing phase-specific availability from generic abundance.

## Frozen exact input and grain

- Use only the original official EIDC Scottish blue tit site-year panel admitted by `scripts/payoff_b_scotland_measured_mass_window.py` from the original OGL archive DOI 10.5285/b63d53ae-2fe7-4ce9-82a2-2325098489e3.
- Preserve original CSV SHA256 gates, measured-mass years **2018–21 only**, verified blue tits, no unverified treatments, valid hatch and fledged/clutch, 14-day hatch resource count/mass window fully supported, >80% source mass-covered branches on individual sampling dates, no interpolation beyond source support, mass detection <0.02 g bracket [0,0.02] per standardized beating.
- Do not change the original sample: all phase and nonphase models must use the **same 2018–21 admitted 138 site-years and same nests** as the original corrected measurement-era cohort, unless an externally identified source quality failure mandates NO_GO. Any sample mismatch blocks model fit and must report counts.
- Inferential row is *one equal-weight site × year*. Source prey "g" is grams per standardized 30-hit branch beating, **not g/m², grams consumed, energy, or biomass production**. The number of prey observation dates and their seasonal span must be reported for each site-year and source mass bound.
- Seasonal resource control: for every site × year, take the **unweighted mean of directly observed sampling-date mass rates** across all >=80%-mass-covered dates in the source season (equal observed-date weight, not seasonal integral). The two censored-bound series are computed separately. No extrapolated days; no site-year estimated as zero because all positive-count masses missing. Report min, max, observation-date counts and range of source DOYs. This season mean is only a *sampled-season abundance proxy* and can be affected by temporal coverage and effort.

## Predetermined prediction models (on identical rows)

Fledged/clutch site-year mean, fixed ridge penalty 1, training-only feature standardization, unpenalized intercept, full-calendar-year LOYO and full-site LOSO. No data-selected stage shift or optimal seasons.

- A: year + original site latitude + elevation + mean hatch DOY + mean clutch size + original site-year March 1–Apr 15 temperature + source seasonal peak count per beat + signed peak date minus hatch.
- B: A + log1p(hatch+0:13 **count** / standardized beating) — prior count-only failure.
- H_low/H_high: B + log1p(hatch-window **mass** lower/upper g/beat) — prior mixed evidence.
- S_low/S_high: B + log1p(observed-**season mean mass** lower/upper g/beat) — new abundance-only control.
- HS_low/HS_high: B + *both* hatch-window and season mean mass lower/upper — tests conditional phase-specific information, not posthoc feature interaction.

**Primary specificity contrast:** heldout MSE(S) − MSE(HS) at each censor bound. **Strict exploratory gate requires** >0 for both lower and upper in LOYO and LOSO, **and** MSE(S) − MSE(H) >0 for both bounds in both LOYO and LOSO, and HS improves vs S in >=3/4 heldout calendar years for both bounds. All other outcomes, including negative, are HOLD. Also report B and A as guards. The full 4-year cohort is primary; 2020-excluded (2018,19,21) sensitivity retains same model names and is descriptive, never replaces primary. No other window widths/lag shifts are searched.

## Critical interpretation

Even a passing phase-specificity gate would only say that an observed hatch-window resource proxy contains **incremental out-of-year/out-of-site prediction** versus sampled-season mass abundance. It does **not** identify birds' consumed caterpillars, parent feeding effort, alternative prey, a mechanistic coordination game, perfect information/remote forecast, movement recourse, or a causal mismatch pathway. With overlapping source publications, a positive result is an exploratory bridge, not a new discovery of biomass-phenology fitness relations.

Stop if source dates/units/sample grain cannot be reverified. Preserve the original negative or limited results. New tests use synthetic fixtures, never present synthetic test values as empirical evidence.
