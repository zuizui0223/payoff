# Ortega within-animal stopover analysis implementation plan

> For agentic workers: use superpowers:executing-plans to implement this one-task plan. Steps use checkboxes.

**Goal:** Estimate one conditional within-animal departure-phase/stopover association from authenticated original biological data.

**Architecture:** Reuse the existing XLSX XML parser, validate one-to-one source joins, and estimate exact two-way fixed effects by Frisch-Waugh-Lovell residualization. Keep only aggregate outputs and publish the reproducible analysis on a separate draft branch.

**Tech Stack:** Python 3.12, NumPy, existing source parser, pytest; statsmodels only for an independent verification if available.

**Spec:** data/payoff_b_ortega_within_animal_contract_v2_20261122.json; original v1 and its support failure are retained.

## Global Constraints

- Original source SHA256 is 2645420b74c8e2228eb555d14c755bba207c49ea72ecb2eff4c950892f743364.
- Primary model is stopover ~ DFP_Start + animal fixed intercepts + year fixed intercepts.
- Complete cases and repeated animals only; zero stopovers retained; missing values never imputed.
- Bootstrap 10,000 animal draws, seed 20261122; refit all fixed effects each time.
- No arrival-phase forecast, full-journey speed, duration adjustment, raw-source publication, eBird, or manuscript replacement.
- Existing animal/year random-effect analyses are prior art; this is post-publication exploratory robustness.

## Review Focus

- An unbalanced panel requires exact fixed-effect projection, not one pass subtracting two means.
- True zero days and BBMM missing values must remain distinct.
- Duplicate source keys must fail rather than silently overwrite.
- Each bootstrap draw must retain its entire animal history and receive its own cluster label.
- Support and missingness must be reported even if the new coefficient is not supported.

## Task 1: Authenticated within-animal analysis and source-backed result

**Files:**

- Create scripts/payoff_b_ortega_within_animal.py.
- Create tests/test_ortega_within_animal.py.
- Create data/payoff_b_ortega_within_animal_support_20261122.json.
- Create data/payoff_b_ortega_within_animal_result_20261122.json.
- Create docs/PAYOFF_B_ORTEGA_WITHIN_ANIMAL_RESULT_20261122.md.

**Interfaces:**

- join_records(phase, actuators) validates source identities and returns normalized rows.
- repeated_panel(rows) returns complete observations from repeated animals.
- fit_twfe(rows) returns the common slope, nuisance rank, residual degrees of freedom and residual exposure variance.
- resample_animals(rows, rng) returns entire, independently relabeled sampled histories.
- analyze(rows, contract) returns aggregate inference and all year-omission outcomes.
- CLI accepts --source, --contract, --support-only and --output.

- [ ] Step 1: Add behavioral tests for zero/missing handling, duplicate joins, an unbalanced hand-constructed fixed-effect slope of -0.5, no residual identifying variation, and whole-history bootstrap relabeling.
- [ ] Step 2: Run the tests and observe missing implementation failures. Expected: the new interfaces do not yet exist.
- [ ] Step 3: Implement the reader, exact estimator, support check and bootstrap; run the focused tests. Expected: all new tests pass.
- [ ] Step 4: Run support-only against the SHA-verified original workbook. Expected: 152/72 source, 127/65 complete, 15 genuine zeros; publish all support counts before fitting. If the declared support fails, preserve that outcome and do not fit.
- [ ] Step 5: Run the fixed 10,000-replicate analysis once, independently verify the coefficient using a full categorical-design least-squares fit, and check every year omission. Expected: reproducible values; no required biological sign.
- [ ] Step 6: Write the result with prior-art and identifiability limits, then run the full repository tests. Expected: no new failures; report existing environment-dependent failures separately.
- [ ] Step 7: Commit the code, tests and aggregate result; obtain a fresh review and fix material issues. Push the isolated branch and open a draft PR without merging.

## Decisions made before fitting

- The initially considered arrival-phase/speed predictive comparison was rejected because the predictor encodes the arrival date.
- No search for a favorable endpoint follows an unsupported primary result.
- The source is already published and known; fixing this comparison before its new coefficient does not make it independent confirmatory evidence.
- After source-only support inspection, v2 corrects the unnecessary one-component rule. See docs/PAYOFF_B_ORTEGA_WITHIN_ANIMAL_DESIGN_20261122.md. Rows, model, variables and bootstrap remain unchanged.
