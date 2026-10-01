# PAYOFF-B prospective extension: stagewise information and signed recourse

Date: **2026-10-01**  
Status: **prospective theory/evidence extension; does not retune the frozen GEB Paper 2 submission**

## Bottom line

The current Paper 2 already contains an exact effective-deadline model for
**late commitment followed by downstream compensation** and an exact hidden-
state comparison between **precommitted compensation** and **perfectly adaptive
compensation after the state is known**.

The current Paper 2 does **not** yet contain a full model in which:

1. phase error can be either early or late and recourse can act in both
   directions;
2. the actor acquires only partial/noisy information while moving;
3. repeated route stages progressively reveal the seasonal state while the
   feasible action set shrinks.

This prospective branch implements (1) and a one-signal version of (2). A full
multi-stage Bellman recursion remains unimplemented.

## 1. Existing implementation that already supports the new framing

Current exact code:

    src/compensated_information_deadline.py

The frozen model uses

    D_eff = J(delta) + min_c [K(c)+M(delta-c)].

It already establishes:

- raw delay need not rank effective deadline cost;
- greater compensation capacity weakly lowers effective cost when compensation
  is worthwhile;
- direct waiting cost can survive full timing recovery;
- two actors with different effective costs have different cue-use thresholds;
- raw-delay order can reverse cue-threshold order;
- if a future state H affects compensation, state-contingent compensation after
  H is learned has weakly lower expected cost than choosing one compensation
  plan before H is known.

The last result is already a perfect-information recourse result:

    E[min_c L(c,H)] <= min_c E[L(c,H)].

So the latent-state / "Schroedinger's spring" intuition is already present at
the endpoints **no later information** versus **perfect later information**.

## 2. Gap A — signed recourse

The old linear compensated-deadline implementation only repairs positive delay.

The prospective signed model defines a phase error e:

- e > 0: late;
- e < 0: early.

Recourse is signed:

    -C_delay <= c <= C_advance.

Interpretation:

- c > 0: speed up / compress stopovers / advance progress;
- c < 0: slow down / extend stopovers / wait.

With

    L(c,e) = J + kappa |c| + mu |e-c|,

the exact optimum is zero correction when kappa >= mu and otherwise the
projection of e onto the feasible signed-recourse interval.

Thus the same optimization principle predicts both:

- late actor -> faster / shorter-stopover correction;
- early actor -> slower / longer-stopover correction.

This is the mathematical form of the "late Shinkansen catches up; early
Shinkansen can use schedule slack" analogy.

Implementation:

    src/stagewise_information_recourse.py

## 3. Gap B — noisy information acquired en route

Let H be an unobserved seasonal state, Z an en-route signal, and a a recourse
action still available after observing Z.

Define no-signal Bayes risk

    R0 = min_a sum_h P(h)L(a,h).

After a noisy signal,

    RZ = sum_z min_a sum_h P(h)P(z|h)L(a,h).

The value of en-route information is

    VZ = R0 - RZ >= 0.

This interpolates between the existing endpoints:

- no useful en-route signal -> precommitted risk;
- perfect state revelation -> adaptive/perfect-information risk.

## 4. Exact irreversibility result

If the feasible recourse set has collapsed to one action before the signal
arrives, then

    VZ = 0

for every signal quality.

The information can become perfectly accurate while having zero behavioral
value because no state-contingent response remains feasible.

This is the exact mathematical content behind the "Schroedinger's spring"
analogy:

> learning the state later is useful only if enough optionality remains when
> the box is opened.

For the symmetric two-state binary example with prior 1/2, wrong-state loss W,
and cue accuracy q in [1/2,1], if both state-matched actions remain available,

    R0 = W/2,
    RZ = W(1-q),
    VZ = W(q-1/2).

If only one action remains feasible,

    RZ = R0 = W/2,
    VZ = 0.

This is established generic value-of-information / recourse logic, not a claim
of generic mathematical novelty.

## 4.5 Information-actionability envelope

A continuous reduced form makes the information/irreversibility tradeoff
explicit.

Let r in [0,1] be the fraction of full state-contingent recourse still
available when the signal is observed. In the symmetric binary problem,

    R0 = W/2,

and mixing the fully actionable cue-following regime with the irreversible
regime gives

    R(q,r)
      = (1-r) W/2 + r W(1-q),

so

    V(q,r)
      = r W (q - 1/2).

Therefore:

- increasing q raises information value when r is fixed;
- increasing r raises information value when q is fixed;
- perfect information has zero behavioral value when r=0;
- if q rises while r falls, V can peak at an intermediate stage.

