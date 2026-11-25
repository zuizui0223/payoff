# Wave 13 — executed source-amended priority competition reanalysis

2026-11-25. Draft PR #426. Secondary developmental-time and body-mass contrasts in one experiment; not a primary endogenous-recourse × actual partner-mismatch fitness effect. Original source article Murillo-Rincón et al. (2017), DOI 10.1111/1365-2656.12605; CC BY 4.0 data DOI 10.6084/m9.figshare.3984482.v1. Provider MD5 dafa108fd1189267ef9fcda5e3353f5f and pinned SHA256 19535539c5585ecd2ed2de6131058267920007b52625468081c8f1a267c5c08a verified on reanalysis.

## Source and methods

Preserved initial composition HOLD and design-only diagnosis; amended fit exactly follows the previously documented 64/65/69-container policies. Strict main: 64 source-conforming tanks, 768 allocated slots, 662 complete observed duration and mass records; 106 incomplete records. Numeric sensitivity: 65 tanks, 673 complete rows; one missing string phenotype read from separately recorded numeric field, validated against source dictionary. Observed-composition sensitivity: 69 tanks, 715 complete of 828 slots, retains four 5:7 mixtures as recorded. No phenotype relabeling beyond resolving one missing text from numeric source code; no missing outcome imputed. All 10 treatment cells pass ≥4 tanks with paired endpoint support. Complete-case target, not ITT; unequal missingness may influence effects and missing duration/mass cannot establish mortality.

Equal-weight tank/cohort means; I = (delayed−normal duration in mixed tanks) − (delayed−normal duration in homogeneous tanks). LarvalPeriod is recorded duration from the start of the larval experiment to metamorphosis, in days, not an exact calendar date or measured individual hatch delay. Original nominal 6/12-day cold treatment differs from observed timing. 10,000 whole-tank stratified bootstrap draws within food/composition, paired cohorts within mixed tanks, shared normal homogeneous controls retained across delay contrasts. Joint covariance of four time and four mass effects saved. Intervals are percentile estimates conditional on observed tanks, not simultaneous or exact block-randomized inference.

## Main duration contrast

| Food/delay | Homogeneous delayed−normal (days) | Mixed delayed−normal (days) | I days | Conditional bootstrap 95% interval |
|---|---:|---:|---:|---|
| High/6 | -1.925325 | 3.413333 | 5.338658 | [2.050561,8.647224] |
| High/12 | -10.689394 | 2.295238 | 12.984632 | [10.075438,15.820368] |
| Low/6 | -4.852067 | 11.506667 | 16.358733 | [11.046131,20.963103] |
| Low/12 | -10.246016 | 10.216667 | 20.462683 | [17.209860,23.752656] |

All four point differences are negative in homogeneous groups and positive within mixed groups. All 12 duration interaction percentile intervals across three modes are above zero; all equal-block and leave-one-common-block-out duration point estimates positive. All-tank mode I=5.468182/12.984632/16.440955/18.347717 days. Low-food interaction larger in point estimates; no new formal food-by-delay inference claimed.

### Relative gap combines two cohort responses

In strict64, delayed-cohort mixed minus homogeneous duration increases by 1.448615/8.575541/9.952789/9.873405 days; non-delayed-cohort mixed minus homogeneous decreases by 3.890043/4.409091/6.405944/10.589277 days. Their difference gives I. Do not describe I as the additional number of days required by the delayed individual alone. This is a relative cohort asymmetry, consistent with the original paper's already published priority-effect mechanism. Resource limitation modifies the point pattern but specific competitive physiology is not identified.

## Mass at metamorphosis

Strict64 log mass interaction (mixed delayed/normal ratio relative to homogeneous ratio): +.056538 [-.079193,.191701], +.225216 [.098248,.359358], -.115239 [-.267962,.041259], +.095798 [-.078356,.287331], in same order. No universal negative mass interaction; one high-food/12-day contrast positive on this relative scale. These are conditional endpoint measures among complete observations, not survival or fitness. A time interaction does not establish that correction trades off against body mass, and no causal mediation is fitted.

## Reproduction

CI run https://github.com/zuizui0223/payoff/actions/runs/45543842879, job 138968560966, artifact 14991015294, upload ZIP SHA256 e4e3e86a71eac349a8e711422aad4eb2dc975417aab47a9ae528e382701ef904. Synthetic checks passed; original hash and design consistency verified; all three calculations completed. Exact result JSON at data/payoff_b_priority_tank_amended_fit_result_20261125.json; independently recomputed two-cohort decomposition from returned means, not a separate fit implementation. ZIP not independently downloaded. One study lineage, no weighted meta-analysis; primary count unchanged 0. No frozen manuscript replacement or merge.

## Next independent data lane

Murillo-Rincón et al. (2017 Oikos 126:565–571; DOI 10.1111/oik.04014) separately manipulates immune challenge and 12-day cold delay. Original supplement https://www.oikosjournal.org/sites/oikosjournal.org/files/appendix/oik-04014.pdf provides model-adjusted duration and mass contrasts for PHA, APBS and control. These are already published results, not a discovery. The two papers' cohort independence and parent structure must be verified before any independent-study count or family-cluster fit. No combined inference across endpoints or papers.
