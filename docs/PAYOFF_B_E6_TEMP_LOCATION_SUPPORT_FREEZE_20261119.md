# PAYOFF-B E6 — source-only temperature-location identification gate

Date: **2026-11-19**. Status: **post-open exploratory design audit, no new temperature-response coefficients opened**.

## Ecological target

The existing [E6 Usui meta-analysis reconstruction](../docs/PAYOFF_B_CROSS_SYSTEM_INFORMATION_RESULT_20260928.md) shows that 279 migratory bird species differ by migration-distance class: adjusted long-minus-short temperature responsiveness **+0.421 d/°C**. That effect was reported by Usui et al. (2017) and is **not** a new PAYOFF-B discovery. Migration distance alone does not identify information access: endogenous/photoperiodic programmes and differences in where climate was measured are competing explanations.

The original Usui [open CC0 file](https://zenodo.org/records/4970634) contains `Temperature_location` and `Migration_distance` metadata. Before any new interaction is fitted, test whether these variables have **independent within-study support**. The requested comparison is a *proxy-only* question: whether the long-vs-short gradient differs by the location at which a study measured its climate predictor. `Temperature_location` is a **researcher-defined covariate location**, not observed animal access to a cue, residence at that site, or a value of future information.

## Locked source and original selection

- Original Usui CSV `Usui_et_al_2016_metadata_dryad.csv` at [Zenodo 4970634](https://zenodo.org/records/4970634), originally [Dryad doi:10.5061/dryad.mb4nd](https://doi.org/10.5061/dryad.mb4nd), license CC0.
- Original SHA256 `68816f6cbfccbb9b47b45be0df49f077db914c8e43e567d0ed2cac9bbafde56c`.
- Use frozen E6 selection only: source `Predictor == 'temperature'`, source `Migration_distance in {'short','long'}`, finite `Slope` and positive finite `SE`. The selection must reproduce exactly **944 rows, 28 studies, 279 species**, unchanged.
- For the *design-only* audit no `Slope`, `SE` or outcomes are output, even as per-study means. They are read **only** to apply the already frozen E6 inclusion rules. No effect coefficient is fitted.
- Grouping unit = original source `Study`; also report unique source `Species`. Rows within the same study/species must not be treated as independent systems.

## Predeclared design admission (source-only)

First, report every **verbatim source `Temperature_location` category**, with number of rows, studies, and species, stratified by migration-distance class. Do not interpret unlabeled or uncertain values as "near" or "far" after seeing the outcome.

A subsequent predeclared biological interaction would only be considered if all gates hold:
1. At least **two semantically distinct and author-documented climate-measurement-location classes** can be defined *without inspecting the response*.
2. At least **five independent studies** contain a fully crossed 2×2 layout: two distance classes × both location classes. This is the key within-study identification requirement.
3. Each location class contains both distance classes in at least **ten distinct studies**; no one study contributes over half the effective eligible contrasts.
4. The original two-way clustered study/species covariate matrix is full rank after adding the interaction; source term semantics and classification are frozen **before** seeing the new coefficient.

If any gate fails, declare `E6_INFORMATION_LOCATION_INTERACTION = NOT_IDENTIFIABLE_OR_NOT_SUPPORTED_AS_DESIGN`, **without fitting** it. A marginal interaction with location potentially confounded with study is insufficient for a causal information-distance claim. Under any pass, the test remains **post-open exploratory**, and a biological information-access mechanism remains unidentified without actual animal cue exposure or commitment-time data.

## What this is not

- Not a restart of stopped V5 annual-cycle propagation (already occupied by Brlík et al. 2026).
- Not a fourth V7 flyway or a replacement for missing 1982–2011 goose regional onsets.
- Not a new cross-taxon plant–pollinator meta-analysis, not a direct q×U test, not an extension of source claims beyond its measurements.
- No eBird or TinyFish inputs; no PDF-derived invented numbers; no raw biological outcome reanalysis until the design gate is audited.

## Execution

The dedicated GitHub Actions source job downloads the exact original CC0 file, checks SHA256, runs the source-only audit, writes a JSON artifact, and prints its **categorical support counts**. No effect size is fitted in this stage.

```bash
python -m scripts.payoff_b_e6_temperature_location_support \
  --input original_usui.csv \
  --output outputs/payoff_b_e6_temperature_location_support.json
```
