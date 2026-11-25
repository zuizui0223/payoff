# Pardee et al. secondary snow-removal × pollen-supply contrast: all three species evaluated

2026-11-25. Continuation of draft PR #426; no new independent study lineage. The original result, diagnostic and amendment remain separately preserved. Source DOI 10.5061/dryad.kd1r166, article DOI 10.1111/1365-2745.13152. Original source bytes were authenticated by provider MD5 and pinned SHA256 before fitting. The article states that snow removal advanced flowering in all four focal species, and that reproductive and visitor responses differed; it already reports a lack of pollen supplementation effect. This reanalysis asks a narrower, secondary interaction question rather than claiming discovery of the article's original finding.

## Source diagnosis and amendment

Diagnostic run 45531164650 (completed), artifact 14985595936. Delphinium has one literal N/A in Total_seeds, now treated as missing, not zero. Potentilla has one pair of nonidentical rows sharing a plant key, both excluded in the main amended analysis; first-row and last-row retention separately tested. Claytonia's original result is exactly reproduced (all estimates and bootstrap summaries), and a post-open sensitivity drops nine noncanonical plant-number rows. All other seed zeros, source pairing, allocation, equal weighting of plot averages and frost strata, >=5 paired plots per stratum, and 10,000 plot-stratified bootstrap draws with seed 20261125 are unchanged. No source row was redistributed. Normalization synthetic checks passed. No new independent preregistration claimed.

## Main secondary estimates

Mean seeds per observed plant, aggregated within plot/pollen arm then equally across paired plots and frost strata. Each species' primary analysis within this secondary lane:

| Species | Paired plots | Natural snow NP | Natural snow AP | Removal NP | Removal AP | Snow-removal change NP | Snow-removal change AP | theta_snow | 95% interval | Bootstrap variance |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| Claytonia lanceolata | 35 | 11.004745 | 13.232639 | 7.754630 | 8.722222 | -29.5338% | -34.0855% | -0.066776 | [-0.533126,0.413048] | 0.0576645 |
| Delphinium nuttallianum | 34 | 53.395833 | 55.508333 | 65.347222 | 44.090278 | +22.3826% | -20.5700% | -0.432276 | [-1.073163,0.219176] | 0.1072029 |
| Potentilla pulcherrima | 36 | 61.852431 | 60.180556 | 54.473611 | 53.536111 | -11.9297% | -11.0408% | +0.010042 | [-0.468481,0.478322] | 0.0586171 |

NP = no added pollen; AP = supplemental pollen. theta_snow = log snow-removal response ratio under AP minus that under NP. All three intervals include zero. In Claytonia and Potentilla, the NP snow-removal point estimate is detrimental; no positive attenuation established. In Delphinium, the NP response is positive in point estimate (interval includes zero), so calling the negative interaction failed rescue of a known loss would be logically wrong. The apparent change in direction is descriptive, not evidence of a significant reversal. No equivalence inferred. All estimates are complete-case rather than intention-to-treat.

Delphinium: 229 original rows, 228 complete, 82 zero seed counts, one missing; paired plot counts 9/10/9/6. Potentilla: 260 original rows, two conflicting records excluded, 252 complete of 258 retained, six missing, two zero seed counts, three observed plots without both pollen arms; paired plot counts 9/8/10/9. Claytonia: original 231 rows, 230 observed pollen/seed records, 35 seed zeros; paired plot counts 8/9/9/9.

## Sensitivities

| Species / rule | theta_snow | 95% interval |
|---|---:|---|
| Claytonia canonical plant numbers only, 34 paired plots | -0.099327 | [-0.569113,0.403447] |
| Potentilla retain first conflicting record | +0.005207 | [-0.473449,0.475065] |
| Potentilla retain last conflicting record | +0.026095 | [-0.453271,0.492108] |

All 10,000 bootstrap draws finite in every contrast. Conclusion stable to these prespecified data-processing sensitivities; not a universal claim of robustness to unknown attrition. No attempt to establish which of the two conflicting raw records is correct.

## Biological and meta-analytic interpretation

None of the three secondary snow-removal × externally supplied pollen contrasts gives clear evidence of attenuation. The original article additionally reports substantial differences in visitor response and flowering advance, but pollen treatment does not isolate endogenous compensation, and snow removal alters abiotic exposure. Neither mechanism-specific limitations nor a universal absence of pollen limitation can be inferred. No independence assumed between species sharing one study/plot system, no species-level pooled estimate or heterogeneity inference. The 3 main contrasts and 3 sensitivities are not 6 independent effect sizes. Cumulative screen remains 31 source lineages. Primary endogenous-recourse × partner-mismatch theta count remains 0; no primary pooling.

Next direction: independent seasonal perturbation × supplementation experiments, distinguishing external service-relief from the original endogenous recourse hypothesis and retaining all null results. Candidate Gezon et al. (2016), 10.1111/gcb.13209, must undergo separate exact source and prior-art admission before fitting. The Vázquez raw-source access issue remains unresolved. No manuscript replacements or merge.

## Reproduction receipt

Amended run [45535654566](https://github.com/zuizui0223/payoff/actions/runs/45535654566), job 138941482021. Exact aggregate [JSON](../data/payoff_b_pardee_source_amended_fit_result_20261125.json) parsed from executed logs, artifact 14986192837, ZIP SHA256 8ba29b42910c74676e6c2ef6b3b2e1e1308344e6e478ca943627010f7c972657 (upload log, ZIP not independently downloaded). No raw IDs or source rows exported, no independently replicated alternative implementation.
