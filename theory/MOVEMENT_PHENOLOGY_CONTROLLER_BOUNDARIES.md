# Movement–phenology controller boundaries: information, actuation, and endogeneity

Status: conceptual/theoretical synthesis for the empirical PAYOFF-B extension.

The cross-system evidence identifies three logically distinct requirements for phase locking.

## 1. Information

The migrant must have usable information about the environmental process it is trying to track.

Let \(P\) denote predictability of downstream environmental timing conditional on information available at the current location.

Low \(P\) limits the value of any otherwise capable behavioral controller.

Barnacle-geese evidence motivates this axis: phase precision is higher where spring anomalies propagate more predictably among stopovers.

## 2. Actuation

The migrant must be able to express the movement response implied by its phase error.

Write

\[
u_{\rm realized}(E,s)
=
G(s)\,u_{\rm desired}(E),
\]

where \(G(s)\) is control permeability.

Industrial disturbance can reduce \(G\) even if the route remains physically passable.

This axis is motivated by gas-field mule deer, which held up at development and allowed the green wave to pass.

## 3. Environmental exogeneity

The environment must be sufficiently independent of the animal for \(c_e\) to be treated as an input.

Let \(\chi\) denote environmental endogeneity: the strength with which animal use modifies the resource timing process.

For \(\chi\approx0\), an exogenous-wave controller is plausible.

For large \(\chi\), animal and environmental dynamics must be modeled jointly.

Yellowstone bison motivate this axis because grazing modifies vegetation phenology.

## A three-axis control space

The simplest controller framework therefore lives in

\[
(P,G,\chi).
\]

~~~text
high P, high G, low chi:
  classical phase locking / surfing is feasible

low P:
  information-limited tracking

low G:
  actuation-limited / barrier-induced controller failure

high chi:
  endogenous resource engineering; exogenous tracking model invalid
~~~

These failure modes should not be pooled.

## Interaction with movement strategy

The strategy taxonomy is:

~~~text
SURF      continuous controller
STEP      discrete stopover controller
JUMP      relocation between seasonal states
OVERTAKE  target phase changes systematically along route
ENGINEER  resource wave is endogenous
~~~

Strategy and control limits are separate dimensions.

For example:

- a goose can use STEP dynamics under high predictability;
- a deer can JUMP across a discontinuous phenology landscape;
- a surfer can fail because \(G\) falls near industrial infrastructure;
- an ENGINEER system can show large satellite mismatch without ecological failure.

## Macroecological prediction

The existence and strength of phase locking should be modeled conditionally:

\[
\kappa_{\rm observed}
=
f(P,G,\chi,\text{strategy},\text{cue coupling}).
\]

A null or weak \(\kappa\) has different meanings depending on the limiting axis.

This explains why a broad cross-species average can be uninformative even when strong controllers exist within particular ecological regimes.

## Relation to PAYOFF-B

PAYOFF-B1 provides an exact benchmark for fixed-rate movement under externally imposed anti-phase switching.

The macro extension now separates:

~~~text
fixed-rate optimum:
  what movement rate performs best?

feedback controller:
  how does movement respond to phase error?

controller feasibility:
  does the animal have information, actuation, and an exogenous target?

strategy:
  does the animal surf, step, jump, overtake, or engineer?
~~~

This hierarchy is the intended architecture of the empirical programme.
