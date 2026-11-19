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
