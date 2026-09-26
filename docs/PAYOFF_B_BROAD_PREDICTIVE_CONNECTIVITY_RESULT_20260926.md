# PAYOFF-B broad predictive connectivity — frozen result

Frozen: **2026-09-26**

## Registered result

The preregistered broad-bird information-axis prediction is supported in the
declared pooled GAM.

The analysis retained 3,311 outcome rows from 37 species, 635 species-cell
units and eight outcome years. Predictive connectivity was estimated only from
preceding years, using the frozen 8-year window and separate detrending of
source and target green-up series.

Primary coefficient:

[
\hat\beta_{\rho}=-0.0462,
\quad SE=0.0208,
]

[
95\%\ CI=[-0.0870,-0.0054],
\quad p=0.0265.
]

Thus higher pre-existing predictive connectivity is associated with smaller
arrival–green-up mismatch in the registered pooled analysis.

## The result is not a generic climate-trend effect

The sensitivity pattern is informative.

- 6-year detrended window: beta = -0.0294, CI crosses zero.
- 8-year detrended window: beta = -0.0462, registered support.
- 10-year detrended window: beta = -0.0569, CI below zero.
- 8-year **undetrended** correlation: beta = +0.0043, p = 0.831.
- Gaussian binary-q bridge: beta = -0.0685, CI below zero.

The information signal therefore appears when shared long-term trends are
removed. Simply correlating raw source and destination green-up dates produces
essentially no effect.

## Dependence audit

The 3,311 rows are not 3,311 independent routes. The same species, cells,
source–target pairs and years recur.

Re-expressing the model with species-cell and year fixed effects keeps the
coefficient negative (about -0.0627), but cluster-robust uncertainty is wider:

- cluster by species: 95% CI -0.153 to +0.028;
- cluster by cell-year: -0.131 to +0.006;
- cluster by source–target pair: -0.143 to +0.017;
- two-way species × source–target pair: -0.159 to +0.034.

The direction is nevertheless not carried by one obvious taxon or year:
all 37 leave-one-species-out fits and all eight leave-one-year-out fits remain
negative.

A stricter species-by-species decomposition is mixed. Of 33 estimable species,
21 have negative coefficients and 12 positive; the one-sided sign-test p-value
for a negative majority is 0.081. The inverse-variance species summary is
-0.0415 with 95% CI -0.0863 to +0.0033.

## Licensed interpretation

The result should therefore be described as:

> **a pooled, directionally stable association between pre-outcome predictive
> connectivity and smaller phenological mismatch, with uncertainty that becomes
> non-conclusive when species and route dependence are treated conservatively.**

It should **not** be described as a universal species-level effect.

This distinction matters for PAYOFF-B. The broad signal says information
structure is relevant to realized mismatch at the macroecological level. It
does not establish one common information coefficient for all migratory birds.

## Contrast with wigeon

The result is deliberately kept next to the wigeon null.

- Broad birds: predictive connectivity is associated with realized mismatch in
  the registered pooled model.
- Wigeon: predictive connectivity does not strengthen the phase-correction
  coefficient across 224 staging transitions.

This supports a useful separation:

[
\text{information available before commitment}
\neq
\text{strength of correction after phase error appears}.
]

Predictive connectivity may matter by changing earlier decisions and reachable
timing regimes rather than by acting as a universal stronger feedback
controller.

## Provenance

Primary/dependency workflow:

- run 36233116170
- artifact 10903132499
- SHA256 a14f80f4ddcfe55aff27e1069cadb1ccd35189ee2c5643968d69e54e856fc10c

Sensitivity workflow:

- run 36231377031
- artifact 10903000065
- SHA256 5416d21a08a133af16a17307498afd82c5544b0d63c796d70f2d45209ad8db9c
