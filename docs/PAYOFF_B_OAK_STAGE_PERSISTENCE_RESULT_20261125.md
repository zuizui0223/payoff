# PAYOFF-B wave 4: actual oak original-data stage contrast and source resolution

25 November 2026. Continuation of draft PR #426. This adds one study lineage, Bogdziewicz et al. (2020), to the previous 28-source screen (29 source records, not 29 independent eligible effect sizes). The [source and pre-fit contract](PAYOFF_B_OAK_STAGE_PERSISTENCE_FREEZE_20261125.md) preceded the new contrast. [Exact executed aggregate receipt](../data/payoff_b_oak_stage_persistence_result_20261125.json) records all results, including the negative outcome.

## 1. Source admission and result

Original public CC0 dataset DOI 10.5061/dryad.sn02v6x2b, Zenodo record 5306693, paper DOI 10.1111/ele.13609. Original semicolon CSV, 31,612 bytes, provider MD5 9bb924a2d0739e78e6823f1df6878e6a and actual SHA256 3075bfa3f41a0f702d23bab9ce444318160ce37fea91cf7eea602dc098e5bd21. Actual source hash verified again before the fit in [run 45530248666](https://github.com/zuizui0223/payoff/actions/runs/45530248666).

960 shoot rows, 480 per source treatment. Control: 61 incomplete and 2 zero-flower records excluded; pollen addition: 81 incomplete and 1 zero-flower record excluded. Positive-flower complete records 417 and 398, respectively, before restricting to complete paired tree-years. Of 151 observed tree-years, 137 contain both arms, representing 75 individual trees and 67/70 paired tree-years in 2018/2019. No final acorn count exceeds the June count on retained complete shoots. No assumed missing=zero or shoot-level independent bootstrap.

Equal paired-tree-year average of original female-flower-denominator fruit-set rates; 10,000 whole-tree bootstrap resamples preserving both years and arms. Haphazard assignment within tree (not independently randomized trees), complete-case target, one biological study.

| Stage | Control | Pollen addition | Difference (percentage points) | Tree-bootstrap 95% interval of difference |
|---|---:|---:|---:|---:|
| June | 45.516% | 47.582% | +2.066 | [-5.062, +9.109] |
| September | 30.121% | 32.845% | +2.724 | [-3.760, +9.220] |
| Final minus early difference | | | +0.659 | [-2.393, +3.620] |

Log response ratio: June +0.04438 [-0.11077,+0.19613]; September +0.08658 [-0.12035,+0.29410]; final minus early +0.04220 [-0.05274,+0.13671]. Both scales fail to establish attenuation of the supplemented advantage. The early advantage itself is not established; equivalence is not inferred from a nonsignificant contrast.

2018 point estimates: early -3.391 pp, final -0.123 pp; 2019 early +7.289 pp, final +5.450 pp. These are descriptive year strata, not independent studies or a formal year interaction. The absolute and relative stage effects are different estimands. A decline in fruit set from June to September in both arms is not proof that compensation is costly.

**Conclusion:** the specific prediction that supplementation's early benefit decays over reproductive stages is **NOT SUPPORTED** in this complete-case secondary reanalysis. This does not invalidate the original study's published pollen addition x flowering synchrony mechanism: the public CSV has no flowering synchrony covariate. The supplementary treatment changes service supply, not the organism's intrinsic capacity or observed information. Neither realized seasonal mismatch nor causal cost of compensation nor drought-specific effect is identified. Do not promote these paired effects as the frozen primary theta, or as two independent meta-analytic entries.

## 2. Vázquez file manifest problem solved

The prior source run 45528449801 completed and its five synthetic source tests passed, but original Schenk (two files), Nanke and Kudo/Cooper downloads returned HTTP 401. A successful workflow means the access status was recorded, not that protected source bytes were obtained. The Vázquez manifest mismatch was a separate problem: Dryad API pagination. Exact published version 420579 was recovered; following the official same-host next link over two pages yielded 25 metadata entries, including all six required raw input files. The observed manifest count includes all provider entries; the public landing page count need not match if metadata files are present.

The result JSON preserves exact official file identifiers, sizes, and provider SHA-256 values, including trampas.csv file ID 4565811, 70,242 bytes, SHA256 ed2d158fc1930924c06ff72883d296e4a8690984bd8d7daf8a386880441f9c59. Original source-data bytes for Vázquez remain unopened. The official landing page and metadata are public; access is not guaranteed. Do not infer authorization or biological outcomes from a digest listing.

## 3. Next scientific gate

Use a source-authorized complete Vázquez archive (https://doi.org/10.5061/dryad.37pvmcvmp) or the exact two Schenk workbooks (https://doi.org/10.5061/dryad.rm317). A user-supplied original can be hash checked against the provider manifests. If using Vázquez, independently authenticate plant, nest, emergence and first-three-year pollen source and source code; freeze the distinct historic-diet portfolio held-out prediction before opening any new fit. That observational analysis will remain secondary, not primary theta. Continue the independently identified buffer/perturbation experimental search, retaining all negative evidence. Primary eligible factorial contrasts: **0**, unchanged; no pooled effect, no manuscript replacement, no merge.

## 4. Reproducibility

Run 45530248666 completed the synthetic assertions and the original-data calculation. Job 138923474484 emitted the exact aggregate JSON saved here. Artifact 14983749525; ZIP SHA256 f6d11b08ea22994515408834b3a3b00c0ffd5741f69d33977472ba70e9fd2db1 reported by upload step (ZIP not independently downloaded). All outputs aggregate, no original row, tag or tree ID exported. The original source-only run 45530063949 authenticated the schema before the pre-fit contract. This was not independently rerun by a second implementation. All prior receipt and manuscript files remain unchanged.
