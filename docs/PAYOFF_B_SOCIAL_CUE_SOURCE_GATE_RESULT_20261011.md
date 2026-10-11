# PAYOFF-B social-cue source Gate-A result — 2026-10-11

Status: **SOURCE_ACCESS_OR_SCHEMA_BLOCKED**. Admitted primary Dryad files: **0 of 7**. Biological outcomes: **UNOPENED**.

## Verified source and CI facts

- Samplonius & Both (2017), Dryad DOI https://doi.org/10.5061/dryad.bs427, seven file IDs / sizes frozen before download attempt.
- Source-only GitHub Actions run: https://github.com/zuizui0223/payoff/actions/runs/38107447614 , commit 160f2caf743c41e3f0c828be2e6735cd0396e193.
- Six network-free schema / firewall tests passed.
- All seven registered Direct Dryad /api/v2/files/{id}/download URLs returned **HTTP 401 Unauthorized**. The fallback public file_stream URLs yielded no matching registered files. The workflow failed closed, and uploaded its metadata/error-only audit receipt.
- No biological observations, treatment contrasts, regression coefficients, joining outcomes, or survival/fitness values were opened. This is an access failure, NOT a negative biological test.

## Inspectable published model code on a separate public GitHub mirror

A secondary, independently inspectable text copy of arrival_early_late.R exists at:
https://github.com/Dahouabdelhalim/Projects/blob/main/R_files_Zenodo/arrival_early_late.R

Do not claim that the mirror's bytes match the original Dryad source; it is **textual script provenance, not source archive validation**. The script reads semicolon-delimited files with decimal commas. It indicates:
- 2014 and 2015 resident-hatch manipulations merged to nestbox/plot records by year and nestbox, then to male arrival records by year and replicate;
- titden = N.x / hectare (plot-level resident competitor density, NOT a random density treatment);
- relhd = resident hatch timing; relexphd = planned hatch date; relmarr = relative male arrival; pair = pairing outcome;
- mring2 is male identity; replicate is a subplot identifier; rcs = ncs - 9.064748 is clutch-size covariate;
- a published model contains pair as the binary response, relhd × relmarr, relexphd, rcs, yr, and random intercepts for male identity and replicate.

These are source-code features, not newly calculated effects. All seven original Dryad CSV sources remain unmaterialized by PAYOFF-B.

## Specific pre-data biological comparator now visible, but NOT estimable

The secondary published script makes one narrow additional question feasible **if** original raw sources become available:

Does the effect of *randomized resident hatch timing* on flycatcher male pairing vary with premeasured plot-level resident density, conditional on relative male arrival and plot/year structure?

A secondary model could retain the published timing-by-arrival interaction and original control covariates, then assess the resident-hatch-timing × competitor-density interaction with plot/year dependencies respected. Density is observational, not independently manipulated; thus this moderation cannot establish a pure informational mechanism, the causal density effect, or the fitness benefit of avoiding dangerous competitors. Binary male pairing is not offspring survival or fecundity.

Freeze model specification, primary outcome, density measurement time, effect-modifier range, effective independent replication and multiplicity/exploratory status **before opening new outcomes**. Keep original models as prior art. Do not select alternative windows/densities after seeing the fit.

## Strong novelty collision to retain

Morinay, Forsman & Doligez (2020), Animal Behaviour 161:103–113, DOI https://doi.org/10.1016/j.anbehav.2020.01.002, already separated heterospecific song playback from real great tit pair presence and tested aggressiveness-dependent settlement in *collared flycatchers*. The 2017 manipulation concerns *pied flycatchers*. No unverified cross-paper joins or pooled effect sizes.

## Decision

Do not replace inaccessible source data by model assumptions. PR #325 is a source-readiness and prior-art gate only. The main V7R and V8 falsifications and V4 manuscript remain frozen; there is no new independently demonstrated fitness or information-control mechanism. The next valid step is an authorized exact source import, not a claim upgrade.
