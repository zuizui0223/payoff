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

## 3. Primitive readiness, opportunity and decision gain are not separately identified

Because

\[
h=GOg,
\]

any admissible triplet \((G,O,g)\) with the same product produces the same
mean and variance phase moments.

Therefore:

> **Phase tracking can identify effective enacted correction, but cannot by
> itself tell whether weak correction reflects incomplete physiological
> readiness, an ecological opportunity that is closing, or weak decision gain.**

The earlier phase-sense inverse should consequently be interpreted as
identifying \(K\) and \(h=GOg\), unless the primitive gates are independently
measured.

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
## 5. What separates readiness, opportunity and decision gain

Once \(h=GOg\) is identified, **two independent primitive quantities are
generally required to recover all three of \(G,O,g\)**.

One independent quantity is still useful, but it identifies only the product
of the other two. For example:

### Independent readiness measure

If \(G\) is independently measured,

\[
Og=\frac{h}{G}.
\]

The remaining opportunity and decision gain are still confounded.

### Independent opportunity measure

If \(O\) is independently measured,

\[
Gg=\frac{h}{O}.
\]

### Independent decision-gain calibration

If \(g\) is independently calibrated,

\[
GO=\frac{h}{g}.
\]

Full primitive separation follows when any two are independently known. For
example, if \(G\) and \(O\) are measured,

\[
\boxed{
g=\frac{h}{GO}.
}
\]

If \(G\) and \(g\) are known,

\[
\boxed{
O=\frac{h}{Gg}.
}
\]

If \(O\) and \(g\) are known,

\[
\boxed{
G=\frac{h}{Og}.
}
\]

Without this additional information, separate estimates of \(G,O,g\) are not
licensed.

## 6. Four perturbations target four different mechanisms

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

\[
O.
\]

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

Mule deer now provide the strongest same-system natural bridge. In a
predeclared temporally conservative Source Data analysis, March scaled IFBFat
precedes migration start in 62 animal-years and predicts standardized
migration-start timing in the primary animal-clustered analysis. The same
population independently supplies D2 signed speed/stopover correction and a
whole-route phase funnel.

This licenses **T3_CANDIDATE + D2 -> H1_CANDIDATE**, not H2. The year-fixed-
effect and rank-based readiness sensitivities are weaker, exact March capture
dates are unavailable, and the analysis does not show that readiness gates the
signed feedback slope.

Insect emergence systems still provide complementary developmental/readiness
evidence, but no current natural PAYOFF-B system jointly identifies
(G,O,K,g,phi,Q) or directly demonstrates H2 readiness-gated feedback.

The full primitive decomposition is therefore prospective.

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
