# PAYOFF-B two-clock identification theorem

Date: **2026-10-03**  
Status: **prospective post-freeze identification result; frozen GEB V2 unchanged**

## 1. The two clock layers enter multiplicatively

Let

- \(G_t\in[0,1]\) be a developmental/physiological readiness or actuator gate;
- \(K_t\in[0,1]\) be the effective information weight for signed phase;
- \(g_t\ge0\) be decision gain once the action is available.

The correction is

\[
u_t
=
G_tO_tg_t\hat e_t.
\]

Define effective correction gain

\[
\boxed{
h_t=G_tO_tg_t.
}
\]

The route controller is therefore

\[
e_{t+1}
=
\phi_t(e_t-h_t\hat e_t)+w_t.
\]

This establishes an identification issue: readiness, remaining opportunity and
decision gain enter the observed trajectory as a product.

## 2. Mean and variance signatures identify information and effective correction

For the Gaussian checkpoint model with information weight \(K\),

\[
\boxed{
\lambda
=
\phi(1-hK)
}
\]

and

\[
\boxed{
\rho_V
=
\frac{P_{t+1}-Q}{P}
=
\phi^2[1-Kh(2-h)].
}
\]

Define

\[
d
=
1-\frac{\lambda}{\phi}
=
hK
\]

and

\[
v
=
\frac{P_{t+1}-Q}{\phi^2P}.
\]

Then

\[
v
=
1-2d+\frac{d^2}{K}.
\]

Hence, when \(d\ne0\),

\[
\boxed{
K
=
\frac{d^2}{v-1+2d}
}
\]

and

\[
\boxed{
h
=
\frac{d}{K}.
}
\]

With independent \(\phi\) and \(Q\), mean plus variance retention can therefore
separate information quality from **effective** correction strength.

## 3. Readiness and decision gain are not separately identified

Because

\[
h=Gg,
\]

every pair

\[
(G,g)
=
(G,h/G)
\]

with admissible \(G>0\) produces the same phase moments.

Therefore:

> **Mean and variance phase tracking cannot, by themselves, distinguish a
> weakly available strong controller from a fully available weak controller.**

This is the central two-clock identification boundary.

The earlier phase-sense inverse should consequently be interpreted as
identifying \(K\) and \(h=Gg\) unless \(G=1\) is independently justified.

## 4. Readiness, opportunity, information and decision gain are multiplicative complements

Because

\[
\lambda=\phi(1-GOgK),
\]

the active correction term is the product \(GOgK\), not a sum.

The exact local sensitivities are

\[
\frac{\partial\lambda}{\partial G}
=
-\phi OgK,
\]

\[
\frac{\partial\lambda}{\partial O}
=
-\phi GgK,
\]

\[
\frac{\partial\lambda}{\partial K}
=
-\phi GOg,
\]

and

\[
\frac{\partial\lambda}{\partial g}
=
-\phi GOK.
\]

Therefore better information has no phase-control effect if the organism is not
ready (\(G=0\)) or if the opportunity has already expired (\(O=0\)). Likewise,
readiness does not help when no ecologically useful action remains.

The mechanisms are **multiplicative complements**.

For small actor differences around a common baseline,

\[
\delta\lambda
\approx
(1-GOgK)\delta\phi
-
\phi OgK\,\delta G
-
\phi GgK\,\delta O
-
\phi GOK\,\delta g
-
\phi GOg\,\delta K.
\]

This is a local attribution, not an exact finite-change decomposition.
## 5. What separates the two clocks

One additional independent quantity is sufficient in the reduced model.

### Independent readiness measure

If \(G\) is measured from physiology, developmental stage, photoperiodic
readiness, endocrine state, or experimental gating,

\[
\boxed{
g=\frac{h}{G}.
}
\]

### Independent decision-gain calibration

If \(g\) is estimated under a condition where the actuator is fully available
or experimentally calibrated,

