# PAYOFF-B E6: within-study short–long migration contrast — post-open prefit plan

Date: **2026-11-19**. Status **post-open exploratory robustness design, not independent preregistration**. Existing Usui et al. 2017 original migration-distance effects are already published and the 2026-09-28 PAYOFF E6 pooled result is already opened. This plan is fixed **before** the newly defined within-study coefficient is fitted on this branch; the original E6 data source and source-policy restrictions are unchanged.

## Ecological issue

The existing corrected E6 temperature slope difference `long − short = +0.602 d/°C` in a source-described 676-row cohort is a between-and-within-study association. A published study can sample only one migration class, making the comparison vulnerable to differences in temperature window, arrival measure, geography and study design. An information-distance causal claim is not licensed from a pooled coefficient.

The actual **design-only** prefit audit on the SHA256-verified original E6 944-row derivative found:

- Verified known eBird-derived Hurlbert & Liang 2012 source: **264 effects excluded**, entire original study.
- One source whose original monitoring database remains unidentified (Zalakevicius 2002, Lithuania): **4 effects not admitted**.
- Source-described original-local-observation panel: **676 effects, 26 studies, 279 species**.
- Only **13 of those 26 studies** represent **both short and long** source-coded migrant classes. These 13 contain **444 effect rows**. Thirteen studies contain only one class and cannot identify a within-study distance contrast. The 670-row stricter source-custodian panel removes two *only-long* studies and retains the exact same 13 within-study-capable studies and 444 effect rows.

## Frozen primary estimand (study fixed effects)

Among **only the 13 original studies** reporting both distance classes, fit:

```
observed source slope [days/°C] ~ 1 + I(long migration) + study fixed intercepts
weights = 1 / original reported source SE²
```

- Use the exact source-defined E6 `Slope`, `SE`, `Migration_distance` and `Study`; no new ecological outcome, species relabeling or synthetic timing.
- The primary coefficient is the weighted **within-study** long-minus-short days/°C. Include 12 fixed study dummy intercepts and check full column rank (14 columns including intercept and focal contrast).
- Use the frozen **Study × Species two-way clustered** covariance (inclusion–exclusion meat) from `scripts/payoff_b_cross_system_information.py`. The t critical value and p use **12** df (13 contributing source studies minus 1) instead of all 26 study clusters or 444 effect rows.
- **No further original covariate adjustment in the primary:** most temperature-location, arrival-location, continent and data-source categories may be largely nested by study and unidentifiable after fixed intercepts. Absorbing study-level confounding is the target.
- Report full estimate, SE, CI, p and number of source studies/species, while describing it as **exploratory robustness of a known source result, not new independent discovery**.

## Frozen stress tests

1. Repeat the same fixed-effect fit with a 99th-percentile cap on inverse-SE² weights **within the 444 source rows**, using the cap computed before the fit; no optimization.
2. Repeat unweighted source-row OLS using the same 13 study intercepts and same two-way clustering. This tests dependence on source precision weighting.
3. Repeat the fixed-effect fit 13 times, leaving out one **entire** source study each time. All results, signs and intervals are reported, without discarding influential studies.
4. Report each of the original 13 studies' **descriptive weighted** long−short mean-slope difference and source row counts. These source contrasts are not independent species replicates, and there is no per-study p-value.
5. Report how many contributing study contrasts have each sign; one positive population mean must not be called universally positive.
6. A synthetic-only rank check and source-integrity tests must reject a fabricated 944-row artifact and a sample lacking within-study pairs.

## Explicit failure / claim criteria

If source studies <10, original 444-row support drifts, fixed effects are rank deficient, or cluster covariance invalid, label `WITHIN_STUDY_NOT_ESTIMABLE` **before opening the coefficient** and do not relax gates. A CI crossing zero is **NOT_SUPPORTED** for the mean within-study association. If positive, it licenses only a robust residual within-study **published association** under the declared model, not evidence of actual cue timing, causal information access or universal population-level adaptation.

Even if the coefficient is nonzero, it does **not** identify the PAYOFF-B theoretical information-use deadline `q_wait`, true upstream cue predictive connectivity, downstream recourse, coordination, fitness or source-year V7 `q×U`. All reused source published research remains prior art. Actual bird cue availability is unmeasured.

## Original source / access contract

Usui et al. 2017: `10.1111/1365-2656.12612`; original public CC0 source `https://zenodo.org/records/4970634`. Use only the old frozen E6 GitHub Actions artifact 10953792024; original ZIP SHA256 `443cab62531d9b633aa6ee67da010fa66b6c230ef87e919d697269e77a7373f0`, original-derived 944-row CSV SHA256 `817a2d2d18931944103283c93e4d9bf80568906a21a92369ee168e4f8f203085`. The artifact contains published meta-analytic effect slopes, not raw eBird checklists; no new eBird data are fetched. Source provenance tiers are in parent PR #404 and in `docs/PAYOFF_B_E6_STUDY_ORIGIN_PARTIAL_AUDIT_20261119.md`.

Code implementation / tests are added only after this prefit design note. No change to main or the frozen V2/V7 manuscripts.
