# PAYOFF-B three-player Bayesian timing game and hysteresis

Status: **exploratory synthetic mechanism extension, 2026-09-26**

## Why the one-migrant threshold model is not enough

The binary migrant-versus-resident threshold result isolates an exact
information--coordination wedge, but destination residents are treated there as
state-following rather than strategic players.

This extension makes all three ecological actors strategic:

- flowering resource;
- local pollinator;
- migrant.

Each chooses an early/late policy as a function of a private cue about one
shared hidden spring state.

## Bayesian game

Each player has four pure cue-contingent policies:

    always late,
    follow cue,
    invert cue,
    always early.

Expected payoff combines:

    state mismatch cost
    +
    pairwise timing mismatch cost.

The implementation exactly enumerates all pure Bayesian Nash equilibria and
also runs sequential best-response dynamics. The second object is important
because PAYOFF distinguishes equilibrium value from historical accessibility.

## Canonical mechanism witness

The transparent witness uses:

    P(early spring) = 0.40

flower and local pollinator:
    cue accuracy = 0.90
    false-early cost = 1.00
    missed-early cost = 0.25
    interaction strength = 0.50

migrant:
    cue accuracy = varied from 1.00 down to 0.50 and back
    false-early cost = 2.00
    missed-early cost = 1.00
    interaction strength = 0.50.

These values are mechanism probes, not estimates for named taxa.

## Information-triggered coordination collapse

Initialize all three players at

    follow cue | follow cue | follow cue.

Under descending migrant cue reliability, sequential best responses retain that
profile through q=0.72 in the canonical grid.

At q=0.71, the profile collapses to

    always late | always late | always late.

Thus a change in the information quality of one mobile partner can trigger a
collective timing-regime shift in actors whose own cue quality has not changed.

## Hysteresis under information recovery

Now restore migrant cue reliability from q=0.50 back toward q=1.00 while using
the previous endpoint as the initial condition at each step.

At full migrant information, the historical path does **not** return to the
original all-following equilibrium. The retained endpoint is

    always late | always late | follow cue.

At q=1.00 both this history-locked profile and

    follow cue | follow cue | follow cue

are pure Bayesian Nash equilibria, but the latter has higher expected joint
payoff in the canonical witness:

    all-follow joint payoff ~= -0.33
    history-locked joint payoff ~= -0.60.

Therefore temporary information degradation can leave a persistent coordination
scar after the information itself has recovered.

## Candidate ecological conclusion

The candidate conclusion is stronger than generic phenological mismatch:

> A transient loss of predictive connectivity for one migratory partner can
> tip an interacting seasonal system into another self-consistent timing
> regime, and restoring the original information need not restore the original
> phenology.

This is an **information-triggered coordination hysteresis** mechanism.

The ecological surprise is that the species whose local cues never degraded
can remain shifted because partner-dependent payoff changes the basin of
attraction.

## Relation to existing PAYOFF-B mechanisms

The current programme now contains three distinct barriers:

1. **capacity barrier** — timing has finite range and movement must re-enter;
2. **known-state coordination barrier** — both partners know a better joint
   strategy exists, but unilateral moves are selected against;
3. **partial-information coordination barrier** — uncertain pre-commitment can
   trigger a switch between self-consistent timing regimes, with hysteresis
   after cue recovery.

These must not be collapsed into one generic mismatch mechanism.

## Prior-art boundary

Incomplete-information coordination and global games are established game
theory. Migration ecology already recognizes that migrants must anticipate
conditions at distant destinations and that useful departure cues depend on
environmental connectivity. Climate-driven informational mismatch has also
been proposed previously.

Accordingly, novelty cannot rest on "Bayesian games exist" or "migrants have
imperfect information." The candidate contribution is the ecological coupling
of:

    remote cue reliability
    x interaction-dependent timing payoff
    x historical accessibility
    -> phenological regime shift and hysteresis,

with a direct decomposition against the independently implemented
known-state PAYOFF-B coordination barrier.

## Next empirical discriminator

The most useful empirical axis is no longer simply migrant distance.

For a migratory interaction, estimate year-specific or route-specific
predictive connectivity:

    departure-site cue
    -> future destination spring / resource phase.

The model predicts nonlinear timing changes near cue-reliability thresholds and
history dependence after temporary predictability loss, even when destination
warming magnitude itself changes smoothly.

## Claim ceiling

The present result is a synthetic witness. It does not establish:

- that natural flower--pollinator--bird triplets follow the canonical payoff
  numbers;
- that a real system has crossed the q=0.71 threshold;
- that cue reliability has historically recovered while phenology stayed
  locked;
- that sequential best response is the only appropriate evolutionary dynamic.

Those are empirical and robustness targets, not current conclusions.
