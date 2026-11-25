# Wave 9: GloPL full-source uncertainty audit and Trifolium duplicate quarantine

2026-11-25. Continuation of draft PR #426, no changes to frozen manuscripts or original primary endogenous-recourse × mismatch theta. Source author-input CSV, 2969 rows, Git blob d22fe333b19489c473e076dd173ed7a67b1afbf0 / SHA256 8c764ce03da86db0cb280e8f8f92cc0e62e2df6d85a2226e3246dc1afeb3f65f. The author-input CSV is not established identical to the deposited curated version. See prior freeze for fixed numerical fingerprint criteria.

## Completed diagnostic

| Endpoint | All arm cells | Eligible interior positive mean, integer N≥2 and positive SD field | Exclusive binomial SE match | Exclusive binomial SD match | Neither | Papers with at least one SE fingerprint |
|---|---:|---:|---:|---:|---:|---:|
| Fruit set (FS) | 8907 | 4003 | 2268 (56.66%) | 1 | 1734 | 418/688 tested |
| Seed/ovule (SO) | 8907 | 1139 | 10 (0.88%) | 0 | 1129 | 4/149 tested |

FS arm counts: natural 1124/2003 eligible, supplemented 599/1244, bagout 545/756. The tighter/nominal/relaxed absolute tolerances 0.00005/0.0002/0.0005 with constant relative tolerance 2% give FS SE matches 2242/2268/2301, SO 2/10/25. All 36 previously identified Collinsia FS cells match. Within the seasonal candidate rows FS has 50/66 eligible cells matching, SO 0/22. All tested FS cells match the SE fingerprint in 383 of 418 flagged publication groups, mixed in 35. No exact source duplication claim follows from the fingerprint alone.

**Interpretation:** widespread numerical SE-like convention in the author's input fruit-set uncertainty fields, not proof of 2268 erroneous estimates. Bennett et al. (2018), https://doi.org/10.1038/sdata.2018.249, explicitly allows reconstructing variance from mean and sample size for binomial fruit set. A true Bernoulli individual SD and an estimated mean's SE are different, but aggregate proportions, cluster means and uncertainty at different units need separate treatment. SO is not necessarily Bernoulli at the reported unit; matching prevalence cannot validate nonmatches. No global correction, downweighting, or new inverse-variance fit undertaken. Source study-level uncertainty audit remains required before weighted synthesis; earlier Cerastium intervals stay conditional, not established validated sampling intervals.

## Trifolium source anomaly

Geib & Galen (2012), https://doi.org/10.1890/11-1271.1. Searchable full-text rendering https://www.academia.edu/176520473/Tracing_impacts_of_partner_abundance_in_facultative_pollination_mutualisms_from_individuals_to_populations confirms each species' plant N for open (15 early,5 late), hand (12 early,4 late) and caged (12 early,4 late). GloPL SPFL cells match open/hand N for both taxa, but **all twelve summary fields** (four means, four reported SDs, four Ns) are identical across distinct T. dasyphyllum and T. parryi rows 2192–2195. The compiled early natural/hand means are .311/.686 and late .989/.653 for both; the computed seasonal ln ratio difference -1.206202 is therefore a duplicated candidate, not two species estimates. Both are quarantined until original species-specific means and treatment mapping can be authenticated. No assumption about which row is correct or that the source must be an error.

Public Figshare article metadata confirms all three original appendix HTML files are CC0 with MD5 and file size. First access script failed before requesting bytes because the expected downloadUrl metadata field was absent. The separate correction uses the documented Figshare public endpoint and pinned identifiers/MD5; no protected URL bypass. Any appendix figures/tables must be evaluated for species, arm, phase, and sampling grain, not simply significance. Prior findings about functional redundancy and plant performance vs population growth remain published background.

## Reproducibility

Completed audit run https://github.com/zuizui0223/payoff/actions/runs/45540456520, job 138957413807, artifact 14989250810, ZIP SHA256 f69e234f5bbf2a6194e4a905b57022c3f7ec48bea53894b99a60a7042d8721c8 from upload log; ZIP not independently downloaded. Synthetic fingerprint checks passed. Aggregate compact job log preserved at data/payoff_b_glopl_variance_trifolium_wave9_result_20261125.json; per-cell flag list remains in artifact. No primary eligible theta, no pooled estimates, no merge.