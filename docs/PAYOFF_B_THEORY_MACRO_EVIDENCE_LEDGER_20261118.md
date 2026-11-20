# PAYOFF-B mathematics × macroecology evidence audit — 2026-11-18

**Role:** source-controlled synthesis / next-test routing, **not** a new biological fit, submission revision, proof of causal information use, or approval to merge draft empirical branches.

## Main claim and its limits

> Seasonal tracking is constrained separately by (i) predictive information about future environmental states, (ii) the timing at which that information can be observed, (iii) downstream correction/recourse, and (iv) coordination with interacting partners.

The mathematical layers are conditional results. Their natural anchors are *not* one causal chain estimated on one linked dataset. The strongest natural bridge is **differential phenological response among interacting partners**, not a measured natural information-use threshold or game equilibrium.

**Important reversal of the original environmental-loss intuition:** the latest eBird-free eastern North American forest MODIS diagnostic shows an **increase**, not a decline, in geographical spring correlation in this sample (draft PR #396). PAYOFF-B must not call generic climate-driven loss of cue connectivity established. A related but different question remains alive: even a strongly predictive cue may become **observable too late for the focal action** (draft PRs #397–399). The satellite calculations do not observe animal decisions.

## 1. Exact mathematical and synthetic results (not field effects)

| Formal result | Exact scope | Natural evidence bridge / missing link |
|---|---|---|
| Anti-phase two-patch seasonal growth premium has a unique positive optimum in migration for any nonzero contrast; weak-contrast optimum $m\tau\to1.6061153$ | symmetric 2-patch, 2-season model only | no corresponding universal macro-estimate; keep Theoretical Ecology paper separate |
| Time adjustment buffers route costs, but has a finite range; synthetic zigzag route growth penalty −0.04189 → −0.006996 (83% decrease) as allowed phenology increases | 2-D finite-horizon synthetic model, not measured ecological velocity | route and phenology can both be adjustable, but natural quantitative costs not fitted |
| A coordinated shift can outperform a locally selected endpoint while either partner's unilateral move is disadvantageous; 22/24 positive-interaction design cells show barriers | synthetic 2-D coevolution, not 22/24 wild cases | Burgess/Samplonius show response asymmetry and changed relative timing, **not** local fitness barriers |
| Frozen information-use threshold follows cue accuracy and the **effective** waiting cost $D_{eff}$, not raw departure delay | the declared fixed-cost binary cue decision game; dual-use cues require the distinct conditional theorem | no observed actor-level $D_{eff}$ or $q_{wait}$ |
| Under exponential learning and loss of recourse, $t^*=\ln(1+\alpha/\beta)/\alpha$ maximizes usable information | declared $q(t),r(t)$ and zero extra waiting cost, not a universal timing optimum | experiment and sources motivate time-varying cue availability; no fitted natural $\alpha,\beta$ |
| $e_{t+1}=\phi_t(e_t-u_t)+w_t$, with segment $\lambda=\phi(1-hK)$ only under specified linear feedback assumptions | active gain, passive carry-over, information and route geometry are not identified by one $\lambda$ | mule deer, barnacle goose, wigeon show estimator-scale retention; actuators differ |
| Even at perfect environmental cue quality, high-payoff coordinated information use can be individually inaccessible | declared perfect-information coordination game | no observed wild information-acquisition hysteresis; registered E4/E5 recovery gates failed |

Canonical sources: [information theorem map](../docs/PAYOFF_B_INFORMATION_DEADLINE_THEOREM_MAP_20260930.md), [actionability theorem](../theory/ACTIONABILITY_BALANCE_THEOREM.md), [synthetic 2-D receipt](../docs/PAYOFF_B_2D_CONNECTIVITY_RESULTS_20260920.md), [perfect-information trap](../theory/PERFECT_INFORMATION_COORDINATION_TRAP.md), [publication status](../docs/PUBLICATION_STATUS.md).

## 2. Natural affirmative evidence on main — ordered by ecological proximity to the prediction

| Evidence / sample | Positive result | Licensed level |
|---|---|---|
| **E1** migratory birds, 3,311 rows / 37 species | pooled predictive-connectivity coefficient **−0.0462**, 95% CI [−0.0870,−0.0054], p=0.0265 | directional association only: species/route/cell-year cluster intervals include zero |
| **E6** Usui source reconstruction, 944 temperature-response rows / 28 studies / 279 species | long-minus-short migrant response **+0.421 d/°C**, 95% CI [+0.121,+0.722], p=0.0077; all 28 leave-one-study-out fits positive | robust existing migration-distance gradient; endogenous/photoperiodic control also explains it |
| **E6** Freimuth published local benchmark, 1,763 species | mean days/°C: plants −5.152, bees −2.024, flies −3.879, Lepidoptera −1.848, beetles −1.706 | response heterogeneity among local guilds, *not* linked pair causal contrast |
| **E6b** Burgess et al. bird–caterpillar pairs | temporal tracking slopes **0.510**, **0.515**, **0.348** (blue tit, great tit, pied flycatcher); published 95% credible intervals exclude one | interacting consumer–resource timing responds asymmetrically |
| **E6b** Samplonius et al. 10 European nest-box schemes | resident tit vs migrant flycatcher laying-date interval widened **0.94 d/decade** | interacting groups can diverge even under shared climate forcing |
| **route response** mule deer, 152 animal-years / 72 individuals | incoming phase SD 26.406 d vs final SD 13.173 d; whole-route descriptive $\lambda\approx0.10734$ | published resynchronization with reanalysis; not latent belief or fitness identification |
| **route response** barnacle goose (3 route rows) and wigeon (224 transitions) | barnacle goose signed $\lambda$ −0.1063, +0.1307, +0.4941; wigeon POWER 0.7498 and independent ERA5 0.8113 | a portable **estimator-scale response coordinate**, not one universal latent $\lambda$ or actuator |
 
All published bridge findings are attributed as published prior art; their reproduction is not promoted to new discovery. See [main claim stack](../docs/PAYOFF_B_CANONICAL_CLAIM_STACK_20260927.md), [pairwise bridge](../docs/PAYOFF_B_PAIRWISE_TRACKING_BRIDGE_20260929.md), [E6 result](../docs/PAYOFF_B_CROSS_SYSTEM_INFORMATION_RESULT_20260928.md) and [wigeon revalidation](../docs/PAYOFF_B_WIGEON_PHASE_RETENTION_REVALIDATED_20260922.md).

## 3. 2026-11-17 newer environmental-only diagnostics: **draft, post-open exploratory**

These PRs are *not* present as validated new biological claims on main. Each must retain its prior result and negative gate on eventual review.

| Pending PR | What actually passed | Why this does not prove adaptive information use |
|---|---|---|
| [#396](https://github.com/zuizui0223/payoff/pull/396) | 106 original forest satellite cells, 104 geographic pairs; mean detrended source–target $r$: **0.79859 → 0.87916** (2002–09 vs 2010–17), Δr=**+0.08057**, source-cell block CI [+0.02410,+0.13913] | environmental covariance **increased**, not decreased; ecological scale restricted to these forests |
| [#397](https://github.com/zuizui0223/payoff/pull/397) | retrospective next-year forecast with completed contemporaneous southern green-up reduces target-only baseline squared error **74.54%** early and **59.94%** late | a future source-event completion time need not be observable *before* the required action; late−early gain change CI crosses zero |
| [#398](https://github.com/zuizui0223/payoff/pull/398) | under hypothetical 7-day decision lead plus 7-day report delay, gated error saving **0.1606%** early and **22.0806%** late | post-scoring validity audit: **21.9909 percentage points of the 22.0806 late gain (~99.59%)** came from decisions retrospectively classified as **after the actual target onset**. Only **0.0896 pp** came from truly pretarget rows. The apparently large 22% figure is **not** a predecision bird result |
| [#399](https://github.com/zuizui0223/payoff/pull/399) | hypothetical censored status (“source spring has not yet occurred”) has early skill +0.07479, 95% CI [+0.00220,+0.14694] | late skill −0.03536; late−early Δ −0.11014, CI [−0.25963,+0.02295] crosses zero; both statuses depend on an assumed monitoring system, not observed birds |

The MODIS analyses share source years and environmental sample, and were developed after prior signs were seen. They cannot be counted as independent macro-replications. Earlier eBird-conditioned V8 +0.369 is **quarantined** from ecological claims; do not add it to these source-only estimates.

The resulting **methodological conclusion** is narrower and stronger than “connectivity is being lost”: *cross-site correlation, out-of-year potential forecast skill, and usable information by the decision deadline are three different estimands.*

## 4. Negative results, absence of proof and source gates to preserve

- **E3** wigeon registered predictive-connectivity × incoming-phase: β=+0.0202, CI [−0.1058,+0.1461], p=0.756 — **NOT SUPPORTED**.
- Wigeon stopover association appears in the preregistered POWER reconstruction, but ERA5 replication p=0.3104 — not a robust universal actuator.
- **E4/E5** Hoge Veluwe cue-driver/cue-resource “decline then recovery” gate failed; downstream historical network hysteresis was **NOT RUN**.
- The original Scottish caterpillar/blue-tit follow-up [#389–392](https://github.com/zuizui0223/payoff/pull/392) does not provide an unambiguous heldout test that hatch-window food mass uniquely predicts reproduction beyond seasonal food controls. Do not treat an exploratory mass association as confirmed timing/fitness mediation.
- **V7 [#395](https://github.com/zuizui0223/payoff/pull/395) / [#400](https://github.com/zuizui0223/payoff/pull/400)** recovered 52,443 original goose GPS fixes from 44 source-identified birds and **23 published historical interregional q coefficients**; 13 correspond to adjacent transitions and 11 avoid unresolved region alias mappings. This is a **data-source achievement, not a fitted q×urgency effect**. The original annual region-year spring onset and authoritative GPS-region polygons/crosswalk remain absent. Source Table S1 region means must never be substituted for annual $S_{j,y}$.

## 5. Next analysis, chosen without outcome-dependent retuning

**Primary biological test remains the frozen V7 q × route-urgency interaction.** It is more decisive for the PAYOFF-B thesis than adding more positive environmental correlations.

The existing [V7 contract](../docs/PAYOFF_B_V7_PREDICTABILITY_URGENCY_CONTRACT_20261005.md) defines:

- response $Y_{ij}=|A_{ij}-S_{j,y}|$ using source-faithful arrival and region-year spring onset;
- independent *historical environmental* $q_j$ for the preceding route transition;
- geometry-only $U_j=1-d_{j,breed}/d_{winter,breed}$, **not** stopover duration/speed;
- focal interaction $\beta_{qU}$, with both β>0 (urgency weakens cue benefit) and β<0 (final-step information importance) predeclared interpretations.

**Admission before fitting:** at least 10 distinct independent-q transitions, at least 3 route positions, at least 30 genuine individual stopover visits, at least 2 flyways, and $|corr(q,U)|<0.90$ across transitions. Currently only the *aggregate q-candidate count* is demonstrated; the other gates are **NOT YET EVALUABLE**. Do not lower thresholds or infer visits from GPS fixes.

**Source-first executable sequence** (no goose outcome opened):

1. Recover a source-verifiable **1982–2011 region×year spring-onset matrix** or original equivalent annual series, not a plotted curve approximation or regional means.
2. Recover authoritative 16-region stopover boundaries and original study region-name crosswalk, resolving NLDK and NSE without guesses.
3. Reconstruct animal-year stops and geometry-only urgency *independently of timing-error outcome*, run the frozen admission criteria.
4. **Only if the gate passes:** execute the original preregistered q×U model, full frozen sensitivities and held-out uncertainty. Otherwise report **NOT_ESTIMABLE**, not “the ecological mechanism failed.”

**Secondary macro replication**, separate from V7: on a genuinely independent environmental cohort/new years if source files are obtained, preregister a geography-only source→target green-up pairing and compare (i) historical signed correlation, (ii) rolled-forward oracle forecast skill, (iii) **actually observable before a predeclared decision** binary/full cue. Report all three irrespective of signs, and reserve claims about migratory behavior for source-verified animal decision dates. This second lane must not reuse already-open MODIS years as an independent validation.

## Claim ceilings and handoff

- **Can say now:** multiple natural systems show heterogeneous seasonal responses and incomplete phase tracking; model theory gives concrete conditional pathways by which information, opportunity and interaction coupling could cause mismatch.
- **Can say as a draft environmental diagnostic:** geographical spring coherence strengthened here, but much apparent satellite forecast gain was not available before the target in the defined hypothetical timing scenario.
- **Cannot yet say:** climate change has generally destroyed teleconnections, the observed bird/plant gradients are caused by Bayesian information distances, natural pairwise $D_{eff}$ thresholds have been fitted, or ecological hysteresis has been observed.

No manuscript retuning, reopening of previous outcomes, silent import of eBird, or unreviewed merge of PRs #395–400 is authorized by this ledger.


## 2026-11-18 follow-up: V7 source-only q-topology audit (independent draft PR #400)

A subsequent **outcome-blind source-only prefit** on the original Kölzsch 2015 published q values has now been added to [PR #400](https://github.com/zuizui0223/payoff/pull/400), with executable source-only code, regression tests and [source result ledger](https://github.com/zuizui0223/payoff/blob/analysis/payoff-b-v7-uploaded-suppinfo-source-20261117/docs/PAYOFF_B_V7_SOURCE_TOPOLOGY_PREFIT_20261118.md).

- All 13 author-published adjacent q pairs: average signed q **0.545385**; q vs **ordinal** normalized route stage r=**−0.056225**; incoming ecological-barrier q mean **0.178** (5 links) versus **0.775** (8 links).
- Excluding the two unresolved code-to-S1 label aliases yields 11 original adjacent q candidates: average q **0.515455**; ordinal-stage r=**+0.050275**; 5 barrier links q=**0.178** versus 6 non-barrier links q=**0.796667**.
- Source-only coding-dependent q×ordinal-rank auxiliary VIF is **5.2894** (n=13) or **5.5906** (n=11), after flyway dummy, q, ordinal stage and barrier columns; the corresponding 7-column design leaves 6 or 4 transition-level residual df *if* those source transitions were independent.

**Interpretation:** original historical environmental q is not a simple monotone function of published ordinal route order; however, barrier and route structure can be highly explanatory, leaving limited independent interaction variation. These quantities are **not** the registered geographic q×U diagnostic, not an animal effect, and not a new discovery over Kölzsch. The real V7 interaction **remains NOT_ESTIMABLE**, and the 1982–2011 annual onset and original 16-region GPS geometries/membership remain unverified. The new prefit result must not be merged as a substitute for a bird timing or fitness test.


## 2026-11-18 continuation: annual GDD-jerk source authenticity guard

The author-paper/KNAW public source recheck confirms a separate issue beyond incomplete GPS region geography: the original Kölzsch 2015 source used **1982–2011 daily temperature observations** to obtain historical regional GDD-jerk onset dates, but the supplied supplement publishes only 16 regional *means/SDs*, 23 signed q values and plotted annual traces. The three Movebank datasets are GPS source archives, not the missing 480 original regional year-onset values.

The V7 source branch [PR #400](https://github.com/zuizui0223/payoff/pull/400) now contains a quantitative **candidate annual source replay gate** (no goose outcome access):

- Given **16 regions × 30 years = 480** independently sourced candidate original yearly onset rows, validate key coverage, finite Julian days, region-to-flyway membership and source identifier presence.
- Recompute the **16 original published mean/SD pairs** (fixed printed-precision tolerances ±0.5 d, ±0.05 d), then all **23 signed Pearson q coefficients** (±0.005).
- A synthetic *negative control* deliberately matches **16/16** marginal means/SDs and fails **23/23** q correlations. This demonstrates why published marginal climate summaries alone cannot authenticate an annual source table.
- Even a candidate table satisfying all printed statistics remains **NOT AUTHENTICATED**. This source-consistency gate cannot certify the original raw temperature stream, the shifted Icelandic climate representative coordinate, the 16-region GPS-to-climate spatial assignment or the published 40 complete spring-migration cohort. The registered q×geographic-U timing interaction stays **HOLD_NOT_ESTIMABLE**.

The existing candidate readiness tool now invokes this numeric replay when an annual CSV is supplied and continues to fail closed. All three GitHub Actions workflows for the final source-gate commit **passed**: [test](https://github.com/zuizui0223/payoff/actions/runs/44305270069), [test-environments](https://github.com/zuizui0223/payoff/actions/runs/44305267350) and [V2 archive verification](https://github.com/zuizui0223/payoff/actions/runs/44305267330).

The original study additionally reports that ecological barriers reduce the physical interregional environmental q signal but do not by themselves alter goose timing precision in the same straightforward way. This is a **published prior-art decoupling** consistent with treating potential information and realized timing separately; it does not identify downstream information-use strategy or compensation.

**Direct source still required:** original machine-readable 1982–2011 16-region onset dates *with* original regional coordinates/assignment and original 40 migration inclusion key. A new gridded climate reanalysis without those author-grounded coordinates would be an independent *new environmental replication*, not a V7 original-source reproduction.


## 2026-11-19: published Kölzsch Fig. 3 biological aggregate — failed cross-flyway transfer

A new *stacked draft* [PR #402](https://github.com/zuizui0223/payoff/pull/402) uses the 13 **printed original Fig. 3 region-level goose arrival RMSD values** (publication 2015; `RMSD` aggregate of individual stopover-site mismatches), matched to the 13 consecutive source-published historical regional q values in draft #400. This yields a real **published ecological aggregate**, but **not** the registered V7 individual `|A_ij-S_j,y|` outcome. It is also **not independent of the original authors' q–RMSD finding** (Table 1b original adjusted P=0.03).

The source-only diagnostic was frozen as **post-publication exploratory** before the new fit. With 13 paired region aggregates (11 if two source-code aliases are withheld), simple q–RMSD Pearson r is **−0.140/−0.265**, whereas pooled Spearman is **+0.074/−0.091**. A seven-column descriptive OLS model adding q×**ordinal route rank** decreases in-sample SSE **25.8%/16.9%**; the nominal remaining df are only **6/4** even before accounting for dependence.

**Independent transfer is negative:** a fixed-penalty, train-standardized ridge model that leaves out an **entire flyway** at a time gives 3-fold held-out MSE **138.45→183.29 days²** for 13 rows, and **119.59→182.57 days²** for 11 rows, when adding the ordinal q×stage product. The three original flyways show nonidentical simple q–RMSD signs. This is **a failed transportability stress test**, not evidence for a universal stage interaction, a proof against the original q predictor, or a new biological null at population scale.

**Claim ceiling remains unchanged:** published Fig. 3 site-level RMSD vs regional q is a mixed-grain prior-art-only ecological crosswalk; ordinal rank is not geographical urgency U; original annual GDD series and 16 GPS-region assignments are not verified. Preserve **V7 biological q×U = NOT_ESTIMABLE**, no invented uncertainty, animal cue use, causal fitness or hysteresis.

## 2026-11-19: E6 source-policy correction and causal mechanism gate

**Material correction to the original E6 interpretation:** the 944 Usui et al. temperature-effect rows used for the promoted E6 migration-distance benchmark included **264 effect rows from Hurlbert & Liang (2012)**, whose *original published Methods* explicitly used **eBird checklists** (PLoS ONE DOI [10.1371/journal.pone.0031662](https://doi.org/10.1371/journal.pone.0031662)). This is not inferred from the study title; the primary paper documents the original eBird input. The original E6 source cannot be labeled eBird-free.

The original E6 GitHub Actions artifact (ID 10953792024) was downloaded again and exactly SHA256-verified (`443cab62531d9b633aa6ee67da010fa66b6c230ef87e919d697269e77a7373f0`). Its frozen 944-row derived CSV SHA256 is `817a2d2d18931944103283c93e4d9bf80568906a21a92369ee168e4f8f203085`. Re-running the **same** inverse-variance WLS with Study×Species robust covariance reproduced original adjusted long-minus-short **+0.421476 d/°C** (95%CI [+0.121326,+0.721627]; p=0.007672). Excluding the **entire eBird-derived Hurlbert study**, independent of effect sign, produces **+0.608389 d/°C** (95%CI [+0.361817,+0.854961]; p=0.00002781) in **680 effect rows from 27 studies**. This +0.608389 is the original source's **already reported leave-one-study-out endpoint**, **not** a new independent PAYOFF discovery. See [PR #404](https://github.com/zuizui0223/payoff/pull/404). **The other 27 source studies are not all verified eBird-free**; do not promote 680 rows as a compliant fully source-audited dataset until the original studies are screened.

A separate **source-only** analysis of original study temperature-measurement-location labels and short/long distance classes gives the following corrected counts after that one mandatory provenance exclusion:

| Original temperature-location label | Effect rows | Studies | Studies including both short/long migrants at this location |
|---|---:|---:|---:|
| breeding | 155 | 9 | 4 |
| passage | 146 | 6 | 3 |
| passage or breeding | 286 | 15 | 8 |
| wintering | 93 | 1 | 1 |

**Only two** source studies contain the complete short/long × breeding/passage 2×2 crossed design; all other five location-class pairings have **zero** fully crossed source studies. The **predeclared minimum five** independent crossed studies is not met. Therefore the new temperature-location × migration-distance effect is **NOT IDENTIFIABLE / DO NOT FIT** (design result, *not* p-value for biological null). In particular, source `Temperature_location` is where researchers measured temperature, **not a direct observation of information actually available to an animal before commitment**. See [PR #403](https://github.com/zuizui0223/payoff/pull/403).

**Conclusion for the PAYOFF-B paper claim:** the migratory-distance phenological gradient remains a published association under one forced source-provenance exclusion, but the *information-distance causal mechanism* has not been identified; do not use E6 as direct proof of differential Bayesian cue use, and do not revive the V7 q×U effect without independent annual source geography and timing. The original E6 paper/source uses external bird data, and this no-eBird provenance correction must be kept visibly separate from the core frozen manuscript rather than retroactively described as its original protocol.


## 2026-11-19 continued original study provenance audit: 15/27 study primary observation systems identified

The original September-2026 E6 Usui-derived 944-row meta-analytic archive contains 264 published Hurlbert & Liang effects explicitly derived from eBird. After mandatory exclusion, 680 effect rows from 27 studies remain. A source-only methods and institutional-archive check, anchored in [PR #404](https://github.com/zuizui0223/payoff/pull/404) (`docs/PAYOFF_B_E6_STUDY_ORIGIN_PARTIAL_AUDIT_20261119.md`), now **identifies non-eBird-named primary observation sources for 15 original studies contributing 657/680 (96.62%) effect rows**. Examples include Japan Meteorological Agency standardized phenology, Delta Marsh/Helgoland ringing or first-sighting series, Buffalo ornithological records, Iceland's standardized local daily bird-arrival transects, and historical naturalist/phenological networks. This is an **observation-origin identification**, **not** certification of all auxiliary source streams or of complete eBird independence. Remaining **23 effect rows from 12 studies** are **NOT VERIFIED**; they must not be silently deemed compliant. No new temperature-response coefficient or original migration decision-time cue analysis was fit based on this selection.

The original +0.421 d/°C remains source-mixed provenance; the forced one-study-exclusion +0.608 d/°C remains a post-open sensitivity endpoint already available in the original leave-one-study-out result. **Neither should be called a fully source-audited eBird-free meta-analysis**, a new migration-distance result or causal information-access evidence. The original individual-level V7 interaction still lacks source-year regional GDD values and authoritative spatial geometry.

## 2026-11-19 source-audit closure to one unresolved original study, with nested sensitivity

The previous 15-study/657-effect primary-source inventory (statement F5) was a **historical partial stage**, not an additional independent set. Following explicit original-article/record-source checks, **26 of 27** studies retained after excluding verified Hurlbert & Liang 2012 eBird-derived source effects now have a published original local or named bird observation basis (**676 of 680** effects). The remaining **4 effects** come from Zalakevicius (2002, Lithuania), whose accessible original abstract does not identify an unambiguous original observation-record custodian. For Rubolini et al. 2007 (4 effects) and Ahola et al. 2004 (2), source studies describe local phenology records but raw-observation custodian remains uncertain. Do not infer source from geographically adjacent institutions.

The **post-open**, source-led nested same-model sensitivity has been executed using the exact immutable original E6 GitHub artifact and original study×species two-way clustered WLS:

| Cohort | Effects (studies) | Adjusted long-minus-short days/°C | 95% CI | Claim boundary |
|---|---:|---:|---|---|
| Original prior-art E6, **includes eBird-derived study** | 944 (28) | +0.421 | +0.121 to +0.722 | Old source-mixed provenance only |
| Entire verified eBird-derived Hurlbert study removed | 680 (27) | +0.608 | +0.362 to +0.855 | Not fully source-audited |
| Only original source-described observation series | 676 (26) | +0.602 | +0.354 to +0.849 | Two raw log custodians still unclear |
| Also remove those two weaker-documented site series | 670 (24) | +0.624 | +0.371 to +0.876 | Secondary/auxiliary use not fully audited |

**Evidence interpretation:** original published migration-distance phenological temperature-response gradient survives these *nested provenance restrictions*, **not** independent new geographic/taxon replication. Neither source locations nor migration-distance labels measure precommitment bird information use, downstream recourse, pairwise mismatch, fitness or the V7 source-geographic q×U. No effect was selected by the sign or significance of its coefficient. The corrected model is **not certified as completely eBird-free** and is **not** a causal information-access test. Updated source evidence and executable gates: [PR #404](https://github.com/zuizui0223/payoff/pull/404), `docs/PAYOFF_B_E6_STUDY_ORIGIN_PARTIAL_AUDIT_20261119.md` and `docs/PAYOFF_B_E6_PROVENANCE_TIER_SENSITIVITY_RESULT_20261119.md`.

Original theoretical claim and publication targets remain frozen. The most important forward biological gap is **actual cue observability before irreversible action**, **actual remaining control**, and individual-level matching/fitness, not adding non-independent published temperature slopes.


## 2026-11-19: original within-study migration-distance gradient survives study fixed effects

A separate post-open source study fixed-effects test was frozen and run in [PR #405](https://github.com/zuizui0223/payoff/pull/405), **stacked on the source-provenance branch #404**. Starting from the 676 source-described original Usui et al. effects, **13 of 26** studies contain **both** original source-coded short- and long-distance migrant classes (**444 effect rows, 269 species**). Other studies with only one distance class **cannot** identify a within-study distance effect; their effect rows were not used for the fixed-effects comparison.

Under original inverse-SE² source weights, study fixed intercepts, and Study×Species two-way clustered uncertainty using only 13 contributing study df=12, the adjusted **within-study long-minus-short temperature-response difference** is **+0.525253 days/°C** (95%CI **+0.224283 to +0.826223**, p=**0.002518**). The declared weight-cap sensitivity is **+0.525438**, and the unweighted comparison is **+0.608607**. All **13** leave-one-original-study-out effect estimates remain positive (**+0.472793 to +0.623006**), while 11/13 source studies have a positive *descriptive* weight-averaged difference and 2/13 negative. This is meaningful **within-original-study robustness** of a previously published migration-distance gradient, **not** 13 independent new ecological field studies or novel causal evidence.

Source code and tests: `scripts/payoff_b_e6_within_study_distance.py` and `tests/test_payoff_b_e6_within_study_distance.py` in draft #405, with full numeric receipts at `docs/PAYOFF_B_E6_WITHIN_STUDY_RESULT_20261119.md`; the dedicated original SHA256-pinned GitHub Actions [run 44484580314](https://github.com/zuizui0223/payoff/actions/runs/44484580314) completed **SUCCESS**, artifact **14509328403** independently opened and checked.

**Scientific limit unchanged:** within-study fixed effects remove arbitrary *study-level intercept* differences, but migration distance can remain associated with species physiology/photoperiod, phenological endpoints, and spatial climate measurement within a study. No direct precommitment cue accessibility, Bayesian information value, downstream correction capacity, interaction partner timing, fitness or natural hysteresis is inferred. The original data/source-tier panel is **not fully eBird-free certified**. Source-year geospatial [V7 goose q×U](https://github.com/zuizui0223/payoff/pull/400) remains `NOT_ESTIMABLE` and the canonical manuscript is frozen.


## 2026-11-19: new independent Bylot breeding/climate data-source feasibility — outcome held

[Draft PR #406](https://github.com/zuizui0223/payoff/pull/406) verifies original official 2026 **Nordicana D41** nesting-summary source metadata, **Nordicana D2** Bylot Lac du camp 1993–2023 daily mean air temperature metadata, and original Movebank study 1442516400 (2019–2023 greater snow goose GPS *study summary only*). It also checks PAYOFF's **existing** Reséndiz-Infante & Gauthier 2020 two-sided breeding-fitness source anchor, which already used **1991–2015** Bylot data; those years are *not* new independently untested fitness evidence.

Without viewing any new biological outcome, the fixed source calendar crosswalk gives:
- 1994–2015: 22 nominal nest-summary × BYLCAMP May 1–15 climate years, mostly already overlapping the 2020 published reproductive-timing work;
- **2016, 2017, 2018, 2019, 2022, 2023**: at most **6** genuinely post-2015 climate × nesting-summary calendar years, below a frozen **≥10 year** credible out-of-year transfer gate;
- 2019 only: nominal GPS calendar overlap with Nordicana **individual nest visit data**; 2019/2022/2023: nominal GPS overlap with Nest **summaries**, which have no verified individual bird-ID crosswalk.

Original Nordicana ZIP downloads require separate acceptance of source terms and have **not** been obtained by this work; no undocumented timestamps, source raw climate, nest IDs, behavior or demographic fitness are reconstructed. GPS owner permissions are also not established. The code and tests in PR #406 therefore correctly report **OUTYEAR_GATE_FAIL (maximum 6 years)** and **GPS_TO_NEST_INDIVIDUAL_JOIN_NOT_IDENTIFIED**. This is a new **source/estimability finding**, not a negative biological coefficient. A fresh post-2015 phenology–weather model is **not** fitted and the original 2015–2020 biology is not presented as new independent evidence.

**Recommendation:** retain E6's source-verified *prior published* distance gradient and exact theory unchanged; do not reopen V7 q×U. A direct test of information/actionability/fitness needs a source-provenance-cleared individual trajectory and independent future-state / reproductive observation with genuine identifiers, or a distinctly designed intervention. Adding more same-source temperature slopes or six nominal years is not sufficient.


## 2026-11-19 latest independent prior-art conflict: more stopovers and individual variation already tested

Scientific novelty audit [Draft PR #407](https://github.com/zuizui0223/payoff/pull/407) reopened two *original peer-reviewed* 2026 East Asian waterfowl sources:

- **Liu et al., J Anim Ecol, published 5 Nov 2026**, DOI [10.1111/1365-2656.70395](https://doi.org/10.1111/1365-2656.70395): **220 spring migratory paths from five species (2015–2023)**. The original paper **already reports** that higher stopover-site number is associated with greater sensitivity / closer alignment with breeding-area spring green-up.
- **Liu et al., Movement Ecology, published 27 July 2026**, DOI [10.1186/s40462-026-00685-3](https://doi.org/10.1186/s40462-026-00685-3): **323 tracks from 172 birds in four species (2015–2022)**; individual phenological variation and population tracking vary across species. The paper distinguishes coherent intermediate individual variation from excessive asynchrony. Same lead-author lineage and overlapping taxa/periods, but original individual ID overlap unverified, so **do not count the publications as two independent new replicates**.

**Mandatory novelty change:** a general macro-empirical claim `more stopovers -> better phenological tracking` or `individual phenological variance -> tracking` is now clearly **prior published work** and should not be sold as novel PAYOFF. The mathematical 2-patch optimum and synthetic coordination/barrier mechanisms remain valid within their declared models. The most distinct remaining ecological question is whether the environmental cue was **observable before the individual's actual decision**, whether useful speed/stopover/route correction was still feasible, and whether different interacting partners' uptake causes phase mismatch. Those *joint* causal/behavioral components have not been identified by the source-level effects inspected here and remain prospective, not a new positive macro result.

The JAE paper says raw GPS tracking data are in Movebank **available by request**; code/derived dataset DOI [10.5061/dryad.pk0p2nh4p](https://doi.org/10.5061/dryad.pk0p2nh4p) was located as a citation but its exact original file schema was **not opened**. No raw movements are assumed accessible, and neither eBird files nor altered V7 outcomes were used.


## 2026-11-19 independent source candidate: Eurasian Curlew GPS-to-nest-success joins (not cue evidence)

Hanzelka et al. (2026, DOI [10.1002/jav.03665](https://doi.org/10.1002/jav.03665)), original Dryad [10.5061/dryad.31zcrjf22](https://doi.org/10.5061/dryad.31zcrjf22) describes a **new** Europe-wide telemetry-derived breeding-performance data package, 2016–2025, **124 GPS-tracked Eurasian Curlews** and **233 season/period records**. The archive README documents a derived `dt_hab_Curlew.csv` (inside the ~591MB `Curlew_COE_habitat.zip`) with `Bird_ID`, `ID_seas`, `Nest_succ`, `Prebr` (days between arrival at breeding area and start of incubation), migration distance `Dist`, sex, regional groups and original stopover/nonbreeding habitat-use proportions.

This is stronger individual **movement-derived behaviour → binary nest-success** metadata than the Bylot calendar overlap, but the *original published study* already analyzes stopover/non-breeding habitat vs nest success, and those habitat effects are **prior art**, not new PAYOFF discoveries. The source `Nest_succ` is incubated nest success, not juvenile survival/recruited offspring. `Prebr` is an **observed, downstream interval** partly determined by incubation timing and cannot be mechanically equated with retained theoretical actionability `r_t` or causal waiting cost `D_{eff}`. The source says breeding/nonbreeding coordinates are **redacted** for conservation sensitivity. No original timestamped predecision cue quality, independent before-arrival destination forecast, or animal-level climate exposure is identified in this derived table.

The original large ZIP has **not been downloaded** and SHA256 is **not verified** in the current audit. **C1 remains a source-admission candidate only**, with source semantics from its original README. Direct information-deadline or natural pairwise hysteresis inference remains **NOT ESTIMABLE** until a properly licensed source with original cue chronology, corrective action, valid IDs and enough independent contexts is obtained. No guessed sensitive coordinates or alternative eBird occurrence records are to be used.


## 2026-11-19 original Curlew Dryad archive access and repeated-ID eligibility

Following the 2026 Hanzelka et al. Eurasian Curlew candidate source, **[draft PR #408](https://github.com/zuizui0223/payoff/pull/408)** froze and executed a source-only admission gate before any nest-success fit. The original [Dryad dataset DOI 10.5061/dryad.31zcrjf22](https://doi.org/10.5061/dryad.31zcrjf22), published 2026-10-01, has official original version ID **466868** and CC0 metadata. Official Dryad REST v2 metadata directly identified ZIP **file ID 4989265**, **590,985,065 bytes**, **provider SHA256 e3556851ef646eabad21dc0d482da58028b0327a8aaf459fdb02c3896bd48372**, and original README **file ID 4989366**, **14,323 bytes**, **provider SHA256 feb2e058090abd6863ef91570cd3afe4136d7ec9bb41f040612764648b5b892b**. **These SHA256 digests were declared by the provider and were NOT recomputed from inaccessible original file bytes.**

The official anonymous README and bounded Range ZIP download requests **both returned HTTP 401**. Thus the actual `dt_hab_Curlew.csv` source grain, distinct `Bird_ID`/season counts, repeated bird-years and within-individual mixed nesting outcomes remain **NOT VERIFIED**. The author-reported 124 GPS birds and 233 periods do *not* establish the statistical support of a within-bird new model. The original paper already models `Prebr` as a covariate and defines `Nest_succ` by GPS nest-cluster assessment; it does not directly observe predecision cue availability or an independent recourse budget.

PR #408 includes an offline user-authorized source gate. A full original `Curlew_COE_habitat.zip` would be verified against **both provider size and SHA256**; an extracted `dt_hab_Curlew.csv` is accepted for **provisional aggregate-only source support** but marked **NOT INDEPENDENTLY SOURCE-HASH VERIFIED** without the original ZIP. Neither path exports bird IDs, sensitive GPS coordinates, or biological effect coefficients. Dedicated GitHub Actions [run 44509246382](https://github.com/zuizui0223/payoff/actions/runs/44509246382) passed **10 synthetic source tests** and reproduced the **HTTP401** source limitation. **Curlew mechanism evidence remains source-blocked, not a negative ecological result.** The canonical PAYOFF-B information-deadline, V7 q×U and natural interaction-hysteresis claims remain unverified.

This update adds **F9**, bringing the evidence ledger to **32 distinct entries** (many are source audits and negative gates, not 32 independent affirmative ecological findings). Original theory and frozen main manuscripts unchanged.


## 2026-11-19: original Greenland white-fronted geese measured weather → later feeding and breeding (D7)

After 2026 Curlew Dryad original file downloads returned HTTP401, we located a **genuinely accessible, separately sourced 2024 original GPS/ACC/field model data lineage**: [Schindler et al. (2024), Proc R Soc B, 10.1098/rspb.2023.2016](https://doi.org/10.1098/rspb.2023.2016), archived public [author GitHub](https://github.com/aschindler23/Schindler_etal_2024_ProcB). This **2024 original publication already demonstrated** weather/habitat links to feeding and energy expenditure and subsequent breeding; not a new independent species/population effect newly collected by PAYOFF.

Exact-original `spring_data.csv` Git blob SHA1 `ca3736a281dfd2465921efc940dd985499c71a4f`, SHA256 `5d31ef41867d7f591f5a3fc5f2936df6e01dd91951c006e35b607a1e542e8972`. Source includes **49 birds, 107 distinct bird-years, 30 repeated birds, five calendar years 2018–2022, and exactly six ordered spring stages per bird-year**. There are 28 successes, 72 failed breeding attempts and seven deferrals. No event/ACC pseudoreplication or individual IDs redistributed.

A **post-publication exploratory**, pre-fit frozen test on same-source **stage3 earlier freezing → stage4 later feeding** (weather at first vs second half of Iceland spring staging), with earlier feeding, stage3/4 weather and original year fixed effects, shows:

- **β = −0.0013725 feeding *fraction* per 10 percentage-point increase in first-stage freezing** (bird-cluster 95%CI **[−0.013697,+0.010952]**, p=**0.8238**, n=107 bird-years/49 birds): **not supported** as an independent conditional linear lagged response.
- Adding earlier freezing to fixed-penalty ridge predictors improves out-of-bird MSE **0.004734→0.004400** (7.07%) and out-of-year MSE **0.012609→0.010500** (16.72%), **but only 3/5 years individually improve**. Weather has some retrospective forecasting signal at this source/cohort scale; this is **not** an animal's demonstrated cue use or an identified behavioral feedback mechanism.
- Leaving out 2018 makes `storm4` a **zero-variance covariate** for the other four years, so that full frozen covariate omission fit is **NOT_ESTIMABLE** (preserved rather than silently dropping the covariate). The remaining four omit-year β CIs cross zero.
- Adding observed **late-stage feeding and log ODBA** to same-time weather/earlier-behavior predictors of later *breeding_success* **worsens out-of-bird log loss 0.650239→0.652046**, while **improving out-of-year 0.654137→0.642096** with an important negative 2020 fold. **No consistent transferred behavior→breeding predictive gain** across both independent groups.

**Claim ceiling:** this explicitly separates *physical weather forecastability*, *measured temporal behavior*, and *later reproduction* in a previously published original lineage; it **does not** identify q as an individual's pre-commitment belief, a causal correction actuator budget, marginal waiting cost D_eff, multi-partner asynchronous decisions or natural hysteresis. Do not promote the partial CV improvement into evidence for the exact PAYOFF-B information deadline or claim newly discovered weather→breeding effects.

Original-source SHA-pinned [GitHub Actions run 44529079285](https://github.com/zuizui0223/payoff/actions/runs/44529079285) **SUCCESS**, output artifact **14532508038** independently downloaded and hash checked. Full exact model/scope/result and aggregated JSON source: [Draft PR #409](https://github.com/zuizui0223/payoff/pull/409), `docs/PAYOFF_B_GWFG_LAGGED_WEATHER_RESULT_20261119.md`. This is D7 in the evidence ledger (33 distinct records, **not** 33 independent ecological studies). V7 original q×geographic U remains **NOT_ESTIMABLE**, no eBird, no original manuscript or main merge.


### D7 follow-up 2026-11-19: within-year weather-assignment null — original signal exceeds most shuffles, not a causal cue test

After observing the frozen 2024 Greenland-goose stage3 freezing→stage4 feeding β=−0.00137 (95%CI crosses zero, p=.824) and modest heldout prediction gain, a **clearly post-open** permutation design was separately fixed **before looking at permutation outcomes**: within each of the original five calendar years, shuffle **only the bird-year assignment** of the observed stage3 freezing fractions 99 times (NumPy seed 20261119), preserving all original year-specific weather marginal values, bird outcomes, stage3 feeding and stage3/4 weather/time covariates. This **is not** a randomized natural cue intervention: weather timing/date and habitat correspondence are not preserved.

The original frozen Ridge α=1 added-freeze forecast gain was **+0.000334617 bird-heldout MSE** and **+0.002108508 year-heldout MSE**. The shuffled median gains were respectively **−0.000061006** and **−0.000066713**, with only **1/99** within-year shuffled assignments matching or exceeding each observed gain; the +1 corrected post-open tail fraction is **0.02** for both evaluations. The source-weather matching retains *observational, individual/year-indexed predictive information beyond yearly marginal distributions under this specific shuffle design*. It does **not** establish that a goose perceived any reliable upstream cue before commitment, an adaptive feedback controller, the information deadline (q_{wait}), a causal compensation pathway or breeding fitness mediation. The primary conditional OLS response remains **NOT SUPPORTED**, and stage4-feeding→breeding heldout results remain mixed.

This is **another test on the same 107 original 2024 bird-years**, attached to D7 rather than counted as independent new empirical evidence. Source and 99-permutation tests in [Draft PR #409](https://github.com/zuizui0223/payoff/pull/409); source-hashed [Actions run 44530687896](https://github.com/zuizui0223/payoff/actions/runs/44530687896) **SUCCESS**, result `docs/PAYOFF_B_GWFG_WITHIN_YEAR_FREEZE_PERMUTATION_RESULT_20261119.md`, aggregate artifact ID **14533148638**. No eBird or raw GPS exported and no frozen manuscript changed.


### D7 decisive calendar-matched control: prior 0.02 source-weather assignment finding **does not survive**

A more stringent **post-open** timing-aligned original source check has now been completed on the **same 107 Schindler et al. (2024) Greenland white-fronted goose bird-years**. It uses the same original SHA-verified CSV, same frozen ridge α=1 stage-3 freezing → stage-4 feeding model and the same leave-bird/year-out predictions; only the randomization blocks were changed **after an outcome-blind source-support inspection**. Every shuffle holds year, outcome, original feeding, the animal's real start-day and other weather fixed, while shuffling the earlier freezing values only inside matched eligible source strata.

| Freeze3 assignment null (99 shuffles) | Swappable bird-years | Nonconstant blocks | Bird-heldout upper tail | Year-heldout upper tail |
|---|---:|---:|---:|---:|
| Original year-only shuffle | all 107 potentially | 5 year groups | **0.02** | **0.02** |
| Same original year **and exact first-stage starting day** | **48** | **14** | **0.48** | **0.58** |
| Same year + **7-day start bin and 3-day stage3 duration bin** | **52** | **11** | **0.35** | **0.47** |
| Same year + exact start day **and exact staging duration** | **17** | **7** | **NOT ESTIMABLE** | **NOT ESTIMABLE** |

Tail fractions are **descriptive post-open permutation exceedance fractions** with +1 correction, NOT causal p-values or equivalent tests across these different exchangeable-row counts. Exact-day null median forecast improvements approach the real data gains (+0.000328 vs observed +0.000335 bird-heldout MSE; +0.002216 vs observed +0.002109 year-heldout MSE). The week+duration null likewise gives medians +0.000307 and +0.001891. Therefore the strong **special bird-year weather-alignment interpretation from the first year-only 0.02 permutation is no longer defensible**. Calendar exposure matching explains why the original matching cannot be called extraordinary under a more appropriate constrained null, but does **not** prove all weather signal is due entirely to calendar: **55–59 bird-years were fixed by low-support matching** and the strict same-day×same-duration contrast failed its frozen ≥40-row/8-block gate.

Crucially, the original year-FE bird-clustered linear model remained nonsignificant **β=−0.001373 (95%CI −0.013697 to +0.010952, p=.824)**; adding late-stage behavior still failed consistently across bird/year withheld breeding-success forecasts. The new source-linked outcome is a **falsifying robustness result for an overly strong information-use narrative**, not a discovery that geese do not perceive information. No newly estimated `q`, `D_eff`, `r(t)`, causal compensation or animal fitness mechanism exists.

This is a **within D7 revision**, NOT independent evidence entry #34: [PR #409](https://github.com/zuizui0223/payoff/pull/409) contains locked matching protocols, source-only code, **15 passed dedicated tests**, [GitHub Actions run 44537189557](https://github.com/zuizui0223/payoff/actions/runs/44537189557), aggregate artifact ID **14537265791**, and `docs/PAYOFF_B_GWFG_CALENDAR_MATCHED_PERMUTATION_RESULT_20261119.md`. **Stop further same-source post-hoc mechanism searches** in these 107 bird-years. The correct next biological target is an **independent source that actually records cue information at commitment, subsequent capacity for movement adjustment, and ideally reproductive outcomes** with original identifiers. Original 2024 published work, main, V2/V7 and journal manuscripts are unchanged.


## 2026-11-19: original 2023 songbird sequential decision timestamps/source linkage (C2, prior art)

A separately sourced, original **Rüppel et al. (2023), *Royal Society Open Science* 10:221420** dataset was independently accessed through its primary [Figshare DOI 10.6084/m9.figshare.c.6403996](https://doi.org/10.6084/m9.figshare.c.6403996). Its CC BY 4.0 100,303-byte `rsos221420_si_002.zip` was SHA256 verified (`0ef08e19104aaceff5ef2700c324a094c49cbe2cd24ca198e3853b656d7744c6`). R's native source loader recovered the actual **`data.Event` 1,783 bird×night/day-at-risk records (33 columns)** and **`flights` 178 first-flight records (70 columns)** after the generic Python RData parser proved unsupported. Both include `motusTagID` and the **entire 178-individual ID sets match**, with zero unmatched or duplicated first-flight IDs. Original source has **1,605 nondeparture risk days + 178 terminal departure event rows**, **24 observed landings + 154 nonlandings**, all 178 flights with complete start/end wind-cloud fields, and 175/178 terminal-event dates on the exact same UTC calendar day as first flight start (178/178 within ±1 day). No original bird IDs, coordinates or individual source rows were exported.

**This is verified suitability of an original three-stage observational movement dataset, not an independent newly discovered natural mechanism.** Rüppel et al. themselves reported favourable-weather departure, wind-linked route choice and adverse-weather flight interruptions/landing. PAYOFF's source audit has **not** refitted any biological effect, authenticated bird-specific future destination spring forecast q, independently measured remaining movement recourse `r(t)`, identified causal net waiting cost `D_eff`, partner phenological mismatch, or breeding fitness. Weather at departure is not necessarily what the bird subjectively forecast about future route conditions. Landing and offshore flights are receiver-coverage/selection sensitive.

The source is a distinct potential contributor to **information-timing / correction** measurement, but any added forecast-error or cue→landing model requires independent *forecast-issue-time* weather information, source-author route coding, detection-bias controls and an explicitly frozen new endpoint. It is not a natural validation of the mathematical `q_wait(D_eff)` or information-constrained coordination trap.

[Draft PR #410](https://github.com/zuizui0223/payoff/pull/410) holds all source-only contracts, original RData loading code, joined original-grain verification, tests and aggregate-only source receipts; original source [Actions 44543643759](https://github.com/zuizui0223/payoff/actions/runs/44543643759) **SUCCESS**, independently downloaded aggregated artifact ID **14538699556** with ZIP SHA256 `bba1e8256451cc730aa9b6c8b2c7045af2d570143a39bd160b01aea7f9f20b25`. This is new ledger entry **C2**, yielding **34 distinct model/source/evidence records, not 34 independent ecological effect confirmations**. Frozen manuscripts and `main` untouched.


### C2 next independent environmental source gate — issued historical GFS forecasts, not a bird cue yet

[NCAR GDEX NCEP GFS 0.25° operational historical forecast archive d084001](https://gdex.ucar.edu/datasets/d084001/) **DOI 10.5065/D65D8PWK** includes original initialization-time forecast products for **2019, 2020 and 2021**, the exact original Rüppel coastal songbird observation years. Operational GFS is initialized 00/06/12/18 UTC; unlike ERA5 retrospective reanalysis, a genuine archived forecast with issue time **before** a bird's choice could potentially be tested for external *future-condition* availability. The [official provider data-access page](https://gdex.ucar.edu/datasets/d084001/dataaccess/) shows that customized *time×place×parameter subsets require registration/login*. No user login has been performed, no original GRIB2 file or file digest obtained, and no verification yet that the original meteorological fields/lead times survive the extraction.

The independent before-decision issue-time source gate has been **frozen without accessing biological forecast outcomes** in [PR #410](https://github.com/zuizui0223/payoff/pull/410), `docs/PAYOFF_B_RUPPEL_GFS_ISSUE_TIME_SOURCE_GATE_20261119.md`, with source-only deterministic verification code/tests. It requires a genuine operational initialization **≥1 h before** original decision, a forecast valid **after** the bird's decision, and a primary target ~6 h after choice (±1.5 h) without substituting zero-lead nowcasts, forecasts initialized *after* departure, 4-week rolling current AWS files or source ERA5 retrospectively. Separate 3/12 h targets remain fixed sensitivities. **Model issuance time is only potential environmental information; whether an individual bird perceived or used it is still unmeasured.** This is a continuation of C2 (34 statements total), not a new biological positive result. No actual forecast archive bytes or original source bird values used or distributed.


### C2 route×landing frozen support failure, 2026-11-19 — do not promote stepwise migration as information recourse

Following successful source-faithful linkage of **178** Motus bird identifiers across **1,783** departure at-risk rows and **178** first-flight records, the original Rüppel et al. 2023 (Royal Society Open Science, DOI [10.1098/rsos.221420](https://doi.org/10.1098/rsos.221420)) source was audited as a full **2×2 route × later observed landing table**. Frozen route-support gates required **≥5 landings and ≥5 nonlandings in each route**, and observed landing across multiple original species and years, before any new natural route-specific recourse interaction could be attempted.

| Original source route | Landing | No landing | Total first flights |
|---|---:|---:|---:|
| `coasting` | **21** | **133** | **154** |
| `sea-crossing` | **3** | **21** | **24** |

The original source has **only 3 sea-crossing landings**. Marginals both happen to equal 24 (24 sea flights, 24 total landings), but they **are not the same 24 birds**. The prespecified balanced-cell necessary condition was \(5 \le x_{sea,land} \le 19\); actual \(x=3\) fails. Original species composition is Garden Warbler (66 flights, 15 sea), Greater Whitethroat (68 flights, 9 sea), **Sedge Warbler (44 flights, 0 sea)**, precluding robust cross-species replication of a route modifier. Original years 2019/2020/2021 have 48/68/62 first flights and 8/11/5 observed landings.

**Source-design conclusion: `ROUTE_LANDING_MODIFIER_NOT_ESTIMABLE_UNDER_FROZEN_SUPPORT`.** This is **not a p-value for biological absence**, a new habitat/route fitness finding or an observed cue-use mechanism. An end-flight `u_end/v_end/c_end` weather measurement cannot be used as if it were issued before departure, and receiver-coverage selection bias is not resolved. NCEP GFS historical forecast issue-time metadata are available for 2019–2021 (NCAR GDEX d084001, DOI [10.5065/D65D8PWK](https://doi.org/10.5065/D65D8PWK)), but no original issued forecast GRIB bytes were acquired. Retrieving large forecasts for this particular **route × landing** biological interaction is therefore not the next justified step unless a genuinely better supported independent source is selected.

This source-only negative identification result belongs inside **existing C2**, not as a 35th independent evidence item. Original SHA-pinned [Actions run 44546509558](https://github.com/zuizui0223/payoff/actions/runs/44546509558) completed successfully; 5 purpose-built synthetic cross-tab tests passed, resulting artifact ID **14540384944** with ZIP SHA256 **`0eb07b73b93d3487f350aca93ff26c4ac7c7556022f23b41b769e741d4970633`**. Executable and full source audit in [draft PR #410](https://github.com/zuizui0223/payoff/pull/410), `docs/PAYOFF_B_RUPPEL_ROUTE_LANDING_SUPPORT_RESULT_20261119.md`. Continue independent forecast-and-trajectory research only after obtaining a larger detection-audited dataset that actually crosses routes and landings; do not retune the 178-bird source. Frozen V2/V7/manuscripts and `main` unchanged.


## 2026-11-20: experimentally manipulated physiological flexibility is real *published prior art* — C3

A new original-data provenance audit [Draft PR #411](https://github.com/zuizui0223/payoff/pull/411) accessed the authors' [Lameris et al. 2025 *Functional Ecology* resource manipulation](https://doi.org/10.1111/1365-2435.70183) and original CC BY 4.0 [Figshare DOI 10.6084/m9.figshare.28660718](https://doi.org/10.6084/m9.figshare.28660718) (version 2). Red Knot `Calidris canutus islandica` food access was experimentally randomized to **6, 12 or 24 hours/day** and departure following release monitored; the authors **already reported** increased capacity for body-store gain and earlier departure as foraging opportunity improves. This manipulation addresses an **action/physiological capacity** component in nature, **not predictive information timing**.

Original 2025 Figshare file 53244101 `4.combined_data.csv`, SHA256 `755833eb13e241def834f12ea2c8d775ec643def807b23a4b3695ee7805e834f`, directly yields **102** bird-season records (not automatically identical to 97 published experimental subjects), of which **2021 pilot: 14 rows/zero dated departures; 2022: 43 rows/27 release dates/20 departure dates; 2023: 45 rows/33 release dates/25 departure dates**. Totals: **60** release dates, **45** directly observed departure dates, **53** nonmissing source departure-event flags and **44** Julian departure entries. Literal `NA` missing values were correctly excluded after identifying and fixing an initial parser error; no missing departure was coded as a nondeparture. Original year/treatment codes and three author MD5 checksums were independently verified; original 2,336-row repeated biometric series is **not** the experimental replication grain.

**Source-identification limitation:** original treatment was assigned at an **aviary within year**. The publicly available combined data include bird/year/treatment but **lack an independently authenticated bird→aviary membership crosswalk**, so an independently reconstructed **aviary-clustered** food-access treatment effect is **NOT_ESTIMABLE** from these derivative data without further source mapping. This does not invalidate or retune the original authors' already-published estimates. The additional source has no subjective early weather forecast, q, source–destination environmental channel, pairwise partner timing or realized demographic fitness.

### Crucial two-gate distinction for PAYOFF-B

| Mechanism component | Source-backed ecological observation | Limitation |
|---|---|---|
| Environmental conditions can influence sequential decisions | Rüppel et al. (2023) **178** tracked songbirds, original departure→route→landing source [PR #410](https://github.com/zuizui0223/payoff/pull/410) | Weather is realized local observation, **not** authenticated bird-accessible issue-time forecast q; sea-crossing landings only **3**, no robust route-specific recourse effect |
| Resource constraints can determine feasible timing changes | Lameris et al. (2025) **6/12/24 h/day** randomized food opportunity, already published earlier departure | Source aviary mapping not independently reconstructed; **no cue revelation manipulated** |
| **Information availability × actionability** changes the same individual's choice and final payoff | **No direct naturally identified joint test** in the two studies | Different subjects, species, years, assignment units and endpoints; cannot multiply or concatenate separate effects |

The original exact **information-deadline threshold**, (q_{wait}(D_{eff})), the joint (q\times r(t)) value of recourse, and cross-species coordination/hysteresis **remain theoretical and not verified in natural data**. Prior 2025 shorebird experiment **occupies the simple novelty claim** that extra resource access allows earlier migratory departure. It is **not** a new PAYOFF natural positive and should not be counted as independent validation of the entire causal chain.

This is **C3**, bringing the ledger to **35 source/model/evidence entries, not 35 independent ecological studies**. Exact original source, correction and audit: `docs/PAYOFF_B_RED_KNOT_AVIARY_AND_DEPARTURE_RESULT_20261120.md` in [PR #411](https://github.com/zuizui0223/payoff/pull/411); dedicated original-source [GitHub Actions run 44660943443](https://github.com/zuizui0223/payoff/actions/runs/44660943443) **SUCCESS**, artifact **14595686528** verified. No original animal ID, location or source rows exported; manuscripts and `main` unchanged.


## 2026-11-20: original urgency×weather-selectivity already covered by 2025 songbird research — P2

The original open paper [Klinner et al. (2025), *Movement Ecology* 13:64, DOI 10.1186/s40462-025-00575-0](https://doi.org/10.1186/s40462-025-00575-0) **already reports** that pre-Saharan spring migrants **wait longer and select favourable tailwinds more strongly** than trans-Saharan migrants. Five species were monitored at Helgoland (two pre-Saharan, three trans-Saharan) with 883 at-risk bird-night observations before seven excluded crosswind/flow-assistance source records. The time-urgency interpretation is **inferred from migratory strategy**, not independently randomized urgency or observed information about future destinations. Source supplemental data DOI [10.57782/WXZE6H](https://doi.org/10.57782/WXZE6H) is cited by the authors but not independently byte-verified/refit here.

This literature **preempts a simple PAYOFF novelty headline** that greater migration urgency causes weaker departure weather selectivity. Together with Lameris et al. 2025 food-access manipulation **already demonstrating physiological flexibility and earlier departure**, and Liu et al. 2026 **already demonstrating benefits of multiple stopovers**, basic time-urgency and resource-recourse biological components are established outside PAYOFF. Their **different birds, original populations, calendars, decision grains and outcomes** cannot be joined as a same-individual information×actionability causal experiment.

What remains specifically prospective is the **joint gate**: historical cue predictive reliability known to the analyst *at or before the focal organism's commitment*, objectively quantified remaining movement/phenological options, and independently observed partner synchrony/fitness after the choice. No original source inspected here identifies the theoretical (q_{wait}(D_{eff})), (q\times r(t)) as a jointly identified natural causal response, or perfect-information coordination/recovery hysteresis. The exact synthetic/mathematical theorem remains intact and should not be retroactively presented as a novel discovery of known departure-weather selectivity.

P2 added as a **prior-art collision**, with full specific citation/limits in `docs/PAYOFF_B_2025_URGENCY_WIND_PRIOR_ART_20261120.md`. Ledger now **36 theory/source/evidence statements**, not 36 independent positive ecological results. Original V7 unopened, main and frozen manuscripts unchanged.


## 2026-11-20 prospective q×actionability joint-assay design — NOT a new natural evidence record

The 2026 published source review concluded that the biological building blocks are **already prior art**: Rüppel 2023 sequential weather-associated decisions, Lameris 2025 randomized food-access departure flexibility, Klinner 2025 time-urgency / favourable-tailwind selection, and Liu 2026 stopover/individual tracking. **None** identifies the canonical information q and remaining actionability r jointly with a downstream partner or breeding payoff on the same decision units.

A distinct **prospective controlled ecological mechanism-proxy assay** is now specified in [Draft PR #412](https://github.com/zuizui0223/payoff/pull/412), **not merged to main**. The assay proposes 2×2 assignment at the level of **independent bumblebee colonies** of externally generated state-signal reliability q=.65/.95 and a physically enforced corrective-switch opportunity r=.20/.85 in a contained two-floral-patch matching task, before commitment. The exact reduced PAYOFF witness has π=.4, C_F=2, C_M=1, q0=.75, and D=.08; only the high q/high r arm makes r×V_A(q)−D positive (+.192 model loss units) under a Bayes-optimal actor. The biological cue, physical correction-gate fidelity, real loss scale and learning are **not assumed valid** and must pass **independent pilot calibration** before outcome collection.

A fixed **synthetic-only 300-replicate, 4-arm colony-unit sample-size simulation** using 48 hypothetical trials/colony was executed in [GitHub Actions 44681774335](https://github.com/zuizui0223/payoff/actions/runs/44681774335). Under assumed **75% policy adherence**, positive-interaction approximate-normal detection increases from **76% at 16 independent colonies/arm** to **89% at 24/arm**, and **98% at 32/arm**. Under **50%** compliance, detection reaches only **70% even at 32/arm**. A genuine no-use sharp-null simulation was corrected and rerun after detecting a truncated-Gaussian compliance bug in an early attempt; its interaction estimates are ~0. Some approximate-null two-sided rejection frequencies reached **7.3%**, so real-world small-colony inference must use a validated cluster-level procedure rather than these normal power approximations. **96 colonies total for 24/arm is a hypothesis-conditioned estimate, not a feasibility or funding claim.**

**This is NOT a new 37th evidence statement**: no organisms or real biological outcomes were observed, nor was any naturally measured q/r, season-scale phenological synchrony, migration fitness or information-deadline causal effect estimated. It is a prospective *measurement and design readiness* step only. Original submitted V2/V7 and main remain unchanged; the 36-entry evidence/source/theory ledger count stays fixed.
