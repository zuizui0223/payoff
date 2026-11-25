# Wave 13b — executed descriptive immune challenge analysis

2026-11-25. Draft PR #426. Secondary analysis only; no primary theta, independent-family interval, or pooled meta-analysis.

Murillo-Rincón, Laurila & Orizaola (2017), Oikos 126:565–571, DOI 10.1111/oik.04014, data DOI 10.6084/m9.figshare.4239314.v1. Original workbook MD5 bbf6ad22d4ca9add79723a7a85f8bb3c and SHA256 e7d47607bc2501d73ca94d430104bec6adde1eeb89feb8c1344f0de211938488 verified. The source dictionary identifies 426 unique larvae, 21 male × female families with 9 male and 7 female IDs. Three connected components of families sharing same-sex parent IDs contain 9,9,3 families, respectively. Thus no naive bootstrap of 21 independent families. Original assignment/rearing Methods and independence from JAE 2017 cohort are not fully verified. Descriptive, complete-family target rather than an ITT effect.

## Source-supported estimates

17 families (9/7/1 from parental components) meet the fixed all-six-cell complete-duration-and-mass rule, yielding 343 complete endpoint rows. 188 observed injected-response records in those families support a separate signed percentage response analysis. Each family/cell mean equally weighted. No missing outcomes imputed or untreated immune response fabricated.

| Treatment | Normal larval days | Delayed larval days | Delayed − normal |
|---|---:|---:|---:|
| PHA immune challenge | 37.285294 | 37.287255 | +0.001961 |
| APBS sham injection | 37.529412 | 32.117647 | −5.411765 |
| Untreated | 36.008824 | 33.767647 | −2.241176 |

PHA vs APBS difference of delayed-minus-normal duration: +5.413725 days. Leave-one-parental-component-out estimates +7.395833, +3.8, +5.431250 days. These are sensitivity point estimates, not confidence limits. APBS vs untreated −3.170588 days and PHA vs untreated +2.243137 days; retain handling-specific differences. Original Appendix 2 reports a model-adjusted PHA/APBS difference of duration contrasts +4.820 days and omnibus phenology × immunity p<.0001. The raw family-balanced descriptive calculation is consistent in direction, not an exact replication of the original model.

Delayed vs normal log mass ratios: PHA −.180287, APBS −.199166, untreated −.081901. PHA vs sham mass interaction +.018879, with leave-component-out point estimates −.099811, +.091141, +.031976; no consistent challenge-specific mass penalty.

Signed tail-width response (%) under PHA: normal 6.996675, delayed 1.763239; APBS normal .895022, delayed −1.275605. Difference of delay-associated response changes PHA minus APBS −3.062810 percentage points; leave-one-component-out −.095100/−6.002770/−2.709190. Original immune-response omnibus interaction p=.130, so no independently established challenge-specific response loss. All recorded signed responses retained, not a measured infection survival endpoint. Duration/mass and immune observations need not be the same individuals; no mediation or causal cost of acceleration.

## Reproduction and next gate

CI run https://github.com/zuizui0223/payoff/actions/runs/45544222895, job 138969813827, artifact 14990786608; upload ZIP SHA256 2c69a7235ccd724c20f0707a253788fa687afd488b0922c14916388f9674eeff. Exact source-checked aggregate JSON in data/payoff_b_immune_challenge_descriptive_wave13_result_20261125.json. ZIP not independently downloaded. Original supplement text inspected; screenshot retrieval failed, so no claim of visual table verification. No primary eligible theta added; no cross-paper independence claimed. Next source priority: independent temperature/resource constraints experiment, check cohort years, assignment grain and archive; or actual host-switching × phenological perturbation experiments. Preserve all source holds and frozen manuscripts.