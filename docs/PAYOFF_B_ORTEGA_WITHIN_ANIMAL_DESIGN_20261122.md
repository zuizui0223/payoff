# Ortega within-animal comparison: coefficient-blind design amendment

Date: 2026-11-22. This is exploratory reanalysis of already published data.

The original design was committed at eaf8d99. Its source-support result was
committed at 72a5ad4 before the new slope or interval was computed. That result
remains SUPPORT_NOT_MET because v1 required one connected animal-year component.
No primary coefficient was opened under v1.

The repeated complete-case panel has 100 animal-years from 38 animals in eight
observed years. The animal-year graph has two components: 2011–2012 (4 animals,
8 rows) and 2014/2016–2020 (34 animals, 92 rows). Its fixed-effect nuisance rank
is 38 + 8 - 2 = 44, with 55 residual degrees of freedom after adding one slope.
The fixed-effect residual exposure RMS is 13.5967 days.

## Why the requirement is corrected

A connected graph is needed to compare all individual and year intercept levels
under one normalization, but it is not needed for a common within-component
slope. The slope is unique when x' M_Z x is positive, even if individual nuisance
coefficients are not unique. Exact projection onto the fixed-effect column space
is invariant to component-specific reference levels.

An independent statistical review, still without the new coefficient, confirmed
this distinction. Version 2 allows component-specific normalizations while
retaining every original row, predictor, outcome, model, bootstrap setting and
sample-size/variation requirement. A behavioral test verifies a known -0.5 slope
in a disconnected unbalanced design and invariance to arbitrary component level
shifts. The original connected-graph rule still returns its original failure.

The later component supplies 97.962% of residual exposure sum of squares; the
early component supplies 2.038%. The common slope therefore draws its identifying
variation mainly from the later cohort. These are not two independent biological
replications, nor the same animals observed throughout all eight years.

## Interpretation remains limited

Version 2 is a transparent structural amendment made before coefficient access,
not a pass under the original design or an independent confirmatory study.
The result concerns within-animal time allocation conditional on observed years.
The original paper already reports compensation and mixed models with animal
and year effects: https://doi.org/10.1038/s41467-023-37750-z.

Whole-journey speed is distance divided by total journey time. It was excluded
from the proposed arrival forecast before any fit because it encodes arrival
time. Stopover is modeled as an outcome, not a departure-time predictor; total
journey duration is not adjusted for, and information use or causality is not
identified. DFP itself is a retrospectively reconstructed seasonal coordinate.
