# GloPL seasonal pollen limitation — wave 7 result

2026-11-25. Draft PR #426; no merge or replacement of any frozen manuscript.

## Source inventory

The original GloPL author CSV contains 2,969 source rows (SHA256 8c764ce03da86db0cb280e8f8f92cc0e62e2df6d85a2226e3246dc1afeb3f65f; Git blob d22fe333b19489c473e076dd173ed7a67b1afbf0). The 16 candidate-paper DOIs identify 95 rows when all contexts are inspected, not only keyword hits. Exact early/late label matching within study, taxon, population, year, supplementation unit and other context identifies 28 pairs across 12 papers; 27 have a common endpoint with positive means, SD and N. These are screening counts, not independent effects or a systematic-review census. See data/payoff_b_glopl_seasonal_inventory_initial_20261125.json for exact source IDs and all candidate contexts.

## Confirmed design and executed secondary contrast

Totland & Schulte-Herbrüggen (2003), DOI 10.1657/1523-0430(2003)035[0242:BSIFVA]2.0.CO;2, original methods specify separate high-elevation early and late periods in 2000, naturally flowering individuals and random treatment assignment among flowers on separate plants within each period. Source Fig. 1 measures seed-to-ovule ratio. Initial generic extractor failed because the third, low-elevation row also contained the early label. The explicit altitude filter was amended before opening either numerical contrast. It matches source IDs 1073/1074 and 1076/1077 and excludes IDs 1072/1075. No alternative endpoint, significance filter or source selection based on means.

| Species | Early natural / supplemented | Late natural / supplemented | Early lnRR | Late lnRR | Late − early | 95% maximum-variance sensitivity |
|---|---|---|---:|---:|---:|---|
| Cerastium alpinum | .40 / .54 | .32 / .35 | .300105 | .089612 | -.210492 | [-1.218283,.797298] |
| Cerastium cerastoides | .57 / .62 | .25 / .35 | .084083 | .336472 | .252389 | [-.517302,1.022080] |

All four GloPL cell sample sizes per species are 12. Conditional zero-between-period covariance approximate normal 95% intervals: alpinum [-.931390,.510405]; cerastoides [-.308847,.813625]. Marginal variances are delta-method approximations from compiled SD/N and within-period independence; cross-period covariance is not known. Maximum-variance intervals use the Cauchy–Schwarz upper bound given those marginal variances; these are sensitivity intervals, not exact confidence coverage. No between-species test or pooled estimate. The opposite signs of the point estimates are descriptive only. In both species natural seed/ovule ratio declines later, while supplemented seed/ovule ratio also declines. This motivates separating variation in pollen limitation from changes in the reproductive ceiling, without claiming an identified physiological mechanism or true partner mismatch.

This is one publication, two species-level secondary contrasts based on source summary cells, not newly collected raw plant data. Natural flowering period is not an assigned timing perturbation; external pollen provision is not endogenous corrective capacity. Primary theta eligibility remains 0.

## Next exact source gates

- Kalisz & Vogler (2003), DOI 10.1890/02-0519: six early/late pairs across three sites and two years, all with fruit-set means/SD/N. Original methods refer to floral treatments within whorls and attempted within-plant allocation, so treatment covariance must not be ignored. Publisher supplement collection https://doi.org/10.6084/m9.figshare.c.3297944 is a next source route; no original files inspected or new effect fitted.
- Geib & Galen (2012), DOI 10.1890/11-1271.1: original abstract explicitly links early specialist versus later generalized T. parryi cohorts, bumblebee density and reproductive redundancy. Two Trifolium early/late GloPL candidates are available; exact supplementation protocol and shared units require review. Publisher supplement collection https://doi.org/10.6084/m9.figshare.c.3304797. Existing findings are prior art. Do not convert their demographic conclusion into a new causal result.
- Stanton (1987), DOI 10.2307/2444020: four paired flower-colour strata, one paper. Copland & Whelan (1989), DOI 10.2307/2260766: two paired years, one species. Full unit/contrast verification required.
- Robson (2010), DOI 10.1139/B10-003: source abstract compares earliest capitula with peak flowering, so the compiled Late label must not be assumed to mean the end of the flowering season.

## Reproducibility

Run 45539515597, job 138954294354, artifact 14988711746; upload ZIP SHA256 0fa126b721aa366d867f456ca870ab54a6ebaa15d02d341cdd49cd2c45d3b53f. Both calculation steps and synthetic arithmetic checks completed; exact log-derived result JSON is data/payoff_b_glopl_cerastium_amended_result_20261125.json. The artifact ZIP has not been separately downloaded. No independent source-data replication, no new primary effects, and no cross-study pooling.
