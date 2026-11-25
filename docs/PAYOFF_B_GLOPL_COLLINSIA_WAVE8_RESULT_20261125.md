# Wave 8 result — Collinsia seasonal selfing and remaining reproductive limitation

2026-11-25. Draft PR #426. One additional GloPL publication design audited; no primary eligible timing × endogenous-recourse effect, no meta-analytic pooling. Keep the separate Cerastium results and all frozen manuscripts unchanged.

## Executed source extraction

Kalisz & Vogler (2003), Ecology 84:2928–2942, https://doi.org/10.1890/02-0519. Original published methods and Tables 1–2 accessed via searchable article text (https://www.academia.edu/61005907/Benefits_of_Autonomous_Selfing_Under_Unpredictable_Pollinator_Environments). The numerical source is the authors' GloPL CSV (SHA256 8c764ce03da86db0cb280e8f8f92cc0e62e2df6d85a2226e3246dc1afeb3f65f; Git blob d22fe333b19489c473e076dd173ed7a67b1afbf0). Original article's O1: intact, outcross pollen added, visitors allowed; O2: emasculated, visitors allowed; O3: intact, visitors allowed, no added pollen. Same plants may contribute multiple treatments and periods; no independent-flower sampling variance assumed. These natural period contrasts do not manipulate mismatch. Article already identifies autonomous selfing as reproductive assurance and the importance of timing/resource limitation; this is not a newly discovered mechanism.

Source extraction read all 18 pinned GloPL summaries (3 sites × 2 years × 3 periods), reproduced separate O1/O2/O3 descriptive early/late rates from searchable Table 2 and checked arithmetic. Original published count/percentage conflict is retained rather than silently corrected.

| Site-year | Added-pollen early fruit set | Added-pollen late fruit set | Change, pp | Late−early ln supplementation ratio | Late−early intact-minus-emasculated change, pp |
|---|---:|---:|---:|---:|---:|
| BT 1999 | 75.2% | 5.0% | −70.2 | −0.410729 | +3.1855 |
| BT 2000 | 84.6% | 75.4% | −9.2 | +0.112913 | −10.9860 |
| EF 1999 | 69.9% | 6.5% | −63.4 | +0.002223 | +7.4352 |
| EF 2000 | 94.3% | 48.4% | −45.9 | −0.057216 | −5.3731 |
| TMC 1999 | 26.1% | 2.1% | −24.0 | −0.011561 | −5.0912 |
| TMC 2000 | 88.3% | 9.2% | −79.1 | HOLD | HOLD |

All six supplemented fruit-set point estimates decline later; five valid O1/O3 contrasts have two positive and three negative changes in log response ratio. Net intact-minus-emasculated point difference increases in two and decreases in three valid pairs. Do not infer significance, independent replication, or that late selfing always fails. Declining supplemented fruit set indicates residual reproductive constraints consistent with the source study, not proof that resource supply alone caused the decline. O2 vs O3 is an operational selfing contribution proxy, not a causal mediation decomposition. The source's earlier result of average 8% reproductive assurance is prior art.

## Material source QC — preserve both flags

1. TMC 2000 early O3, source ID 1003: searchable article table lists count 170:170 and percentage 92%; GloPL stores Natural mean .500 and N=340, matching the inconsistent count rather than the printed percentage. This may be a source-table or transcription issue; underlying typeset original not verified. Quarantine TMC 2000 from all O3-dependent effects, including the tempting large −1.096785 compiled seasonal contrast; O1 is independently consistent and retained for the supplemental-only comparison. Do not substitute .92 or guess a denominator.
2. Every one of 36 reported GloPL SD cells for this paper matches the binomial SE calculated from its rounded proportion and N to within 0.00005 (max absolute discrepancy 0.000049128; reported SD/SE ratio 0.99653–1.00228). This is a strong numeric fingerprint of SE-like rather than individual-level SD values; not proof of the original compiler's intention or independent flower sampling. Dividing these numbers by sqrt(N) as if they were SDs would be unsafe. Hold variance, no CI. Before using other papers' SD/N, audit each against original reporting and dependence (do not generalize this one source issue to all GloPL).

## Trifolium source progress

Geib & Galen (2012), https://doi.org/10.1890/11-1271.1, publisher abstract and 2009 conference abstract https://programarchives.z20.web.core.windows.net/2009/Paper17678.html confirm bumblebee addition, hand pollen controls, and within-season variation in alternative pollinators. Full institutional PDF timed out. Their published study already connects guild redundancy to pollinator density and demographic effects. Exact GloPL source-arm and sampling-unit correspondence remains unverified, so both Trifolium pairs remain HOLD. Public Figshare collection metadata retrieved in CI: 3304797 has Appendix A (pathway/visitation figures), B (projection matrices), C (ANOVA/ANCOVA tables; item DOI 10.6084/m9.figshare.3553698.v1). Collinsia collection 3297944 has only two listed appendices (pollination environment and floral visitors). Neither inventory establishes availability of individual raw data. Next: inspect Geib Appendix C and full source methods; no guessed SE or pooled arm outcome.

## Receipt

Run https://github.com/zuizui0223/payoff/actions/runs/45540032947, job 138956035394, artifact 14987928568; ZIP SHA256 93d56b01f439a4b0f27cbab9f7c400c55d0e050a57ec27fef56f0e019af90e36 from upload log. Source and arithmetic checks passed. Exact aggregate result and separate post-output QA: ../data/payoff_b_glopl_collinsia_wave8_result_20261125.json. ZIP not independently downloaded; no new raw measurements, no independent alternative implementation of original experiment, no primary theta. Source-frame counts remain screening rather than admitted meta-analysis cases.