\[
\boxed{
G=\frac{h}{g}.
}
\]

Without such information, reporting separate \(G\) and \(g\) is not licensed.

## 6. Three perturbations target three different mechanisms

The cleanest empirical programme uses conceptually distinct perturbations.

### A. Timer/readiness perturbation

Manipulate a driver of physiological readiness while holding phase information
as comparable as possible.

Examples:
- photoperiod;
- diapause temperature history;
- endocrine/developmental state.

Primary target:

\[
G.
\]

### B. Opportunity perturbation

Change whether an otherwise possible action remains ecologically useful,
without changing readiness or cue reliability.

Examples:
- experimentally alter stopover availability;
- impose/remove a route barrier;
- alter the duration of a resource window.

Primary target:

[
O.
]

### C. Information perturbation

Change the reliability or availability of the phase cue without changing
physical actuator capacity.

Primary target:

\[
K.
\]

### D. Actuator perturbation

Change the cost or availability of speed, stopover, route or timing correction
after readiness.

Primary target:

\[
g
\quad\text{or an action-specific availability gate}.
\]

The three effects should not be inferred from one response variable by
relabeling coefficients.

## 7. Developmental timer versus decision controller: predicted signatures

### Developmental/physiological timer

Expected observations:
- event timing changes with accumulated or entraining conditions;
- a threshold/readiness state predicts event occurrence;
- once the focal transition occurs, timing of that transition is not corrected
  by later information;
- signed early/late error need not predict opposite actions.

### Inferential decision controller

Expected observations:
- signed incoming phase predicts action direction;
- cue quality changes response strength;
- early and late individuals take opposite corrective actions;
- repeated checkpoints can narrow the phase distribution.

### Hybrid organism

Both signatures appear, but at different stages.

A migrant can therefore have:
1. a circannual/photoperiodic readiness gate;
2. repeated information-dependent stopover and pacing decisions.

## 8. Actionability as a reduction of multiple gates

If actuator \(a\) has gate \(G_a\) and declared ecological importance
\(\omega_a\), one possible reduced actionability coordinate is

\[
r
=
\frac{
\sum_a\omega_aG_aO_a
}{
\sum_a\omega_a
}.
\]

This is **not** a universal definition of Paper-2 \(r\). It demonstrates how a
shrinking physiological/physical action space can generate the reduced
actionability object used by the information theorem.

Different reductions are appropriate when actions have nonlinear values or
substitutability.

## 9. Interaction consequence

Actor \(i\) has

\[
\lambda_i
=
\phi_i(1-G_iO_i g_iK_i).
\]

For a synchronized interacting pair under shared seasonal error \(m_t\),

\[
\boxed{
\Delta_{t+1}
=
(\lambda_1-\lambda_2)m_t.
}
\]

Thus mismatch can originate in any of three different clock/control
differences:

\[
G_1\ne G_2,
\qquad
K_1\ne K_2,
\qquad
g_1\ne g_2.
\]

The same observed interaction mismatch does not reveal which layer differs.

## 10. Empirical claim boundary

The current natural evidence does not jointly estimate \(G,K,g,\phi,Q\) in one
system.

Mule deer provide strong information about signed actuator correction and a
phase funnel, but no independent physiological readiness gate for the same
transition.

Insect emergence systems can provide developmental/readiness information, but
the current PAYOFF-B data stack does not estimate a matched signed decision
controller for the emergence event.

The full two-clock decomposition is therefore prospective.

## 11. Novelty boundary

Developmental thresholds, diapause physiology, photoperiodic clocks,
state-dependent decisions, Bayesian filtering and feedback control all have
substantial prior literatures.

The PAYOFF-B contribution is the identification synthesis:

> **physiological readiness and decision gain are biologically distinct clocks
> but are observationally confounded as an effective correction product unless
> one layer is independently measured or manipulated.**

This distinction prevents "biological clock" from becoming an uninterpretable
single latent parameter.
