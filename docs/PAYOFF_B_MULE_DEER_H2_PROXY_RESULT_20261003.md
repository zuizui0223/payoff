# PAYOFF-B mule-deer H2 proxy moderation result

Date: **2026-10-03**  
Status: **post-freeze, preregistered-within-branch proxy test; frozen GEB V2 unchanged**

## Question

Does March scaled IFBFat, treated only as a physiological readiness proxy, modify the strength of signed phase-dependent correction during migration?

The test was frozen before outcome inspection. In the temporally safe subset the declared models were:

movement rate ~ centered DFP_Start + centered IFBFat + DFP_Start × IFBFat

and

stopover days ~ centered DFP_Start + centered IFBFat + DFP_Start × IFBFat.

Strong proxy support required both interactions to have the predicted sign and animal-cluster bootstrap intervals excluding zero.

## Movement rate

Interaction coefficient:

\[
\hat\beta_{DFP\times fat}=-0.0152,
\]

95% animal-cluster bootstrap CI:

\[
[-0.0542,+0.0219].
\]

The preregistered readiness-gating direction was positive. The result therefore does not support the predicted moderation. Within-year centering gives -0.0173 with CI [-0.0625,+0.0151].

## Stopover duration

Interaction coefficient:

\[
\hat\beta_{DFP\times fat}=+0.0481,
\]

95% animal-cluster bootstrap CI:

\[
[-0.1539,+0.2365].
\]

The preregistered readiness-gating direction was negative. The result again does not support the predicted moderation. Within-year centering gives +0.0414 with CI [-0.1505,+0.2541].

## Decision

Neither actuator passes the frozen criterion:

H2_PROXY_OUTCOME = NO_PROXY_SUPPORT

This leaves the mule-deer evidence at:

TIMER = T3_CANDIDATE
DECISION = D2
HYBRID = H1_CHANNEL_SEPARATION_CANDIDATE
H2_READINESS_GATED_FEEDBACK = NOT_SUPPORTED_BY_IFBFAT_PROXY

## Biological interpretation

The same population still shows a clean two-channel pattern: predeparture physiological condition is associated with migration-start timing, while signed ecological phase is associated with postdeparture speed and stopover. What is not supported is the stronger claim that animals with higher March IFBFat express a stronger signed feedback controller.

That negative result matters because it prevents the two clocks from collapsing back into one scalar state variable. The readiness-related variable and the route-wise correction signal can coexist without a detectable multiplicative interaction in this proxy test.

## Boundary

This does not prove that physiological readiness never gates feedback. IFBFat may be an imperfect proxy for G, the relevant gate may operate closer to a later checkpoint, and all actuator summaries are post-departure. Direct H2 requires a readiness measure at the decision stage or an experimental manipulation of readiness/opportunity.