Exact witness:

    stage:                  1      2      3      4
    cue accuracy q:       0.55   0.75   0.95   1.00
    recourse r:           1.00   0.80   0.30   0.00
    V/W:                  0.05   0.20   0.135  0.00

The state is known most accurately at the final stage, but the information is
then behaviorally worthless because no optionality remains.

This is the cleanest exact form of the "Schroedinger's spring" idea in this
prospective model. It is still classical value-of-information logic; the
ecological question is whether real migration and phenological systems occupy
different trajectories through the (q,r) plane.

## 4.55 Actionable-information coordinate and pairwise stage divergence

The binary reduced model admits a compact normalized coordinate

    A = r (2q - 1),

with A in [0,1]. The gross information value is

    V = (W/2) A.

This is useful because q and r can move in opposite directions.

For two actors exposed to the same improving cue sequence

    q = [0.60, 0.80, 0.95],

consider different remaining-recourse trajectories:

    actor 1: r = [1.00, 0.70, 0.20]
    actor 2: r = [1.00, 0.90, 0.80].

With zero additional waiting cost, the reduced-form best commitment stages are

    actor 1 -> stage 2
    actor 2 -> stage 3.

Thus a shared environmental-information trajectory can generate different
optimal commitment stages solely because recourse is lost at different rates.

This is the stagewise analogue of the existing Paper-2 asynchronous uptake
result. It remains a declared binary reduced-form consequence, not an empirical
claim that any current taxon pair has measured q and r on this scale.

## 4.6 Finite-horizon commitment result

The prospective implementation now also solves an exact binary finite-horizon
route problem:

1. at stage t the actor observes a cue with reliability q_t;
2. Bayes-updates the probability of EARLY versus LATE destination spring;
3. either commits using an action still feasible at stage t or pays a waiting
   cost and proceeds;
4. the feasible action set can shrink at later stages.

The Bellman recursion is evaluated exactly over all reachable cue histories.

Two limiting cases are recovered:

- with full recourse at every stage and zero waiting cost, the actor waits for
  the most informative future cue;
- if later stages lose state-contingent actions, an earlier imperfect cue can
  be optimal even when a later cue is perfect.

Therefore "wait until you know the state best" is not a general ecological
rule. The relevant quantity is the joint path of information quality, direct
waiting cost and remaining actionability.

This result is a dynamic-programming realization of the one-shot
information-deadline logic. Generic Bayesian optimal stopping is established
prior art; the prospective ecological contribution would have to come from a
distinctive prediction about biological trajectories through this state space.

## 5. What is now supported naturally

### 5.1 Both directions of migratory recourse — strong support

Ortega et al. (2023), Nature Communications 14:2008,
DOI 10.1038/s41467-023-37750-z:

- 72 adult female mule deer over 152 animal-years;
- early migrants started about 30 d ahead of peak IRG;
- late migrants started about 20 d behind;
- late migrants moved about 2.5x faster;
- late migrants spent about 72% less time on stopovers than early migrants;
- migration-end timing was much more compressed than migration-start timing.

This supports the qualitative signed-recourse mapping:

early -> slower / longer stopover  
late -> faster / shorter stopover

It does not estimate the prospective model's kappa, mu, or capacities on a
common fitness scale.

### 5.2 Early departure can be absorbed by later waiting — direct avian support

Conklin, Lisovski & Battley (2021), Nature Communications 12:4780,
DOI 10.1038/s41467-021-25022-7:

- bar-tailed godwit departure from New Zealand advanced by about six days over
  2008-2020;
- earlier departure did not produce earlier Alaska arrival or breeding;
- prolonged Yellow Sea stopovers absorbed the advance.

This directly supports the biological existence of an
**early-departure / later-waiting** strategy, but does not prove that individuals
depart early *in order to* acquire later information.

### 5.3 En-route cue updating — direct avian support

Bauer, Gienapp & Madsen (2008), Ecology 89:1953-1960,
DOI 10.1890/07-1101.1:

- pink-footed geese used different environmental information at successive
  route stages;
- local accumulated temperature at stopovers informed advancement of spring;
- birds adjusted northward progression accordingly.

This supports the biological premise that migration can be a sequential
information-acquisition process.

It does not by itself identify the Bayes-risk quantities in the prospective
model.

### 5.4 Delayed departure followed by faster migration with fitness cost — support

Dossman et al. (2023), Ecology 104:e3938,
DOI 10.1002/ecy.3938:

- about 10 d later departure;
- about 43% faster migration;
- about 6.3% lower apparent annual survival.

