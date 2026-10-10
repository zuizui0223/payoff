# PAYOFF-B ecological mechanism admission: separate information from environmental state

Date: 2026-10-10
Status: **PROSPECTIVE IDENTIFICATION CONTRACT — NOT AN EMPIRICAL CONFIRMATION**.
Branch basis: PR #322 annual BTBW prior-art benchmark; V3 / V7R / V8 / frozen V4 manuscript are unchanged.

## Decision after auditing the proposed Hoge Veluwe fitness continuation

**Do not present a new Hoge Veluwe laying-date ~ food-peak ~ recruitment regression as a PAYOFF-B discovery.**

1. Reed et al. 2013, Journal of Animal Ecology, DOI 10.1111/j.1365-2656.2012.02020.x, already analysed 37 years of individual great-tit phenology and showed within-/between-year differences in timing-related fitness and demographic responses. It explicitly defines individual mismatch as \`laying date + 30 - caterpillar peak\`, and explicitly cautions that the zero of this descriptive index is not a proven fitness optimum.
2. Visser et al. 2021, Proceedings B, DOI 10.1098/rspb.2021.1337, analysed 48 years (1973–2020) in the Hoge Veluwe, including individual recruit-based selection differentials and the caterpillar resource series. Their population mismatch definition is \`mean laying date + 33 - caterpillar peak\`; they report an initial increase followed by weakening of selection for earlier laying.
3. In that source, during one year \`mismatch_iy = laying_iy + (33 - caterpillar_peak_y)\`. With unrestricted year fixed effects, signed individual mismatch and calendar laying date are **exactly collinear**, so a regression cannot give them independent coefficients. Absolute mismatch and nonlinear response functions can vary within year, but do not solve the causal identification of an animal's cue belief or its unobserved fitness optimum.
4. Previously registered PAYOFF-B Hoge Veluwe African-cue × caterpillar-resource reversal **failed Gate B**: the segmented prespecified fit had pre-break slope +0.22790 and post-break +0.02693, not the required decline then recovery. Original Gate C partner-history outcome was deliberately not opened and must remain closed. Do NOT retune that result by reusing the great-tit recruitment file.
5. The 25-year BTBW analysis in PR #322 is a prior-art sanity check, not an independent demonstration of beneficial mismatch; lag-fledgling adjusted CI spans zero. The BTBW global and empirical workflows pass after import-skipping in the minimal runner.

## External ecological evidence: what is already known

| Study | Natural or manipulated coordinate | Direct finding | PAYOFF-B novelty constraint |
|---|---|---|---|
| Gienapp et al. (2006), Functional Ecology, doi:10.1111/j.1365-2435.2006.01079.x | Experimentally shifted food-experience during breeding and later lay dates | Prior experience can retune future timing; evaluating early-breeding fitness under supplementation is confounded | Do not claim that resource-experience learning or feedback is a new hypothesis |
| Samplonius & Both (2017), J Anim Ecol, doi:10.1111/1365-2656.12640; Dryad doi:10.5061/dryad.bs427 | Randomized advancing/delaying of resident tit hatching by subplot/year; migrant flycatcher pairing/settlement | Later-arriving females avoided pairing in delayed-phenology plots; males did not show a parallel settlement effect; males generally settled before hatch-cue revelation | Sex- and stage-dependent information availability and heterospecific timing-as-social-cue are already published |
| Samplonius & Both (2019), Current Biology, doi:10.1016/j.cub.2018.11.063 | Cross-species nest-site overlap/density, fatal interference | Seasonal overlap and tit density predict lethal encounters; mismatch can change competitor risk, not only resource reward | No novelty for “different timing changes competition mortality” alone |
| Salis et al. (2019), Dryad doi:10.5061/dryad.jh9w0vt6d | Manipulated perceived photoperiod | Earlier gonadal development did not imply earlier laying | Entry/development versus downstream realized timing are already distinguishable empirically |
| Both & Visser (2026), J Avian Biol, doi:10.1002/jav.03537; Dryad doi:10.5061/dryad.rxwdbrvq3 | Supplementary feeding and, in great tits, nest-box night temperature manipulation | Their two food supplement experiments had no laying-date effect; the additional night-temperature treatment affected great-tit laying | Food limitation alone is insufficient in those experiments, but heating combines physiological and environmental-cue changes. No novelty for either headline |

Publication-quality mechanism separation must exceed these findings; reproducing them cannot itself upgrade Paper 2.

## New ecology-first question

> **Does a species act upon a partner's seasonal state because it *learned something* about future ecology, or because the partner's real state changes its immediate opportunities and costs? Does the answer flip when the cue arrives after irreversible commitment?**

A simple correlation between cue and target, or even a manipulation shifting BOTH true state and available cues, cannot separate the mechanisms.

## Prospectively crossed intervention (a target for a new experimental dataset, not yet an available result)

Experimental unit: replicated independently randomized plot / territory / individual-choice unit, with animal and year blocking.

Independent factors:
- H (true state): experimentally shift the partner's actual reproductive or food-resource peak early vs late, without altering unrelated cue presentation where possible.
- S (perceived cue): provide a predeclared early vs late signal about that partner that is manipulated independently of H and separated from resource/thermal inputs.
- T (information timing): present that signal **before** the actor's still-reversible settlement/phenology decision vs **after** that same decision. Do not define timing using a retrospective outcome date.

Primary behavioural response A: predeclared *first still-reversible decision* (where/when settle, leave stopover, lay). Primary ecological outcome W: subsequent actual reproduction/survival/recruitment, not absolute phenological overlap alone.

Full 2 × 2 × 2 randomization (or an ethically feasible equivalent with documented independence) yields a \`state × signal × availability\` contrast; its observed effects remain study-/context-specific.

**Predeclared mechanism contrasts**
1. H_info: at fixed H, experimentally changing S influences predecision action but not the *already committed* action under postdecision delivery. The difference in \`S × T\` effect is the information-availability contrast. Its ecological value requires an effect on W conditioned by congruence of S and actual H.
2. H_direct_state: at fixed S, H influences behaviour or fitness even when cue arrives after commitment, consistent with exposure to true partner state / competition / thermal resource. There may be H × T interactions because sensitivity changes with developmental stage.
3. H_cost/fitness-optimal undertracking: partial seasonal overlap can remain when cue and true state are aligned, if the *causal fitness surface* peaks away from maximum overlap. No claimed optimum without W contrasts and independently specified admissible action sets.
4. H_clock: action follows a fixed photoperiod/seasonal program regardless of independent S changes (and independent H where direct exposure is excluded). A null S response alone is NOT proof of a fixed clock without manipulation power and cue perception checks.

**Necessary validity checks**
- Signal S must demonstrably be perceivable, biologically meaningful, but not independently move the true resource H or impose unmeasured thermal/energetic costs.
- Manipulating actual H must not automatically reveal S (or the independent treatment is compromised).
- Assignment before outcome; adherence and actual realization documented; analyze intention-to-treat first.
- Time T cannot be assigned based on the individual's future observed action: that would bias information-availability contrast.
- Randomize and analyze at the true manipulated cluster (not thousands of nests in a handful of plots as independent trials).
- No selective exclusion of animals who chose a different territory after learning.
- Group-by-treatment balance, minimal detectable fitness effect, assay power, and costs specified a priori.
- Correctly distinguish **information's effect on choice** from **accuracy's effect on fitness**; when S disagrees with H, the fitness penalty depends on whether following the cue creates a real mismatch with ecological opportunity.
- If S inevitably changes H, the design is only a state-plus-cue manipulation and the pure information effect remains NOT_IDENTIFIED.

## Specific game-theoretic ecological hypothesis: the same neighbour is a cue and a threat

Two different published results point to a **prospective interaction** rather than another generic mismatch slope: experimental tit phenology can influence later-arriving female flycatcher settlement (Samplonius & Both 2017), while actual tit density and temporal overlap can increase fatal interspecific encounters (Samplonius & Both 2019). The data are from distinct study designs: **do not pool their effects as a demonstrated single-system mechanism**.

A migrant considering a patch can rationally regard resident phenology as *simultaneously informative about resource quality and hazardous through competition*. Let the expected advantage of entering the patch rather than avoiding it be

    DeltaW(s,t,d) = B * E[Q | s,t] - C * d * p_overlap(t,s,H) - K(t),

where \`Q\` is patch quality (estimated from a cue with documented visibility), \`d\` is resident competitor density, \`p_overlap\` is the likelihood of an ecologically harmful encounter, and \`K\` is arrival/settlement opportunity cost. All coefficients and functions are prospective; **no coefficient is fitted from the two published papers**. For \`p_overlap>0\`, a simple attraction-to-avoidance threshold occurs at

    d_star = [B * E[Q | s,t] - K(t)] / [C * p_overlap(t,s,H)].

When \`d > d_star\`, avoidance can be fitness-optimal even if the signal is accurate and indicates good habitat. A cue increasing predictive accuracy need not increase attraction; its payoff value can change sign with the interaction risk. This is a hypothesis from a model combining two published biological effects, **not** a demonstrated threshold or a novel algebraic theorem.

**Distinctive preregisterable tests** (requires independent, prospectively sourced observations or manipulations):
- cue quality held constant: a predecision tit signal changes its effect on migrant settlement with independently measured tit density and overlap;
- density held constant: signal-access manipulation acts only while settlement remains reversible;
- evaluate **actual reproductive success and mortality** jointly, not only settlement odds (a convenient social cue could have a fitness penalty);
- apply calendar, contemporary local ecology and female arrival-order controls, plus plot/season-level assignment accounting;
- include the null that density alters preference directly and apparent cue-use is only immediate competitive avoidance;
- do not infer causal information use from an observational signal-by-density coefficient when cue and real competitor state covary.

A positive result would establish a system-specific **information-value sign reversal generated by an interacting competitor**, rather than merely another association between climate warming and phenological mismatch. The idea remains source-screened, not empirically tested in PAYOFF-B.

## Exact rank / identifiability guard

The simplest model \`E[A | H,S,T] = beta0 + betaH H + betaS S + betaT T + interactions\` requires independent manipulation of H and S to distinguish those coefficients. If the historical observational data have S=H for all units, then \`H\` and \`S\` design columns are identical and no regression can attribute their joint effect to information versus immediate ecology. Adding N or a more elaborate algorithm does not break this aliasing. More explicit saturated 2×2×2 rank checks are implemented in \`src/payoff_b_cue_state_rank.py\`.

## Source-admission verdict (do not open unnecessary old analyses)

| Existing dataset | H state manipulable | S independently manipulable | T independently manipulable | fitness W | end-to-end information-vs-state test |
|---|---|---|---|---|---|
| Hoge Veluwe 1973–2020, Visser 2021 | no | no | no | recruit count | **NO**; prior-art benchmark only |
| Dutch tit/flycatcher randomized hatching, Samplonius 2017 | yes | no (cue covaries with actual hatch) | no, revelation determined by hatching/arrival | pairing outcome, not direct lifetime fitness | **NO**; social cue benchmark |
| Feeding/heated nestboxes, Both & Visser 2026 | conditions manipulated | not independent from actual warmth/energetics | no | lay date outcome | **NO**; thermal-vs-food intervention anchor |
| Newly crossed H×S×T experiment | yes | yes | yes | required | **PROSPECTIVE CANDIDATE** |

## Paper-level stop rule

These prior studies establish components and are positive ecological context, but **PAYOFF-B has not identified a new causal mechanism in a natural system**. Do not reframe V8 (positive changes in cross-site correlations) as cue reliability available to birds, and do not claim V7R's information × recourse interaction positive (exact within-flyway p=0.56994). The existing theory-led V4 manuscript remains a conditional account; do not promote new Nature/Ecology Letters novelty from a source audit or a rank demonstration alone.

### References
- Reed et al. (2013) https://doi.org/10.1111/j.1365-2656.2012.02020.x
- Visser et al. (2021) https://doi.org/10.1098/rspb.2021.1337
- Gienapp et al. (2006) https://doi.org/10.1111/j.1365-2435.2006.01079.x
- Samplonius & Both (2017) https://doi.org/10.1111/1365-2656.12640; data https://doi.org/10.5061/dryad.bs427
- Samplonius & Both (2019) https://doi.org/10.1016/j.cub.2018.11.063
- Salis et al. (2019) https://doi.org/10.5061/dryad.jh9w0vt6d
- Both & Visser (2026) https://doi.org/10.1002/jav.03537; data https://doi.org/10.5061/dryad.rxwdbrvq3
