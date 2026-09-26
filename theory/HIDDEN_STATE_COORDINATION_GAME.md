# PAYOFF-B hidden-state coordination game

Status: **new exploratory theory lane, 2026-09-26**  
Scientific role: candidate reframe of the integrated PAYOFF-B ecology paper.  
Evidence boundary: synthetic theory only; no named-system cue reliability is claimed.

## 1. Ecological question

A local plant and a local pollinator can often respond to the same local spring
conditions. A long-distance migrant must instead make a departure or movement
decision before it directly observes conditions at the destination.

The important asymmetry is therefore not only response capacity. It is
**information at the time of commitment**.

The informal "Schrodinger's cat" intuition is useful, but the formal model is
not quantum. It is a **Bayesian coordination game with a hidden environmental
state**.

The focal question is:

> Can a viable coordinated climate response exist, and even be a
> full-information Nash equilibrium, while a migrant rationally chooses not to
> make that response because destination conditions are insufficiently
> predictable at departure?

## 2. Hidden state and heterogeneous cues

The environmental state is binary:

```text
theta = 0  baseline/normal seasonal state
theta = 1  advanced/early seasonal state.
```

Species `i` receives private signal `s_i` with reliability

```text
r_i = P(s_i = theta).
```

Local responders can have `r_i` near one because the relevant environment is
experienced directly. A long-distance migrant may have lower `r_i` because
its departure cue is geographically separated from the destination state.

Each species chooses

```text
a_i = 0  retain baseline timing
a_i = 1  advance timing / depart early.
```

The decision is made from the cue before the hidden state is revealed.

## 3. Payoff

For species `i`, realized low-density growth is

```text
g_i =
    b_i
    - A_i 1[a_i != theta]
    - I_i partner_mismatch_fraction
    - C_i a_i.
```

where

- `A_i` is the abiotic cost of choosing the wrong seasonal action;
- `I_i` is the cost of losing synchrony with interaction partners;
- `C_i` is the asymmetric cost of advancing;
- `b_i` is baseline low-density growth.

This deliberately keeps response **capacity** separate from response
**information**. Both actions exist in the strategy set; the problem can arise
even when the correct action is physically available.

## 4. Exact migrant threshold

Suppose the other species observe the state and follow it:

```text
a_partner = theta.
```

Let

```text
q = P(theta=1 | migrant cue).
```

For the focal migrant, the expected payoff difference between advancing and
retaining baseline timing is exactly

```text
Delta U
= (2q - 1)(A + I) - C.
```

Therefore advancing is optimal only if

```text
q > q*
```

with

```text
q*
= 1/2 [1 + C/(A+I)].
```

This produces a genuine information threshold.

If advancing is costly, `C>0`, then `q*>1/2`: a weakly positive cue is not
enough. A species can receive a cue pointing toward early spring and still
rationally retain baseline timing.

For prior probability `pi=P(theta=1)`, the positive-cue reliability threshold
is obtained by combining this condition with Bayes' rule:

```text
P(theta=1 | s=1)
= pi r / [pi r + (1-pi)(1-r)].
```

At `pi=1/2`, the posterior after a positive cue equals `r`, so the critical
cue reliability is simply `r*=q*`.

## 5. Canonical three-species witness

The first canonical witness represents two local responders plus one
long-distance migrant.

Local responders:

```text
cue accuracy                 = 1.00
baseline growth              = 0.30
abiotic mismatch cost A      = 0.60
interaction mismatch cost I  = 0.20
advance cost C               = 0.05
```

Migrant:

```text
cue accuracy                 = 0.60
baseline growth              = 0.40
abiotic mismatch cost A      = 0.50
interaction mismatch cost I  = 0.40
advance cost C               = 0.30
```

with equal prior probability of baseline and advanced states.

For the migrant,

```text
q*
= 1/2 [1 + 0.30/(0.50+0.40)]
= 2/3.
```

But a positive cue with reliability 0.60 gives

```text
P(theta=1 | s=1)=0.60 < 2/3.
```

So the exact best response to perfectly state-following partners is

```text
always retain baseline timing.
```

This is not a failure to detect a positive cue. It is a rational response to a
cue that is not reliable enough to justify an asymmetric commitment cost.

## 6. Perfect information versus Bayesian equilibrium

With perfect information:

```text
theta=0 -> (0,0,0)
theta=1 -> (1,1,1)
```

are the joint-payoff optima, and the advanced-state profile `(1,1,1)` is also
the unique pure Nash equilibrium in the canonical witness.

Advanced-state low-density growth at `(1,1,1)` is

```text
local 1 = +0.25
local 2 = +0.25
migrant = +0.10.
```

The adaptive solution therefore exists and all three species are viable.

