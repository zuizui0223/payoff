# PAYOFF-B two-clock empirical discrimination contract

Date: **2026-10-03**  
Status: **prospective; frozen GEB V2 unchanged**

## Target

Separate:

1. developmental/physiological readiness \(G\);
2. phase information weight \(K\);
3. decision/controller gain \(g\).

Do not infer all three from a single timing response.

## Minimum data structure

For each focal decision interval collect:

- independent physiological/readiness state before the action;
- signed incoming ecological phase error;
- cue information available before the action;
- actuator choice or magnitude;
- downstream signed phase error;
- route/stage and environmental innovation.

## Primary model quantities

\[
u=Gg\hat e,
\]

\[
\lambda=\phi(1-GOgK),
\]

\[
P_{next}
=
\phi^2P[1-K(Gg)(2-Gg)]+Q.
\]

Mean and variance moments identify \(K\) and \(h=GOg\) only when \(\phi,Q\)
are independently supported.

## Required extra identification

To split \(G\) from \(g\), require at least one:

- direct physiological readiness measure;
- independent measure/manipulation of whether an ecological opportunity is
  still open;
- independent calibration of decision gain under full readiness and
  opportunity;
- within-individual contrasts across known readiness/opportunity states.

## Strong falsifiers

The hybrid two-clock interpretation is weakened if:

- physiological readiness has no relation to action availability or timing;
- signed phase error does not predict decision direction after readiness;
- information manipulations change only readiness but not decision response;
- decision-actuator constraints change readiness timing itself rather than the
  post-readiness correction channel;
- fitted \(G,K,g\) require circularly defining each quantity from the same
  response.

## Cross-taxon comparison rule

Do not encode taxon as clock type.

A bee can use decision control after emergence, and a bird can have a strong
developmental/circannual readiness programme before migration.

Clock architecture must be assigned from measured mechanism, not taxonomy.

## Current evidence status

- insect diapause/emergence literature: supports developmental/physiological
  timing mechanisms, but no current PAYOFF-B matched controller decomposition;
- mule deer: supports signed decision correction and phase funnel, but no
  independent readiness decomposition;
- migratory birds: endogenous/photoperiodic readiness is an established
  alternative/parallel timing mechanism, while stopover departure and pacing
  provide decision-control opportunities.

Therefore the direct two-clock decomposition remains prospective.