This remains a compensation-with-cost bridge, not a direct information-waiting
test.

## 6. Plant-pollinator comparison: what is and is not supported

The existing E7 source screen identifies multiple local interaction systems
where partners respond differently to temperature, including cases where the
identity of the more temperature-responsive partner reverses.

The strongest directly comparable published example currently in the repo is
Kharouba & Vellend (2015), Journal of Animal Ecology,
DOI 10.1111/1365-2656.12373:

- 166 butterfly-plant associations;
- 61 butterfly species and 54 plant species in the same-spring comparison;
- plant flowering was on average 5.70 +/- 1.03 d/C more temperature-sensitive
  than butterfly flight in that comparison;
- partner sensitivities were not correlated.

This supports:

> local access to the same seasonal environment does not guarantee matched
> phenological response.

It does **not** identify:

- plant versus pollinator recourse capacity;
- information distance for either partner;
- irreversibility cost;
- effective deadline cost;
- a causal migrant-versus-pollinator contrast.

The repo's E7 promotion gate therefore remains correct: no pooled
plant-pollinator meta-effect should be promoted until at least three independent
systems have a common estimand and defensible covariance/uncertainty.

## 7. Revised cross-system hypothesis that is currently defensible

Do **not** claim:

> migrants have more recourse than pollinators.

Current evidence does not identify that comparison.

A defensible prospective hypothesis is:

> systems differ along at least two separable axes: information available before
> commitment and recourse remaining after commitment.

Migration systems provide direct evidence for large post-commitment recourse
through speed and stopover adjustment, and for information acquisition en
route. Local plant-pollinator systems provide direct evidence that shared local
environmental exposure does not guarantee matched phenological sensitivity.

The untested prediction is that mismatch risk should be highest where
pre-commitment information is poor **and** post-commitment recourse is narrow.

## 8. Full current implementation gap

| component | status |
|---|---|
| fixed effective deadline D_eff | IMPLEMENTED_EXACT |
| raw-delay rank reversal | IMPLEMENTED_EXACT |
| actor-specific asynchronous q window | IMPLEMENTED_EXACT |
| direct nonrecoverable waiting cost J | IMPLEMENTED_EXACT |
| hidden H with perfect state-contingent later compensation | IMPLEMENTED_EXACT |
| hidden H with precommitted compensation | IMPLEMENTED_EXACT |
| cue-dependent dual-use compensation | IMPLEMENTED_EXACT |
| signed early/late recourse | PROSPECTIVE_IMPLEMENTED_THIS_BRANCH |
| one noisy en-route signal | PROSPECTIVE_IMPLEMENTED_THIS_BRANCH |
| irreversibility -> zero behavioral value after one action remains | PROSPECTIVE_IMPLEMENTED_THIS_BRANCH |
| continuous information-actionability envelope V=rW(q-1/2) | PROSPECTIVE_IMPLEMENTED_THIS_BRANCH |
| normalized actionable-information coordinate A=r(2q-1) | PROSPECTIVE_IMPLEMENTED_THIS_BRANCH |
| shared-cue / different-recourse commitment-stage divergence | PROSPECTIVE_IMPLEMENTED_THIS_BRANCH |
| repeated route signals / shrinking binary action sets | PROSPECTIVE_IMPLEMENTED_THIS_BRANCH |
| finite-horizon Bayesian Bellman recursion | PROSPECTIVE_IMPLEMENTED_THIS_BRANCH |
| continuous real-valued route/pace Bellman control | NOT_IMPLEMENTED |
| empirical natural D_eff | NOT_IDENTIFIED |
| empirical q_wait | NOT_IDENTIFIED |
| direct migrant-vs-pollinator recourse comparison | NOT_IDENTIFIED |
| natural pairwise asynchronous q window | NOT_IDENTIFIED |

## 9. Next exact extension if pursued

The next mathematically honest model is a finite-horizon dynamic programme with

    B_t(b_t,A_t)
      = min_{a_t in A_t}
        { C_t(a_t,b_t)
          + E[B_{t+1}(b_{t+1},A_{t+1})] },

where:

- b_t is the belief about the latent seasonal state;
- environmental observations update b_t;
- A_t is the recourse set still feasible at stage t;
- A_{t+1} can shrink as commitment becomes irreversible.

That recursion would connect the current one-shot deadline theorem to genuine
migration stages:

departure -> stopover -> route/pace update -> final approach -> settlement.

Do not add this to the frozen GEB manuscript unless it produces a genuinely new
ecological prediction not already implied by classical sequential VOI.