Under partial information, exhaustive enumeration of pure signal-contingent
strategies gives one Bayesian Nash equilibrium:

```text
local 1: follow cue
local 2: follow cue
migrant: always baseline.
```

Expected low-density growth becomes

```text
local 1 = +0.225
local 2 = +0.225
migrant = -0.050.
```

Even when the true state is advanced and all three species receive positive
cues, the equilibrium action profile is

```text
(1,1,0),
```

with realized growth

```text
local 1 = +0.15
local 2 = +0.15
migrant = -0.50.
```

Yet the viable `(1,1,1)` solution is present in the same payoff system.

This is the central new mechanism:

> **The adaptive solution exists, is viable, and is strategically stable once
> the state is known, but it is not rationally selectable before the state is
> known with the available cue.**

## 7. Deficit decomposition

The implementation separates three values.

### Oracle value

The state is known and actions can be coordinated.

### Full-information equilibrium value

The state is known but species act individually. The highest-welfare pure Nash
equilibrium is used.

### Partial-information equilibrium value

Species act from private cues. The highest-welfare pure Bayesian Nash
equilibrium is used.

In the canonical witness:

```text
oracle expected mean growth                 = 0.2666667
full-information equilibrium expected mean  = 0.2666667
partial-information equilibrium mean        = 0.1333333

coordination deficit = 0
information deficit  = 0.1333333.
```

Thus the loss in this witness is **purely informational**, not a consequence of
a missing adaptive action or a full-information coordination failure.

This is deliberately distinct from the existing PAYOFF-B unilateral
coordination barrier, where both species know the relevant payoff surface but
cannot reach the superior joint strategy through individually improving
mutations.

## 8. Three distinct PAYOFF-B failure modes

The combined programme can now separate:

```text
1. CAPACITY
   the required movement/phenology response does not exist within feasible
   bounds;

2. STRATEGIC ACCESSIBILITY
   a viable joint response exists, but unilateral change is selected against;

3. INFORMATION
   a viable and strategically stable response exists once the state is known,
   but the correct response is not inferable at the time of commitment.
```

These mechanisms should not be collapsed into one generic "failure to track."

## 9. Connection to migration and phenology

This changes the interpretation of phenological mismatch.

A standard account is

```text
warming
-> spring advances
-> species shift at different rates
-> mismatch.
```

The hidden-state game adds a different causal route:

```text
climate change
-> cross-site predictability changes
-> species possess unequal information about the same future state
-> state-contingent coordinated solution still exists
-> migrant cannot justify the correct commitment from its departure cue
-> realized mismatch / demographic loss.
```

The relevant climate variable is therefore not only the magnitude or velocity
of environmental change. It can also be the reliability of the mapping

```text
departure-site cue -> destination seasonal state.
```

## 10. Falsifiable ecological predictions

The new mechanism predicts that, holding response capacity constant:

1. long-distance migrants should show larger mismatch when cross-site cue
   predictability weakens, even if mean warming is unchanged;
2. local residents should track local phenology more tightly than migrants when
   resident cues are closer to the realized state;
3. mismatch should change sharply when cue reliability crosses the
   decision threshold, rather than varying only smoothly with warming;
4. en-route information updates should reduce the information deficit when
   decisions remain revisable;
5. systems with large irreversible advance costs should require more reliable
   remote cues before shifting early;
6. apparent "failure to adapt" can occur despite positive growth under the
   perfect-information coordinated action.

These are empirical predictions, not yet empirical results.

## 11. Relationship to the current temporal-buffering result

The temporal-buffering story remains useful but changes role.

```text
movement/phenology alternatives
-> multiple feasible response architectures
-> partner coordination determines strategic accessibility
-> hidden environmental state determines informational accessibility.
```

The stronger candidate headline is therefore not merely that timing delays
movement. It is:

> **Climate adaptation can fail even when a viable coordinated response exists,
> because interacting species must commit using unequal information about a
> future environmental state.**

An even sharper form for the migration case is:

> **The problem may be not failure to adapt, but failure to know what to adapt
> to before commitment becomes costly or irreversible.**

## 12. Claim boundary

This lane currently establishes only a synthetic theoretical possibility and
an exact threshold in the declared binary-state model.

It does not establish:

- that any named bird, plant, or pollinator system has the canonical parameter
  values;
- that the critical reliability is universally 2/3;
- that real cues are binary or conditionally independent;
- that migration departure is always irreversible;
- that local plants or pollinators have perfect environmental information;
- that climate change has already reduced a named cross-site cue correlation;
- that the existing 55-species dataset directly tests this information game.

The immediate empirical target is therefore **cross-site cue predictability**,
not another generic movement-speed correlation.
