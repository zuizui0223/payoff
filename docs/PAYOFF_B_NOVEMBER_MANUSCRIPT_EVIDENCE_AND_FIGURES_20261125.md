# PAYOFF-B November candidate: claim disposition, figure plan and admission gates

25 November 2026. Companion to the [new working manuscript](../manuscript/PAYOFF_B_INFORMATION_ACTIONABILITY_NOVEMBER_CANDIDATE_20261125.md). This document records editorial decisions; it is not a new analysis or an amendment to preregistration. Base: the October S4-corrected manuscript, PR #335, head c3b7ba1e63ad5fe2df5d27b1a18c2fd85eb6c5a0. No frozen manuscript is replaced. No draft source branch is merged by this integration.

## Single scientific story

**A cue's potential predictability, availability before commitment and remaining opportunities to respond are separate. Partner asymmetry in these quantities can generate mismatch under shared environmental forcing.**

The paper is theory-led. The natural examples are not linked individual-level estimates of the proposed causal mechanism. The environmental chronology diagnostic and within-animal robustness are the two strongest November contributions to the manuscript; the migration-distance result is provisional pending provenance review. The anti-phase theorem paper remains separate.

## Main evidence and figures: replace rather than add

| Figure | Panels / data and estimand | Required counterevidence or qualification | Source |
|---|---|---|---|
| 1: Theory, finite actionability window | Normalized binary cue, exponential learning and opportunity loss; gross value, retained value, fixed-cost crossings; conditional general optimum and special-case label. Show two independently specified opportunity-decay rates. | Illustrative curves, not empirical estimates. No claim that free optional information harms an individual under fixed actions. | [#335](https://github.com/zuizui0223/payoff/pull/335); theory/ACTIONABILITY_BALANCE_THEOREM.md; manuscript V2 |
| 2: Theory, partners | Pairwise phase-error recursion, shared input, different lambda; distinguish inherited and generated mismatch. Optional third panel of the existing synthetic coordination gate (22/24 barriers, 21/24 persistence rescue). | lambda is conditional mean retention under stated assumptions, not active correction gain. Synthetic cells are not natural cases. Do not equate relative timing with fitness. | [#335](https://github.com/zuizui0223/payoff/pull/335); docs/PAYOFF_B_2D_CONNECTIVITY_RESULTS_20260920.md |
| 3: Environmental evidence | A: detrended r early 0.79859, late 0.87916, delta +0.08057 [0.02410,0.13913]; B: held-out oracle SSE savings 74.54%, 59.94%; C: gated savings separated into before versus after target onset (early 0.0502 and 0.1103 pp; late 0.0896 and 21.9909 pp). 104 geographical links/88 source-cell blocks, 2002–2017. | Same source across A–C; no independent replication. Oracle change interval crosses zero. Timing classifications post-scoring and decision/report delays hypothetical. Show negative censored-status sensitivity in supplement. | [#396](https://github.com/zuizui0223/payoff/pull/396), [#397](https://github.com/zuizui0223/payoff/pull/397), [#398](https://github.com/zuizui0223/payoff/pull/398), [#399](https://github.com/zuizui0223/payoff/pull/399) |
| 4: Animal evidence | A: within-deer FE slope -0.689113 [-0.815051,-0.572581] days/day, 38 deer and 100 animal-years; eight year-omission estimates as range (-0.802203 to -0.514595) unless source-level values obtained; B: descriptive incoming/final phase SD 26.406/13.173 days in published full-route sample (152 animal-years/72 deer), distinct sample. | Within-animal fit is exploratory; calendar versus phase VIF 16.54 blocked the joint coefficient, identifying variation almost entirely later cohort. Full-route convergence not a direct causal estimate. No individual points invented. | [#413](https://github.com/zuizui0223/payoff/pull/413), [#414](https://github.com/zuizui0223/payoff/pull/414), [#401](https://github.com/zuizui0223/payoff/pull/401) |
| 5: Interaction implications | Conceptual phase-control predictions with local/mobile scenarios; published bird–caterpillar slopes 0.510/0.515/0.348 and resident–migrant interval change 0.94 d/decade as attributed anchors. Include independent measurements necessary for a causal test. | Do not assign measured q or r to taxa; no natural pairwise game or fitness claim. No error bars for values unless source intervals recovered. | Burgess et al. 2018 DOI 10.1038/s41559-018-0543-1; Samplonius et al. 2018 DOI 10.1111/gcb.14160; #401 |

The optional fifth figure may instead become a conceptual panel in Fig. 2; retain a four-figure main text if space is constrained. Radar chronology and negative held-out prediction appear together in supplementary Table S1, not as a sixth headline. Source summary estimates must be labeled as summaries; use original data marks only from an authenticated, permission-reviewed source artifact. The five figure concepts above have not been rendered.

## Evidence disposition (keep successes and failures paired)

| Module | Disposition | Reason |
|---|---|---|
| MODIS satellite-only #396–399 | MAIN, exploratory | distinct covariance, forecast skill, pretarget observability; not bird cue use |
| Radar #415–417 | MAIN brief paragraph + S1 | chronology often precedes passage, yet no reliable independent green-up increment |
| Mule deer #413–414 | MAIN, exploratory | individual-level association, not phase-specific causal feedback; paired support failure |
| Within-study E6 #405 | SUPPLEMENT PROVISIONAL | 444 effects/13 studies/269 species, +0.525253 [0.224283,0.826223]; known eBird-derived and unverified sources removed, complete policy audit still needed; prior-art gradient |
| Original V8 species-mask result and pooled E6 | QUARANTINE | original eBird-linked inputs conflict with project policy; retain provenance, not active manuscript data |
| Published interaction asymmetries E6b | MAIN, cited anchors | evidence of unequal timing responses, not PAYOFF mechanism or new discovery |
| Wigeon E3, E4/E5 recovery, Scottish prey specificity #392 | NEGATIVE / LIMITS | direct interaction/actuator/recovery or specificity not supported/estimable |
| Stork #421–423 | SOURCE APPENDIX ONLY | 27,023,367 GPS rows, 519 common days, strict 1/11 and sensitivity 2/16 coarse triple candidates; no verified sensory exposure, independent bird count, or q/r effect |
| Barnacle goose V7 #424 | HOLD | authentic archive metadata and small source references, but original annual onset series and region assignments unavailable; no primary q x U outcome |
| Bumblebee #412 | PROSPECTIVE ONLY | exact synthetic witness and power design, no biological observations |
| Two-patch anti-phase optimum | OTHER PAPER | independent exact Theoretical Ecology paper |

## Discriminating tests, not more positive-result mining

1. Natural test: recover source-authenticated 16-region × 30-year (1982–2011) spring-onset series and region-to-GPS assignments for frozen V7. Require original route transition/visit support, at least 10 independent-q transitions, at least 3 positions, at least 30 visits, at least 2 flyways and the original correlation admission rule. Preserve the frozen q x geometry-U estimand; past-only q is a separately documented no-lookahead support/sensitivity, not an unauthorized redefinition. Even a pass is not a fitness-scale q x r identification.
2. Direct mechanism: retain the prospective #412 independent-colony 2×2 reliability/opportunity experiment; calibrate actual cue discrimination and feasible response separately; assess colony-level ITT loss interaction, not individual bee trial pseudo-replication. Do not treat the hypothetical power run as an experiment.
3. If no source or experimental data become available, keep the manuscript theory-led and report direct natural identification as absent. Do not add another correlational taxon purely to increase sample count.

## Editorial and reproducibility release gates

- Current: working English main-text candidate drafted; section structure, selected citations and claim-to-source links exist. Exact October manuscript is unchanged.
- Before main-text promotion: inspect and approve all source receipts, verify full source policy and permissions (including radar), replay included analyses from original authenticated data where allowed, and obtain exact published intervals and full bibliography.
- Before reviewer package: render actual figures from permitted data or explicitly labeled summaries; verify each number, plot caption and units against receipts; run relevant source/model/packaging tests and every-page PDF inspection.
- Before submission: reconcile with frozen publication plan, author approval, complete declarations, anonymous reproducibility archive and current journal requirements. No submission or merge is implied.

## Japanese handoff

本稿は「予測可能性が高いほど適応しやすい」という単純な説明を、情報取得のタイミングと修正可能性を区別することで精密化する。衛星データでは潜在的な予測関係と実際にターゲット発生前に利用できる情報が異なる。シカでは個体内の補償的な行動パターンが残るが、暦日と季節位相の効果は分離できない。数学は、同じ環境変化でも二種の制御・修正能力が違うだけで非同期化が生じ得ることを示す。自然界で情報×修正能力の機構を直接確認したわけではない。今はこの一本の理論主導ストーリーを優先し、凍結済み原稿と否定結果を保護する。
