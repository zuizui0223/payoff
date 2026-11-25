# Wave 12 — public original-data acquisition and priority experiment design diagnosis

2026-11-25. Draft PR #426. No previous result or primary estimand changed.

## Completed source work

Original data from three studies authenticated via Figshare file MD5 and SHA256: Murillo-Rincon et al. JAE 2017 (10.1111/1365-2656.12605, 10.6084/m9.figshare.3984482.v1, 828 rows in 69 containers); their Oikos 2017 immune study (10.1111/oik.04014, 10.6084/m9.figshare.4239314.v1, 426 rows, 21 family IDs); Weir 2024 (10.1007/s00442-024-05629-5, 10.6084/m9.figshare.27679935.v1, 3600 individuals and nine host taxa; two sheets not two samples). All CC BY 4.0. Exact original archive metadata/structure in data/payoff_b_compensation_priority_source_gate_result_20261125.json. No raw source rows redistributed.

Original JAE Table 1 all 21 tests and descriptive source contrasts in data/payoff_b_compensation_priority_published_anchor_wave12_20261125.json. Phenology x priority F(2,69.86)=58.82 for larval period; F(2,74.17)=4.10, p=.020 for metamorphic mass; F(2,77.65)=4.19, p=.0186 for growth. Original study already demonstrates competition can suppress catch-up; these are dependent published statistics, not new independent effect sizes. Cold delay is not separately measured resource-relative mismatch; timing/growth/mass do not establish lifetime fitness.

## Source diagnosis

First prospective secondary fit stopped on UNEXPECTED_TANK_COMPOSITION, no estimates. Second diagnostic stopped on UNRESOLVED_TANK_CODE because the source labels use hyphen-separated group/food/replicate (e.g. NN-H-1). Third, label-only diagnostic recovered all 69 codes and both independent recorded phenotype fields; exact data/payoff_b_priority_tank_design_label_receipt_20261125.json. 64 containers satisfy the intended 12 homogeneous or 6+6 mixed design exactly in both fields; one ND-H-1 has one missing string label but numeric PhenN=1 and a 6+6 numeric composition; four other mixed tanks have matching text and numeric 5 normal + 7 delayed. All assignments and slot uniqueness verified in the diagnostic. These anomalies do not establish that the authors misallocated larvae or that the metadata is wrong. Original files unchanged. Strict design support before endpoint checking:

| Group | High food | Low food |
|---|---:|---:|
| NN | 7/7 | 7/7 |
| DD | 7/7 | 7/7 |
| EE | 7/7 | 7/7 |
| ND | 5/7 | 5/6 |
| NE | 7/7 | 5/7 |

## Next fixed design-only amendment before new outcomes

Preserve initial HOLD. Main contrast restricted to exact 64 tanks, no individual relabeling. Sensitivity 1 additionally admits ND-H-1 using the independently recorded numeric phenotype field for the sole missing string; require its dictionary mapping and matching assignment. Sensitivity 2 includes the other four 5:7 mixed tanks using their observed agreed phenotype labels as recorded (different composition, not a randomized 6:6 contrast). Require exact original hashes, source codes and known issue list; stop on unexpected deviations. Use original endpoint and 10,000 whole-container bootstrap, retain shared controls and within-container cohort covariance. Require at least four usable tanks per group after endpoint completeness, report all exclusions and block sensitivity. No imputed counts, no survival inference, no actual individual hatch dates or lifetime fitness. Report all sensitivities regardless of sign; strict subset is post-source-diagnostic, not an ITT analysis. No primary theta promotion. Secondary fit not yet run under this amendment.

Separate independent studies of immune challenge, thermal/resource constraints and host alternatives are the next source-authenticated lanes. Hegyi et al. (2013) is natural timing x experimentally induced food shortage; separate observational moderation. The four blocked GloPL original papers remain on hold; prior 28-pair disposition unchanged. No pooling, manuscript replacement or merge.
