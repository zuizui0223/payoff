# PAYOFF-B Bayesian timing phase diagram — preliminary robustness result

Date: **2026-09-26**  
Status: **exploratory synthetic robustness result; not yet promoted into the frozen integrated manuscript**

## Question

The canonical three-player witness showed that loss of predictive information by
one migrant can pull a flowering resource and local pollinator into another
timing regime, with history dependence after the migrant's information
recovers.

A single witness is not enough. This robustness map asks whether the effect
occupies a meaningful region of the declared game and, more strictly, when the
history-dependent endpoint is actually worse than another pure Bayesian Nash
equilibrium still available after full information recovery.

## Strict promotion criterion

A cell counts as **inefficient information hysteresis** only if all four
conditions hold:

1. with migrant cue accuracy 1.0, sequential best response from the all-follow
   state remains 'follow_cue | follow_cue | follow_cue';
2. reducing migrant cue accuracy causes at least one resident player to leave
   'follow_cue';
3. restoring migrant cue accuracy to 1.0 does not recover the original
   all-follow state;
4. at recovered full information, another pure Bayesian Nash equilibrium has
   strictly higher joint payoff than the historical endpoint.

Thus simple migrant mismatch, reversible switching, neutral path dependence and
baseline non-following states do not count.

## Declared grid

The robustness design crosses:

- local cue accuracy: 0.75 to 1.00 by 0.025;
- interaction strength: 0 to 1 by 0.025;
- migrant cue accuracy: 1.00 down to 0.50 and back to 1.00 by 0.01.

This gives 451 local-information x interaction cells and 51 migrant-information
levels in each direction.

## Preliminary deterministic enumeration

Of 451 cells, 391 begin in the required high-information all-follow state.

Within those 391 eligible cells:

- 221 show a resident cascade when migrant information degrades;
- 201 remain history-dependent after information recovery;
- 121 satisfy the strict inefficient-hysteresis criterion.

These are design frequencies, not estimates of prevalence in nature.

The canonical cell remains:

    local cue accuracy     = 0.90
    interaction strength   = 0.50
    cascade threshold      = migrant accuracy 0.71
    low-information state  = late | late | late
    recovered state        = late | late | follow
    better recovered BNE   = follow | follow | follow
    history-lock loss      = 0.27 joint-payoff units.

The qualitative canonical result also survives all six update orders: the
identity of the coordinate order changes, but the migrant is the only player
that resumes cue following while the two resident partners remain late.

## The new pattern: vulnerability is non-monotone in local information

The strict result is not strongest where local information is worst.

At local cue accuracy 0.95, 0.975 and 1.00, no resident cascade occurs anywhere
on the sampled interaction grid. Near-perfect local information is strong
enough for residents to resist the migrant's informational deterioration.

At lower local cue accuracies 0.75--0.80, cascades and history dependence are
common, but the recovered historical endpoint is not worse than the best pure
equilibrium under the strict joint-payoff criterion.

The inefficient hysteresis window appears at intermediate-high local
information:

| local cue accuracy | eligible | cascade | strict inefficient hysteresis | sampled interaction range for strict result |
|---:|---:|---:|---:|---:|
| 0.825 | 36 | 36 | 28 | 0.300--0.975 |
| 0.850 | 40 | 40 | 38 | 0.050--0.975 |
| 0.875 | 41 | 36 | 33 | 0.175--0.975 |
| 0.900 | 41 | 27 | 21 | 0.500--1.000 |
| 0.925 | 41 | 13 | 1 | 1.000 |
| >=0.950 | 41 each | 0 | 0 | none |

This produces a counterintuitive candidate prediction:

> **Seasonal interaction networks may be most vulnerable to a migrant's loss of
> predictive connectivity not when resident information is poorest, but when
> residents have good-but-imperfect local information and partner coupling is
> strong enough to change their best-response basin.**

## Ecological interpretation

The mechanism now has three separable stages.

1. **Information asymmetry.** The migrant must commit from a remote cue while
   residents have better destination information.
2. **Interaction cascade.** A decline in migrant cue reliability changes the
   payoffs of resident timing policies even though resident cue quality itself
   did not change.
3. **Coordination hysteresis.** After migrant information recovers, the former
   high-joint-payoff timing regime can again exist as an equilibrium without
   being reached from the historically displaced state.

The ecological novelty candidate is therefore not simply "migrants have poor
information." It is:

    transient loss of predictive connectivity in one mobile partner
    x interaction-dependent timing payoffs
    x multiple self-consistent timing regimes
    -> persistent community-level timing change.

## Relationship to the earlier PAYOFF-B story

The programme now separates three barriers:

- **capacity:** an adaptive response is physically exhausted;
- **known-state coordination:** a better joint response is known but
  unilaterally inaccessible;
- **partial-information coordination:** information loss changes which basin is
  reached before the state is fully knowable, and the historical basin can
  persist after information recovers.

The earlier temporal-buffering result remains useful as the capacity layer, but
the Bayesian coordination result is a stronger candidate for the ecological
headline because it predicts a regime shift and path dependence rather than
only finite buffering.

## Claim ceiling

The current map remains synthetic. In particular:

- the 121/391 fraction is not a natural frequency;
- the accuracy values are not estimates for a named bird or plant-pollinator
  system;
- sequential best response is one explicit accessibility dynamic;
- correlated resident cues, continuous timing actions and demographic feedback
  remain robustness targets;
- the empirical discriminator is predictive connectivity from the migrant's
  decision site to the future destination state, not migration distance alone.


## Prior-state sensitivity: a transition-window effect

The canonical local-information / interaction cell was also checked while
varying the prior probability of an early spring.

| prior early | resident cascade threshold | recovered state | better full-information equilibrium? | history-lock loss |
|---:|---:|---|---|---:|
| 0.20 | 0.87 | late | late | follow | no | 0 |
| 0.25 | 0.83 | late | late | follow | yes | 0.0225 |
| 0.30 | 0.79 | late | late | follow | yes | 0.105 |
| 0.35 | 0.76 | late | late | follow | yes | 0.1875 |
| 0.40 | 0.71 | late | late | follow | yes | 0.270 |
| 0.45 | none | follow | follow | follow | no lock | 0 |
| 0.50 | none | follow | follow | follow | no lock | 0 |

Thus the strict mechanism is also non-monotone in the environmental prior. It
is strongest in an intermediate regime where an early spring is plausible
enough that cue-contingent timing is worthwhile, but not yet common enough that
early action becomes effectively unconditional.

This suggests a second empirical discriminator: information-triggered
coordination failure should be most visible during environmental transitions,
not necessarily after the new seasonal state has become commonplace.
