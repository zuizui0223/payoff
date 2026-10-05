# PAYOFF-B V4 adversarial manuscript audit — 2026-10-05

Status: **POST-V8 INTERNAL REVIEW; DOES NOT ALTER FROZEN RESULTS**

## Bottom line

The V8 result closes the proposed high-impact "climate change broadly degrades
migration information" route. It does not close the integrated paper.

The strongest remaining paper is an **American Naturalist-style
theory-plus-natural-evidence paper** centered on one question:

> **Why can better environmental information fail to produce better seasonal
> tracking?**

The answer must be stated narrowly:

> Environmental information has ecological value only while biologically
> consequential actions remain available. Cue quality and actionability are
> therefore separate state variables.

The candidate mathematical contribution is not generic value of information,
optimal stopping, sequential migration decisions, or the claim that constraints
matter. Those all have clear prior art.

The narrow contribution that survives the prior-art screen is the
seasonal-ecological specialization in which:
- cue reliability q(t) can improve monotonically;
- retained actionability r(t) can decline;
- actionable information value r(t)V_A(q(t)) can therefore peak at an
  intermediate stage;
- under the declared exponential special case the peak has the closed form
  t* = log(1 + alpha/beta)/alpha;
- two actors exposed to the same information trajectory can commit at
  different times solely because their actionability decays at different rates;
- with a positive deadline cost, information can have a finite entry–peak–exit
  use window while cue accuracy continues to improve.

This is the paper's theory headline.

## What V8 now contributes

V8 is not evidence that actionability loss caused mismatch.

It is a **falsification layer** against a simpler external-information story.

The prospective environmental hypothesis predicted broad degradation of
source–destination spring predictability. Instead, the frozen point pattern is
strongly positive and remains positive across the existing scale/window
sensitivities.

The registered change-on-change prediction also failed: larger connectivity
gains did not produce larger reductions in bird mismatch. Structural nulls
show that the raw positive slope cannot be interpreted as a biological
worsening response.

Therefore the licensed use of V8 is:

> Broad loss of this environmental predictive coordinate is not a sufficient
> explanation for persistence of mismatch in this sampled system, and improving
> the coordinate did not guarantee improved realized tracking.

Do not turn this into:

> actionability caused the missing improvement.

That mechanism remains supplied by theory and separate natural evidence.

## Main manuscript problem

The current V4 has too many co-equal ideas:
- value of information/actionability balance;
- Bayesian phase estimation;
- proportional control;
- phase-retention decomposition;
- timer–controller serial architecture;
- pairwise mismatch decomposition;
- network Laplacian extension;
- coordination-game irreversibility;
- prediction/correction substitution;
- variance-funnel identification;
- multiple bird, ungulate and interaction examples.

All are individually defensible, but together they obscure the one result a
reader should remember.

## Recommended main-text hierarchy

### Core theory — keep in main text

1. **Information–actionability balance**
   - N(t) = r(t)[S q(t) - B] - C(t)
   - exact interior balance;
   - exponential t*;
   - finite information-use window.

2. **Minimal downstream phase bridge**
   - e_(t+1) = phi_t(e_t - u_t) + w_t;
   - lambda = phi(1 - hK);
   - enough to explain why correction opportunity matters after commitment.

3. **Minimal two-actor consequence**
   - Delta_n decomposition into inherited entry mismatch and
     controller-generated mismatch.

These three pieces answer one ecological question.

### Supporting theory — move to supplement or one compact Discussion paragraph

- full Gaussian filtering derivation;
- variance-funnel identification;
- prediction/correction portfolio substitution;
- network Laplacian generalization;
- full coordination-game derivation.

The coordination result can stay conceptually important, but it should not
compete with the information–actionability theorem for the headline.

## Recommended empirical hierarchy

### Figure-level evidence

1. **Prospective migratory-bird falsification**
   - environmental predictive connectivity change;
   - no registered mismatch improvement transfer;
   - structural-null audit.

2. **Mule deer mechanism anchor**
   - predeparture condition associated with entry timing;
   - signed phase associated with downstream speed/stopover;
   - phase convergence;
   - retain all existing claim ceilings.

### Text-only or supplement

- long-vs-short migrant temperature-response reconstruction;
- godwit buffering;
- pink-footed goose stagewise information;
- snow-goose carryover/buffering;
- redstart compensation cost;
- resident–migrant interaction asymmetry;
- failed hysteresis/reversal lanes;
- wigeon null.

These systems show breadth, but breadth is not the paper's novelty.

## Prior-art pressure

Bauer et al. (2020) already model environmental predictability, intermediate
stopovers as information sources, and better timing under higher
predictability.

Torstenson & Shaw (2025) already distinguish cue accuracy from cue efficacy
and show that environmentally responsive cues are not universally superior.

General ecological value-of-information and optimal-stopping logic is also
established.

Therefore wording such as:
- "information matters";
- "more information is not always better";
- "constraints limit phenological adjustment";
- "migration is sequential";
cannot be presented as the novelty.

The novelty claim should be tied to the exact q(t) × r(t) seasonal geometry
and its actor-specific desynchronization consequence.

## Current overclaim to remove

The current abstract says the combined results "show why" predictability alone
does not determine tracking and that adaptation "depends on when organisms can
act and how much downstream correction remains possible."

The bird data do not identify that mechanism.

Safer:

> The bird result rejects broad information degradation as a sufficient
> explanation in this system. We then show theoretically how improving
> information can fail to improve tracking when actionability declines, and use
> individual-level movement evidence to establish that downstream correction is
> biologically available and phase-dependent.

## Stronger headline

Preferred title:

**Improved environmental predictability need not improve seasonal tracking**

Alternative:

**When better environmental information fails to improve seasonal tracking**

Avoid making "timer–controller architecture" the title. The architecture is
the explanation, not the biological question.

## One-sentence claim

> Seasonal adaptation depends on actionable information: environmental
> predictability can improve while the opportunity to convert information into
> timing correction disappears.

The second clause is a theoretical mechanism, not a direct interpretation of
the bird data.

## Journal ceiling

With the present evidence:
- **American Naturalist**: credible first target if the manuscript is compressed
  to the single information–actionability question.
- **GEB / Oikos**: strong fallback routes.
- **Ecology Letters / PNAS / Nature Ecology & Evolution**: the present V8
  outcome does not provide the broad positive empirical discovery previously
  envisioned. Reaching that tier would require a direct, independent natural
  test of q(t) and r(t), ideally across stages or systems.

## Remaining critical audit before V8 enters the main figure

The strong positive V8 environmental contrast currently uses unique-pair
bootstrap uncertainty. Before using "strengthened strongly" in the abstract,
audit:
- source-cell and target-cell reuse;
- coarse spatial dependence;
- calendar-year leverage;
- early/late remote-sensing support;
- range-column semantics.

That audit is separately locked and currently determines whether V8 remains a
main-text falsification or is demoted to dependence-sensitive supporting
evidence.
