# PAYOFF-B prospective route-wise phase-control theorem

Date: **2026-10-02**  
Status: **prospective post-freeze Paper-2 extension; frozen GEB V2 unchanged**

## 1. Ecological question

Migration is not one departure decision followed by passive travel.  Animals
can observe new local conditions at successive route stages and can change
speed, stopover duration, route, or subsequent timing.

The motivating analogy is a train running toward a destination whose seasonal
"timetable" is not yet fully known:

> **a Shinkansen running toward Schroedinger's spring.**

The train analogy is used only as intuition.  The formal object is a sequential
feedback controller with a latent moving seasonal target.

The key ecological question is:

> At each route checkpoint, can an organism estimate whether it is early or late
> relative to the seasonal resource wave, and use the remaining recourse to
> reduce that phase error before the next checkpoint?

## 2. Signed phase state

Let

    e_t > 0  : actor is late relative to the local seasonal optimum
    e_t < 0  : actor is early.

At checkpoint t the actor does not necessarily observe e_t directly.  It has an
internal estimate

    ehat_t = E[e_t | I_t],

where I_t is the accumulated information available by that checkpoint.

A signed correction u_t has the ecological interpretation

    u_t > 0  : speed up / shorten stopover / advance progress
    u_t < 0  : slow down / lengthen stopover / delay progress.

The realized phase state evolves as

    e_(t+1) = phi_t (e_t - u_t) + w_t,

where

- phi_t is passive phase retention in the absence of active correction;
- w_t is change in the local seasonal target between checkpoints.

Thus even perfect correction at one checkpoint does not guarantee zero phase
error later when the resource wave itself shifts.

## 3. Exact phase-retention decomposition

Consider proportional feedback

    u_t = g_t ehat_t.

Under perfect phase estimation, no actuator clipping, and w_t=0,

    e_(t+1)
      = phi_t (1-g_t) e_t.

Therefore the segment-scale phase-retention coefficient is exactly

    lambda_t = phi_t (1-g_t).

This decomposition separates two processes that a raw lambda estimate conflates:

1. passive carry-over phi_t;
2. active feedback gain g_t.

Consequences:

- g_t = 0 gives lambda_t = phi_t: no active phase correction;
- 0 < g_t < 1 reduces retained phase error;
- g_t = 1 resets the current checkpoint error when w_t=0;
- g_t > 1 overshoots the current target and gives negative lambda_t when
  phi_t>0.

Therefore neither

    1 - |lambda|

nor lambda itself can be identified with "recourse", "control effort" or the
Paper-2 actionability coordinate r without an independently identified phi and
a biologically explicit actuator model.

This strengthens, rather than relaxes, the existing PAYOFF-B guard against
substituting phase-retention lambda for retained actionability.

## 4. The animal's "sense" as Bayesian phase estimation

A simple exact observation model is

    e_t ~ Normal(m_t, P_t)

and checkpoint cue

    z_t = e_t + nu_t,
    nu_t ~ Normal(0, R_t).

The posterior phase estimate is

    K_t = P_t / (P_t + R_t),

    m_t^+ = m_t + K_t (z_t - m_t),

    P_t^+ = (1-K_t) P_t.

The control-relevant "sense" is therefore not perfect knowledge of phase.  It is
a posterior estimate whose reliability improves when checkpoint cues are more
informative.

This is standard scalar Bayesian filtering, not a new mathematical result.

## 5. Exact one-checkpoint correction under uncertainty

Let correction u incur quadratic cost kappa u^2 and residual phase error incur
mu (e-u)^2.

Conditional on the posterior belief,

    E[L(u) | I_t]
      = kappa u^2
        + mu [ (m_t^+ - u)^2 + P_t^+ ].

Without actuator bounds, the optimum is

    u_t*
      = g* m_t^+,

with

    g*
      = mu / (kappa + mu).

Thus:

- the sign of optimal correction follows the estimated phase-error sign;
- stronger residual mismatch cost increases feedback gain;
- stronger correction cost decreases feedback gain;
- posterior variance contributes irreducible expected loss but does not change
  the unbounded one-step certainty-equivalent action.

With speed/stopover limits, the implemented action is the projection of u_t*
onto the feasible signed correction interval.

## 6. Connection to Schroedinger's spring

The future destination state can remain latent while route checkpoints improve
the estimate of seasonal phase.  But the value of that better estimate depends
on whether useful corrections remain feasible.

The route-wise controller therefore combines the two existing Paper-2 objects:

    information quality     -> quality of ehat_t
    remaining actionability -> feasible magnitude/direction of u_t.

The new interpretation is not "wait at the origin until spring is known."
Rather:

    move -> observe -> update phase belief -> correct -> move again.

Migration itself can therefore be an information-acquisition and
error-correction process.

## 7. Relation to the actionability-balance theorem

The continuous actionability theorem asks when better information is worth
waiting for as q(t) rises and r(t) falls.

The route-wise controller supplies the missing state dynamics:

    e_t
      -> information update
      -> u_t
      -> e_(t+1).

The two views are complementary:

- actionability balance determines **when information should be acted on**;
- route-wise phase control determines **how phase error changes after acting**.

A complete future model can make q_t, actuator bounds and control costs
checkpoint-specific and solve the joint partially observed control problem.

## 8. Falsifiable ecological predictions

The reduced controller generates predictions that are more specific than
"long-distance migrants track spring."

1. **Signed correction**
   Incoming late phase error should predict faster movement or shorter
   stopovers; incoming early error should predict slower movement or longer
   stopovers, conditional on remaining actuator capacity.

2. **Checkpoint convergence**
   Departure-date variance can be much larger than arrival-date variance if
   repeated feedback gains are positive.

3. **Actuator-loss effect**
   Removing or constraining stopover/speed/route recourse should increase
   retained phase error even if cue quality is unchanged.

4. **Intermediate information-use peak**
   Cue responsiveness can peak at an intermediate route stage when information
   improves but correction capacity is being lost.

5. **Overshoot diagnostic**
   Negative segment-scale lambda is compatible with gain above one in the
   simple proportional representation, but the myopic quadratic controller
   never chooses g>1.  Natural negative lambda therefore points to anticipatory
   control, a moving target, coordinate changes, or other non-myopic dynamics
   rather than proving "strong recourse" by itself.

## 9. Current natural anchors and boundaries

Published systems already motivate separate pieces:

- mule deer: late migrants can move faster and shorten stopovers;
- bar-tailed godwits: earlier departure can be absorbed by longer later
  stopovers;
- pink-footed geese: cue relevance changes among route stages;
- American redstarts: faster compensation after late departure can coexist with
  survival cost.

The existing three-taxon PAYOFF-B phase-retention receipt also records direct
segment-scale lambda estimates in mule deer, barnacle goose and Eurasian
wigeon.

These observations do **not** estimate the internal phase belief, feedback gain
g_t, passive retention phi_t, or the full route controller.  They are source
anchors for prospective tests, not direct validation of this decomposition.

## 10. Claim boundary

Generic Kalman filtering, feedback control, LQG/certainty equivalence and
optimal control are established prior art.

PAYOFF-B should claim, at most, the ecological synthesis:

> seasonal migration can be represented as sequential inference and signed
> phase correction toward a partly latent moving target, and observed
> phase-retention lambda can be decomposed into passive carry-over and active
> feedback only when the required components are separately identified.

The direct natural test remains prospective.
