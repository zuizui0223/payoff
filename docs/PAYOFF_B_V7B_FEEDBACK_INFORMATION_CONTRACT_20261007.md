# PAYOFF-B V7B prospective contract — local feedback information × recourse

Date: **2026-10-07**  
Status: **PRE-ENVIRONMENT-OUTCOME; POST-V7R-NULL**

This route starts only after the frozen V7R forecast-predictability × recourse test returned a robust null. It does not reopen or rescue V7R.

## 1. Question

V7R used `q_F` = cross-region spring-onset predictability, which asks how well conditions in one migration region forecast a future region.

V7B asks a different question:

> Is corrective stopover behavior stronger where the **local seasonal state is more environmentally readable** and downstream temporal recourse remains?

Define `q_B` as a behavior-independent local feedback/state-estimation information proxy.

## 2. Fixed biological system

Use the same three Kölzsch barnacle-goose flyways and the same frozen Stage-3 region and transition tables used by V7R.

No transition threshold changes.

V7B uses the 95 individual transition rows already admitted across the ten V7R transition types.

## 3. Fixed environmental sampling locations

Environmental data are sampled at the frozen generalized-region coordinates from the pre-existing Stage-3 region tables.

Primary sampling unit:

`one fixed MODIS cell containing each region coordinate`

No individual GPS point, individual arrival location, or behavior-selected pixel is used to define q_B.

Primary origin regions:

- Greenland: R1, R2
- Svalbard: R1, R2
- Barents Sea: R1, R2, R3, R4, R5

## 4. Environmental years

Request the fixed window **2006–2011** at every primary region coordinate.

For a behavioral transition row from year y, use q_B at its origin region in the same year y.

No nearest-year substitution.

## 5. Environmental processing

Use the existing PAYOFF IRG reconstruction family:

`src/irg_reconstruction.py`

with the current-product environmental lane:

- MOD09Q1.061 surface reflectance
- MOD10A2.061 snow information

through the existing AppEEARS request / ingest layer.

This is a new V7B environmental measurement, not a bit-for-bit reconstruction of Shariatinajafabadi et al. (2014), who used MOD13A2.

## 6. Primary q_B

For region j and year y, fit the frozen annual NDVI curve and define

`q_B,jy = peak_IRG_value_jy`.

This is the maximum positive first derivative of the scaled annual NDVI curve.

Interpretation: **local phase-readability potential**.

Under a simple observation model with comparable local-greenness noise, a steeper spring trajectory maps the same greenness uncertainty to a smaller timing uncertainty.

q_B is not claimed to be neural information, Fisher information, or a direct measurement of what a goose perceives.

## 7. Mandatory environmental sensitivities

1. inverse spring time scale: `1 / spring_scale_days`;
2. peak-IRG signal-to-fit-error ratio: `peak_IRG_value / fit_rmse`, only when fit_rmse is finite and strictly positive; no arbitrary epsilon;
3. region-level median q_B across 2006–2011 instead of same-year q_B;
4. failed region-years are excluded rather than imputed.

A neighborhood/buffer extraction requires a separate source-only contract and cannot replace the primary single-cell result after outcomes are opened.

## 8. Direct behavioral response

Do not use lambda as the primary response.

For each individual transition row i:

- E_i = incoming phase error at origin;
- D_i = origin stopover duration in days;
- B_i = standardized local q_B for origin-region × year;
- R_e = frozen V7R remaining-route recourse.

Positive E means the migrant is late relative to local seasonal phase.

Corrective stopover shortening predicts `dD/dE < 0`.

## 9. Primary model

Fit:

`D_i = alpha_transition[e] + alpha_year[y] + beta_E E_i + beta_B B_i + beta_EB E_i B_i + beta_ER E_i R_e + beta_BR B_i R_e + beta_EBR E_i B_i R_e + error_i`

Transition fixed effects absorb transition-level intercept differences and the main effect of R.

Focal coefficient: **beta_EBR**.

Directional prediction:

`beta_EBR < 0`.

## 10. Scaling

Standardize q_B across all successfully reconstructed primary region-year environmental units before joining behavior rows:

`B = (q_B - mean(q_B)) / sd(q_B)`.

E and R retain their existing scales.

## 11. Primary inference

q_B is shared by behavioral rows from the same origin region-year.

Primary inference uses a fixed-seed block permutation:

- hold E, D, R, transition and year identity fixed;
- within each origin region, permute annual q_B labels among available years;
- all rows sharing a region-year receive the same permuted q_B;
- refit the identical model;
- use 20,000 fixed-seed permutations unless the complete unique space is smaller, in which case enumerate all unique permutations.

Seed: **20261007**.

One-sided p:

`p = (1 + count(beta_EBR_perm <= beta_EBR_observed)) / (1 + N_perm)`.

## 12. Admission gate

Do not open the behavioral interaction unless:

1. at least 8 of 9 primary origin regions have >=2 valid q_B years;
2. at least 80% of the 95 frozen behavioral rows join to valid same-region same-year q_B;
3. all 3 flyways remain represented;
4. q_B has nonzero variance;
5. q_B uses no focal goose stopover duration, phase correction, or arrival response.

If the gate fails: `V7B_PRIMARY = NOT_ESTIMABLE`.

No environmental threshold is relaxed after behavioral results are seen.

## 13. Mandatory behavioral sensitivities

1. inverse spring-scale q_B;
2. q_B_snr;
3. region-median q_B;
4. remove low-support Barents R5→R7;
5. transition-level direct stopover gain as a descriptive cross-check.

No sensitivity replaces the primary.

## 14. Claim ceiling

If supported:

> Corrective stopover responses were strongest where independently measured local green-up dynamics provided greater phase-readability potential and more downstream temporal recourse remained.

Not licensed:

- geese directly sense satellite NDVI;
- peak IRG is a direct cognitive information measure;
- q_B is exact Fisher information;
- causal manipulation of cue reliability.

If null, close this environmental-readability proxy without redefining q_B post hoc.

## 15. Stop rule

Do not tune region coordinates, MODIS cell choice, year inclusion, IRG processing, recourse construction, or transition admission after outcome opening.
