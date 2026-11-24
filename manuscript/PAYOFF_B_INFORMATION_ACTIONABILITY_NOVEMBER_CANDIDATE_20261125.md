# Knowing in time: information and recourse in seasonal ecological interactions

**Paper 2 — November evidence integration candidate, 25 November 2026.** Theory-led Major Article development draft (The American Naturalist is a proposed venue, not a submission decision). This is an alternative working manuscript, not a replacement of the frozen V2/V3 or the October V4 reviewer packet. It incorporates the corrected mathematics of [PR #335](https://github.com/zuizui0223/payoff/pull/335) and distinguishes exact conditional results from exploratory reanalysis and published background. No new ecological outcome is fitted here.

## Abstract

Seasonal organisms must anticipate environmental change while they still retain the means to respond. We distinguish environmental predictability, information available before commitment, and remaining corrective opportunities. In a reduced decision model, learning and irreversible loss of actionability can create a finite interval during which information is worth using; different commitment costs can desynchronize interacting actors even when they receive the same cue. An explicit phase controller shows how partner differences can transform shared seasonal forcing into timing divergence. Exploratory reanalysis of 104 eastern North American forest green-up links found increasing spatial correlation between 2002–2009 and 2010–2017, yet almost all apparent late-period forecasting gain in a hypothetical deadline scenario occurred after actual target onset. Among 38 repeatedly observed mule deer, later departure relative to green-up was associated with shorter stopovers within individuals and years, although calendar timing could not be separated from seasonal phase. Published consumer–resource and resident–migrant timing asymmetries motivate the interaction-level prediction. These findings support distinct components, not a demonstrated natural information-by-recourse mechanism. We propose that seasonal vulnerability should be evaluated through both decision-time information and feasible subsequent correction, rather than arrival timing or cue correlation alone.

**Keywords:** phenological mismatch; ecological interactions; migration; information; actionability; seasonal timing.

## 1. Introduction

Seasonal matching requires both an appropriate target and an ability to reach it. A migrant that reaches a resource peak may have departed at the appropriate time, or it may have departed early or late and subsequently altered its movement. A plant that correctly detects early spring may nevertheless flower before a partner becomes active. These examples illustrate why the timing of the final event does not alone diagnose the mechanism of adaptation.

Remote environmental information, optimal migration timing and changes in the value of cues along migratory routes are established problems (Bauer et al. 2008; Kölzsch et al. 2015; Torstenson and Shaw 2025). Migration speed and stopovers can compensate for initial phenological error (Ortega et al. 2023; Dossman et al. 2023). We do not claim discovery of these phenomena. Instead, we ask when information that could guide a seasonal response becomes useful relative to the time at which the available actions are constrained, and how differences between interacting actors convert this individual problem into an ecological mismatch.

This distinction changes the simplest climate-change prediction. A geographical correlation may increase without increasing the marginal forecast value of a cue, or the cue may be observable only after the focal event. Conversely, an organism that initiates movement under uncertainty may retain opportunities to adjust later. The two situations cannot be ordered by initial cue quality alone.

Our theory provides three linked results. First, information accuracy and its realizable value can have different time courses. Second, differences in error retention can generate timing divergence even under shared forcing. Third, a coordination penalty can make a beneficial joint transition inaccessible to unilateral changes. We use source-faithful environmental and animal reanalyses to evaluate the separately observable components of this account, retaining negative controls and limits of identification rather than treating them as a single confirmed causal sequence.

## 2. Theory

### 2.1 Information has value only while a response is possible

Let the future state be early or late, with prior probability \(\pi\) of early. False-early and missed-early action losses are \(C_F,C_M>0\). For a binary symmetric signal of accuracy \(q\geq1/2\), define \(S=(1-\pi)C_F+\pi C_M\) and \(B=\max((1-\pi)C_F,\pi C_M)\). With a free option to ignore a signal, the gross gain of the state-contingent policy relative to the best prior-only action is

\[
V_A(q)=[Sq-B]_+.
\]

The reduced waiting model assumes that a fraction \(r(t)\in[0,1]\) of that gain can still be realized at time \(t\), and that acquiring or waiting for the cue costs \(C(t)\). The net benefit relative to an unchanged outside option is \(N(t)=r(t)V_A(q(t))-C(t)\). This multiplicative factorization is a model assumption, not an identity for arbitrary biological response spaces. Free optional information has nonnegative gross decision value at fixed actions; the cost or loss of actions, rather than information itself, can make waiting unattractive.

On the branch \(Sq>B\), any differentiable interior stationary point satisfies

\[
rSq'=-r'(Sq-B)+C'.
\]

With no direct waiting cost and \(q(t)=q_{\rm init}+\Delta q(1-e^{-\alpha t})\), \(r(t)=e^{-\beta t}\), \(\alpha,\beta>0\), define \(A=S(q_{\rm init}+\Delta q)-B\), \(D=S\Delta q\), and constrain the cue trajectory to \([1/2,1]\). If \(A\leq0\), no finite action has positive net benefit relative to the outside option. If \(A>0,D=0\), immediate use is optimal. Otherwise a maximizing time with positive value is

\[
t^*=\max\{0,\alpha^{-1}\log[(\alpha+\beta)D/(\beta A)]\}.
\]

Only when \(Sq_{\rm init}=B\) and \(\Delta q>0\) does this reduce to \(t^*=\alpha^{-1}\log(1+\alpha/\beta)\). In that threshold-normalized case the value is zero initially, strictly positive at intermediate times and tends to zero as opportunities vanish. A fixed positive cost below its maximum therefore yields a finite profitable-use window. Faster loss of actionability moves the optimum earlier even at the same learning rate. This is a conditional consequence of the exponential model, not an assertion that all biological deadlines have this form. The general optimum correction follows the October S4 mathematical note (#335).

A raw departure delay also need not measure its effective cost. The single-commitment formulation \(D_{\rm eff}(\delta)=J(\delta)+\min_{c\in\mathcal{C}(\delta)}[K(c)+M(\delta-c)]\) distinguishes irreversible waiting loss \(J\), compensation cost \(K\), and residual delay loss \(M\), subject to a feasible correction set. Two individuals with different correction budgets can rank differently in elapsed delay and effective cost.

### 2.2 Interaction mismatch is generated as well as inherited

Write a signed error relative to an explicitly defined seasonal target as \(e_{i,t}\). After action \(u_{i,t}\), a local model is \(e_{i,t+1}=\phi_{i,t}(e_{i,t}-u_{i,t})+w_{i,t}\), where \(w\) is a change or innovation in the target and \(\phi\) represents passive propagation. With a linear, unclipped action \(u=h\hat e\) and a centered linear observation model with conditional-mean gain \(K\), the conditional-mean retention is \(\lambda=\phi(1-hK)\). This coefficient is not generally equal to a feedback gain, nor is it a full variance-propagation coefficient.

For two actors measured on a common phase coordinate (including any required optimal lag offset), suppose their conditional mean recursions have no unaccounted intercept and constant retentions \(\lambda_1,\lambda_2\). For \(m_t=(e_{1,t}+e_{2,t})/2\), \(\Delta_t=e_{1,t}-e_{2,t}\),

\[
\Delta_{t+1}=(\lambda_1-\lambda_2)m_t+
\frac{\lambda_1+\lambda_2}{2}\Delta_t+(w_{1,t}-w_{2,t}).
\]

Even if \(\Delta_t=0\), a common nonzero phase error and unequal retention can generate divergence when innovations are shared. Under shared constant additive forcing \(w\) and \(|\lambda_i|<1\),

\[
\Delta^*=w\,\frac{\lambda_1-\lambda_2}{(1-\lambda_1)(1-\lambda_2)}.
\]

Thus an actor that improves its tracking relative to a common reference can become less synchronized with a slower-adjusting partner. This does not imply that every timing difference reduces interaction fitness; the resource or interaction window and payoff must be measured separately.

### 2.3 A strategic barrier is distinct from loss of opportunity

The existing PAYOFF-B perfect-information coordination game shows that both an obsolete and an informed convention can be strict equilibria under specified individual gains and mismatch penalties, despite higher joint payoff in the latter. Consequently, restored environmental predictability need not restore coordination in the model. In the explicit synthetic moving-landscape study at mutation step 0.1, 22 of 24 declared positive-interaction design cells contained a coordination barrier and 21 of 24 changed from local extinction to persistence at a coordinated strategy. These are sampled model conditions, not estimated probabilities in nature. The model does not establish natural hysteresis or show that the same parameters govern the empirical systems.

## 3. Evidence design and scope

We distinguish (i) exact conditional results, (ii) synthetic demonstrations, (iii) exploratory original-data analyses, and (iv) published anchors. Our evidence units differ among modules; no omnibus effect, shared latent parameter or cross-module causal path is estimated.

The primary environmental module uses the satellite-only forest file of Amaral et al. (2025), excluding species-conditioned range masks linked to eBird. It pairs each target with the nearest strictly southern valid cell within 800 km, yielding 104 links from 106 forest cells and 88 source-cell blocks over 2002–2017. Signed within-window detrended correlations, rolled-forward target-year error and hypothetical observation availability are distinct estimands. The availability analysis sets the decision date from the training-only target forecast minus seven days and assumes seven days of report latency; both are illustrative rather than measured animal deadlines or operational MODIS latency. Held-out target onset is used only for post-scoring chronology classification. These analyses share the same source and were developed after earlier results were known; they are not independent preregistered replications.

The independent radar source (Adams et al. 2025) uses 828 complete station-years from 53 stations, 2003–2018, for migration-passage dates and retrospective mean green-up. We retain the baseline versus augmented leave-entire-year-out prediction and descriptive event ordering. An unexplained green-up DOY of -27 is not silently recoded; the chronology fractions bound its possible contribution.

The animal module uses original Ortega et al. (2023) source data, with individual and year fixed effects on stopover days and signed departure phase for 100 complete animal-years of 38 repeatedly observed deer. Missing stops are missing, observed zero stops are retained, and uncertainty is conditional on observed years, via 10,000 whole-animal bootstrap draws. The amended fixed-effect design allows component-specific intercept normalizations after a structural support failure but before coefficient estimation; the analysis remains exploratory. The same-source departure calendar versus phase model was screened before a new coefficient was opened.

An additional Usui et al. (2017) meta-analysis robustness result is eligible as a *provisional* supplementary comparator only: the known eBird-derived and one unverified source have been excluded from the 13-study within-study subset. Full remaining source-policy review is required before promotion to the main submission. Previously frozen eBird-conditioned V8 and pooled E6 values remain in historical provenance, not active evidence.

## 4. Results

### 4.1 Environmental predictability and information available in time are different

Mean source–target detrended green-up correlation increased from 0.79859 to 0.87916, with a change of +0.08057 (source-cell block 95% interval +0.02410 to +0.13913). This is a restricted geographical forest sample, not a global trend or a biological migration response.

In rolled-forward held-out target years, adding completed same-year southern green-up to a target-calendar model reduced squared prediction error by 74.54% in 2002–2009 and 59.94% in 2010–2017. The difference in relative skill (-0.14608, interval -0.31459 to +0.02572) was uncertain; absolute prediction errors improved in both models. This is a source-event oracle comparison, not necessarily information an animal can use.

With the illustrative seven-day lead and seven-day reporting-delay gate, apparent relative squared-error savings fell to 0.1606% and 22.0806%. Of the latter 22.0806 percentage points, 21.9909 were attributable to rows classified *after scoring* as decisions after actual target onset. Only 0.0896 percentage points came from pretarget rows. This identifies a chronology problem with interpreting the apparent gain as prediction before the target; the post-scoring classification is not an operational real-time policy. A separate binary event-not-yet-observed sensitivity did not establish a change between periods (late-minus-early skill -0.11014, interval -0.25963 to +0.02295).

The radar study supplies an independent chronology context, not a replication of this forecast design. Of 828 complete station-years, 455 had green-up before the 10th-percentile passage date and 739 before the median passage date (logical fractions 54.95–55.07% and 89.25–89.37%, allowing the one unknown record). Yet adding mean green-up to the site/year/temperature baseline did not improve held-out mean year-MSE: 7.164544 to 7.184004 days squared, incremental saving -0.019460 (year-bootstrap interval -0.095294 to +0.049598). Satellite event ordering therefore does not establish perception or added predictive value for actual migratory decisions.

### 4.2 Within-individual behavior is associated with initial phase error

Within repeatedly observed mule deer, later departure phase was associated with shorter stopovers (slope -0.689113 stopover days per day of later phase; animal-bootstrap interval -0.815051 to -0.572581). A ten-day later phase was associated with 6.89 fewer stopover days. All eight leave-one-year-out coefficients were negative. The later source cohort accounts for 97.962% of identifying exposure variation.

This strengthens the within-individual robustness of the published compensation association, not the discovery of compensation itself. A same-sample screen for a joint calendar-day and departure-phase coefficient had VIF 16.53673, exceeding the frozen maximum of 10; the joint coefficient was not fitted. Therefore a calendar schedule cannot be ruled out. Descriptive phase convergence in the published 152 animal-years/72 individuals is compatible with correction, but neither perceived error nor fitness-scale recourse is identified by these observations.

### 4.3 Interacting partners differ in seasonal response

Published Burgess et al. (2018) bird–caterpillar timing slopes below unity (0.510, 0.515, 0.348 for blue tit, great tit, pied flycatcher in the source reconstruction) and Samplonius et al. (2018) resident–migrant laying-date separation (0.94 days per decade across 10 nest-box schemes) motivate the predicted asymmetry. These are published interaction-level timing patterns, not novel PAYOFF results or fitted controller retentions.

The provisional source-restricted E6 comparator finds a long-minus-short migration temperature-response contrast of +0.525253 days/degree C (444 published effects, 269 species, 13 crossed studies; study/species two-way clustered 95% interval +0.224283 to +0.826223). All 13 study-omission estimates are positive. The positive contrast is consistent with weaker advance in long-distance migrants; cue location, physiology, photoperiod and species composition remain possible explanations. This post-open comparison is not direct evidence for information distance and is pending full provenance review before main-text use.

## 5. Discussion

The key distinction is not between an informed and an uninformed species, but between what can be inferred at a particular stage and what can still be changed at that stage. The environmental module demonstrates how a large statistical relationship can lose its interpretation as a forecast when the action deadline is imposed. The animal module shows that final matching can hide behavior associated with initial timing, while also exposing the difficulty of separating phase information from a calendar schedule. Neither result by itself identifies the proposed mechanism.

The framework yields three discriminating ecological predictions. For equivalent cue trajectories, organisms with independently measured faster loss of feasible correction should commit earlier under the specified model conditions. Where downstream adjustments are possible, large initial phase error need not imply large final error; loss of an adjustment option should reveal previously hidden vulnerability. Finally, under shared forcing, partner differences in conditional-mean retention can generate relative timing divergence even if both actors track the environment in the same direction. Tests of the last prediction require a common phase coordinate and measured interaction windows, not just taxonomy or a shared climate covariate.

Plants and pollinators, resident and migrant birds, and consumers and seasonal resources provide candidate contrasts. Local sensing and mobile recourse are independent axes, not fixed properties of all members of a taxon. Flowering duration, repeated flower production and phenotypic plasticity can provide plant recourse, whereas energetic constraints can restrict mobile animals. The model predicts that these dimensions, and their asymmetry across partners, matter more directly than movement distance alone. The fitness consequence remains conditional on actual costs and interaction benefits; tighter timing is not always individually optimal.

The principal empirical limitation is the absence of a same-decision-unit measurement of precommitment cue reliability, remaining feasible response and subsequent loss or fitness. The existing frozen barnacle-goose V7 analysis remains unestimated; source historical annual GDD-jerk onset and authoritative region assignments are missing. Route-stage geometry \(U\) is not fitness-scale \(r\). The registered wigeon predictive-connectivity-by-incoming-phase test did not support the proposed effect. The historical hysteresis prerequisites failed, and Scottish bird–prey results did not establish hatch-window mass specificity beyond sampled seasonal abundance. These outcomes are not promoted or omitted to manufacture confirmation.

A direct test should vary cue reliability and remaining response opportunity independently while holding reward and decision state fixed. A proposed colony-randomized bumblebee assay (#412) specifies such a factorial design but has no observed colonies or biological results. A positive interaction on a measured loss endpoint could discriminate joint cue/recourse dependence in that assay; natural migration or partner-network fitness would still require distinct validation. The existing theory-led article is therefore defensible as a conditional framework with illustrative and limiting evidence, not as a validated universal mechanism.

## 6. Conclusion

Seasonal adaptation depends on knowing the relevant environmental state before the last useful opportunity to respond. The same observed timing can conceal distinct initial errors and corrective pathways. By separating cue accuracy, observation timing, retained actionability and interaction coordination, the framework specifies when these pathways could generate or prevent mismatch, and identifies the measurements necessary to test them.

## Selected literature and source identity

- Amaral et al. 2025. Shifting gears in a shifting climate: birds adjust migration speed in response to spring vegetation green-up. https://doi.org/10.1111/ddi.70033 (satellite-only forest source for this draft).
- Adams et al. 2025. Ecology. https://doi.org/10.1002/ecy.70110; data https://doi.org/10.6084/m9.figshare.26050390.v2.
- Bauer et al. 2008. The relevance of environmental conditions for departure decision changes en route in migrating geese. https://doi.org/10.1890/07-1101.1.
- Burgess et al. 2018. Tritrophic phenological match–mismatch in space and time. https://doi.org/10.1038/s41559-018-0543-1.
- Dossman et al. 2023. Migratory birds with delayed spring departure migrate faster but pay the costs. https://doi.org/10.1002/ecy.3938.
- Kölzsch et al. 2015. Forecasting spring from afar? https://doi.org/10.1111/1365-2656.12281.
- Liu et al. 2026. Journal of Animal Ecology. https://doi.org/10.1111/1365-2656.70395 (stopover/phenological sensitivity prior-art boundary; verify complete citation before submission).
- Ortega et al. 2023. Migrating mule deer compensate en route for phenological mismatches. https://doi.org/10.1038/s41467-023-37750-z.
- Samplonius et al. 2018. Phenological sensitivity to climate change is higher in resident than in migrant bird populations among European cavity breeders. https://doi.org/10.1111/gcb.14160.
- Torstenson and Shaw 2025. Strength of seasonality and type of migratory cue determine the fitness consequences of changing phenology for migratory animals. https://doi.org/10.1111/oik.10862.
- Usui et al. 2017. Temporal shifts and temperature sensitivity of avian spring migratory phenology: a phylogenetic meta-analysis. https://doi.org/10.1111/1365-2656.12612.

## Development evidence links (not journal-facing)

[#335](https://github.com/zuizui0223/payoff/pull/335) corrected V4 mathematics; [#401](https://github.com/zuizui0223/payoff/pull/401) theory–evidence ledger; [#396](https://github.com/zuizui0223/payoff/pull/396) geographical MODIS; [#397](https://github.com/zuizui0223/payoff/pull/397) oracle forecast; [#398](https://github.com/zuizui0223/payoff/pull/398) availability; [#399](https://github.com/zuizui0223/payoff/pull/399) censored status; [#405](https://github.com/zuizui0223/payoff/pull/405) within-study E6; [#407](https://github.com/zuizui0223/payoff/pull/407) prior art; [#412](https://github.com/zuizui0223/payoff/pull/412) prospective assay; [#413](https://github.com/zuizui0223/payoff/pull/413) deer FE; [#414](https://github.com/zuizui0223/payoff/pull/414) calendar-phase support failure; [#415](https://github.com/zuizui0223/payoff/pull/415) radar prediction; [#416](https://github.com/zuizui0223/payoff/pull/416) median chronology; [#417](https://github.com/zuizui0223/payoff/pull/417) passage window; [#424](https://github.com/zuizui0223/payoff/pull/424) V7 source-only access status.

**Submission HOLD.** This is a fresh synthesis of existing receipts and source manuscripts; no new primary model, source-data replay, package rendering, author review, permission review or anonymous archive verification is claimed. No original GPS/individual records, eBird-dependent input or new outcome data are added. The original V2/V3/V4, all freezes and registered outcomes remain unchanged.
