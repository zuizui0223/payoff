# PAYOFF-B Paper 2 — original V8 data, row scatterplots and independent raw-source replay

Date: 2026-10-13
Status: SCIENTIFIC COMPUTATIONAL REPRODUCIBILITY PASS; MECHANISM AND ANONYMOUS SUBMISSION HOLD

## 1. Original immutable row outputs

Original historical V8 raw row-output restoration CI:
https://github.com/zuizui0223/payoff/actions/runs/38404051747

Original data artifact:
https://github.com/zuizui0223/payoff/actions/runs/38404051747/artifacts/11815774403

The Oct 5 environmental, bird-transfer and structural-null GitHub Actions
archives were verified to match their original registered SHA256 digests
before download. The Amaral final.rds source was verified byte-for-byte via
its pinned Git blob hash f1c9e63a377bb96152c573081e7c482cfe49ebc3
at repository commit 62c58d77c2028bd863dfe3697b0d9cf29ceaeab0.

Independent Python arithmetic using the original archived source rows and
bootstrap/permutation draws reproduced:
- 166 unique environmental source–target pairs used by 28 species;
  mean signed detrended green-up correlation change +0.369022496335682;
  95% unique-pair bootstrap CI +0.298437106219935 to +0.436480085225.
- 150 species-target observations using 72 distinct environmental pairs
  and 22 species; species-equal weighted change-on-change beta
  +0.062439691713989, CI -0.014111777339515 to +0.136348885248793.
- Fixed-arrival null beta +0.047422123617332; observed minus null
  +0.015017568096656, CI -0.052122394015565 to +0.102727480160906.
- 10,000 bootstrap draws in each of the environmental, transfer and
  structural-null analyses, and 2,000 within-window arrival permutations.
  Registered environmental degradation and negative transfer are both
  NOT SUPPORTED. A bird-specific increment over the fixed-arrival
  environmental-geometry null is not detected.

## 2. Pinned original R code independently rerun

Original three script Git blob hashes exactly match their respective
Oct 5 CI execution:
- environmental primary fe142e7202980a854a2968bc73cf50b270b0ab91
- bird transfer f60eaed13a2d164e3fd65ed4a376876aff7d1c17
- structural null 5dfa2cce7def5164ef7f42d07c9f04aadf8f6677

The R scripts ran to completion from the identical pinned upstream
final.rds in GitHub Actions run 38404684023. Its downstream Python
validator had an invocation-path error, unrelated to the R scientific
calculation. A **separate** GitHub Actions run checked all three original
R steps and the input-source SHA step finished successfully, recovered
their saved calculation outputs, and independently executed the corrected
Python comparison.

Certified replay CI: https://github.com/zuizui0223/payoff/actions/runs/38406403991

Replay comparison receipt:
https://github.com/zuizui0223/payoff/actions/runs/38406403991/artifacts/11816699221

The comparison PASSED with 9 unit tests. Across environment pairs (166
rows, 498 numeric values), species means (28 rows) and the transfer panel
(150 rows, 750 numeric values) the maximum observed absolute difference
was 0.0. Environmental species incidence also matches exactly (393 rows).
The structural null includes 150 rows, with a maximum numeric difference
5.61e-14 (floating-point precision), while original registered
summary estimates and bootstrap/arrival-permutation intervals all match.
The environmental-pair, species-mean, incidence and transfer-row CSVs
have byte-identical SHA256 across old and independently rerun outputs;
the structural rows differ in insignificant last-place numeric formatting.

This licenses: same original input, same frozen original R code, separately
executed, computationally reproducible numerical analyses and original
sample membership. It does NOT license a new independent experimental
study, causal identification of bird information use, actionability,
fitness, or a climate-change driver.

## 3. Real original-data figure preview

Actual restored spatial-pair and species-target data were plotted in two
SVGs (with raster PNG previews) only AFTER the source/row gate passed.

Figure preview CI:
https://github.com/zuizui0223/payoff/actions/runs/38405925813

Observed SVG/PNG source figure artifact:
https://github.com/zuizui0223/payoff/actions/runs/38405925813/artifacts/11816818754

- Figure 2: 166 actual pair-level points (early correlation versus late
  correlation), with no fabricated observations.
- Figure 3: 150 actual species-target observations (standardized source
  correlation change versus log-mismatch change) plus the original
  fixed-arrival structural-null regression comparator. These 150 rows
  share 72 environmental pairs and cannot be treated as 150 independently
  estimated environmental relationships.

11 figure/source tests passed. This output is an original-row scientific
preview, not a visually author-approved final journal panel.

## 4. Submission stopping conditions

The underlying publisher/reuse rights and anonymous version of the
complete data/code archive still require checking. The existing PR #328
anonymous PDF was built from summary-only Figure 2 and Figure 3, not yet
replaced by these newly recovered observation-level panels. Any
anonymized reviewer artifact must remove repository and author-identifying
metadata while preserving all original methods, results and source DOIs.
Mule-deer figures are still numerical-summary reconstructions and not
individual-data scatterplots.

The resulting scientific conclusion is that environmental correlations
strengthened, the prespecified negative transfer did not materialize,
and the apparent positive slope is structurally explainable. Neither
the reason birds did not show the registered transfer nor the effect on
demographic fitness is identified.
